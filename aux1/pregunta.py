# coding=utf-8
"""
Auxiliar 1 modelo
"""

# Importamos librerías
import numpy as np
import matplotlib.pyplot as plt
import tqdm

# Constantes
ITERATIONS = 10000


class Estanque(object):
    """
    Clase estanque, itera.
    """

    def __init__(self, ancho, alto, h):
        """
        Constructor

        :param ancho: Ancho del sistema
        :param alto: Alto del sistema
        :param h: Espaciado de la malla
        """
        # Almacenamos valores
        self.ancho = ancho
        self.alto = alto
        self.dh = h

        # Almacenamos cantidad de celdas de mi matriz
        self.w = ancho / h
        self.h = alto / h

        # Creamos la matriz (mallado)
        self.matrix = np.zeros((self.h, self.w))

        # Definimos la condición de borde
        self.matrix[0, :] = self.alto

    def __str__(self):
        """
        Imprime la matriz
        :return:
        """
        print self.matrix
        return ''

    def iterate(self):
        """
        Itera
        :return: Retorna nada, hace algo
        """

        for _ in tqdm.tqdm(range(ITERATIONS)):

            # Trabajamos en los bordes
            for i in range(1, self.h - 1):  # borde izquierdo
                self.matrix[i, 0] = 0.25 * (
                    2 * self.matrix[i, 1] + self.matrix[i - 1, 0] + self.matrix[
                        i + 1, 0])
            for i in range(1, self.h - 1):  # borde derecho
                self.matrix[i, self.w - 1] = 0.25 * (
                    2 * self.matrix[i, self.w - 2] + self.matrix[
                        i - 1, self.w - 1] + self.matrix[i + 1, self.w - 1])
            for j in range(1, self.w - 1):  # borde inferior
                self.matrix[self.h - 1, j] = 0.25 * (
                    2 * self.matrix[self.h - 2, j] + self.matrix[
                        self.h - 1, j - 1] + self.matrix[self.h - 1, j + 1])

            # Trabajo en las esquinas

            # izquierdo
            self.matrix[self.h - 1, 0] = 0.5 * (
                self.matrix[self.h - 2, 0] + self.matrix[self.h - 1, 1])

            # derecho
            self.matrix[self.h - 1, self.w - 1] = 0.5 * (
                self.matrix[self.h - 2, self.w - 1] + self.matrix[
                    self.h - 1, self.w - 2])

            # Trabajamos en el interior del sistema
            for i in range(1, self.h - 1):  # fila
                for j in range(1, self.w - 1):  # columnas
                    self.matrix[i, j] = 0.25 * (
                        self.matrix[i - 1, j] + self.matrix[i + 1, j] +
                        self.matrix[i, j - 1] + self.matrix[i, j + 1])

    def plot(self):
        """
        Plotea la solución
        :return:
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Se agrega grafico al plot
        cax = ax.imshow(self.matrix)
        fig.colorbar(cax)

        plt.show()


if __name__ == '__main__':
    est = Estanque(100, 30, 1)
    est.iterate()
    print est
    est.plot()
