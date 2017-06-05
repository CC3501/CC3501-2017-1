# coding=utf-8
"""
CAMERA
Provee clases para manejar una cámara.

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
from OpenGL.GL import *
from OpenGL.GLU import *
from utils_math import *

# Constantes
CAMERA_CENTER_LIMIT_Z_DOWN = -3500
CAMERA_CENTER_LIMIT_Z_UP = 3500
CAMERA_CENTER_VEL = 10
CAMERA_DEFAULT_RVEL = 10
CAMERA_MIN_THETA_VALUE = 0.000001
CAMERA_NEGATIVE = -1.0
CAMERA_POSITIVE = 1.0
CAMERA_ROUNDED = 2
CAMERA_SPHERICAL = 0x0fb
CAMERA_XYZ = 0x0fa


# noinspection PyMethodMayBeStatic
class _Camera:
    """Clase abstracta"""

    def __init__(self):
        """Funcion constructora void"""
        pass

    def place(self):
        """Ubica la cámara en el mundo"""
        pass

    def move_x(self, direction=CAMERA_POSITIVE):
        """Mueve la posición de la cámara en el eje x"""
        pass

    def move_y(self, direction=CAMERA_POSITIVE):
        """Mueve la posición de la cámara en el eje y"""
        pass

    def move_z(self, direction=CAMERA_POSITIVE):
        """Mueve la posición de la cámara en el eje z"""
        pass

    def set_vel_move_x(self, vel):
        """Define la velocidad de movimiento de la cámara en el eje x"""
        pass

    def set_vel_move_y(self, vel):
        """Define la velocidad de movimiento de la cámara en el eje y"""
        pass

    def set_vel_move_z(self, vel):
        """Define la velocidad de movimiento de la cámara en el eje z"""
        pass

    def set_center_vel(self, vel):
        """Define la velocidad de acercamiento/alejamiento de la cámara"""
        pass

    def move_center_x(self, dist):
        """Mueve la coorenada x del centro de visión"""
        pass

    def move_center_y(self, dist):
        """Mueve la coorenada y del centro de visión"""
        pass

    def move_center_z(self, dist):
        """Mueve la coorenada z del centro de visión"""
        pass

    def rotate_center_z(self, angle):
        """Rota la posición en el eje z"""
        pass

    def far(self):
        """Aleja la posición de la cámara"""
        pass

    def close(self):
        """Acerca la posición de la cámara"""
        pass

    def setRvel(self, vel):
        """Define la velocidad radial con la que la cámara se mueve"""
        pass

    # noinspection PyRedeclaration
    def place(self):
        """Ubica la camara en el mundo"""
        pass

    def rotateX(self, angle):
        """Rota la posición eye en el eje X cartesiano"""
        pass

    def rotateY(self, angle):
        """Rota la posición eye en el eje Y cartesiano"""
        pass

    def rotateZ(self, angle):
        """Rota la posición eye en el eje Z cartesiano"""
        pass

    def convert_to_xyz(self):
        """Convierte el sistema esférico a cartesiano"""
        pass

    def __str__(self):
        """Retorna el estado de la cámara"""
        pass

    def get_name(self):
        """Retorna el nombre de la cámara"""
        pass

    # noinspection PyShadowingNames
    def set_name(self, name):
        """Define el nombre de la cámara"""
        pass


# Clase que maneja la camara
class CameraXYZ(_Camera):
    """Cámara en XYZ, pos es del tipo (x,y,z), permite rotación en z"""

    def __init__(self, pos, center, up=Point3(0, 0, 1)):
        """Función constructora"""
        _Camera.__init__(self)
        if isinstance(pos, Point3) and isinstance(center,
                                                  Point3) and isinstance(up,
                                                                         Point3):
            self.pos = Vector3(*pos.export_to_list())
            self.center = Vector3(*center.export_to_list())
            self.up = Vector3(*up.export_to_list())
        else:
            raise Exception("pos, center y up deben ser del tipo Point3")
        self.cameraVel = Vector3(1.0, 1.0, 1.0)
        self.viewVel = Vector3(1.0, 1.0, 1.0)
        self.angle = 45.0
        self.centerangle = 0.0
        self.centervel = Vector3(CAMERA_CENTER_VEL, CAMERA_CENTER_VEL,
                                 CAMERA_CENTER_VEL)
        self._name = "unnamed"

    def place(self):
        """Ubica la cámara en el mundo"""
        glLoadIdentity()
        gluLookAt(self.pos.get_x(), self.pos.get_y(), self.pos.get_z(),
                  self.center.get_x(), self.center.get_y(),
                  self.center.get_z(), self.up.get_x(), self.up.get_y(),
                  self.up.get_z())

    def move_x(self, direction=CAMERA_POSITIVE):
        """Mueve la posición de la cámara en el eje x"""
        self.pos.set_x(self.pos.get_x() + self.cameraVel.get_x() * direction)

    def move_y(self, direction=CAMERA_POSITIVE):
        """Mueve la posición de la cámara en el eje y"""
        self.pos.set_y(self.pos.get_y() + self.cameraVel.get_y() * direction)

    def move_z(self, direction=CAMERA_POSITIVE):
        """Mueve la posición de la cámara en el eje z"""
        self.pos.set_z(self.pos.get_z() + self.cameraVel.get_z() * direction)

    def set_vel_move_x(self, vel):
        """Define la velocidad de movimiento de la camara en el eje x"""
        self.cameraVel.set_x(vel)

    def set_vel_move_y(self, vel):
        """Define la velocidad de movimiento de la cámara en el eje y"""
        self.cameraVel.set_y(vel)

    def set_vel_move_z(self, vel):
        """Define la velocidad de movimiento de la cámara en el eje z"""
        self.cameraVel.set_z(vel)

    def set_center_vel(self, vel):
        """Define la velocidad de acercamiento/alejamiento de la cámara"""
        self.centervel = Vector3(abs(vel), abs(vel), abs(vel))

    def rotateX(self, ang):
        """Rota la posición con respecto al eje X"""
        x = self.pos.get_x()
        y = self.pos.get_y() * cos(ang) - self.pos.get_z() * sin(ang)
        z = self.pos.get_y() * sin(ang) + self.pos.get_z() * cos(ang)
        self.pos.set_x(x)
        self.pos.set_y(y)
        self.pos.set_z(z)

    def rotateY(self, ang):
        """Rota la posición de la cámara con respecto al eje Y"""
        x = self.pos.get_x() * cos(ang) + self.pos.get_z() * sin(ang)
        y = self.pos.get_y()
        z = -self.pos.get_x() * sin(ang) + self.pos.get_z() * cos(ang)
        self.pos.set_x(x)
        self.pos.set_y(y)
        self.pos.set_z(z)

    def rotateZ(self, ang):
        """Rota la posición de la cámara con respecto al eje Z"""
        x = self.pos.get_x() * cos(ang) - self.pos.get_y() * sin(ang)
        y = self.pos.get_x() * sin(ang) + self.pos.get_y() * cos(ang)
        z = self.pos.get_z()
        self.pos.set_x(x)
        self.pos.set_y(y)
        self.pos.set_z(z)

    def move_center_x(self, dist):
        """Mueve la coorenada x del centro de visión"""
        self.center.set_x(self.center.get_x() + dist)

    def move_center_y(self, dist):
        """Mueve la coorenada y del centro de visión"""
        self.center.set_y(self.center.get_y() + dist)

    def move_center_z(self, dist):
        """Mueve la coorenada z del centro de visión"""
        if (CAMERA_CENTER_LIMIT_Z_DOWN <= self.center.get_z() and dist < 0) or \
                (self.center.get_z() <= CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self.center.set_z(self.center.get_z() + dist)

    def rotate_center_z(self, angle):
        """Rota la posición en el eje z"""
        rad = math.sqrt(self.pos.get_x() ** 2 + self.pos.get_y() ** 2)
        self.pos.set_x(rad * cos(self.angle))
        self.pos.set_y(rad * sin(self.angle))

    def far(self):
        """Aleja la posición de la cámara
        @deprecated"""
        self.center += self.centervel

    def close(self):
        """Acerca la posicion de la camara"""
        self.center -= self.centervel

    def get_name(self):
        """Retorna el nombre de la cámara"""
        return self._name

    # noinspection PyShadowingNames
    def set_name(self, name):
        """Define el nombre de la cámara"""
        self._name = name


# noinspection PyUnresolvedReferences
class CameraR(_Camera):
    """Cámara en coordenadas esféricas, recibe un radio R, y angulos phi y theta"""

    def __init__(self, r=1.0, phi=45, theta=45, center_point=Point3(),
                 up_vector=Vector3(0, 0, 1)):
        """Función constructora"""
        _Camera.__init__(self)
        if isinstance(center_point, Point3):
            if isinstance(up_vector, Vector3):
                if r > 0:
                    if 0 <= phi <= 360 and 0 <= theta <= 180:
                        self.r = r
                        self.phi = phi
                        self.theta = theta
                        self.center = center_point
                        self.up = up_vector
                        self.rvel = CAMERA_DEFAULT_RVEL
                        self._name = "unnamed"
                    else:
                        raise Exception(
                            "el angulo phi debe variar entre 0 y 360, theta debe variar entre 0 y 180")
                else:
                    raise Exception("El radio debe ser mayor a cero""")
            else:
                raise Exception("up_vector debe ser del tipo vector3")
        else:
            raise Exception("center_point debe ser del tipo point3")

    def setRvel(self, vel):
        """Define la velocidad radial con la que la camara se mueve"""
        if vel > 0:
            self.rvel = vel
        else:
            raise Exception("la velocidad debe ser mayor a cero")

    def place(self):
        """Ubica la cámara en el mundo"""
        glLoadIdentity()
        gluLookAt(self.r * sin(self.theta) * cos(self.phi),
                  self.r * sin(self.theta) * sin(self.phi),
                  self.r * cos(self.theta),
                  self.center.get_x(), self.center.get_y(), self.center.get_z(),
                  self.up.get_x(), self.up.get_y(),
                  self.up.get_z())

    def __str__(self):
        """Retorna el estado de la camara"""
        x, y, z = self.convert_to_xyz()
        r = CAMERA_ROUNDED
        msg = 'Camera: {12}\nRadius: {0}\nPhi angle: {1}, Theta angle: {2}\nXYZ eye pos: ({3},{4},{5})\nXYZ center ' \
              'pos: ({6},{7},{8})\nXYZ up vector: ({9},{10},{11})'
        return msg.format(round(self.r, r), round(self.phi, r),
                          round(self.theta, r), round(x, r), round(y, r),
                          round(z, r), round(self.center.get_x(), r),
                          round(self.center.get_y(), r),
                          round(self.center.get_z(), r),
                          round(self.up.get_x(), r), round(self.up.get_y(), r),
                          round(self.up.get_z(), r), self.get_name())

    def far(self):
        """Aleja la cámara"""
        self.r += self.rvel

    def close(self):
        """Aleja la cámara"""
        self.r -= self.rvel

    def rotateX(self, angle):
        """Rota la posición eye en el eje X cartesiano"""
        # Convierto a (x,y,z)
        x, y, z = self.convert_to_xyz()
        # Roto las componentes (x,y,z) segun x en
        xr = x
        yr = y * cos(angle) - z * sin(angle)
        zr = y * sin(angle) + z * cos(angle)
        # Convierto a componentes esfericas y se guardan
        r, phi, theta = xyz_to_spr(xr, yr, zr)
        self.r = r
        self.phi = phi
        self.theta = theta

    def rotateY(self, angle):
        """Rota la posición eye en el eje Y cartesiano"""
        self.theta = min(max(self.theta + angle, CAMERA_MIN_THETA_VALUE), 180)

    def rotateZ(self, angle):
        """Rota la posición eye en el eje Z cartesiano"""
        self.phi = (self.phi + angle) % 360

    def convert_to_xyz(self):
        """Convierte el sistema esférico a cartesiano"""
        return spr_to_xyz(self.r, self.phi, self.theta)

    def move_center_x(self, dist):
        """Mueve la coorenada x del centro de visión"""
        self.center.set_x(self.center.get_x() + dist)

    def move_center_y(self, dist):
        """Mueve la coorenada y del centro de visión"""
        self.center.set_y(self.center.get_y() + dist)

    def move_center_z(self, dist):
        """Mueve la coorenada z del centro de visión"""
        if (CAMERA_CENTER_LIMIT_Z_DOWN <= self.center.get_z() and dist < 0) or \
                (self.center.get_z() <= CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self.center.set_z(self.center.get_z() + dist)

    def get_name(self):
        """Retorna el nombre de la cámara"""
        return self._name

    # noinspection PyShadowingNames
    def set_name(self, name):
        """Define el nombre de la cámara"""
        self._name = name

    def getRadius(self):
        """Retorna el radio de la cámara"""
        return self.r

    def setRadius(self, r):
        """Define el radio de la cámara"""
        self.r = r

    def getPhi(self):
        """Retorna el angulo phi"""
        return self.phi

    def setPhi(self, phi):
        """Define el angulo phi"""
        self.phi = phi

    def getTheta(self):
        """Retorna el angulo theta"""
        return self.theta

    def setTheta(self, theta):
        """Define el angulo theta"""
        self.theta = theta
