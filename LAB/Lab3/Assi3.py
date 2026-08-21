from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import math
import random
import time


# -----------------------------
# Quadric helper (reuse single quadric instance)
# -----------------------------
quadric = None

def get_quadric():
    global quadric
    if quadric is None:
        quadric = gluNewQuadric()
    return quadric


# -----------------------------
# Grid / arena constants
# -----------------------------
GRID_LENGTH = 700
TILE = 100
WALL_HEIGHT = 100
PLAYER_LIMIT = GRID_LENGTH - 40
ENEMY_COUNT = 5

# -----------------------------
# Gameplay constants
# -----------------------------
MOVE_STEP = 20.0
TURN_STEP = 15.0

BULLET_SPEED = 2000.0
ENEMY_SPEED = 30.0

CHEAT_SPIN_SPEED = 150
CHEAT_FIRE_COOLDOWN = 0.10

fovY = 120


# -----------------------------
# Player state
# -----------------------------
player_x = 0.0
player_y = 0.0
player_angle = 0.0

# Used mainly for first-person camera direction
view_angle = 0.0


# -----------------------------
# Game status
# -----------------------------
life = 5
score = 0
missed = 0
game_over = False


# -----------------------------
# Cheat / camera modes
# -----------------------------
cheat_mode = False
cheat_follow = False
first_person = False

camera_angle = 180.0
camera_height = 600.0
camera_radius = 550.0

# First-person over-the-head camera default height
DEFAULT_FP_HEIGHT = 180.0
fp_height = DEFAULT_FP_HEIGHT


# -----------------------------
# Game objects
# -----------------------------
bullets = []
enemies = []


# -----------------------------
# Timing
# -----------------------------
last_time = time.time()
last_cheat_shot = 0.0
game_animation_time = time.time()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)

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


def cuboid(width, depth, height):
    """
    Draws a box centered at the current origin.
    Uses only glutSolidCube and glScalef.
    """
    glPushMatrix()
    glScalef(width, depth, height)
    glutSolidCube(1)
    glPopMatrix()


def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def direction_from_angle(angle):
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)


def gun_direction():
    return direction_from_angle(player_angle)

def draw_grid():
    """
    Dynamically generated checkerboard floor.
    Alternates white and light-purple tiles.
    """
    tiles_per_side = int((GRID_LENGTH * 2) // TILE)

    glBegin(GL_QUADS)

    for i in range(tiles_per_side):
        for j in range(tiles_per_side):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)

            x = -GRID_LENGTH + i * TILE
            y = -GRID_LENGTH + j * TILE

            glVertex3f(x, y, 0)
            glVertex3f(x + TILE, y, 0)
            glVertex3f(x + TILE, y + TILE, 0)
            glVertex3f(x, y + TILE, 0)

    glEnd()


def draw_walls():
    """
    Four vertical boundary walls around the grid.
    Colors: Blue (y=+G), Cyan (x=+G), Green (y=-G), White (x=-G).
    """
    G = GRID_LENGTH
    H = WALL_HEIGHT

    glBegin(GL_QUADS)

    # Blue wall, y = +G (top-left in reference view)
    glColor3f(0, 0, 1)
    glVertex3f(-G, G, 0)
    glVertex3f(G, G, 0)
    glVertex3f(G, G, H)
    glVertex3f(-G, G, H)

    # Cyan wall, x = +G (top-right in reference view)
    glColor3f(0, 1, 1)
    glVertex3f(G, -G, 0)
    glVertex3f(G, G, 0)
    glVertex3f(G, G, H)
    glVertex3f(G, -G, H)

    # Green wall, y = -G (bottom-right in reference view)
    glColor3f(0, 1, 0)
    glVertex3f(-G, -G, 0)
    glVertex3f(G, -G, 0)
    glVertex3f(G, -G, H)
    glVertex3f(-G, -G, H)

    # White wall, x = -G (bottom-left in reference view)
    glColor3f(1, 1, 1)
    glVertex3f(-G, -G, 0)
    glVertex3f(-G, G, 0)
    glVertex3f(-G, G, H)
    glVertex3f(-G, -G, H)

    glEnd()

