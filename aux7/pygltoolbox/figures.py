# coding=utf-8
"""
FIGURES
Funciones utilitarias para adminsitrar figuras en PyOpenGL.

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
from OpenGL.arrays import vbo
from numpy import array
from utils import *

# Constantes
COLOR_BLACK = [0.0, 0.0, 0.0, 1.0]
COLOR_BLUE = [0.0, 0.0, 1.0, 1.0]
COLOR_RED = [1.0, 0.0, 0.0, 1.0]
COLOR_GREEN = [0.0, 1.0, 0.0, 1.0]
COLOR_WHITE = [1.0, 1.0, 1.0, 1.0]
FIGURE_LIST = 0xfa01
FIGURE_VBO = 0xfa02
_ERRS = []
for i in range(10):
    _ERRS.append(False)


# noinspection PyDefaultArgument
class VboObject:
    """Objeto del tipo VBO el cual permite cargar y dibujar elementos usando shaders"""

    def __init__(self, vertex, fragment, total_vertex, texture=None):
        """Funcion constructora"""
        if isinstance(vertex, vbo.VBO) and isinstance(fragment, vbo.VBO):
            if isinstance(total_vertex, types.IntType):
                self.vertex = vertex
                self.fragment = fragment
                self.totalVertex = total_vertex
                self.texture = texture
                if self.texture is None:
                    self.texlen = 0
                else:
                    self.texlen = len(self.texture)
            else:
                raise Exception("total_vertex debe ser del tipo int")
        else:
            raise Exception(
                "vertex y fragment deben ser del tipo VBO (OpenGL.arrays.vbo)")

    def draw(self, pos=[0.0, 0.0, 0.0], rgb=None):
        """Dibuja el objeto"""
        try:
            glPushMatrix()

            # Se hace un bind entre los vbos y el programa del shader
            self.vertex.bind()
            glVertexPointerf(self.vertex)
            self.fragment.bind()
            glNormalPointerf(self.fragment)

            # Se activan los vbos
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_NORMAL_ARRAY)

            # Se activan las transformaciones
            if rgb is not None:
                glColor4fv(rgb)
            glTranslate(pos[0], pos[1], pos[2])

            # Se activan las texturas
            for _i in range(self.texlen):
                glActiveTexture(GL_TEXTURE0 + _i)
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture[_i])

            # Se dibujan los triangulos cada 3 elementos de los vbo
            glDrawArrays(GL_TRIANGLES, 0, self.totalVertex)

            # Se desactivan las texturas
            for _i in range(self.texlen):
                glActiveTexture(GL_TEXTURE0 + _i)
                glDisable(GL_TEXTURE_2D)

            # Se desactivan los vbos
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)

            glPopMatrix()

        except:
            raise Exception("error al dibujar el objeto vbo")


def loadOBJModel(file_name):
    """Carga un modelo almacenado en un archivo .obj"""
    file_text = open(file_name, "r")
    text = file_text.readlines()
    vertex = []
    normals = []
    uv = []
    faces_vertex = []
    faces_normal = []
    faces_uv = []
    for line in text:
        info = line.split(" ")
        if info[0] == "v":
            vertex.append(
                (float(info[1]), float(info[2]) - 0.1, float(info[3])))
        elif info[0] == "vn":
            normals.append((float(info[1]), float(info[2]), float(info[3])))
        elif info[0] == "vt":
            uv.append((float(info[1]), float(info[2])))
        elif info[0] == "f":
            p1 = info[1].split("/")
            p2 = info[2].split("/")
            p3 = info[3].split("/")
            faces_vertex.append((int(p1[0]), int(p2[0]), int(p3[0])))
            faces_uv.append((int(p1[1]), int(p2[1]), int(p3[1])))
            faces_normal.append((int(p1[2]), int(p2[2]), int(p3[2])))
    return vertex, normals, uv, faces_vertex, faces_normal, faces_uv


def loadGMSHModel(modelfile, scale, dx=0.0, dy=0.0, dz=0.0, avg=True,
                  neg_normal=False, texture=None):
    """Carga un modelo .msh o .gmsh almacenado en file y lo retorna en un objeto vboObject escalado en 'scale',
    por defecto las normales se promedian, para desactivar pruebe con avg=False. El modeo adicionalmente puede
    desplazarse en (dx, dy, dz), y revertir las normales si neg_normal es igual a True """

    # noinspection PyPep8Naming,PyUnboundLocalVariable,PyShadowingNames,PyUnusedLocal
    def load(gmshfile, scale, dx, dy, dz):
        """Carga un archivo gmsh y retorna 3 listas, una lista de vertices, otra de normales y otra de normales promedio. \n
        Toma como argumento el archivo, una escala y la posicion (dx,dy,dz)"""

        # noinspection PyPep8Naming,PyShadowingNames
        def getAveNormals(nodes, elems):
            """Calcula las normales promedio por cada vertice"""
            nodetrilist = []
            for nodenum in range(len(nodes)):
                nodetrilist.append([])
                for elemnum in range(len(elems)):
                    if nodenum in elems[elemnum]:
                        nodetrilist[nodenum].append(elemnum)
            avenorms = []
            for tri in nodetrilist:
                aveNi = 0.0
                aveNj = 0.0
                aveNk = 0.0
                denom = max(float(len(tri)), 1)
                for elem in tri:
                    vert1 = [nodes[elems[elem][0]][0], nodes[elems[elem][0]][1],
                             nodes[elems[elem][0]][2]]
                    vert2 = [nodes[elems[elem][1]][0], nodes[elems[elem][1]][1],
                             nodes[elems[elem][1]][2]]
                    vert3 = [nodes[elems[elem][2]][0], nodes[elems[elem][2]][1],
                             nodes[elems[elem][2]][2]]
                    normals = getNormals(vert1, vert2, vert3)
                    aveNi += normals[0]
                    aveNj += normals[1]
                    aveNk += normals[2]
                avenorms.append([aveNi / denom, aveNj / denom, aveNk / denom])
            return avenorms

        # noinspection PyPep8Naming
        def getNormals(vertA, vertB, vertC):
            """Calcula las normales por cada 3 vertices"""
            xA = vertA[0]
            xB = vertB[0]
            xC = vertC[0]
            yA = vertA[1]
            yB = vertB[1]
            yC = vertC[1]
            zA = vertA[2]
            zB = vertB[2]
            zC = vertC[2]
            ABx = xB - xA
            ABy = yB - yA
            ABz = zB - zA
            BCx = xC - xB
            BCy = yC - yB
            BCz = zC - zB
            Nx = ABy * BCz - ABz * BCy
            Ny = ABz * BCx - ABx * BCz
            Nz = ABx * BCy - ABy * BCx
            VecMag = math.sqrt(Nx ** 2 + Ny ** 2 + Nz ** 2)
            Ni = Nx / VecMag
            Nj = Ny / VecMag
            Nk = Nz / VecMag
            return [Ni, Nj, Nk]

        # Lee el archivo
        try:
            infile = open(gmshfile, 'r')
        except:
            raise Exception("el archivo del modelo no existe")

        # Crea el modeo
        try:
            gmshlines = infile.readlines()
            readnodes = False
            readelems = False
            skipline = 0
            elems = []
            lnum = 0
            nnodes = 0
            for line in gmshlines:
                if "$Nodes" in line:
                    readnodes = True
                    skipline = 2
                    nnodes = int(gmshlines[lnum + 1].strip())
                    nodes = []
                    for i in range(nnodes):
                        nodes.append(99999.9)
                elif "$EndNodes" in line:
                    readnodes = False
                    skipline = 1
                elif "$Elements" in line:
                    readelems = True
                    skipline = 2
                elif "$EndElements" in line:
                    readelems = False
                    skipline = 1
                if skipline < 1:
                    if readnodes:
                        nXYZ = line.strip().split()
                        nodenum = int(nXYZ[0]) - 1
                        nX = float(nXYZ[1]) * scale + dx
                        nY = float(nXYZ[2]) * scale + dy
                        nZ = float(nXYZ[3]) * scale + dz
                        if neg_normal:
                            nZ *= -1
                        nodes[nodenum] = [nX, nY, nZ]
                    elif readelems:
                        n123 = line.split()
                        if n123[1] == "2":
                            n1 = int(n123[-3]) - 1
                            n2 = int(n123[-1]) - 1
                            n3 = int(n123[-2]) - 1
                            elems.append([n1, n2, n3])
                else:
                    skipline -= 1
                lnum += 1
            triarray = []
            normarray = []
            avenorms = []
            nodeavenorms = getAveNormals(nodes, elems)
            for elem in elems:
                vert1 = [nodes[elem[0]][0], nodes[elem[0]][1],
                         nodes[elem[0]][2]]
                vert2 = [nodes[elem[1]][0], nodes[elem[1]][1],
                         nodes[elem[1]][2]]
                vert3 = [nodes[elem[2]][0], nodes[elem[2]][1],
                         nodes[elem[2]][2]]
                avenorm0 = nodeavenorms[elem[0]]
                avenorm1 = nodeavenorms[elem[1]]
                avenorm2 = nodeavenorms[elem[2]]
                normals = getNormals(vert1, vert2, vert3)
                triarray.append(vert1)
                triarray.append(vert2)
                triarray.append(vert3)
                normarray.append(normals)
                normarray.append(normals)
                normarray.append(normals)
                avenorms.append(avenorm0)
                avenorms.append(avenorm1)
                avenorms.append(avenorm2)
            return triarray, normarray, avenorms

        except:
            raise Exception("error al cargar el modelo")

    vertex, norm, avgnorm = load(modelfile, scale, float(dx), float(dy),
                                 float(dz))
    if avg:
        return VboObject(vbo.VBO(array(vertex, 'f')),
                         vbo.VBO(array(avgnorm, 'f')), len(vertex), texture)
    else:
        return VboObject(vbo.VBO(array(vertex, 'f')), vbo.VBO(array(norm, 'f')),
                         len(vertex), texture)


# noinspection PyBroadException
def create_sphere(lat=10, lng=10, color=COLOR_WHITE):
    """Crea una esfera con latitud y longitud definidos de radio 1.0"""
    if lat >= 3 and lng >= 10:
        obj = glGenLists(1)
        glNewList(obj, GL_COMPILE)
        glPushMatrix()
        glColor4fv(color)
        try:
            glutSolidSphere(1.0, lat, lng)
        except:
            if not _ERRS[0]:
                printGLError(
                    "la version actual de OpenGL no posee la funcion glutSolidSphere")
            _ERRS[0] = True
        glPopMatrix()
        glEndList()
        return obj
    else:
        raise Exception(
            "La latitud y longitud de la figura deben ser mayores a 3")


# noinspection PyDefaultArgument
def create_circle(rad=1.0, diff=0.1, normal=[0.0, 0.0, 1.0], color=COLOR_WHITE):
    """Crea un circulo"""
    if diff > 0:
        obj = glGenLists(1)
        glNewList(obj, GL_COMPILE)
        glPushMatrix()
        glColor4fv(color)
        ang = 0.0
        glBegin(GL_POLYGON)
        while ang <= 360.0:
            glNormal3fv(normal)
            glVertex2f(sin(ang) * rad, cos(ang) * rad)
            ang += diff
        glEnd()
        glBegin(GL_LINE_LOOP)
        while ang <= 360.0:
            glVertex2f(sin(ang) * rad, cos(ang) * rad)
            ang += diff
        glEnd()
        glPopMatrix()
        glEndList()
        return obj
    else:
        raise Exception("La diferencia debe ser mayor estricto a cero")


# noinspection PyBroadException
def create_cone(base=1.0, height=1.0, lat=20, lng=20, color=COLOR_WHITE):
    """Crea un cono de base y altura de radio 1.0"""
    if lat >= 3 and lng >= 10:
        circlebase = create_circle(base - 0.05, 0.1, [0.0, 0.0, -1.0], color)
        obj = glGenLists(1)
        glNewList(obj, GL_COMPILE)
        glPushMatrix()
        glColor4fv(color)
        try:
            glutSolidCone(base, height, lat, lng)
        except:
            if not _ERRS[3]:
                printGLError(
                    "la version actual de OpenGL no posee la funcion glutSolidCone")
            _ERRS[3] = True
        glCallList(circlebase)
        glPopMatrix()
        glEndList()
        return obj
    else:
        raise Exception(
            "La latitud y longitud de la figura deben ser mayores a 3")


def create_cube(color=COLOR_WHITE):
    """Crea un cubo de arista 1.0"""
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


def create_cube_textured(texture_list):
    """Crea un cubo con texturas"""
    a = Point3(-1.0, -1.0, -1.0)
    b = Point3(1.0, -1.0, -1.0)
    c = Point3(1.0, -1.0, 1.0)
    d = Point3(-1.0, -1.0, 1.0)
    e = Point3(-1.0, 1.0, -1.0)
    f = Point3(1.0, 1.0, -1.0)
    g = Point3(1.0, 1.0, 1.0)
    h = Point3(-1.0, 1.0, 1.0)
    t_list = [Point2(0, 0), Point2(1, 0), Point2(1, 1), Point2(0, 1)]

    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    for _i in range(len(texture_list)):
        glActiveTexture(GL_TEXTURE0 + _i)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_list[_i])
    glBegin(GL_QUADS)
    drawVertexListCreateNormal_textured([a, b, c, d], t_list)
    drawVertexListCreateNormal_textured([b, f, g, c], t_list)
    drawVertexListCreateNormal_textured([f, e, h, g], t_list)
    drawVertexListCreateNormal_textured([e, a, d, h], t_list)
    drawVertexListCreateNormal_textured([d, c, g, h], t_list)
    drawVertexListCreateNormal_textured([a, e, f, b], t_list)
    glEnd()
    for _i in range(len(texture_list)):
        glActiveTexture(GL_TEXTURE0 + _i)
        glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_torus(minr=0.5, maxr=1.0, lat=30, lng=30, color=COLOR_WHITE):
    """Crea un toro de radio menor minr y radio mayor maxr"""
    if lat >= 3 and lng >= 3:
        obj = glGenLists(1)
        glNewList(obj, GL_COMPILE)
        glPushMatrix()
        glColor4fv(color)
        try:
            glutSolidTorus(minr, maxr, lat, lng)
        except:
            if not _ERRS[2]:
                printGLError(
                    "la version actual de OpenGL no posee la funcion glutSolidTorus")
            _ERRS[2] = True
        glPopMatrix()
        glEndList()
        return obj
    else:
        raise Exception(
            "La latitud y longitud de la figura deben ser mayores a 3")


# noinspection PyBroadException
def create_cube_solid(color=COLOR_WHITE):
    """Crea un cubo solido de arista 1.0"""
    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    glColor4fv(color)
    try:
        glutSolidCube(1.0)
    except:
        if not _ERRS[3]:
            printGLError(
                "la version actual de OpenGL no posee la funcion glutSolidCube")
        _ERRS[3] = True
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_piramid(color=COLOR_WHITE):
    """Crea una pirámide de base cuadrada"""
    arista = 2.0
    a = Point3(-0.5, -0.5, -0.333) * arista
    b = Point3(0.5, -0.5, -0.333) * arista
    c = Point3(0.5, 0.5, -0.333) * arista
    d = Point3(-0.5, 0.5, -0.333) * arista
    e = Point3(0.0, 0.0, 0.666) * arista

    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    glColor4fv(color)
    glBegin(GL_QUADS)
    drawVertexListCreateNormal([d, c, b, a])
    glEnd()
    glBegin(GL_TRIANGLES)
    drawVertexListCreateNormal([a, b, e])
    drawVertexListCreateNormal([b, c, e])
    drawVertexListCreateNormal([c, d, e])
    drawVertexListCreateNormal([d, a, e])
    glEnd()
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_piramid_textured(texture_list):
    """Crea una pirámide de base cuadrada con texturas"""
    arista = 2.0
    a = Point3(-0.5, -0.5, -0.333) * arista
    b = Point3(0.5, -0.5, -0.333) * arista
    c = Point3(0.5, 0.5, -0.333) * arista
    d = Point3(-0.5, 0.5, -0.333) * arista
    e = Point3(0.0, 0.0, 0.666) * arista
    t_list = [Point2(0, 0), Point2(1, 0), Point2(1, 1), Point2(0, 1)]
    t_list_face = [Point2(0, 0), Point2(0.5, 1.0), Point2(1, 0)]

    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    for _i in range(len(texture_list)):
        glActiveTexture(GL_TEXTURE0 + _i)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_list[_i])
    glBegin(GL_QUADS)
    drawVertexListCreateNormal_textured([d, c, b, a], t_list)
    glEnd()
    glBegin(GL_TRIANGLES)
    drawVertexListCreateNormal_textured([a, b, e], t_list_face)
    drawVertexListCreateNormal_textured([b, c, e], t_list_face)
    drawVertexListCreateNormal_textured([c, d, e], t_list_face)
    drawVertexListCreateNormal_textured([d, a, e], t_list_face)
    glEnd()
    for _i in range(len(texture_list)):
        glActiveTexture(GL_TEXTURE0 + _i)
        glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_diamond(color=COLOR_WHITE):
    """Crea un rombo de base cuadrada"""
    a = Point3(-1.0, -1.0, 0.0)
    b = Point3(1.0, -1.0, 0.0)
    c = Point3(1.0, 1.0, 0.0)
    d = Point3(-1.0, 1.0, 0.0)
    e = Point3(0.0, 0.0, 1.0)
    f = Point3(0.0, 0.0, -1.0)

    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    glColor4fv(color)
    glBegin(GL_TRIANGLES)
    drawVertexListCreateNormal([a, b, e])
    drawVertexListCreateNormal([b, c, e])
    drawVertexListCreateNormal([c, d, e])
    drawVertexListCreateNormal([d, a, e])
    drawVertexListCreateNormal([b, a, f])
    drawVertexListCreateNormal([c, b, f])
    drawVertexListCreateNormal([d, c, f])
    drawVertexListCreateNormal([a, d, f])
    glEnd()
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_teapot(color=COLOR_WHITE):
    """Crea un teapot de OpenGL"""
    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    glColor4fv(color)
    glRotate(90, 1, 0, 0)
    try:
        glutSolidTeapot(1.0)
    except:
        if not _ERRS[4]:
            printGLError(
                "la version actual de OpenGL no posee la funcion glutSolidTeapot")
        _ERRS[4] = True
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_teapot_textured(texture_list):
    """Crea un teapot con texturas"""
    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    for _i in range(len(texture_list)):
        glActiveTexture(GL_TEXTURE0 + _i)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_list[_i])
    glRotate(90, 1, 0, 0)
    try:
        glutSolidTeapot(1.0)
    except:
        if not _ERRS[4]:
            printGLError(
                "la version actual de OpenGL no posee la funcion glutSolidTeapot")
        _ERRS[4] = True
    for _i in range(len(texture_list)):
        glActiveTexture(GL_TEXTURE0 + _i)
        glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException,PyTypeChecker,PyTypeChecker
def create_piramid_vbo(arista=1.0):
    """Crea una piramide de base cuadrada usando vbos para el manejo de shaders, retorna un objeto vboObject"""

    def ex(element):
        """Exporta el elemento a una lista"""
        return element.export_to_list()

    # Se crean los puntos
    a = Point3(-0.5, -0.5, -0.333) * arista
    b = Point3(0.5, -0.5, -0.333) * arista
    c = Point3(0.5, 0.5, -0.333) * arista
    d = Point3(-0.5, 0.5, -0.333) * arista
    e = Point3(0.0, 0.0, 0.666) * arista

    # Se crean las normales
    n1 = ex(normal3points(a, b, e))
    n2 = ex(normal3points(b, c, e))
    n3 = ex(normal3points(c, d, e))
    n4 = ex(normal3points(d, a, e))
    n5 = ex(normal3points(c, b, a))

    # Se crean las listas de puntos y normales en orden por triangulos, cada 3 puntos se forma una cara
    vertex_array = [ex(b), ex(e), ex(a), ex(b), ex(c), ex(e), ex(c), ex(d),
                    ex(e), ex(d), ex(a), ex(e), ex(a), ex(b),
                    ex(c), ex(c), ex(d), ex(a)]
    normal_array = [n1, n1, n1, n2, n2, n2, n3, n3, n3, n4, n4, n4, n5, n5, n5,
                    n5, n5, n5]

    # Se retornan los vertex buffer object
    return VboObject(vbo.VBO(array(vertex_array, 'f')),
                     vbo.VBO(array(normal_array, 'f')), len(vertex_array))


# noinspection PyTypeChecker,PyTypeChecker
def create_tetrahedron_vbo(arista=1.0):
    """Crea un tetraedro usando vbos para el manejo de shaders, retorna un objeto vboObject"""

    def ex(element):
        """Exporta el elemento a una lista"""
        return element.export_to_list()

    # Se crean los puntos
    a = Point3(-0.5, -0.288675, -0.288675) * arista
    b = Point3(0.5, -0.288675, -0.288675) * arista
    c = Point3(0.0, 0.577350, -0.288675) * arista
    d = Point3(0.0, 0.0, 0.57735) * arista

    # Se crean las normales
    n1 = ex(normal3points(a, b, d))
    n2 = ex(normal3points(b, c, d))
    n3 = ex(normal3points(c, a, d))
    n4 = ex(normal3points(c, b, a))

    # Se crean las listas de puntos y normales en orden por triangulos, cada 3 puntos se forma una cara
    vertex_array = [ex(a), ex(b), ex(d), ex(b), ex(c), ex(d), ex(c), ex(a),
                    ex(d), ex(a), ex(b), ex(c)]
    normal_array = [n1, n1, n1, n2, n2, n2, n3, n3, n3, n4, n4, n4]

    # Se retornan los vertex buffer object
    return VboObject(vbo.VBO(array(vertex_array, 'f')),
                     vbo.VBO(array(normal_array, 'f')), len(vertex_array))


# noinspection PyBroadException
def create_tetrahedron():
    """Crea un tetraedro solido de arista 1.0"""
    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    try:
        glutSolidTetrahedron()
    except:
        if not _ERRS[5]:
            printGLError(
                "la version actual de OpenGL no posee la funcion glutSolidTetrahedron")
        _ERRS[5] = True
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_dodecahedron():
    """Crea un dodecahedro de arista 1.0"""
    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    try:
        glutSolidDodecahedron()
    except:
        if not _ERRS[6]:
            printGLError(
                "la version actual de OpenGL no posee la funcion glutSolidDodecahedron")
        _ERRS[6] = True
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_octahedron():
    """Crea un octahedro de arista 1.0"""
    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    try:
        glutSolidOctahedron()
    except:
        if not _ERRS[7]:
            printGLError(
                "la version actual de OpenGL no posee la funcion glutSolidOctahedron")
        _ERRS[7] = True
    glPopMatrix()
    glEndList()
    return obj


# noinspection PyBroadException
def create_icosaedron():
    """Crea un icosahedro de arista 1.0"""
    obj = glGenLists(1)
    glNewList(obj, GL_COMPILE)
    glPushMatrix()
    try:
        glutSolidIcosahedron()
    except:
        if not _ERRS[8]:
            printGLError(
                "la version actual de OpenGL no posee la funcion glutSolidIcosahedron")
        _ERRS[8] = True
    glPopMatrix()
    glEndList()
    return obj
