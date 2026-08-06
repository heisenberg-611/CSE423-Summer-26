from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- WINDOW SETTINGS ---
W, H = 800, 800

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
        # TODO: Fill in zones 2, 5, 6
        pass

    return 0 # Default

# (x, y) in zone z -> Zone-0 coordinates
TO_ZONE0 = {
    0: lambda x, y: ( x,  y),
    1: lambda x, y: ( y,  x),
    2: lambda x, y: ( y, -x),
    # TODO: Fill in 3, 4, 5, 6, 7
}

# Zone-0 (x, y) -> back to zone z
FROM_ZONE0 = {
    0: lambda x, y: ( x,  y),
    1: lambda x, y: ( y,  x),
    2: lambda x, y: (-y,  x),
    # TODO: Fill in 3, 4, 5, 6, 7
}

def to_zone0(x, y, zone):
    return TO_ZONE0[zone](<x, y>)

def from_zone0(x, y, zone):
    return FROM_ZONE0[zone](<x, y>)

def midpoint_line(x1, y1, x2, y2):
    """
    Draws a line from (x1, y1) to (x2, y2) using the midpoint algorithm in any zone.
    """
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

# --- MAIN DISPLAY & RUN ---

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    
    # Testing the 8 zones
    glColor3f(1.0, 1.0, 1.0) # White lines
    CX, CY = 400, 400
    targets = [
        (700, 500), # Zone 0
        (500, 700), # Zone 1
        (300, 700), # Zone 2
        (100, 500), # Zone 3
        (100, 300), # Zone 4
        (300, 100), # Zone 5
        (500, 100), # Zone 6
        (700, 300)  # Zone 7
    ]
    for tx, ty in targets:
        midpoint_line(CX, CY, tx, ty)
        
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(W, H)
glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(display)
glutMainLoop()
