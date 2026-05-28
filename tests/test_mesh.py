import pytest
from src.geometry.shapes import cube
from src.geometry.mesh import Mesh
from src.linalg.vector import Vec3


def test_cube_has_twelve_faces():
    """A cube is 6 square sides, each split into 2 triangles."""
    mesh = cube()
    assert len(mesh.faces) == 12


# Build the cube once and turn its 12 faces into test cases, so each
# triangle shows up as its own pass/fail line under `pytest -v`.
_cube = cube()


@pytest.mark.parametrize("face_index,triangle", list(enumerate(_cube.faces)))
def test_face_normal_points_outward(face_index, triangle):
    """
    Each triangle must be wound counter-clockwise as seen from outside
    the cube. For a CCW triangle, (p1 - p0) x (p2 - p0) points outward.

    The cube is centered at the origin, so 'outward' means the normal
    points the same way as the vector from the cube center (origin) to
    the triangle's centroid -- i.e. their dot product is positive.
    """
    i0, i1, i2 = triangle
    p0 = _cube.vertices[i0]
    p1 = _cube.vertices[i1]
    p2 = _cube.vertices[i2]

    normal = (p1 - p0).cross(p2 - p0)
    centroid = (p0 + p1 + p2) * (1 / 3)

    # cube center is the origin, so (centroid - center) == centroid
    outward_dot = normal.dot(centroid)

    assert outward_dot > 0, (
        f"face {face_index} {triangle} is wound inward "
        f"(normal . centroid = {outward_dot}); reverse two of its indices"
    )