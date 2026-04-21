# AIHunt

AIHunt is a fresh implementation track for climbing-scene-to-avatar generation.

The legacy paper code lives under [../virtual-avatar-generation](../virtual-avatar-generation) and is treated as reference material only. New development happens inside this `momaoto_banana/` project.

## Phase 1

Phase 1 builds a controllable MVP:

1. load a static climbing wall scene specification
2. plan a simple route/contact sequence
3. synthesize a lightweight skeleton animation
4. render a demo video

This stage is intentionally simple. The goal is to lock down the data model and module boundaries before adding learned components.

## Current Scope

- validated JSON scene input
- heuristic upward route planner
- smoothed 2D skeleton animation
- OpenCV video rendering with synthetic fallback background

## Layout

```text
aihunt/
  cli.py
  models.py
  io.py
  planner.py
  animator.py
  renderer.py
examples/
  scene_spec.json
docs/
  phase1.md
```

## Intended Usage

```bash
python -m aihunt.cli --scene examples/scene_spec.json --output outputs/demo.mp4
```

## Next Phase 1 Tasks

- replace the planner with hold graph search
- allow manual route annotations
- improve body proportions and contact timing
- add tests for scene loading and route validity
