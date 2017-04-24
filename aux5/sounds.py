# coding=utf-8
"""
Administrador de sonidos
"""

# Importación de librerías
import pygame.mixer
from constants import *
import random


class Sounds(object):
    def __init__(self):
        """
        Constructor.
        
        """
        self._sound_pong = [pygame.mixer.Sound(PONG_SOUND1),
                            pygame.mixer.Sound(PONG_SOUND2)]
        self._sound_dead = pygame.mixer.Sound(END_SOUND)
        self._sound_rebote = pygame.mixer.Sound(REBOTE_SOUND)

    def pong(self):
        """
        Elige un sonido aleatorio al tocar los pong.
        
        :return: 
        """
        s = random.choice(self._sound_pong)
        s.play(0)

    def die(self):
        """
        Reproduce sonido de muerte.
        
        :return: 
        """
        self._sound_dead.play(0)

    def rebote(self):
        """
        Reproduce sonido de rebote.
        
        :return: 
        """
        self._sound_rebote.play(0)
