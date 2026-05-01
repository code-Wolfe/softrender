import math
import pygame
from src.linalg.vector import Vec3
from src.linalg.matrix import Mat4
from src.geometry.shapes import cube
from src.render.camera import Camera
from src.render.renderer import WIDTH, HEIGHT, draw_mesh


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Engine")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Menlo", 18)

    # Two cubes for spatial reference
    mesh = cube(size=2.0)
    mesh2 = cube(size=1.0)
    for i, v in enumerate(mesh2.vertices):
        mesh2.vertices[i] = v + Vec3(3, 0, 0)

    # Free-fly camera state
    eye = Vec3(0.0, 0.0, 8.0)   # start position
    yaw = math.pi               # facing -Z (toward the origin from +Z side)
    pitch = 0.0                 # level

    MOVE_SPEED = 0.08
    LOOK_SPEED = 0.03
    PITCH_LIMIT = math.radians(89)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # --- Look controls (arrows): update yaw/pitch ---
        if keys[pygame.K_LEFT]:
            yaw -= LOOK_SPEED
        if keys[pygame.K_RIGHT]:
            yaw += LOOK_SPEED
        if keys[pygame.K_UP]:
            pitch += LOOK_SPEED
        if keys[pygame.K_DOWN]:
            pitch -= LOOK_SPEED

        pitch = max(-PITCH_LIMIT, min(PITCH_LIMIT, pitch))

        # --- Compute the forward and right vectors from yaw/pitch ---
        forward = Vec3(
            math.cos(pitch) * math.sin(yaw),
            math.sin(pitch),
            math.cos(pitch) * math.cos(yaw),
        )
        world_up = Vec3(0, 1, 0)
        right = forward.cross(world_up).normalize()

        # --- Movement controls (WASD + space/shift) ---
        if keys[pygame.K_w]:
            eye = eye + forward * MOVE_SPEED
        if keys[pygame.K_s]:
            eye = eye - forward * MOVE_SPEED
        if keys[pygame.K_a]:
            eye = eye + right * MOVE_SPEED   # we'll discuss this sign below
        if keys[pygame.K_d]:
            eye = eye - right * MOVE_SPEED
        if keys[pygame.K_SPACE]:
            eye = eye + world_up * MOVE_SPEED
        if keys[pygame.K_LSHIFT]:
            eye = eye - world_up * MOVE_SPEED

        # --- Build the camera looking one unit ahead in the forward direction ---
        camera = Camera(
            eye=eye,
            target=eye + forward,
            up=world_up,
        )

        screen.fill((0, 0, 0))

        view = camera.view_matrix()
        model = Mat4.identity()
        transform = view @ model

        draw_mesh(screen, mesh, transform, (100, 200, 255))
        draw_mesh(screen, mesh2, transform, (255, 200, 100))

        info_lines = [
            f"eye:    ({eye.x:6.2f}, {eye.y:6.2f}, {eye.z:6.2f})",
            f"yaw:    {math.degrees(yaw):6.1f}°",
            f"pitch:  {math.degrees(pitch):6.1f}°",
            "WASD: move   SPACE/SHIFT: up/down   Arrows: look",
        ]
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (200, 200, 200))
            screen.blit(text, (10, 10 + i * 22))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()