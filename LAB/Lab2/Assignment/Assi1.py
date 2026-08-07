from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
    glColor3f(1.0, 1.0, 0.0) # Yellow diamond
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

# --- PART 3: MOVEMENT & CONTROLS ---
import time

CATCHER_STEP = 20 # How fast the catcher moves per key press
speed = 150.0  # Pixels per second
last_time = time.time()

def special_key(key, x, y):
    global catcher_x
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

def animate():
    global diamond_y, last_time
    
    now = time.time()
    dt = now - last_time
    last_time = now
    
    # Update diamond position based on speed and time passed
    diamond_y -= speed * dt
    
    # If the diamond falls off the bottom of the screen, reset it to the top for now
    if diamond_y < 0:
        diamond_y = H
        
    glutPostRedisplay()

# --- MAIN DISPLAY & RUN ---

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_diamond()
    draw_catcher()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(W, H)
glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(display)
glutSpecialFunc(special_key) 
glutIdleFunc(animate) 
glutMainLoop()
