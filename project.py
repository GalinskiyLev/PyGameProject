import pygame
import os
import sys
from math import cos, sin, radians


def draw_word(word, flag):
    font = pygame.font.Font(None, 50)
    text = font.render(str(word), True, (100, 255, 100))
    text_w = text.get_width()
    text_h = text.get_height()
    if flag == 1:
        x, y = 11, 11
    elif flag == 2:
        x, y = width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2
    else:
        x, y = width - text_w - 11, 11
    screen.blit(text, (x, y))
    pygame.draw.rect(screen, (0, 255, 0), (x - 10, y - 10, text_w + 20, text_h + 20), 1)


def load_image(name, w, h):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (w, h))
    return image


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, file_name, angle, *group):
        super().__init__(*group)
        self.width = 20
        self.height = 10
        self.image = load_image(file_name, self.width, self.height)
        self.image.set_colorkey(-1)
        self.rect = self.image.get_rect()
        self.angle = angle
        self.rect.x = pos_x  # + self.width * cos(radians(self.angle))
        self.rect.y = pos_y  # + self.height * sin(radians(self.angle))
        self.image = pygame.transform.rotate(self.image, self.angle + 180)
        self.image.set_colorkey(-1)
        self.ax = 70 * cos(radians(self.angle))
        self.ay = 70 * -sin(radians(self.angle))
        self.timer = 0

    def moving(self):
        if self.rect.x > width - self.width // 2:
            self.rect.x = 0 - self.width // 2
        elif self.rect.x < -self.width // 2:
            self.rect.x = width - self.width // 2
        if self.rect.y > height - self.height // 2:
            self.rect.y = 0 - self.height // 2
        elif self.rect.y < -self.height // 2:
            self.rect.y = height - self.height // 2
        self.timer += 1
        if self.timer >= FPS * 0.5:
            self.kill()
        self.rect = self.rect.move(self.ax, self.ay)


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
        self.hp = 500


    def reverse(self, angle):
        self.angle += angle
        if self.angle == 360 or self.angle == -360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.ship_image, self.angle)
        self.image.set_colorkey(-1)

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

    def laser_shot(self, file_name, *group):
        pos_x = self.rect.x + self.ship_width / 2
        pos_y = self.rect.y + self.ship_height / 2
        Laser(pos_x, pos_y, file_name, self.angle, *group)
        self.hp -= 1


pygame.init()
FPS = 24
size = width, height = 1200, 900
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
all_ships = pygame.sprite.Group()
lasers = pygame.sprite.Group()
first_ship = Ship(50, height / 2, 'ship_1.png', all_sprites, all_ships)
second_ship = Ship(width - 50, height / 2, 'ship_2.png', all_sprites, all_ships)

second_ship.reverse(180)
all_sprites.add(first_ship)

pygame.display.flip()

running = True
FLAG = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if FLAG:
        if pygame.key.get_pressed()[pygame.K_w]:
            first_ship.update()
        if pygame.key.get_pressed()[pygame.K_a]:
            first_ship.reverse(10)
        if pygame.key.get_pressed()[pygame.K_d]:
            first_ship.reverse(-10)
        if pygame.key.get_pressed()[pygame.K_x]:
            first_ship.laser_shot('laser3.png', all_sprites, lasers)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            second_ship.laser_shot('laser4.png', all_sprites, lasers)
        if pygame.key.get_pressed()[pygame.K_UP]:
            second_ship.update()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            second_ship.reverse(10)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            second_ship.reverse(-10)
        screen.fill(pygame.Color('white'))
        for sprite in all_sprites:
            sprite.moving()
    for ship in all_ships:
        if pygame.sprite.spritecollideany(ship, lasers, collided=None):
            pygame.sprite.spritecollideany(ship, lasers, collided=None).kill()
            ship.hp -= 20
        if ship.hp <= 0:
            ship.kill()
            FPS = 10
    draw_word(first_ship.hp, True)
    draw_word(second_ship.hp, False)
    #first_ship.moving()
    #second_ship.moving()
    if not first_ship.alive() and not second_ship.alive():
        draw_word('Ничья', 2)
        FLAG = False
    elif not first_ship.alive():
        draw_word('Победа 2 игрока', 2)
        FLAG = False
    elif not second_ship.alive():
        draw_word('Победа 1 игрока', 2)
        FLAG = False
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
