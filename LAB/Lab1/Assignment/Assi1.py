from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

# Global variables
winWidth, winHeight = 500, 500
rain_drops = []
rain_dx = 0
day_night_factor = 1.0 # 1 is day, 0.0 is night (gradual transition)

# Initialize raindrops
for _ in range(100):
    x = random.randint(0, winWidth)
    y = random.randint(0, winHeight)
    rain_drops.append([x, y])

def setup_projection():
    glViewport(0, 0, winWidth, winHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, winWidth, 0.0, winHeight, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def set_color(day_r, day_g, day_b, night_r, night_g, night_b):
    # Interpolates color based on day_night_factor
    r = day_r * day_night_factor + night_r * (1.0 - day_night_factor)
    g = day_g * day_night_factor + night_g * (1.0 - day_night_factor)
    b = day_b * day_night_factor + night_b * (1.0 - day_night_factor)
    glColor3f(r, g, b)

def set_bg_color():
    # Sky: Light sky blue (0.6, 0.8, 1.0) to Dark night sky (0.0, 0.0, 0.0)
    r = 0.6 * day_night_factor + 0.0 * (1.0 - day_night_factor)
    g = 0.8 * day_night_factor + 0.0 * (1.0 - day_night_factor)
    b = 1.0 * day_night_factor + 0.0 * (1.0 - day_night_factor)
    glClearColor(r, g, b, 1.0)

def draw_rect(x1, y1, x2, y2):
    # Helper to draw a filled rectangle using only GL_TRIANGLES (since GL_QUADS is not allowed)
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_ground():
    # Ground color: brown/orange to dark brown
    set_color(0.6, 0.4, 0.1, 0.2, 0.1, 0.0)
    draw_rect(0, 0, 500, 250)

def draw_trees():
    # A row of contiguous green triangles along the horizon (y=250)
    set_color(0.0, 0.8, 0.0, 0.0, 0.3, 0.0) 
    glBegin(GL_TRIANGLES)
    for i in range(10): # 10 trees, 50 pixels wide each
        x_start = i * 50
        glVertex2f(x_start, 250)
        glVertex2f(x_start + 50, 250)
        glVertex2f(x_start + 25, 310)
    glEnd()

def draw_house():
    # House Body (White)
    set_color(1.0, 1.0, 1.0, 0.5, 0.5, 0.5)
    draw_rect(150, 150, 350, 250)

    # Roof (Purple)
    set_color(0.4, 0.2, 0.7, 0.2, 0.1, 0.4)
    glBegin(GL_TRIANGLES)
    glVertex2f(130, 250)
    glVertex2f(370, 250)
    glVertex2f(250, 340)
    glEnd()
    
    # Door (Blue)
    set_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    draw_rect(230, 150, 270, 210)
    
    # Door Knob (Black)
    set_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glPointSize(4)
    glBegin(GL_POINTS)
    glVertex2f(262, 180)
    glEnd()
    
    # Left Window (Blue)
    set_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    draw_rect(175, 175, 215, 215)
    
    # Left Window Cross (Black)
    set_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(195, 175); glVertex2f(195, 215)
    glVertex2f(175, 195); glVertex2f(215, 195)
    glEnd()
    
    # Right Window (Blue)
    set_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    draw_rect(285, 175, 325, 215)
    
    # Right Window Cross (Black)
    set_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(305, 175); glVertex2f(305, 215)
    glVertex2f(285, 195); glVertex2f(325, 195)
    glEnd()

def draw_rain():
    # Rain is semi-transparent/light blue
    set_color(0.5, 0.7, 1.0, 0.3, 0.4, 0.7) 
    
    glLineWidth(1)
    glBegin(GL_LINES)
    for drop in rain_drops:
        glVertex2f(drop[0], drop[1])
        # Tail of the raindrop points backwards along the velocity vector
        glVertex2f(drop[0] - rain_dx * 2, drop[1] + 10)
    glEnd()

def display():
    set_bg_color() # Clear sky
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    
    draw_ground()
    draw_trees()
    draw_house()
    draw_rain()
    
    glutSwapBuffers()

def animate():
    global rain_drops, rain_dx, winWidth, winHeight
    
    for drop in rain_drops:
        drop[1] -= 5 # fall down
        drop[0] += rain_dx # bend rain
        
        # wrap around
        if drop[1] < 0:
            drop[1] = winHeight
        if drop[0] < 0:
            drop[0] = winWidth
        elif drop[0] > winWidth:
            drop[0] = 0
            
    glutPostRedisplay()

def special_keys(key, x, y):
    global rain_dx
    if key == GLUT_KEY_LEFT:
        rain_dx -= 0.5
    elif key == GLUT_KEY_RIGHT:
        rain_dx += 0.5
    glutPostRedisplay()

def keyboard(key, x, y):
    global day_night_factor
    if key == b'd' or key == b'D':
        day_night_factor += 0.05
        if day_night_factor > 1.0:
            day_night_factor = 1.0
    elif key == b'n' or key == b'N':
        day_night_factor -= 0.05
        if day_night_factor < 0.0:
            day_night_factor = 0.0
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Task 1")
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
