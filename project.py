import pygame
import os
import sys


def load_image(name, w, h):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (w, h))
    return image


class Ship(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.ship_width = 100
        self.ship_height = 100
        self.image = load_image('ship_1.png', self.ship_width, self.ship_height)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400
        self.vx = 0
        self.vy = 0
        self.v = 0
        self.angle = 0

    def reverse(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.image, self.angle)

    def update(self):
        if self.v < 50:
            self.v += 1

    def moving(self):
        if self.rect.x > width - self.ship_width // 2:
            self.rect.x = 0 - self.ship_width // 2
        elif self.rect.x < -self.ship_width // 2:
            self.rect.x = width - self.ship_width // 2
        if self.rect.y > height - self.ship_height // 2:
            self.rect.y = 0 - self.ship_height // 2
        elif self.rect.y < -self.ship_height // 2:
            self.rect.y = height - self.ship_height // 2
        self.rect = self.rect.move(0, -self.v)



pygame.init()
FPS = 24
size = width, height = 1200, 900
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
first_ship = Ship()
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
        first_ship.reverse(-10)
    elif pygame.key.get_pressed()[pygame.K_d]:
        first_ship.reverse(10)
    screen.fill(pygame.Color('white'))
    first_ship.moving()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()