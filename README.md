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
| `W` / `S` | Move camera closer / farther |
| `←` / `→` | Rotate around Y axis |
| `↑` / `↓` | Rotate around X axis |
| `Q` / `E` | Rotate around Z axis |

## Project Structure

```
src/
  linalg/    # Vec3, Mat4 — vectors, matrices, transforms
  geometry/  # Mesh, primitive shapes (cube, ...)
  camera/    # Camera model
  render/    # Perspective projection, wireframe drawing
main.py      # Entry point
```

## Getting Started

```bash
pip install -r requirements.txt
python main.py
```

Requires Python 3.10+ and pygame 2.x.
