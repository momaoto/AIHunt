from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Hold:
    id: str
    x: float
    y: float
    radius: float = 24.0
    role: str = "any"


@dataclass(frozen=True)
class SceneSpec:
    image_path: Path
    holds: list[Hold]
    start_hold: str
    target_hold: str
    frame_count: int = 144
    fps: int = 24
    wall_height: int = 720
    wall_width: int = 512


@dataclass(frozen=True)
class ContactState:
    frame_index: int
    left_hand: str
    right_hand: str
    left_foot: str
    right_foot: str


@dataclass(frozen=True)
class SkeletonFrame:
    head: tuple[float, float]
    neck: tuple[float, float]
    hip: tuple[float, float]
    left_hand: tuple[float, float]
    right_hand: tuple[float, float]
    left_foot: tuple[float, float]
    right_foot: tuple[float, float]
