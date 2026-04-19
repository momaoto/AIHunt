from __future__ import annotations

import argparse

from .animator import animate
from .io import load_scene_spec
from .planner import plan_contacts
from .renderer import render_video


def main() -> None:
    parser = argparse.ArgumentParser(description="AIHunt Phase 1 demo pipeline.")
    parser.add_argument("--scene", required=True, help="Path to a JSON scene spec.")
    parser.add_argument("--output", required=True, help="Path to the output mp4 file.")
    args = parser.parse_args()

    scene = load_scene_spec(args.scene)
    contacts = plan_contacts(scene)
    frames = animate(scene, contacts)
    output = render_video(scene, frames, args.output)
    print(output)


if __name__ == "__main__":
    main()
