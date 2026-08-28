from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time


# =========================
# CONSTANTS
# =========================
GRID_LENGTH = 2500
ROOM_HEIGHT = 900
SQUARE_SIZE = 250
PICKUP_RADIUS = 350

fovY = 85

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

PALETTE = {
    "cream": (0.91, 0.86, 0.74),
    "cream_light": (0.97, 0.94, 0.86),
    "teal": (0.25, 0.50, 0.48),
    "teal_dark": (0.16, 0.34, 0.35),
    "teal_light": (0.46, 0.65, 0.61),
    "terracotta": (0.72, 0.34, 0.25),
    "terracotta_light": (0.84, 0.47, 0.35),
    "wood": (0.45, 0.30, 0.20),
    "sage": (0.48, 0.62, 0.45),
    "gold": (0.84, 0.65, 0.31),
    "metal": (0.63, 0.66, 0.65),
    "dark": (0.12, 0.16, 0.16),
}


CAMERA_HEIGHT_MIN = 500
CAMERA_HEIGHT_MAX = 1900
CAMERA_HEIGHT_STEP = 60
PLAYER_SPEED = 90
TURN_SPEED = 8


# Fixed kitchen station coordinates (x, y) on the floor plane.
STATIONS = {
    "storage_table": (-2000, -1000),
    "cutting":       (-1000, -2000),
    "stove":         (0, -2000),
    "fryer":         (1000, -2000),
    "mixing":        (2000, -2000),
    "oven":          (2000, -1000),
    "prep":          (-2000, 0),
    "plating":       (2000, 0),
    "customer":      (0, 2000),
}


STATION_DISPLAY_NAMES = {
    "storage_table": "Storage Table",
    "cutting":       "Cutting Station",
    "stove":         "Stove / Oven",
    "fryer":         "Fryer",
    "mixing":        "Mixing Station",
    "oven":          "Oven Station",
    "prep":          "Prep Table",
    "plating":       "Plating Counter",
    "customer":      "Customer",
}


# =========================
# FEATURE 1 & 2 DATA & STATES
# =========================
REQUIRED_INGREDIENTS = ["Tomato", "Onion", "Carrot"]
INCORRECT_INGREDIENTS = ["Sausage", "Potato", "Frozen Patty", "Cucumber"]

MAX_INVENTORY_CAP = 3

STATE_COLLECTING = "COLLECTING"
STATE_CUTTING = "CUTTING"
STATE_COOKING = "COOKING"
STATE_PLATING = "PLATING"
STATE_LEVEL_COMPLETE = "LEVEL_COMPLETE"

# Level 2 Burger Gameplay States
STATE_L2_COLLECTING = "BURGER_INGREDIENT_COLLECTION"
STATE_L2_FRYING = "PATTY_FRYING"
STATE_L2_PATTY_READY = "PATTY_READY"
STATE_L2_ASSEMBLY = "BURGER_ASSEMBLY"
STATE_L2_COMPLETE = "BURGER_COMPLETE"

# Level 2 French Fries Gameplay States
STATE_FRIES_COLLECTING = "POTATO_COLLECTION"
STATE_FRIES_CUTTING = "POTATO_CUTTING"
STATE_FRIES_BOILING = "POTATO_BOILING"
STATE_FRIES_FRYING = "FRIES_FRYING"
STATE_FRIES_READY = "FRIES_READY"

# Level 3 Pizza Gameplay States
STATE_L3_COLLECTING_SAUSAGE = "SAUSAGE_COLLECTION"
STATE_L3_SAUSAGE_CUTTING = "PIZZA_SAUSAGE_CUTTING"
STATE_L3_DOUGH_MAKING = "PIZZA_DOUGH_MAKING"
STATE_L3_TOPPING = "PIZZA_TOPPING"
STATE_L3_BAKING = "PIZZA_BAKING"
STATE_L3_COMPLETE = "PIZZA_COMPLETE"

PATTY_STATE_FROZEN = "FROZEN"
PATTY_STATE_FRYING = "FRYING"
PATTY_STATE_COOKED = "COOKED"
PATTY_STATE_BURNT = "BURNT"

PIZZA_STATE_UNCOOKED = "UNCOOKED"
PIZZA_STATE_BAKING = "BAKING"
PIZZA_STATE_COOKED = "COOKED"
PIZZA_STATE_BURNT = "BURNT"

CUT_REQUIREMENT = 3
CUTS_PER_VEGETABLE = 3          # each vegetable must be cut into 3 pieces
TOTAL_VEG_CUTS = CUT_REQUIREMENT * CUTS_PER_VEGETABLE
POTATO_CUT_REQUIREMENT = 4
SAUSAGE_CUT_REQUIREMENT = 4
DOUGH_MIX_REQUIREMENT = 5
PLATING_REQUIREMENT = 3
KNIFE_ANIM_DURATION = 0.3
FRYING_DURATION = 8.0  # seconds to reach 100% cooked state
BOILING_DURATION = 6.0  # seconds to reach 100% boiled state
FRIES_FRYING_DURATION = 7.0  # seconds to reach 100% crispy french fries
PIZZA_BAKING_DURATION = 8.0  # seconds to reach 100% baked state

BURGER_STEPS = ["Bottom Bun", "Cooked Patty", "Cheese", "Tomato", "Cucumber", "Top Bun"]
FRIES_TARGET_SEQUENCE = ['→', '↑', '←', '↓', '→', '↑']
PIZZA_TOPPING_STEPS = ["Dough Base", "Tomato Sauce", "Cheese", "Cut Sausage"]

# World positions for ingredients in separated baskets along the storage table
INGREDIENT_POSITIONS = {
    "Frozen Patty": {"pos": (-2000, -1600, 160), "color": (0.45, 0.40, 0.38), "shape": "cylinder"},
    "Tomato":       {"pos": (-2000, -1400, 160), "color": (0.90, 0.15, 0.12), "shape": "sphere"},
    "Onion":        {"pos": (-2000, -1200, 160), "color": (0.82, 0.67, 0.78), "shape": "sphere"},
    "Carrot":       {"pos": (-2000, -1000, 160), "color": (0.95, 0.45, 0.08), "shape": "cylinder"},
    "Sausage":      {"pos": (-2000,  -800, 160), "color": (0.85, 0.25, 0.25), "shape": "cylinder"},
    "Potato":       {"pos": (-2000,  -600, 160), "color": (0.60, 0.45, 0.25), "shape": "sphere"},
    "Cucumber":     {"pos": (-2000,  -400, 160), "color": (0.15, 0.65, 0.25), "shape": "cylinder"},
}


# =========================
# CAMERA / PLAYER STATE
# =========================
camera_pos = [200, 900, 1800]  # [yaw, height, distance]
angle = 0
hero_pos = [0, -1200, 0]
hero_pov = False

score = 0
collection_score = 0
matching_score = 0
cutting_score = 0
cooking_score = 0

game_state = STATE_COLLECTING
cutting_unlocked = False
cut_count = 0
cutting_done = False
prep_oven_unlocked = False
plating_count = 0
plating_done = False
level2_unlocked = False
level3_unlocked = False
knife_anim_start = 0.0

# Locked-camera cutting sequences (Q-key driven across all levels)
veg_cutting_active = False
veg_cutting_index = 0
veg_cut_progress = {"Tomato": 0, "Onion": 0, "Carrot": 0}
potato_cutting_active = False
sausage_cutting_active = False

# Level 2 Burger & Plating Variables
has_frozen_patty = False
patty_on_stove = False
patty_frying_start = 0.0
patty_progress = 0
patty_state = PATTY_STATE_FROZEN
has_cooked_patty = False
burger_assembly_step = 0
burger_ingredients_placed = []
burger_ready = False
burger_plated = False
l2_score = 0
l2_frying_score = 0
l2_assembly_score = 0

# Level 2 French Fries Preparation Variables
has_potato = False
potato_cut_count = 0
potato_cut_done = False
potato_boiling = False
potato_boil_start = 0.0
potato_boil_progress = 0
potato_boiled = False
fries_frying_active = False
fries_frying_start = 0.0
fries_progress = 0
fries_target_index = 0
fries_quality = 100
fries_ready = False
fries_plated = False
l2_fries_score = 0

# Level 3 Pizza Preparation Variables
has_sausage = False
sausage_cut_count = 0
sausage_cut_done = False
dough_mix_count = 0
dough_ready = False
pizza_topping_step = 0
pizza_topping_done = False
pizza_in_oven = False
pizza_baking_start = 0.0
pizza_baking_progress = 0
pizza_baked = False
pizza_state = PIZZA_STATE_UNCOOKED
l3_score = 0
l3_cutting_score = 0
l3_mixing_score = 0
l3_topping_score = 0
l3_baking_score = 0

collected_ingredients = set()

last_time = time.time()
message_log = []             # rolling list of short feedback strings for the HUD


