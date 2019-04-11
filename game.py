import sys
import random
import pygame
from pygame.locals import *

# CONSTANTES
SCREENRECT = Rect(0, 0, 640, 640)
PLAYER_SPEED = 12
ALIEN_SPEED = 10
SHOT_SPEED = 10
MAX_SHOTS = 2


# IMAGENS
playerImage = pygame.image.load("player.png")
alienImage = pygame.image.load("alien.png")
background = pygame.image.load("background.png")
shotImage = pygame.image.load("bullet.png")


class Actor:

    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def update(self):
        pass


class Player(Actor):

    def __init__(self):
        Actor.__init__(self, playerImage)
        # A CADA SPACE apertado somente sai um tiro
        self.reloading = 0
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


class Shot(Actor):

    def __init__(self, player):
        Actor.__init__(self, shotImage)
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top - 10

    def update(self):
        self.rect.top = self.rect.top - SHOT_SPEED


pygame.init()

screen = pygame.display.set_mode(SCREENRECT.size)

# CRIA AS SPRITES
player = Player()
alien = Alien()
shots = []

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

    # CRIA O TIRO
    if not player.reloading and keystate[K_SPACE] and len(shots) < MAX_SHOTS:
        shots.append(Shot(player))
    player.reloading = keystate[K_SPACE]

    # LIMPA O TIRO FORA DA TELA
    for shot in shots:
        if shot.rect.top <= 0:
            shots.remove(shot)

    # ATUALIZA O RECT DOS OBJETOS
    for actor in [player] + [alien] + shots:
        actor.update()

    # UPDATE NOS RECT PARA ATUALIZAR A TELA
    screen.blit(background, (0, 0))
    screen.blit(alienImage, alien.rect)
    screen.blit(playerImage, player.rect)
    for shot in shots:
        screen.blit(shotImage, shot.rect)
    pygame.display.flip()
