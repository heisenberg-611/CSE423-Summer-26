from OpenGL.GLUT import glutKeyboardFunc
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import sys

# --- WINDOW SETTINGS ---
W, H = 800, 800

# --- PART 2: GAME SHAPES ---
# Shape Dimensions
D_HALF_W = 10  # Diamond half width
D_HALF_H = 15  # Diamond half height
C_HALF_W = 40  # Catcher half width (top)
C_HALF_W_BOTTOM = 30 # Catcher half width (bottom)
CATCHER_H = 15 # Catcher height
CATCHER_Y = 20 # Catcher's fixed Y position near the bottom
# Initial Positions
catcher_x = W // 2
diamond_x = W // 2
diamond_y = 600
score = 0
game_over = False
paused = False
cheat = False
dt=1
diamond_color = [1.0, 1.0, 0.0]

def iterate():
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W, 0.0, H, 0.0, 1.0) # Origin is at bottom-left
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# --- PART 1: MIDPOINT LINE ALGORITHM (8-WAY SYMMETRY) ---

def find_zone(dx, dy):
    """
    Returns the zone (0-7) of a line given its dx and dy.
    """
    if abs(dx) >= abs(dy): # shallow line: |dx| dominates -> zones 0, 3, 4, 7
        if dx >= 0 and dy >= 0:
            return 0
        # TODO: Fill in zones 3, 4, 7
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx >= 0 and dy < 0:
            return 7
    else: # steep line: |dy| dominates -> zones 1, 2, 5, 6
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx >= 0 and dy < 0:
            return 6
    return 0 # Default

# (x, y) in zone z -> Zone-0 coordinates
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

# Zone-0 (x, y) -> back to zone z
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

def draw_diamond():
    glColor3fv(diamond_color)
    cx, cy = diamond_x, diamond_y
    
    # Top to Right
    midpoint_line(cx, cy + D_HALF_H, cx + D_HALF_W, cy)
    # Right to Bottom
    midpoint_line(cx + D_HALF_W, cy, cx, cy - D_HALF_H)
    # Bottom to Left
    midpoint_line(cx, cy - D_HALF_H, cx - D_HALF_W, cy)
    # Left to Top
    midpoint_line(cx - D_HALF_W, cy, cx, cy + D_HALF_H)

def draw_catcher():
    if game_over:
        glColor3f(1.0, 0.0, 0.0) # Red on game over
    else:
        glColor3f(1.0, 1.0, 1.0) # White catcher
    cx, cy = catcher_x, CATCHER_Y
    # Top Line
    midpoint_line(cx - C_HALF_W, cy + CATCHER_H, cx + C_HALF_W, cy + CATCHER_H)
    # Right Slant
    midpoint_line(cx + C_HALF_W, cy + CATCHER_H, cx + C_HALF_W_BOTTOM, cy)
    # Bottom Line
    midpoint_line(cx + C_HALF_W_BOTTOM, cy, cx - C_HALF_W_BOTTOM, cy)
    # Left Slant
    midpoint_line(cx - C_HALF_W_BOTTOM, cy, cx - C_HALF_W, cy + CATCHER_H)

def midpoint_line(x1, y1, x2, y2):
    """
    Draws a line from (x1, y1) to (x2, y2) using the midpoint algorithm in any zone.
    """
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    dx, dy = x2 - x1, y2 - y1
    zone = find_zone(dx, dy)
    
    # Convert endpoints to Zone 0
    x1_0, y1_0 = to_zone0(x1, y1, zone)
    x2_0, y2_0 = to_zone0(x2, y2, zone)
    
    # Recalculate dx, dy for Zone 0
    dx_0, dy_0 = x2_0 - x1_0, y2_0 - y1_0
    
    # Zone 0 Midpoint Algorithm
    d = 2 * dy_0 - dx_0
    incE = 2 * dy_0
    incNE = 2 * (dy_0 - dx_0)
    
    y = y1_0
    for x in range(x1_0, x2_0 + 1):
        # Convert back from Zone 0 to original zone before drawing
        orig_x, orig_y = from_zone0(x, y, zone)
        draw_pixel(orig_x, orig_y)
        
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

# --- PART 3: MOVEMENT & CONTROLS ---\

CATCHER_STEP = 20 # How fast the catcher moves per key press
speed = 150.0  # Pixels per second
last_time = time.time()

def special_key(key, x, y):
    global catcher_x
    if game_over or paused:
        return

    if key == GLUT_KEY_LEFT:
        catcher_x -= CATCHER_STEP
    elif key == GLUT_KEY_RIGHT:
        catcher_x += CATCHER_STEP
        
    # Clamp the catcher's position so it doesn't go off screen!
    if catcher_x < C_HALF_W:
        catcher_x = C_HALF_W
    elif catcher_x > W - C_HALF_W:
        catcher_x = W - C_HALF_W
    glutPostRedisplay()

def cheatkey(key, x, y):
    global cheat
    if key == b'c':
        cheat = not cheat
        print("Cheat mode:", "ON" if cheat else "OFF")