def draw_player():
    glPushMatrix()
    
    # """
    # Player model components:
    # - Head: 1 Sphere
    # - Body / Torso: 1 Cuboid
    # - Both Hands / Arms: 2 Cylinders (left and right)
    # - Gun: 1 Cylinder (in the middle between both hands)
    # - Both Legs: 2 Cylinders (standing on floor)
    # """  

    if game_over:
        # Lift lying body so the back rests cleanly on the floor
        glTranslatef(player_x, player_y, 20)
    else:
        glTranslatef(player_x, player_y, 0)

    # Rotate whole player/gun direction
    glRotatef(player_angle, 0, 0, 1)

    # Lie down when game over (fall backwards, face up)
    if game_over:
        glRotatef(-90, 0, 1, 0)

    # 1. -----------------------------
    # Both Legs: two tapered cylinders (drawn first, bottom layer)
    # -----------------------------
    for side in (-1, 1):
        glPushMatrix()
        glTranslatef(0, side * 14, 0)
        glColor3f(0, 0, 1)
        gluCylinder(get_quadric(), 5, 11, 50, 10, 10)
        glPopMatrix()

    # 2. -----------------------------
    # Body / Torso: wider shoulder-to-shoulder (Y=48), narrower front-to-back (X=18)
    # -----------------------------
    glPushMatrix()
    glTranslatef(0, 0, 75)
    glColor3f(0.25, 0.3, 0.15)
    cuboid(18, 48, 50)
    glPopMatrix()

    # 3. -----------------------------
    # Gun: cylinder in the middle between both hands
    # -----------------------------
    glPushMatrix()
    glTranslatef(10, 0, 75)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.7, 0.7, 0.7)
    gluCylinder(get_quadric(), 8, 2, 70, 10, 10)
    glPopMatrix()

    # 4. -----------------------------
    # Both Hands: two tapered cylinders holding the gun
    # -----------------------------
    for side in (-1, 1):
        glPushMatrix()
        glTranslatef(10, side * 20, 80)
        glRotatef(90, 0, 1, 0)
        glColor3f(1, 0.8, 0.6)
        gluCylinder(get_quadric(), 8, 3, 40, 10, 10)
        glPopMatrix()

    # 5. -----------------------------
    # Head: sphere (drawn last so it sits on TOP of body and shoulders)
    # -----------------------------
    glPushMatrix()
    glTranslatef(0, 0, 110)
    glColor3f(0, 0, 0)
    gluSphere(get_quadric(), 12, 12, 12)
    glPopMatrix()

    glPopMatrix()

def fire_bullet():
    # """
    # Fires a cube bullet in the direction of the gun.
    # """
    if game_over:
        return

    dx, dy = gun_direction()

    bullets.append({
        "x": player_x + dx * 70,
        "y": player_y + dy * 70,
        "z": 75,
        "dx": dx,
        "dy": dy
    })
    print("Player Bullet Fired!")


def draw_one_bullet(b):
    glPushMatrix()
    glTranslatef(b["x"], b["y"], b["z"])
    glColor3f(1, 0, 0)
    glutSolidCube(12)
    glPopMatrix()


def spawn_enemy():
    """
    Spawns one enemy at a random position.
    Avoid spawning too close to the player.
    """
    while True:
        x = random.uniform(-GRID_LENGTH + 80, GRID_LENGTH - 80)
        y = random.uniform(-GRID_LENGTH + 80, GRID_LENGTH - 80)

        if math.hypot(x - player_x, y - player_y) > 200:
            return {
                "x": x,
                "y": y,
                "phase": random.uniform(0, math.pi * 2)
            }


def init_enemies():
    enemies.clear()
    for _ in range(ENEMY_COUNT):
        enemies.append(spawn_enemy())


def enemy_radius(e, t):
    """
    Enemies continuously shrink and expand.
    """
    return 40 + 8 * math.sin(t * 2 + e["phase"])


def draw_one_enemy(e, t):
    """
    Enemy is made of exactly two spheres:
    - red body sphere
    - smaller black head sphere
    """
    r = enemy_radius(e, t)

    glPushMatrix()

    # Body sphere center is lifted by r so the sphere touches the floor
    glTranslatef(e["x"], e["y"], r)
    glColor3f(1, 0, 0)
    gluSphere(get_quadric(), r, 12, 12)

    # Head sphere
    glTranslatef(0, 0, r * 0.9)
    glColor3f(0, 0, 0)
    gluSphere(get_quadric(), r * 0.45, 10, 10)

    glPopMatrix()

def trigger_game_over():
    global game_over, cheat_mode, cheat_follow, first_person
    if not game_over:
        game_over = True
        cheat_mode = False
        cheat_follow = False
        first_person = False


def move_bullets(dt):
    global missed

    for b in list(bullets):
        b["x"] += b["dx"] * BULLET_SPEED * dt
        b["y"] += b["dy"] * BULLET_SPEED * dt

        # Bullet left the arena => missed bullet (always counted)
        if abs(b["x"]) > GRID_LENGTH or abs(b["y"]) > GRID_LENGTH:
            if b in bullets:
                bullets.remove(b)
            missed += 1
            print(f"Bullet missed: {missed}")

    if missed >= 10:
        trigger_game_over()


