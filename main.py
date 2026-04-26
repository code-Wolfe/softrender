import math
import pygame
from src.linalg.matrix import Mat4
from src.geometry.shapes import cube
from src.render.renderer import WIDTH, HEIGHT, draw_mesh


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Engine")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Menlo", 18)

    mesh = cube(size=2.0)

    z_offset = 5.0
    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            z_offset -= 0.05
        if keys[pygame.K_s]:
            z_offset += 0.05
        if keys[pygame.K_LEFT]:
            angle_y -= 0.03
        if keys[pygame.K_RIGHT]:
            angle_y += 0.03
        if keys[pygame.K_UP]:
            angle_x -= 0.03
        if keys[pygame.K_DOWN]:
            angle_x += 0.03
        if keys[pygame.K_q]:
            angle_z -= 0.03
        if keys[pygame.K_e]:
            angle_z += 0.03

        screen.fill((0, 0, 0))

        transform = (
            Mat4.translation(0, 0, z_offset)
            @ Mat4.rotation_x(angle_x)
            @ Mat4.rotation_y(angle_y)
            @ Mat4.rotation_z(angle_z)
        )

        draw_mesh(screen, mesh, transform, (100, 200, 255))

        info_lines = [
            f"z_offset: {z_offset:.2f}     (W/S to move)",
            f"angle_x:  {math.degrees(angle_x):6.1f}°  (UP/DOWN)",
            f"angle_y:  {math.degrees(angle_y):6.1f}°  (LEFT/RIGHT)",
            f"angle_z:  {math.degrees(angle_z):6.1f}°  (Q/E)",
        ]
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (200, 200, 200))
            screen.blit(text, (10, 10 + i * 22))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()