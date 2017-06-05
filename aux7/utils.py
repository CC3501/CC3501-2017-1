# coding=utf-8

# Importación de librerías
import math
import types
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# Constantes
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [1, 1, 1]

def printGLError(err_msg):
    """Imprime un error en consola"""
    print "[GL-ERROR] {0}".format(err_msg)


def draw_text(text, pos, color=COLOR_WHITE, font=GLUT_BITMAP_TIMES_ROMAN_24, linespace=20):
    """Dibuja un texto en una posicon dada por un punto point3"""
    glColor3fv(color)
    if isinstance(pos, Point3):
        x = pos.get_x()
        y = pos.get_y()
        z = pos.get_z()
        glRasterPos3f(x, y, z)
        for char in text:
            if char == "\n":
                y += linespace
                glRasterPos3f(x, y, z)
            else:
                try:
                    glutBitmapCharacter(font, ord(char))
                except:
                    if not _ERRS[0]:
                        printGLError("la version actual de OpenGL no posee la funcion glutBitmapCharacter")
                    _ERRS[0] = True
    else:
        raise Exception("el punto debe ser del tipo point3")



def create_axes(s, both=False, text=True):
    """Dibuja los ejes en pantalla"""
    # Se convierte la distancia a un entero positivo
    s = abs(s)

    if s > 0:  # Si es una distancia valida

        # Vectores de dibujo
        x = Point3(s, 0, 0)
        y = Point3(0, s, 0)
        z = Point3(0, 0, s)
        o = Point3()

        # Se crea nueva lista
        lista = glGenLists(1)
        glNewList(lista, GL_COMPILE)

        # Se agregan los vectores al dibujo
        glBegin(GL_LINES)

        glColor4fv([1, 0, 0, 1])
        drawVertexList([o, x])
        glColor4fv([0, 1, 0, 1])
        drawVertexList([o, y])
        glColor4fv([0, 0, 1, 1])
        drawVertexList([o, z])

        if both:  # Se dibujan los ejes en ambos sentidos
            x = Point3(-s, 0, 0)
            y = Point3(0, -s, 0)
            z = Point3(0, 0, -s)

            glColor4fv([1, 0, 0, 1])
            drawVertexList([o, x])
            glColor4fv([0, 1, 0, 1])
            drawVertexList([o, y])
            glColor4fv([0, 0, 1, 1])
            drawVertexList([o, z])

        glEnd()

        if text:  # Se dibujan los nombres de los ejes
            draw_text("x", Point3(s + 60, 0, -15), [1, 0, 0], GLUT_BITMAP_HELVETICA_18)
            draw_text("y", Point3(0, s + 50, -15), [0, 1, 0], GLUT_BITMAP_HELVETICA_18)
            draw_text("z", Point3(+0, +0, s + 50), [0, 0, 1], GLUT_BITMAP_HELVETICA_18)

            if both:
                draw_text("-x", Point3(-s - 60, 0, -15), [1, 0, 0], GLUT_BITMAP_HELVETICA_18)
                draw_text("-y", Point3(0, -s - 70, -15), [0, 1, 0], GLUT_BITMAP_HELVETICA_18)
                draw_text("-z", Point3(+0, +0, -s - 80), [0, 0, 1], GLUT_BITMAP_HELVETICA_18)

        # Se retorna la lista
        glEndList()
        return lista

    else:
        raise Exception("la dimension de los ejes debe ser mayor a cero")



# Constantes
POINT_2 = "util-point-2"
POINT_3 = "util-point-3"

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
def draw_list(lista, pos=[0.0, 0.0, 0.0], angle=0.0, rot=None, sz=None, rgb=None):
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



