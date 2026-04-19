from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .models import SceneSpec, SkeletonFrame


def _fallback_background(scene: SceneSpec) -> np.ndarray:
    canvas = np.full((scene.wall_height, scene.wall_width, 3), 238, dtype=np.uint8)
    cv2.putText(
        canvas,
        "AIHunt Phase 1",
        (20, 36),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (70, 70, 70),
        2,
    )
    return canvas


def render_video(scene: SceneSpec, frames: list[SkeletonFrame], output_path: str | Path) -> Path:
    background = cv2.imread(str(scene.image_path))
    if background is None:
        background = _fallback_background(scene)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    height, width = background.shape[:2]
    writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), scene.fps, (width, height))

    limb_pairs = [
        ("head", "neck"),
        ("neck", "hip"),
        ("neck", "left_hand"),
        ("neck", "right_hand"),
        ("hip", "left_foot"),
        ("hip", "right_foot"),
    ]

    for skeleton in frames:
        frame = background.copy()
        for hold in scene.holds:
            center = (int(hold.x), int(hold.y))
            cv2.circle(frame, center, int(hold.radius), (0, 170, 255), 2)
            cv2.putText(frame, hold.id, (center[0] + 6, center[1] - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 170, 255), 1)

        for start_name, end_name in limb_pairs:
            start = getattr(skeleton, start_name)
            end = getattr(skeleton, end_name)
            cv2.line(frame, (int(start[0]), int(start[1])), (int(end[0]), int(end[1])), (30, 220, 30), 3)

        for point in [
            skeleton.head,
            skeleton.neck,
            skeleton.hip,
            skeleton.left_hand,
            skeleton.right_hand,
            skeleton.left_foot,
            skeleton.right_foot,
        ]:
            cv2.circle(frame, (int(point[0]), int(point[1])), 5, (30, 220, 30), -1)

        writer.write(frame)

    writer.release()
    return output
