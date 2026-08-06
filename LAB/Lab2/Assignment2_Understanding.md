# CSE 423 — Lab 02 / Assignment 2: "Catch the Diamonds!"

> Source: `Assignment 2.docx.pdf` (Dept. of CSE, BRACU — Course CSE 423, Computer Graphics, Credits 0.75).
> The document is really two things stitched together: a **lab manual on the Midpoint Line Drawing Algorithm**
> (Topic Overview → Challenges → Activity Detail) and then the **Activity Task**, which is the graded game.

---

## 0. The one-paragraph version

Build a 2D game in Python + PyOpenGL called **Catch the Diamonds!**. A trapezoid "catcher" sits at the bottom
and slides left/right with the arrow keys; diamonds fall from the top at random x-positions in random bright
colors; catching one scores a point, missing one ends the game. Three clickable buttons sit at the top
(restart / play-pause / exit), and pressing `c` toggles an auto-play "cheat mode".

**The catch:** you may not use any OpenGL drawing primitive except `GL_POINTS`. Every single line on
screen — the diamond, the catcher, all three button icons — must be produced by **your own implementation of
the Midpoint Line Drawing Algorithm, generalized to all 8 zones**.

### Grading (stated explicitly, in red, at the end of the PDF)

| Weight | What it's for |
|---|---|
| 50% | Midpoint line drawing implementation (8-zone) |
| 50% | The game itself |
| **0** | **If the game is built without midpoint lines, the whole assignment scores 0** |
| **−50%** | Using any OpenGL function that is not in the two demo `.py` files shared on BuX |

---

# PART A — The Midpoint Line Drawing Algorithm (50%)

## A.1 Why not DDA?

You already saw **DDA** in theory class: given `(x1,y1)` and `(x2,y2)`, find all the intermediate pixels.
DDA works, but it uses **floating-point arithmetic** (it accumulates `y += m` every step), which is slow and
needs rounding at every pixel.

**Midpoint** does the same job with **integer arithmetic only** — no floats, no rounding — by tracking a
*decision variable* incrementally. That's the whole point of the lab.

## A.2 The core idea (Zone 0 only)

The base algorithm assumes:

- the line is drawn **left → right** (`x1 < x2`, `y1 < y2`)
- the slope is **between 0 and 1** (`0 < m < 1`)

That is **Zone 0**. Under those assumptions, from the current pixel `P(xp, yp)` there are only **two**
candidates for the next pixel:

- **E** (East) = `(xp+1, yp)` — go straight right
- **NE** (North-East) = `(xp+1, yp+1)` — go right and up

The **midpoint** between them is `M(xp+1, yp+½)`. The rule:

- **M is above the line → pick E**
- **M is below the line → pick NE**

### How do you know if M is above or below?

Take `y = mx + B`, substitute `m = dy/dx`, and rearrange into an implicit form:

```
F(x, y) = dy·x − dx·y + B·dx
```

Then:

| Position of (x, y) | F(x, y) |
|---|---|
| On the line | `= 0` |
| Above the line | `< 0` |
| Below the line | `> 0` |

So evaluate `F` at the midpoint, and the sign tells you which pixel to take. Because `F` is linear, you never
have to recompute it from scratch — you just add a constant increment each step. That's the decision variable `d`.

## A.3 Zone-0 pseudocode (verbatim from the PDF)

```c
DrawLine(int x1, int y1, int x2, int y2)
{
    int dx, dy, d, incE, incNE, x, y;
    dx    = x2 - x1;
    dy    = y2 - y1;
    d     = 2*dy - dx;          // initial decision variable
    incE  = 2*dy;               // increment if we went East
    incNE = 2*(dy - dx);        // increment if we went North-East
    y = y1;
    for (x = x1; x <= x2; x++)
    {
        WritePixel(x, y);
        if (d > 0) {            // midpoint below line → NE
            d = d + incNE;
            y = y + 1;
        } else {                // midpoint above line → E
            d = d + incE;
        }
    }
}
```

Everything here is `int`. That's the payoff.

> In Python/PyOpenGL, `WritePixel(x, y)` becomes:
> `glBegin(GL_POINTS); glVertex2f(x, y); glEnd()` — using the point primitive only.

```python
def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
```

Set the colour *before* the `glBegin` block, not inside it:

```python
glColor3f(1.0, 1.0, 1.0)     # white catcher
draw_pixel(x, y)
```