def move_enemies(dt):
    """
    Enemies continuously move toward the player.
    """
    for e in enemies:
        dx = player_x - e["x"]
        dy = player_y - e["y"]
        dist = math.hypot(dx, dy)

        if dist > 1:
            e["x"] += (dx / dist) * ENEMY_SPEED * dt
            e["y"] += (dy / dist) * ENEMY_SPEED * dt


def check_collisions(t):
    global score, life, game_over

    if game_over:
        return

    # -----------------------------
    # Bullet vs enemy
    # -----------------------------
    for b in list(bullets):
        bullet_hit = False

        for e in list(enemies):
            r = enemy_radius(e, t)
            dist = math.hypot(b["x"] - e["x"], b["y"] - e["y"])

            # 6 is approximately half the bullet cube size
            if dist <= r + 6:
                score += 1

                if b in bullets:
                    bullets.remove(b)

                if e in enemies:
                    enemies.remove(e)
                    enemies.append(spawn_enemy())

                bullet_hit = True
                break

        if bullet_hit:
            continue

    # -----------------------------
    # Enemy vs player
    # -----------------------------
    for e in list(enemies):
        r = enemy_radius(e, t)
        dist = math.hypot(player_x - e["x"], player_y - e["y"])

        # 25 is an approximate player collision radius
        if dist <= r + 25:
            life -= 1
            print(f"Remaining player life: {life}")

            if e in enemies:
                enemies.remove(e)
                enemies.append(spawn_enemy())

            if life <= 0:
                life = 0
                trigger_game_over()
                break

    if missed >= 10:
        trigger_game_over()


def do_cheat(dt, now):
    """
    Cheat mode:
    - gun rotates continuously and smoothly
    - fires automatically when an enemy is within the gun's geometric line of sight
    """
    global player_angle, last_cheat_shot

    player_angle = (player_angle + CHEAT_SPIN_SPEED * dt) % 360

    if now - last_cheat_shot >= CHEAT_FIRE_COOLDOWN:
        dx, dy = gun_direction()

        for e in enemies:
            ex = e["x"] - player_x
            ey = e["y"] - player_y
            dist = math.hypot(ex, ey)

            if dist < 1:
                continue

            r = enemy_radius(e, now)
            # Exact geometric condition for gun ray to intersect the enemy sphere
            required_alignment = dist / math.hypot(dist, r)

            alignment = (ex / dist) * dx + (ey / dist) * dy

            if alignment >= required_alignment:
                fire_bullet()
                last_cheat_shot = now
                break


def restart():
    global life, score, missed, game_over
    global player_x, player_y, player_angle, view_angle
    global cheat_mode, cheat_follow, first_person
    global camera_angle, camera_height, fp_height
    global last_cheat_shot

    life = 5
    score = 0
    missed = 0
    game_over = False

    player_x = 0.0
    player_y = 0.0
    player_angle = 0.0
    view_angle = 0.0

    cheat_mode = False
    cheat_follow = False
    first_person = False

    camera_angle = 180.0
    camera_height = 600.0
    fp_height = DEFAULT_FP_HEIGHT

    last_cheat_shot = 0.0

    bullets.clear()
    init_enemies()
    print(f"Remaining player life: {life}")

def camera_position():
    """
    Returns current camera eye position.
    Used by setupCamera and draw-order sorting.
    """
    if first_person:
        dx, dy = direction_from_angle(view_angle)
        # Position camera behind and above the head, tracking rotation
        return (
            player_x - dx * 28.0,
            player_y - dy * 28.0,
            fp_height
        )

    rad = math.radians(camera_angle)
    return (
        camera_radius * math.cos(rad),
        camera_radius * math.sin(rad),
        camera_height
    )


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 3000.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    ex, ey, ez = camera_position()

    if first_person:
        dx, dy = direction_from_angle(view_angle)

        # Dynamic perspective looking forward over head and gun into arena
        gluLookAt(
            ex, ey, ez,
            player_x + dx * 150.0, player_y + dy * 150.0, ez - 28.0,
            0, 0, 1
        )
    else:
        gluLookAt(
            ex, ey, ez,
            0, 0, 0,
            0, 0, 1
        )


