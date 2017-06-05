# coding=utf-8
"""
Jugador
"""

# Importación de librerías
from centered_figure import CenteredFigure

# Importación de constantes
from constants import SWIDTH, SHEIGHT, COLOR_WHITE


class Player(object):
    def __init__(self, x, y, vel, color, surface, sounds):
        """
        Crea la paleta en una posición x, y
        :param x: Posición en x
        :param y: Posición en y
        :param vel: Velocidad
        :param color: Color
        :param surface: Superficie del canvas
        :param sounds: Sonidos
        """
        self.center = [x, y]
        self.center_backup = [x, y]
        self.vel = vel
        self.color = color
        self.figure = CenteredFigure(
            [(0, 50), (20, 50), (20, -50), (0, -50)], self.center,
            color=color, pygame_surface=surface, width=0)
        self.vida = 3
        self.sounds = sounds

    def draw(self):
        """
        Dibuja al jugador
        :return: 
        """
        self.figure.draw()

    def reset(self):
        """
        Resetea la posición del jugador
        :return: 
        """
        self.center[0] = self.center_backup[0]
        self.center[1] = self.center_backup[1]

    def stop(self):
        """
        Detiene la bolita.

        :return: 
        """
        self.vel = 0

    def get_life(self):
        """
        Retorna la vida del jugador
        :return: 
        """
        return str(self.vida)

    def lose(self):
        """
        Pierde una vida y suena musica
        :return: 
        """
        self.vida -= 1
        self.sounds.die()

    def move_up(self):
        """
        Sube al jugador
        :return: 
        """
        self.center[1] = max(50, self.center[1] - self.vel)

    def move_down(self):
        """
        Baja al jugador
        :return: 
        """
        self.center[1] = min(SHEIGHT - 50, self.center[1] + self.vel)

    def get_figure(self):
        """
        Retorna la figura
        :return: 
        """
        return self.figure

    def is_dead(self):
        """
        Retorna true/false si está muerto o no
        :return: 
        """
        return self.vida < 0