Opening and closing `glBegin`/`glEnd` per pixel is wasteful but perfectly fine at this scale. If you'd rather
batch, open it once and emit all the vertices of a line inside — but only if `glBegin`/`glVertex2f`/`glEnd`
are in the demo files (they are).

## A.4 Eight-way symmetry — the actual assignment

The above only draws one eighth of all possible lines. The naive fix is to write eight different versions of
the algorithm. The PDF explicitly rejects that:

> *"Couldn't we get rid of all these redundant methods & have only one method that would handle lines in all
> 8 zones? It would make things more compact, flexible & robust."*

So you write **one** line routine and wrap it in a coordinate transformation:

```
    convert to Zone 0  →  run Zone-0 midpoint  →  convert each computed point back  →  plot
```

Note the order carefully: **you convert the endpoints in, and you convert every intermediate point back out
before plotting.** If you convert back only the endpoints, you'll draw a line in the wrong direction.

### The 8 zones

The zones are the 8 sectors cut by the x-axis, y-axis, and the two diagonals `y = x` and `y = −x`. With
`dx = x2 − x1` and `dy = y2 − y1`:

| Zone | Slope range | Condition on dx, dy |
|---|---|---|
| 0 | `0 < m < 1` | `dx > 0, dy > 0, \|dx\| > \|dy\|` |
| 1 | `m > 1` | `dx > 0, dy > 0, \|dy\| > \|dx\|` |
| 2 | `m < −1` | `dx < 0, dy > 0, \|dy\| > \|dx\|` |
| 3 | `−1 < m < 0` | `dx < 0, dy > 0, \|dx\| > \|dy\|` |
| 4 | `0 < m < 1` | `dx < 0, dy < 0, \|dx\| > \|dy\|` |
| 5 | `m > 1` | `dx < 0, dy < 0, \|dy\| > \|dx\|` |
| 6 | `m < −1` | `dx > 0, dy < 0, \|dy\| > \|dx\|` |
| 7 | `−1 < m < 0` | `dx > 0, dy < 0, \|dx\| > \|dy\|` |

Zones 0–3 are the "upper" half, 4–7 mirror them. Note that slope alone is ambiguous (Zone 0 and Zone 4 have
the same slope range) — **the sign of dx/dy is what disambiguates**, which is why the PDF's `FindZone` skeleton
branches on `dx` and `dy`, not on `m`.

The PDF gives you the skeleton and leaves the rest to you:

```c
int FindZone(int x1, int y1, int x2, int y2)
{
    if (abs(dx) >= abs(dy)) {
        if (dx > 0 && dy > 0)
            Zone = 0;
        // write conditions for other zones
    }
    else {
        if (dx > 0 && dy > 0)
            Zone = 1;
        // write conditions for other zones
    }
    return Zone;
}
```

In Python, with the zone table above as your reference:

```python
def find_zone(dx, dy):
    if abs(dx) >= abs(dy):          # shallow line: |dx| dominates -> zones 0, 3, 4, 7
        if dx >= 0 and dy >= 0:
            return 0
        # TODO: dx < 0, dy > 0 -> ?
        # TODO: dx < 0, dy < 0 -> ?
        # TODO: dx > 0, dy < 0 -> ?
    else:                           # steep line: |dy| dominates -> zones 1, 2, 5, 6
        if dx >= 0 and dy >= 0:
            return 1
        # TODO: the other three
```

Walk it as: *"which quadrant is the direction vector in (signs of dx, dy), and is the line shallow or
steep (|dx| vs |dy|)?"* Two bits of sign plus one bit of steepness = 8 cases.

**Quick way to test it:** draw eight lines from the screen centre, one aimed into each zone, and check that
all eight come out straight and land where you told them to.

```python
CX, CY = 400, 400        # screen centre
targets = [(700, 500), (500, 700), (300, 700), (100, 500),
           (100, 300), (300, 100), (500, 100), (700, 300)]
for tx, ty in targets:
    midpoint_line(CX, CY, tx, ty)
```

If one of the eight is missing, bent, or mirrored, that zone's entry in one of the two tables is wrong.

### Conversion tables

The PDF works one example in full (Zone 2) and says *"the students need to figure out the required conversion
for points in other zones."* Here is the complete pair of mappings, following the same logic.

**Into Zone 0** — given `(x, y)` in zone `z`, produce the Zone-0 equivalent:

