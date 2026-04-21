from __future__ import annotations

from .models import ContactState, SceneSpec, SkeletonFrame


def _lerp(start: tuple[float, float], end: tuple[float, float], alpha: float) -> tuple[float, float]:
    return (
        start[0] + (end[0] - start[0]) * alpha,
        start[1] + (end[1] - start[1]) * alpha,
    )


def _target_pose(scene: SceneSpec, contact: ContactState) -> SkeletonFrame:
    hold_lookup = scene.hold_lookup()
    lh = hold_lookup[contact.left_hand]
    rh = hold_lookup[contact.right_hand]
    lf = hold_lookup[contact.left_foot]
    rf = hold_lookup[contact.right_foot]

    shoulder_x = (lh.x + rh.x) / 2.0
    hip_x = (lh.x + rh.x + lf.x + rf.x) / 4.0
    hip_y = max((lf.y + rf.y) / 2.0 - 70.0, 80.0)
    neck = ((shoulder_x + hip_x) / 2.0, hip_y - 48.0)
    head = (neck[0], neck[1] - 36.0)

    return SkeletonFrame(
        head=head,
        neck=neck,
        hip=(hip_x, hip_y),
        left_hand=(lh.x, lh.y),
        right_hand=(rh.x, rh.y),
        left_foot=(lf.x, lf.y),
        right_foot=(rf.x, rf.y),
    )


def _smooth(previous: SkeletonFrame | None, current: SkeletonFrame, alpha: float = 0.35) -> SkeletonFrame:
    if previous is None:
        return current
    return SkeletonFrame(
        head=_lerp(previous.head, current.head, alpha),
        neck=_lerp(previous.neck, current.neck, alpha),
        hip=_lerp(previous.hip, current.hip, alpha),
        left_hand=_lerp(previous.left_hand, current.left_hand, alpha),
        right_hand=_lerp(previous.right_hand, current.right_hand, alpha),
        left_foot=_lerp(previous.left_foot, current.left_foot, alpha),
        right_foot=_lerp(previous.right_foot, current.right_foot, alpha),
    )


def animate(scene: SceneSpec, contacts: list[ContactState]) -> list[SkeletonFrame]:
    frames: list[SkeletonFrame] = []
    previous: SkeletonFrame | None = None

    for contact in contacts:
        target = _target_pose(scene, contact)
        current = _smooth(previous, target)
        frames.append(current)
        previous = current

    return frames