# =========================
# GEOMETRY HELPERS
# =========================
def draw_cube(cx, cy, cz, sx, sy, sz, r, g, b):
    """Axis-aligned box centered at (cx,cy,cz) with size (sx,sy,sz). z is up."""
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
    x0, x1 = cx - hx, cx + hx
    y0, y1 = cy - hy, cy + hy
    z0, z1 = cz - hz, cz + hz
    glColor3f(r, g, b)
    faces = [
        [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],
        [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
        [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
        [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
        [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
    ]
    for f in faces:
        glBegin(GL_QUADS)
        for v in f:
            glVertex3f(*v)
        glEnd()


def draw_sphere(cx, cy, cz, radius, r, g, b, slices=8, stacks=6):
    """Simple UV sphere approximation, purely from quads."""
    glColor3f(r, g, b)
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + float(i) / stacks)
        lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
        for j in range(slices):
            lon0 = 2 * math.pi * float(j) / slices
            lon1 = 2 * math.pi * float(j + 1) / slices

            def pt(lat, lon):
                x = cx + radius * math.cos(lat) * math.cos(lon)
                y = cy + radius * math.cos(lat) * math.sin(lon)
                z = cz + radius * math.sin(lat)
                return (x, y, z)

            v0, v1, v2, v3 = pt(lat0, lon0), pt(lat0, lon1), pt(lat1, lon1), pt(lat1, lon0)
            glBegin(GL_QUADS)
            glVertex3f(*v0)
            glVertex3f(*v1)
            glVertex3f(*v2)
            glVertex3f(*v3)
            glEnd()


def draw_cylinder(cx, cy, cz, radius, height, r, g, b, slices=10):
    """Simple cylinder with a top cap, purely from quads/triangles."""
    glColor3f(r, g, b)
    for j in range(slices):
        a0 = 2 * math.pi * j / slices
        a1 = 2 * math.pi * (j + 1) / slices
        x0, y0 = cx + radius * math.cos(a0), cy + radius * math.sin(a0)
        x1, y1 = cx + radius * math.cos(a1), cy + radius * math.sin(a1)
        glBegin(GL_QUADS)
        glVertex3f(x0, y0, cz)
        glVertex3f(x1, y1, cz)
        glVertex3f(x1, y1, cz + height)
        glVertex3f(x0, y0, cz + height)
        glEnd()
    for j in range(slices):
        a0 = 2 * math.pi * j / slices
        a1 = 2 * math.pi * (j + 1) / slices
        x0, y0 = cx + radius * math.cos(a0), cy + radius * math.sin(a0)
        x1, y1 = cx + radius * math.cos(a1), cy + radius * math.sin(a1)
        glBegin(GL_TRIANGLES)
        glVertex3f(cx, cy, cz + height)
        glVertex3f(x0, y0, cz + height)
        glVertex3f(x1, y1, cz + height)
        glEnd()


def draw_marker(x, y, z, r, g, b, size=40):
    """Small floating diamond marker."""
    glColor3f(r, g, b)
    glBegin(GL_TRIANGLES)
    glVertex3f(x, y, z + size)
    glVertex3f(x - size, y, z)
    glVertex3f(x + size, y, z)

    glVertex3f(x, y, z + size)
    glVertex3f(x, y - size, z)
    glVertex3f(x, y + size, z)
    glEnd()


def draw_knife(x, y, z, angle_deg=0.0):
    """3D chef's knife prop: metallic silver blade and wooden handle."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(angle_deg, 0, 0, 1)

    # Blade (metallic silver / steel)
    glColor3f(0.82, 0.85, 0.90)
    glBegin(GL_QUADS)
    glVertex3f(-7, -10, 0)
    glVertex3f(7, -10, 0)
    glVertex3f(7, 85, 0)
    glVertex3f(-7, 85, 0)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex3f(-7, 85, 0)
    glVertex3f(7, 85, 0)
    glVertex3f(0, 105, 0)
    glEnd()

    # Knife bevel / sharp edge shine
    glColor3f(0.92, 0.95, 0.98)
    glBegin(GL_QUADS)
    glVertex3f(-2, -10, 1)
    glVertex3f(2, -10, 1)
    glVertex3f(2, 85, 1)
    glVertex3f(-2, 85, 1)
    glEnd()

    # Bolster / Steel Collar
    glColor3f(0.60, 0.62, 0.66)
    glBegin(GL_QUADS)
    glVertex3f(-9, -18, 0)
    glVertex3f(9, -18, 0)
    glVertex3f(9, -10, 0)
    glVertex3f(-9, -10, 0)
    glEnd()

    # Handle (dark ergonomic wooden grip)
    glColor3f(0.28, 0.18, 0.12)
    glBegin(GL_QUADS)
    glVertex3f(-8, -95, 0)
    glVertex3f(8, -95, 0)
    glVertex3f(8, -18, 0)
    glVertex3f(-8, -18, 0)
    glEnd()

    # Silver rivets on handle
    glColor3f(0.75, 0.78, 0.82)
    for ry in (-35, -55, -75):
        glBegin(GL_QUADS)
        glVertex3f(-3, ry - 3, 1)
        glVertex3f(3, ry - 3, 1)
        glVertex3f(3, ry + 3, 1)
        glVertex3f(-3, ry + 3, 1)
        glEnd()

    glPopMatrix()


# =========================
# HUD & TEXT HELPERS
# =========================
def draw_ui_panel(x, y, w, h, bg_r=0.07, bg_g=0.10, bg_b=0.14, bg_a=0.90, border_r=0.85, border_g=0.68, border_b=0.28, border_width=2):
    """Renders a solid/semi-transparent 2D backdrop card with a colored border for high readability."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_DEPTH_TEST)

    # Filled background quad
    glColor4f(bg_r, bg_g, bg_b, bg_a)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

    # Border outline
    if border_width > 0:
        glLineWidth(border_width)
        glColor4f(border_r, border_g, border_b, min(1.0, bg_a + 0.2))
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()

    glEnable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_text(x, y, text, r=1.0, g=1.0, b=1.0, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(r, g, b)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_label_3d(x, y, z, text, font=GLUT_BITMAP_HELVETICA_18, r=1.0, g=1.0, b=1.0):
    """Render floating text label anchored at 3D world position (x, y, z)."""
    glColor3f(r, g, b)
    glPushMatrix()
    glTranslatef(x, y, z)
    glRasterPos2f(0, 0)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()


# =========================
# ENVIRONMENT & PROPS
# =========================
def grid_wall():
    gx_max = GRID_LENGTH
    gx_min = -GRID_LENGTH
    gy_max = GRID_LENGTH
    gy_min = -GRID_LENGTH
    square_size = SQUARE_SIZE

    x = gx_min
    i = 0
    while x < gx_max:
        x1 = x + square_size
        y = gy_min
        j = 0
        while y < gy_max:
            y1 = y + square_size
            if (i + j) % 2 == 0:
                glColor3f(*PALETTE["cream_light"])
            else:
                glColor3f(*PALETTE["teal_light"])
            glBegin(GL_QUADS)
            glVertex3f(x,  y,  0)
            glVertex3f(x1, y,  0)
            glVertex3f(x1, y1, 0)
            glVertex3f(x,  y1, 0)
            glEnd()
            y = y1
            j += 1
        x = x1
        i += 1


def draw_room_walls():
    gx_max, gx_min = GRID_LENGTH, -GRID_LENGTH
    gy_max, gy_min = GRID_LENGTH, -GRID_LENGTH
    h = ROOM_HEIGHT

    glColor3f(*PALETTE["cream"])
    glBegin(GL_QUADS)
    glVertex3f(gx_min, gy_min, 0)
    glVertex3f(gx_max, gy_min, 0)
    glVertex3f(gx_max, gy_min, h)
    glVertex3f(gx_min, gy_min, h)
    glEnd()

    glBegin(GL_QUADS)
    glVertex3f(gx_min, gy_max, 0)
    glVertex3f(gx_max, gy_max, 0)
    glVertex3f(gx_max, gy_max, h)
    glVertex3f(gx_min, gy_max, h)
    glEnd()

    glColor3f(*PALETTE["teal_dark"])
    glBegin(GL_QUADS)
    glVertex3f(gx_min, gy_min, 0)
    glVertex3f(gx_min, gy_max, 0)
    glVertex3f(gx_min, gy_max, h)
    glVertex3f(gx_min, gy_min, h)
    glEnd()

    glBegin(GL_QUADS)
    glVertex3f(gx_max, gy_min, 0)
    glVertex3f(gx_max, gy_max, 0)
    glVertex3f(gx_max, gy_max, h)
    glVertex3f(gx_max, gy_min, h)
    glEnd()


def draw_ingredient_storage_table():
    """Draws a long storage table with 5 separated baskets containing multiple ingredient items (visually persistent)."""
    tx, ty = -2000, -1000

    # Wooden storage tabletop & frame
    draw_cube(tx, ty, 60, 160, 1100, 110, *PALETTE["wood"])
    draw_cube(tx, ty, 120, 180, 1120, 16, *PALETTE["cream"])
    draw_label_3d(tx - 120, ty, 280, "STORAGE TABLE")

    # Render 5 separated baskets along the storage tabletop
    for name, info in INGREDIENT_POSITIONS.items():
        bx, by = info["pos"][0], info["pos"][1]
        bz = 135

        # Basket wooden crate structure
        draw_cube(bx, by, bz, 120, 140, 35, 0.45, 0.30, 0.20)
        draw_cube(bx, by, bz + 18, 110, 130, 6, 0.75, 0.60, 0.40)

        # Always draw 4 ingredient pieces inside every basket (visually persistent)
        r, g, b = info["color"]
        for ox, oy in ((-20, -20), (20, -20), (-20, 20), (20, 20)):
            if info["shape"] == "cylinder":
                draw_cylinder(bx + ox, by + oy, bz + 18, 12, 35, r, g, b)
            else:
                draw_sphere(bx + ox, by + oy, bz + 28, 15, r, g, b)
        draw_marker(bx, by, bz + 85, 1.0, 0.8, 0.2, 25)
        draw_label_3d(bx - len(name) * 3.5, by, bz + 125, name)


def draw_cutting_station_content():
    """Draws chopping board, ingredients (whole/chopped), and animated knife on the cutting table (tabletop at Z=290)."""
    cx, cy = STATIONS["cutting"]

    # --- CHOPPING BOARD (placed directly on top of the cutting table at Z=290) ---
    # Bamboo chopping board base
    draw_cube(cx, cy, 298, 340, 210, 16, 0.88, 0.74, 0.50)
    # Beveled edge rim
    draw_cube(cx, cy, 304, 320, 190, 4, 0.92, 0.78, 0.54)
    # Perimeter juice groove
    draw_cube(cx, cy + 80, 306, 280, 5, 2, 0.68, 0.52, 0.32)
    draw_cube(cx, cy - 80, 306, 280, 5, 2, 0.68, 0.52, 0.32)
    draw_cube(cx - 138, cy, 306, 5, 160, 2, 0.68, 0.52, 0.32)
    draw_cube(cx + 138, cy, 306, 5, 160, 2, 0.68, 0.52, 0.32)
    # Inner smooth cutting board surface
    draw_cube(cx, cy, 305, 270, 150, 2, 0.86, 0.72, 0.46)

    # --- INGREDIENTS ON CHOPPING BOARD ---
    # Level 1 Vegetables
    if cutting_unlocked or game_state == STATE_CUTTING:
        if not cutting_done:
            # Whole ingredients placed on the chopping board for cutting
            draw_sphere(cx - 50, cy, 335, 26, 0.90, 0.15, 0.12)  # Tomato
            draw_sphere(cx, cy, 335, 24, 0.82, 0.67, 0.78)      # Onion
            draw_cylinder(cx + 40, cy, 306, 14, 45, 0.95, 0.45, 0.08) # Carrot
        else:
            # Chopped pieces scattered on the board after cuts completed
            for ox, oy, r, g, b in (
                (-60, -25, 0.90, 0.15, 0.12),
                (-35, 25, 0.90, 0.15, 0.12),
                (-10, -20, 0.90, 0.15, 0.12),
                (15, 25, 0.82, 0.67, 0.78),
                (40, -20, 0.82, 0.67, 0.78),
                (65, 20, 0.82, 0.67, 0.78),
                (-30, -5, 0.95, 0.45, 0.08),
                (0, -5, 0.95, 0.45, 0.08),
                (30, 5, 0.95, 0.45, 0.08)
            ):
                draw_cube(cx + ox, cy + oy, 314, 18, 18, 14, r, g, b)

    # Level 2 Potato
    elif level2_unlocked and (has_potato or potato_cut_done or potato_cutting_active):
        if not potato_cut_done:
            # Whole 3D Potato on board at exact same board placement & angle
            draw_sphere(cx - 10, cy, 330, 22, 0.70, 0.52, 0.28)
            draw_sphere(cx + 10, cy, 330, 22, 0.70, 0.52, 0.28)
            draw_sphere(cx, cy, 332, 24, 0.72, 0.54, 0.30)
        else:
            # Cut Potato Fry Strips on board
            for ox, oy in ((-40, -15), (-15, 15), (10, -10), (35, 10)):
                draw_cube(cx + ox, cy + oy, 314, 32, 8, 8, 0.85, 0.70, 0.30)

    # Level 3 Sausage
    elif level3_unlocked and ((has_sausage and game_state in (STATE_L3_COLLECTING_SAUSAGE, STATE_L3_SAUSAGE_CUTTING)) or sausage_cut_done or sausage_cutting_active):
        if not sausage_cut_done:
            # Whole 3D Sausage placed on board surface (Z=305..335) at exact same board angle
            draw_cylinder(cx - 30, cy, 318, 16, 75, 0.85, 0.25, 0.25)
            draw_sphere(cx - 30, cy, 318, 16, 0.85, 0.25, 0.25)
            draw_sphere(cx + 45, cy, 318, 16, 0.85, 0.25, 0.25)
        else:
            # Cut sausage slices on board surface
            for ox in (-40, -15, 10, 35):
                draw_cylinder(cx + ox, cy, 306, 14, 12, 0.85, 0.25, 0.25)

    # --- KNIFE ON THE CUTTING TABLE / CHOPPING BOARD ---
    knife_active = False
    knife_x = cx
    knife_y = cy

    if cutting_unlocked and not cutting_done and game_state == STATE_CUTTING:
        knife_active = True
        knife_x = cx + min(cut_count, TOTAL_VEG_CUTS) * 10 - 45
    elif level2_unlocked and has_potato and not potato_cut_done:
        knife_active = True
        knife_x = cx + min(potato_cut_count, POTATO_CUT_REQUIREMENT) * 20 - 30
    elif level3_unlocked and has_sausage and not sausage_cut_done:
        knife_active = True
        knife_x = cx + min(sausage_cut_count, SAUSAGE_CUT_REQUIREMENT) * 20 - 30

    if knife_active:
        knife_z_rest = 380
        knife_z_low = 312
        elapsed = time.time() - knife_anim_start
        if elapsed < KNIFE_ANIM_DURATION and knife_anim_start > 0.0:
            t = elapsed / KNIFE_ANIM_DURATION
            swing = math.sin(t * math.pi)
            knife_z = knife_z_rest - swing * (knife_z_rest - knife_z_low)
        else:
            knife_z = knife_z_rest
        draw_knife(knife_x, knife_y, knife_z)
    else:
        # Knife resting on the right side of the chopping board on the table
        draw_knife(cx + 120, cy, 310)


def draw_station_prop(name):
    """Draws detailed prop geometry for each kitchen station."""
    if name not in STATIONS:
        return
    x, y = STATIONS[name]

    def dc(cx, cy, cz, sx, sy, sz, r, g, b):
        draw_cube(x + 2.0 * (cx - x), y + 2.0 * (cy - y), 2.0 * cz,
                  2.0 * sx, 2.0 * sy, 2.0 * sz, r, g, b)

    def ds(cx, cy, cz, radius, r, g, b, slices=8, stacks=6):
        draw_sphere(x + 2.0 * (cx - x), y + 2.0 * (cy - y), 2.0 * cz,
                    2.0 * radius, r, g, b, slices, stacks)

    def dcy(cx, cy, cz, radius, height, r, g, b, slices=10):
        draw_cylinder(x + 2.0 * (cx - x), y + 2.0 * (cy - y), 2.0 * cz,
                      2.0 * radius, 2.0 * height, r, g, b, slices)

    if name == "cutting":
        for lx in (-150, 150):
            for ly in (-70, 70):
                dcy(x + lx, y + ly, 0, 14, 130, 0.3, 0.2, 0.12)
        dc(x, y, 130, 340, 200, 30, 0.42, 0.28, 0.16)

    elif name == "stove":
        dc(x, y, 130, 320, 260, 260, 0.22, 0.22, 0.25)
        dc(x, y + 130, 130, 320, 10, 260, 0.12, 0.12, 0.14)
        dc(x, y - 60, 90, 260, 120, 140, 0.15, 0.15, 0.17)
        dc(x, y - 60, 90, 240, 8, 130, 0.35, 0.35, 0.38)
        dcy(x - 70, y - 60, 90, 6, 1, 0.6, 0.6, 0.65)
        dc(x, y + 60, 210, 250, 60, 12, 0.3, 0.3, 0.33)
        for kx in (-90, -30, 30, 90):
            dcy(x + kx, y + 60, 216, 14, 14, 0.85, 0.15, 0.1)
        dc(x, y, 260, 300, 250, 16, 0.18, 0.18, 0.2)
        for bx, by in ((-75, -60), (75, -60), (-75, 60), (75, 60)):
            dcy(x + bx, y + by, 268, 55, 14, 0.1, 0.1, 0.1)
            dcy(x + bx, y + by, 282, 30, 8, 0.35, 0.35, 0.38)

    elif name == "fryer":
        dc(x, y, 120, 260, 220, 220, 0.18, 0.18, 0.45)
        dc(x, y, 220, 220, 190, 12, 0.28, 0.3, 0.65)
        dc(x - 65, y, 210, 90, 150, 40, 0.85, 0.75, 0.15)
        dc(x + 65, y, 210, 90, 150, 40, 0.85, 0.75, 0.15)
        for bx in (-65, 65):
            dc(x + bx, y, 260, 78, 130, 10, 0.4, 0.4, 0.45)
            dc(x + bx - 30, y, 300, 8, 8, 90, 0.5, 0.5, 0.55)
            dc(x + bx + 30, y, 300, 8, 8, 90, 0.5, 0.5, 0.55)
            dc(x + bx, y, 345, 70, 8, 8, 0.5, 0.5, 0.55)
        dc(x, y + 100, 150, 240, 20, 90, 0.22, 0.22, 0.5)
        dcy(x - 80, y + 100, 210, 12, 6, 0.9, 0.2, 0.15)
        dcy(x + 80, y + 100, 210, 12, 6, 0.9, 0.2, 0.15)

    elif name == "mixing":
        for lx in (-150, 150):
            for ly in (-80, 80):
                dcy(x + lx, y + ly, 0, 16, 110, 0.35, 0.24, 0.14)
        dc(x, y, 120, 340, 220, 30, 0.65, 0.5, 0.32)
        dc(x - 30, y + 30, 190, 130, 120, 130, 0.75, 0.15, 0.15)
        dcy(x - 30, y + 30, 255, 55, 30, 0.7, 0.12, 0.12)
        dc(x - 30, y - 20, 220, 30, 30, 130, 0.6, 0.1, 0.1)
        dcy(x - 30, y - 60, 150, 90, 100, 0.92, 0.92, 0.95)
        dcy(x - 30, y - 60, 248, 6, 40, 0.55, 0.55, 0.58)
        ds(x + 120, y - 20, 160, 55, 0.85, 0.72, 0.5)
        dcy(x + 130, y + 70, 130, 40, 100, 0.85, 0.85, 0.9)
        for ux in (-15, 0, 15):
            dc(x + 130 + ux, y + 70, 235, 6, 6, 90, 0.5, 0.35, 0.2)

    elif name == "prep":
        for lx in (-150, 150):
            for ly in (-70, 70):
                dcy(x + lx, y + ly, 0, 14, 130, 0.3, 0.2, 0.12)
        dc(x, y, 130, 340, 200, 26, 0.45, 0.3, 0.18)
        dc(x - 70, y, 148, 140, 140, 8, 0.35, 0.55, 0.75)
        dc(x + 70, y, 148, 140, 140, 8, 0.75, 0.35, 0.3)
        dc(x, y + 85, 210, 260, 18, 60, 0.4, 0.26, 0.15)
        for i, sx in enumerate((-90, -50, -10, 30, 70)):
            dcy(x + sx, y + 88, 225, 12, 30, 0.8, 0.6, 0.25)
        dcy(x, y - 10, 148, 55, 45, 0.85, 0.2, 0.2)
        ds(x, y - 10, 190, 30, 0.85, 0.75, 0.55)

    elif name == "plating":
        for lx in (-150, 150):
            for ly in (-70, 70):
                dcy(x + lx, y + ly, 0, 15, 130, 0.4, 0.32, 0.22)
        dc(x, y, 130, 320, 200, 26, 0.55, 0.42, 0.28)
        dc(x, y, 150, 300, 180, 10, 0.9, 0.9, 0.92)
        for i in range(4):
            dcy(x - 110, y, 158 + i * 10, 75, 8, 0.97, 0.97, 0.98)
        dcy(x + 40, y - 10, 160, 85, 10, 0.97, 0.97, 0.98)
        ds(x + 40, y - 10, 178, 40, 0.55, 0.35, 0.2)
        dcy(x + 40, y - 10, 220, 65, 55, 0.85, 0.9, 0.95)
        dc(x + 130, y + 70, 165, 90, 60, 10, 0.75, 0.6, 0.4)
        ds(x + 110, y + 70, 178, 14, 0.2, 0.6, 0.2)
        ds(x + 140, y + 70, 178, 14, 0.85, 0.2, 0.2)
        ds(x + 155, y + 55, 178, 14, 0.9, 0.85, 0.2)

    elif name == "oven":
        # Heavy metallic oven counter base cabinet
        dc(x, y, 130, 320, 220, 260, 0.22, 0.24, 0.26)
        # Stainless steel top frame
        dc(x, y, 260, 340, 240, 16, 0.45, 0.48, 0.50)
        # Oven door frame (Dark metal)
        dc(x - 60, y, 130, 20, 200, 190, 0.15, 0.15, 0.18)
        # Oven glass window with glowing warm orange heating interior
        dc(x - 65, y, 130, 10, 160, 150, 0.90, 0.45, 0.10)
        # Oven door handle (Metallic chrome bar)
        dc(x - 80, y, 195, 12, 140, 12, 0.75, 0.78, 0.80)
        # Front control panel knobs
        for ky in (-60, -20, 20, 60):
            dcy(x - 60, y + ky, 235, 10, 10, 0.85, 0.15, 0.10)
        # Top baking ventilation hood
        dc(x, y, 275, 260, 180, 10, 0.18, 0.20, 0.22)

    elif name == "customer":
        dcy(x, y, 0, 260, 20, 0.55, 0.4, 0.25)
        dcy(x, y, 20, 30, 90, 0.35, 0.25, 0.15)
        dcy(x, y, 110, 260, 20, 0.62, 0.46, 0.28)
        dcy(x, y, 132, 60, 8, 0.95, 0.95, 0.97)
        for i, off in enumerate((-320, 0, 320)):
            bx, by = x + off, y + 260
            dcy(bx, by, 0, 55, 70, 0.4, 0.3, 0.2)
            dc(bx, by + 45, 130, 100, 15, 140, 0.35, 0.25, 0.16)
            dcy(bx, by - 40, 90, 55, 60, 0.32, 0.5, 0.82)
            ds(bx, by - 40, 170, 48, 0.92, 0.78, 0.62)
            dcy(bx, by - 55, 60, 40, 55, 0.25, 0.4, 0.7)
            ds(bx - 55, by - 20, 110, 18, 0.92, 0.78, 0.62)
            ds(bx + 55, by - 20, 110, 18, 0.92, 0.78, 0.62)


def draw_plating_station_content():
    """Draws 3D plate and dynamically placed prepared ingredients at Plating Station."""
    px, py = STATIONS["plating"]

    # 3D Ceramic Plate (using allowed cylinder primitives)
    draw_cylinder(px, py, 150, 95, 14, 0.95, 0.95, 0.97)
    draw_cylinder(px, py, 162, 82, 4, 0.88, 0.88, 0.92)

    # Dynamically render plated ingredients based on plating_count
    if plating_count >= 1:
        # Diced tomatoes (Red)
        for ox, oy in ((-30, -15), (-15, 20), (25, -10)):
            draw_cube(px + ox, py + oy, 172, 22, 22, 14, 0.90, 0.15, 0.12)

    if plating_count >= 2:
        # Diced onions (Light purple)
        for ox, oy in ((10, 15), (-25, 5), (5, -30)):
            draw_cube(px + ox, py + oy, 175, 20, 20, 12, 0.82, 0.67, 0.78)

    if plating_count >= 3:
        # Diced carrots (Orange) placed neatly on top to complete dish
        for ox, oy in ((0, 0), (-10, -10), (15, -5), (10, -20)):
            draw_cube(px + ox, py + oy, 180, 18, 18, 14, 0.95, 0.45, 0.08)

    # Level 2 Plated Burger
    if burger_plated:
        draw_cylinder(px - 30, py, 166, 45, 12, 0.75, 0.50, 0.22) # Bottom bun
        draw_cylinder(px - 30, py, 178, 42, 10, 0.38, 0.18, 0.08) # Patty
        draw_cube(px - 30, py, 192, 70, 70, 6, 0.95, 0.85, 0.15)   # Cheese
        draw_cylinder(px - 30, py, 198, 45, 12, 0.78, 0.52, 0.24) # Top bun

    # Level 2 Plated French Fries
    if fries_plated:
        for ox, oy in ((-10, -20), (5, 0), (20, -15), (-5, 15), (15, 15)):
            draw_cube(px + 30 + ox, py + oy, 172, 6, 26, 6, 0.95, 0.78, 0.15)


def draw_boiling_pot_content():
    """Draws 3D metallic boiling pot on stove with potato strips and rising bubbles."""
    sx, sy = STATIONS["stove"]

    # Metallic Cooking Pot body (resting on back right stove burner at Z=565)
    draw_cylinder(sx + 150, sy - 120, 565, 90, 75, 0.55, 0.58, 0.62)
    # Pot Rim & Handles
    draw_cylinder(sx + 150, sy - 120, 635, 95, 8, 0.45, 0.48, 0.52)
    draw_cube(sx + 240, sy - 120, 605, 36, 30, 16, 0.25, 0.25, 0.28)
    draw_cube(sx + 60, sy - 120, 605, 36, 30, 16, 0.25, 0.25, 0.28)

    # Water surface inside pot
    draw_cylinder(sx + 150, sy - 120, 630, 84, 8, 0.35, 0.65, 0.88)

    if potato_cut_done or potato_boiling or potato_boiled:
        # Potato strips inside pot/water (transferred immediately after cutting)
        draw_cube(sx + 135, sy - 120, 634, 18, 65, 14, 0.92, 0.82, 0.35)
        draw_cube(sx + 165, sy - 120, 634, 18, 65, 14, 0.92, 0.82, 0.35)

        # Rising bubbles and steam particles when boiling
        if potato_boiling and potato_boil_progress < 100:
            t_now = time.time()
            for i, (ox, oy) in enumerate(((-25, -15), (20, 20), (-10, 30), (25, -15))):
                b_z = 640 + ((t_now * 40 + i * 15) % 45)
                draw_sphere(sx + 150 + ox, sy - 120 + oy, b_z, 8, 0.95, 0.95, 0.98)


def draw_fries_frying_pan_content():
    """Draws right frying pan for fries on stove with red rim and sizzling golden fries (always visible throughout game)."""
    sx, sy = STATIONS["stove"]

    # Right Frying Pan (always visible on top of front right stove burner at Z=565: bright red rim with handle)
    draw_cylinder(sx + 150, sy + 120, 565, 95, 28, 0.85, 0.20, 0.18)
    draw_cylinder(sx + 150, sy + 120, 568, 85, 8, 0.18, 0.18, 0.20)
    # Pan handle
    draw_cube(sx + 270, sy + 120, 578, 120, 24, 20, 0.25, 0.25, 0.28)

    if potato_cut_done or potato_boiling or potato_boiled or fries_frying_active or fries_ready:
        # Sizzling golden french fries inside right pan (transferred immediately after cutting)
        for ox, oy in ((-35, -20), (0, 20), (30, -20), (-20, 25), (35, 10)):
            draw_cube(sx + 150 + ox, sy + 120 + oy, 580, 16, 55, 14, 0.95, 0.78, 0.15)

        if fries_frying_active:
            t_now = time.time()
            for i, (ox, oy) in enumerate(((-20, -20), (20, 20), (-10, 30), (30, -10))):
                st_z = 600 + ((t_now * 45 + i * 18) % 45)
                draw_sphere(sx + 150 + ox, sy + 120 + oy, st_z, 9, 0.95, 0.95, 0.95)


def draw_stove_frying_content():
    """Draws left frying pan on stove with red rim and patty (always visible throughout game)."""
    sx, sy = STATIONS["stove"]

    # Left Frying Pan (always visible on top of front left stove burner at Z=565: bright red rim with handle)
    draw_cylinder(sx - 150, sy + 120, 565, 95, 28, 0.85, 0.20, 0.18)
    draw_cylinder(sx - 150, sy + 120, 568, 85, 8, 0.18, 0.18, 0.20)
    # Pan handle
    draw_cube(sx - 270, sy + 120, 578, 120, 24, 20, 0.25, 0.25, 0.28)

    # Render patty inside left frying pan if placed on stove or frying
    if patty_on_stove or (game_state in (STATE_L2_FRYING, STATE_L2_PATTY_READY) and patty_state != PATTY_STATE_FROZEN):
        # Color based on frying progress / state
        if patty_state == PATTY_STATE_BURNT or patty_progress > 115:
            r, g, b = 0.08, 0.08, 0.08  # Burnt black
        elif patty_state == PATTY_STATE_COOKED or (60 <= patty_progress <= 115):
            r, g, b = 0.38, 0.18, 0.08  # Rich seared brown
        elif patty_progress > 0:
            # Transitioning from frozen grey-brown to cooked brown
            t = min(1.0, patty_progress / 100.0)
            r = 0.45 - 0.07 * t
            g = 0.40 - 0.22 * t
            b = 0.38 - 0.30 * t
        else:
            r, g, b = 0.45, 0.40, 0.38  # Frozen greyish brown

        draw_cylinder(sx - 150, sy + 120, 578, 68, 24, r, g, b)

        # Sizzling steam particles when frying
        if patty_state == PATTY_STATE_FRYING and patty_progress > 0:
            t_now = time.time()
            for i, (ox, oy) in enumerate(((-25, -20), (20, 25), (-10, 35), (35, -15))):
                st_z = 605 + ((t_now * 45 + i * 18) % 50)
                draw_sphere(sx - 150 + ox, sy + 120 + oy, st_z, 10, 0.90, 0.90, 0.95)


def draw_burger_assembly_content():
    """Draws 3D burger stack layer by layer at Prep Table for Level 2."""
    px, py = STATIONS["prep"]

    # Only render burger assembly if in Level 2 assembly or completed stage
    if burger_assembly_step > 0 or game_state in (STATE_L2_ASSEMBLY, STATE_L2_COMPLETE):
        cur_z = 150  # Start on top of prep table surface

        # 1. Bottom Bun
        if burger_assembly_step >= 1:
            draw_cylinder(px, py, cur_z, 65, 18, 0.75, 0.50, 0.22)
            cur_z += 18

        # 2. Cooked Patty
        if burger_assembly_step >= 2:
            draw_cylinder(px, py, cur_z, 62, 16, 0.38, 0.18, 0.08)
            cur_z += 16

        # 3. Cheese Slice (Yellow square)
        if burger_assembly_step >= 3:
            draw_cube(px, py, cur_z + 4, 110, 110, 8, 0.95, 0.85, 0.15)
            cur_z += 8

        # 4. Tomato Slice (Red round)
        if burger_assembly_step >= 4:
            draw_cylinder(px, py, cur_z, 58, 10, 0.90, 0.15, 0.12)
            cur_z += 10

        # 5. Cucumber Slice (Green round)
        if burger_assembly_step >= 5:
            draw_cylinder(px, py, cur_z, 54, 10, 0.15, 0.65, 0.25)
            cur_z += 10

        # 6. Top Bun (Domed golden bun)
        if burger_assembly_step >= 6:
            draw_cylinder(px, py, cur_z, 65, 16, 0.78, 0.52, 0.24)
            draw_sphere(px, py, cur_z + 16, 50, 0.78, 0.52, 0.24)


def draw_sausage_cutting_content():
    """Unified cutting station content (handled in draw_cutting_station_content)."""
    pass


def draw_dough_mixing_content():
    """Draws 3D mixing bowl with flour or flat pizza dough disc at Mixing Station."""
    mx, my = STATIONS["mixing"]
    if game_state in (STATE_L3_SAUSAGE_CUTTING, STATE_L3_DOUGH_MAKING) or dough_ready:
        # Mixing bowl
        draw_cylinder(mx - 30, my - 60, 150, 70, 50, 0.85, 0.88, 0.92)
        if not dough_ready:
            # Raw flour / dough mix inside bowl
            draw_cylinder(mx - 30, my - 60, 185, 60, 10, 0.95, 0.92, 0.82)
            # Animated mixing paddle
            t_now = time.time()
            pad_angle = (t_now * 360) if dough_mix_count > 0 else 0
            glPushMatrix()
            glTranslatef(mx - 30, my - 60, 195)
            glRotatef(pad_angle, 0, 0, 1)
            draw_cube(0, 0, 20, 10, 50, 30, 0.45, 0.30, 0.18)
            glPopMatrix()
        else:
            # Formed smooth flat pizza dough disc
            draw_cylinder(mx - 30, my - 60, 195, 62, 8, 0.91, 0.82, 0.65)


def draw_pizza_assembly_content():
    """Draws 3D pizza dough disc and toppings layer by layer at Prep Table."""
    px, py = STATIONS["prep"]
    if game_state in (STATE_L3_TOPPING, STATE_L3_BAKING, STATE_L3_COMPLETE) or pizza_topping_done:
        # Step 0: Base Pizza Dough Disc (Cream)
        draw_cylinder(px, py, 150, 75, 10, 0.91, 0.82, 0.65)

        # Step 1: Tomato Sauce Layer (Red)
        if pizza_topping_step >= 1:
            draw_cylinder(px, py, 160, 68, 4, 0.88, 0.18, 0.12)

        # Step 2: Cheese Layer (Yellow)
        if pizza_topping_step >= 2:
            draw_cylinder(px, py, 164, 64, 4, 0.95, 0.85, 0.15)

        # Step 3: Cut Sausage Slices (Pinkish Red round slices)
        if pizza_topping_step >= 3:
            for ox, oy in ((-30, -20), (20, -25), (0, 30), (-25, 20), (30, 15), (0, -5)):
                draw_cylinder(px + ox, py + oy, 168, 12, 6, 0.80, 0.28, 0.22)


def draw_pizza_oven_content():
    """Draws 3D raw/baked pizza inside Oven Station when baking."""
    ox, oy = STATIONS["oven"]
    if pizza_in_oven or (game_state == STATE_L3_COMPLETE and pizza_baked):
        # Pizza inside oven shelf
        r, g, b = (0.91, 0.82, 0.65) if not pizza_baked else (0.75, 0.50, 0.20)
        draw_cylinder(ox - 65, oy, 160, 55, 12, r, g, b)
        # Toppings on oven pizza
        draw_cylinder(ox - 65, oy, 172, 48, 4, 0.88, 0.18, 0.12)
        draw_cylinder(ox - 65, oy, 176, 44, 4, 0.95, 0.85, 0.15)


def draw_fryer_content():
    """Draws deep fryer interior, bubbling hot oil, fryer baskets, and sizzling french fries at the Fryer Station."""
    fx, fy = STATIONS["fryer"]

    # Sizzling golden french fries inside the fryer baskets when fries are frying or ready
    if potato_boiled or fries_frying_active or fries_ready:
        for bx in (-65, 65):
            for ox, oy in ((-20, -15), (10, 15), (-10, 20), (18, -10), (0, 0)):
                draw_cube(fx + bx + ox, fy + oy, 240, 14, 48, 12, 0.95, 0.78, 0.15)

        # Sizzling bubbles and steam when deep frying
        if fries_frying_active:
            t_now = time.time()
            for bx in (-65, 65):
                for i, (ox, oy) in enumerate(((-18, -15), (15, 15), (-8, 20), (18, -8))):
                    b_z = 245 + ((t_now * 50 + i * 15) % 40)
                    draw_sphere(fx + bx + ox, fy + oy, b_z, 7, 0.96, 0.92, 0.5)


def draw_kitchen_props():
    for name in STATIONS:
        draw_station_prop(name)
    draw_ingredient_storage_table()
    draw_cutting_station_content()
    draw_plating_station_content()
    draw_stove_frying_content()
    draw_boiling_pot_content()
    draw_fries_frying_pan_content()
    draw_fryer_content()
    draw_burger_assembly_content()
    draw_sausage_cutting_content()
    draw_dough_mixing_content()
    draw_pizza_assembly_content()
    draw_pizza_oven_content()
    draw_cube(-2600, 2600, 50, 90, 90, 100, 0.5, 0.35, 0.2)
    draw_cube(-2400, 2600, 50, 90, 90, 100, 0.55, 0.4, 0.22)
    draw_cylinder(2600, -2600, 0, 60, 160, 0.4, 0.4, 0.42)
    draw_station_labels()


def draw_station_labels():
    """Draw high-contrast floating nameplates and live timer badges above every kitchen station."""
    now = time.time()
    for name, (sx, sy) in STATIONS.items():
        label = STATION_DISPLAY_NAMES.get(name, name.upper())
        text_w = len(label) * 16.0

        draw_cube(sx, sy, 370, text_w + 50, 18, 44, 0.11, 0.14, 0.16)
        draw_cube(sx, sy, 370, text_w + 58, 14, 48, 0.85, 0.68, 0.28)
        draw_label_3d(sx - (text_w / 2.0) + 4, sy - 10, 362, label, GLUT_BITMAP_HELVETICA_18, 1.0, 0.96, 0.82)

        # Dynamic live status & timer badges for active cooking stations
        if name in ("stove", "fryer"):
            if name == "stove" and potato_boiling and potato_boil_progress < 100:
                elapsed = now - potato_boil_start
                b_text = f"POT BOILING: {potato_boil_progress}% ({elapsed:.1f}s / {BOILING_DURATION:.1f}s)"
                bw = len(b_text) * 15.0
                draw_cube(sx, sy, 435, bw + 40, 18, 36, 0.15, 0.30, 0.45)
                draw_label_3d(sx - (bw / 2.0), sy - 10, 428, b_text, GLUT_BITMAP_HELVETICA_18, 0.4, 0.85, 1.0)
            elif name == "stove" and patty_on_stove:
                elapsed = now - patty_frying_start
                if 60 <= patty_progress <= 115:
                    p_text = f"PATTY READY! {patty_progress}% ({elapsed:.1f}s / {FRYING_DURATION:.1f}s)"
                    pw = len(p_text) * 15.0
                    draw_cube(sx, sy, 435, pw + 40, 18, 36, 0.12, 0.42, 0.15)
                    draw_label_3d(sx - (pw / 2.0), sy - 10, 428, p_text, GLUT_BITMAP_HELVETICA_18, 0.3, 1.0, 0.3)
                elif patty_progress > 115:
                    p_text = "PATTY BURNT! (-20 pts)"
                    pw = len(p_text) * 15.0
                    draw_cube(sx, sy, 435, pw + 40, 18, 36, 0.5, 0.1, 0.1)
                    draw_label_3d(sx - (pw / 2.0), sy - 10, 428, p_text, GLUT_BITMAP_HELVETICA_18, 1.0, 0.3, 0.3)
                else:
                    p_text = f"PATTY FRYING: {patty_progress}% ({elapsed:.1f}s / {FRYING_DURATION:.1f}s)"
                    pw = len(p_text) * 15.0
                    draw_cube(sx, sy, 435, pw + 40, 18, 36, 0.45, 0.25, 0.08)
                    draw_label_3d(sx - (pw / 2.0), sy - 10, 428, p_text, GLUT_BITMAP_HELVETICA_18, 1.0, 0.75, 0.2)

            if name == "fryer" and (fries_frying_active or (potato_boiled and not fries_ready)):
                if fries_frying_active:
                    elapsed = now - fries_frying_start
                    if 60 <= fries_progress <= 115:
                        f_text = f"FRIES READY! {fries_progress}% ({elapsed:.1f}s / {FRIES_FRYING_DURATION:.1f}s)"
                        fw = len(f_text) * 15.0
                        draw_cube(sx, sy, 435, fw + 40, 18, 36, 0.12, 0.42, 0.15)
                        draw_label_3d(sx - (fw / 2.0), sy - 10, 428, f_text, GLUT_BITMAP_HELVETICA_18, 0.3, 1.0, 0.3)
                    elif fries_progress > 115:
                        f_text = "FRIES BURNT! (-20 pts)"
                        fw = len(f_text) * 15.0
                        draw_cube(sx, sy, 435, fw + 40, 18, 36, 0.5, 0.1, 0.1)
                        draw_label_3d(sx - (fw / 2.0), sy - 10, 428, f_text, GLUT_BITMAP_HELVETICA_18, 1.0, 0.3, 0.3)
                    else:
                        f_text = f"FRYER SIZZLING: {fries_progress}% ({elapsed:.1f}s / {FRIES_FRYING_DURATION:.1f}s)"
                        fw = len(f_text) * 15.0
                        draw_cube(sx, sy, 435, fw + 40, 18, 36, 0.45, 0.30, 0.08)
                        draw_label_3d(sx - (fw / 2.0), sy - 10, 428, f_text, GLUT_BITMAP_HELVETICA_18, 1.0, 0.85, 0.2)


def draw_player():
    """Chef model: solid 3D opaque geometry hierarchy using allowed GLUT / GL calls."""
    glPushMatrix()
    glTranslatef(hero_pos[0], hero_pos[1], 0)
    glRotatef(angle, 0, 0, 1)
    glScalef(2.5, 2.5, 2.5)

    # ---- TORSO / CHEF JACKET (White / Light Grey solid coat) ----
    glColor3f(0.92, 0.92, 0.95)
    glPushMatrix()
    glTranslatef(0, 0, 130)
    glScalef(90, 65, 110)
    glutSolidCube(1.0)
    glPopMatrix()

    # ---- JACKET BUTTONS (Dark accent) ----
    glColor3f(0.15, 0.15, 0.18)
    for bx in (-18, 18):
        for bz in (100, 130, 160):
            glPushMatrix()
            glTranslatef(bx, -33, bz)
            glScalef(8, 6, 8)
            glutSolidCube(1.0)
            glPopMatrix()

    # ---- APRON front (cream/gold) ----
    glColor3f(*PALETTE["cream_light"])
    glPushMatrix()
    glTranslatef(0, -38, 120)
    glScalef(60, 6, 95)
    glutSolidCube(1.0)
    glPopMatrix()

    # ---- NECK ----
    draw_cylinder(0, 0, 180, 16, 25, 0.93, 0.76, 0.58)

    # ---- HEAD ----
    draw_sphere(0, 0, 220, 40, 0.93, 0.76, 0.58)

    # ---- CHEF HAT ----
    # Hat base brim
    draw_cylinder(0, 0, 255, 44, 18, *PALETTE["cream_light"])
    # Hat main body
    draw_cylinder(0, 0, 273, 36, 45, *PALETTE["cream_light"])
    # Hat top puff
    draw_sphere(0, 0, 325, 30, *PALETTE["cream_light"])

    # ---- LEGS (Dark trousers) ----
    for lx in (-22, 22):
        draw_cylinder(lx, 0, 0, 17, 80, 0.12, 0.12, 0.16)
        # Shoes
        glColor3f(0.08, 0.08, 0.08)
        glPushMatrix()
        glTranslatef(lx, -10, 8)
        glScalef(30, 24, 16)
        glutSolidCube(1.0)
        glPopMatrix()

    # ---- ARMS & HANDS ----
    for ax in (-52, 52):
        draw_cylinder(ax, 0, 115, 15, 60, 0.90, 0.90, 0.93)
        draw_sphere(ax, 0, 110, 16, 0.93, 0.76, 0.58)

    glPopMatrix()


# =========================
# UTILITY / POSITION HELPER
# =========================
def distance_between(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)


def clamp_player_position():
    limit = GRID_LENGTH - 80
    hero_pos[0] = max(-limit, min(limit, hero_pos[0]))
    hero_pos[1] = max(-limit, min(limit, hero_pos[1]))


def player_near_station(name, radius=PICKUP_RADIUS):
    if name not in STATIONS:
        return False
    sx, sy = STATIONS[name]
    return distance_between(hero_pos[0], hero_pos[1], sx, sy) <= radius


def nearest_station_within_radius(radius=PICKUP_RADIUS):
    best, best_d = None, None
    for name, (sx, sy) in STATIONS.items():
        d = distance_between(hero_pos[0], hero_pos[1], sx, sy)
        if d <= radius and (best_d is None or d < best_d):
            best, best_d = name, d
    return best


def log_message(text):
    message_log.append(text)
    del message_log[:-4]


def reset_game():
    global hero_pos, angle, score, cutting_unlocked, game_state, hero_pov
    global cut_count, cutting_done, prep_oven_unlocked, knife_anim_start
    global plating_count, plating_done, level2_unlocked, level3_unlocked
    global collection_score, matching_score, cutting_score, cooking_score
    global veg_cutting_active, veg_cutting_index, veg_cut_progress
    global potato_cutting_active, sausage_cutting_active
    global has_frozen_patty, patty_on_stove, patty_frying_start, patty_progress, patty_state
    global has_cooked_patty, burger_assembly_step, burger_ingredients_placed
    global burger_ready, burger_plated, fries_plated
    global l2_score, l2_frying_score, l2_assembly_score, l2_fries_score
    global has_potato, potato_cut_count, potato_cut_done, potato_boiling
    global potato_boil_start, potato_boil_progress, potato_boiled
    global fries_frying_active, fries_frying_start, fries_progress, fries_target_index, fries_quality, fries_ready
    global has_sausage, sausage_cut_count, sausage_cut_done, dough_mix_count, dough_ready
    global pizza_topping_step, pizza_topping_done, pizza_in_oven, pizza_baking_start
    global pizza_baking_progress, pizza_baked, pizza_state
    global l3_score, l3_cutting_score, l3_mixing_score, l3_topping_score, l3_baking_score
    global collected_ingredients, message_log

    hero_pos = [0, -1200, 0]
    angle = 0
    score = 0
    collection_score = 0
    matching_score = 0
    cutting_score = 0
    cooking_score = 0
    hero_pov = False
    cutting_unlocked = False
    cut_count = 0
    cutting_done = False
    prep_oven_unlocked = False
    plating_count = 0
    plating_done = False
    level2_unlocked = False
    level3_unlocked = False
    knife_anim_start = 0.0

    veg_cutting_active = False
    veg_cutting_index = 0
    potato_cutting_active = False
    sausage_cutting_active = False
    for k in veg_cut_progress:
        veg_cut_progress[k] = 0

    has_frozen_patty = False
    patty_on_stove = False
    patty_frying_start = 0.0
    patty_progress = 0
    patty_state = PATTY_STATE_FROZEN
    has_cooked_patty = False
    burger_assembly_step = 0
    burger_ingredients_placed = []
    burger_ready = False
    burger_plated = False
    l2_score = 0
    l2_frying_score = 0
    l2_assembly_score = 0

    has_potato = False
    potato_cut_count = 0
    potato_cut_done = False
    potato_boiling = False
    potato_boil_start = 0.0
    potato_boil_progress = 0
    potato_boiled = False
    fries_frying_active = False
    fries_frying_start = 0.0
    fries_progress = 0
    fries_target_index = 0
    fries_quality = 100
    fries_ready = False
    fries_plated = False
    l2_fries_score = 0

    has_sausage = False
    sausage_cut_count = 0
    sausage_cut_done = False
    dough_mix_count = 0
    dough_ready = False
    pizza_topping_step = 0
    pizza_topping_done = False
    pizza_in_oven = False
    pizza_baking_start = 0.0
    pizza_baking_progress = 0
    pizza_baked = False
    pizza_state = PIZZA_STATE_UNCOOKED
    l3_score = 0
    l3_cutting_score = 0
    l3_mixing_score = 0
    l3_topping_score = 0
    l3_baking_score = 0

    game_state = STATE_COLLECTING
    collected_ingredients.clear()
    message_log[:] = []
    log_message("Game & Inventory fully reset to Level 1.")


def start_level_2():
    global game_state, hero_pos, angle, hero_pov, collected_ingredients
    global has_frozen_patty, patty_on_stove, patty_frying_start, patty_progress, patty_state
    global has_cooked_patty, burger_assembly_step, burger_ingredients_placed
    global burger_ready, burger_plated, fries_plated
    global l2_score, l2_frying_score, l2_assembly_score, plating_done
    global has_potato, potato_cut_count, potato_cut_done, potato_boiling
    global potato_boil_start, potato_boil_progress, potato_boiled
    global fries_frying_active, fries_frying_start, fries_progress, fries_target_index, fries_quality, fries_ready, l2_fries_score
    global potato_cutting_active

    game_state = STATE_L2_COLLECTING
    hero_pos = [0, -1200, 0]
    angle = 0
    hero_pov = False
    plating_done = False
    potato_cutting_active = False

    # Level 2 retained ingredients in inventory
    collected_ingredients = {"Tomato", "Cucumber"}

    has_frozen_patty = False
    patty_on_stove = False
    patty_frying_start = 0.0
    patty_progress = 0
    patty_state = PATTY_STATE_FROZEN
    has_cooked_patty = False
    burger_assembly_step = 0
    burger_ingredients_placed = []
    burger_ready = False
    burger_plated = False
    l2_score = 0
    l2_frying_score = 0
    l2_assembly_score = 0

    has_potato = False
    potato_cut_count = 0
    potato_cut_done = False
    potato_boiling = False
    potato_boil_start = 0.0
    potato_boil_progress = 0
    potato_boiled = False
    fries_frying_active = False
    fries_frying_start = 0.0
    fries_progress = 0
    fries_target_index = 0
    fries_quality = 100
    fries_ready = False
    fries_plated = False
    l2_fries_score = 0

    log_message("LEVEL 2 STARTED: Burger & French Fries Preparation!")


def start_level_3():
    global game_state, hero_pos, angle, hero_pov, collected_ingredients
    global has_cooked_patty, burger_ready, patty_on_stove
    global has_sausage, sausage_cut_count, sausage_cut_done, dough_mix_count, dough_ready
    global pizza_topping_step, pizza_topping_done, pizza_in_oven, pizza_baking_start
    global pizza_baking_progress, pizza_baked, pizza_state
    global l3_score, l3_cutting_score, l3_mixing_score, l3_topping_score, l3_baking_score
    global sausage_cutting_active

    game_state = STATE_L3_COLLECTING_SAUSAGE
    hero_pos = [0, -1200, 0]
    angle = 0
    hero_pov = False
    sausage_cutting_active = False
    collected_ingredients.clear()

    has_cooked_patty = False
    burger_ready = False
    patty_on_stove = False

    has_sausage = False
    sausage_cut_count = 0
    sausage_cut_done = False
    dough_mix_count = 0
    dough_ready = False
    pizza_topping_step = 0
    pizza_topping_done = False
    pizza_in_oven = False
    pizza_baking_start = 0.0
    pizza_baking_progress = 0
    pizza_baked = False
    pizza_state = PIZZA_STATE_UNCOOKED

    l3_score = 0
    l3_cutting_score = 0
    l3_mixing_score = 0
    l3_topping_score = 0
    l3_baking_score = 0

    log_message("LEVEL 3 STARTED: Collect Sausage from Storage Area first!")


# =========================
# GAMEPLAY LOGIC (FEATURES 1 & 2)
# =========================
def try_collect_ingredient():
    global score, cutting_unlocked, game_state, collection_score, matching_score
    global has_frozen_patty, has_potato, has_sausage

    best_name, best_dist = None, None
    for name, info in INGREDIENT_POSITIONS.items():
        x, y, z = info["pos"]
        d = distance_between(hero_pos[0], hero_pos[1], x, y)
        if d <= PICKUP_RADIUS and (best_dist is None or d < best_dist):
            best_name, best_dist = name, d

    if not best_name:
        return False

    # --- LEVEL 2 INGREDIENTS (Only active when Level 2 is in progress) ---
    if level2_unlocked and not level3_unlocked and game_state != STATE_LEVEL_COMPLETE:
        if best_name == "Frozen Patty":
            has_frozen_patty = True
            collected_ingredients.add("Frozen Patty")
            game_state = STATE_L2_FRYING
            log_message("Collected Frozen Patty! Carry it to the Stove Area.")
            return True

        if best_name == "Potato":
            has_potato = True
            collected_ingredients.add("Potato")
            game_state = STATE_FRIES_CUTTING
            log_message("Collected Potato! Take it to the Cutting Board.")
            return True

    # --- LEVEL 3 INGREDIENTS (Only active when Level 3 is in progress) ---
    if level3_unlocked or game_state.startswith("PIZZA") or game_state.startswith("SAUSAGE") or game_state in (STATE_L3_COLLECTING_SAUSAGE, STATE_L3_SAUSAGE_CUTTING):
        if best_name == "Sausage":
            has_sausage = True
            collected_ingredients.add("Sausage")
            game_state = STATE_L3_SAUSAGE_CUTTING
            log_message("Collected Sausage! Carry it to the Cutting Board.")
            return True

    # --- LEVEL 1 INGREDIENT COLLECTION (Only active when Level 1 is in progress) ---
    if not level2_unlocked and not level3_unlocked and game_state != STATE_LEVEL_COMPLETE:
        if len(collected_ingredients) >= MAX_INVENTORY_CAP:
            log_message("Inventory Full (3/3 max)! Press 'R' to remove wrong items.")
            return True

        if best_name in collected_ingredients:
            log_message("Already collected %s!" % best_name)
            return True

        collected_ingredients.add(best_name)
        if best_name in REQUIRED_INGREDIENTS:
            collection_score += 1
            score += 1
            log_message("Collected correct %s! (+1 score)" % best_name)

            # Unlock cutting station immediately when all required ingredients are collected!
            correct_collected = set(REQUIRED_INGREDIENTS).intersection(collected_ingredients)
            if len(correct_collected) == len(REQUIRED_INGREDIENTS):
                if not cutting_unlocked:
                    matching_score += 20
                    score += 20
                    cutting_unlocked = True
                    game_state = STATE_CUTTING
                    log_message("ALL REQUIRED INGREDIENTS COLLECTED! +20 pts | Cutting Station UNLOCKED!")
        else:
            collection_score -= 1
            score -= 1
            log_message("Collected wrong %s! (-1 score). Press 'R' to remove wrong item." % best_name)
        return True

    return False


# =========================
# HUD DISPLAY
# =========================
def draw_hud():
    if game_state.startswith("PIZZA") or game_state.startswith("SAUSAGE") or game_state in (STATE_L3_COLLECTING_SAUSAGE, STATE_L3_SAUSAGE_CUTTING, STATE_L3_DOUGH_MAKING, STATE_L3_TOPPING, STATE_L3_BAKING, STATE_L3_COMPLETE):
        cur_level = 3
    elif level2_unlocked or game_state.startswith("BURGER") or game_state.startswith("POTATO") or game_state.startswith("FRIES") or game_state in (STATE_L2_COLLECTING, STATE_L2_FRYING, STATE_L2_PATTY_READY, STATE_L2_ASSEMBLY, STATE_L2_COMPLETE):
        cur_level = 2
    else:
        cur_level = 1

    # ==========================================
    # 1. TOP-LEFT HUD CARD: Status & Actions
    # ==========================================
    draw_ui_panel(10, 595, 410, 195, bg_r=0.06, bg_g=0.09, bg_b=0.14, bg_a=0.92, border_r=0.30, border_g=0.70, border_b=0.65, border_width=2)
    draw_text(20, 765, "LEVEL: %d" % cur_level, 0.3, 1.0, 0.4)
    draw_text(160, 765, "SCORE: %d" % score, 1.0, 0.85, 0.2)
    draw_text(20, 740, "STAGE: %s" % game_state, 0.9, 0.9, 0.9)

    near = nearest_station_within_radius()
    if near:
        label = STATION_DISPLAY_NAMES.get(near, near.upper())
        draw_text(20, 712, "Near Station: %s" % label, 0.4, 0.95, 0.4)

    if level2_unlocked and game_state == STATE_LEVEL_COMPLETE:
        draw_text(20, 680, "PRESS '2' FOR LEVEL 2 (BURGER & FRIES)", 0.3, 1.0, 0.3)
    elif level3_unlocked and game_state == STATE_L2_COMPLETE:
        draw_text(20, 680, "PRESS '3' FOR LEVEL 3 (PIZZA PREP)", 0.3, 1.0, 0.3)

    # --- Cutting Station Instructions ---
    if player_near_station("cutting"):
        if game_state in (STATE_L3_COLLECTING_SAUSAGE, STATE_L3_SAUSAGE_CUTTING) or (level3_unlocked and not sausage_cut_done):
            if not has_sausage:
                draw_text(20, 675, "CUTTING BOARD: Collect Sausage from Storage first!", 1.0, 0.85, 0.2)
            elif sausage_cutting_active:
                draw_text(20, 675, "SAUSAGE CUTTING: Press 'Q' to Cut Sausage", 1.0, 0.85, 0.2)
                draw_text(20, 650, "Sausage Cuts: %d / %d" % (sausage_cut_count, SAUSAGE_CUT_REQUIREMENT), 0.3, 1.0, 0.3)
            else:
                draw_text(20, 675, "SAUSAGE CUTTING: Left Click / E to Begin", 1.0, 0.85, 0.2)
                draw_text(20, 650, "Sausage Cuts: %d / %d" % (sausage_cut_count, SAUSAGE_CUT_REQUIREMENT), 0.3, 1.0, 0.3)
        elif has_potato and not potato_cut_done:
            if potato_cutting_active:
                draw_text(20, 675, "POTATO CUTTING: Press 'Q' to Cut Potato", 1.0, 0.85, 0.2)
                draw_text(20, 650, "Potato Cuts: %d / %d" % (potato_cut_count, POTATO_CUT_REQUIREMENT), 0.3, 1.0, 0.3)
            else:
                draw_text(20, 675, "POTATO CUTTING: Left Click / E to Begin", 1.0, 0.85, 0.2)
                draw_text(20, 650, "Potato Cuts: %d / %d" % (potato_cut_count, POTATO_CUT_REQUIREMENT), 0.3, 1.0, 0.3)
        elif veg_cutting_active:
            draw_text(20, 675, "VEGETABLE CUTTING: Press 'Q' to Cut", 1.0, 0.85, 0.2)
            if veg_cutting_index < len(REQUIRED_INGREDIENTS):
                cur_v = REQUIRED_INGREDIENTS[veg_cutting_index]
                draw_text(20, 650, "Cutting: %s  (%d / %d)" % (cur_v, veg_cut_progress[cur_v], CUTS_PER_VEGETABLE), 0.3, 1.0, 0.3)
        elif cutting_unlocked and not cutting_done:
            draw_text(20, 675, "CUTTING STATION: Left Click / E to Begin Cutting", 1.0, 0.85, 0.2)
        elif cutting_done or potato_cut_done or sausage_cut_done:
            draw_text(20, 675, "CUTTING STATION: Cutting Completed!", 0.3, 1.0, 0.3)
        else:
            draw_text(20, 675, "CUTTING STATION: LOCKED", 1.0, 0.3, 0.3)

    # --- Mixing Station Instructions ---
    if player_near_station("mixing"):
        if game_state == STATE_L3_DOUGH_MAKING:
            draw_text(20, 675, "DOUGH MIXING: Left Click / E to Mix Dough", 1.0, 0.85, 0.2)
            draw_text(20, 650, "Mixing: %d / %d" % (dough_mix_count, DOUGH_MIX_REQUIREMENT), 0.3, 1.0, 0.3)
        elif dough_ready:
            draw_text(20, 675, "MIXING STATION: Dough Ready", 0.3, 1.0, 0.3)

    # --- Plating Station Instructions ---
    if player_near_station("plating"):
        if level2_unlocked and not level3_unlocked and game_state != STATE_LEVEL_COMPLETE:
            if burger_ready and not burger_plated:
                draw_text(20, 675, "PLATING STATION: Left Click / E to Place Burger", 1.0, 0.85, 0.2)
            elif fries_ready and not fries_plated:
                draw_text(20, 675, "PLATING STATION: Left Click / E to Place Fries", 1.0, 0.85, 0.2)
            elif burger_plated and not fries_plated:
                draw_text(20, 675, "PLATING: Burger Plated | Plate French Fries next", 0.3, 1.0, 0.3)
            elif fries_plated and not burger_plated:
                draw_text(20, 675, "PLATING: Fries Plated | Plate Burger next", 0.3, 1.0, 0.3)
            elif burger_plated and fries_plated:
                draw_text(20, 675, "PLATING: Level 2 Complete! Both Plated", 0.3, 1.0, 0.3)
            else:
                draw_text(20, 675, "PLATING: Prepare Burger or Fries first", 1.0, 0.85, 0.2)
        elif not level2_unlocked:
            if prep_oven_unlocked and not plating_done:
                draw_text(20, 675, "PLATING STATION: Left Click / E to Place", 1.0, 0.85, 0.2)
                draw_text(20, 650, "Plate Progress: %d / %d" % (plating_count, PLATING_REQUIREMENT), 0.3, 1.0, 0.3)
            elif plating_done:
                draw_text(20, 675, "PLATING STATION: Plating Completed!", 0.3, 1.0, 0.3)
            else:
                draw_text(20, 675, "PLATING STATION: LOCKED", 1.0, 0.3, 0.3)

    # --- Stove Station Instructions & Timers ---
    if player_near_station("stove"):
        if potato_cut_done and not potato_boiling and not potato_boiled:
            draw_text(20, 675, "STOVE POT: Left Click / E to Boil Potato Strips", 1.0, 0.85, 0.2)
        elif potato_boiling and not potato_boiled:
            elapsed = time.time() - potato_boil_start
            draw_text(20, 675, f"BOILING POTATO: {potato_boil_progress}%", 0.4, 0.9, 1.0)
            draw_text(20, 650, f"Timer: {elapsed:.1f}s / {BOILING_DURATION:.1f}s", 0.9, 0.9, 0.9)
        elif patty_on_stove:
            elapsed = time.time() - patty_frying_start
            if 60 <= patty_progress <= 115:
                draw_text(20, 675, f"PATTY READY! {patty_progress}% (Click/E to Flip & Remove)", 0.3, 1.0, 0.3)
                draw_text(20, 650, f"Timer: {elapsed:.1f}s / {FRYING_DURATION:.1f}s (SWEET SPOT)", 0.3, 1.0, 0.3)
            elif patty_progress > 115:
                draw_text(20, 675, f"PATTY BURNT! {patty_progress}% (Click/E to Clear)", 1.0, 0.3, 0.3)
                draw_text(20, 650, f"Timer: {elapsed:.1f}s — Start over from Storage", 1.0, 0.3, 0.3)
            else:
                draw_text(20, 675, f"PATTY SIZZLING: {patty_progress}% (Flip at 60-115%)", 1.0, 0.85, 0.2)
                draw_text(20, 650, f"Timer: {elapsed:.1f}s / {FRYING_DURATION:.1f}s", 0.9, 0.9, 0.9)
        elif not has_cooked_patty and has_frozen_patty:
            draw_text(20, 675, "STOVE PAN: Left Click / E to Fry Patty", 1.0, 0.85, 0.2)
        elif potato_boiled and not fries_ready:
            draw_text(20, 675, "STOVE / FRYER: Take strips to Deep Fryer", 1.0, 0.85, 0.2)

    # --- Deep Fryer Station Instructions & Live Timers ---
    if player_near_station("fryer"):
        if potato_boiled and not fries_ready:
            if not fries_frying_active:
                draw_text(20, 675, "DEEP FRYER: Left Click / E to Fry Strips", 1.0, 0.85, 0.2)
            else:
                elapsed = time.time() - fries_frying_start
                if 60 <= fries_progress <= 115:
                    draw_text(20, 675, f"FRIES READY! {fries_progress}% (Click/E to Remove)", 0.3, 1.0, 0.3)
                    draw_text(20, 650, f"Timer: {elapsed:.1f}s / {FRIES_FRYING_DURATION:.1f}s", 0.9, 0.9, 0.9)
                elif fries_progress > 115:
                    draw_text(20, 675, f"FRIES BURNT! {fries_progress}% (Click/E to Clear)", 1.0, 0.3, 0.3)
                    draw_text(20, 650, f"Timer: {elapsed:.1f}s", 0.9, 0.9, 0.9)
                else:
                    draw_text(20, 675, f"DEEP FRYER: {fries_progress}%", 1.0, 0.85, 0.2)
                    draw_text(20, 650, f"Timer: {elapsed:.1f}s / {FRIES_FRYING_DURATION:.1f}s (60-115%)", 0.9, 0.9, 0.9)
        elif fries_ready:
            draw_text(20, 675, "DEEP FRYER: Fries Ready! Plate at Plating Station", 0.3, 1.0, 0.3)
        elif not potato_boiled:
            draw_text(20, 675, "DEEP FRYER: Boil Potato Strips in Stove Pot first!", 0.9, 0.9, 0.9)

    # --- Oven Station Instructions ---
    if player_near_station("oven"):
        if game_state == STATE_L3_BAKING or pizza_in_oven:
            if pizza_in_oven:
                if 60 <= pizza_baking_progress <= 115:
                    draw_text(20, 675, f"PIZZA READY! {pizza_baking_progress}% (Click/E to Remove)", 0.3, 1.0, 0.3)
                elif pizza_baking_progress > 115:
                    draw_text(20, 675, f"PIZZA BURNT! {pizza_baking_progress}% (Click/E to Clear)", 1.0, 0.3, 0.3)
                else:
                    draw_text(20, 675, f"PIZZA BAKING: {pizza_baking_progress}%", 1.0, 0.85, 0.2)
            elif pizza_topping_done and not pizza_baked:
                draw_text(20, 675, "OVEN: Left Click / E to Place Pizza Inside", 1.0, 0.85, 0.2)

    # --- Prep Table Instructions ---
    if player_near_station("prep"):
        if game_state == STATE_L2_ASSEMBLY:
            draw_text(20, 675, "BURGER ASSEMBLY: %d / 6" % burger_assembly_step, 1.0, 0.85, 0.2)
            if burger_assembly_step < len(BURGER_STEPS):
                draw_text(20, 650, "Left Click / E to Add: %s" % BURGER_STEPS[burger_assembly_step], 0.3, 1.0, 0.3)
        elif game_state == STATE_L3_TOPPING:
            draw_text(20, 675, "PIZZA TOPPING: %d / 3" % min(3, pizza_topping_step), 1.0, 0.85, 0.2)
            if pizza_topping_step < len(PIZZA_TOPPING_STEPS):
                msg = "Next: Add %s" % PIZZA_TOPPING_STEPS[pizza_topping_step]
                draw_text(20, 650, msg, 0.3, 1.0, 0.3)

    # ==========================================
    # 2. TOP-RIGHT HUD CARD: Goals & Checklists
    # ==========================================
    if veg_cutting_active:
        draw_ui_panel(WINDOW_WIDTH - 290, 560, 280, 230, bg_r=0.06, bg_g=0.09, bg_b=0.14, bg_a=0.92, border_r=0.3, border_g=0.8, border_b=0.9, border_width=2)
        draw_text(WINDOW_WIDTH - 275, 765, "CUTTING BOARD", 1.0, 0.85, 0.2)
        draw_text(WINDOW_WIDTH - 275, 742, "Ingredients to Cut:", 0.9, 0.9, 0.9)
        for i, veg in enumerate(REQUIRED_INGREDIENTS):
            prog = veg_cut_progress[veg]
            done = prog >= CUTS_PER_VEGETABLE
            active_marker = ">" if i == veg_cutting_index and not done else " "
            symbol = "[✓]" if done else "[ ]"
            col = (0.3, 1.0, 0.3) if done else (1.0, 1.0, 1.0)
            draw_text(WINDOW_WIDTH - 275, 715 - i * 22, "%s%s %s (%d/%d)" % (active_marker, symbol, veg, prog, CUTS_PER_VEGETABLE), *col)
        draw_text(WINDOW_WIDTH - 275, 620, "Press 'Q' to cut", 1.0, 0.85, 0.2)

    elif game_state.startswith("PIZZA") or game_state.startswith("SAUSAGE") or game_state in (STATE_L3_COLLECTING_SAUSAGE, STATE_L3_SAUSAGE_CUTTING, STATE_L3_DOUGH_MAKING, STATE_L3_TOPPING, STATE_L3_BAKING, STATE_L3_COMPLETE):
        draw_ui_panel(WINDOW_WIDTH - 290, 440, 280, 350, bg_r=0.06, bg_g=0.09, bg_b=0.14, bg_a=0.92, border_r=0.85, border_g=0.68, border_b=0.28, border_width=2)
        draw_text(WINDOW_WIDTH - 275, 765, "LEVEL 3 PIZZA PREP:", 1.0, 0.85, 0.2)
        s_col = (0.3, 1.0, 0.3) if has_sausage else (1.0, 1.0, 1.0)
        draw_text(WINDOW_WIDTH - 275, 742, "%s 1. Collect Sausage" % ("[✓]" if has_sausage else "[ ]"), *s_col)
        sc_col = (0.3, 1.0, 0.3) if sausage_cut_done else (1.0, 1.0, 1.0)
        draw_text(WINDOW_WIDTH - 275, 720, "%s 2. Cut Sausage (%d/4)" % ("[✓]" if sausage_cut_done else "[ ]", sausage_cut_count), *sc_col)
        m_col = (0.3, 1.0, 0.3) if dough_ready else (1.0, 1.0, 1.0)
        draw_text(WINDOW_WIDTH - 275, 698, "%s 3. Mix Dough (%d/5)" % ("[✓]" if dough_ready else "[ ]", dough_mix_count), *m_col)
        t_col = (0.3, 1.0, 0.3) if pizza_topping_done else (1.0, 1.0, 1.0)
        draw_text(WINDOW_WIDTH - 275, 676, "%s 4. Toppings (%d/3)" % ("[✓]" if pizza_topping_done else "[ ]", min(3, pizza_topping_step)), *t_col)
        b_col = (0.3, 1.0, 0.3) if pizza_baked else (1.0, 1.0, 1.0)
        draw_text(WINDOW_WIDTH - 275, 654, "%s 5. Bake in Oven (%d%%)" % ("[✓]" if pizza_baked else "[ ]", pizza_baking_progress), *b_col)

        draw_text(WINDOW_WIDTH - 275, 615, "PIZZA TOPPINGS:", 1.0, 0.85, 0.2)
        displayed_toppings = [step for step in PIZZA_TOPPING_STEPS if step != "Cut Sausage"]
        for i, step_name in enumerate(displayed_toppings):
            is_p = i < pizza_topping_step
            p_sym = "[✓]" if is_p else "[ ]"
            p_c = (0.3, 1.0, 0.3) if is_p else (1.0, 1.0, 1.0)
            draw_text(WINDOW_WIDTH - 275, 592 - i * 20, "%s %s" % (p_sym, step_name), *p_c)

        draw_text(WINDOW_WIDTH - 275, 465, "Total Score: %d" % score, 0.4, 0.9, 0.4)

    elif game_state.startswith("BURGER") or game_state.startswith("POTATO") or game_state.startswith("FRIES") or game_state in (STATE_L2_COLLECTING, STATE_L2_FRYING, STATE_L2_PATTY_READY, STATE_L2_ASSEMBLY, STATE_L2_COMPLETE):
        draw_ui_panel(WINDOW_WIDTH - 290, 440, 280, 350, bg_r=0.06, bg_g=0.09, bg_b=0.14, bg_a=0.92, border_r=0.85, border_g=0.68, border_b=0.28, border_width=2)
        draw_text(WINDOW_WIDTH - 275, 765, "BURGER INGREDIENTS:", 1.0, 0.85, 0.2)
        draw_text(WINDOW_WIDTH - 275, 742, "[✓] Tomato", 0.3, 1.0, 0.3)
        draw_text(WINDOW_WIDTH - 275, 722, "[✓] Cucumber", 0.3, 1.0, 0.3)
        p_sym = "[✓]" if has_frozen_patty else "[ ]"
        p_col = (0.3, 1.0, 0.3) if has_frozen_patty else (1.0, 1.0, 1.0)
        draw_text(WINDOW_WIDTH - 275, 702, "%s Frozen Patty" % p_sym, *p_col)

        draw_text(WINDOW_WIDTH - 275, 668, "FRENCH FRIES PREP:", 1.0, 0.85, 0.2)
        draw_text(WINDOW_WIDTH - 275, 646, "%s 1. Collect Potato" % ("[✓]" if has_potato else "[ ]"), *(0.3, 1.0, 0.3) if has_potato else (1.0, 1.0, 1.0))
        draw_text(WINDOW_WIDTH - 275, 626, "%s 2. Cut Strips (%d/4)" % ("[✓]" if potato_cut_done else "[ ]", potato_cut_count), *(0.3, 1.0, 0.3) if potato_cut_done else (1.0, 1.0, 1.0))
        draw_text(WINDOW_WIDTH - 275, 606, "%s 3. Boil (%d%%)" % ("[✓]" if potato_boiled else "[ ]", potato_boil_progress), *(0.3, 1.0, 0.3) if potato_boiled else (1.0, 1.0, 1.0))
        draw_text(WINDOW_WIDTH - 275, 586, "%s 4. Deep Fry (%d%%)" % ("[✓]" if fries_ready else "[ ]", 100 if fries_ready else 0), *(0.3, 1.0, 0.3) if fries_ready else (1.0, 1.0, 1.0))

        draw_text(WINDOW_WIDTH - 275, 550, "FINAL PLATING:", 1.0, 0.85, 0.2)
        draw_text(WINDOW_WIDTH - 275, 528, "%s Burger Plated" % ("[✓]" if burger_plated else "[ ]"), *(0.3, 1.0, 0.3) if burger_plated else (1.0, 1.0, 1.0))
        draw_text(WINDOW_WIDTH - 275, 508, "%s Fries Plated" % ("[✓]" if fries_plated else "[ ]"), *(0.3, 1.0, 0.3) if fries_plated else (1.0, 1.0, 1.0))

        draw_text(WINDOW_WIDTH - 275, 465, "Total Score: %d" % score, 0.4, 0.9, 0.4)

    else:
        draw_ui_panel(WINDOW_WIDTH - 290, 595, 280, 195, bg_r=0.06, bg_g=0.09, bg_b=0.14, bg_a=0.92, border_r=0.85, border_g=0.68, border_b=0.28, border_width=2)
        draw_text(WINDOW_WIDTH - 275, 765, "REQUIRED INGREDIENTS:", 1.0, 0.85, 0.2)
        correct_count = 0
        for i, ingr in enumerate(REQUIRED_INGREDIENTS):
            has_it = ingr in collected_ingredients
            if has_it:
                correct_count += 1
            symbol = "[✓]" if has_it else "[ ]"
            col = (0.3, 1.0, 0.3) if has_it else (1.0, 1.0, 1.0)
            draw_text(WINDOW_WIDTH - 275, 738 - i * 24, "%s %s" % (symbol, ingr), *col)

        y_offset = 738 - len(REQUIRED_INGREDIENTS) * 24
        draw_text(WINDOW_WIDTH - 275, y_offset, "Collected: %d / %d" % (correct_count, len(REQUIRED_INGREDIENTS)), 0.9, 0.9, 0.9)
        draw_text(WINDOW_WIDTH - 275, y_offset - 24, "Score: %d" % score, 0.4, 0.9, 0.4)

    # ==========================================
    # 3. FRYING MINI-GAME HUD (Centered Floating Card)
    # ==========================================
    if fries_frying_active:
        elapsed = time.time() - fries_frying_start
        draw_ui_panel((WINDOW_WIDTH - 520) // 2, 490, 520, 240, bg_r=0.07, bg_g=0.10, bg_b=0.15, bg_a=0.96, border_r=1.0, border_g=0.75, border_b=0.2, border_width=2)
        draw_text((WINDOW_WIDTH - 460) // 2, 705, f"DEEP FRYING: {fries_progress}% | Timer: {elapsed:.1f}s / {FRIES_FRYING_DURATION:.1f}s", 1.0, 0.95, 0.2)
        draw_text((WINDOW_WIDTH - 460) // 2, 680, "MATCH ARROWS (WASD / ARROWS / MOUSE CLICK)", 0.9, 0.9, 0.9)
        
        if fries_target_index < len(FRIES_TARGET_SEQUENCE):
            cur_t = FRIES_TARGET_SEQUENCE[fries_target_index]
            draw_text((WINDOW_WIDTH - 200) // 2, 650, f"TARGET:  {cur_t}", 0.3, 1.0, 0.3)
        else:
            draw_text((WINDOW_WIDTH - 380) // 2, 650, "DIRECTIONS MATCHED! (SIZZLING)", 1.0, 0.85, 0.2)

        draw_text((WINDOW_WIDTH - 320) // 2, 620, f"Progress: {fries_target_index} / 6  |  Quality: {fries_quality}%", 0.9, 0.9, 0.9)
        draw_text((WINDOW_WIDTH - 20) // 2, 585, "^", 1.0, 1.0, 1.0)
        draw_text((WINDOW_WIDTH - 120) // 2, 565, "<   [FRYER]   >", 1.0, 1.0, 1.0)
        draw_text((WINDOW_WIDTH - 20) // 2, 545, "v", 1.0, 1.0, 1.0)

        # Action prompt
        if 60 <= fries_progress <= 115:
            draw_text((WINDOW_WIDTH - 480) // 2, 510, "[ READY! PRESS 'E' / SPACE TO LIFT BASKET (+35 PTS) ]", 0.3, 1.0, 0.3)
        elif fries_progress > 115:
            draw_text((WINDOW_WIDTH - 480) // 2, 510, "[ BURNT! PRESS 'E' / SPACE TO CLEAR (-20 PTS) ]", 1.0, 0.3, 0.3)
        else:
            draw_text((WINDOW_WIDTH - 480) // 2, 510, "[ SIZZLING IN OIL: PRESS 'E' / SPACE AT 60-115% ]", 1.0, 0.85, 0.2)

    # ==========================================
    # 4. BOTTOM NOTIFICATION & LOG TICKER BAR
    # ==========================================
    draw_ui_panel(10, 8, WINDOW_WIDTH - 20, 95, bg_r=0.05, bg_g=0.07, bg_b=0.10, bg_a=0.92, border_r=0.25, border_g=0.45, border_b=0.45, border_width=1)
    draw_text(22, 78, "ACTIVITY & NOTIFICATION LOG", 0.4, 0.75, 0.9)
    y_log = 56
    for msg in message_log[-3:]:
        draw_text(22, y_log, msg, 0.92, 0.92, 0.92)
        y_log -= 22

    # ==========================================
    # 5. LEVEL 1 COMPLETION MODAL DIALOG
    # ==========================================
    if game_state == STATE_LEVEL_COMPLETE:
        # Fullscreen dimming backdrop
        draw_ui_panel(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 0.0, 0.0, 0.0, 0.75, border_width=0)

        # Centered luxury modal card
        card_w, card_h = 580, 420
        cx = (WINDOW_WIDTH - card_w) // 2
        cy = (WINDOW_HEIGHT - card_h) // 2
        draw_ui_panel(cx, cy, card_w, card_h, bg_r=0.07, bg_g=0.10, bg_b=0.15, bg_a=0.98, border_r=1.0, border_g=0.85, border_b=0.25, border_width=3)

        # Top title banner
        draw_ui_panel(cx + 15, cy + card_h - 65, card_w - 30, 50, bg_r=0.10, bg_g=0.30, bg_b=0.20, bg_a=1.0, border_r=0.3, border_g=1.0, border_b=0.3, border_width=1)
        draw_text(cx + 90, cy + card_h - 48, "DISH COMPLETE - LEVEL 1 CLEAR!", 0.3, 1.0, 0.3)

        # Score Breakdown Rows
        draw_text(cx + 40, cy + 285, "Ingredient Collection Score:   %d pts" % collection_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 250, "Matching Score:                %d pts" % matching_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 215, "Cutting Score:                 %d pts" % cutting_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 180, "Cooking / Plating Score:       %d pts" % cooking_score, 0.9, 0.9, 0.9)

        # Total score badge
        draw_ui_panel(cx + 30, cy + 125, card_w - 60, 36, bg_r=0.10, bg_g=0.15, bg_b=0.22, bg_a=1.0, border_r=0.85, border_g=0.68, border_b=0.28, border_width=1)
        draw_text(cx + 45, cy + 134, "FINAL LEVEL 1 SCORE:           %d PTS" % score, 1.0, 0.9, 0.2)

        # Call-to-action button
        draw_ui_panel(cx + 30, cy + 40, card_w - 60, 55, bg_r=0.15, bg_g=0.45, bg_b=0.22, bg_a=1.0, border_r=0.3, border_g=1.0, border_b=0.3, border_width=2)
        draw_text(cx + 70, cy + 58, "PRESS '2' TO START LEVEL 2: BURGER & FRIES!", 1.0, 1.0, 1.0)

    # ==========================================
    # 6. LEVEL 2 COMPLETION MODAL DIALOG
    # ==========================================
    if game_state == STATE_L2_COMPLETE:
        # Fullscreen dimming backdrop
        draw_ui_panel(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 0.0, 0.0, 0.0, 0.75, border_width=0)

        card_w, card_h = 580, 420
        cx = (WINDOW_WIDTH - card_w) // 2
        cy = (WINDOW_HEIGHT - card_h) // 2
        draw_ui_panel(cx, cy, card_w, card_h, bg_r=0.07, bg_g=0.10, bg_b=0.15, bg_a=0.98, border_r=1.0, border_g=0.85, border_b=0.25, border_width=3)

        # Top title banner
        draw_ui_panel(cx + 15, cy + card_h - 65, card_w - 30, 50, bg_r=0.10, bg_g=0.30, bg_b=0.20, bg_a=1.0, border_r=0.3, border_g=1.0, border_b=0.3, border_width=1)
        draw_text(cx + 90, cy + card_h - 48, "LEVEL 2 COMPLETE: BURGER & FRIES!", 0.3, 1.0, 0.3)

        # Score Breakdown Rows
        draw_text(cx + 40, cy + 285, "Burger Patty Frying Score:     %d pts" % l2_frying_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 250, "Burger Assembly Score:         %d pts" % l2_assembly_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 215, "French Fries Preparation:      %d pts" % l2_fries_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 180, "Level 2 Completion Bonus:      +30 pts", 0.3, 1.0, 0.3)

        # Total score badge
        draw_ui_panel(cx + 30, cy + 125, card_w - 60, 36, bg_r=0.10, bg_g=0.15, bg_b=0.22, bg_a=1.0, border_r=0.85, border_g=0.68, border_b=0.28, border_width=1)
        draw_text(cx + 45, cy + 134, "TOTAL GAME SCORE:              %d PTS" % score, 1.0, 0.9, 0.2)

        # Call-to-action button
        draw_ui_panel(cx + 30, cy + 40, card_w - 60, 55, bg_r=0.15, bg_g=0.45, bg_b=0.22, bg_a=1.0, border_r=0.3, border_g=1.0, border_b=0.3, border_width=2)
        draw_text(cx + 70, cy + 58, "PRESS '3' TO START LEVEL 3: GOURMET PIZZA!", 1.0, 1.0, 1.0)

    # ==========================================
    # 7. LEVEL 3 VICTORY MODAL DIALOG
    # ==========================================
    if game_state == STATE_L3_COMPLETE:
        # Fullscreen dimming backdrop
        draw_ui_panel(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 0.0, 0.0, 0.0, 0.80, border_width=0)

        card_w, card_h = 580, 430
        cx = (WINDOW_WIDTH - card_w) // 2
        cy = (WINDOW_HEIGHT - card_h) // 2
        draw_ui_panel(cx, cy, card_w, card_h, bg_r=0.07, bg_g=0.10, bg_b=0.15, bg_a=0.98, border_r=1.0, border_g=0.85, border_b=0.25, border_width=3)

        # Top title banner
        draw_ui_panel(cx + 15, cy + card_h - 65, card_w - 30, 50, bg_r=0.10, bg_g=0.30, bg_b=0.20, bg_a=1.0, border_r=0.3, border_g=1.0, border_b=0.3, border_width=1)
        draw_text(cx + 60, cy + card_h - 48, "GOURMET PIZZA COMPLETE — GAME VICTORY!", 0.3, 1.0, 0.3)

        # Score Breakdown Rows
        draw_text(cx + 40, cy + 295, "Sausage Cutting Score:         %d pts" % l3_cutting_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 265, "Dough Kneading Score:          %d pts" % l3_mixing_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 235, "Pizza Toppings Score:          %d pts" % l3_topping_score, 0.9, 0.9, 0.9)
        draw_text(cx + 40, cy + 205, "Oven Baking Score:             %d pts" % l3_baking_score, 0.9, 0.9, 0.9)

        # Total score badge
        draw_ui_panel(cx + 30, cy + 135, card_w - 60, 36, bg_r=0.10, bg_g=0.15, bg_b=0.22, bg_a=1.0, border_r=0.85, border_g=0.68, border_b=0.28, border_width=1)
        draw_text(cx + 45, cy + 144, "FINAL MASTER CHEF SCORE:       %d PTS" % score, 1.0, 0.9, 0.2)

        # Call-to-action button
        draw_ui_panel(cx + 30, cy + 40, card_w - 60, 55, bg_r=0.15, bg_g=0.45, bg_b=0.22, bg_a=1.0, border_r=0.3, border_g=1.0, border_b=0.3, border_width=2)
        draw_text(cx + 80, cy + 58, "ALL LEVELS CLEARED! PRESS '1' TO REPLAY", 1.0, 1.0, 1.0)


# =========================
# INPUT LISTENERS & ACTIONS
# =========================
def handle_fries_direction_input(direction):
    """Process directional input (arrows or WASD or mouse clicks) in frying mini-game."""
    global fries_target_index, fries_quality, fries_frying_active, fries_ready
    global hero_pov, game_state, l2_fries_score, score
    global potato_boiled, has_potato, potato_cut_done, potato_cut_count
    if not fries_frying_active or fries_ready:
        return
    if fries_target_index >= len(FRIES_TARGET_SEQUENCE):
        log_message("All directions completed! Press 'E' / Space to lift basket at 60-115% sweet spot.")
        return

    target_dir = FRIES_TARGET_SEQUENCE[fries_target_index]
    if direction == target_dir:
        fries_target_index += 1
        score += 5
        log_message("CORRECT DIRECTION %s! (%d / 6) (+5 pts)" % (direction, fries_target_index))
        if fries_target_index >= len(FRIES_TARGET_SEQUENCE):
            if 60 <= fries_progress <= 115:
                fries_frying_active = False
                fries_ready = True
                hero_pov = False
                if has_cooked_patty:
                    game_state = STATE_L2_ASSEMBLY
                    log_message(f"CRISPY FRENCH FRIES READY ({fries_progress}%)! (+35 pts). Move to Prep Table for Burger Assembly.")
                else:
                    game_state = STATE_FRIES_READY
                    log_message(f"CRISPY FRENCH FRIES READY ({fries_progress}%)! (+35 pts). Now prepare the Patty.")
                l2_fries_score = 35
                score += 35
            else:
                log_message("All 6 directions matched! Frying sizzling... Press 'E' / Space at 60-115% to lift basket!")
    else:
        fries_quality = max(0, fries_quality - 15)
        log_message("WRONG DIRECTION! Input %s, Target was %s (-15%% Quality, current: %d%%)" % (direction, target_dir, fries_quality))
        if fries_quality <= 0:
            fries_frying_active = False
            hero_pov = False
            potato_boiled = False
            has_potato = False
            potato_cut_done = False
            potato_cut_count = 0
            collected_ingredients.discard("Potato")
            score = max(0, score - 20)
            log_message("Fries Burnt! Quality dropped to 0% (-20 pts). Collect a new Potato from Storage to retry frying.")


def keyboardListener(key, x, y):
    global hero_pos, angle, hero_pov
    global veg_cutting_active, veg_cutting_index, veg_cut_progress
    global potato_cutting_active, potato_cut_count, potato_cut_done, has_potato
    global sausage_cutting_active, sausage_cut_count, sausage_cut_done, has_sausage, l3_cutting_score
    global cut_count, cutting_done, prep_oven_unlocked, game_state, knife_anim_start
    global cutting_score, score

    k = key.lower() if isinstance(key, bytes) else key

    # Direction handling in Frying Mini-Game
    if fries_frying_active and k in (b'w', b's', b'a', b'd'):
        if k == b'w':
            handle_fries_direction_input('↑')
        elif k == b's':
            handle_fries_direction_input('↓')
        elif k == b'a':
            handle_fries_direction_input('←')
        elif k == b'd':
            handle_fries_direction_input('→')
        glutPostRedisplay()
        return

    if k == b'w':
        rad = math.radians(angle)
        hero_pos[0] += PLAYER_SPEED * math.sin(rad)
        hero_pos[1] -= PLAYER_SPEED * math.cos(rad)
        clamp_player_position()

    elif k == b's':
        rad = math.radians(angle)
        hero_pos[0] -= PLAYER_SPEED * math.sin(rad)
        hero_pos[1] += PLAYER_SPEED * math.cos(rad)
        clamp_player_position()

    elif k == b'd':
        angle = (angle - TURN_SPEED) % 360

    elif k == b'a':
        angle = (angle + TURN_SPEED) % 360

    elif k == b'e' or k == b' ':
        # Universal interact key: pick up ingredients, interact with stations
        perform_interact_action()

    elif k == b'1':
        # Reset / Restart Game
        reset_game()

    elif k == b'2':
        # Start Level 2 only once, after Level 1 is complete.
        if level2_unlocked and game_state == STATE_LEVEL_COMPLETE:
            start_level_2()
        elif not level2_unlocked:
            log_message("Level 2 is locked! Complete Level 1 first.")

    elif k == b'3':
        # Start Level 3 only after Level 2 is complete.
        if level3_unlocked and game_state == STATE_L2_COMPLETE:
            start_level_3()
        elif not level3_unlocked:
            log_message("Level 3 is locked! Complete Level 2 first.")

    elif k == b'r':
        if not level2_unlocked:
            wrong_items = [ing for ing in collected_ingredients if ing not in REQUIRED_INGREDIENTS]
        else:
            wrong_items = [ing for ing in collected_ingredients if ing in INCORRECT_INGREDIENTS]

        if wrong_items:
            for ing in wrong_items:
                collected_ingredients.remove(ing)
            log_message("Removed wrong items (%s). Collect correct ones!" % ", ".join(wrong_items))
        else:
            log_message("No wrong items in inventory to remove.")

    elif k == b'f':
        # Toggle camera to the chef's first-person point of view.
        hero_pov = not hero_pov
        log_message("Camera: " + ("CHEF POV (First Person)" if hero_pov else "THIRD PERSON"))

    elif k == b'q':
        # One cut per 'Q' key press while the locked cutting-board camera view is active across Level 1, 2, and 3.
        if veg_cutting_active and cutting_unlocked and not cutting_done:
            if veg_cutting_index < len(REQUIRED_INGREDIENTS):
                current_veg = REQUIRED_INGREDIENTS[veg_cutting_index]
                veg_cut_progress[current_veg] += 1
                knife_anim_start = time.time()
                cut_count += 1
                cutting_score += 5
                score += 5
                log_message("Cut %s %d/%d! (+5 pts)" % (current_veg, veg_cut_progress[current_veg], CUTS_PER_VEGETABLE))

                if veg_cut_progress[current_veg] >= CUTS_PER_VEGETABLE:
                    veg_cutting_index += 1
                    if veg_cutting_index >= len(REQUIRED_INGREDIENTS):
                        # All vegetables fully chopped: unlock next stage and restore camera.
                        cutting_done = True
                        prep_oven_unlocked = True
                        game_state = STATE_COOKING
                        cutting_score += 20
                        score += 20
                        veg_cutting_active = False
                        hero_pov = False
                        log_message("ALL VEGETABLES CHOPPED! +20 pts | Camera restored to normal view!")
                    else:
                        log_message("Move on: now cutting %s" % REQUIRED_INGREDIENTS[veg_cutting_index])
        elif potato_cutting_active and has_potato and not potato_cut_done:
            potato_cut_count += 1
            knife_anim_start = time.time()
            score += 5
            log_message("Cut Potato %d / %d completed! (+5 pts)" % (potato_cut_count, POTATO_CUT_REQUIREMENT))
            if potato_cut_count >= POTATO_CUT_REQUIREMENT:
                potato_cut_done = True
                game_state = STATE_FRIES_BOILING
                score += 15
                potato_cutting_active = False
                hero_pov = False
                log_message("POTATO CUT INTO STRIPS! +15 bonus pts | Take strips to Stove to Boil!")
        elif sausage_cutting_active and has_sausage and not sausage_cut_done:
            sausage_cut_count += 1
            knife_anim_start = time.time()
            score += 5
            log_message("Cut Sausage %d / %d completed! (+5 pts)" % (sausage_cut_count, SAUSAGE_CUT_REQUIREMENT))
            if sausage_cut_count >= SAUSAGE_CUT_REQUIREMENT:
                sausage_cut_done = True
                game_state = STATE_L3_DOUGH_MAKING
                l3_cutting_score = 20
                score += 20
                sausage_cutting_active = False
                hero_pov = False
                log_message("SAUSAGE CHOPPED! +20 pts | Walk to Mixing Station to make dough.")
        else:
            log_message("Nothing to cut right now.")

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global camera_pos
    yaw, height, distance = camera_pos

    if fries_frying_active:
        if key == GLUT_KEY_UP:
            handle_fries_direction_input('↑')
        elif key == GLUT_KEY_DOWN:
            handle_fries_direction_input('↓')
        elif key == GLUT_KEY_LEFT:
            handle_fries_direction_input('←')
        elif key == GLUT_KEY_RIGHT:
            handle_fries_direction_input('→')
        glutPostRedisplay()
        return

    if key == GLUT_KEY_UP:
        height = min(height + CAMERA_HEIGHT_STEP, CAMERA_HEIGHT_MAX)
    elif key == GLUT_KEY_DOWN:
        height = max(height - CAMERA_HEIGHT_STEP, CAMERA_HEIGHT_MIN)
    elif key == GLUT_KEY_LEFT:
        yaw = (yaw - 8) % 360
    elif key == GLUT_KEY_RIGHT:
        yaw = (yaw + 8) % 360

    camera_pos = [yaw, height, distance]
    glutPostRedisplay()


def perform_interact_action(x=500, y=400):
    """Universal interaction logic: picks up ingredients or operates nearby stations."""
    global hero_pov, score, cut_count, cutting_done, prep_oven_unlocked, game_state, knife_anim_start
    global plating_count, plating_done, level2_unlocked, level3_unlocked
    global cutting_score, cooking_score
    global veg_cutting_active, veg_cutting_index, veg_cut_progress
    global potato_cutting_active, sausage_cutting_active
    global has_frozen_patty, patty_on_stove, patty_frying_start, patty_progress, patty_state
    global has_cooked_patty, burger_assembly_step, burger_ingredients_placed, burger_ready, burger_plated
    global l2_score, l2_frying_score, l2_assembly_score
    global has_potato, potato_cut_count, potato_cut_done, potato_boiling, potato_boil_start
    global potato_boil_progress, potato_boiled, fries_frying_active, fries_target_index
    global fries_quality, fries_ready, fries_plated, l2_fries_score
    global sausage_cut_count, sausage_cut_done, dough_mix_count, dough_ready
    global pizza_topping_step, pizza_topping_done, pizza_in_oven, pizza_baking_start
    global pizza_baking_progress, pizza_baked, pizza_state
    global l3_score, l3_cutting_score, l3_mixing_score, l3_topping_score, l3_baking_score

    # 1. Try collecting nearby 3D ingredient first
    if not try_collect_ingredient():
        # 2. Check if near Cutting Station
        if player_near_station("cutting"):
            if game_state in (STATE_L3_COLLECTING_SAUSAGE, STATE_L3_SAUSAGE_CUTTING) or (level3_unlocked and not sausage_cut_done):
                if not has_sausage:
                    log_message("Collect Sausage from Storage Area first!")
                else:
                    if not sausage_cutting_active:
                        sausage_cutting_active = True
                        hero_pov = True
                        log_message("Entered Cutting View! Press 'Q' to cut Sausage (%d cuts)." % SAUSAGE_CUT_REQUIREMENT)
                    else:
                        log_message("Already cutting! Press 'Q' to continue cutting.")
            elif has_potato and not potato_cut_done:
                if not potato_cutting_active:
                    potato_cutting_active = True
                    hero_pov = True
                    log_message("Entered Cutting View! Press 'Q' to cut Potato into strips (%d cuts)." % POTATO_CUT_REQUIREMENT)
                else:
                    log_message("Already cutting! Press 'Q' to continue cutting.")
            elif cutting_unlocked and not cutting_done:
                if not veg_cutting_active:
                    veg_cutting_active = True
                    veg_cutting_index = 0
                    for k in veg_cut_progress:
                        veg_cut_progress[k] = 0
                    hero_pov = True
                    log_message("Entered Cutting View! Press 'Q' to cut each vegetable (3 cuts each).")
                else:
                    log_message("Already cutting! Press 'Q' to continue cutting.")
            elif cutting_done or potato_cut_done or sausage_cut_done:
                log_message("Cutting complete! Move to next station.")
            else:
                log_message("Cutting Station is LOCKED! Collect required ingredients first.")

        # 3. Check if near Mixing Station (Level 3 Dough Mixing)
        elif player_near_station("mixing") and game_state == STATE_L3_DOUGH_MAKING:
            dough_mix_count += 1
            score += 5
            log_message("Mixed Dough %d / %d completed! (+5 pts)" % (dough_mix_count, DOUGH_MIX_REQUIREMENT))
            if dough_mix_count >= DOUGH_MIX_REQUIREMENT:
                dough_ready = True
                game_state = STATE_L3_TOPPING
                l3_mixing_score = 25
                score += 25
                log_message("PIZZA DOUGH READY! +25 pts | Carry dough to Prep Table for Toppings.")

        # 4. Check if near Plating Station
        elif player_near_station("plating"):
            if level2_unlocked and not level3_unlocked and game_state != STATE_LEVEL_COMPLETE:
                if burger_ready and not burger_plated:
                    burger_plated = True
                    score += 15
                    log_message("Placed Completed Burger on Plate! (+15 pts)")
                    if burger_plated and fries_plated:
                        game_state = STATE_L2_COMPLETE
                        level3_unlocked = True
                        l2_score = l2_frying_score + l2_assembly_score + l2_fries_score + 30
                        score += 30
                        log_message("LEVEL 2 COMPLETE! Burger & Fries Plated (+30 pts) | Press '3' for Level 3.")
                    else:
                        log_message("Burger Plated! Now prepare and plate French Fries to complete Level 2.")
                elif fries_ready and not fries_plated:
                    fries_plated = True
                    score += 15
                    log_message("Placed French Fries on Plate! (+15 pts)")
                    if burger_plated and fries_plated:
                        game_state = STATE_L2_COMPLETE
                        level3_unlocked = True
                        l2_score = l2_frying_score + l2_assembly_score + l2_fries_score + 30
                        score += 30
                        log_message("LEVEL 2 COMPLETE! Burger & Fries Plated (+30 pts) | Press '3' for Level 3.")
                    else:
                        log_message("French Fries Plated! Now prepare and plate Burger to complete Level 2.")
                elif burger_plated and fries_plated:
                    log_message("LEVEL 2 COMPLETE! Press '3' to start Level 3.")
                elif burger_plated and not fries_plated:
                    log_message("Burger already plated! Prepare & plate French Fries next.")
                elif fries_plated and not burger_plated:
                    log_message("French Fries already plated! Prepare & plate Burger next.")
                else:
                    log_message("Prepare Burger or French Fries first before plating!")

            elif not level2_unlocked:
                if prep_oven_unlocked and not plating_done:
                    plating_count += 1
                    cooking_score += 5
                    score += 5
                    log_message("Placed ingredient %d / %d onto plate! (+5 pts)" % (plating_count, PLATING_REQUIREMENT))
                    if plating_count >= PLATING_REQUIREMENT:
                        plating_done = True
                        level2_unlocked = True
                        cooking_score += 20
                        score += 20
                        game_state = STATE_LEVEL_COMPLETE
                        log_message("DISH COMPLETE! Level 2 UNLOCKED! Press '2' to start Level 2.")
                elif plating_done:
                    log_message("DISH COMPLETE! Level 1 Clear. Press '2' to start Level 2.")
                else:
                    log_message("Plating Station is LOCKED!")

        # 5. Check if near Stove Station or Fryer Station (Patty Frying, Potato Boiling, & Fries Deep Frying)
        elif player_near_station("stove") or player_near_station("fryer"):
            if player_near_station("stove") and potato_cut_done and not potato_boiling and not potato_boiled:
                potato_boiling = True
                potato_boil_start = time.time()
                potato_boil_progress = 0
                game_state = STATE_FRIES_BOILING
                hero_pov = True
                log_message("Placed Potato Strips in Cooking Pot! Boiling started (6.0s timer)...")

            elif potato_boiled and not fries_ready:
                if not fries_frying_active:
                    fries_frying_active = True
                    fries_frying_start = time.time()
                    fries_progress = 0
                    fries_target_index = 0
                    fries_quality = 100
                    game_state = STATE_FRIES_FRYING
                    hero_pov = True
                    log_message(f"Lowered Strips into Deep Fryer! Frying started ({FRIES_FRYING_DURATION:.0f}s timer). Match directions & remove at 60-115%!")
                else:
                    if fries_progress < 60:
                        score = max(0, score - 10)
                        log_message(f"French Fries Undercooked ({fries_progress}%)! (-10 pts penalty). Keep frying until golden!")
                    elif 60 <= fries_progress <= 115:
                        fries_frying_active = False
                        fries_ready = True
                        hero_pov = False
                        l2_fries_score = 35
                        score += 35
                        if has_cooked_patty:
                            game_state = STATE_L2_ASSEMBLY
                            log_message(f"CRISPY FRENCH FRIES READY ({fries_progress}%)! (+35 pts). Move to Prep Table for Burger Assembly.")
                        else:
                            game_state = STATE_FRIES_READY
                            log_message(f"CRISPY FRENCH FRIES READY ({fries_progress}%)! (+35 pts). Now prepare the Patty.")
                    elif fries_progress > 115:
                        fries_frying_active = False
                        hero_pov = False
                        potato_boiled = False
                        has_potato = False
                        potato_cut_done = False
                        potato_cut_count = 0
                        collected_ingredients.discard("Potato")
                        score = max(0, score - 20)
                        log_message(f"French Fries BURNT ({fries_progress}%)! (-20 pts penalty). Collect a new Potato from Storage to try again.")

            elif not patty_on_stove and has_frozen_patty and not has_cooked_patty and player_near_station("stove"):
                patty_on_stove = True
                patty_state = PATTY_STATE_FRYING
                patty_frying_start = time.time()
                patty_progress = 0
                hero_pov = True
                log_message("Placed Frozen Patty on Stove! Frying started (8.0s timer)...")
            elif patty_on_stove:
                if patty_progress < 60:
                    patty_on_stove = False
                    patty_state = PATTY_STATE_FROZEN
                    hero_pov = False
                    score = max(0, score - 10)
                    log_message("Patty Undercooked (%d%%)! (-10 pts penalty). Place back on stove." % patty_progress)
                elif 60 <= patty_progress <= 115 or patty_state == PATTY_STATE_COOKED:
                    patty_on_stove = False
                    has_cooked_patty = True
                    patty_state = PATTY_STATE_COOKED
                    hero_pov = False
                    l2_frying_score = 25
                    score += 25
                    game_state = STATE_L2_ASSEMBLY
                    log_message("PATTY READY! (+25 pts). Carry cooked patty to Prep Table for Burger Assembly!")
                elif patty_progress > 115 or patty_state == PATTY_STATE_BURNT:
                    patty_on_stove = False
                    patty_state = PATTY_STATE_BURNT
                    hero_pov = False
                    has_frozen_patty = False
                    collected_ingredients.discard("Frozen Patty")
                    score = max(0, score - 20)
                    log_message("Patty BURNT (%d%%)! (-20 pts penalty). Collect a new Frozen Patty from Storage to try again." % patty_progress)
            elif has_cooked_patty:
                log_message("Patty already cooked! Move to Prep Table for Burger Assembly.")
            else:
                log_message("Collect a Frozen Patty or Potato from Storage Area first.")

        # 6. Check if near Oven Station (Level 3 Pizza Baking)
        elif player_near_station("oven") and (game_state == STATE_L3_BAKING or pizza_in_oven):
            if not pizza_in_oven and pizza_topping_done and not pizza_baked:
                pizza_in_oven = True
                pizza_state = PIZZA_STATE_BAKING
                pizza_baking_start = time.time()
                pizza_baking_progress = 0
                log_message("Placed Raw Pizza in Oven! Baking started...")
            elif pizza_in_oven:
                if pizza_baking_progress < 60:
                    pizza_in_oven = False
                    pizza_state = PIZZA_STATE_UNCOOKED
                    score = max(0, score - 10)
                    log_message("Pizza Undercooked (%d%%)! (-10 pts penalty). Place back in oven." % pizza_baking_progress)
                elif 60 <= pizza_baking_progress <= 115 or pizza_state == PIZZA_STATE_COOKED:
                    pizza_in_oven = False
                    pizza_baked = True
                    pizza_state = PIZZA_STATE_COOKED
                    game_state = STATE_L3_COMPLETE
                    l3_baking_score = 30
                    l3_score = l3_cutting_score + l3_mixing_score + l3_topping_score + l3_baking_score
                    score += 30
                    log_message("PIZZA READY! - PIZZA COMPLETE! (+30 bonus pts)")
                elif pizza_baking_progress > 115 or pizza_state == PIZZA_STATE_BURNT:
                    pizza_in_oven = False
                    pizza_state = PIZZA_STATE_BURNT
                    pizza_topping_done = False
                    pizza_topping_step = 0
                    dough_ready = False
                    dough_mix_count = 0
                    has_sausage = False
                    sausage_cut_done = False
                    sausage_cut_count = 0
                    collected_ingredients.discard("Sausage")
                    score = max(0, score - 20)
                    game_state = STATE_L3_COLLECTING_SAUSAGE
                    log_message("Pizza BURNT (%d%%)! (-20 pts penalty). Start over from Sausage Collection!" % pizza_baking_progress)

        # 7. Check if near Prep Table (Level 2 Burger Assembly & Level 3 Pizza Topping)
        elif player_near_station("prep"):
            if level3_unlocked or game_state.startswith("PIZZA") or game_state in (STATE_L3_COLLECTING_SAUSAGE, STATE_L3_SAUSAGE_CUTTING, STATE_L3_DOUGH_MAKING, STATE_L3_TOPPING):
                if game_state == STATE_L3_TOPPING or (dough_ready and not pizza_topping_done):
                    if pizza_topping_step == 0:
                        pizza_topping_step = 1
                        score += 10
                        log_message("Applied Tomato Sauce! (+10 pts)")
                    elif pizza_topping_step == 1:
                        pizza_topping_step = 2
                        score += 10
                        log_message("Applied Cheese! ALIGN THE CHEESE! (+10 pts)")
                    elif pizza_topping_step == 2:
                        pizza_topping_step = 3
                        pizza_topping_done = True
                        game_state = STATE_L3_BAKING
                        l3_topping_score = 35
                        score += 35
                        log_message("Added Cut Sausage! PIZZA PREPARED! (+35 pts) | Carry to Oven to Bake!")
                    elif pizza_topping_done:
                        log_message("Pizza Toppings completed! Carry pizza to Oven Station.")
                else:
                    log_message("Mix the Pizza Dough at Mixing Station first!")

            elif game_state == STATE_L2_ASSEMBLY or (level2_unlocked and not level3_unlocked and has_cooked_patty):
                if not has_cooked_patty:
                    log_message("Fry the Frozen Patty at the Stove Area first!")
                elif burger_assembly_step < len(BURGER_STEPS):
                    next_item = BURGER_STEPS[burger_assembly_step]
                    burger_ingredients_placed.append(next_item)
                    burger_assembly_step += 1
                    l2_assembly_score += 10
                    score += 10
                    log_message("Placed %s (%d / 6)! (+10 pts)" % (next_item, burger_assembly_step))
                    if burger_assembly_step >= len(BURGER_STEPS):
                        burger_ready = True
                        l2_assembly_score = 30
                        log_message("BURGER READY! Carry completed burger to Plating Station!")
                elif burger_ready:
                    log_message("BURGER READY! Take completed burger to Plating Station.")

        else:
            near = nearest_station_within_radius()
            if near:
                log_message("Near %s. Move to target station." % near.capitalize())


def mouseListener(button, state, x, y):
    global hero_pov

    if state != GLUT_DOWN:
        return

    if button == GLUT_RIGHT_BUTTON:
        hero_pov = not hero_pov
        log_message("Camera: " + ("FIRST PERSON" if hero_pov else "THIRD PERSON"))

    elif button == GLUT_LEFT_BUTTON:
        if fries_frying_active:
            dx = x - (WINDOW_WIDTH // 2)
            dy = y - (WINDOW_HEIGHT // 2)
            if abs(dx) > abs(dy):
                clicked_dir = '→' if dx > 0 else '←'
            else:
                clicked_dir = '↓' if dy > 0 else '↑'
            handle_fries_direction_input(clicked_dir)
        else:
            perform_interact_action(x, y)

    glutPostRedisplay()


# =========================
# GAME LOOP & CAMERA SETUP
# =========================
def idle():
    global last_time, patty_progress, patty_state, hero_pov
    global potato_boiling, potato_boil_start, potato_boil_progress, potato_boiled, score
    global fries_frying_active, fries_frying_start, fries_progress, fries_ready
    global pizza_in_oven, pizza_baking_start, pizza_baking_progress, pizza_state
    now = time.time()
    last_time = now

    # Continuous patty frying progress logic (without freezing)
    if patty_on_stove and not has_cooked_patty:
        elapsed = now - patty_frying_start
        patty_progress = min(150, int((elapsed / FRYING_DURATION) * 100))
        if patty_progress > 115:
            patty_state = PATTY_STATE_BURNT
        elif patty_progress >= 60:
            patty_state = PATTY_STATE_COOKED
        else:
            patty_state = PATTY_STATE_FRYING

    # Continuous french fries deep frying progress timer
    if fries_frying_active and not fries_ready:
        elapsed = now - fries_frying_start
        fries_progress = min(150, int((elapsed / FRIES_FRYING_DURATION) * 100))

    # Continuous boiling progress logic (without glutTimerFunc)
    if potato_boiling and not potato_boiled:
        elapsed = now - potato_boil_start
        potato_boil_progress = min(100, int((elapsed / BOILING_DURATION) * 100))
        if potato_boil_progress >= 100:
            potato_boiling = False
            potato_boiled = True
            hero_pov = False
            score += 20
            log_message("BOILED POTATO STRIPS (+20 pts)! Take strips to Deep Fryer.")

    # Continuous pizza baking progress logic (without freezing)
    if pizza_in_oven and not pizza_baked:
        elapsed = now - pizza_baking_start
        pizza_baking_progress = min(150, int((elapsed / PIZZA_BAKING_DURATION) * 100))
        if pizza_baking_progress > 115:
            pizza_state = PIZZA_STATE_BURNT
        elif pizza_baking_progress >= 60:
            pizza_state = PIZZA_STATE_COOKED
        else:
            pizza_state = PIZZA_STATE_BAKING

    glutPostRedisplay()


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, float(WINDOW_WIDTH) / float(WINDOW_HEIGHT), 0.1, 8000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    yaw, height, distance = camera_pos
    yaw_rad = math.radians(yaw)

    if hero_pov:
        cam_x = hero_pos[0]
        cam_y = hero_pos[1]
        cam_z = 600

        is_cutting_view = (
            (veg_cutting_active and not cutting_done) or
            (potato_cutting_active and not potato_cut_done) or
            (sausage_cutting_active and not sausage_cut_done)
        )
        is_fryer_view = (
            fries_frying_active or
            (game_state == STATE_FRIES_FRYING)
        )
        is_stove_view = (
            patty_on_stove or
            potato_boiling or
            (game_state in (STATE_L2_FRYING, STATE_FRIES_BOILING))
        )
        if is_cutting_view:
            # Lock the camera to look only at the cutting board at the exact same angle
            # while any cutting sequence (Q-key driven) is in progress.
            cx, cy = STATIONS["cutting"]
            target_x = cx
            target_y = cy - 10
            target_z = 175
        elif is_fryer_view:
            # Centered high-angle camera view over Deep Fryer station and sizzling oil baskets
            fx, fy = STATIONS["fryer"]
            cam_x = fx
            cam_y = fy + 550
            cam_z = 1100
            target_x = fx
            target_y = fy - 20
            target_z = 380
        elif is_stove_view:
            # Centered high-angle camera view over 2X stove top and 2 red frying pans (matching reference image)
            sx, sy = STATIONS["stove"]
            cam_x = sx
            cam_y = sy + 600
            cam_z = 1150
            target_x = sx
            target_y = sy - 20
            target_z = 520
        else:
            target_x = cam_x + 500 * math.sin(math.radians(angle))
            target_y = cam_y - 500 * math.cos(math.radians(angle))
            target_z = 230
    else:
        cam_x = hero_pos[0] - distance * math.sin(yaw_rad)
        cam_y = hero_pos[1] - distance * math.cos(yaw_rad)
        cam_z = height
        target_x = hero_pos[0]
        target_y = hero_pos[1]
        target_z = 120

    gluLookAt(cam_x, cam_y, cam_z,
              target_x, target_y, target_z,
              0, 0, 1)


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    setupCamera()
    grid_wall()
    draw_room_walls()
    draw_kitchen_props()

    # Don't draw the chef's own body while looking through the chef's own
    # eyes -- otherwise the first-person camera sits inside the head/hat
    # geometry and the whole screen fills with a single flat interior
    # color (looks like a blank "ash" screen with only the HUD text on
    # top of it).
    if not hero_pov:
        draw_player()

    draw_hud()
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Cooking Academy 3D - Feature 2: Cutting Mini-Game")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glEnable(GL_DEPTH_TEST)  # Enable 3D depth testing for solid opaque rendering
    glClearColor(0.11, 0.20, 0.20, 1.0)
    glutMainLoop()


if __name__ == "__main__":
    main()