| Zone | → Zone 0 |
|---|---|
| 0 | `( x,  y)` |
| 1 | `( y,  x)` |
| 2 | `( y, −x)` |
| 3 | `(−x,  y)` |
| 4 | `(−x, −y)` |
| 5 | `(−y, −x)` |
| 6 | `(−y,  x)` |
| 7 | `( x, −y)` |

**Back out of Zone 0** — given a computed `(x, y)` in Zone 0, restore it to zone `z`:

| Zone | Zone 0 → original |
|---|---|
| 0 | `( x,  y)` |
| 1 | `( y,  x)` |
| 2 | `(−y,  x)` |
| 3 | `(−x,  y)` |
| 4 | `(−x, −y)` |
| 5 | `(−y, −x)` |
| 6 | `( y, −x)` |
| 7 | `( x, −y)` |

A compact way to hold both tables — fill in the rest yourself from the tables above:

```python
# (x, y) in zone z  ->  Zone-0 coordinates
TO_ZONE0 = {
    0: lambda x, y: ( x,  y),
    1: lambda x, y: ( y,  x),
    2: lambda x, y: ( y, -x),
    # TODO: 3, 4, 5, 6, 7
}

# Zone-0 (x, y)  ->  back to zone z
FROM_ZONE0 = {
    0: lambda x, y: ( x,  y),
    1: lambda x, y: ( y,  x),
    2: lambda x, y: (-y,  x),      # note: NOT the same as TO_ZONE0[2]
    # TODO: 3, 4, 5, 6, 7
}

def to_zone0(x, y, zone):
    return TO_ZONE0[zone](x, y)

def from_zone0(x, y, zone):
    return FROM_ZONE0[zone](x, y)
```

**Self-test before you trust it** — round-tripping any point must give you back the original:

```python
for z in range(8):
    for (px, py) in [(3, 7), (-5, 2), (0, 4), (-6, -1)]:
        assert from_zone0(*to_zone0(px, py, z), z) == (px, py), f"zone {z} broken"
print("all 8 zones round-trip correctly")
```

Zones 0, 1, 3, 4, 5 are **self-inverse** (the same formula both ways). Only **2 and 6 differ between the two
tables** — that asymmetry is exactly where most people lose marks. Sanity-check the PDF's worked example:

> Zone 2 has `x < 0, y > 0`. To reach Zone 0 you need both coordinates positive with `|x| > |y|`, so swap
> them and negate what used to be `x`: `x₀ = y₂`, `y₀ = −x₂`. Going back: `y₂ = x₀`, `x₂ = −y₀`.

### The full pipeline (PDF's numbered steps)

1. Given two points `(x1, y1)` and `(x2, y2)`.
2. `zone1 = findZone(x1, y1)`, `zone2 = findZone(x2, y2)`. **Assume both endpoints are in the same zone**
   (`zone1 == zone2`) — the PDF grants this simplification. In practice compute the zone once from `dx, dy`.
3. Convert `(x1, y1)` from its zone to Zone 0 → `(x1', y1')`.
4. Convert `(x2, y2)` from its zone to Zone 0 → `(x2', y2')`.
5. Run the Zone-0 midpoint algorithm on `(x1', y1')` and `(x2', y2')`.
6. Calculate the intermediate points `(x, y)`.
7. **Before drawing each pixel, convert `(x, y)` back to its original zone**, then plot.

### Two pitfalls the PDF calls out by name

1. **Careless conversion.** Have a solid mental picture of which coordinates are positive/negative and which
   of `|dx|`/`|dy|` dominates in each zone. Most errors happen here.
2. **Order-dependence.** Your routine must draw the same line for `(x1,y1)→(x2,y2)` and `(x2,y2)→(x1,y1)`.
   The PDF's suggested fix is literally **"Swap!"** — normalize the endpoints before you start.

### Suggested Python shape

```python
def find_zone(dx, dy): ...            # returns 0..7

def to_zone0(x, y, zone): ...         # table 1
def from_zone0(x, y, zone): ...       # table 2

def draw_pixel(x, y): ...             # glBegin(GL_POINTS) ... glEnd()

def midpoint_line(x1, y1, x2, y2):
    zone = find_zone(x2 - x1, y2 - y1)
    x1, y1 = to_zone0(x1, y1, zone)
    x2, y2 = to_zone0(x2, y2, zone)
    dx, dy = x2 - x1, y2 - y1
    d, incE, incNE = 2*dy - dx, 2*dy, 2*(dy - dx)
    y = y1
    for x in range(x1, x2 + 1):
        draw_pixel(*from_zone0(x, y, zone))   # convert back before plotting
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
```

