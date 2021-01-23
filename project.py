import pygame
import random


class ship:
    def __init__(self, pos_x, pos_y, color):
        pygame.draw.circle(screen, color, (int(pos_x), pos_y), 20)


class bullet:
    def __init__(self, pos_x, pos_y, color):
        pygame.draw.circle(screen, color, (int(pos_x), pos_y), 2)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Звёздные войны')
    size = width, height = 1000, 800
    screen = pygame.display.set_mode(size)

    x_pos_first_ship = 0
    y_pos_first_ship = height / 2
    x_pos_second_ship = width
    y_pos_second_ship = height / 2

    v_first_ship = 80
    v_second_ship = -80

    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        first = ship(int(x_pos_first_ship), y_pos_first_ship, (255, 0, 0))
        second = ship(int(x_pos_second_ship), y_pos_second_ship, (0, 0, 255))

        x_pos_first_ship += v_first_ship / fps
        x_pos_second_ship += v_second_ship / fps

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
