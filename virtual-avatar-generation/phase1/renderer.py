from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .animator import SkeletonFrame
from .models import SceneSpec


def render_video(scene: SceneSpec, frames: list[SkeletonFrame], output_path: str | Path) -> Path:
    background = cv2.imread(str(scene.image_path))
    if background is None:
        background = np.full((720, 512, 3), 235, dtype=np.uint8)
        cv2.putText(
            background,
            "Synthetic wall background",
            (24, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (60, 60, 60),
            2,
        )

    height, width = background.shape[:2]
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), scene.fps, (width, height))

    hold_lookup = {hold.id: hold for hold in scene.holds}
    limbs = [
        ("head", "hip"),
        ("hip", "left_hand"),
        ("hip", "right_hand"),
        ("hip", "left_foot"),
        ("hip", "right_foot"),
    ]

    for skeleton in frames:
        frame = background.copy()
        for hold in scene.holds:
            cv2.circle(frame, (int(hold.x), int(hold.y)), int(hold.radius), (255, 180, 0), 2)
            cv2.putText(frame, hold.id, (int(hold.x) + 6, int(hold.y) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 180, 0), 1)
        for start_name, end_name in limbs:
            start = getattr(skeleton, start_name)
            end = getattr(skeleton, end_name)
            cv2.line(frame, (int(start[0]), int(start[1])), (int(end[0]), int(end[1])), (20, 220, 20), 3)
        for point in [skeleton.head, skeleton.hip, skeleton.left_hand, skeleton.right_hand, skeleton.left_foot, skeleton.right_foot]:
            cv2.circle(frame, (int(point[0]), int(point[1])), 6, (20, 220, 20), -1)
        writer.write(frame)

    writer.release()
    return output
