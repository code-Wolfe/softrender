from src.linalg.vector import Vec3

class Mesh:
    def __init__(self, vertices: list[Vec3], edges: list[tuple[int, int]]):
        """
        A mesh is a collection of 3D vertices and the edges connecting them.

        vertices: list of Vec3 points in the mesh's local coordinate space
        edges: list of (i, j) pairs, where i and j are indices into vertices
        """

        self.vertices = vertices
        self.edges = edges

        