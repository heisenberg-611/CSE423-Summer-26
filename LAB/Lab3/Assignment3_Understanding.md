# CSE 423 — Lab 03 / Assignment 3: "Bullet Frenzy"

> Source: `Assignment 3.pdf` (Dept. of CSE, BRACU — CSE 423, Computer Graphics, Credits 0.75).
> Title in the PDF: **Lab 03 — OpenGL 3D Introduction and Transformation**.
> Structure: I. Topic Overview → II. Anticipated Challenges → III. Activity Discussion → IV. Activity Task.
> The template you must build on is sitting next to this file: **`3D_OpenGL_Intro.py`**.

---

## 0. The one-paragraph version

Build a **3D game in PyOpenGL** called **Bullet Frenzy**. A player character with a gun stands on a
checkerboard grid floor walled in by four coloured boundaries. Five enemies (spheres) constantly chase the
player. You move with **W/S**, turn the gun with **A/D**, and fire cube-shaped bullets with the **left mouse
button**. Arrow keys move/orbit the camera, right-click toggles first-person vs third-person, **C** turns on
an auto-firing cheat mode, **V** makes the camera follow the gun in cheat mode, and **R** restarts after
game over.

**The catch:** you may only use OpenGL functions that already appear in `3D_OpenGL_Intro.py`.

### The rules stated in red in the PDF

> **You can not use any other OpenGL function to implement this assignment other than what is given in this
> template code. Doing so will induce a 50% penalty on the overall assignment mark. [This includes
> glutTimerFunc too.] You have to run the above code file and understand its contents to proceed doing the
> assignment.**

Two things to notice: **`glutTimerFunc` is explicitly banned** (so all your animation happens in `idle()`),
and the restriction is on **OpenGL functions** — plain Python (`math`, `random`, `time`) is fine.

---

# PART A — The theory you're being taught (Topic Overview)

## A.1 The three fundamental transformations

Transformations are applied as **matrices** that modify the coordinates of objects:

| Transformation | Function | What it does |
|---|---|---|
| Translation | `glTranslatef(tx, ty, tz)` | Moves an object in 3D space |
| Rotation | `glRotatef(angle, x, y, z)` | Rotates around an axis — `angle` in **degrees**, `(x,y,z)` picks the axis |
| Scaling | `glScalef(sx, sy, sz)` | Changes size along each axis |

## A.2 Transformations accumulate — and order matters

This is the single most important idea in the lab. The PDF walks through this example line by line:

```python
glPushMatrix()

glTranslatef(2.0, 0.0, 0.0);  glColor3f(1,0,0);  draw_square()   # 2 right
glRotatef(45, 0.0, 0.0, 1.0); glColor3f(0,1,0);  draw_square()   # 2 right, rotated 45°
glTranslatef(2.0, 0.0, 0.0);  glColor3f(0,0,1);  draw_square()   # 4 right, rotated 45°
glRotatef(45, 0.0, 0.0, 1.0);                    draw_square()   # 4 right, rotated 90° total
glTranslatef(2.0, 0.0, 0.0);  glColor3f(1,0,1);  draw_square()   # 6 right, rotated 90° total

glPopMatrix()
```

The PDF's own conclusion:

> *"The transformations accumulate, so each square is drawn relative to the previously applied
> transformations."*

You are not moving objects — **you are moving the coordinate system**, and everything drawn afterwards
inherits every transformation applied before it. Note how the second `glRotatef(45,...)` brings the total to
90°, not back to 45°.

- **`glPushMatrix()`** saves the current matrix onto a stack.
- **`glPopMatrix()`** restores it, undoing *everything* done since the matching push.

**Rule of thumb for the whole assignment:** wrap every object you draw in its own `glPushMatrix()` /
`glPopMatrix()` pair. If you forget, the player's transformations will leak into the enemies, the enemies'
into the bullets, and your scene will drift apart in ways that are very hard to debug.

## A.3 Perspective projection — `gluPerspective(fovY, aspect, zNear, zFar)`

