from __future__ import annotations

from .models import ContactState, SceneSpec


def _route_from_scene(scene: SceneSpec) -> list[str]:
    hold_ids = [hold.id for hold in scene.holds]
    if scene.start_hold not in hold_ids:
        raise ValueError(f"Unknown start_hold: {scene.start_hold}")
    if scene.target_hold not in hold_ids:
        raise ValueError(f"Unknown target_hold: {scene.target_hold}")

    ordered = sorted(scene.holds, key=lambda hold: hold.y, reverse=True)
    route = [hold.id for hold in ordered]
    if scene.start_hold in route:
        route.remove(scene.start_hold)
    if scene.target_hold in route:
        route.remove(scene.target_hold)
    return [scene.start_hold, *route, scene.target_hold]


def plan_contacts(scene: SceneSpec) -> list[ContactState]:
    route = _route_from_scene(scene)
    frames_per_step = max(scene.frame_count // max(len(route), 1), 1)
    contacts: list[ContactState] = []

    left_hand = scene.start_hold
    right_hand = scene.start_hold
    left_foot = scene.start_hold
    right_foot = scene.start_hold

    for step, hold_id in enumerate(route):
        if step % 2 == 0:
            left_hand = hold_id
        else:
            right_hand = hold_id

        left_foot = route[max(step - 1, 0)]
        right_foot = route[max(step - 2, 0)]

        for local_index in range(frames_per_step):
            frame_index = step * frames_per_step + local_index
            if frame_index >= scene.frame_count:
                break
            contacts.append(
                ContactState(
                    frame_index=frame_index,
                    left_hand=left_hand,
                    right_hand=right_hand,
                    left_foot=left_foot,
                    right_foot=right_foot,
                )
            )

    if not contacts:
        return contacts

    last = contacts[-1]
    while len(contacts) < scene.frame_count:
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
