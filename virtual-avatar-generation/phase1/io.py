from __future__ import annotations

import json
from pathlib import Path

from .models import Hold, SceneSpec


def load_scene_spec(path: str | Path) -> SceneSpec:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    holds = [Hold(**item) for item in raw["holds"]]
    return SceneSpec(
        image_path=Path(raw["image_path"]),
        holds=holds,
        start_hold=raw["start_hold"],
        target_hold=raw["target_hold"],
        frame_count=raw.get("frame_count", 120),
        fps=raw.get("fps", 24),
    )

