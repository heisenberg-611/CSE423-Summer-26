from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

W=500
H=500
balls=[]
speed=1
pause=False
blink=False
show=True
last=time.time()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0,0,0,1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,W,0,H,0,1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPointSize(5)
    glBegin(GL_POINTS)
    for i in balls:
        if blink==True and show==False:
            glColor3f(0,0,0)
        else:
            glColor3f(i["r"],i["g"],i["b"])
        glVertex2f(i["x"],i["y"])
    glEnd()
    glutSwapBuffers()

def animate():
    global show,last
    if blink:
        if time.time()-last>0.5:
            show=not show
            last=time.time()
    if pause==False:
        for i in balls:
            i["x"]+=i["dx"]*speed
            i["y"]+=i["dy"]*speed
            if i["x"]<=0:
                i["x"]=0
                i["dx"]=-i["dx"]
            if i["x"]>=W:
                i["x"]=W
                i["dx"]=-i["dx"]
            if i["y"]<=0:
                i["y"]=0
                i["dy"]=-i["dy"]
            if i["y"]>=H:
                i["y"]=H
                i["dy"]=-i["dy"]
    glutPostRedisplay()

def mouseListener(button,state,x,y):
    global blink
    if pause:
        return
    if state==GLUT_DOWN:
        y=H-y
        if button==GLUT_RIGHT_BUTTON:
            angle=random.uniform(0,2*math.pi)
            ball={}
            ball["x"]=x
            ball["y"]=y
            ball["dx"]=math.cos(angle)
            ball["dy"]=math.sin(angle)
            ball["r"]=random.random()
            ball["g"]=random.random()
            ball["b"]=random.random()
            balls.append(ball)
        elif button==GLUT_LEFT_BUTTON:
            blink=not blink

def keyboard(key,x,y):
    global pause
    if key==b' ':
        pause=not pause

def specialKey(key,x,y):
    global speed
    if pause:
        return
    if key==GLUT_KEY_UP:
        speed+=0.5
    elif key==GLUT_KEY_DOWN:
        speed-=0.5
        if speed<0.1:
            speed=0.1

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(W,H)
    glutInitWindowPosition(100,100)
    glutCreateWindow(b"Task2")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialKey)
    glutMainLoop()

main()