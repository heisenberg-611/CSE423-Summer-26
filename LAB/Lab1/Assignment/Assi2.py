from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

# Global variables
winWidth, winHeight = 500, 500
points = [] # list of dictionaries: {'x': x, 'y': y, 'dx': dx, 'dy': dy, 'color': (r,g,b)}
speed_multiplier = 1.0
is_blinking = False
is_frozen = False
blink_state = True # Used for toggling colors during blink
last_blink_time = time.time()

def convert_coordinate(x, y):
    # Convert mouse coordinates to OpenGL coordinates
    # For ortho(0, winWidth, 0, winHeight), the origin is bottom-left
    # But mouse coordinates have origin at top-left
    return x, winHeight - y

def setup_projection():
    glViewport(0, 0, winWidth, winHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, winWidth, 0.0, winHeight, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def draw_box():
    glColor3f(1.0, 1.0, 1.0) # White boundary
    glBegin(GL_LINES)
    # top
    glVertex2f(0, winHeight-1)
    glVertex2f(winWidth-1, winHeight-1)
    # bottom
    glVertex2f(0, 0)
    glVertex2f(winWidth-1, 0)
    # left
    glVertex2f(0, 0)
    glVertex2f(0, winHeight-1)
    # right
    glVertex2f(winWidth-1, 0)
    glVertex2f(winWidth-1, winHeight-1)
    glEnd()

def draw_points():
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        if is_blinking and not blink_state:
            # draw as background color (black)
            glColor3f(0.0, 0.0, 0.0)
        else:
            glColor3f(p['color'][0], p['color'][1], p['color'][2])
        glVertex2f(p['x'], p['y'])
    glEnd()

def display():
    glClearColor(0.0, 0.0, 0.0, 1.0) # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    
    draw_box()
    draw_points()
    
    glutSwapBuffers()

def animate():
    global points, is_blinking, blink_state, last_blink_time, is_frozen
    
    if is_blinking:
        current_time = time.time()
        if current_time - last_blink_time > 0.5: # 500ms transition
            blink_state = not blink_state
            last_blink_time = current_time

    if not is_frozen:
        for p in points:
            # move
            p['x'] += p['dx'] * speed_multiplier
            p['y'] += p['dy'] * speed_multiplier
            
            # bounce back from the wall (by changing the sign of corresponding position update parameter)
            if p['x'] < 0:
                p['x'] = 0
                p['dx'] = -p['dx']
            elif p['x'] >= winWidth:
                p['x'] = winWidth - 1
                p['dx'] = -p['dx']
                
            if p['y'] < 0:
                p['y'] = 0
                p['dy'] = -p['dy']
            elif p['y'] >= winHeight:
                p['y'] = winHeight - 1
                p['dy'] = -p['dy']
                
    glutPostRedisplay()

def mouse(button, state, x, y):
    global points, is_blinking
    if is_frozen:
        return
        
    x, y = convert_coordinate(x, y)
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Vibrant random colors (avoiding dark colors since background is black)
        r = random.uniform(0.3, 1.0)
        g = random.uniform(0.3, 1.0)
        b = random.uniform(0.3, 1.0)
        
        # Random direction in any angle, but every ball is initiated with the exact same speed magnitude
        angle = random.uniform(0, 2 * math.pi)
        base_speed = 1.0
        dx = math.cos(angle) * base_speed
        dy = math.sin(angle) * base_speed
        
        points.append({
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy,
            'color': (r, g, b)
        })
        
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Toggle blinking
        is_blinking = not is_blinking

def special_keys(key, x, y):
    global speed_multiplier
    if is_frozen:
        return
        
    if key == GLUT_KEY_UP:
        speed_multiplier += 0.5
    elif key == GLUT_KEY_DOWN:
        speed_multiplier -= 0.5
        if speed_multiplier < 0.1: # prevent negative or zero speed completely
            speed_multiplier = 0.1

def keyboard(key, x, y):
    global is_frozen
    if key == b' ':
        is_frozen = not is_frozen

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Task 2: Building the Amazing Box")
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