# noinspection PyMethodFirstArgAssignment
class Point3:
    """
    Punto de 3 componentes.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Funcion constructora"""
        self._point = Vector3(x, y, z)
        self._type = POINT_3

    def get_type(self):
        """Retorna el tipo de punto"""
        return self._type

    def get_x(self):
        """Retorna el primer elemento del punto"""
        return self._point.get_x()

    def get_y(self):
        """Retorna el segundo elemento del punto"""
        return self._point.get_y()

    def get_z(self):
        """Retorna el tercer elemento del punto"""
        return self._point.get_z()

    def set_x(self, value):
        """Define el primer elemento del punto"""
        self._point.set_x(value)

    def set_y(self, value):
        """Define el segundo elemento del punto"""
        self._point.set_y(value)

    def set_z(self, value):
        """Define el tercer elemento del punto"""
        self._point.set_z(value)

    def export_to_list(self):
        """Exportar el punto a una lista"""
        return [self._point.get_x(), self._point.get_y(), self._point.get_z()]

    def export_to_tuple(self):
        """Exportar el punto a una tupla"""
        return self._point.get_x(), self._point.get_y(), self._point.get_z()

    def normalize(self):
        """Normaliza el punto"""
        self._point.normalize()

    # override
    def echo(self, mantise=1):
        """Imprime el punto"""
        self._point.echo(mantise, point3=True)

    def __add__(self, other):
        """Sumar el punto con otro"""
        return self._vecto_point(self._point.__add__(self._point_to_vec(other)))

    def __sub__(self, other):
        """Restar el punto con otro"""
        return self._vecto_point(self._point.__sub__(self._point_to_vec(other)))

    def __mul__(self, other):
        """Multiplicar el punto por otro"""
        return self._vecto_point(self._point.__mul__(self._point_to_vec(other)))

    def __str__(self, mantise=1, **kwargs):
        """Retornar el string del punto"""
        return self._point.__str__(mantise, point3=True)

    def __div__(self, other):
        """Dividir el punto por otro"""
        return self._vecto_point(self._point.__div__(self._point_to_vec(other)))

    def __abs__(self):
        """Retornar el valor absoluto del punto"""
        return self._vecto_point(self._point.__abs__())

    def __iadd__(self, other):
        """Suma el mismo punto con other"""
        self = self._vecto_point(self._point.__iadd__(other))
        return self

    def __isub__(self, other):
        """Resta el mismo punto con other"""
        self = self._vecto_point(self._point.__isub__(other))
        return self

    def __imul__(self, other):
        """Multiplica el mismo punto con other"""
        self = self._vecto_point(self._point.__imul__(other))
        return self

    def __idiv__(self, other):
        """Divide el mismo punto con other"""
        self = self._vecto_point(self._point.__iadd__(other))
        return self

    # noinspection PyMethodMayBeStatic,PyShadowingNames
    def _point_to_vec(self, point):
        """Convierte un punto a un vector"""
        if isinstance(point, Point3):
            return Vector3(point.get_x(), point.get_y(), point.get_z())
        else:
            return point

    # noinspection PyMethodMayBeStatic
    def _vecto_point(self, vec):
        """Convierte un vector a un punto"""
        if isinstance(vec, Vector3):
            return Point3(vec.get_x(), vec.get_y(), vec.get_z())
        else:
            return vec


# Punto de 2 componentes
class Point2(Point3):
    def __init__(self, x=0.0, y=0.0):
        Point3.__init__(self, x, y)
        self._point = Vector3(x, y, 0.0)
        self._type = POINT_2

    # noinspection PyMethodMayBeStatic,PyShadowingNames
    def _point_to_vec(self, point):
        """Convierte un punto a un vector"""
        if isinstance(point, Point2):
            return Vector3(point.get_x(), point.get_y(), 0.0)
        else:
            return point

    # noinspection PyMethodMayBeStatic
    def _vecto_point(self, vec):
        """Convierte un vector a un punto"""
        if isinstance(vec, Vector3):
            return Point2(vec.get_x(), vec.get_y())
        else:
            return vec

    def __str__(self, mantise=1, **kwargs):
        """Retornar el string del punto"""
        return self._point.__str__(mantise, point2=True)

    # override
    def echo(self, mantise=1):
        """Imprime el punto"""
        self._point.echo(mantise, point2=True)

    def export_to_list(self):
        """Exportar el punto a una lista"""
        return [self._point.get_x(), self._point.get_y()]

    def export_to_tuple(self):
        """Exportar el punto a una tupla"""
        return self._point.get_x(), self._point.get_y()


