import math
import pytest
from src.linalg.vector import Vec3


def test_addition():
    a = Vec3(1, 2, 3)
    b = Vec3(4, 5, 6)
    result = a + b
    assert result.x == 5
    assert result.y == 7
    assert result.z == 9


def test_subtraction():
    a = Vec3(4, 5, 6)
    b = Vec3(1, 2, 3)
    result = a - b
    assert result.x == 3
    assert result.y == 3
    assert result.z == 3


def test_scalar_multiplication():
    v = Vec3(1, 2, 3)
    result = v * 2
    assert result.x == 2
    assert result.y == 4
    assert result.z == 6


def test_scalar_multiplication_reversed():
    # Tests __rmul__ (scalar on the left)
    v = Vec3(1, 2, 3)
    result = 3 * v
    assert result.x == 3
    assert result.y == 6
    assert result.z == 9


def test_magnitude_3_4_5_triangle():
    # Classic Pythagorean triple
    v = Vec3(3, 4, 0)
    assert v.magnitude() == 5.0


def test_magnitude_unit_axes():
    assert Vec3(1, 0, 0).magnitude() == 1.0
    assert Vec3(0, 1, 0).magnitude() == 1.0
    assert Vec3(0, 0, 1).magnitude() == 1.0


def test_normalize_preserves_direction():
    v = Vec3(5, 0, 0)
    result = v.normalize()
    assert result.x == 1.0
    assert result.y == 0.0
    assert result.z == 0.0


def test_normalize_produces_unit_length():
    v = Vec3(1, 1, 1)
    result = v.normalize()
    # Floating point math is imprecise, so use pytest.approx
    assert result.magnitude() == pytest.approx(1.0)


def test_normalize_zero_vector_raises():
    with pytest.raises(ValueError):
        Vec3(0, 0, 0).normalize()

def test_perpendicular_vector_gives_zero():
    assert Vec3(1,0,0).dot(Vec3(0,1,0)) == 0

def test_parallel_vector_gives_positive_value():
    assert Vec3(1,0,0).dot(Vec3(2,0,0)) == 2

def test_opposite_vector_gives_negative_value():
    assert Vec3(1,0,0).dot(Vec3(-3,0,0)) == -3

def test_general_case():
    assert Vec3(1,2,3).dot(Vec3(4,5,6)) == 32

def test_x_cross_y_equals_z():
    result = Vec3(1,0,0).cross(Vec3(0,1,0))
    assert result.x == 0.0
    assert result.y == 0.0
    assert result.z == 1.0

def test_anti_commutativity():
    result = Vec3(0,1,0).cross(Vec3(1,0,0))
    assert result.x == 0.0
    assert result.y == 0.0
    assert result.z == -1.0

def test_parallel_vectors_give_zero_vector():
    result = Vec3(1,2,3).cross(Vec3(2,4,6))
    assert result.x == 0.0
    assert result.y == 0.0
    assert result.z == 0.0

def test_cross_product_is_perpendicular_to_both_inputs():
    a = Vec3(1,2,3)
    b = Vec3(4,5,6)
    c = a.cross(b)
    assert a.dot(c) == pytest.approx(0)
    assert a.dot(c) == pytest.approx(0)