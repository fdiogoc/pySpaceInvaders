import sys
import random
import pygame
from pygame.locals import *

# CONSTANTES
SCREENRECT = Rect(0, 0, 640, 640)
PLAYER_SPEED = 12
ALIEN_SPEED = 10


# IMAGENS
playerImage = pygame.image.load("player.png")
alienImage = pygame.image.load("alien.png")
background = pygame.image.load("background.png")


class Actor:

    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()


class Player(Actor):

    def __init__(self):
        Actor.__init__(self, playerImage)
        self.rect.centerx = SCREENRECT.centerx
        self.rect.bottom = SCREENRECT.bottom - 25

    def move(self, direction):
        self.rect = self.rect.move(
            direction*PLAYER_SPEED, 0).clamp(SCREENRECT)


class Alien(Actor):

    def __init__(self):
        Actor.__init__(self, alienImage)
        # DIRECAO DO ALIEN - direção nevativa ele volta
        self.speed = random.choice((-1, 1)) * ALIEN_SPEED
        if self.speed < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        global SCREENRECT
        self.rect[0] = self.rect[0] + self.speed
        if not SCREENRECT.contains(self.rect):
            self.speed = -self.speed
            self.rect.top = self.rect.bottom + 3
            self.rect = self.rect.clamp(SCREENRECT)


pygame.init()

screen = pygame.display.set_mode(SCREENRECT.size)

# CRIA AS SPRITES
player = Player()
alien = Alien()

# LOOP ETERNO
while 1:

    # EVENTO DE EXIT
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # MOVE O JOGADOR
    direction = keystate[K_RIGHT] - keystate[K_LEFT]
    player.move(direction)

    # MOVE O ALIEN
    alien.update()

    screen.blit(background, (0, 0))
    screen.blit(alienImage, alien.rect)
    screen.blit(playerImage, player.rect)
    pygame.display.flip()
