# Phase 1 Design

## Goal

Given a static climbing wall image and a list of holds, produce a watchable climbing animation.

## Boundaries

Phase 1 does not try to solve:

- automatic hold segmentation
- realistic SMPL motion generation
- scene-conditioned diffusion
- video refinement

Phase 1 does define the interfaces that later phases will reuse.

## Core Types

- `SceneSpec`: wall image path, holds, route endpoints, timing
- `Hold`: hold id and 2D coordinates
- `ContactState`: which hold each limb is attached to at a frame
- `SkeletonFrame`: 2D joints for rendering

## Phase Progression

### Phase 1

- heuristic contact planner
- lightweight 2D skeleton animation
- OpenCV renderer

### Phase 2

- hold detection / route extraction
- dataset builder
- contact supervision and motion examples

### Phase 3

- learned route planner
- learned motion generator
- SMPL or mesh rendering
