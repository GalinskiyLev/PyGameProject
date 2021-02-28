import pygame
import os
import sys
from math import cos, sin, radians


def write_text(message, y_pos, x_pos=0, flag=False, font_size=30):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, (100, 255, 100))
    least_with_texts = []

    text_w = text.get_width()
    text_h = text.get_height()
    x_pos = (width - text.get_width()) // 2 + x_pos
    screen.blit(text, (x_pos, y_pos))
    if flag:
        pygame.draw.rect(screen, (0, 255, 0), (x_pos, y_pos, text_w, text_h), 1)


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
        self.rect.x = pos_x + self.width * cos(radians(self.angle))
        self.rect.y = pos_y - self.height * sin(radians(self.angle))
        self.image = pygame.transform.rotate(self.image, self.angle + 180)
        self.image.set_colorkey(-1)
        self.ax = 60 * cos(radians(self.angle))
        self.ay = 60 * -sin(radians(self.angle))
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

    def update(self, events):
        if events[pygame.K_w]:
            first_ship.speeding()
        if events[pygame.K_a]:
            first_ship.reverse(10)
        if events[pygame.K_d]:
            first_ship.reverse(-10)
        if events[pygame.K_x]:
            first_ship.laser_shot('laser3.png', all_sprites, lasers)
        if events[pygame.K_UP]:
            second_ship.speeding()
        if events[pygame.K_LEFT]:
            second_ship.reverse(10)
        if events[pygame.K_RIGHT]:
            second_ship.reverse(-10)
        if events[pygame.K_SPACE]:
            second_ship.laser_shot('laser4.png', all_sprites, lasers)

    def reverse(self, angle):
        self.angle += angle
        if self.angle == 360 or self.angle == -360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.ship_image, self.angle)
        self.image.set_colorkey(-1)

    def speeding(self):
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
        # pos_x = self.rect.x + self.ship_width / 2# + self.ship_width * cos(radians(self.angle))
        # pos_y = self.rect.y + self.ship_height / 2# + self.ship_height * sin(radians(self.angle))
        pos_x, pos_y = self.rect.center
        pos_x += (self.ship_width / 2 - 20) * -cos(radians(self.angle))
        pos_y += (self.ship_height / 2 - 20) * sin(radians(self.angle))
        Laser(pos_x, pos_y, file_name, self.angle, *group)
        self.hp -= 1


pygame.init()
FPS = 24
size = width, height = 1270, 900
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
all_ships = pygame.sprite.Group()
lasers = pygame.sprite.Group()
background = load_image('screen2.jpg', width, height)

line_spacing = 25
upper_margin = 40
write_text('Бойцы! Чтобы защитится от космических отак, их надо понять.', upper_margin)
write_text('Так что находи себе партнёра, и добро пожаловать в тренировочную симуляцию комического боя.',
           upper_margin + line_spacing * 1)
write_text('Здесь вы научитесь управлять кораблём, эффиктивно уничтожать врага и тактике космических боёв.',
           upper_margin + line_spacing * 2)
write_text('А чтобы вам было не скучно, тренировка будет PvP, что придаст симуляции сопернический дух.',
           upper_margin + line_spacing * 3)
write_text('Правила просты, как... пареная морковка:', upper_margin + line_spacing * 4)
write_text('На войне бегут только трусы, так что лететь вы можете только вперёд.', upper_margin + line_spacing * 5)
write_text('Для левого игрока - это кнопка "W", а для правого - "вверх"', upper_margin + line_spacing * 6)
write_text('Однако просто лететь вперёд и дурак может, а мы тут вообще-то элиту готовим.',
           upper_margin + line_spacing * 7)
write_text('Так что главная часть данной симуляции - это маневрирование и конечно же стрельба!',
           upper_margin + line_spacing * 8)
write_text('Кнопки поворота левого игрока - это "A" - налево и "D" - направо.', upper_margin + line_spacing * 9)
write_text('Для правого это - "влево" и "вправо". Довольно легко, правда?', upper_margin + line_spacing * 10)
write_text('Кнопка стрельбы - это "Х" для левого и "пробел" для правого.', upper_margin + line_spacing * 11)
write_text(
    'Так как обычно поле боя окружено пространственным барьером, который телепортирует тебя от одного края к другому,',
    upper_margin + line_spacing * 12)
