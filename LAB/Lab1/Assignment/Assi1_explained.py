"""
Assi1_explained.py

A commented and educational version of `Assi1.py` from Lab1/Assignment.
This file recreates the interactive OpenGL scene: a house with rain
and a day/night interpolation, but with detailed explanations for
each section and function to help you learn how it works.

Run with:
    python3 Assi1_explained.py

Requirements:
    - PyOpenGL
    - PyOpenGL_accelerate (optional, improves performance)
    - GLUT (via freeglut or system-provided)

Install libs on macOS using Homebrew + pip if needed:
    brew install freeglut
    pip3 install PyOpenGL PyOpenGL_accelerate

Controls:
    - Left / Right arrow keys: change wind (bends rain)
    - D / d: increase day (toward full daylight)
    - N / n: decrease day (toward night)

"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

# -----------------------------
# Global configuration
# -----------------------------
# Window dimensions used for the orthographic projection and initial
# placement of scene objects. The coordinate system maps (0,0) to the
# lower-left of the window and (winWidth, winHeight) to the upper-right.
winWidth, winHeight = 500, 500

# A list of raindrop positions. Each entry is a mutable [x, y] pair.
rain_drops = []
# Horizontal velocity component for the rain. Positive values bend rain
# to the right; negative values bend it to the left.
rain_dx = 0

# Day-night blend factor: 1.0 = full day, 0.0 = full night. Values in
# between interpolate colors smoothly.
day_night_factor = 1.0

# Initialize raindrops randomly across the window. We choose 100 drops
# which is enough for a visible rain effect without being too heavy.
for _ in range(100):
    x = random.randint(0, winWidth)
    y = random.randint(0, winHeight)
    rain_drops.append([x, y])

# -----------------------------
# Projection / Utility helpers
# -----------------------------

def setup_projection():
    """Set up an orthographic projection matching the window size.

    We call this each frame to ensure the projection matches the
    current window dimensions in case the window was resized (a more
    complete program would update `winWidth`/`winHeight` during a
    reshape callback).
    """
    glViewport(0, 0, winWidth, winHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # glOrtho(left, right, bottom, top, near, far)
    glOrtho(0.0, winWidth, 0.0, winHeight, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def set_color(day_r, day_g, day_b, night_r, night_g, night_b):
    """Set the current OpenGL color by interpolating between a day
    color and a night color using `day_night_factor`.

    This helper allows each drawable element to have a bright (day)
    and dark (night) variant; the scene smoothly blends between
    those states based on the user's input.
    """
    r = day_r * day_night_factor + night_r * (1.0 - day_night_factor)
    g = day_g * day_night_factor + night_g * (1.0 - day_night_factor)
    b = day_b * day_night_factor + night_b * (1.0 - day_night_factor)
    glColor3f(r, g, b)


def set_bg_color():
    """Set the clear color for the sky. This uses a simple blend from
    a daytime sky color (light blue) to a night sky (near black).
    glClearColor defines the color used when the color buffers are
    cleared at the start of `display()`.
    """
    r = 0.6 * day_night_factor + 0.0 * (1.0 - day_night_factor)
    g = 0.8 * day_night_factor + 0.0 * (1.0 - day_night_factor)
    b = 1.0 * day_night_factor + 0.0 * (1.0 - day_night_factor)
    glClearColor(r, g, b, 1.0)


def draw_rect(x1, y1, x2, y2):
    """Draw a filled axis-aligned rectangle using two triangles.

    We avoid `GL_QUADS` since it's deprecated in modern OpenGL. Two
    triangles (six vertices) will draw a filled rectangle efficiently
    in immediate mode for this educational example.
    """
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)

    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

# -----------------------------
# Scene drawing functions
# -----------------------------

def draw_ground():
    """Draw the ground as a large rectangle at the bottom half of the
    scene. Use `set_color` to allow day/night variants (lighter brown
    during day, darker at night).
    """
    set_color(0.6, 0.4, 0.1, 0.2, 0.1, 0.0)
    draw_rect(0, 0, winWidth, 250)


def draw_trees():
    """Draw a row of triangular trees along the horizon. Each tree is
    a single isosceles triangle placed next to the others.
    """
    set_color(0.0, 0.8, 0.0, 0.0, 0.3, 0.0)
    glBegin(GL_TRIANGLES)
    for i in range(10):
        x_start = i * 50
        # left base, right base, top
        glVertex2f(x_start, 250)
        glVertex2f(x_start + 50, 250)
        glVertex2f(x_start + 25, 310)
    glEnd()


def draw_house():
    """Draw a stylized house composed of simple geometric primitives:
    - Rectangular body
    - Triangular roof
    - Door and windows

    Each element uses `set_color` so colors transition during day/night.
    """
    # House Body (interpolates between white and gray)
    set_color(1.0, 1.0, 1.0, 0.5, 0.5, 0.5)
    draw_rect(150, 150, 350, 250)

    # Roof
    set_color(0.4, 0.2, 0.7, 0.2, 0.1, 0.4)
    glBegin(GL_TRIANGLES)
    glVertex2f(130, 250)
    glVertex2f(370, 250)
    glVertex2f(250, 340)
    glEnd()

    # Door
    set_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    draw_rect(230, 150, 270, 210)

    # Door knob (drawn as a point)
    set_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glPointSize(4)
    glBegin(GL_POINTS)
    glVertex2f(262, 180)
    glEnd()

    # Left window and cross bars
    set_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    draw_rect(175, 175, 215, 215)

    set_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(195, 175); glVertex2f(195, 215)
    glVertex2f(175, 195); glVertex2f(215, 195)
    glEnd()

    # Right window and cross bars
    set_color(0.2, 0.5, 1.0, 0.1, 0.25, 0.5)
    draw_rect(285, 175, 325, 215)

    set_color(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(305, 175); glVertex2f(305, 215)
    glVertex2f(285, 195); glVertex2f(325, 195)
    glEnd()


def draw_rain():
    """Render each raindrop as a short line segment. The tail's end is
    offset by `rain_dx` so the rain appears to bend with wind.

    We use semi-bright blue for the rain during day and a darker blue at
    night for visual contrast.
    """
    set_color(0.5, 0.7, 1.0, 0.3, 0.4, 0.7)

    glLineWidth(1)
    glBegin(GL_LINES)
    for drop in rain_drops:
        # start point at the raindrop head
        glVertex2f(drop[0], drop[1])
        # end point behind the head along the falling vector and
        # offset by horizontal wind component for a slanted tail
        glVertex2f(drop[0] - rain_dx * 2, drop[1] + 10)
    glEnd()

# -----------------------------
# Frame update and input
# -----------------------------

def display():
    """Main display callback called by GLUT whenever the window needs
    to be redrawn. Clears the screen, sets up projection, draws the
    scene and swaps the back buffer to the screen.
    """
    set_bg_color()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    draw_ground()
    draw_trees()
    draw_house()
    draw_rain()

    glutSwapBuffers()


def animate():
    """Idle callback used to update raindrop positions and request a
    redraw. We move each raindrop down and horizontally according to
    `rain_dx`. When a drop falls below y=0 we wrap it to the top for
    continuous rain.
    """
    global rain_drops, rain_dx, winWidth, winHeight

    for drop in rain_drops:
        drop[1] -= 5  # move downwards each frame
        drop[0] += rain_dx  # apply horizontal wind effect

        # Wrap vertically: if below the bottom, place at the top
        if drop[1] < 0:
            drop[1] = winHeight

        # Wrap horizontally: keep drops inside [0, winWidth]
        if drop[0] < 0:
            drop[0] = winWidth
        elif drop[0] > winWidth:
            drop[0] = 0

    # Ask GLUT to call `display()` soon
    glutPostRedisplay()


def special_keys(key, x, y):
    """Handle special (non-ASCII) keys like the arrow keys. Left/Right
    adjust the `rain_dx` which changes how the rain bends.
    """
    global rain_dx
    if key == GLUT_KEY_LEFT:
        rain_dx -= 0.5
    elif key == GLUT_KEY_RIGHT:
        rain_dx += 0.5
    glutPostRedisplay()


def keyboard(key, x, y):
    """Handle regular keyboard keys. `D` increases day factor, `N`
    decreases it. We clamp to [0.0, 1.0].
    """
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

# -----------------------------
# Program entry point
# -----------------------------

def main():
    """Initialize GLUT, set up window and callbacks, and start the
    main loop. This is the standard structure for simple GLUT-based
    applications.
    """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Assi1 Explained: House in Rain")

    # Register callbacks
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)

    # Enter the GLUT event processing loop
    glutMainLoop()

if __name__ == "__main__":
    main()