def keyboardListener(key, x, y):
    global player_x, player_y, player_angle
    global cheat_mode, cheat_follow, view_angle

    # Restart game
    if key in (b"r", b"R"):
        restart()
        return

    if game_over:
        return

    # Move forward
    if key in (b"w", b"W"):
        dx, dy = gun_direction()
        player_x += dx * MOVE_STEP
        player_y += dy * MOVE_STEP

    # Move backward
    elif key in (b"s", b"S"):
        dx, dy = gun_direction()
        player_x -= dx * MOVE_STEP
        player_y -= dy * MOVE_STEP

    # Rotate gun/player left
    elif key in (b"a", b"A"):
        player_angle = (player_angle + TURN_STEP) % 360

    # Rotate gun/player right
    elif key in (b"d", b"D"):
        player_angle = (player_angle - TURN_STEP) % 360

    # Toggle cheat mode
    elif key in (b"c", b"C"):
        cheat_mode = not cheat_mode

        if cheat_mode:
            print("Cheat Mode Enabled")
        else:
            cheat_follow = False
            print("Cheat Mode Disabled")

    # Toggle cheat camera follow
    # Works only when cheat mode is active
    elif key in (b"v", b"V"):
        if cheat_mode:
            cheat_follow = not cheat_follow

    # Keep player inside arena
    player_x = clamp(player_x, -PLAYER_LIMIT, PLAYER_LIMIT)
    player_y = clamp(player_y, -PLAYER_LIMIT, PLAYER_LIMIT)

    # Keep first-person view synchronized when appropriate
    if first_person and ((not cheat_mode) or cheat_follow):
        view_angle = player_angle


def specialKeyListener(key, x, y):
    global camera_angle, camera_height, fp_height

    # Disable all camera adjustments when game over
    if game_over:
        return

    if first_person:
        # In first-person, UP/DOWN adjust eye height
        if key == GLUT_KEY_UP:
            fp_height = clamp(fp_height + 10, 120, 260)

        if key == GLUT_KEY_DOWN:
            fp_height = clamp(fp_height - 10, 120, 260)

    else:
        # Third-person orbit camera
        if key == GLUT_KEY_LEFT:
            camera_angle -= 5

        if key == GLUT_KEY_RIGHT:
            camera_angle += 5

        if key == GLUT_KEY_UP:
            camera_height = clamp(camera_height + 20, 150, 1500)

        if key == GLUT_KEY_DOWN:
            camera_height = clamp(camera_height - 20, 150, 1500)


def mouseListener(button, state, x, y):
    global first_person, view_angle, fp_height

    # Disable all mouse actions (shooting and camera toggle) when game over
    if game_over:
        return

    # Left click fires bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()

    # Right click toggles first-person / third-person
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person

        if first_person:
            view_angle = player_angle
            fp_height = DEFAULT_FP_HEIGHT

def update_view_angle():
    """
    Keeps first-person camera direction connected to gun direction
    when cheat mode is off or when cheat_follow is active.
    """
    global view_angle

    if first_person:
        if (not cheat_mode) or cheat_follow:
            view_angle = player_angle


def idle():
    """
    GLUT idle callback.
    All animation happens here because glutTimerFunc is not allowed.
    """
    global last_time

    now = time.time()
    dt = now - last_time
    last_time = now

    # Avoid huge jumps if window lags
    if dt > 0.1:
        dt = 0.1

    if not game_over:
        move_bullets(dt)
        move_enemies(dt)
        check_collisions(now)

        if cheat_mode:
            do_cheat(dt, now)

        update_view_angle()

    glutPostRedisplay()


def draw_moving_objects(t):
    """
    Draws player, enemies, and bullets sorted from farthest to nearest.
    This is the painter's algorithm substitute for depth testing.
    """
    ex, ey, ez = camera_position()

    def dist2(x, y):
        return (x - ex) ** 2 + (y - ey) ** 2

    items = []

    # Draw player model
    items.append((dist2(player_x, player_y), lambda: draw_player()))

    for e in enemies:
        items.append((dist2(e["x"], e["y"]), lambda e=e: draw_one_enemy(e, t)))

    for b in bullets:
        items.append((dist2(b["x"], b["y"]), lambda b=b: draw_one_bullet(b)))

    # Farthest first, nearest last
    items.sort(key=lambda item: item[0], reverse=True)

    for _, draw_function in items:
        draw_function()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    # Static scene
    draw_grid()
    draw_walls()

    # Moving objects (freeze animation time when game over)
    global game_animation_time
    if not game_over:
        game_animation_time = time.time()
    draw_moving_objects(game_animation_time)

    # HUD text
    if game_over:
        draw_text(10, 770, f"Game is Over. Your Score is {score}.")
        draw_text(10, 740, 'Press "R" to Restart the Game.')
    else:
        draw_text(10, 770, f"Player Life Remaining: {life}")
        draw_text(10, 740, f"Game Score: {score}")
        draw_text(10, 710, f"Player Bullet Missed: {missed}")

    glutSwapBuffers()


def main():
    init_enemies()

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)

    wind = glutCreateWindow(b"Bullet Frenzy")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()