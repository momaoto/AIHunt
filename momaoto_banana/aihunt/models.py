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

    def hold_lookup(self) -> dict[str, Hold]:
        return {hold.id: hold for hold in self.holds}

    def validate(self) -> None:
        if self.frame_count <= 0:
            raise ValueError("frame_count must be positive")
        if self.fps <= 0:
            raise ValueError("fps must be positive")
        if self.wall_height <= 0 or self.wall_width <= 0:
            raise ValueError("wall dimensions must be positive")
        if not self.holds:
            raise ValueError("scene must contain at least one hold")

        hold_lookup = self.hold_lookup()
        if len(hold_lookup) != len(self.holds):
            raise ValueError("hold ids must be unique")
        if self.start_hold not in hold_lookup:
            raise ValueError(f"Unknown start_hold: {self.start_hold}")
        if self.target_hold not in hold_lookup:
            raise ValueError(f"Unknown target_hold: {self.target_hold}")

        for hold in self.holds:
            if hold.radius <= 0:
                raise ValueError(f"hold {hold.id} must have positive radius")
            if not (0 <= hold.x <= self.wall_width):
                raise ValueError(f"hold {hold.id} x is outside wall width")
            if not (0 <= hold.y <= self.wall_height):
                raise ValueError(f"hold {hold.id} y is outside wall height")


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
