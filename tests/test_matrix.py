import math
import pytest
from src.linalg.vector import Vec3
from src.linalg.matrix import Mat4

def test_identity_leaves_vector_unchanged():
    v = Vec3(1,2,3)
    result = Mat4.identity().transform(v)
    assert result.x == 1
    assert result.y == 2
    assert result.z == 3

def test_identity_times_identity_is_identity():
    result = Mat4.identity() @ Mat4.identity()
    expected = Mat4.identity()
    for i in range(4):
        for j in range(4):
            assert result.m[i][j] == expected.m[i][j]

def test_scale_x_by_2():

    scale_x = Mat4([
        [2, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    v = Vec3(3, 4, 5)
    result = scale_x.transform(v)
    assert result.x == 6
    assert result.y == 4
    assert result.z == 5

def test_matrix_multi_non_commutative():
    test_x = Mat4([
        [2, 3, 1, 4],
        [3, 1, 5, 1],
        [4, 1, 1, 1],
        [1, 2, 3, 1],
    ])

    test_y = Mat4([
        [6, 6, 6, 6],
        [6, 1, 6, 6],
        [6, 6, 1, 6],
        [6, 6, 6, 1],
    ])

    result1 = test_x @ test_y
    result2 = test_y @ test_x

    assert any(
        result1.m[i][j] != result2.m[i][j]
        for i in range(4) for j in range(4)
    )


def test_translation_moves_a_point():
    result = Mat4.translation(10,20,30).transform(Vec3(1,2,3))
    assert result.x == 11
    assert result.y == 22
    assert result.z == 33

def test_translation_by_zero():
    result = Mat4.translation(0,0,0).transform(Vec3(0,1,2))
    assert result.x == 0
    assert result.y == 1
    assert result.z == 2

def test_scale_increases_proper_component():
    result = Mat4.scale(2,1,1).transform(Vec3(3,4,5))
    assert result.x == 6
    assert result.y == 4
    assert result.z == 5


def test_rotating_90deg_around_z_turns_x_into_y():
    rotated = Mat4.rotation_z(math.pi / 2).transform(Vec3(1, 0, 0))
    assert rotated.x == pytest.approx(0)
    assert rotated.y == pytest.approx(1)
    assert rotated.z == pytest.approx(0)

def test_rotate_full_turn_is_identity():
    # Rotating any vector by 2π (360°) should return the original vector
    v = Vec3(1, 2, 3)
    rotated = Mat4.rotation_y(2 * math.pi).transform(v)
    assert rotated.x == pytest.approx(1)
    assert rotated.y == pytest.approx(2)
    assert rotated.z == pytest.approx(3)

def test_rotate_by_zero_is_identity():
    # Rotating by 0 radians should leave any vector unchanged
    v = Vec3(5, -3, 7)
    rotated = Mat4.rotation_x(0).transform(v)
    assert rotated.x == pytest.approx(5)
    assert rotated.y == pytest.approx(-3)
    assert rotated.z == pytest.approx(7)

def test_translation():
    translate = Mat4([
        [1, 0, 0, 5],
        [0, 1, 0, -3],
        [0, 0, 1, 2],
        [0, 0, 0, 1],
    ])

    result = translate.transform(Vec3(1, 1, 1))
    assert result.x == 6
    assert result.y == -2
    assert result.z == 3

def test_rotating_90deg_around_x_turns_y_into_z():
    rotated = Mat4.rotation_x(math.pi / 2).transform(Vec3(0, 1, 0))
    assert rotated.x == pytest.approx(0)
    assert rotated.y == pytest.approx(0)
    assert rotated.z == pytest.approx(1)

def test_rotating_90deg_around_y_turns_x_into_negative_z():
    rotated = Mat4.rotation_y(math.pi / 2).transform(Vec3(1, 0, 0))
    assert rotated.x == pytest.approx(0)
    assert rotated.y == pytest.approx(0)
    assert rotated.z == pytest.approx(-1)

def test_translation_then_rotation_differs_from_rotation_then_translation():
    v = Vec3(1, 0, 0)
    t = Mat4.translation(5, 0, 0)
    r = Mat4.rotation_y(math.pi / 2)
    tr = (t @ r).transform(v)
    rt = (r @ t).transform(v)
    assert tr.x != pytest.approx(rt.x) or tr.y != pytest.approx(rt.y) or tr.z != pytest.approx(rt.z)

def test_chaining_equals_sequential_transform():
    scale_x = Mat4([
        [2, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    translate = Mat4([
        [1, 0, 0, 5],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    v = Vec3(3, 4, 5)
    chained = (translate @ scale_x).transform(v)
    sequential = translate.transform(scale_x.transform(v))

    assert chained.x == sequential.x
    assert chained.y == sequential.y
    assert chained.z == sequential.z

