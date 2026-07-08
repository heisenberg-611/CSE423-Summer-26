from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

# Global state
width, height = 500, 500
particles = []
velocity_factor = 1.0
pause_simulation = False
toggle_visibility = False
show_particles = True
last_toggle = time.time()

def screen_to_opengl_coords(mouse_x, mouse_y):
    return mouse_x, height - mouse_y

def render_frame():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for item in particles:
        if toggle_visibility and not show_particles:
            glColor3f(0.0, 0.0, 0.0)
        else:
            red, green, blue = item['color']
            glColor3f(red, green, blue)
        glVertex2f(item['x'], item['y'])
    glEnd()
    
    glutSwapBuffers()

def update_physics():
    global show_particles, last_toggle
    
    if toggle_visibility:
        now = time.time()
        if now - last_toggle >= 0.5:
            show_particles = not show_particles
            last_toggle = now

    if not pause_simulation:
        for elem in particles:
            elem['x'] += elem['dx'] * velocity_factor
            elem['y'] += elem['dy'] * velocity_factor
            
            if elem['x'] < 0:
                elem['x'] = 0
                elem['dx'] = -elem['dx']
            elif elem['x'] >= width:
                elem['x'] = width - 1
                elem['dx'] = -elem['dx']
                
            if elem['y'] < 0:
                elem['y'] = 0
                elem['dy'] = -elem['dy']
            elif elem['y'] >= height:
                elem['y'] = height - 1
                elem['dy'] = -elem['dy']
                
    glutPostRedisplay()

def handle_mouse_event(button, action, x_pos, y_pos):
    global particles, toggle_visibility
    if pause_simulation or action != GLUT_DOWN:
        return
        
    x_gl, y_gl = screen_to_opengl_coords(x_pos, y_pos)
    
    if button == GLUT_RIGHT_BUTTON:
        c_r = random.uniform(0.3, 1.0)
        c_g = random.uniform(0.3, 1.0)
        c_b = random.uniform(0.3, 1.0)
        
        direction = random.uniform(0, 2 * math.pi)
        base_vel = 1.0
        delta_x = math.cos(direction) * base_vel
        delta_y = math.sin(direction) * base_vel
        
        particles.append({
            'x': x_gl,
            'y': y_gl,
            'dx': delta_x,
            'dy': delta_y,
            'color': (c_r, c_g, c_b)
        })
        
    elif button == GLUT_LEFT_BUTTON:
        toggle_visibility = not toggle_visibility

def process_special_key(key_code, x, y):
    global velocity_factor
    if pause_simulation:
        return
        
    if key_code == GLUT_KEY_UP:
        velocity_factor += 0.5
    elif key_code == GLUT_KEY_DOWN:
        velocity_factor -= 0.5
        if velocity_factor < 0.1:
            velocity_factor = 0.1

def process_normal_key(key_char, x, y):
    global pause_simulation
    if key_char == b' ':
        pause_simulation = not pause_simulation

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow(b"Task 2: Building the Amazing Box")
    
    glutDisplayFunc(render_frame)
    glutIdleFunc(update_physics)
    glutMouseFunc(handle_mouse_event)
    glutSpecialFunc(process_special_key)
    glutKeyboardFunc(process_normal_key)
    
    glutMainLoop()

if __name__ == "__main__":
    main()