import pytest
from src.linalg.vector import Vec3
from src.render.renderer import face_normal


def test_face_normal_ccw_points_up():
    """A triangle wound CCW in the xy-plane has a +z normal."""
    v0 = Vec3(0, 0, 0)
    v1 = Vec3(1, 0, 0)
    v2 = Vec3(0, 1, 0)
    n = face_normal(v0, v1, v2)
    assert n.z > 0


def test_face_normal_reverses_with_winding():
    """Reversing the winding flips the normal to the opposite direction."""
    v0 = Vec3(0, 0, 0)
    v1 = Vec3(1, 0, 0)
    v2 = Vec3(0, 1, 0)
    ccw = face_normal(v0, v1, v2)
    cw = face_normal(v0, v2, v1)  # same triangle, two indices swapped
    assert ccw.z > 0
    assert cw.z < 0