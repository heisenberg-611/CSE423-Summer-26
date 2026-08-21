from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import math
import random
import time



# Quadric helper

quadric = None

def get_quadric():
    global quadric
    if quadric is None:
        quadric = gluNewQuadric()
    return quadric



# Grid / arena constants

GRID_LENGTH = 700
TILE = 100
WALL_HEIGHT = 100
PLAYER_LIMIT = GRID_LENGTH - 40
ENEMY_COUNT = 5



# Gameplay constants

MOVE_STEP = 20.0
TURN_STEP = 15.0

BULLET_SPEED = 2000.0
ENEMY_SPEED = 30.0

CHEAT_SPIN_SPEED = 150
CHEAT_FIRE_COOLDOWN = 0.10

fovY = 120



# Player state

player_x = 0.0
player_y = 0.0
player_angle = 0.0
view_angle = 0.0



# Game status

life = 5
score = 0
missed = 0
game_over = False



# Cheat / camera modes

cheat_mode = False
cheat_follow = False
first_person = False

camera_angle = 180.0
camera_height = 600.0
camera_radius = 550.0

DEFAULT_FP_HEIGHT = 180.0
fp_height = DEFAULT_FP_HEIGHT



# Game objects

bullets = []
enemies = []



# Timing

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
    G = GRID_LENGTH
    H = WALL_HEIGHT

    glBegin(GL_QUADS)

    glColor3f(0, 0, 1)
    glVertex3f(-G, G, 0)
    glVertex3f(G, G, 0)
    glVertex3f(G, G, H)
    glVertex3f(-G, G, H)

    glColor3f(0, 1, 1)
    glVertex3f(G, -G, 0)
    glVertex3f(G, G, 0)
    glVertex3f(G, G, H)
    glVertex3f(G, -G, H)

    glColor3f(0, 1, 0)
    glVertex3f(-G, -G, 0)
    glVertex3f(G, -G, 0)
    glVertex3f(G, -G, H)
    glVertex3f(-G, -G, H)

    glColor3f(1, 1, 1)
    glVertex3f(-G, -G, 0)
    glVertex3f(-G, G, 0)
    glVertex3f(-G, G, H)
    glVertex3f(-G, -G, H)

    glEnd()


def draw_player():
    glPushMatrix()

    if game_over:
        glTranslatef(player_x, player_y, 20)
    else:
        glTranslatef(player_x, player_y, 0)

    glRotatef(player_angle, 0, 0, 1)

    if game_over:
        glRotatef(-90, 0, 1, 0)

    
    # Legs
    
    for side in (-1, 1):
        glPushMatrix()
        glTranslatef(0, side * 14, 0)
        glColor3f(0, 0, 1)
        gluCylinder(get_quadric(), 5, 11, 50, 10, 10)
        glPopMatrix()

    
    # Body / Torso
    
    glPushMatrix()
    glTranslatef(0, 0, 75)
    glColor3f(0.25, 0.3, 0.15)
    cuboid(18, 48, 50)
    glPopMatrix()

    
    # Gun
    
    glPushMatrix()
    glTranslatef(10, 0, 75)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.7, 0.7, 0.7)
    gluCylinder(get_quadric(), 8, 2, 70, 10, 10)
    glPopMatrix()

    
    # Hands
    
    for side in (-1, 1):
        glPushMatrix()
        glTranslatef(10, side * 20, 80)
        glRotatef(90, 0, 1, 0)
        glColor3f(1, 0.8, 0.6)
        gluCylinder(get_quadric(), 8, 3, 40, 10, 10)
        glPopMatrix()

    
    # Head
    
    glPushMatrix()
    glTranslatef(0, 0, 110)
    glColor3f(0, 0, 0)
    gluSphere(get_quadric(), 12, 12, 12)
    glPopMatrix()

    glPopMatrix()


def fire_bullet():
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
    return 40 + 8 * math.sin(t * 2 + e["phase"])


def draw_one_enemy(e, t):
    r = enemy_radius(e, t)

    glPushMatrix()

    glTranslatef(e["x"], e["y"], r)
    glColor3f(1, 0, 0)
    gluSphere(get_quadric(), r, 12, 12)

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

        if abs(b["x"]) > GRID_LENGTH or abs(b["y"]) > GRID_LENGTH:
            if b in bullets:
                bullets.remove(b)
            missed += 1
            print(f"Bullet missed: {missed}")

    if missed >= 10:
        trigger_game_over()


def move_enemies(dt):
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

    
    # Bullet vs enemy
    
    for b in list(bullets):
        bullet_hit = False

        for e in list(enemies):
            r = enemy_radius(e, t)
            dist = math.hypot(b["x"] - e["x"], b["y"] - e["y"])

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

    
    # Enemy vs player
    
    for e in list(enemies):
        r = enemy_radius(e, t)
        dist = math.hypot(player_x - e["x"], player_y - e["y"])

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
    if first_person:
        dx, dy = direction_from_angle(view_angle)
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

    if key in (b"r", b"R"):
        restart()
        return

    if game_over:
        return

    if key in (b"w", b"W"):
        dx, dy = gun_direction()
        player_x += dx * MOVE_STEP
        player_y += dy * MOVE_STEP

    elif key in (b"s", b"S"):
        dx, dy = gun_direction()
        player_x -= dx * MOVE_STEP
        player_y -= dy * MOVE_STEP

    elif key in (b"a", b"A"):
        player_angle = (player_angle + TURN_STEP) % 360

    elif key in (b"d", b"D"):
        player_angle = (player_angle - TURN_STEP) % 360

    elif key in (b"c", b"C"):
        cheat_mode = not cheat_mode

        if cheat_mode:
            print("Cheat Mode Enabled")
        else:
            cheat_follow = False
            print("Cheat Mode Disabled")

    elif key in (b"v", b"V"):
        if cheat_mode:
            cheat_follow = not cheat_follow

    player_x = clamp(player_x, -PLAYER_LIMIT, PLAYER_LIMIT)
    player_y = clamp(player_y, -PLAYER_LIMIT, PLAYER_LIMIT)

    if first_person and ((not cheat_mode) or cheat_follow):
        view_angle = player_angle


def specialKeyListener(key, x, y):
    global camera_angle, camera_height, fp_height

    if game_over:
        return

    if first_person:
        if key == GLUT_KEY_UP:
            fp_height = clamp(fp_height + 10, 120, 260)

        if key == GLUT_KEY_DOWN:
            fp_height = clamp(fp_height - 10, 120, 260)

    else:
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

    if game_over:
        return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person

        if first_person:
            view_angle = player_angle
            fp_height = DEFAULT_FP_HEIGHT


def update_view_angle():
    global view_angle

    if first_person:
        if (not cheat_mode) or cheat_follow:
            view_angle = player_angle


def idle():
    global last_time

    now = time.time()
    dt = now - last_time
    last_time = now

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
    ex, ey, ez = camera_position()

    def dist2(x, y):
        return (x - ex) ** 2 + (y - ey) ** 2

    items = []

    items.append((dist2(player_x, player_y), lambda: draw_player()))

    for e in enemies:
        items.append((dist2(e["x"], e["y"]), lambda e=e: draw_one_enemy(e, t)))

    for b in bullets:
        items.append((dist2(b["x"], b["y"]), lambda b=b: draw_one_bullet(b)))

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

    
    # Moving objects
    
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