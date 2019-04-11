import sys
import random
import pygame
from pygame.locals import *

# CONSTANTES

SCREENRECT = Rect(0, 0, 640, 640)
PLAYER_SPEED = 12

pygame.init()


screen = pygame.display.set_mode(SCREENRECT.size)


alien = pygame.image.load("alien.png")
alienrect = alien.get_rect()

player = pygame.image.load("player.png")
playerrect = alien.get_rect()
playerrect.centerx = SCREENRECT.centerx
playerrect.bottom = SCREENRECT.bottom - 25

background = pygame.image.load("background.png")

alienspeed = [5, 0]
while 1:

    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    playedirection = keystate[K_RIGHT] - keystate[K_LEFT]
    playerrect = playerrect.move(
        playedirection*10, 0).clamp(SCREENRECT)

    alienrect = alienrect.move(alienspeed)
    if alienrect.left < 0 or alienrect.right > SCREENRECT.width:
        alienspeed[0] = -alienspeed[0]
        alienrect.top = alienrect.bottom + 0.2
    if alienrect.bottom > SCREENRECT.height:
        alienrect = alien.get_rect()

    screen.blit(background, (0, 0))
    screen.blit(alien, alienrect)
    screen.blit(player, playerrect)
    pygame.display.flip()
