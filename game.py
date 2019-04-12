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
RESPAW_ALIEN = 1300


# IMAGENS
playerImage = pygame.image.load("player.png")
alienImage = pygame.image.load("alien.png")
background = pygame.image.load("background.png")
shotImage = pygame.image.load("bullet.png")
explosionImage = pygame.image.load("explosion.png")


class Actor:

    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def update(self):
        pass


class Player(Actor):

    def __init__(self):
        Actor.__init__(self, playerImage)
        self.life = 1
        # A CADA SPACE apertado somente sai um tiro
        self.reloading = 0
        # CRIA O PLAYER NO MEIO DA TELA
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


class Explosion(Actor):

    def __init__(self, actor):
        Actor.__init__(self, explosionImage)
        self.life = 10
        self.rect.center = actor.rect.center

    def update(self):
        self.life = self.life - 1


pygame.init()

screen = pygame.display.set_mode(SCREENRECT.size)

# CRIA AS SPRITES
player = Player()
aliens = [Alien()]
shots = []
explosions = []

tempo = 0
clock = pygame.time.Clock()

# LOOP ENQUANTO O PLAYER ESTA VIVO
while player.life:

    # EVENTO DE EXIT
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    dt = clock.tick()

    tempo += dt

    if tempo > RESPAW_ALIEN:
        aliens.append(Alien())
        tempo = 0

    # MOVE O JOGADOR
    direction = keystate[K_RIGHT] - keystate[K_LEFT]
    player.move(direction)

    # CRIA O TIRO
    if not player.reloading and keystate[K_SPACE] and len(shots) < MAX_SHOTS:
        shots.append(Shot(player))
    player.reloading = keystate[K_SPACE]

    # LIMPA TIROS E EXPLOSOES
    for shot in shots:
        if shot.rect.top <= 0:
            shots.remove(shot)
    for explosion in explosions:
        if explosion.life <= 0:
            explosions.remove(explosion)

    # ATUALIZA O RECT DOS OBJETOS
    for actor in [player] + aliens + shots + explosions:
        actor.update()

    # CRIA COLISAO
    alienrects = []
    for a in aliens:
        alienrects.append(a.rect)

    # collidelist retorna -1 caso falso ou o index
    hit = player.rect.collidelist(alienrects)
    if hit != -1:
        alien = aliens[hit]
        explosions.append(Explosion(alien))
        explosions.append(Explosion(player))
        player.life = player.life - 1
    for shot in shots:
        hit = shot.rect.collidelist(alienrects)
        if hit != -1:
            alien = aliens[hit]
            explosions.append(Explosion(alien))
            shots.remove(shot)
            aliens.remove(alien)
            # CRIA NOVO ALIEN
            aliens.append(Alien())
            break

    # BLIT NOS RECTS PARA ATUALIZAR A TELA
    screen.blit(background, (0, 0))
    for a in aliens:
        screen.blit(alienImage, a.rect)
    screen.blit(playerImage, player.rect)
    for shot in shots:
        screen.blit(shotImage, shot.rect)
    for explosion in explosions:
        screen.blit(explosionImage, explosion.rect)
    pygame.display.flip()
