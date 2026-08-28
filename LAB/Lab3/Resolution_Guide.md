# Display Resolution & Screen Compatibility Guide for `Tutul.py`

This guide explains why `Tutul.py` runs on high-resolution displays but fails or gets cut off on lower-resolution screens (like laptops with 1366×768 or Windows displays with 125%/150% scaling), exactly which lines need to be changed, and how to configure different resolutions.

---

## 1. Why Does It Fail on Your Friend's Display?

1. **Window Height Exceeds Screen Boundary (800px vs 768px):**
   - The default window size is **1000×800**.
   - Most standard student laptops have a native resolution of **1366×768** or **1280×720**.
   - With the Windows taskbar and title bar, the maximum usable height on a 768p screen is only ~**720px**. Because the 800px window is taller than the screen, FreeGLUT can fail to create the OpenGL window, crash with a video driver error, or get clipped off the bottom of the screen.

2. **Windows Display Scaling (125% / 150% DPI Scaling):**
   - On 1080p (1920×1080) laptops, Windows often defaults to **125% or 150% scaling**.
   - At 150% scaling, effective vertical space is `1080 / 1.5 = 720px`, which also causes the 800px window to overflow.

3. **Hardcoded Internal Coordinates:**
   - The OpenGL viewport, aspect ratio, 2D HUD projection, and mouse click center are hardcoded to `1000` and `800`. If you only change `glutInitWindowSize` without updating the other lines, the 3D scene gets distorted and mouse clicks in mini-games register in the wrong positions.

---

## 2. Quick Reference: All Lines to Change in `Tutul.py`

There are **5 specific locations** in [Tutul.py](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Tutul.py) that depend on the screen resolution:

| Location / Function | Line No. | Original Code (1000×800) | What It Controls |
| :--- | :--- | :--- | :--- |
| **Window Creation** (`main`) | **Line 2251** | `glutInitWindowSize(1000, 800)` | Physical window size in pixels |
| **OpenGL Viewport** (`showScreen`) | **Line 2229** | `glViewport(0, 0, 1000, 800)` | Area of the window where OpenGL draws |
| **3D Camera Aspect Ratio** (`setupCamera`) | **Line 2170** | `gluPerspective(fovY, 1.25, 0.1, 8000)` | Field-of-view aspect ratio (`Width / Height`) |
| **2D HUD Projection** (`draw_text`) | **Line 395** | `glOrtho(0, 1000, 0, 800, -1, 1)` | 2D coordinate space for on-screen text |
| **Mouse Click Center** (`mouseListener`) | **Lines 1942–1943** | `dx = x - 500`<br>`dy = y - 400` | Center point (`Width/2`, `Height/2`) for mini-game clicks |

---

## 3. Resolution Presets & Exact Values

Choose the preset that matches your friend's display:

### Preset A: 800 × 600 (Recommended for 1366×768 & Small Laptops)
*Guaranteed to fit comfortably on any standard laptop screen with plenty of room for taskbars.*

- **Aspect Ratio:** `800 / 600 = 1.333`
- **Center X / Center Y:** `400 / 300`

```python
# Line 395:
glOrtho(0, 800, 0, 600, -1, 1)

# Lines 1942-1943:
dx = x - 400
dy = y - 300

# Line 2170:
gluPerspective(fovY, 800.0 / 600.0, 0.1, 8000)

# Line 2229:
glViewport(0, 0, 800, 600)

# Line 2251:
glutInitWindowSize(800, 600)
```

---

### Preset B: 960 × 540 (16:9 Compact Widescreen)
*Great for modern widescreen 16:9 displays with high DPI scaling.*

- **Aspect Ratio:** `960 / 540 = 1.778` (16:9)
- **Center X / Center Y:** `480 / 270`

```python
# Line 395:
glOrtho(0, 960, 0, 540, -1, 1)

# Lines 1942-1943:
dx = x - 480
dy = y - 270

# Line 2170:
gluPerspective(fovY, 16.0 / 9.0, 0.1, 8000)

# Line 2229:
glViewport(0, 0, 960, 540)

# Line 2251:
glutInitWindowSize(960, 540)
```

---

### Preset C: 1280 × 720 (Standard HD 720p)
*Standard 720p for full-screen or high-resolution monitors.*

- **Aspect Ratio:** `1280 / 720 = 1.778` (16:9)
- **Center X / Center Y:** `640 / 360`

```python
# Line 395:
glOrtho(0, 1280, 0, 720, -1, 1)

# Lines 1942-1943:
dx = x - 640
dy = y - 360

# Line 2170:
gluPerspective(fovY, 16.0 / 9.0, 0.1, 8000)

# Line 2229:
glViewport(0, 0, 1280, 720)

# Line 2251:
glutInitWindowSize(1280, 720)
```

---

### Preset D: 640 × 480 (Ultra-Low Resolution / Old Hardware)
*For very small screens or legacy virtual machines.*

- **Aspect Ratio:** `640 / 480 = 1.333` (4:3)
- **Center X / Center Y:** `320 / 240`

```python
# Line 395:
glOrtho(0, 640, 0, 480, -1, 1)

# Lines 1942-1943:
dx = x - 320
dy = y - 240

# Line 2170:
gluPerspective(fovY, 4.0 / 3.0, 0.1, 8000)

# Line 2229:
glViewport(0, 0, 640, 480)

# Line 2251:
glutInitWindowSize(640, 480)
```

---

## 4. Best Practice: Make `Tutul.py` Dynamic (One-Line Change in the Future)

Instead of manually editing 5 separate files and lines every time you want to switch resolutions, you can define `WINDOW_WIDTH` and `WINDOW_HEIGHT` at the top of the file:

### Step 1: Add Constants at the Top (around Line 18)
```python
# =========================
# DISPLAY CONSTANTS
# =========================
WINDOW_WIDTH = 800   # Change here (e.g. 800, 960, 1000, 1280)
WINDOW_HEIGHT = 600  # Change here (e.g. 600, 540, 800, 720)
```

### Step 2: Use the Constants Across the Code

1. **In `draw_text()` (Line 395):**
   ```python
   glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
   ```

2. **In `mouseListener()` (Lines 1942–1943):**
   ```python
   dx = x - (WINDOW_WIDTH // 2)
   dy = y - (WINDOW_HEIGHT // 2)
   ```

3. **In `setupCamera()` (Line 2170):**
   ```python
   gluPerspective(fovY, float(WINDOW_WIDTH) / float(WINDOW_HEIGHT), 0.1, 8000)
   ```

4. **In `showScreen()` (Line 2229):**
   ```python
   glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
   ```

5. **In `main()` (Line 2251):**
   ```python
   glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
   ```

With this pattern, whenever you or your friend need to adjust the resolution, you only need to edit **`WINDOW_WIDTH`** and **`WINDOW_HEIGHT`** at the top of the file.

---

## 5. Summary Table for Custom Resolutions

If you want to try any custom resolution $(W, H)$:

| Parameter | Formula / Value |
| :--- | :--- |
| **Window Size** | `glutInitWindowSize(W, H)` |
| **Viewport** | `glViewport(0, 0, W, H)` |
| **Aspect Ratio** | `W / H` (pass into `gluPerspective`) |
| **Ortho 2D Bounds** | `glOrtho(0, W, 0, H, -1, 1)` |
| **Center Offset X** | `W // 2` |
| **Center Offset Y** | `H // 2` |
