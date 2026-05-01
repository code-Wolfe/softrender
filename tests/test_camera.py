import pytest
from src.linalg.vector import Vec3
from src.linalg.matrix import Mat4
from src.render.camera import Camera


def test_default_camera_view_matrix_is_identity():
    """A camera at the origin, looking down +Z with up=+Y, requires no
    transformation: world space already IS camera space."""
    cam = Camera(
        eye=Vec3(0, 0, 0),
        target=Vec3(0, 0, 1),  # any point on +Z axis works
        up=Vec3(0, 1, 0),
    )
    view = cam.view_matrix()

    # Compare element-by-element against the identity matrix.
    expected = Mat4.identity()
    for i in range(4):
        for j in range(4):
            assert view.m[i][j] == pytest.approx(expected.m[i][j])


def test_camera_sees_itself_at_origin():
    """No matter where the camera is placed, applying its view matrix to
    its own eye position must give (0, 0, 0). The camera is always at the
    origin of its own coordinate system."""
    eye = Vec3(5, 2, -10)
    cam = Camera(
        eye=eye,
        target=Vec3(0, 0, 0),
        up=Vec3(0, 1, 0),
    )
    view = cam.view_matrix()

    result = view.transform(eye)
    assert result.x == pytest.approx(0.0, abs=1e-9)
    assert result.y == pytest.approx(0.0, abs=1e-9)
    assert result.z == pytest.approx(0.0, abs=1e-9)


def test_point_in_front_of_translated_camera():
    """Camera at world (0, 0, -5) looking at origin, up=+Y.
    A point at the world origin sits 5 units directly in front of the
    camera, so in camera space it should be at (0, 0, 5)."""
    cam = Camera(
        eye=Vec3(0, 0, -5),
        target=Vec3(0, 0, 0),
        up=Vec3(0, 1, 0),
    )
    view = cam.view_matrix()

    result = view.transform(Vec3(0, 0, 0))
    assert result.x == pytest.approx(0.0, abs=1e-9)
    assert result.y == pytest.approx(0.0, abs=1e-9)
    assert result.z == pytest.approx(5.0, abs=1e-9)


def test_point_to_the_side_of_rotated_camera():
    """Camera at world (5, 0, 0) looking at the origin, up=+Y.
    A point at world (5, 0, 3) is 3 units to the camera's right
    (we worked this out by hand). In camera space: (3, 0, 0)."""
    cam = Camera(
        eye=Vec3(5, 0, 0),
        target=Vec3(0, 0, 0),
        up=Vec3(0, 1, 0),
    )
    view = cam.view_matrix()

    result = view.transform(Vec3(5, 0, 3))
    assert result.x == pytest.approx(3.0, abs=1e-9)
    assert result.y == pytest.approx(0.0, abs=1e-9)
    assert result.z == pytest.approx(0.0, abs=1e-9)