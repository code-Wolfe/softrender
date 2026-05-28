import pygame
from src.linalg.vector import Vec3
from src.geometry.mesh import Mesh



# Screen resolution and simulated camera focal length in pixels.
# Increasing FOCAL_LENGTH zooms in (narrows the field of view).
WIDTH = 800
HEIGHT = 600
FOCAL_LENGTH = 500

def project(point: Vec3) -> tuple[int, int]:
    """
    Project a 3D world-space point onto the 2D screen using perspective division.

    Returns pixel coordinates (x, y). Returns (-1, -1) if the point is behind
    the camera (z <= 0), which callers use as a sentinel to skip drawing.

    The camera sits at the origin looking down +Z. Points are mapped so that:
      - x increases rightward on screen
      - y increases upward in world space but downward in screen space (flipped)
      - the screen origin (0,0) is the center of the window
    """
    if point.z <= 0:
        # Behind the camera — perspective division would invert or explode.
        return (-1, -1)

    # Perspective divide: scale x/y by focal length and divide by depth so that
    # objects farther away appear smaller and closer to the center of the screen.
    screen_x = FOCAL_LENGTH * point.x / point.z
    screen_y = FOCAL_LENGTH * point.y / point.z

    # Translate from camera-centered coords to top-left pixel coords.
    # Y is negated because screen Y grows downward while world Y grows upward.
    pixel_x = int(WIDTH / 2 + screen_x)
    pixel_y = int(HEIGHT / 2 - screen_y)

    return (pixel_x, pixel_y)

def draw_point(screen, point: Vec3, color=(255, 255, 255)):
    """
    Project a 3D point and draw it as a filled circle on the pygame surface.
    Points behind the camera (project returns -1) are silently skipped.
    """
    x, y = project(point)
    if x >= 0:
        pygame.draw.circle(screen, color, (x, y), 4)

def draw_line(screen, start: Vec3, end: Vec3, color=(255, 255, 255)):
    """
    Project both endpoints of a 3D line segment and draw it on the pygame surface.
    The line is skipped entirely if either endpoint is behind the camera.
    No clipping is performed — partial lines that cross z=0 are not drawn.
    """
    x1, y1 = project(start)
    x2, y2 = project(end)
    if x1 >= 0 and x2 >= 0:
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)

def face_normal(v0: Vec3, v1: Vec3, v2: Vec3) -> Vec3:
    """
    Return the normal of the triangle (v0, v1, v2).

    For vertices wound counter-clockwise as seen from the side the
    normal should point toward, (v1 - v0) x (v2 - v0) points outward.
    The result is NOT normalized -- back-face culling only checks the
    sign of normal.z, so unit length isn't needed here.
    """
    return (v1 - v0).cross(v2 - v0)

def draw_mesh(screen, mesh: Mesh, transform=None, color=(255, 255, 255)):
    """Draw a mesh as a back-face-culled wireframe.

    If `transform` is given (a Mat4), each vertex is transformed into view
    space first. Faces whose outward normal points away from the camera
    are skipped (back-face culling).
    """
    if transform is None:
        view_vertices = mesh.vertices
    else:
        view_vertices = [transform.transform(v) for v in mesh.vertices]

    for i0, i1, i2 in mesh.faces:
        v0 = view_vertices[i0]
        v1 = view_vertices[i1]
        v2 = view_vertices[i2]

        # Back-face cull: the camera looks down +Z, so a face whose
        # outward normal also has +Z points away from the camera.
        normal = face_normal(v0, v1, v2)
        if normal.dot(v0) > 0:
            continue

        # Project the three view-space vertices to pixel coordinates.
        p0 = project(v0)
        p1 = project(v1)
        p2 = project(v2)

        # Skip the whole face if any vertex is behind the camera.
        if p0[0] < 0 or p1[0] < 0 or p2[0] < 0:
            continue

        pygame.draw.polygon(screen, color, [p0, p1, p2], width=1)