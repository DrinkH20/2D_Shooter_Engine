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
bullet_img = resize_img(pygame.image.load("Bullets.png"), 10, 10)
bullet_mask = pygame.mask.from_surface(bullet_img)
run = True
Playerx = 200
Playery = 200
bullet_list = []
time_count = 0
scroll_x = 0
scroll_y = 0


class Player:
    def __init__(self):
        self.img = player_img
        self.mask = player_mask
        self.x = Playerx
        self.y = Playery
        self.xvel = 0
        self.yvel = 0

    def move_left(self):
        self.xvel -= 1

    def move_right(self):
        self.xvel += 1

    def jump(self):
        self.yvel = -10

    def movex(self):
        self.xvel = (self.xvel * .9)
        self.x += self.xvel

    def movey(self):
        self.yvel += .5
        self.y += self.yvel

    def collidex(self):
        self.x += self.xvel * -1
        self.xvel = 0

    def collidey(self):
        self.y += self.yvel * -1
        self.yvel = 0

    def set_vars(self):
        global Playerx
        global Playery
        Playerx = self.x
        Playery = self.y

    def draw_player(self, window):
        window.blit(self.img, (self.x + scroll_x, self.y + scroll_y))

    def colliding(self, offset_y=0):
        global player_mask
        player_mask = pygame.mask.from_surface(self.img)
        poi = level_mask.overlap(player_mask, (self.x, self.y + offset_y))
        return poi


class Bullets:
    def __init__(self):
        global Playerx, Playery
        global mx, my
        self.bltx = Playerx + 5
        self.blty = Playery + 5
        self.dir = math.atan2(Playerx - mx + scroll_x, Playery - my + scroll_y)
        self.vx = math.sin(self.dir) * -1
        self.vy = math.cos(self.dir) * -1
        self.img = bullet_img
        self.delete = 0

    def move(self):
        self.bltx += self.vx * 10
        self.blty += self.vy * 10
        self.delete += 1
        return self.delete

    def draw(self):
        WIN.blit(self.img, (self.bltx + scroll_x, self.blty + scroll_y))


Player = Player()

while run:
    keys = pygame.key.get_pressed()
    pygame.time.delay(10)
    WIN.fill((10, 20, 10))
    WIN.blit(level_img, (scroll_x, scroll_y))
    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    Player.draw_player(WIN)

    Player.movey()

    if Player.colliding():
        Player.collidey()
        if Player.colliding(1):
            if keys[pygame.K_UP]:
                Player.jump()

    Player.movex()

    if Player.colliding():
        Player.collidex()

    if keys[pygame.K_LEFT]:
        Player.move_left()
    if keys[pygame.K_RIGHT]:
        Player.move_right()

    Player.set_vars()

    if click[0] and time_count > 10:
        time_count = 0
        bullet_list.append(())
        bullet_list[len(bullet_list) - 1] = Bullets()

    for i in bullet_list:
        bullet = i
        bullet.draw()
        if bullet.move() >= 100:
            bullet_list.remove(i)

    time_count += 1

    scroll_x -= (Playerx + scroll_x - 250) * .1
    scroll_y -= (Playery + scroll_y - 250) * .1

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