Once this works, every shape in the game is just a handful of calls to `midpoint_line`.

---

# PART B — The Game "Catch the Diamonds!" (50%)

> *"There will be diamonds falling from the top, your goal is to catch them before they hit the ground. The
> more diamonds you catch, the greater you score. But if you miss any of the diamonds, your game is over. You
> then have to start over again."*

## B.1 Rules (as listed in the PDF)

**Catcher**
- A **catcher bowl** (trapezoid) sits at the bottom of the screen.
- Moves **horizontally** with the **left and right arrow keys**.
- Must **not go off-screen** — clamp its position.

**Diamonds**
- Fall **vertically** from the top.
- **One diamond on screen at a time.**
- Each new diamond gets a **random horizontal position** and a **random color**.
- Colors must be **bright enough to contrast with the black background**.
- **Falling speed increases gradually over time** to ramp up difficulty.

**Catching**
- A diamond counts as caught when the catcher is beneath it *at the right moment* — i.e. **the two collide**.
- On a catch: `score += 1`, **print the current score to the console**, spawn a new diamond from the top.

**Game Over** (a diamond is missed)
- The falling diamond **vanishes**.
- **No further diamonds** fall.
- The catcher **can no longer be moved**.
- The catcher **turns red** instead of its usual white.
- Console prints **`"Game Over"` along with the final score** (demo shows `Game Over! Score: 4`).

**Shapes**
- The diamond and catcher must look **exactly like the figure**: the **diamond is four midpoint lines**, the
  **catcher is another four midpoint lines** (a trapezoid — wide top, narrower base).
- Sizes must be sensible: the diamond not too big, not so small it's invisible; the catcher not so wide that
  it makes the game trivially easy.

## B.2 The three buttons (top of the screen, all drawn with midpoint lines, all clickable)

| Button | Colour | Shape | Behaviour |
|---|---|---|---|
| Left | **Bright teal** | Left arrow `←` | **Restart** the game — *whether or not the game is over*. Reset score, reset diamond speed, spawn a new falling diamond, **revert the catcher's colour to white**. Console prints something like `"Starting over!"` |
| Middle | **Amber** | Play `▷` / Pause `❚❚` | **Toggle play/paused.** The icon reflects the state: **pause icon while playing, play icon while paused.** When paused, the diamond **freezes** and the catcher **cannot move**. |
| Right | **Red** | Cross `✕` | **Exit.** Print `"Goodbye"` with the score, then terminate the application. |

## B.3 Cheat Mode

