import pygame
import os
import sys
from math import cos, sin, radians


def load_image(name, w, h):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (w, h))
    return image


class Ship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, file_name, *group):
        super().__init__(*group)
        self.ship_width = 50
        self.ship_height = 50
        self.image = load_image(file_name, self.ship_width, self.ship_height)
        self.image.set_colorkey(-1)
        self.ship_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.x = 0
        self.y = 0
        self.ax = 0
        self.ay = 0
        self.angle = 0

    def reverse(self, angle):
        self.angle += angle
        if self.angle == 360 or self.angle == -360:
            self.angle = 0
        print(self.angle)
        self.image = pygame.transform.rotate(self.ship_image, self.angle)
        self.image.set_colorkey(-1)
        #self.image = pygame.transform.scale(self.ship_image, (self.ship_width, self.ship_height))

    def update(self):
        self.ax += 1 * cos(radians(self.angle))
        self.ay -= 1 * sin(radians(self.angle))
        if self.ax < -30 or self.ax > 30:
            self.ax -= 1 * cos(radians(self.angle))
        if self.ay < -30 or self.ay > 30:
            self.ay += 1 * sin(radians(self.angle))
        self.x = self.ax * abs(cos(radians(self.angle)))
        self.y = self.ay * abs(sin(radians(self.angle)))

    def moving(self):
        if self.rect.x > width - self.ship_width // 2:
            self.rect.x = 0 - self.ship_width // 2
        elif self.rect.x < -self.ship_width // 2:
            self.rect.x = width - self.ship_width // 2
        if self.rect.y > height - self.ship_height // 2:
            self.rect.y = 0 - self.ship_height // 2
        elif self.rect.y < -self.ship_height // 2:
            self.rect.y = height - self.ship_height // 2
        self.rect = self.rect.move(self.x, self.y)


pygame.init()
FPS = 24
size = width, height = 1200, 900
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
first_ship = Ship(50, height / 2, 'ship_1.png', all_sprites)
second_ship = Ship(width - 50, height / 2, 'ship_2.png', all_sprites)
second_ship.reverse(180)
all_sprites.add(first_ship)

pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.key.get_pressed()[pygame.K_w]:
        first_ship.update()
    if pygame.key.get_pressed()[pygame.K_a]:
        first_ship.reverse(10)
    if pygame.key.get_pressed()[pygame.K_d]:
        first_ship.reverse(-10)
    if pygame.key.get_pressed()[pygame.K_UP]:
        second_ship.update()
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        second_ship.reverse(10)
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        second_ship.reverse(-10)
    screen.fill(pygame.Color('white'))
    first_ship.moving()
    second_ship.moving()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
