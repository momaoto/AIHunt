import argparse
import concurrent.futures
import os
import sys
import threading
import zipfile
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import requests


LIST_FILES = {
    "context": "sabr-climb/context_urls.txt",
    "inpainted": "sabr-climb/inpainted_urls.txt",
    "training": "sabr-climb/training-data-truncated_urls.txt",
    "checkpoint": "sabr-climb/sabr_climb_checkpoint.txt",
}


def read_urls(zip_path: Path, list_name: str) -> list[str]:
    inner_path = LIST_FILES[list_name]
    with zipfile.ZipFile(zip_path) as zf:
        lines = zf.read(inner_path).decode("utf-8", errors="replace").splitlines()
    return [line.strip() for line in lines if line.strip()]


def build_target_path(output_root: Path, url: str) -> Path:
    parsed = urlparse(url)
    relative = parsed.path.lstrip("/")
    return output_root / parsed.netloc / relative


def download_one(
    session: requests.Session,
    url: str,
    output_root: Path,
    force: bool,
    timeout: int,
) -> tuple[str, str]:
    target = build_target_path(output_root, url)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and not force:
        return "skip", str(target)

    with session.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        tmp = target.with_suffix(target.suffix + ".part")
        with open(tmp, "wb") as fh:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)
        os.replace(tmp, target)
    return "ok", str(target)


def batched_urls(all_urls: list[str], limit: int | None) -> list[str]:
    if limit is None or limit <= 0:
        return all_urls
    return all_urls[:limit]


def print_summary(name: str, urls: Iterable[str]) -> None:
    urls = list(urls)
    print(f"{name}: {len(urls)} urls")
    if urls:
        print(f"first: {urls[0]}")
        print(f"last:  {urls[-1]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Download SABR-Climb assets from sabr-climb.zip URL lists.")
    parser.add_argument(
        "--zip-path",
        default="sabr-climb.zip",
        help="Path to the zip file containing the URL lists.",
    )
    parser.add_argument(
        "--types",
        nargs="+",
        choices=list(LIST_FILES.keys()) + ["all"],
        default=["checkpoint"],
        help="Which asset groups to download. Default downloads only the checkpoint.",
    )
    parser.add_argument(
        "--output-dir",
        default="downloads",
        help="Root directory for downloaded files.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel downloads.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional cap per asset group for quick testing. 0 means no cap.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download files even if they already exist.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Per-request timeout in seconds.",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Only print counts and sample URLs without downloading.",
    )
    args = parser.parse_args()

    zip_path = Path(args.zip_path)
    output_dir = Path(args.output_dir)
    selected = list(LIST_FILES.keys()) if "all" in args.types else args.types

    all_jobs: list[tuple[str, str]] = []
    for name in selected:
        urls = batched_urls(read_urls(zip_path, name), args.limit)
        print_summary(name, urls)
        all_jobs.extend((name, url) for url in urls)

    if args.print_only:
        return 0

    total = len(all_jobs)
    if total == 0:
        print("No URLs selected.")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()
    completed = 0
    ok = 0
    skipped = 0
    failed = 0

    def worker(job: tuple[str, str]) -> tuple[str, str, str]:
        group, url = job
        with requests.Session() as session:
            session.headers.update({"User-Agent": "sabr-climb-downloader/1.0"})
            status, path = download_one(session, url, output_dir, args.force, args.timeout)
        return group, status, path

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        future_map = {pool.submit(worker, job): job for job in all_jobs}
        for future in concurrent.futures.as_completed(future_map):
            group, url = future_map[future]
            try:
                _, status, path = future.result()
                with lock:
                    completed += 1
                    if status == "ok":
                        ok += 1
                    else:
                        skipped += 1
                    print(f"[{completed}/{total}] {status.upper():4} {group}: {path}", flush=True)
            except Exception as exc:
                with lock:
                    completed += 1
                    failed += 1
                    print(f"[{completed}/{total}] FAIL {group}: {url} -> {exc}", flush=True)

    print(f"done: ok={ok} skipped={skipped} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