These four numbers define a **view frustum** (a truncated pyramid). Nothing outside it is visible.

| Parameter | Meaning (paraphrased from the PDF) |
|---|---|
| **fovY** | The angle between the plane through the camera + top of screen and the plane through the camera + bottom of screen. **Bigger angle = you see more of the world, but everything looks smaller.** |
| **aspect** | The viewport's aspect ratio. The template uses `1.25` — because the window is 1000×800, and 1000/800 = 1.25. (That's the answer to the template's `# Think why aspect ratio is 1.25?` comment.) |
| **zNear / zFar** | Distances to the near and far clipping planes. Nothing nearer than `zNear` or further than `zFar` is drawn. **Both must be > 0 and `zFar > zNear`.** |

On `zNear`/`zFar`: making `zFar` bigger than necessary **wastes depth-buffer precision and causes z-fighting**
(flickering where surfaces overlap). Setting `zNear` too close to the camera causes the same thing — and the
PDF notes that **a reasonable `zNear` matters more than `zFar`**.

## A.4 The camera — `gluLookAt`

```
gluLookAt(eyeX, eyeY, eyeZ,        # camera position
          centerX, centerY, centerZ, # target point it looks at
          upX, upY, upZ)             # up direction
```

**Read the template's `setupCamera()` carefully, because it fixes the convention for the entire assignment:**

```python
gluLookAt(x, y, z,     # camera_pos
          0, 0, 0,     # looking at the origin
          0, 0, 1)     # up vector is the Z axis
```

> ### ⚠️ In this template, **Z is up**, not Y.
> The floor grid is drawn in the **XY plane at z = 0** (see `showScreen()` — every grid vertex is
> `glVertex3f(±GRID_LENGTH, ±GRID_LENGTH, 0)`). So:
> - The player walks around in **x and y**.
> - "Height" — the player's head, the bullet's flight altitude, the camera's elevation — is **z**.
> - Turning the gun left/right is a rotation **about the z-axis**: `glRotatef(angle, 0, 0, 1)`.
>
> Getting this wrong is the fastest way to spend an evening wondering why your player is lying inside the
> floor.

---

# PART B — The Activity Task: "Bullet Frenzy"

> *"This assignment involves creating a 3D game in which the player controls a character with a gun that can
> move, rotate, and shoot bullets at enemies. The game environment includes a grid, moving enemies
> (represented as spheres), and features such as cheat modes and camera controls. The game also contains
> visual feedback on the player's actions and the status of the game."*

**Gaming setup:** the game starts exactly like the reference image, with the **player spawning at the centre
of the grid**.

## B.1 Drawing components (three crucial elements)

### i) The player — 1 player

Must look **exactly** like the reference figure. Built from three primitive types only:

1. **Sphere** — `gluSphere(gluNewQuadric(), radius, slices, stacks)`
2. **Cylinders** — `gluCylinder(gluNewQuadric(), base_r, top_r, height, slices, stacks)`
3. **Cuboids** — `glutSolidCube(size)` combined with `glScalef` (see F.3)

Reading the side / top / front views in the PDF, the parts are:

| Part | Shape in the figure |
|---|---|
| Head | one sphere, sitting on top of the torso |
| Torso | a cuboid (a box, taller than it is deep) |
| Two legs | tapered cylinders (base radius > top radius), splayed slightly |
| Two hands | small spheres at the front of the torso, either side of the gun |
| Gun | a long **tapered** cylinder pointing forward — `gluCylinder` with a big base radius and a tiny top radius makes the cone shape in the side view |

### ii) Enemies — **5 enemies at all times**

> *"The enemy should be exactly like the picture. It should take **two spheres** to complete."*

A large body sphere (red) plus a small head sphere (black) on top. That's it — no other shapes.

### iii) The grid floor + four boundaries

The floor is a **checkerboard** of alternating light-purple and white tiles, surrounded by **four vertical
boundary walls** in four different colours (blue, cyan, green, white in the reference shots).

