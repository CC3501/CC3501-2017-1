# coding=utf-8
"""
GLPYTHON
Funciones utilitarias para manejar PyOpenGL.

Copyright (C) 2017 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Importación de librerías
import pygame
from pygame.locals import *
import os

# Constantes
_DEFAULT_CAPTION = "Program title"


def initPygame(w, h, caption=_DEFAULT_CAPTION, center_mouse=False, icon=None, centered=False):
    """
    Inicia Pygame

    :param w: Ancho de la ventana (px)
    :param h: Alto de la ventana (px)
    :param caption: Título de la ventana
    :param center_mouse: Indica si el mouse está centrado
    :param icon: Indica el ícono de la ventana
    :param centered: Indica si la ventana está centrada
    :return: None
    """
    pygame.init()
    if centered:
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_mode((w, h), OPENGLBLIT | DOUBLEBUF)
    pygame.display.set_caption(caption)
    if center_mouse:
        pygame.mouse.set_pos(w / 2, h / 2)
    if icon is not None:
        pygame.display.set_icon(icon)


# noinspection PyBroadException,PyUnresolvedReferences
def loadPythonImage(path, convert=False):
    """Carga una imagen en pygame"""
    try:
        image = pygame.image.load(path)
        if convert:
            image = image.convert_alpha()
        return image
    except:
        print "fail"
        return None
