from src.linalg.vector import Vec3
from src.geometry.mesh import Mesh

def cube(size: float = 1.0) -> Mesh:
    """Create a cube centered at the origin with the given side length."""
    s = size /2 #vertices go from -s to +s

    # 8 vertices — every combination of (±s, ±s, ±s)
    vertices = [
        Vec3(-s, -s, -s),  # 0: back-bottom-left
        Vec3( s, -s, -s),  # 1: back-bottom-right
        Vec3( s,  s, -s),  # 2: back-top-right
        Vec3(-s,  s, -s),  # 3: back-top-left
        Vec3(-s, -s,  s),  # 4: front-bottom-left
        Vec3( s, -s,  s),  # 5: front-bottom-right
        Vec3( s,  s,  s),  # 6: front-top-right
        Vec3(-s,  s,  s),  # 7: front-top-left
    ]

    # 12 edges — 4 on the back face, 4 on the front face, 4 connecting them
    edges = [
        # Back face (z = -s)
        (0, 1), (1, 2), (2, 3), (3, 0),
        # Front face (z = +s)
        (4, 5), (5, 6), (6, 7), (7, 4),
        # Connecting edges (front to back)
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]

    # 12 triangular faces — 2 per cube side.
    # Each triple is wound counter-clockwise as seen from OUTSIDE the cube,
    # so (p1-p0) x (p2-p0) points outward. Both triangles of a side fan
    # from the same first corner, so they share that side's winding.
    faces = [
        # Front face (z = +s), outward normal +z
        (4, 5, 6), (4, 6, 7),
        # Back face (z = -s), outward normal -z
        (1, 0, 3), (1, 3, 2),
        # Right face (x = +s), outward normal +x
        (1, 2, 6), (1, 6, 5),
        # Left face (x = -s), outward normal -x
        (0, 4, 7), (0, 7, 3),
        # Top face (y = +s), outward normal +y
        (3, 7, 6), (3, 6, 2),
        # Bottom face (y = -s), outward normal -y
        (0, 1, 5), (0, 5, 4),
    ]

    return Mesh(vertices, edges, faces)