import pygame
import math
from utils import resize_img, draw_img, scale_img
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
level = 0
Target_Places = [[(1895, 200), (1895, 250), (1895, 300), (1895, 350)],
                 [(850, 235), (950, 235), (1050, 235), (1150, 235)],
                 [(1225, 50), (1225, 100), (1225, 150), (1225, 200)]]
Level_Targets = Target_Places[level]
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
repeat = 0
zom = 1


def load_everything():
    global level
    global Level_Targets
    global level_mask
    global level_img
    global Plyr_X
    global Plyr_Y
    global VelX
    global VelY
    global level_img_img
    Level_Targets = Target_Places[level]
    name = ("Level" + str(level + 1) + ".png")
    level_img = resize_img(pygame.image.load(name), 2000, 600)
    level_img_img = scale_img(level_img, zom)
    level_mask = pygame.mask.from_surface(level_img_img)
    Plyr_X = 200
    Plyr_Y = 200
    VelX = 0
    VelY = 0


class Player:
    def __init__(self):
        self.img = scale_img(player_img, zom)
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
        self.img = scale_img(player_img, zom)
        self.mask = player_mask
        # window.blit(self.img, (self.x + scroll_x, self.y + scroll_y))
        draw_img(window, self.img, self.x, self.y, scroll_x, scroll_y, zom)

    def colliding(self, offset_y=0):
        global player_mask
        self.mask = pygame.mask.from_surface(self.img)
        poi = level_mask.overlap(self.mask, (int(self.x / zom), self.y / zom + offset_y))
        return poi

    def move_up(self):
        self.y -= 1

    def half_width(self):
        self.img = scale_img(player_img, zom)
        return self.img.get_width()/2


class Bullets:
    def __init__(self):
        global Plyr_X, Plyr_Y
        global mx, my
        global bullet_masks
        self.X = round(Plyr_X + (VelX * 2))
        self.Y = round(Plyr_Y + (VelY * 2))
        self.dir = math.atan2((Plyr_X + scroll_x + 10) / zom - mx, (Plyr_Y + scroll_y + 14) / zom - my)
        self.vx = math.sin(self.dir) * -1
        self.vy = math.cos(self.dir) * -1
        self.img = scale_img(bullet_img, zom)
        self.mask = bullet_mask
        self.delete = 0
        self.rotated = 0
        self.place = 0
        self.item = (self.mask, round(self.X), round(self.Y))
        self.poi = 0
        bullet_masks.append(self.item)

    def move(self):
        global bullet_mask
        global level_mask
        global bullet_masks
        self.X += self.vx * 10
        self.Y += self.vy * 10
        self.poi = level_mask.overlap(self.mask, (int((self.X + 5) / zom), (self.Y + 15) / zom))

        # This is a failsafe just in case the code glitches for some reason
        if bullet_masks.__contains__(self.item):
            part = bullet_masks.index(self.item)
            self.item = (self.mask, round(self.X), round(self.Y))
            bullet_masks[part] = self.item

        self.delete += 1
        if self.poi:
            self.delete = 1000
            self.item = ""
        return self.delete

    def draw(self):
        if self.delete > 2:
            self.img = scale_img(bullet_img, zom)
            self.mask = bullet_mask
            self.rotated = pygame.transform.rotate(self.img, self.dir * (180 / 3.14))
            self.place = self.X-(self.rotated.get_width()/2)+10, self.Y-(self.rotated.get_height() / 2)+15
            # WIN.blit(self.rotated, (self.place[0] + scroll_x, self.place[1] + scroll_y))
            draw_img(WIN, self.rotated, self.place[0], self.place[1], scroll_x, scroll_y, zom)


class Gun:
    def __init__(self):
        self.weapon = scale_img(current_gun, zom)
        self.dir = 0
        self.place = 0
        self.rotated = 0

    def draw_gun(self):
        self.weapon = scale_img(current_gun, zom)
        if abs(self.dir) != self.dir:
            self.weapon = scale_img(current_gun, zom)
        else:
            self.weapon = pygame.transform.flip(scale_img(current_gun, zom), True, False)

        self.dir = math.atan2((Plyr_X + scroll_x + 10) / zom - mx, (Plyr_Y + scroll_y + 15) / zom - my)
        self.rotated = pygame.transform.rotate(self.weapon, self.dir * (180 / 3.14))
        self.place = ((Plyr_X + 10) - ((self.rotated.get_width()/2) * zom)), ((Plyr_Y + 15) - ((self.rotated.get_height() / 2) * zom))
        # WIN.blit(self.rotated, (self.place[0] + scroll_x, self.place[1] + scroll_y))
        draw_img(WIN, self.rotated, self.place[0], self.place[1], scroll_x, scroll_y, zom)


class Targets:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = scale_img(target_img, zom)
        self.mask = target_mask

    def draw_target(self, place):
        self.img = scale_img(target_img, zom)
        self.mask = target_mask
        # WIN.blit(self.img, (place[0] + scroll_x, place[1] + scroll_y))
        draw_img(WIN, self.img, place[0], place[1], scroll_x, scroll_y, zom)
        self.x = place[0]
        self.y = place[1]

    def collision(self):
        for p in bullet_masks:
            poi = p[0].overlap(self.mask, (self.x - p[1] - 10, self.y - p[2] - 15))
            if poi:
                return 1


def generate_targets():
    global Level_Targets
    global repeat
    repeat = 0
    for j in Level_Targets:
        alive_targets.append(Targets())
        alive_targets[repeat].draw_target(j)
        repeat += 1


player = Player()
gun = Gun()

generate_targets()

load_everything()

while run:
    keys = pygame.key.get_pressed()
    pygame.time.delay(10)
    WIN.fill((0, 0, 20))

    # This is to draw the targets and to delete them when their hit
    repeat = 0
    for i in alive_targets:
        i.draw_target(Level_Targets[repeat])
        repeat += 1
    for i in alive_targets:
        if i.collision():
            Level_Targets.pop(alive_targets.index(i))
            alive_targets.remove(i)

    # WIN.blit(level_img, (scroll_x, scroll_y))
    level_img_img = scale_img(level_img, zom)
    level_mask = pygame.mask.from_surface(level_img_img)
    draw_img(WIN, level_img_img, scroll_x, scroll_y, 0, 0, zom)

    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    player.draw_player(WIN)

    player.move_y()

    if player.colliding():
        player.collide_y()
        if player.colliding(1):
            if keys[pygame.K_UP]:
                player.jump()

    player.move_x()

    if player.colliding():
        player.collide_x()

    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    player.set_vars()

    if click[0] and time_count > bullet_wait:
        time_count = 0
        bullet_list.append(Bullets())

    repeat = 0
    for i in bullet_list:
        bullet = i
        bullet.draw()
        if bullet.move() > 80:
            bullet_masks.remove(bullet_masks[repeat])
            bullet_list.remove(bullet_list[repeat])
        else:
            repeat += 1

    gun.draw_gun()

    time_count += 1

    scroll_x -= (Plyr_X + scroll_x - 250 * zom) * .1
    scroll_y -= (Plyr_Y + scroll_y - 250 * zom) * .1

    if len(alive_targets) == 0 and level < 2:
        level += 1
        load_everything()
        generate_targets()
        player.__init__()

    if keys[pygame.K_x]:
        zom += .05
        player.move_up()
    if keys[pygame.K_z]:
        zom -= .05
        player.move_up()
    if zom > 3:
        zom = 3
    elif zom < .5:
        zom = .5

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
