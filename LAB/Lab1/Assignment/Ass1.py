from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

winWidth, winHeight = 500, 500
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

def main_house():
    # House body (white/gray)
    s_color(1.0, 1.0, 1.0, 0.5, 0.5, 0.5)
    d_rect(150, 200, 350, 300)
    
    # House border (black)
    s_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(3)
    glBegin(GL_LINE_LOOP)
    glVertex2f(150, 200)
    glVertex2f(350, 200)
    glVertex2f(350, 300)
    glVertex2f(150, 300)
    glEnd()
    
    # Roof (purple)
    s_color(0.4, 0.2, 0.7, 0.2, 0.1, 0.4)
    glBegin(GL_TRIANGLES)
    glVertex2f(130, 300)
    glVertex2f(370, 300)
    glVertex2f(250, 390)
    glEnd()
    
    # Roof border (black)
    s_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(3)
    glBegin(GL_LINE_LOOP)
    glVertex2f(130, 300)
    glVertex2f(370, 300)
    glVertex2f(250, 390)
    glEnd()
    
    # Door (blue)
    s_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    d_rect(230, 200, 270, 260)
    
    # Door border (black)
    s_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(230, 200)
    glVertex2f(270, 200)
    glVertex2f(270, 260)
    glVertex2f(230, 260)
    glEnd()
    
    # Left window (blue)
    s_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    d_rect(175, 225, 215, 265)
    
    # Left window grills (black cross)
    s_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(195, 225); glVertex2f(195, 265)  # vertical
    glVertex2f(175, 245); glVertex2f(215, 245)  # horizontal
    glEnd()
    
    # Left window border (black)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(175, 225)
    glVertex2f(215, 225)
    glVertex2f(215, 265)
    glVertex2f(175, 265)
    glEnd()
    
    # Right window (blue)
    s_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    d_rect(285, 225, 325, 265)
    
    # Right window grills (black cross)
    s_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(305, 225); glVertex2f(305, 265)  # vertical
    glVertex2f(285, 245); glVertex2f(325, 245)  # horizontal
    glEnd()
    
    # Right window border (black)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(285, 225)
    glVertex2f(325, 225)
    glVertex2f(325, 265)
    glVertex2f(285, 265)
    glEnd()

def draw_lamppost():
    # Base
    s_color(0.2, 0.2, 0.2, 0.1, 0.1, 0.1)
    d_rect(70, 150, 100, 170)
    
    # Pole
    s_color(0.3, 0.3, 0.3, 0.1, 0.1, 0.1)
    d_rect(80, 170, 90, 330)
    
    # Light bulb (yellow)
    s_color(1.0, 1.0, 0.0, 0.8, 0.8, 0.0)
    d_rect(75, 330, 95, 350)

    # Top cover
    s_color(0.2, 0.2, 0.2, 0.1, 0.1, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(65, 350)
    glVertex2f(105, 350)
    glVertex2f(85, 370)
    glEnd()

def draw_grass():
    s_color(0.1, 0.6, 0.1, 0.0, 0.2, 0.0) # Green
    glLineWidth(2)
    glBegin(GL_LINES)
    for i in range(10, winWidth, 30):
        # Tuft 1
        glVertex2f(i + 15, 60)
        glVertex2f(i + 10, 75)
        glVertex2f(i + 15, 60)
        glVertex2f(i + 20, 75)
        glVertex2f(i + 15, 60)
        glVertex2f(i + 15, 80)
        
        # Tuft 2
        glVertex2f(i, 100)
        glVertex2f(i - 5, 115)
        glVertex2f(i, 100)
        glVertex2f(i + 5, 115)
        glVertex2f(i, 100)
        glVertex2f(i, 120)
        
        # Tuft 3
        glVertex2f(i + 10, 180)
        glVertex2f(i + 5, 195)
        glVertex2f(i + 10, 180)
        glVertex2f(i + 15, 195)
        glVertex2f(i + 10, 180)
        glVertex2f(i + 10, 200)
    glEnd()

def animate():
    global rndx, rndrps, winWidth, winHeight
    for x in rndrps:
        x[1] -= 5
        x[0] += rndx
        if x[1] < 0:
            x[1] = winHeight
        if x[0] < 0:
            x[0] = winWidth
        elif x[0] > winWidth:
            x[0] = 0
    glutPostRedisplay()

def display():
    s_color(0.6, 0.8, 1.0, 0.0, 0.0, 0.0, is_bg=True)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    s_color(0.6, 0.4, 0.1, 0.2, 0.1, 0.0) #Ground
    d_rect(0, 0, winWidth, 250)
    draw_grass()
    main_house()
    draw_lamppost()
    d_rain()
    glutSwapBuffers()

def main():
    rndrop()
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"Ass1.py")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMainLoop()

if __name__ == "__main__":
    main()