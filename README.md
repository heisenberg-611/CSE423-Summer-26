# CSE423 - Computer Graphics Lab

This repository contains the lab work and assignments for **CSE423: Computer Graphics** (8th Semester at BRACU).

## 📁 Directory Structure

```
CSE423/
└── LAB/
    └── Lab1/
        ├── CSE423_OpenGL_Lab_Reference.ipynb    # Lab reference notebook with OpenGL concepts
        ├── Assignment/                         # Assignment code and related files
        │   ├── Assi1_explained.py              # Assignment 1 explained version
        │   ├── Assi1.py                        # Assignment 1 solution code
        │   ├── Assi2_explained.py              # Assignment 2 explained version
        │   ├── Assi2.py                        # Assignment 2 solution code
        │   └── OpenGL/                         # Local Python OpenGL bindings and helper files
        └── First Program/                      # Initial OpenGL example programs
            ├── Hello_openGL.py                 # Basic OpenGL setup program
            ├── Lets_draw_sth.py                # Drawing shapes with OpenGL
            └── OpenGL/                         # Local Python OpenGL bindings and helper files
```

## 🎯 Course Overview

This lab covers fundamentals of **Computer Graphics** using Python and OpenGL. Key topics include:
- OpenGL initialization and rendering pipeline
- 2D/3D coordinate systems and transformations
- Drawing primitives and shapes
- Event handling and interactive rendering
- Python OpenGL bindings with PyOpenGL

## 🛠️ Getting Started

### Prerequisites
- Python 3.x
- OpenGL support on your system
- Python packages: `PyOpenGL`, `PyOpenGL_accelerate` (optional but recommended)

Install the required packages with:

```bash
python3 -m pip install PyOpenGL PyOpenGL_accelerate
```

### Running the Example Programs

1. Change into the example folder:
   ```bash
   cd LAB/Lab1/First\ Program/
   ```

2. Run an example:
   ```bash
   python3 Hello_openGL.py
   python3 Lets_draw_sth.py
   ```

### Running Assignment Code

1. Change into the assignment folder:
   ```bash
   cd LAB/Lab1/Assignment/
   ```

2. Run an assignment script:
   ```bash
   python3 Assi1.py
   python3 Assi2.py
   ```

## ⚠️ macOS Specific Configuration

If you are running these scripts on macOS, you might encounter the following error:

```
freeglut (Assi1.py): failed to open display ''
```

This happens because PyOpenGL defaults to finding Homebrew's `freeglut` (which relies on X11) instead of Apple's native `GLUT.framework`.

### Solution

The repository includes a **patched `OpenGL` library** that resolves this issue without requiring XQuartz or modifying system packages. The local `OpenGL/` folders (present in both `Lab1/Assignment/` and `Lab1/First Program/` directories) override the library loader in `OpenGL/platform/darwin.py` to prioritize the native macOS `/System/Library/Frameworks/GLUT.framework/GLUT`.

**No additional setup is required** — simply ensure the patched `OpenGL` folder is present in the same directory as your assignment scripts. If the `OpenGL` folder is missing for any reason, it can be extracted from **`OpenGL.zip`** (located at the root directory).

```bash
# Only run this if OpenGL/ folder is missing
unzip OpenGL.zip
```

### Running on macOS

Once the `OpenGL` folder is in place, run the scripts normally:

```bash
cd LAB/Lab1/Assignment/
python3 Assi1.py
python3 Assi2.py
```

## 📚 Resources

- `CSE423_OpenGL_Lab_Reference.ipynb`: Detailed lab reference with explanations and examples
- `Assi1.py`, `Assi2.py`: Assignment solutions
- `Assi1_explained.py`, `Assi2_explained.py`: Annotated versions with explanations
- `Hello_openGL.py`, `Lets_draw_sth.py`: Basic OpenGL demo programs

## 📝 Notes

- The `OpenGL/` folders contain Python OpenGL bindings included with the lab files.
- If you already have a system-wide PyOpenGL install, these local `OpenGL/` directories can often be ignored.


---

For any issues or questions, refer to the course materials and lab documentation.
