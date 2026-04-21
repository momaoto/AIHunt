import requests

urls = [
    "https://pub-3c0608dd10d94739877d2c061fd18e43.r2.dev?list-type=2",
    "https://pub-b1bb8623cf5c44e8848b47e4b9e5580b.r2.dev?list-type=2",
    "https://pub-f43d6d328c0f424eb93a1100f66ace4d.r2.dev?list-type=2",
]

for url in urls:
    print(f"requesting: {url}", flush=True)
    try:
        r = requests.get(url, timeout=10)
        print(f"status: {r.status_code}", flush=True)
        print(r.text[:1000], flush=True)
    except Exception as e:
        print(f"error: {type(e).__name__}: {e}", flush=True)
    print("-" * 80, flush=True)
