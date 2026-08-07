from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GL import *
import random
import time
import os

W, H = 800, 800
DIA_HALF_WIDTH = 10
DIA_HALF_HEIGHT = 15
CAT_HALF_WIDTH_T = 60
CAT_HALF_WIDTH_B = 50
CAT_H = 20
CAT_Y = 10
catcher_x = W // 2
diamond_x = W // 2
diamond_y = 600
score = 0
game_over = False
paused = False
cheat = False
dt=1
diamond_color = [1.0, 1.0, 0.0]
diamond_speed = 150.0

def iterate():
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W, 0.0, H, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

#8-WAY SYMMETRY

def find_zone(dx, dy):
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx >= 0 and dy < 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx >= 0 and dy < 0:
            return 6
    return 0

TO_ZONE0 = {
    0: lambda x, y: ( x,  y),
    1: lambda x, y: ( y,  x),
    2: lambda x, y: ( y, -x),
    3: lambda x, y: (-x,  y),
    4: lambda x, y: (-x, -y),
    5: lambda x, y: (-y, -x),
    6: lambda x, y: (-y,  x),
    7: lambda x, y: ( x, -y)
}

FROM_ZONE0 = {
    0: lambda x, y: ( x,  y),
    1: lambda x, y: ( y,  x),
    2: lambda x, y: (-y,  x),
    3: lambda x, y: (-x,  y),
    4: lambda x, y: (-x, -y),
    5: lambda x, y: (-y, -x),
    6: lambda x, y: ( y, -x),
    7: lambda x, y: ( x, -y)
}

def to_zone0(x, y, zone):
    return TO_ZONE0[zone](x, y)

def from_zone0(x, y, zone):
    return FROM_ZONE0[zone](x, y)

#Midpoint_Algo

def midpoint_line(x1, y1, x2, y2):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    dx, dy = x2 - x1, y2 - y1
    zone = find_zone(dx, dy)

    x1_0, y1_0 = to_zone0(x1, y1, zone)
    x2_0, y2_0 = to_zone0(x2, y2, zone)
    dx_0, dy_0 = x2_0 - x1_0, y2_0 - y1_0

    d = 2 * dy_0 - dx_0
    incE = 2 * dy_0
    incNE = 2 * (dy_0 - dx_0)
    
    y = y1_0
    for x in range(x1_0, x2_0 + 1):
        orig_x, orig_y = from_zone0(x, y, zone)
        draw_pixel(orig_x, orig_y)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

def draw_diamond():
    glColor3fv(diamond_color)
    cx, cy = diamond_x, diamond_y
    # Top to Right
    midpoint_line(cx, cy + DIA_HALF_HEIGHT, cx + DIA_HALF_WIDTH, cy)
    # Right to Bottom
    midpoint_line(cx + DIA_HALF_WIDTH, cy, cx, cy - DIA_HALF_HEIGHT)
    # Bottom to Left
    midpoint_line(cx, cy - DIA_HALF_HEIGHT, cx - DIA_HALF_WIDTH, cy)
    # Left to Top
    midpoint_line(cx - DIA_HALF_WIDTH, cy, cx, cy + DIA_HALF_HEIGHT)

def draw_catcher():
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    cx, cy = catcher_x, CAT_Y
    # Top Line
    midpoint_line(cx - CAT_HALF_WIDTH_T, cy + CAT_H, cx + CAT_HALF_WIDTH_T, cy + CAT_H)
    # Right Slant
    midpoint_line(cx + CAT_HALF_WIDTH_T, cy + CAT_H, cx + CAT_HALF_WIDTH_B, cy)
    # Bottom Line
    midpoint_line(cx + CAT_HALF_WIDTH_B, cy, cx - CAT_HALF_WIDTH_B, cy)
    # Left Slant
    midpoint_line(cx - CAT_HALF_WIDTH_B, cy, cx - CAT_HALF_WIDTH_T, cy + CAT_H)

#MOVEMENT & CONTROLS

CATCHER_STEP = 30
last_time = time.time()

def special_key(key, x, y):
    global catcher_x
    if game_over or paused:
        return

    if key == GLUT_KEY_LEFT:
        catcher_x -= CATCHER_STEP
    elif key == GLUT_KEY_RIGHT:
        catcher_x += CATCHER_STEP

    if catcher_x < CAT_HALF_WIDTH_T:
        catcher_x = CAT_HALF_WIDTH_T
    elif catcher_x > W - CAT_HALF_WIDTH_T:
        catcher_x = W - CAT_HALF_WIDTH_T
    glutPostRedisplay()

def cheatkey(key, x, y):
    global cheat
    if key == b'c':
        cheat = not cheat
        print("Cheat mode:", "ON" if cheat else "OFF")