# noinspection PyTypeChecker,PyArgumentList
class Vector3:
    """
    Vector de 3 componentes, provee funciones matemáticas básicas.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Funcion constructora"""
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def get_module(self):
        """Retorna el modulo del vector"""
        return self.distancewith(Vector3(0, 0, 0))

    def set_x(self, x):
        """Define la coordenada x"""
        self.x = x

    def set_y(self, y):
        """Define la coordenada y"""
        self.y = y

    def set_z(self, z):
        """Define la coordenada z"""
        self.z = z

    def get_x(self):
        """Retorna la coordenada x"""
        return self.x

    def get_y(self):
        """Retorna la coordenada y"""
        return self.y

    def get_z(self):
        """Retorna la coordenada z"""
        return self.z

    def ponderate(self, a=1):
        """Pondera el vector por un numero"""
        if isinstance(a, types.FloatType) or isinstance(a, types.IntType):
            self.x *= a
            self.y *= a
            self.z *= a
        else:
            self.throwError(2, "ponderate")
            return self

    def __add__(self, other):
        """Suma el vector con otro"""
        if isinstance(other, Vector3):
            return Vector3(self.x + other.get_x(), self.y + other.get_y(), self.z + other.get_z())
        elif isinstance(other, types.TupleType) or isinstance(other, types.ListType):
            if len(other) == 3:
                return Vector3(self.x + other[0], self.y + other[1], self.z + other[2])
        else:
            self.throwError(2, "__add__")
            return self

    def __sub__(self, other):
        """Resta el vector con otro"""
        if isinstance(other, Vector3):
            return Vector3(self.x - other.get_x(), self.y - other.get_y(), self.z - other.get_z())
        elif isinstance(other, types.TupleType) or isinstance(other, types.ListType):
            if len(other) == 3:
                return Vector3(self.x - other[0], self.y - other[1], self.z - other[2])
        else:
            self.throwError(2, "__sub__")
            return self

    def __mod__(self, other):
        """Calcula el modulo con otro"""
        return Vector3(self.x % other.get_x(), self.y % other.get_y(), self.z % other.get_z())

    def __mul__(self, other):
        """Producto punto o producto por valor"""
        if isinstance(other, Vector3):
            return Vector3(self.x * other.get_x(), self.y * other.get_y(), self.z * other.get_z())
        else:
            if isinstance(other, types.ListType) or isinstance(other, types.TupleType):
                return Vector3(self.x * other[0], self.y * other[1], self.z * other[2])
            elif isinstance(other, types.IntType) or isinstance(other, types.FloatType):
                return Vector3(self.x * other, self.y * other, self.z * other)
            else:
                self.throwError(2, "__mul__")
                return self

    def __abs__(self):
        """Valor absoluto"""
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __div__(self, other):
        """Dividir por un ector o por un valor"""
        if isinstance(other, Vector3):
            return Vector3(self.x / other.get_x(), self.y / other.get_y(), self.z / other.get_z())
        else:
            if isinstance(other, types.IntType) or isinstance(other, types.FloatType):
                return Vector3(self.x / other, self.y / other, self.z / other)
            else:
                self.throwError(2, "__div__")
                return self

    def __invert__(self, other):
        """Invertir signo del vector en forma ~"""
        return Vector3(-self.x, -self.y, -self.z)

    def __neg__(self):
        """Invertir signo del vector en forma -"""
        return Vector3(-self.x, -self.y, -self.z)

    def __pos__(self):
        """Aplicar signo positivo"""
        return Vector3(self.x, self.y, self.z)

    def __and__(self, other):
        """Calcula el operador logico and"""
        if isinstance(other, Vector3):
            if self.x > 0 and other.get_x() > 0:
                x = 1
            else:
                x = 0
            if self.y > 0 and other.get_y() > 0:
                y = 1
            else:
                y = 0
            if self.z > 0 and other.get_z() > 0:
                z = 1
            else:
                z = 0
            return Vector3(x, y, z)
        else:
            self.throwError(2, "__and__")
            return Vector3()

    def __or__(self, other):
        """Calcula el operador logico and"""
        if isinstance(other, Vector3):
            if self.x > 0 or other.get_x() > 0:
                x = 1
            else:
                x = 0
            if self.y > 0 or other.get_y() > 0:
                y = 1
            else:
                y = 0
            if self.z > 0 or other.get_z() > 0:
                z = 1
            else:
                z = 0
            return Vector3(x, y, z)
        else:
            self.throwError(2, "__or__")
            return Vector3()

    def __int__(self):
        """Convierte el vector a enteros"""
        return Vector3(int(self.x), int(self.y), int(self.z))

    def __float__(self):
        """Convierte el vector a flotante"""
        return Vector3(float(self.x), float(self.y), float(self.z))

    def normalize(self):
        """Normalizar el vector"""
        modl = self.get_module()
        self.x /= modl
        self.y /= modl
        self.z /= modl

    def get_normalized(self):
        """Retorna el vector normalizado"""
        modl = self.get_module()
        return Vector3(self.x / modl, self.y / modl, self.z / modl)

    def clone(self):
        """Clonar el vector"""
        return Vector3(self.x, self.y, self.z)

    def __complex__(self):
        """Genera un vector complejo"""
        return Vector3(complex(self.x), complex(self.y), complex(self.z))

    def __long__(self):
        """Genera un vector long"""
        return Vector3(long(self.x), long(self.y), long(self.z))

    def __hex__(self):
        """Genera un vector hex"""
        return Vector3(hex(self.x), hex(self.y), hex(self.z))

    def __oct__(self):
        """Genera un vector oct"""
        return Vector3(oct(self.x), oct(self.y), oct(self.z))

    def __iadd__(self, other):
        """Suma un vector con otro"""
        if isinstance(other, Vector3):
            self.x += other.get_x()
            self.y += other.get_y()
            self.z += other.get_z()
            return self
        elif isinstance(other, types.TupleType) or isinstance(other, types.ListType):
            if len(other) == 3:
                self.x += other[0]
                self.y += other[1]
                self.z += other[2]
                return self
        else:
            self.throwError(2, "__iadd__")
            return self

    def __isub__(self, other):
        """Resta un vector con otro"""
        if isinstance(other, Vector3):
            self.x -= other.get_x()
            self.y -= other.get_y()
            self.z -= other.get_z()
            return self
        elif isinstance(other, types.TupleType) or isinstance(other, types.ListType):
            if len(other) == 3:
                self.x -= other[0]
                self.y -= other[1]
                self.z -= other[2]
                return self
        else:
            self.throwError(2, "__isub__")
            return self

    def __imul__(self, other):
        """Producto punto con otro"""
        if isinstance(other, Vector3):
            self.x *= other.get_x()
            self.y *= other.get_y()
            self.z *= other.get_z()
            return self
        else:
            if isinstance(other, types.ListType) or isinstance(other, types.TupleType):
                self.x *= other[0]
                self.y *= other[1]
                self.z *= other[2]
                return self
            elif isinstance(other, types.IntType) or isinstance(other, types.FloatType):
                self.x *= other
                self.y *= other
                self.z *= other
                return self
            else:
                self.throwError(2, "__imul__")
                return self

    def __idiv__(self, other):
        """Division con otro vector por valor"""
        if isinstance(other, Vector3):
            self.x /= other.get_x()
            self.y /= other.get_y()
            self.z /= other.get_z()
            return self
        else:
            if isinstance(other, types.ListType) or isinstance(other, types.TupleType):
                self.x /= other[0]
                self.y /= other[1]
                self.z /= other[2]
                return self
            elif isinstance(other, types.IntType) or isinstance(other, types.FloatType):
                self.x /= other
                self.y /= other
                self.z /= other
                return self
            else:
                self.throwError(2, "__idiv__")
                return self

    @staticmethod
    def throwError(err_num, err_func):
        """Imprime un error en pantalla"""

        def _printError(error):
            print "Error :: {0} ~ {1}".format(error, err_func)

        if err_num == 1:
            _printError("La mantisa es menor a 1")
        elif err_num == 2:
            _printError("Tipo invalido")

    # override
    def echo(self, mantise=1, **kwargs):
        """Imprime el vector en pantalla"""
        print self.__str__(mantise, **kwargs)

    def dot(self, other):
        """Producto punto"""
        return self.__mul__(other)

    def dotwith(self, other):
        """Producto punto con otro"""
        dot = self.dot(other)
        self.x = dot.get_x()
        self.y = dot.get_y()
        self.z = dot.get_z()

    def cross(self, other):
        """Retorna el producto cruz"""
        if isinstance(other, Vector3):
            i = self.y * other.get_z() - self.z * other.get_y()
            j = self.z * other.get_x() - self.x * other.get_z()
            k = self.x * other.get_y() - self.y * other.get_x()
            return Vector3(i, j, k)
        elif isinstance(other, types.TupleType) or isinstance(other, types.ListType):
            return self.cross(Vector3(*other))
        else:
            self.throwError(2, "cross")
            return self

    def crosswith(self, other):
        """Aplica el producto cruz con el otro vector"""
        cross = self.cross(other)
        self.x = cross.get_x()
        self.y = cross.get_y()
        self.z = cross.get_z()

    def distancewith(self, other):
        """Retorna la distancia a otro vector"""
        if isinstance(other, Vector3):
            return math.sqrt(
                (self.x - other.get_x()) ** 2 + (self.y - other.get_y()) ** 2 + (self.z - other.get_y()) ** 2)
        elif isinstance(other, types.ListType) or isinstance(other, types.TupleType):
            return self.distancewith(Vector3(*other))
        else:
            self.throwError(2, "distance")
            return 0.0

    def __str__(self, mantise=1, **kwargs):
        """Retorna el string del punto"""
        if mantise >= 1:
            if kwargs.get("formated"):
                _format = "/{0}\\\n|{1}|\n\\{2}/"
            else:
                _format = "[{0},{1},{2}]"
            if kwargs.get("point3"):
                _format = "({0},{1},{2})"
            if kwargs.get("point2"):
                _format = "({0},{1})"
            return _format.format(round(self.x, mantise), round(self.y, mantise), round(self.z, mantise))
        else:
            self.throwError(1, "echo")

    def export_to_list(self):
        """Exportar el vector a una lista"""
        return [self.x, self.y, self.z]

    def export_to_tuple(self):
        """Exportar el vector a una tupla"""
        return self.x, self.y, self.z


