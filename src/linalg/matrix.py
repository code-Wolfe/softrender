from src.linalg.vector import Vec3
import math


class Mat4:
    def __init__(self, rows: list[list[float]]):
        """Create a 4x4 matrix from a list of 4 rows of 4 numbers each."""
        if len(rows) != 4 or any(len(r) != 4 for r in rows):
            raise ValueError("Mat4 requires a 4x4 list of numbers")
        self.m = [row[:] for row in rows]  # copy to avoid aliasing

    def __repr__(self):
        lines = []
        for row in self.m:
            lines.append("  " + "  ".join(f"{v:7.3f}" for v in row))
        return "Mat4(\n" + "\n".join(lines) + "\n)"
    
    @classmethod
    def identity(cls)->"Mat4":
        return cls([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
    
    def transform(self, v: Vec3) ->Vec3:
        
        #treat v as [x,y,z,1]
        x = self.m[0][0]*v.x + self.m[0][1]*v.y + self.m[0][2]*v.z + self.m[0][3]*1
        y = self.m[1][0]*v.x + self.m[1][1]*v.y + self.m[1][2]*v.z + self.m[1][3]*1
        z = self.m[2][0]*v.x + self.m[2][1]*v.y + self.m[2][2]*v.z + self.m[2][3]*1
        w = self.m[3][0]*v.x + self.m[3][1]*v.y + self.m[3][2]*v.z + self.m[3][3]*1

        #perspective divide: if w isnt 1, normalize back
        # (For most transforms w stays 1; for perspective projection it doesn't)

        if w != 0 and w != 1:
            x /= w
            y /= w
            z /= w

        return Vec3(x, y, z)
    
    def __matmul__(self, other: "Mat4") -> "Mat4":
        result = [[0.0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                result[i][j] = sum(self.m[i][k] * other.m[k][j] for k in range(4))
        return Mat4(result)
    
    @classmethod 
    def translation(cls, tx: float, ty: float, tz: float) -> "Mat4":
        return cls([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1],
        ])
    
    @classmethod
    def scale(cls, sx: float, sy: float, sz: float) -> "Mat4":
        return cls([
            [sx, 0,  0,  0],
            [0,  sy, 0,  0],
            [0,  0,  sz, 0],
            [0,  0,  0,  1],
        ])
    
    @classmethod
    def rotation_x(cls, angle: float) -> "Mat4":
        c = math.cos(angle)
        s = math.sin(angle)
        return cls([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1],
        ])
    
    @classmethod
    def rotation_y(cls, angle: float) -> "Mat4":
        c = math.cos(angle)
        s = math.sin(angle)
        return cls([
            [c,  0, s, 0],
            [0,  1, 0, 0],
            [-s, 0, c, 0],
            [0,  0, 0, 1],
        ])

    @classmethod
    def rotation_z(cls, angle: float) -> "Mat4":
        c = math.cos(angle)
        s = math.sin(angle)
        return cls([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1],
        ])
    