> ### ⚠️ From "Anticipated Challenges" (b):
> *"The grid in the game has a pattern in creating it which the students need to comprehend as this grid needs
> to be created **dynamically and NOT through hardcode!**"*

So: nested loops with an alternating-colour rule, not 100 hand-typed `glVertex3f` calls. See F.2.

## B.2 Game features

### 1. Player movement and gun control

| Input | Action |
|---|---|
| **W** | Move the gun/player **forward** |
| **S** | Move **backward** |
| **A** | Rotate the gun **left** |
| **D** | Rotate the gun **right** |
| **Left mouse button** | **Fire a bullet** |

### 2. Camera control

| Input | Action |
|---|---|
| **UP / DOWN arrows** | Move the camera **up and down** |
| **LEFT / RIGHT arrows** | **Rotate the camera around the whole game floor** (orbit) |
| **Right mouse button** | Toggle **first-person** (camera follows the gun) ↔ **third-person** (fixed default position) |

Third-person is the **default** mode.

### 3. Cheat modes

- **C** toggles **cheat mode**: the gun **continuously rotates** and **fires automatically at enemies when one
  is in its line of sight**. The player can still move forward and backward while cheating.
- **V** toggles **automatic gun following**, which adjusts the camera's perspective. This works
  **only when cheat mode is active**, and is **only visible in first-person mode**.

> From "Anticipated Challenges" (c): cheat mode needs **no new machinery** — it's the fire-bullet function
> plus the turn-gun function plus a boolean flag, combined.

### 4. Game over and restart

- The game ends when **player life reaches zero** *or* the player **misses 10 bullets**.
- **Life reduces by 1 when an enemy touches the player.**
- On game over the player **lies down** (rotate the whole player 90°).
- **R** restarts: **life back to 5, score back to 0, bullets missed back to 0.**

### 5. Bullets and enemies

- Bullets are **cubes**, and travel **in the direction of the gun's angle**.
- Enemies **continuously move towards the player**; if the player moves, they follow.
- When an enemy is hit it **respawns at a random point** — so there are **always exactly 5**.
- Enemy spheres **shrink and expand continuously** (a pulsing animation).
- The game checks collisions between **bullets ↔ enemies** and between **player ↔ enemies**.

## B.3 On-screen text (HUD)

Top-left of the screen, drawn with the template's `draw_text()`:

```
Player Life Remaining: 5
Game Score: 0
Player Bullet Missed: 0
```

---

# PART C — Anticipated challenges (the PDF's own warnings)

**a. Camera and coordinates.** You must understand perspective projection and where the camera sits before
you can place the gun, enemies, and bullets. Explicitly: **the window coordinate system and the 3D world
coordinate system do not align.** Mouse clicks arrive in window pixels; your objects live in world units.

**b. The grid must be generated, not hardcoded.**

**c. Cheat mode is a combination, not a new system** — reuse `fire_bullet()` and the gun rotation, gated by a
flag.

---

# PART D — Hard constraints

1. **Only OpenGL functions present in `3D_OpenGL_Intro.py`.** Anything else → **−50% on the whole
   assignment**.
2. **`glutTimerFunc` is banned by name.** All animation goes in `idle()`.
3. The player, the enemy, and the grid+boundaries must look **exactly like the reference images**.
4. The grid must be built **dynamically**.
5. Always exactly **5 enemies**; **10 missed bullets** ends the game; life starts at **5**.

### Your allowed-function inventory

Everything below appears in the template, so all of it is safe:

```
Drawing    glBegin, glEnd, glVertex3f, GL_QUADS, GL_POINTS, glPointSize, glColor3f, glClear
Transforms glPushMatrix, glPopMatrix, glTranslatef, glRotatef, glScalef, glLoadIdentity, glMatrixMode
Shapes     glutSolidCube, gluSphere, gluCylinder, gluNewQuadric
Camera     gluPerspective, gluLookAt, gluOrtho2D, glViewport
Text       glRasterPos2f, glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
GLUT       glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow,
           glutDisplayFunc, glutKeyboardFunc, glutSpecialFunc, glutMouseFunc, glutIdleFunc,
           glutPostRedisplay, glutSwapBuffers, glutMainLoop
Constants  GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
           GL_PROJECTION, GL_MODELVIEW, GLUT_KEY_UP/DOWN/LEFT/RIGHT, GLUT_LEFT_BUTTON,
           GLUT_RIGHT_BUTTON, GLUT_DOWN
```

