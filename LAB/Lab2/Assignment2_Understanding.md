# Assignment 2: Catch the Diamonds! (OpenGL)

## 🎮 Core Objective
Develop a 2D OpenGL game called **"Catch the Diamonds!"** in Python. The most critical requirement is that **everything** on the screen (the diamonds, the catcher, and the UI buttons) must be drawn using the **Midpoint Line Drawing Algorithm** using only the `GL_POINTS` primitive. 

## 📐 Part 1: The Midpoint Line Algorithm (50% of the grade)
You cannot just use standard OpenGL line functions (`GL_LINES`). You must implement your own line drawing:
1. **Base Algorithm:** Implement the Midpoint Line Algorithm, which natively only works for lines in **Zone 0** (lines going from left to right with a slope between 0 and 1).
2. **8-Way Symmetry:** You must extend your algorithm to draw lines in **any of the 8 zones**. 
   - Write a function `FindZone(x1, y1, x2, y2)` to find which zone a line belongs to.
   - Before drawing, convert the line's coordinates to Zone 0.
   - Run the Zone 0 Midpoint algorithm.
   - Convert the calculated intermediate points *back* to their original zone before plotting them on the screen.

*(Note: If you build the game but don't implement the Midpoint Line drawing, you will get a 0 for the assignment.)*

## 🕹️ Part 2: The Game "Catch the Diamonds!" (50% of the grade)
Here are the gameplay mechanics and rules you need to implement:
* **The Catcher:** Located at the bottom. Move it left and right using the **arrow keys**. Make sure it doesn't go off-screen.
* **The Diamonds:** 
  * Fall from the top of the screen at random horizontal positions.
  * Must have randomized, bright colors.
  * Speed should gradually increase over time to make the game harder.
* **Scoring & Game Over:** 
  * Catching a diamond (collision) increases your score by 1 and spawns a new diamond. Print the score to the console.
  * Missing a diamond results in a Game Over. The catcher should turn red, everything stops falling, and you print "Game Over" with the final score to the console.
* **Collision Detection:** You are recommended to use the **AABB (Axis-Aligned Bounding Box)** algorithm to detect when the catcher and the diamond intersect.

## 🎛️ Part 3: UI Buttons and Modes
At the top of the screen, you need to draw three interactive buttons (again, drawn using your Midpoint Line algorithm):
1. **Left Arrow (Teal):** Restarts the game, resetting the score, speed, and diamond position.
2. **Play/Pause (Amber):** Toggles the game state. When paused, the diamond freezes and the catcher cannot move. The icon must change depending on the state (Play vs. Pause).
3. **Cross (Red):** Exits the game cleanly using `glutLeaveMainLoop()` and prints "Goodbye" with the final score.

* **Cheat Mode:** If the user presses **'c'**, the game enters cheat mode where the catcher automatically tracks and catches the diamond without missing. It must physically move left/right to catch it, not just teleport. Pressing 'c' again disables it.

## ⚠️ Important Restrictions & Tips
* **Strict OpenGL Functions:** You are only allowed to use OpenGL functions that were shown in your previous lab's demo files. Using unauthorized functions will result in a **-50% penalty**.
* **Delta Time:** To ensure the game runs at the same speed on different computers, it is highly recommended to use **Delta Time** (time elapsed between frames using Python's `time` module) to calculate movement, rather than blindly adding constant values to coordinates.
