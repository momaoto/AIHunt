from __future__ import annotations

from .models import ContactState, SceneSpec


def _sorted_route(scene: SceneSpec) -> list[str]:
    hold_lookup = scene.hold_lookup()
    start = hold_lookup[scene.start_hold]
    target = hold_lookup[scene.target_hold]

    candidates = [
        hold
        for hold in scene.holds
        if hold.id not in {scene.start_hold, scene.target_hold}
        and target.y <= hold.y <= start.y
    ]
    candidates.sort(key=lambda hold: (-hold.y, abs(hold.x - start.x)))
    return [scene.start_hold, *[hold.id for hold in candidates], scene.target_hold]


def _contact_for_step(route: list[str], step: int) -> tuple[str, str, str, str]:
    left_hand = route[min(step, len(route) - 1)]
    right_hand = route[min(max(step - 1, 0), len(route) - 1)]
    left_foot = route[min(max(step - 2, 0), len(route) - 1)]
    right_foot = route[min(max(step - 3, 0), len(route) - 1)]
    return left_hand, right_hand, left_foot, right_foot


def plan_contacts(scene: SceneSpec) -> list[ContactState]:
    route = _sorted_route(scene)
    step_count = max(len(route), 2)
    frames_per_step = max(scene.frame_count // (step_count - 1), 1)
    contacts: list[ContactState] = []

    for frame_index in range(scene.frame_count):
        step = min(frame_index // frames_per_step, step_count - 1)
        left_hand, right_hand, left_foot, right_foot = _contact_for_step(route, step)
        contacts.append(
            ContactState(
                frame_index=frame_index,
                left_hand=left_hand,
                right_hand=right_hand,
                left_foot=left_foot,
                right_foot=right_foot,
            )
        )

    return contacts
