# coding=utf-8
"""
Bolita del juego
"""

# Importación de librerías
from centered_figure import CenteredFigure
from constants import SWIDTH, SHEIGHT
import random
import copy


class Ball(object):
    def __init__(self, center, color, surface, player1, player2, sounds):
        """
        Bolita
        :param center: Posición del centro
        :param color: Color de la bolita
        :param surface: Canvas del juego
        :param player1: Jugador 1
        :type player1: Player
        :param player2: Jugador 2
        :type player2: Player
        :param sounds: Sonidos
        """
        self.center = copy.copy(center)
        self.center_backup = copy.copy(center)
        self.vel = [0, 0]
        self.random_velocity()
        self.figure = CenteredFigure(
            [(-1, 1), (1, 1), (1, -1), (-1, -1)], center=self.center,
            color=color, pygame_surface=surface)
        self.figure.scale(15)
        self.p1 = player1
        self.p2 = player2
        self.sounds = sounds

    def draw(self):
        """
        Dibujamos la bolita
        :return: 
        """
        self.figure.draw()

    def random_velocity(self):
        """
        Crea una velocidad aleatoria.
        
        :return: 
        """

        self.vel[0] = random.randrange(1, 10) * random.choice([-1, 1])
        self.vel[1] = random.randrange(1, 5) * random.choice([-1, 1])

    def reset(self):
        """
        Resetea la velocidad y la posición.
        
        :return: 
        """
        self.random_velocity()
        self.center[0] = self.center_backup[0]
        self.center[1] = self.center_backup[1]

        # Resteamos los jugadores
        self.p1.reset()
        self.p2.reset()

    def stop(self):
        """
        Detiene la bolita.
        
        :return: 
        """
        self.vel[0] = 0
        self.vel[1] = 0

    def move(self):
        """
        Movemos la bolita y detectamos colisiones
        :return: 
        """
        self.center[0] = self.center[0] + self.vel[0]
        self.center[1] = self.center[1] + self.vel[1]

        # Vemos colisión con techos
        if self.center[1] < 0:
            self.center[1] = 0
            self.vel[1] *= -1
            self.sounds.rebote()
        if self.center[1] > SHEIGHT - 15:
            self.center[1] = SHEIGHT - 15
            self.vel[1] *= -1
            self.sounds.rebote()

        # Vemos colisión con jugadores
        if self.vel[0] > 0:  # Jugador 2 debe tocar
            if self.figure.intersect(self.p2.get_figure()):
                self.vel[0] = - self.vel[0] - 2
                self.vel[1] = self.vel[1] + random.randrange(-1, 1)
                self.sounds.pong()
            if self.center[0] > SWIDTH:
                self.p2.lose()
                self.reset()
        if self.vel[0] < 0:  # Jugador 1 debe tocar
            if self.figure.intersect(self.p1.get_figure()):
                self.vel[0] = - self.vel[0] + 2
                self.vel[1] = self.vel[1] + random.randrange(-1, 1)
                self.sounds.pong()
            if self.center[0] < 0:
                self.p1.lose()
                self.reset()