- Toggled by pressing the **`c`** key (press again to exit).
- The game **plays itself**: the catcher moves left/right automatically and **never misses a diamond**.
- **Must physically travel** to the diamond's x-position the way a player would — **teleporting the catcher is
  explicitly disallowed.** (So: move toward the target at the catcher's normal speed each frame.)

## B.4 Expected console output

The demo screenshots show exactly this transcript shape:

```
Score: 1
Score: 2
Score: 3
Score: 4
Game Over! Score: 4
Starting over!
Score: 1
Score: 2
Score: 3
Score: 4
Goodbye! Score: 4
```

---

# PART C — Tips the PDF gives you

## C.1 AABB collision detection

Use **Axis-Aligned Bounding Box** collision: wrap the diamond and the catcher each in a rectangle and test
whether the rectangles overlap. Two boxes collide **only when they overlap on both axes** (overlap on one axis
alone is not a collision).

```c
bool hasCollided(AABB box1, AABB box2) {
    return box1.x < box2.x + box2.width  &&
           box1.x + box1.width  > box2.x &&
           box1.y < box2.y + box2.height &&
           box1.y + box1.height > box2.y;
}
```

In Python, a box is just a 4-tuple `(x, y, w, h)` with `(x, y)` as the **bottom-left** corner:

```python
def has_collided(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by
```

Then build each object's box from its centre and half-size:

```python
def diamond_box():
    return (diamond_x - D_HALF_W, diamond_y - D_HALF_H, 2*D_HALF_W, 2*D_HALF_H)

def catcher_box():
    return (catcher_x - C_HALF_W, CATCHER_Y, 2*C_HALF_W, CATCHER_H)
```

Two boxes that merely touch edges do **not** collide here (the comparisons are strict `<`/`>`), which is the
behaviour you want.

## C.2 Delta time (Δt)

Different machines have different refresh rates, and CPU load changes frame rate. If you animate by
**blindly adding a constant to a coordinate every frame**, your game runs at a different speed on every
computer.

Instead, measure the **time elapsed between two frames** and compute displacement from it:

```python
import time
now = time.time()
dt  = now - last_time
last_time = now

diamond_y -= speed * dt          # speed is in units/second, not units/frame
speed     += acceleration * dt   # difficulty ramp
```

The PDF nudges you toward high-school kinematics here (`s = v·t`, `v = v₀ + a·t`) and links the Wikipedia
article on *delta timing*.

## C.3 Termination

Exit with **`glutLeaveMainLoop()`**, not Python's `exit()`. The PDF tells you to work out *why* by trial and
error — the short answer is that `exit()` kills the process from inside GLUT's callback without letting the
main loop unwind and clean up the window/context.

## C.4 Difficulty tuning

Adjust the **diamond's acceleration** and the **catcher's speed** to make the game feel fair.

---

# PART D — Hard constraints (read twice)

1. **`GL_POINTS` only.** No `GL_LINES`, `GL_TRIANGLES`, `GL_QUADS`, `GL_POLYGON`, nothing else.
2. **Only OpenGL functions that appear in the two demo Python files shared on BuX.** Anything outside that
   set → **−50% on the whole assignment**.
3. **Everything on screen must come from your midpoint line implementation** — diamond, catcher, all three
   button icons.
4. **No midpoint line ⇒ 0**, no matter how good the game is.

---

# PART E — Suggested build order

1. **Get a window up** with the demo boilerplate (`glutInit`, display callback, `glutMainLoop`).
2. **`draw_pixel(x, y)`** using `GL_POINTS`. Verify a single dot appears.
3. **Zone-0 midpoint line.** Draw one shallow left-to-right line. Verify.
4. **`find_zone` + both conversion tables.** Test by drawing 8 lines radiating from the screen centre —
   if all eight are straight and hit their targets, Part A is done (that's 50% secured).
5. **Draw the static scene**: diamond (4 lines) and catcher (4 lines) at fixed positions.
6. **Keyboard**: arrow keys move the catcher, with screen-edge clamping.
7. **Animation**: make the diamond fall using delta time; respawn at a random x with a random bright colour.
8. **AABB collision** → score, console print, respawn. Then the miss case → game over, catcher turns red,
   everything freezes.
9. **Speed ramp** over time.
10. **Buttons**: draw the three icons with midpoint lines, then add mouse-click hit-testing on their
    bounding regions. Wire up restart / play-pause (with icon swap) / exit.
11. **Cheat mode** on `c`: each frame, step the catcher toward the diamond's x by its normal speed.

Steps 1–4 are the graded half that everything else depends on. Do not start step 5 until step 4 is solid.

---

# PART F — Scaffolding for the game half

Skeletons only — the `TODO`s are the parts that are actually being graded. **Cross-check every OpenGL/GLUT
name below against your two demo files before using it**; if a name isn't in them, don't use it.

## F.1 Program skeleton

```python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time

W, H = 800, 800

def iterate():
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W, 0.0, H, 0.0, 1.0)     # origin at bottom-left
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_buttons()
    draw_catcher()
    if not game_over:
        draw_diamond()
    glutSwapBuffers()

def animate():
    # all movement happens here, driven by delta time
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W, H)
glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(special_key)       # arrow keys
glutKeyboardFunc(keyboard)         # 'c'
glutMouseFunc(mouse)               # button clicks
glutMainLoop()
```

> Whether your ortho box is `(0, W, 0, H)` or centred like `(-W/2, W/2, ...)` is up to you — but **pick one and
> keep every coordinate in the file consistent with it**. Mixing the two is the #1 source of "my shape is
> off-screen" confusion.

## F.2 Game state

Keep it all in one place so `restart()` is trivial:

```python
catcher_x   = W // 2
diamond_x   = 0
diamond_y   = H
speed       = 150.0        # pixels per SECOND, not per frame
score       = 0
game_over   = False
paused      = False
cheat       = False
last_time   = time.time()
```

## F.3 Drawing the shapes (4 midpoint lines each)

The diamond is four corners connected in a cycle; the catcher is a trapezoid — wide at the **top**, narrower
at the base, matching the figure.

```python
def draw_polyline(points):
    """Connect points in a closed loop using midpoint lines."""
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        midpoint_line(int(x1), int(y1), int(x2), int(y2))

def draw_diamond():
    glColor3f(*diamond_color)
    cx, cy = diamond_x, diamond_y
    draw_polyline([
        (cx, cy + D_HALF_H),     # top
        (cx + D_HALF_W, cy),     # right
        (cx, cy - D_HALF_H),     # bottom
        (cx - D_HALF_W, cy),     # left
    ])

def draw_catcher():
    if game_over:
        glColor3f(1, 0, 0)       # red on game over
    else:
        glColor3f(1, 1, 1)       # usual white
    # TODO: four points of the trapezoid, wide top / narrow base
    draw_polyline([...])
```

`draw_polyline` also handles the button icons — the arrow, the two pause bars, and the cross are all just
short line lists.

## F.4 Random bright colour

"Bright enough to contrast with the background" — keep at least one channel near 1.0:

```python
def random_bright_color():
    c = [random.uniform(0.0, 1.0) for _ in range(3)]
    c[random.randint(0, 2)] = 1.0        # force one channel to full
    return tuple(c)
```

## F.5 Keyboard

```python
def special_key(key, x, y):
    global catcher_x
    if game_over or paused or cheat:
        return                                  # frozen / auto-driven
    if key == GLUT_KEY_LEFT:
        catcher_x -= CATCHER_STEP
    elif key == GLUT_KEY_RIGHT:
        catcher_x += CATCHER_STEP
    # TODO: clamp catcher_x so the bowl never leaves the screen
    #       remember the bowl is centred on catcher_x, so account for its half-width

def keyboard(key, x, y):
    global cheat
    if key == b'c':
        cheat = not cheat
        print("Cheat mode:", "ON" if cheat else "OFF")
```

## F.6 Mouse clicks on the buttons

GLUT gives mouse `y` measured from the **top** of the window, but your ortho world has `y` growing **upward** —
so flip it before hit-testing:

```python
def inside(px, py, box):
    bx, by, bw, bh = box
    return bx <= px <= bx + bw and by <= py <= by + bh

def mouse(button, state, x, y):
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return
    wy = H - y                       # window coords -> world coords
    if inside(x, wy, RESTART_BOX):
        restart()
    elif inside(x, wy, PLAYPAUSE_BOX):
        # TODO: toggle `paused` (and remember the icon must change too)
        pass
    elif inside(x, wy, EXIT_BOX):
        print("Goodbye! Score:", score)
        glutLeaveMainLoop()
```

Define `RESTART_BOX`, `PLAYPAUSE_BOX`, `EXIT_BOX` as generous rectangles around where you drew each icon — the
clickable region does not have to match the drawn shape exactly.

## F.7 The frame update

```python
def animate():
    global last_time, diamond_y, speed, score, game_over

    now = time.time()
    dt  = now - last_time
    last_time = now                  # update it even when paused, or dt explodes on resume

    if game_over or paused:
        glutPostRedisplay()
        return

    if cheat:
        step_catcher_toward(diamond_x, dt)

    diamond_y -= speed * dt
    speed     += ACCEL * dt          # gradual difficulty ramp

    if has_collided(diamond_box(), catcher_box()):
        score += 1
        print("Score:", score)
        spawn_diamond()
    elif diamond_y < 0:              # missed it
        game_over = True
        print("Game Over! Score:", score)

    glutPostRedisplay()
```

That `last_time = now` placement matters: if you skip updating it while paused, the first frame after
un-pausing gets a huge `dt` and the diamond teleports through the catcher.

## F.8 Cheat mode movement

The requirement is that the catcher **travels**, never teleports — so cap each frame's movement by its normal
speed:

```python
def step_catcher_toward(target_x, dt):
    global catcher_x
    max_step = CATCHER_SPEED * dt
    delta = target_x - catcher_x
    # TODO: move by min(abs(delta), max_step) in the direction of `delta`
    #       then clamp to the screen edges, same as manual movement
```

Give `CATCHER_SPEED` enough headroom that it can always outrun a falling diamond — otherwise "never misses a
diamond" quietly stops being true once the speed ramp kicks in.

## F.9 Spawn and restart

```python
def spawn_diamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(D_HALF_W, W - D_HALF_W)   # keep it fully on-screen
    diamond_y = H
    diamond_color = random_bright_color()

def restart():
    global score, speed, game_over, paused, catcher_x
    score, speed = 0, INITIAL_SPEED
    game_over, paused = False, False
    catcher_x = W // 2
    spawn_diamond()
    print("Starting over!")
```

`restart()` must work **whether or not the game is over** — that's stated in the rules — and it must put the
catcher's colour back to white, which happens automatically if `draw_catcher` reads the `game_over` flag.
