"""
Assi2_explained.py

Educational, fully-commented version of `Assi2.py` (Task 2: Building the Amazing Box).
This file reproduces the original interactive program which lets you spawn
colored moving points inside a boxed window and control their motion and
visual behavior using mouse and keyboard. Every significant variable and
function includes explanations to make the program easy to learn from.

How to run (from workspace root):
    python3 Lab1/Assignment/Assi2_explained.py

Controls:
    - Right mouse click: spawn a new colored moving point at cursor
    - Left mouse click: toggle blinking of points
    - Arrow Up/Down: increase / decrease global speed multiplier
    - Spacebar: toggle freeze (pause) / unfreeze

Notes:
    - Immediate-mode OpenGL (glBegin/glEnd) is used for pedagogical clarity.
    - Coordinates conversion done because GLUT mouse has origin at top-left
      while our orthographic projection uses bottom-left origin.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

# --------------------------
# Global state and configuration
# --------------------------
# Window size in pixels. We use an orthographic projection that maps
# coordinates directly to pixel units for simplicity.
winWidth, winHeight = 500, 500

# `points` stores moving colored points. Each point is a dictionary with:
#   'x','y' : current floating-point position
#   'dx','dy' : per-frame velocity components (direction and speed)
#   'color' : a 3-tuple (r,g,b) with values in [0,1]
points = []

# Global multipliers and modes
speed_multiplier = 1.0   # scales per-point velocity when animating
is_blinking = False      # if True, points will toggle between visible/hidden
is_frozen = False        # if True, animation and mouse spawns are ignored
blink_state = True       # internal state that flips periodically when blinking
last_blink_time = time.time()  # timestamp used to implement blinking timing


def convert_coordinate(x, y):
    """Convert GLUT mouse (x,y) to our OpenGL coordinate system.

    GLUT reports mouse `(0,0)` at the top-left of the window. Our
    orthographic projection uses `(0,0)` at the bottom-left, so we flip
    the y coordinate by subtracting from `winHeight`.
    """
    return x, winHeight - y


def setup_projection():
    """Set an orthographic projection matching the window size.

    Using `glOrtho(0, winWidth, 0, winHeight, 0, 1)` makes it easy to
    reason about coordinates in pixel units.
    """
    glViewport(0, 0, winWidth, winHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, winWidth, 0.0, winHeight, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


# def draw_box():
#     """Draw a one-pixel white boundary around the window so the box is visible.

#     We use `GL_LINES` to draw the four edges. Coordinates use `winWidth-1`
#     and `winHeight-1` to keep the line inside the pixel grid.
#     """
#     glColor3f(1.0, 1.0, 1.0)  # white boundary
#     glBegin(GL_LINES)
#     # top
#     glVertex2f(0, winHeight - 1)
#     glVertex2f(winWidth - 1, winHeight - 1)
#     # bottom
#     glVertex2f(0, 0)
#     glVertex2f(winWidth - 1, 0)
#     # left
#     glVertex2f(0, 0)
#     glVertex2f(0, winHeight - 1)
#     # right
#     glVertex2f(winWidth - 1, 0)
#     glVertex2f(winWidth - 1, winHeight - 1)
#     glEnd()


def draw_points():
    """Render all points as small square points using `GL_POINTS`.

    - When blinking mode is enabled we alternate between drawing the
      point color and drawing the background color (black) to make them
      appear to blink.
    - `glPointSize(5)` sets the visual size of each point in pixels.
    """
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        if is_blinking and not blink_state:
            # During the 'off' sub-frame, draw the point using the
            # background color (black) so it appears invisible.
            glColor3f(0.0, 0.0, 0.0)
        else:
            glColor3f(p['color'][0], p['color'][1], p['color'][2])
        glVertex2f(p['x'], p['y'])
    glEnd()


def display():
    """GLUT display callback: clear screen, set projection, draw scene.

    We clear the background to black and then render the box and points.
    Double-buffering (`glutSwapBuffers`) prevents flicker during animation.
    """
    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    # draw_box()
    draw_points()

    glutSwapBuffers()


def animate():
    """GLUT idle callback used as the animation driver.

    Responsibilities:
      - Update blink toggling on a fixed interval (500 ms)
      - Move each point according to its velocity scaled by `speed_multiplier`
      - Bounce points off the box edges by reflecting velocity components
      - Request redraw via `glutPostRedisplay()`
    """
    global points, is_blinking, blink_state, last_blink_time, is_frozen

    # Blink timing: flip `blink_state` every 0.5 seconds when blinking
    if is_blinking:
        current_time = time.time()
        if current_time - last_blink_time > 0.5:  # 500 ms interval
            blink_state = not blink_state
            last_blink_time = current_time

    # Update positions only when not frozen
    if not is_frozen:
        for p in points:
            p['x'] += p['dx'] * speed_multiplier
            p['y'] += p['dy'] * speed_multiplier

            # Bounce off left/right walls
            if p['x'] < 0:
                p['x'] = 0
                p['dx'] = -p['dx']
            elif p['x'] >= winWidth:
                p['x'] = winWidth - 1
                p['dx'] = -p['dx']

            # Bounce off bottom/top walls
            if p['y'] < 0:
                p['y'] = 0
                p['dy'] = -p['dy']
            elif p['y'] >= winHeight:
                p['y'] = winHeight - 1
                p['dy'] = -p['dy']

    glutPostRedisplay()


def mouse(button, state, x, y):
    """GLUT mouse callback. Handles left/right click behaviors.

    Right click (GLUT_RIGHT_BUTTON + GLUT_DOWN): spawn a new point at
    the converted mouse position. The new point has a vibrant random
    color and a random direction with fixed speed magnitude.

    Left click (GLUT_LEFT_BUTTON + GLUT_DOWN): toggle blinking mode.
    When frozen, mouse interactions are ignored.
    """
    global points, is_blinking
    if is_frozen:
        return

    x, y = convert_coordinate(x, y)

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Choose vibrant colors avoiding very dark tones since the
        # background is black and low contrast would be hard to see.
        r = random.uniform(0.3, 1.0)
        g = random.uniform(0.3, 1.0)
        b = random.uniform(0.3, 1.0)

        # Random direction with fixed speed magnitude
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
        # Toggle blinking on/off
        is_blinking = not is_blinking


def special_keys(key, x, y):
    """Handle special keys (arrow keys) to adjust `speed_multiplier`.

    Up increases speed; Down decreases it but we clamp to a small
    positive minimum to avoid zero/negative speeds which would freeze
    motion inadvertently.
    """
    global speed_multiplier
    if is_frozen:
        return

    if key == GLUT_KEY_UP:
        speed_multiplier += 0.5
    elif key == GLUT_KEY_DOWN:
        speed_multiplier -= 0.5
        if speed_multiplier < 0.1:  # maintain a sensible minimum
            speed_multiplier = 0.1


def keyboard(key, x, y):
    """Handle simple ASCII keys. Space toggles the global freeze flag.

    When frozen, animation and right-click spawns are disabled. Toggling
    freeze is a convenient way to inspect the scene or reposition the
    window without motion.
    """
    global is_frozen
    if key == b' ':
        is_frozen = not is_frozen


def main():
    """Program entry: initialize GLUT, register callbacks, and start loop.

    `glutMainLoop()` is blocking; to exit the program close the window
    or interrupt the terminal that launched it.
    """
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Task 2: Building the Amazing Box - Explained")

    # Register the callbacks used by the application
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


if __name__ == "__main__":
    main()
