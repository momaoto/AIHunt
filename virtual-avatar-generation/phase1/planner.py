from __future__ import annotations

from .models import ContactState, SceneSpec


def plan_contacts(scene: SceneSpec) -> list[ContactState]:
    """Produce a simple contact schedule that future learned planners can replace."""
    hold_ids = [hold.id for hold in scene.holds]
    if scene.start_hold not in hold_ids:
        raise ValueError(f"Unknown start_hold: {scene.start_hold}")
    if scene.target_hold not in hold_ids:
        raise ValueError(f"Unknown target_hold: {scene.target_hold}")

    middle = [hold_id for hold_id in hold_ids if hold_id not in {scene.start_hold, scene.target_hold}]
    route = [scene.start_hold, *middle, scene.target_hold]
    frames_per_step = max(scene.frame_count // max(len(route), 1), 1)

    contacts: list[ContactState] = []
    current_left_hand = scene.start_hold
    current_right_hand = scene.start_hold
    current_left_foot = scene.start_hold
    current_right_foot = scene.start_hold

    for step, hold_id in enumerate(route):
        current_left_hand = hold_id
        current_right_hand = hold_id if step % 2 else current_right_hand
        current_left_foot = route[max(step - 1, 0)]
        current_right_foot = route[max(step - 2, 0)]
        for offset in range(frames_per_step):
            frame_index = step * frames_per_step + offset
            if frame_index >= scene.frame_count:
                break
            contacts.append(
                ContactState(
                    frame_index=frame_index,
                    left_hand=current_left_hand,
                    right_hand=current_right_hand,
                    left_foot=current_left_foot,
                    right_foot=current_right_foot,
                )
            )

    if not contacts:
        return []
    while len(contacts) < scene.frame_count:
        last = contacts[-1]
        contacts.append(
            ContactState(
                frame_index=len(contacts),
                left_hand=last.left_hand,
                right_hand=last.right_hand,
                left_foot=last.left_foot,
                right_foot=last.right_foot,
            )
        )
    return contacts

