# coding=utf-8
"""
Test extended
"""
# Se importa opengl
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *
import os
import pygame
from utils import *

# Configuraciones
COLOR_BLACK = [0, 0, 0, 1]
COLOR_RED = [1.0, 0.0, 0.0, 1.0]
COLOR_WHITE = [1.0, 1.0, 1.0, 1.0]
FPS = 60
WINDOW_SIZE = [800, 600]


# noinspection PyShadowingNames
def square(color=COLOR_RED):
    """
    Función que crea un cuadrado de arista 1.0
    """
    a = Point3(-1.0, -1.0, -1.0)
    b = Point3(1.0, -1.0, -1.0)
    c = Point3(1.0, -1.0, 1.0)
    d = Point3(-1.0, -1.0, 1.0)
    e = Point3(-1.0, 1.0, -1.0)
    f = Point3(1.0, 1.0, -1.0)
    g = Point3(1.0, 1.0, 1.0)
    h = Point3(-1.0, 1.0, 1.0)

    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    glBegin(GL_QUADS)
    glColor4fv(color)
    drawVertexListCreateNormal([a, b, c, d])
    drawVertexListCreateNormal([b, f, g, c])
    drawVertexListCreateNormal([f, e, h, g])
    drawVertexListCreateNormal([e, a, d, h])
    drawVertexListCreateNormal([d, c, g, h])
    drawVertexListCreateNormal([a, e, f, b])
    glEnd()
    glPopMatrix()
    glEndList()
    return obj


# Se crea la ventana
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]),
                        OPENGLBLIT | DOUBLEBUF)
pygame.display.set_caption('Ejemplo extendido en Pygame')
pygame.mouse.set_pos(WINDOW_SIZE[0] / 2,
                     WINDOW_SIZE[1] / 2)  # Centramos el mouse
clock = pygame.time.Clock()

# Se inicia OpenGl
glClearColor(*COLOR_BLACK)  # Color de fondo
glClearDepth(1.0)  # Profundidad color de fondo
glShadeModel(GL_SMOOTH)  # Smooth

# Depth test
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LEQUAL)

glEnable(GL_NORMALIZE)  # Normales normalizadas
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)  # Corrección de perspectiva

# Se inician las luces
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)

# Color de luz
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 1)
glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, 0.0, -1.0, 1.0])
glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)
glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0)
glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0)

# Reshape
glLoadIdentity()

# Se crea el viewport
glViewport(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
glMatrixMode(GL_PROJECTION)

# Se deja la camara en perspectiva
gluPerspective(60, float(WINDOW_SIZE[0]) / float(WINDOW_SIZE[1]), 300,
               20000)

# Se deja el modo en modelo
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()


class Figure(object):
    """
    Clase sencilla de figura
    """

    def __init__(self, figurelist):
        self.figure = figurelist
        self.pos = [0, 0, 0]
        self.angle = 0
        self.rot = [0, 0, 0]
        self.color = [0.5, 0.5, 0.5, 1.0]
        self.size = [400, 400, 400]


cubo = Figure(square())
# noinspection PyArgumentEqualDefault
axis = create_axes(2000, False, False)

# Bucle principal
while True:
    clock.tick(FPS)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Ubica la cámara
    glLoadIdentity()
    gluLookAt(1500, 1500, 1500,
              0, 0, 0,
              0, 0, 1)

    glDisable(GL_LIGHTING)
    glCallList(axis)
    glEnable(GL_LIGHTING)

    # Se comprueban eventos
    for event in pygame.event.get():
        if event.type == QUIT:  # Cierra la aplicación
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Cierra la aplicación
                exit()

    glLightfv(GL_LIGHT0, GL_POSITION, (800, 800, 800))  # Luz fija

    # Carga el material
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT,
                 [0.19225, 0.19225, 0.19225, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,
                 [0.50754, 0.50754, 0.50754, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR,
                 [0.508273, 0.508273, 0.508273, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0.4 * 128)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

    glPushMatrix()
    glTranslate(*cubo.pos)
    glScale(*cubo.size)
    glRotatef(cubo.angle, *cubo.rot)
    glCallList(cubo.figure)
    glPopMatrix()

    # Vuelca contenido a pantalla
    pygame.display.flip()
