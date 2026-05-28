from src.linalg.vector import Vec3

class Mesh:
    def __init__(
        self,
        vertices: list[Vec3],
        edges: list[tuple[int, int]],
        faces: list[tuple[int, int, int]] | None = None,
    ):
        """
        A mesh is a collection of 3D vertices, the edges connecting them,
        and the triangular faces spanning them.

        vertices: list of Vec3 points in the mesh's local coordinate space
        edges: list of (i, j) pairs, where i and j are indices into vertices
        faces: list of (i, j, k) triples, where each triple indexes three
               vertices forming a triangle, wound counter-clockwise as seen
               from outside the mesh
        """

        self.vertices = vertices
        self.edges = edges
        self.faces = faces if faces is not None else []

        