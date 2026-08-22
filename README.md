# CSE423: Computer Graphics

This repository contains lab assignments, implementation guides, starter templates, and past midterm exam questions for **CSE423: Computer Graphics** at BRAC University.

---

## 📁 Repository Structure

```
CSE423/
├── LAB/                                      # Lab assignments, starter templates, and guides
│   ├── CSE423_OpenGL_Lab_Reference.ipynb     # Comprehensive OpenGL concepts notebook
│   ├── Lab1/                                 # Lab 01: OpenGL Setup & Basic Primitives
│   │   ├── Assignment/                       # Rain simulation & Bouncing balls
│   │   │   ├── Assi1.py                      # Task 1: House with Rain & Day/Night toggle
│   │   │   ├── Assi1_explained.py            # Task 1 with detailed annotations
│   │   │   ├── Assi2.py                      # Task 2: Interactive Bouncing Particles
│   │   │   ├── Assi2_explained.py            # Task 2 with detailed annotations
│   │   │   ├── Task1.py / Task1_2.py         # Task 1 alternative implementations
│   │   │   └── Task2.py                      # Task 2 alternative implementation
│   │   ├── First Program/                    # Intro OpenGL scripts
│   │   │   ├── Hello_openGL.py               # Basic OpenGL window initialization
│   │   │   └── Lets_draw_sth.py              # Primitive drawing demo
│   │   └── Assignment 1.png                  # Assignment specification screenshot
│   │
│   ├── Lab2/                                 # Lab 02: Midpoint Line Algorithm (2D Game)
│   │   ├── Assignment/                       # "Catch the Diamonds!" game
│   │   │   ├── Assi1.py                      # Complete game implementation
│   │   │   └── Assi1_explained.py            # Line-by-line annotated implementation
│   │   ├── Assignment2_Understanding.md      # Comprehensive deep-dive & theory guide
│   │   ├── Assignment 2.docx.pdf             # Official lab assignment specification
│   │   └── Assignment 2.png                  # Assignment specification screenshot
│   │
│   └── Lab3/                                 # Lab 03: 3D OpenGL & Hierarchical Transformations
│       ├── 3D_OpenGL_Intro.py                # 3D starter template & transformations demo
│       ├── Assi3.py                          # "Bullet Frenzy" 3D Game implementation
│       ├── Assignment3_Understanding.md      # Detailed 3D mechanics & implementation guide
│       ├── Assi3_Viva_Guide.md               # Viva preparation and Q&A guide
│       ├── Assignment 3.pdf                  # Official lab assignment specification
│       └── Assignment 3.png                  # Assignment specification screenshot
│
└── MID questions/                            # Past Midterm Exam Question Papers
    ├── 1. CSE423 Spring 2025 Mid Question.pdf
    ├── 2. CSE423 Summer 2025 Mid Question.pdf
    ├── 3. CSE423 Fall 2025 Mid Question.pdf
    └── 4. CSE423 Spring 2026 Mid Question.pdf
```

---

## 🎯 Lab Modules Overview

### 🔹 Lab 1: OpenGL Setup & 2D Primitives
- **Concepts**: OpenGL initialization pipeline, coordinate systems, basic primitives (`GL_POINTS`, `GL_LINES`, `GL_TRIANGLES`, `GL_QUADS`), keyboard & mouse callbacks, animation loop.
- **Task 1 — House in the Rain**:
  - Interactive day/night cycle with background transitions.
  - Directional rain effect (toggled and adjusted using arrow keys).
- **Task 2 — Interactive Bouncing Particles**:
  - Randomly generated particles with velocity vectors and boundary bouncing.
  - Mouse interaction to spawn particles, speed control (Up/Down arrows), blinking mode (Spacebar), pause/resume (`p`).

### 🔹 Lab 2: Midpoint Line Drawing Algorithm — *"Catch the Diamonds!"*
- **Concepts**: Generalized 8-zone Midpoint Line Drawing Algorithm using integer-only arithmetic, incremental decision variables, zone conversion and symmetric remapping.
- **Rules**: Zero high-level OpenGL line/polygon primitives allowed (only `GL_POINTS` rendered via custom midpoint line algorithm).
- **Game Features**:
  - Sliding basket/catcher controlled via Left/Right arrow keys.
  - Falling diamond targets with random initial positions and distinct colors.
  - Score counter, game-over detection, and clickable UI buttons (Restart, Play/Pause, Exit).
  - Auto-play Cheat Mode (`c` key).