def animate():
    global diamond_y, last_time, score, game_over, speed, CATCHER_STEP
    
    now = time.time()
    dt = now - last_time
    last_time = now

    if game_over or paused:
        return

    if cheat:
        step_catcher_toward(diamond_x, dt)
    
    # Update diamond position based on speed and time passed
    diamond_y -= speed * dt

    if has_collided(diamond_box(), catcher_box()):
        score += 1
        speed += 10.0 # Increase speed by 10 pixels/second on each catch
        CATCHER_STEP += 1.5 # Increase manual catcher step size
        print(f"Score: {score}")
        spawn_diamond()
    
    # If the diamond falls off the bottom of the screen, reset it to the top for now
    if diamond_y < 0:
        game_over = True
        print(f"Game Over! Score: {score}")
    

        
    glutPostRedisplay()

# --- PART 4: GAME LOGIC ---

# Collision Detection
def has_collided(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

def diamond_box():
    return (diamond_x - D_HALF_W, diamond_y - D_HALF_H, 2*D_HALF_W, 2*D_HALF_H)
def catcher_box():
    return (catcher_x - C_HALF_W, CATCHER_Y, 2*C_HALF_W, CATCHER_H)

def spawn_diamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(D_HALF_W, W - D_HALF_W)
    diamond_y = H
    diamond_color = [random.uniform(0.0, 1.0) for _ in range(3)]
    diamond_color[random.randint(0, 2)] = 1.0

# --- PART 5: UI BUTTONS ---

# Button Boxes (x, y, w, h)
RESTART_BOX = (50, 750, 50, 50)
PLAYPAUSE_BOX = (375, 750, 50, 50)
EXIT_BOX = (700, 750, 50, 50)

def draw_buttons():
    # 1. Left Arrow (Restart) - Teal
    glColor3f(0.0, 1.0, 1.0)
    rx, ry = RESTART_BOX[0], RESTART_BOX[1]
    # Arrow drawing
    midpoint_line(rx + 40, ry + 25, rx + 10, ry + 25) # Main line
    midpoint_line(rx + 10, ry + 25, rx + 25, ry + 40) # Top slant
    midpoint_line(rx + 10, ry + 25, rx + 25, ry + 10) # Bottom slant

    # 2. Play/Pause - Amber
    glColor3f(1.0, 0.75, 0.0)
    px, py = PLAYPAUSE_BOX[0], PLAYPAUSE_BOX[1]
    if paused:
        # Draw Play Icon (Triangle)
        midpoint_line(px + 15, py + 10, px + 15, py + 40)
        midpoint_line(px + 15, py + 40, px + 40, py + 25)
        midpoint_line(px + 40, py + 25, px + 15, py + 10)
    else:
        # Draw Pause Icon (Two vertical lines)
        midpoint_line(px + 15, py + 10, px + 15, py + 40)
        midpoint_line(px + 35, py + 10, px + 35, py + 40)

    # 3. Cross (Exit) - Red
    glColor3f(1.0, 0.0, 0.0)
    ex, ey = EXIT_BOX[0], EXIT_BOX[1]
    midpoint_line(ex + 10, ey + 40, ex + 40, ey + 10)
    midpoint_line(ex + 10, ey + 10, ex + 40, ey + 40)

# --- PART 6: MOUSE CLICKS ---

def inside(px, py, box):
    bx, by, bw, bh = box
    return bx <= px <= bx + bw and by <= py <= by + bh

def restart():
    global score, speed, game_over, paused, catcher_x, diamond_color, CATCHER_STEP
    score = 0
    speed = 150.0
    CATCHER_STEP = 20
    game_over = False
    paused = False
    catcher_x = W // 2
    spawn_diamond()
    print("Starting over!")

def mouse(button, state, x, y):
    global paused
    
    # We only care about the left mouse button being pressed down
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return
        
    # GLUT gives y measured from the TOP of the window, 
    # but our OpenGL world has y=0 at the BOTTOM. Let's flip it!
    wy = H - y 
    
    # Check which button was clicked
    if inside(x, wy, RESTART_BOX):
        restart()
        
    elif inside(x, wy, PLAYPAUSE_BOX):
        paused = not paused
        # The display function will automatically redraw the correct icon!
        
    elif inside(x, wy, EXIT_BOX):
        print(f"Goodbye! Final Score: {score}")
        sys.exit(0)

def step_catcher_toward(target_x, dt):
    global catcher_x
    
    # The catcher moves a bit faster than the falling diamond so it doesn't miss!
    max_step = (speed + 150.0) * dt 
    
    delta = target_x - catcher_x
    
    # Move towards the target, but don't overshoot it
    if abs(delta) <= max_step:
        catcher_x = target_x
    else:
        if delta > 0:
            catcher_x += max_step
        else:
            catcher_x -= max_step
            
    # Clamp to screen edges just to be safe
    if catcher_x < C_HALF_W:
        catcher_x = C_HALF_W
    elif catcher_x > W - C_HALF_W:
        catcher_x = W - C_HALF_W


# --- MAIN DISPLAY & RUN ---

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_buttons()
    draw_catcher()
    if not game_over:
        draw_diamond()

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(W, H)
glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(display)
glutSpecialFunc(special_key) 
glutKeyboardFunc(cheatkey)
glutMouseFunc(mouse)
glutIdleFunc(animate) 
glutMainLoop()
