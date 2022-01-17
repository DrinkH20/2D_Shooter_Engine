import pygame
import math
from utils import resize_img
WIN = pygame.display.set_mode((720, 400), -200)
pygame.display.set_caption("2D Shooter!")
p_width = 20
p_height = 40
player_img = resize_img(pygame.image.load("Player.png"), p_width, p_height)
player_mask = pygame.mask.from_surface(player_img)
level_img = resize_img(pygame.image.load("Level1.png"), 2000, 600)
level_mask = pygame.mask.from_surface(level_img)
bullet_img = resize_img(pygame.image.load("Bullets.png"), 4, 4)
bullet_mask = pygame.mask.from_surface(bullet_img)
target_img = resize_img(pygame.image.load("Target.png"), 30, 40)
target_mask = pygame.mask.from_surface(target_img)
current_gun = resize_img(pygame.image.load("Weapon_1.png"), 45, 45)
target_place = [(1885, 200), (1885, 250), (1885, 300), (1885, 350)]
bullet_masks = []
alive_targets = []
hit_targets = []
run = True
Plyr_X = 200
Plyr_Y = 200
VelX = 0
VelY = 0
bullet_list = []
time_count = 0
scroll_x = 0
scroll_y = 0
bullet_wait = 7
level = 0
repeat = 0


class Player:
    def __init__(self):
        self.img = player_img
        self.mask = player_mask
        self.x = Plyr_X
        self.y = Plyr_Y
        self.VelX = 0
        self.VelY = 0
        self.jump_height = 15

    def move_left(self):
        self.VelX -= 1

    def move_right(self):
        self.VelX += 1

    def jump(self):
        self.VelY -= self.jump_height

    def move_x(self):
        self.VelX = (self.VelX * .9)
        self.x += self.VelX

    def move_y(self):
        self.VelY += .6
        self.y += self.VelY

    def collide_x(self):
        self.x += self.VelX * -1
        self.VelX = 0

    def collide_y(self):
        self.y += self.VelY * -1
        self.VelY = 0

    def set_vars(self):
        global Plyr_X, Plyr_Y
        global VelX, VelY
        Plyr_X = self.x
        Plyr_Y = self.y
        VelX = self.VelX
        VelY = self.VelY

    def draw_player(self, window):
        window.blit(self.img, (self.x + scroll_x, self.y + scroll_y))

    def colliding(self, offset_y=0):
        global player_mask
        self.mask = pygame.mask.from_surface(self.img)
        poi = level_mask.overlap(self.mask, (self.x, self.y + offset_y))
        return poi


class Bullets:
    def __init__(self):
        global Plyr_X, Plyr_Y
        global mx, my
        global bullet_masks
        self.X = Plyr_X
        self.Y = Plyr_Y
        self.dir = math.atan2(Plyr_X - mx + scroll_x + 10, Plyr_Y - my + scroll_y + 15)
        self.vx = math.sin(self.dir) * -1
        self.vy = math.cos(self.dir) * -1
        self.img = bullet_img
        self.mask = bullet_mask
        self.delete = 0
        self.rotated = 0
        self.place = 0
        self.item = (self.mask, int(self.X), int(self.Y))
        bullet_masks.append((self.mask, int(self.X), int(self.Y)))

    def move(self):
        global bullet_mask
        global level_mask
        global bullet_masks
        self.X += self.vx * 7
        self.Y += self.vy * 7
        self.delete += 1
        poi = level_mask.overlap(self.mask, (self.X + 5, self.Y + 15))
        part = bullet_masks.index(self.item)
        bullet_masks[part] = (self.mask, int(self.X), int(self.Y))
        self.item = (self.mask, int(self.X), int(self.Y))
        if poi:
            self.delete = 100
        return self.delete

    def draw(self):
        if self.delete > 2:
            self.rotated = pygame.transform.rotate(self.img, self.dir * (180 / 3.14))
            self.place = self.X-int(self.rotated.get_width()/2)+10, self.Y-int(self.rotated.get_height() / 2)+15
            WIN.blit(self.rotated, (self.place[0] + scroll_x + (VelX * 2), self.place[1] + scroll_y + (VelY * 2)))


class Gun:
    def __init__(self):
        self.weapon = current_gun
        self.dir = 0
        self.place = 0
        self.rotated = 0

    def draw_gun(self):
        if abs(self.dir) != self.dir:
            self.weapon = current_gun
        else:
            self.weapon = pygame.transform.flip(current_gun, True, False)

        self.dir = math.atan2(Plyr_X - mx + scroll_x + 10, Plyr_Y - my + scroll_y + 15)
        self.rotated = pygame.transform.rotate(self.weapon, self.dir * (180 / 3.14))
        self.place = Plyr_X - int(self.rotated.get_width() / 2) + 10, Plyr_Y - int(self.rotated.get_height() / 2) + 15
        WIN.blit(self.rotated, (self.place[0] + scroll_x, self.place[1] + scroll_y))


class Targets:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = target_img
        self.mask = target_mask

    def draw_target(self, place):
        WIN.blit(self.img, (place[0] + scroll_x, place[1] + scroll_y))
        self.x = place[0]
        self.y = place[1]

    def collision(self):
        for p in bullet_masks:
            poi = p[0].overlap(self.mask, (self.x - p[1] - 10, self.y - p[2] - 15))
            if poi:
                return 1


def generate_targets():
    global target_place
    global repeat
    repeat = 0
    for j in target_place:
        alive_targets.append(Targets())
        alive_targets[repeat].draw_target(j)
        repeat += 1


Player = Player()
Gun = Gun()

generate_targets()

while run:
    keys = pygame.key.get_pressed()
    pygame.time.delay(10)
    WIN.fill((0, 0, 20))
    WIN.blit(level_img, (scroll_x, scroll_y))
    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    # This is to draw the targets and to delete them when their hit
    repeat = 0
    for i in alive_targets:
        i.draw_target(target_place[repeat])
        repeat += 1
    for i in alive_targets:
        if i.collision():
            target_place.pop(alive_targets.index(i))
            alive_targets.remove(i)

    Player.draw_player(WIN)

    Player.move_y()

    if Player.colliding():
        Player.collide_y()
        if Player.colliding(1):
            if keys[pygame.K_UP]:
                Player.jump()

    Player.move_x()

    if Player.colliding():
        Player.collide_x()

    if keys[pygame.K_LEFT]:
        Player.move_left()
    if keys[pygame.K_RIGHT]:
        Player.move_right()

    Player.set_vars()

    if click[0] and time_count > bullet_wait:
        time_count = 0
        bullet_list.append(())
        bullet_list[len(bullet_list) - 1] = Bullets()

    repeat = 0
    for i in bullet_list:
        bullet = i
        bullet.draw()
        if bullet.move() >= 100:
            bullet_masks.remove(bullet_masks[repeat])
            bullet_list.remove(i)
        repeat += 1

    Gun.draw_gun()

    time_count += 1

    scroll_x -= (Plyr_X + scroll_x - 250) * .1
    scroll_y -= (Plyr_Y + scroll_y - 250) * .1

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
