# coding=utf-8
"""
UTILS GEOMETRY
Provee funciones para dibujar planos y objetos de forma sencilla mediante opengl.
"""

# Importación de librerías
from OpenGL.GL import *
from utils_math import *


def drawVertexList(vertex_list):
    """Dibuja una lista de puntos Point2/Point3"""
    if len(vertex_list) >= 1:
        if vertex_list[0].get_type() == POINT_2:
            for vertex in vertex_list:
                glVertex2fv(vertex.export_to_list())
        elif vertex_list[0].get_type() == POINT_3:
            for vertex in vertex_list:
                glVertex3fv(vertex.export_to_list())
    else:
        raise Exception("lista vacia")


def drawVertexListNormal(normal, vertex_list):
    """Dibuja una lista de puntos Point2/Point3 con una normal"""
    if len(vertex_list) >= 3:
        if isinstance(normal, Vector3):
            glNormal3fv(normal.export_to_list())
            drawVertexList(vertex_list)
        else:
            raise Exception("la normal debe ser del tipo vector3")
    else:
        raise Exceptiom("vertices insucifientes")


def drawVertexListCreateNormal(vertex_list):
    """Dibuja una lista de puntos point2/point3 creando una normal"""
    if len(vertex_list) >= 3:
        normal = normal3points(vertex_list[0], vertex_list[1], vertex_list[2])
        drawVertexListNormal(normal, vertex_list)
    else:
        raise Exceptiom("vertices insucifientes")


def drawVertexList_textured(vertex_list, tvertex_list):
    """Dibuja una lista de puntos point2/point3 con una lista Point2 de aristas
    para modelos texturados"""
    if len(vertex_list) >= 1:
        if vertex_list[0].get_type() == POINT_2:
            for vertex in range(len(vertex_list)):
                glTexCoord2fv(tvertex_list[vertex].export_to_list())
                glVertex2fv(vertex_list[vertex].export_to_list())
        elif vertex_list[0].get_type() == POINT_3:
            for vertex in range(len(vertex_list)):
                glTexCoord2fv(tvertex_list[vertex].export_to_list())
                glVertex3fv(vertex_list[vertex].export_to_list())
        else:
            raise Exception("el tipo de vertex_list debe ser POINT2 o POINT3")
    else:
        raise Exception("lista vacia")


def drawVertexListNormal_textured(normal, vertex_list, tvertex_list):
    """Dibuja una lista de puntos Point2/Point3 con una lista Point2 de aristas
    para modelos texturados con una normal"""
    if len(vertex_list) >= 1:
        if len(tvertex_list) >= 3:
            if isinstance(normal, Vector3):
                glNormal3fv(normal.export_to_list())
                drawVertexList_textured(vertex_list, tvertex_list)
            else:
                raise Exception("la normal debe ser del tipo vector3")
        else:
            raise Exception("vertices insuficientes")
    else:
        raise Exception("lista vacia")


def drawVertexListCreateNormal_textured(vertex_list, tvertex_list):
    """Dibuja una lista de puntos point3 con una lista Point2 de aristas para modelos
    texturados creando una normal"""
    if len(vertex_list) >= 3:
        normal = normal3points(vertex_list[0], vertex_list[1], vertex_list[2])
        drawVertexListNormal_textured(normal, vertex_list, tvertex_list)
    else:
        raise Exception("vertices insuficientes")


# noinspection PyDefaultArgument
def draw_list(lista, pos=[0.0, 0.0, 0.0], angle=0.0, rot=None, sz=None,
              rgb=None):
    """
    Dibuja una lista de OpenGl

    :param lista: Lista OpenGL
    :param pos: Posición
    :param angle: Lista de ángulos a rotar
    :param rot: Indica si rota o no
    :param sz: Escalado de imagen
    :param rgb: Colores del objeto
    :return:
    """
    glPushMatrix()
    glTranslate(pos[0], pos[1], pos[2])
    if sz is not None:
        glScale(sz[0], sz[1], sz[2])
    if rot is not None:
        glRotatef(angle, rot[0], rot[1], rot[2])
    if rgb is not None:
        glColor4fv(rgb)
    glCallList(lista)
    glPopMatrix()
