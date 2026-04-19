from __future__ import annotations

import json
from pathlib import Path

from .models import Hold, SceneSpec


def load_scene_spec(path: str | Path) -> SceneSpec:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    holds = [Hold(**item) for item in payload["holds"]]
    return SceneSpec(
        image_path=Path(payload["image_path"]),
        holds=holds,
        start_hold=payload["start_hold"],
        target_hold=payload["target_hold"],
        frame_count=payload.get("frame_count", 144),
        fps=payload.get("fps", 24),
        wall_height=payload.get("wall_height", 720),
        wall_width=payload.get("wall_width", 512),
    )
