# coding=utf-8
# Importación
import pygame
from pygame.locals import *
import random

# Constantes
PROBABILIDAD = 0.5


# Funciones utilitarias
def load_image(imagen):
    return pygame.image.load(imagen)


class Chansey(object):
    def __init__(self, initx, inity, texture, life, screen):
        """
        Constructor
        :param initx: Posición inicial 
        :param inity: Posición final
        :param texture: 
        :param life:
        """
        self.x = initx
        self.y = inity
        self.tex = texture
        self.life = life
        self.dead = False
        self.dx = 150
        self.c = initx
        self.screen = screen
        self.dir = 0  # Dirección

    def draw(self):
        self.screen.blit(self.tex, (self.x, self.y))

    def moverizq(self):
        if self.dir != -1:
            self.x -= self.dx
            self.dir = -1

    def movercentro(self):
        if self.dir != 0:
            self.x = self.c
            self.dir = 0

    def moverder(self):
        if self.dir != 1:
            self.x += self.dx
            self.dir = 1

    def getx(self):
        return self.x

    def gety(self):
        return self.y


class Huevo:
    def __init__(self, x, y, vel, ac, chansey):
        self.x = x
        self.y = y
        self.vel = vel
        self.ac = ac
        self.mono = chansey

    def update(self, t):
        self.vel += self.ac * t
        self.y = self.y + self.vel * t


# Función principal
def main():
    # Volcar los drivers en windows
    pygame.init()

    # Se hace la ventana
    screen = pygame.display.set_mode((640, 480))

    # Pongo el título
    pygame.display.set_caption('Chansey auxiliar 4')

    # Cargo las imágenes
    background = pygame.image.load('res/background.gif')
    grass = pygame.image.load('res/grass.png')
    mono = pygame.image.load('res/actor.png')
    huevo = load_image('res/huevo.png')
    icono = load_image('res/icon.png')

    # Cargo sonidos
    snd_eat = pygame.mixer.Sound('res/catch.wav')
    snd_main = pygame.mixer.Sound('res/sound.wav')

    # Cargo las fuentes
    font = pygame.font.Font('res/font.ttf', 30)

    # Objeto reloj (para las iteraciones)
    clock = pygame.time.Clock()

    # Establezco el ícono
    pygame.display.set_icon(icono)

    # Reproduzco el sonido principal
    snd_main.play(-1)

    # Creo el mono
    mono = Chansey(278, 370, mono, 3, screen)

    # Lista de huevos
    huevos = []

    # Bucle del juego
    while True:
        clock.tick(30)

        # Agrega un huevo
        if random.random() < PROBABILIDAD:
            h = Huevo(150 * random.choice([-1, 1, 0]) + 278, 0, 10, 10, mono)
            huevos.append(h)

        # Redibujar el fondo
        screen.blit(background, (0, 0))
        screen.blit(grass, (0, 30))

        # Veo eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        # Veo teclas que se están presionando
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            mono.moverizq()
        elif keys[K_RIGHT]:
            mono.moverder()
        else:
            mono.movercentro()

        # Dibujo el mono
        mono.draw()

        # Dibujo los huevos
        for i in huevos:
            i.update(10)
            screen.blit(huevo, (i.x, i.y))

        # Volvo el screen
        pygame.display.flip()


# Codigo principal
if __name__ == '__main__':
    main()
