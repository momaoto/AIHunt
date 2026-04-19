from __future__ import annotations

from .models import ContactState, SceneSpec, SkeletonFrame


def animate(scene: SceneSpec, contacts: list[ContactState]) -> list[SkeletonFrame]:
    hold_lookup = {hold.id: hold for hold in scene.holds}
    frames: list[SkeletonFrame] = []

    for contact in contacts:
        lh = hold_lookup[contact.left_hand]
        rh = hold_lookup[contact.right_hand]
        lf = hold_lookup[contact.left_foot]
        rf = hold_lookup[contact.right_foot]

        hip_x = (lh.x + rh.x + lf.x + rf.x) / 4.0
        hip_y = (lh.y + rh.y + lf.y + rf.y) / 4.0 + 48.0
        neck = (hip_x, hip_y - 48.0)
        head = (hip_x, hip_y - 84.0)

        frames.append(
            SkeletonFrame(
                head=head,
                neck=neck,
                hip=(hip_x, hip_y),
                left_hand=(lh.x, lh.y),
                right_hand=(rh.x, rh.y),
                left_foot=(lf.x, lf.y),
                right_foot=(rf.x, rf.y),
            )
        )
    return frames
