# coding=utf-8
"""
Ejemplo con toolbox
"""

# Importación de librerías
from pygltoolbox.glpython import *
from pygltoolbox.opengl_lib import *
from pygltoolbox.camera import *
from pygltoolbox.particles import *
from pygltoolbox.figures import *
from pygltoolbox.materials import *

# Constantes
AXES_LENGTH = 700
CAMERA_PHI = 45
CAMERA_RAD = 2000.0
CAMERA_ROT_VEL = 2.5
CAMERA_THETA = 56
FPS = 60
WINDOW_SIZE = [800, 600]

# Se inicia ventana
initPygame(WINDOW_SIZE[0], WINDOW_SIZE[1], "Ejemplo Ejes", centered=True)
initGl(transparency=False, materialcolor=False, normalized=True, lighting=True,
       numlights=1,
       perspectivecorr=True, antialiasing=True, depth=True, smooth=True,
       texture=True, verbose=True)
reshape(*WINDOW_SIZE)

# noinspection PyArgumentEqualDefault
initLight(GL_LIGHT0)
clock = pygame.time.Clock()

# Se crean objetos
axis = create_axes(AXES_LENGTH)  # Ejes
camera = CameraR(CAMERA_RAD, CAMERA_PHI,
                 CAMERA_THETA)  # Cámara del tipo esférica

cubo = Particle(0, 0, 0)
cubo.add_property('GLLIST', create_cube())
cubo.add_property('SIZE', [400, 400, 400])
cubo.add_property('MATERIAL', material_gold)
cubo.set_name('Cubo')

luz = Particle(1000, 1000, 100)
luz.set_name('Luz')
luz.add_property('GLLIST', create_cube())
luz.add_property('SIZE', [15, 15, 15])
luz.add_property('MATERIAL', material_silver)
luz.set_ang_vel_x(1, True)
luz.set_ang_vel_y(-1, True)

# Bucle principal
while True:
    clock.tick(FPS)
    clearBuffer()
    camera.place()
    if islightEnabled():
        glDisable(GL_LIGHTING)
        glCallList(axis)
        glEnable(GL_LIGHTING)
    else:
        glCallList(axis)

    # Se actualizan modelos
    luz.update()
    cubo.update()

    # Se comprueban eventos
    for event in pygame.event.get():
        if event.type == QUIT:  # Cierra la aplicación
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Cierra la aplicación
                exit()

    # Dibuja luces
    luz.exec_property_func('MATERIAL')
    glLightfv(GL_LIGHT0, GL_POSITION, luz.get_position_list())
    # noinspection PyArgumentEqualDefault
    draw_list(luz.get_property('GLLIST'), luz.get_position_list(), 0, None,
              luz.get_property('SIZE'), None)

    # Dibuja modelos
    cubo.exec_property_func('MATERIAL')
    # noinspection PyArgumentEqualDefault
    draw_list(cubo.get_property('GLLIST'), cubo.get_position_list(), 0, None,
              cubo.get_property('SIZE'), None)

    pygame.display.flip()
