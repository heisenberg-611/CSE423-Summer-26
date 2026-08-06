from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

winWidth, winHeight = 500, 500
dnfac = 1.0
rndrps = []
rndx = 0
cloud_x = 0

def rndrop():
    for i in range(300):
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
    s_color(0.3, 0.5, 0.9, 0.3, 0.4, 0.7)
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

def main_house():
    s_color(0.7, 0.5, 0.3, 0.3, 0.2, 0.1)
    d_rect(150, 200, 350, 300)
    
    s_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(1)
    glBegin(GL_LINES)
    for y in range(200, 320, 20):
        glVertex2f(150, y)
        glVertex2f(350, y)
    for x in range(150, 370, 20):
        glVertex2f(x, 200)
        glVertex2f(x, 300)
    glEnd()
    
    # Roof 
    s_color(0.4, 0.2, 0.7, 0.2, 0.1, 0.4)
    d_rect(130, 300, 370, 320)
    d_rect(150, 320, 350, 340)
    d_rect(170, 340, 330, 360)
    d_rect(190, 360, 310, 380)
    d_rect(210, 380, 290, 400)
    
    # Door (Oak)
    s_color(0.5, 0.3, 0.1, 0.2, 0.1, 0.0)
    d_rect(230, 200, 270, 260)
    
    # Minecraft door windows
    s_color(0.8, 0.9, 1.0, 0.4, 0.5, 0.8)
    d_rect(235, 235, 245, 255)
    d_rect(255, 235, 265, 255)
    
    
    # Left window (Glass Pane)
    s_color(0.8, 0.9, 1.0, 0.4, 0.5, 0.8)
    d_rect(175, 225, 215, 265)
    
    # Left window grills (black cross)
    s_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(195, 225) 
    glVertex2f(195, 265)  # vertical
    glVertex2f(175, 245) 
    glVertex2f(215, 245)  # horizontal
    glEnd()
    
    # Right window (Glass Pane)
    s_color(0.8, 0.9, 1.0, 0.4, 0.5, 0.8)
    d_rect(285, 225, 325, 265)
    
    # Right window grills (black cross)
    s_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(305, 225) 
    glVertex2f(305, 265)  # vertical
    glVertex2f(285, 245) 
    glVertex2f(325, 245)  # horizontal
    glEnd()

def draw_lamppost():
    s_color(0.2, 0.2, 0.2, 0.1, 0.1, 0.1)
    d_rect(70, 150, 100, 170)
    
    s_color(0.3, 0.3, 0.3, 0.1, 0.1, 0.1)
    d_rect(80, 170, 90, 330)

    s_color(1.0, 1.0, 0.0, 0.8, 0.8, 0.0)
    d_rect(75, 330, 95, 350)

    s_color(0.2, 0.2, 0.2, 0.1, 0.1, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(65, 350)
    glVertex2f(105, 350)
    glVertex2f(85, 370)
    glEnd()

def draw_clouds():
    global cloud_x
    s_color(1.0, 1.0, 1.0, 0.4, 0.4, 0.4) # Minecraft Cloud
    
    # Cloud 1 (Left)
    d_rect(90 + cloud_x, 410, 140 + cloud_x, 430)
    d_rect(70 + cloud_x, 400, 160 + cloud_x, 410)
    d_rect(80 + cloud_x, 390, 150 + cloud_x, 400)
    
    # Cloud 2 (Right)
    d_rect(320 + cloud_x, 440, 370 + cloud_x, 460)
    d_rect(290 + cloud_x, 420, 400 + cloud_x, 440)
    d_rect(300 + cloud_x, 410, 390 + cloud_x, 420)

    # Cloud 3 (Middle)
    d_rect(190 + cloud_x, 390, 240 + cloud_x, 410)
    d_rect(170 + cloud_x, 380, 260 + cloud_x, 390)
    d_rect(180 + cloud_x, 370, 250 + cloud_x, 380)

    # Cloud 4 (Far Right)
    d_rect(510 + cloud_x, 460, 560 + cloud_x, 480)
    d_rect(490 + cloud_x, 440, 580 + cloud_x, 460)
    d_rect(500 + cloud_x, 430, 570 + cloud_x, 440)

def draw_grass():
    s_color(0.3, 0.7, 0.2, 0.1, 0.5, 0.1)
    glLineWidth(2)
    glBegin(GL_LINES)
    for i in range(10, winWidth, 30):
        glVertex2f(i + 5, 20)
        glVertex2f(i, 35)
        glVertex2f(i + 5, 20)
        glVertex2f(i + 10, 35)
        glVertex2f(i + 5, 20)
        glVertex2f(i + 5, 40)

        glVertex2f(i + 15, 60)
        glVertex2f(i + 10, 75)
        glVertex2f(i + 15, 60)
        glVertex2f(i + 20, 75)
        glVertex2f(i + 15, 60)
        glVertex2f(i + 15, 80)
        
        glVertex2f(i, 100)
        glVertex2f(i - 5, 115)
        glVertex2f(i, 100)
        glVertex2f(i + 5, 115)
        glVertex2f(i, 100)
        glVertex2f(i, 120)

        glVertex2f(i + 10, 180)
        glVertex2f(i + 5, 195)
        glVertex2f(i + 10, 180)
        glVertex2f(i + 15, 195)
        glVertex2f(i + 10, 180)
        glVertex2f(i + 10, 200)
    glEnd()

def animate():
    global rndx, rndrps, winWidth, winHeight, cloud_x
    # cloud_x += 0.8
    # if cloud_x > winWidth:
    #     cloud_x = -400
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

def setup_projection():
    glViewport(0, 0, winWidth, winHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, winWidth, 0.0, winHeight, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    s_color(0.5, 0.7, 1.0, 0.0, 0.0, 0.1, is_bg=True)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    s_color(0.4, 0.8, 0.3, 0.05, 0.2, 0.05)
    d_rect(0, 0, winWidth, 250)
    draw_grass()
    draw_clouds()
    main_house()
    draw_lamppost()
    d_rain()
    glutSwapBuffers()

def special_keys_listener(key, x, y):
    global rndx
    if key == GLUT_KEY_LEFT:
        rndx -= 1.0
        print("Rain is bending left")
    elif key == GLUT_KEY_RIGHT:
        rndx += 1.0
        print("Rain is bending right")
    glutPostRedisplay()

def keyboard_keys_listener(key, x, y):
    global dnfac
    if key == b'd' or key == b'D':
        dnfac += 0.05
        if dnfac > 1.0:
            dnfac = 1.0
            print("Wake up from bed!")
        else:
            print("Sun is rising...")
    elif key == b'n' or key == b'N':
        dnfac -= 0.05
        if dnfac < 0.0:
            dnfac = 0.0
            print("Go to sleep!")
        else:
            print("Getting Nighter...")
    glutPostRedisplay()

def main():
    rndrop()
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"Ass1.py")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_keys_listener)
    glutKeyboardFunc(keyboard_keys_listener)
    glutMainLoop()

if __name__ == "__main__":
    main()