### 🔹 Lab 3: 3D OpenGL & Hierarchical Transformations — *"Bullet Frenzy"*
- **Concepts**: 3D coordinate system, projection vs modelview matrices, hierarchical matrix stack (`glPushMatrix` / `glPopMatrix`), composite transformations (`glRotatef`, `glTranslatef`, `glScalef`), collision detection in 3D, first-person & third-person camera views.
- **Rules**: Strict adherence to functions provided in `3D_OpenGL_Intro.py` (`glutTimerFunc` disallowed; frame updates handled via `glutIdleFunc`).
- **Game Features**:
  - 3D arena surrounded by bounding walls and checkerboard ground.
  - Player character with rotatable gun facing direction.
  - Autonomous sphere enemies chasing the player in real-time.
  - Projectile firing (cube bullets) with 3D collision detection and health/scoring.
  - Multi-camera system (Free camera, First-person view, Third-person view, Auto-tracking cheat camera).

---

## 🛠️ Getting Started & Installation

### Prerequisites
- Python 3.8+
- OpenGL & GLUT installed on your system
- Python packages:

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

---

## 🚀 Running the Lab Assignments

### Lab 1
```bash
# Basic demos
cd "LAB/Lab1/First Program"
python3 Hello_openGL.py
python3 Lets_draw_sth.py

# Assignments
cd "../Assignment"
python3 Assi1.py    # Task 1: House and Rain
python3 Assi2.py    # Task 2: Bouncing Particles
```

### Lab 2
```bash
cd "LAB/Lab2/Assignment"
python3 Assi1.py    # "Catch the Diamonds!" 2D Game
```

### Lab 3
```bash
cd "LAB/Lab3"
python3 3D_OpenGL_Intro.py   # 3D Template & Transformations demo
python3 Assi3.py             # "Bullet Frenzy" 3D Game
```

---

## 🎮 Controls Quick Reference

### Lab 2: Catch the Diamonds!
| Input | Action |
|---|---|
| `Left Arrow` / `Right Arrow` | Move catcher left / right |
| `Left Click` (Top Buttons) | Restart (`<`) / Pause-Play (`\|\|` / `▶`) / Exit (`✕`) |
| `c` / `C` | Toggle Auto-play cheat mode |

### Lab 3: Bullet Frenzy
| Input | Action |
|---|---|
| `W` / `S` | Move player forward / backward |
| `A` / `D` | Rotate gun left / right |
| `Left Mouse Button` | Fire bullet |
| `Right Mouse Button` | Toggle First-Person / Third-Person view |
| `Up` / `Down` Arrow | Camera pitch / height adjustment |
| `Left` / `Right` Arrow | Camera yaw / orbit |
| `c` / `C` | Toggle Auto-aim & Auto-fire cheat mode |
| `v` / `V` | Follow gun camera mode (in cheat mode) |
| `r` / `R` | Restart game after game over |

---

## ⚠️ macOS Configuration & Native GLUT Fix

On macOS, running PyOpenGL scripts may fail with:
```
freeglut (Assi1.py): failed to open display ''
```
or segmentation faults caused by Homebrew's `freeglut` (which expects an X11 server like XQuartz).

### Solution
Extract the patched `OpenGL` package from `LAB/OpenGL.zip` into the assignment folder to override `darwin.py` and route directly to Apple's native `/System/Library/Frameworks/GLUT.framework/GLUT`:

```bash
cd LAB
unzip -o OpenGL.zip
```

---

## 📖 Study Materials & Past Exam Questions

### 📚 Theory & Viva Guides
- [Lab 2 Understanding Guide](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab2/Assignment2_Understanding.md): Detailed explanation of 8-zone line drawing algorithm, decision variables, and game structure.
- [Lab 3 Understanding Guide](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Assignment3_Understanding.md): 3D math, matrix stacks, transformations, and game architecture.
- [Lab 3 Viva Guide](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Assi3_Viva_Guide.md): Viva questions, conceptual answers, and code walkthroughs.

### 📝 Past Midterm Exams
Located in [`MID questions/`](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/MID%20questions):
- Spring 2025 Midterm Exam
- Summer 2025 Midterm Exam
- Fall 2025 Midterm Exam
- Spring 2026 Midterm Exam

---

For any questions or clarification regarding algorithms, implementations, or guides, refer to the corresponding markdown notes in each lab directory.
