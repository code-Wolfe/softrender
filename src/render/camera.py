from src.linalg.vector import Vec3
from src.linalg.matrix import Mat4


class Camera:
    def __init__(self, eye: Vec3, target: Vec3, up: Vec3):
        self.eye = eye
        self.target = target
        self.up = up

    def view_matrix(self) -> Mat4:
        
        forward = (self.target - self.eye).normalize()
        right = self.up.cross(forward).normalize()
        up = forward.cross(right)


        return Mat4([
            [right.x,   right.y,   right.z,   -right.dot(self.eye)],
            [up.x,      up.y,      up.z,      -up.dot(self.eye)],
            [forward.x, forward.y, forward.z, -forward.dot(self.eye)],
            [0,         0,         0,         1],
        ])