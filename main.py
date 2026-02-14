import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()