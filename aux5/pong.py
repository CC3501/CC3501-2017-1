# coding=utf-8
"""
Juego sencillo Pong
"""

# Importación de librerías
from ball import Ball
from constants import *
from player import Player
from pygame.locals import *
from sounds import Sounds
import os
import pygame
import random

# Se inician módulos
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Se cargan recursos
sounds = Sounds()
icon = pygame.image.load(ICON)
font = pygame.font.Font(FONT, 40)

# Se inicia la pantalla
surface = pygame.display.set_mode((SWIDTH, SHEIGHT))
pygame.display.set_caption('Pong')
pygame.display.set_icon(icon)

# Se crea el reloj
clock = pygame.time.Clock()

# Creamos los jugadores
player1 = Player(0, SHEIGHT / 2, 10, COLOR_WHITE, surface, sounds)
player2 = Player(SWIDTH - 20, SHEIGHT / 2, 10, COLOR_WHITE, surface, sounds)

# Creamos la bolita
ball = Ball([SWIDTH / 2, SHEIGHT / 2], COLOR_WHITE, surface, player1, player2,
            sounds)

# Entra en bucle principal
while True:

    # Setea el reloj
    clock.tick(FPS)

    # Busca eventos de aplicación
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # Ve teclas pulsadas
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        player1.move_up()
    elif keys[K_s]:
        player1.move_down()
    if keys[K_UP]:
        player2.move_up()
    elif keys[K_DOWN]:
        player2.move_down()

    # Dibuja la pantalla
    surface.fill(COLOR_BLACK)

    # Dibuja los jugadores
    player1.draw()
    player2.draw()

    # Movemos la bolita y detectamos colisiones
    ball.move()

    # Detectamos quien gana
    if player1.is_dead() or player2.is_dead():

        # Borra el fondo
        surface.fill(COLOR_BLACK)

        if player1.is_dead():
            text = font.render('GANA JUGADOR 2', 1, COLOR_WHITE)
            surface.blit(text, (SWIDTH / 2 - 250, SHEIGHT / 2 - 30))
        else:
            text = font.render('GANA JUGADOR 1', 1, COLOR_WHITE)
            surface.blit(text, (SWIDTH / 2 - 250, SHEIGHT / 2 - 30))

        # Detiene a los modelos
        ball.stop()
        player1.stop()
        player2.stop()

        # Vuelca lo dibujado en pantalla
        pygame.display.flip()

    else:

        # Dibuja la linea
        pygame.draw.line(surface, COLOR_GRAY, [SWIDTH / 2, 0],
                         [SWIDTH / 2, SHEIGHT], 2)

        # Dibujamos la bolita
        ball.draw()

        # Dibuja la vida
        v1 = font.render(player1.get_life(), 1, COLOR_WHITE)
        v2 = font.render(player2.get_life(), 1, COLOR_WHITE)
        surface.blit(v1, (30, 30))
        surface.blit(v2, (SWIDTH - 70, 30))

        # Vuelca lo dibujado en pantalla
        pygame.display.flip()
