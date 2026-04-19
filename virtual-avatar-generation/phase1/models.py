from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Hold:
    id: str
    x: float
    y: float
    radius: float = 24.0


@dataclass(frozen=True)
class SceneSpec:
    image_path: Path
    holds: list[Hold]
    start_hold: str
    target_hold: str
    frame_count: int = 120
    fps: int = 24


@dataclass(frozen=True)
class ContactState:
    frame_index: int
    left_hand: str
    right_hand: str
    left_foot: str
    right_foot: str

