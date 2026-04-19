# AIHunt

AIHunt is a fresh implementation track for climbing-scene-to-avatar generation.

The legacy paper code lives under [virtual-avatar-generation](./virtual-avatar-generation) and is treated as reference material only. New development happens in the `aihunt/` package.

## Phase 1

Phase 1 builds a controllable MVP:

1. load a static climbing wall scene specification
2. plan a simple route/contact sequence
3. synthesize a lightweight skeleton animation
4. render a demo video

This is intentionally simple. The goal is to lock down the data model and module boundaries before adding learned components.

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

This command is not assumed to work yet on your machine; the code is being staged before environment setup.