> ### Decision: **no `glEnable(GL_DEPTH_TEST)`**
> The template requests a depth buffer (`GLUT_DEPTH`) and clears it (`GL_DEPTH_BUFFER_BIT`), but **never
> calls `glEnable(GL_DEPTH_TEST)`** — and `glEnable` is not in the allowed set. The rule is absolute and the
> penalty is 50%, so **don't add it.** Objects are therefore painted in **draw order**, and you control
> correctness by choosing that order yourself — the painter's algorithm. See **F.13**.
>
> This costs you far less than it sounds like, because **nothing in this game is lit**. Every object is one
> flat `glColor3f`, so a sphere's back faces overdrawing its front faces is invisible — they're the same
> colour. Depth only matters *between* objects, and object-level sorting handles that completely.

---

# PART E — Suggested build order

1. **Run `3D_OpenGL_Intro.py` unchanged.** The PDF requires this. Press the arrow keys, watch `camera_pos`
   change, and confirm you can see the shapes.
2. **Replace the demo floor with your generated checkerboard**, then add the four boundary walls.
3. **Draw a static player** at the origin out of spheres/cylinders/cuboids until it matches the figure.
4. **Wire the HUD text** — three lines, top-left, using the template's `draw_text`.
5. **W/S/A/D**: move and rotate the player, clamped inside the boundaries.
6. **Arrow keys + right click**: camera orbit/height, and the first/third-person toggle.
7. **Bullets**: fire on left click, fly along the gun angle, count a miss when one leaves the arena.
8. **Enemies**: 5 of them, chasing the player, pulsing in size.
9. **Collisions**: bullet↔enemy (score + respawn) and player↔enemy (life − 1).
10. **Game over** (life 0 or 10 misses) → player lies down; **R** resets.
11. **Cheat mode (C)**, then **camera-follow (V)**.

Steps 1–3 are where the marks for "3D transformation understanding" live. Everything after is game logic.

Once step 8 puts several moving objects on screen at once, add the **draw-order sort from F.13** — that's
what stands in for depth testing here.

---

# PART F — Code scaffolding

Skeletons only — the `TODO`s are the graded parts. Everything here sticks to the allowed function list.

## F.1 State and constants

```python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random, time

GRID_LENGTH = 600          # floor spans -600..600 in x and y
TILE        = 100          # checkerboard tile size -> 12x12 tiles
WALL_H      = 100

player_x, player_y = 0.0, 0.0
player_angle       = 0.0    # degrees, rotation about the Z axis
life, score, missed = 5, 0, 0
game_over  = False

bullets = []                # each: {'x':, 'y':, 'z':, 'dx':, 'dy':}
enemies = []                # each: {'x':, 'y':, 'r':, 'phase':}

cheat_mode      = False
cheat_follow    = False     # the V key
first_person    = False     # right-click toggles
camera_angle    = 0.0       # orbit angle for LEFT/RIGHT arrows
camera_height   = 500.0     # UP/DOWN arrows
```

## F.2 The grid — generated, never hardcoded

Two nested loops over tile indices; the colour alternates with the **parity of `i + j`**:

```python
def draw_grid():
    n = GRID_LENGTH * 2 // TILE            # tiles per side
    glBegin(GL_QUADS)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)          # white
            else:
                glColor3f(0.7, 0.5, 0.95)   # light purple
            x = -GRID_LENGTH + i * TILE
            y = -GRID_LENGTH + j * TILE
            glVertex3f(x,        y,        0)
            glVertex3f(x + TILE, y,        0)
            glVertex3f(x + TILE, y + TILE, 0)
            glVertex3f(x,        y + TILE, 0)
    glEnd()
```