def animate():
    global diamond_y, last_time, score, game_over, diamond_speed, CATCHER_STEP
    now = time.time()
    dt = now - last_time
    last_time = now
    if game_over or paused:
        return
    if cheat:
        cheat_catcher(diamond_x, dt)
    
    diamond_y -= diamond_speed * dt

    if boom_detected(dia_area(), cat_area()):
        score += 1
        diamond_speed += 10.0 
        CATCHER_STEP += 2
        print(f"Score: {score}")
        new_dia()
    
    if diamond_y < 0:
        game_over = True
        print(f"Game Over! Score: {score}")   
    glutPostRedisplay()

#GAME LOGIC

def boom_detected(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

def dia_area():
    return (diamond_x - DIA_HALF_WIDTH, diamond_y - DIA_HALF_HEIGHT, 2*DIA_HALF_WIDTH, 2*DIA_HALF_HEIGHT)
def cat_area():
    return (catcher_x - CAT_HALF_WIDTH_T, CAT_Y, 2*CAT_HALF_WIDTH_T, CAT_H)

def new_dia():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(DIA_HALF_WIDTH, W - DIA_HALF_WIDTH)
    diamond_y = H - 60
    diamond_color = [random.uniform(0.0, 1.0) for _ in range(3)]
    diamond_color[random.randint(0, 2)] = 1.0

#UI BUTTONS

RESTART_BOX = (50, 750, 50, 50)
PLAYPAUSE_BOX = (375, 750, 50, 50)
EXIT_BOX = (700, 750, 50, 50)

def draw_buttons():
    glColor3f(0.0, 1.0, 1.0)
    rx, ry = RESTART_BOX[0], RESTART_BOX[1]
    midpoint_line(rx + 40, ry + 25, rx + 10, ry + 25)
    midpoint_line(rx + 10, ry + 25, rx + 25, ry + 40)
    midpoint_line(rx + 10, ry + 25, rx + 25, ry + 10)

    glColor3f(1.0, 0.75, 0.0)
    px, py = PLAYPAUSE_BOX[0], PLAYPAUSE_BOX[1]
    if paused:
        midpoint_line(px + 15, py + 10, px + 15, py + 40)
        midpoint_line(px + 15, py + 40, px + 40, py + 25)
        midpoint_line(px + 40, py + 25, px + 15, py + 10)
    else:
        midpoint_line(px + 15, py + 10, px + 15, py + 40)
        midpoint_line(px + 35, py + 10, px + 35, py + 40)

    glColor3f(1.0, 0.0, 0.0)
    ex, ey = EXIT_BOX[0], EXIT_BOX[1]
    midpoint_line(ex + 10, ey + 40, ex + 40, ey + 10)
    midpoint_line(ex + 10, ey + 10, ex + 40, ey + 40)

#MOUSE CLICKS

def inside(px, py, box):
    bx, by, bw, bh = box
    return bx <= px <= bx + bw and by <= py <= by + bh

def restart():
    global score, diamond_speed, game_over, paused, catcher_x, diamond_color, CATCHER_STEP
    score = 0
    diamond_speed = 150.0
    CATCHER_STEP = 20
    game_over = False
    paused = False
    catcher_x = W // 2
    new_dia()
    print("Starting over!")

def mouse(button, state, x, y):
    global paused
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return
    wy = H - y 
    if inside(x, wy, RESTART_BOX):
        restart()
    elif inside(x, wy, PLAYPAUSE_BOX):
        paused = not paused
        glutPostRedisplay()    
    elif inside(x, wy, EXIT_BOX):
        print(f"Goodbye! Final Score: {score}")
        os._exit(0)

def cheat_catcher(target_x, dt):
    global catcher_x
    max_step = (diamond_speed + 150.0) * dt 
    delta = target_x - catcher_x
    if abs(delta) <= max_step:
        catcher_x = target_x
    else:
        if delta > 0:
            catcher_x += max_step
        else:
            catcher_x -= max_step

    if catcher_x < CAT_HALF_WIDTH_T:
        catcher_x = CAT_HALF_WIDTH_T
    elif catcher_x > W - CAT_HALF_WIDTH_T:
        catcher_x = W - CAT_HALF_WIDTH_T


#MAIN DISPLAY

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_buttons()
    draw_catcher()
    if not game_over:
        draw_diamond()
    glutSwapBuffers()
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(W, H)
    glutCreateWindow(b"Catch the Diamonds!")
    glutDisplayFunc(display)
    glutSpecialFunc(special_key) 
    glutKeyboardFunc(cheatkey)
    glutMouseFunc(mouse)
    glutIdleFunc(animate) 
    glutMainLoop()

if __name__ == "__main__":
    main()