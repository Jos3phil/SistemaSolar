from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import random

angleSun = 0.0
angleEarth = 0.0
angleMoon = 0.0
angleMars = 0.0
angleAsteroids = 0.0
angleComet = 0.0
eyex, eyey, eyez = 0.0, 50.0, 150.0
zRotated = 0.0
NUM_STARS = 1000
mesh = True


stars = [{'x': random.uniform(-100, 100), 'y': random.uniform(-100, 100), 'z': random.uniform(-100, 100)} for _ in range(NUM_STARS)]

def drawSphere(radius, slices, stacks):
    global mesh
    sphere = gluNewQuadric()
    gluQuadricNormals(sphere, GLU_SMOOTH)
    gluSphere(sphere, radius, slices, stacks)
    if mesh:
        glColor3f(0.5, 0.5, 0.5)  # Color del enmallado, gris para contraste
        # Dibujar meridianos
        for i in range(slices):
            glPushMatrix()
            glRotatef(360.0 / slices * i, 0.0, 1.0, 0.0)
            glBegin(GL_LINE_LOOP)
            for j in range(stacks):
                x = radius * math.sin(j * math.pi / stacks) * math.cos(i * math.pi / slices)
                y = radius * math.cos(j * math.pi / stacks)
                z = radius * math.sin(j * math.pi / stacks) * math.sin(i * math.pi / slices)
                glVertex3f(x, y, z)
            glEnd()
            glPopMatrix()
        # Dibujar paralelos
        for i in range(stacks):
            glPushMatrix()
            glRotatef(360.0 / stacks * i, 1.0, 0.0, 0.0)
            glBegin(GL_LINE_LOOP)
            for j in range(slices):
                x = radius * math.sin(i * math.pi / stacks) * math.cos(j * math.pi / slices)
                y = radius * math.cos(i * math.pi / stacks)
                z = radius * math.sin(i * math.pi / stacks) * math.sin(j * math.pi / slices)
                glVertex3f(x, y, z)
            glEnd()
            glPopMatrix()
    gluDeleteQuadric(sphere)

def drawSun():
    global angleSun
    glPushMatrix()
    glRotatef(angleSun, 0.0, 1.0, 0.0)
    glColor3f(1.0, 1.0, 0.0)
    drawSphere(10.0, 50, 50)
    glPopMatrix()

def drawEarth():
    global angleEarth, zRotated  # Asegurarse de incluir zRotated
    glPushMatrix()
    glRotatef(angleEarth, 0.0, 1.0, 0.0)  # Rotación existente
    glTranslatef(30.0, 0.0, 0.0)
    glRotatef(zRotated, 0, 0, 1)  # Rotación adicional en el eje Z
    
    glColor3f(0.0, 0.0, 1.0)
    drawSphere(4.0, 30, 30)
    glPopMatrix()


def drawMoon():
    global angleEarth, angleMoon
    glPushMatrix()
    glRotatef(angleEarth, 0.0, 1.0, 0.0)
    glTranslatef(30.0, 0.0, 0.0)
    glRotatef(angleMoon, 0.0, 1.0, 0.0)
    glTranslatef(7.0, 0.0, 0.0)
    glColor3f(0.8, 0.8, 0.8)
    drawSphere(1.0, 20, 20)
    glPopMatrix()

def drawMars():
    global angleMars
    glPushMatrix()
    glRotatef(angleMars, 0.0, 1.0, 0.0)
    glTranslatef(50.0, 0.0, 0.0)
    glColor3f(1.0, 0.0, 0.0)
    drawSphere(3.0, 30, 30)
    glPopMatrix()

def drawAsteroids():
    global angleAsteroids
    glPushMatrix()
    glRotatef(angleAsteroids, 0.0, 1.0, 0.0)
    glColor3f(0.5, 0.5, 0.5)
    for i in range(1000):
        glPushMatrix()
        angle = i * 0.36
        radius = 40.0 + (random.random() * 10)
        glRotatef(angle, 0.0, 1.0, 0.0)
        glTranslatef(radius, 0.0, 0.0)
        glutSolidSphere(0.1, 4, 4)
        glPopMatrix()
    glPopMatrix()

def drawComet():
    global angleComet
    glPushMatrix()
    glRotatef(angleComet, 0.0, 0.1, 1.0)
    glTranslatef(80.0, 0.0, 0.0)
    glColor3f(0.8, 0.8, 1.0)
    glutSolidSphere(1.0, 20, 20)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(21):
        angle = i * (math.pi / 10)
        glVertex3f(-20 * math.cos(angle), 2 * math.sin(angle), 0)
    glEnd()
    glPopMatrix()

def drawStars():
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(1.0)
    glBegin(GL_POINTS)
    for star in stars:
        glVertex3f(star['x'], star['y'], star['z'])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(eyex, eyey, eyez, 0, 0, 0, 0, 1, 0)
    drawStars()
    drawSun()
    drawEarth()
    drawMoon()
    drawMars()
    drawAsteroids()
    drawComet()
    glutSwapBuffers()

def update(value):
    global angleSun, angleEarth, angleMoon, angleMars, angleAsteroids, angleComet, zRotated
    angleSun += 0.1
    angleEarth += 1.0
    angleMoon += 2.0
    angleMars += 0.44
    angleAsteroids += 0.2
    angleComet += 0.05
    zRotated += 0.1
    if zRotated > 360: zRotated -= 360
    if angleSun > 360: angleSun -= 360
    if angleEarth > 360: angleEarth -= 360
    if angleMoon > 360: angleMoon -= 360
    if angleMars > 360: angleMars -= 360
    if angleAsteroids > 360: angleAsteroids -= 360
    if angleComet > 360: angleComet -= 360
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_position = [0.0, 0.0, 0.0, 1.0]
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(w) / float(h), 1.0, 500.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640 ,480)
    glutCreateWindow(b"Sistema Solar 3D Mejorado")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(25, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()