The four walls are four vertical quads around the same square, each a different colour:

```python
def draw_walls():
    G, H = GRID_LENGTH, WALL_H
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)        # blue wall
    glVertex3f(-G, G, 0); glVertex3f(G, G, 0); glVertex3f(G, G, H); glVertex3f(-G, G, H)
    # TODO: the other three walls (y = -G, x = G, x = -G) in their own colours
    glEnd()
```

## F.3 A cuboid from `glutSolidCube`

There is no "draw a box with three dimensions" call in the template — so scale a unit cube:

```python
def cuboid(w, d, h):
    """A box w x d x h, centred on the current origin."""
    glPushMatrix()
    glScalef(w, d, h)
    glutSolidCube(1)
    glPopMatrix()
```

Because `glScalef` is inside its own push/pop, the scaling won't leak into whatever you draw next.

## F.4 The player

Build it once, facing along **+x**, then let `glRotatef(player_angle, 0, 0, 1)` aim it:

```python
def draw_player():
    glPushMatrix()
    glTranslatef(player_x, player_y, 0)
    glRotatef(player_angle, 0, 0, 1)

    if game_over:
        glRotatef(90, 0, 1, 0)      # lie the whole body down

    # legs: two tapered cylinders standing on the floor
    for side in (-1, 1):
        glPushMatrix()
        glTranslatef(0, side * 15, 0)
        glColor3f(0, 0, 1)
        gluCylinder(gluNewQuadric(), 12, 6, 50, 10, 10)   # base_r, top_r, height
        glPopMatrix()

    # torso: a cuboid sitting on the legs
    glPushMatrix()
    glTranslatef(0, 0, 75)
    glColor3f(0.25, 0.3, 0.15)
    cuboid(30, 50, 50)
    glPopMatrix()

    # TODO: head sphere on top of the torso   -> gluSphere
    # TODO: two hand spheres at the front     -> gluSphere
    # TODO: the gun: a long tapered cylinder pointing along +x
    #       remember gluCylinder is built along +Z, so glRotatef(90, 0, 1, 0) first

    glPopMatrix()
```

> **`gluCylinder` always grows along the +Z axis** from the current origin. To make it point along +x, rotate
> 90° about y first. This is the trick you need for both the gun and the legs.

## F.5 Gun direction and firing

The gun's heading is just an angle; convert it to a unit vector with `cos`/`sin`:

```python
def gun_direction():
    rad = math.radians(player_angle)
    return math.cos(rad), math.sin(rad)

def fire_bullet():
    dx, dy = gun_direction()
    bullets.append({
        'x': player_x + dx * 40,     # start at the muzzle, not inside the body
        'y': player_y + dy * 40,
        'z': 90,                     # roughly gun height
        'dx': dx, 'dy': dy,
    })
```

Draw each bullet as a small cube:

```python
def draw_bullets():
    glColor3f(1, 0, 0)
    for b in bullets:
        glPushMatrix()
        glTranslatef(b['x'], b['y'], b['z'])
        glutSolidCube(12)
        glPopMatrix()
```

## F.6 Enemies — spawn, chase, pulse

```python
def spawn_enemy():
    return {
        'x': random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50),
        'y': random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50),
        'phase': random.uniform(0, math.pi * 2),     # so they don't all pulse in sync
    }

def enemy_radius(e, t):
    return 30 + 8 * math.sin(t * 2 + e['phase'])     # the shrink/expand animation

def move_enemies(dt):
    for e in enemies:
        dx, dy = player_x - e['x'], player_y - e['y']
        dist = math.hypot(dx, dy)
        if dist > 1:
            e['x'] += dx / dist * ENEMY_SPEED * dt   # normalise, then step
            e['y'] += dy / dist * ENEMY_SPEED * dt
```

Drawing one enemy is two spheres — body, then a smaller head above it:

