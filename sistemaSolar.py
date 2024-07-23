import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

class Cuerpo:
    def __init__(self, masa, posX, posY, vX, vY, tamanio=0.02, r=1, g=0, b=0):
        self.masa = masa
        self.posX = posX
        self.posY = posY
        self.vX = vX
        self.vY = vY
        self.tamanio = tamanio
        self.r = r
        self.g = g
        self.b = b

    def DibujarCuerpo(self):
        glPushMatrix()
        glColor3f(self.r, self.g, self.b)
        glTranslatef(self.posX, self.posY, -10)
        glutSolidSphere(self.tamanio, 100, 20)
        glPopMatrix()

cuerpos = []
G = 0.001

def calcular_fuerza(cuerpo1, cuerpo2):
    dx = cuerpo2.posX - cuerpo1.posX
    dy = cuerpo2.posY - cuerpo1.posY
    distancia = np.sqrt(dx * dx + dy * dy)
    if distancia == 0:
        return
    fuerza_magnitud = G * (cuerpo1.masa * cuerpo2.masa) / (distancia * distancia)
    angulo = np.arctan2(dy, dx)
    fuerza_x = fuerza_magnitud * np.cos(angulo)
    fuerza_y = fuerza_magnitud * np.sin(angulo)
    
    cuerpo1.vX += fuerza_x / cuerpo1.masa
    cuerpo1.vY += fuerza_y / cuerpo1.masa

def actualizar_posicion(dt):
    for cuerpo in cuerpos:
        cuerpo.posX += cuerpo.vX * dt
        cuerpo.posY += cuerpo.vY * dt

def simular_n_cuerpos(dt):
    for i in range(len(cuerpos)):
        for j in range(len(cuerpos)):
            if i != j:
                calcular_fuerza(cuerpos[i], cuerpos[j])
    actualizar_posicion(dt)

def Update(value):
    simular_n_cuerpos(0.01)
    glutPostRedisplay()
    glutTimerFunc(10, Update, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    for cuerpo in cuerpos:
        cuerpo.DibujarCuerpo()
    glutSwapBuffers()

def main():
    global cuerpos

    cuerpos = [
        Cuerpo(2.0, 0.0, 0.0, 0.0, 0.0, 0.5),      # Sol
        Cuerpo(1e-7, 0.3, 0.0, 0.0, 0.8),         # Mercurio
        Cuerpo(2e-6, 0.6, 0.0, 0.0, 0.6),         # Venus
        Cuerpo(1e-6, 3.1, 0.0, 0.0, 0.2, 0.03, 0, 0, 1),  # Tierra
        Cuerpo(4e-7, 1.3, 0.0, 0.0, 0.4),         # Marte
        Cuerpo(1e-2, 2.0, 0.0, 0.0, 0.2),         # Júpiter
        Cuerpo(5e-3, 3.0, 0.0, 0.0, 0.15),        # Saturno
        Cuerpo(8e-4, 4.5, 0.0, 0.0, 0.12),        # Urano
        Cuerpo(1e-3, 6.0, 0.0, 0.0, 0.1)          # Neptuno
    ]

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Esferas de diferentes tamanios moviendose con GL/GLU")
    glutDisplayFunc(display)
    glutTimerFunc(0, Update, 0)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 10)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutMainLoop()

if __name__ == "__main__":
    main()
