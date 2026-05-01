# 3D Engine

A software 3D renderer built from scratch in Python — no GPU, no game engine, no 3D library. Everything from matrix math to perspective projection is implemented by hand.

## Features

- Custom linear algebra library (`Vec3`, `Mat4`) with no numpy dependency
- Perspective projection with configurable focal length
- Affine transforms: translation, rotation (X/Y/Z axes)
- Wireframe mesh rendering via pygame
- Interactive camera controls at 60 fps

## Controls

| Key | Action |
|-----|--------|
| `W` / `S` | Move forward / backward |
| `A` / `D` | Strafe left / right |
| `Space` / `Shift` | Move up / down |
| `←` / `→` | Look left / right (yaw) |
| `↑` / `↓` | Look up / down (pitch) |

A HUD in the top-left shows current eye position, yaw, and pitch.

## Project Structure

```
src/
  linalg/    # Vec3, Mat4 — vectors, matrices, transforms
  geometry/  # Mesh, primitive shapes (cube, ...)
  render/    # Camera, perspective projection, wireframe drawing
main.py      # Entry point
```

## Getting Started

```bash
pip install -r requirements.txt
python main.py
```

Requires Python 3.10+ and pygame 2.x.