```python
def draw_enemies(t):
    for e in enemies:
        r = enemy_radius(e, t)
        glPushMatrix()
        glTranslatef(e['x'], e['y'], r)
        glColor3f(1, 0, 0)
        gluSphere(gluNewQuadric(), r, 12, 12)
        glTranslatef(0, 0, r)                 # stack the head on top
        glColor3f(0, 0, 0)
        gluSphere(gluNewQuadric(), r * 0.45, 12, 12)
        glPopMatrix()
```

## F.7 Collisions

Everything here is a sphere, so distance-vs-radius is enough — no AABB needed:

```python
def close_enough(ax, ay, bx, by, threshold):
    return math.hypot(ax - bx, ay - by) < threshold
```

```python
def check_collisions(t):
    global score, life, game_over
    for b in list(bullets):
        for e in list(enemies):
            if close_enough(b['x'], b['y'], e['x'], e['y'], enemy_radius(e, t)):
                score += 1
                bullets.remove(b)
                enemies.remove(e)
                enemies.append(spawn_enemy())   # always exactly 5
                break
    # TODO: player <-> enemy  ->  life -= 1, and respawn that enemy
    #       otherwise it stays inside you and drains all 5 lives in one frame
    # TODO: if life <= 0 or missed >= 10:  game_over = True
```

## F.8 The frame update (in `idle()` — remember, no `glutTimerFunc`)

```python
last_time = time.time()

def idle():
    global last_time, missed
    now = time.time()
    dt  = now - last_time
    last_time = now

    if not game_over:
        for b in list(bullets):
            b['x'] += b['dx'] * BULLET_SPEED * dt
            b['y'] += b['dy'] * BULLET_SPEED * dt
            if abs(b['x']) > GRID_LENGTH or abs(b['y']) > GRID_LENGTH:
                bullets.remove(b)
                missed += 1                  # a miss = a bullet that left the arena
        move_enemies(dt)
        check_collisions(now)
        if cheat_mode:
            do_cheat(dt)

    glutPostRedisplay()
```

## F.9 Cheat mode

Spin the gun continuously; fire whenever an enemy lines up with the barrel:

```python
def do_cheat(dt):
    global player_angle
    player_angle = (player_angle + CHEAT_SPIN * dt) % 360
    dx, dy = gun_direction()
    for e in enemies:
        ex, ey = e['x'] - player_x, e['y'] - player_y
        dist = math.hypot(ex, ey)
        if dist < 1:
            continue
        # dot product of two unit vectors = cos(angle between them)
        alignment = (ex / dist) * dx + (ey / dist) * dy
        if alignment > 0.99:            # within a few degrees of the barrel
            fire_bullet()
            break
```

That `alignment > 0.99` is your "line of sight" test. Add a small cooldown so one pass doesn't emit fifty
bullets in fifty frames.

## F.10 Camera

Pull the eye position out into its own function — you need it twice: once for `gluLookAt`, and once for
sorting the draw order in F.13.

```python
def camera_position():
    if first_person:
        return player_x, player_y, 110               # roughly eye height
    rad = math.radians(camera_angle)
    return 500 * math.cos(rad), 500 * math.sin(rad), camera_height

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(120, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    ex, ey, ez = camera_position()
    if first_person:
        dx, dy = gun_direction()
        # TODO: when cheat_follow is on, the camera should track the spinning gun
        gluLookAt(ex, ey, ez,
                  ex + dx * 100, ey + dy * 100, ez,   # look where the gun points
                  0, 0, 1)
    else:
        gluLookAt(ex, ey, ez,
                  0, 0, 0,
                  0, 0, 1)
```

The third-person branch is a circular orbit: LEFT/RIGHT change `camera_angle`, UP/DOWN change
`camera_height`. That's the whole of "rotate around the whole game floor".

## F.11 Input

