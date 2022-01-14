import pygame
import math
from utils import resize_img
WIN = pygame.display.set_mode((500, 500))
p_width = 20
p_height = 40
player_img = resize_img(pygame.image.load("Player.png"), p_width, p_height)
player_mask = pygame.mask.from_surface(player_img)
level_img = resize_img(pygame.image.load("Level1.png"), 2000, 600)
level_mask = pygame.mask.from_surface(level_img)
bullet_img = resize_img(pygame.image.load("Bullets.png"), 4, 4)
bullet_mask = pygame.mask.from_surface(bullet_img)
current_gun = resize_img(pygame.image.load("Weapon 1.png"), 45, 45)
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


class Player:
    def __init__(self):
        self.img = player_img
        self.mask = player_mask
        self.x = Plyr_X
        self.y = Plyr_Y
        self.VelX = 0
        self.VelY = 0

    def move_left(self):
        self.VelX -= 1

    def move_right(self):
        self.VelX += 1

    def jump(self):
        self.VelY = -10

    def move_x(self):
        self.VelX = (self.VelX * .9)
        self.x += self.VelX

    def move_y(self):
        self.VelY += .1
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
        self.X = Plyr_X
        self.Y = Plyr_Y
        self.dir = math.atan2(Plyr_X - mx + scroll_x, Plyr_Y - my + scroll_y)
        self.vx = math.sin(self.dir) * -1
        self.vy = math.cos(self.dir) * -1
        self.img = bullet_img
        self.mask = bullet_mask
        self.delete = 0
        self.rotated = 0
        self.place = 0

    def move(self):
        global bullet_mask
        global level_mask
        self.X += self.vx * 10
        self.Y += self.vy * 10
        self.delete += 1
        bullet_mask = pygame.mask.from_surface(self.img)
        poi = level_mask.overlap(bullet_mask, (self.X, self.Y))
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

        self.dir = math.atan2(Plyr_X - mx + scroll_x, Plyr_Y - my + scroll_y)
        self.rotated = pygame.transform.rotate(self.weapon, self.dir * (180 / 3.14))
        self.place = Plyr_X - int(self.rotated.get_width() / 2) + 10, Plyr_Y - int(self.rotated.get_height() / 2) + 15
        WIN.blit(self.rotated, (self.place[0] + scroll_x, self.place[1] + scroll_y))


Player = Player()
Gun = Gun()

while run:
    keys = pygame.key.get_pressed()
    pygame.time.delay(10)
    WIN.fill((20, 10, 20))
    WIN.blit(level_img, (scroll_x, scroll_y))
    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

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

    for i in bullet_list:
        bullet = i
        bullet.draw()
        if bullet.move() >= 100:
            bullet_list.remove(i)

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