write_text(
    'чтобы противники не смогли сбежать, в нашей симуляции действует точно такая же система. Включай это в свою тактику!',
    upper_margin + line_spacing * 13)
write_text(
    'Полёт снарядов действует по такой же схеме, однако помни, что снаряды - энергетические, а значит и не бесконечные.',
    upper_margin + line_spacing * 14)
write_text(
    'Это значит, что каждый выстрел отнимает энергию корабля, а если её не будет, то он взорвётся из-за детонации двигателя',
    upper_margin + line_spacing * 15)
write_text('Поддержка щита тоже нуждается в энергии, так что старайся уворачиваться по максимому.',
           upper_margin + line_spacing * 16)
write_text('Запомни всего энергии - 500, выстрел - -1 энергии, а попадание - -20.', upper_margin + line_spacing * 17)
write_text(
    'Также есть несколько особенных направлений, попадая в которые корабль либо под силой тяги резко устремляется назад,',
    upper_margin + line_spacing * 18)
write_text('либо просто убирая накопленный кораблём импульс. Пользуйся этим с умом.', upper_margin + line_spacing * 19)
write_text('Ну это всё, что тебе надо знать, так что нажимай "F", и на старт!', upper_margin + line_spacing * 20)
write_text('Удачи на полях сражений!', upper_margin + line_spacing * 21)
pygame.display.flip()
running_menu = True
running = False
FLAG = True
i = 0
while running_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_menu = False
    write_text('Press F to start', upper_margin + line_spacing * 24, 0, True, 222)
    pygame.display.flip()
    clock.tick(FPS)
    if pygame.key.get_pressed()[pygame.K_f]:
        for sprite in all_sprites:
            sprite.kill()
        # screen.fill(pygame.Color('white'))
        # screen.blit(background, (0, 0))
        first_ship = Ship(50, height / 2, 'ship_1.png', all_sprites, all_ships)
        second_ship = Ship(width - 50, height / 2, 'ship_2.png', all_sprites, all_ships)

        second_ship.reverse(180)
        all_sprites.add(first_ship)
        running = True
        FLAG = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                running_menu = False
        if FLAG:
            first_ship.update(pygame.key.get_pressed())
            '''second_ship.update(pygame.key.get_pressed())
            if pygame.key.get_pressed()[pygame.K_w]:
                first_ship.speeding()
            if pygame.key.get_pressed()[pygame.K_a]:
                first_ship.reverse(10)
            if pygame.key.get_pressed()[pygame.K_d]:
                first_ship.reverse(-10)
            if pygame.key.get_pressed()[pygame.K_x]:
                first_ship.laser_shot('laser3.png', all_sprites, lasers)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                second_ship.laser_shot('laser4.png', all_sprites, lasers)
            if pygame.key.get_pressed()[pygame.K_UP]:
                second_ship.speeding()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                second_ship.reverse(10)
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                second_ship.reverse(-10)'''
            # screen.fill(pygame.Color('white'))
            screen.blit(background, (0, 0))
            for sprite in all_sprites:
                sprite.moving()
        for ship in all_ships:
            if pygame.sprite.spritecollideany(ship, lasers, collided=None):
                pygame.sprite.spritecollideany(ship, lasers, collided=None).kill()
                ship.hp -= 20
                L = 1
            if ship.hp <= 0:
                ship.kill()
        draw_word(first_ship.hp, True)
        draw_word(second_ship.hp, False)
        # first_ship.moving()
        # second_ship.moving()
        if not first_ship.alive() and not second_ship.alive():
            draw_word('Ничья', 2)
            FLAG = False
        elif not first_ship.alive():
            draw_word('Победа 2 игрока', 2)
            FLAG = False
        elif not second_ship.alive():
            draw_word('Победа 1 игрока', 2)
            FLAG = False
        if not FLAG:
            running = False
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