```python
def keyboardListener(key, x, y):
    global player_x, player_y, player_angle, cheat_mode, cheat_follow
    dx, dy = gun_direction()
    if key == b'w' and not game_over:
        player_x += dx * MOVE_STEP
        player_y += dy * MOVE_STEP
    # TODO: b's' -> backward;  b'a'/b'd' -> player_angle -/+ TURN_STEP
    # TODO: clamp player_x/player_y inside the walls
    if key == b'c':
        cheat_mode = not cheat_mode
    if key == b'v':
        cheat_follow = not cheat_follow      # only meaningful while cheat_mode and first_person
    if key == b'r':
        restart()

def specialKeyListener(key, x, y):
    global camera_angle, camera_height
    if key == GLUT_KEY_LEFT:  camera_angle -= 2
    if key == GLUT_KEY_RIGHT: camera_angle += 2
    # TODO: GLUT_KEY_UP / GLUT_KEY_DOWN -> camera_height

def mouseListener(button, state, x, y):
    global first_person
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person
```

## F.12 HUD and restart

The template's `draw_text` already handles switching to a 2D orthographic projection and back — just call it:

```python
draw_text(10, 770, f"Player Life Remaining: {life}")
draw_text(10, 740, f"Game Score: {score}")
draw_text(10, 710, f"Player Bullet Missed: {missed}")
```

```python
def restart():
    global life, score, missed, game_over, player_x, player_y, player_angle
    life, score, missed = 5, 0, 0
    game_over = False
    player_x = player_y = player_angle = 0
    bullets.clear()
    enemies.clear()
    enemies.extend(spawn_enemy() for _ in range(5))
```

`draw_text` uses `gluOrtho2D(0, 1000, 0, 800)`, so HUD coordinates are in that space regardless of your 3D
world scale — which is a small, concrete example of the PDF's warning that **window coordinates and world
coordinates do not align**.

## F.13 Draw order (your substitute for depth testing)

Since `glEnable(GL_DEPTH_TEST)` is off the table (Part D), whatever you draw **last wins**. So draw
**back to front** — the painter's algorithm.

Fixed order for the static parts:

```python
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()

    draw_grid()          # floor first - everything stands on it
    draw_walls()         # then the boundaries
    draw_moving_objects()  # then everything else, sorted (below)

    draw_text(10, 770, f"Player Life Remaining: {life}")
    draw_text(10, 740, f"Game Score: {score}")
    draw_text(10, 710, f"Player Bullet Missed: {missed}")

    glutSwapBuffers()
```

For the things that move, sort by **distance from the camera, farthest first**:

```python
def draw_moving_objects():
    ex, ey, ez = camera_position()

    def dist2(x, y):                       # squared distance is enough for sorting
        return (x - ex) ** 2 + (y - ey) ** 2

    items = []
    items.append((dist2(player_x, player_y), draw_player))
    for e in enemies:
        items.append((dist2(e['x'], e['y']), lambda e=e: draw_one_enemy(e)))
    for b in bullets:
        items.append((dist2(b['x'], b['y']), lambda b=b: draw_one_bullet(b)))

    items.sort(key=lambda pair: pair[0], reverse=True)   # farthest -> nearest
    for _, draw in items:
        draw()
```

Three notes on that snippet:

- Split `draw_enemies` / `draw_bullets` from F.6 and F.5 into **single-object** `draw_one_enemy(e)` and
  `draw_one_bullet(b)` functions so they can be sorted individually. Drawing all enemies as one group defeats
  the point.
- The `lambda e=e:` default-argument trick is deliberate. Without it, every lambda closes over the *same*
  loop variable and they'd all draw the last enemy.
- Sorting by **squared** distance avoids a pointless `sqrt` on every object every frame, and orders
  identically.

**Why this is enough:** with 5 enemies, a handful of bullets, and one player, you're sorting maybe a dozen
convex, non-overlapping objects per frame. The painter's algorithm only breaks down on objects that
interpenetrate or that mutually overlap in a cycle — neither happens here. And as noted in Part D, since
nothing is lit and every object is a single flat colour, a shape overdrawing *itself* is invisible.

If you notice a far enemy flashing in front of a near one, the sort is being skipped or the camera position
used for sorting doesn't match the one passed to `gluLookAt` — which is exactly why `camera_position()` is a
single shared function in F.10.
