import pygame


def scale_img(img, factor):
    size = img.get_width() / factor, img.get_height() / factor
    return pygame.transform.scale(img, size)


def resize_img(img, sizex, sizey):
    return pygame.transform.scale(img, (sizex, sizey))


def draw_img(screen, img, x, y, scx, scy, zoom):
    screen.blit(img, ((x + scx) / zoom, (y + scy) / zoom))

