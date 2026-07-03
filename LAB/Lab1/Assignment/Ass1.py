from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

winWidth, winHeight = 500, 500;
dnfac = 1.0
rndrps = []
rndx = 0

def rndrop():
    for i in range(200):
        x = random.randint(0, winWidth)
        y = random.randint(0, winHeight)
        rndrps.append([x,y])

def s_color(rd, gd, bd, rn, gn, bn, is_bg=False):
    r = rd * dnfac + rn * (1.0 - dnfac)
    g = gd * dnfac + gn * (1.0 - dnfac)
    b = bd * dnfac + bn * (1.0 - dnfac)
    if is_bg:
        glClearColor(r, g, b, 1.0)
    else:
        glColor3f(r, g, b)

def d_rain():
    s_color(0.5, 0.7, 1.0, 0.3, 0.4, 0.7)
    glLineWidth(1)
    glBegin(GL_LINES)
    for x in rndrps:
        glVertex2f(x[0], x[1])
        glVertex2f(x[0] - rndx * 1.5, x[1] + 20)
    glEnd()

def d_rect(x1, y1, x2, y2):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)

    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()



def setup_projection():
    glViewport(0, 0, winWidth, winHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, winWidth, 0.0, winHeight, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    s_color(0.6, 0.8, 1.0, 0.0, 0.0, 0.0, is_bg=True)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    d_rain()
    s_color(0.6, 0.4, 0.1, 0.2, 0.1, 0.0)
    d_rect(0, 0, winWidth, 250)
    glutSwapBuffers()

def main():
    rndrop()
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"test.py")
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()