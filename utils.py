import pygame


def scale_img(img, factor):
    size = img.get_width() / factor, img.get_height() / factor
    return pygame.transform.scale(img, size)


def resize_img(img, size_x, size_y):
    return pygame.transform.scale(img, (size_x, size_y))


def draw_img(screen, img, x, y, scx, scy, zoom):
    screen.blit(img, ((x + scx) / zoom, (y + scy) / zoom))