def normal3points(a, b, c):
    """Retorna el vector normal dado tres puntos a, b, c"""
    if isinstance(a, types.ListType) or isinstance(a, types.TupleType):
        a = Vector3(*a)
        b = Vector3(*b)
        c = Vector3(*c)
    elif isinstance(a, Point3):
        a = Vector3(*a.export_to_list())
        b = Vector3(*b.export_to_list())
        c = Vector3(*c.export_to_list())
    cross_result = (a - c).cross(b - c).get_normalized()
    if cross_result.get_x() == -0.0:
        cross_result.set_x(0.0)
    if cross_result.get_y() == -0.0:
        cross_result.set_y(0.0)
    if cross_result.get_z() == -0.0:
        cross_result.set_z(0.0)
    return cross_result


def cos(angle):
    """Retorna el coseno de un angulo"""
    return math.cos(math.radians(angle))


def sin(angle):
    """Retorna el seno de un angulo"""
    return math.sin(math.radians(angle))


def sgn(x):
    """Retorna el signo de x"""
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


def spr_to_xyz(r, fi, theta):
    """Convierte las coordenadas esferiacs (r,fi,theta) a (x,y,z)"""
    x = r * sin(theta) * cos(fi)
    y = r * sin(theta) * sin(fi)
    z = r * cos(theta)
    return x, y, z


def xyz_to_spr(x, y, z):
    """Convierte las coordenadas cartesianas (x,y,z) a las coordenadas esfericas (r,phi,theta) con angulos en grados"""
    # Calculo el radio
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    # Calculo el angulo theta
    if z > 0:
        theta = math.atan(math.sqrt(x ** 2 + y ** 2) / z)
    elif z == 0:
        theta = math.pi / 2
    else:
        theta = math.pi + math.atan(math.sqrt(x ** 2 + y ** 2) / z)
    # Calculo el angulo phi
    if x > 0:
        if y > 0:
            phi = math.atan(y / x)
        else:
            phi = 2 * math.pi + math.atan(y / x)
    elif x == 0:
        phi = sgn(y) * math.pi / 2
    else:
        phi = math.pi + math.atan(y / x)
    theta = math.degrees(theta)
    phi = math.degrees(phi) % 360
    theta = min(max(theta, 0.000001), 180)
    return r, phi, theta

