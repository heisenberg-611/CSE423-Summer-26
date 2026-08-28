# Cooking Academy 3D — Complete Gameplay & Keybindings Guide

A comprehensive guide explaining all controls, keybindings, kitchen stations, minigames, and a complete step-by-step walkthrough for all 3 Levels in **Cooking Academy 3D** ([Tutul.py](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Tutul.py)).

---

## 1. Quick Controls & Keybindings Reference

| Key / Input | Action / Function | Context / When to Use |
| :--- | :--- | :--- |
| **`W`** | **Move Forward** | Walks forward in the direction the chef is facing |
| **`S`** | **Move Backward** | Walks backward |
| **`A`** | **Turn Left** | Rotates chef counter-clockwise |
| **`D`** | **Turn Right** | Rotates chef clockwise |
| **`E`** or **`Space`** | **Universal Interact / Action** | Pick up items, mix dough, operate oven/stove, assemble ingredients, plate dishes |
| **`Left Mouse Click`** | **Interact / Action** | Same as `E` / `Space` (pick up, interact with station, minigame actions) |
| **`Q`** | **Chop / Cut Knife Action** | Performs knife chop in cutting minigames (Vegetables, Potato Strips, Sausage) |
| **`F`** or **`Right Click`** | **Toggle Camera View** | Switches between **First-Person (Chef POV)** and **Third-Person** camera |
| **`R`** | **Remove Wrong Ingredients** | Discards wrong/unwanted items from your 3-slot inventory |
| **`1`** | **Restart / Reset Game** | Resets game, scores, stations, and inventory back to Level 1 |
| **`2`** | **Start Level 2** | Starts Level 2 (Burger & Fries) when Level 1 is cleared |
| **`3`** | **Start Level 3** | Starts Level 3 (Pizza Preparation) when Level 2 is cleared |
| **`Arrow Up / Down`** | **Camera Height** | Raises / lowers camera height in Third-Person mode |
| **`Arrow Left / Right`** | **Camera Orbit Yaw** | Orbits camera angle around the chef in Third-Person mode |
| **`Arrow Keys` / `WASD`** | **Frying Direction Input** | Selects direction (`↑`, `↓`, `←`, `→`) in Level 2 French Fries Frying minigame |

---

## 2. Kitchen Stations Map & Overview

The kitchen consists of several interactive stations arranged around the room:

```
                  [ Customer Counter (0, 2000) ]
                                |
[ Prep Table (-2000, 0) ]       |        [ Plating Station (2000, 0) ]
                                |
[ Storage Table (-2000, -1000) ]|        [ Oven Station (2000, -1000) ]
                                |
[ Cutting Station (-1000, -2000)]        [ Mixing Station (2000, -2000) ]
                \                               /
                 [ Stove Station (0, -2000) ]
```

- **Storage Table:** Contains raw ingredients (Tomato, Cucumber, Carrot, Potato, Sausage, Patty, Buns, Cheese).
- **Cutting Station:** Wooden cutting board with an animated chef knife for chopping.
- **Stove Station:** 2 red pans & a cooking pot for boiling potatoes, 4-direction frying, and patty frying.
- **Mixing Station:** Mixing bowl with animated dough paddle.
- **Prep Table:** Assembly table for Level 2 Burger layering and Level 3 Pizza toppings.
- **Oven Station:** 3D animated baking oven with transparent glass door.
- **Plating Station:** Final serving counter to place completed dishes.

---

## 3. Step-by-Step Level Walkthrough

---

### Level 1: Fresh Salad Preparation

#### Step 1: Collect Required Ingredients
1. Walk to the **Storage Table** using `W/A/S/D`.
2. Stand near the floating 3D ingredients:
   - **Tomato** (Red sphere)
   - **Cucumber** (Green cylinder)
   - **Carrot** (Orange cylinder)
3. Press **`E`** (or **Left Click**) to pick them up.
4. *Tip:* Avoid collecting wrong items (like Cheese or Egg). If you collect a wrong item, press **`R`** to remove it.
5. Once all 3 required vegetables are in your inventory, the **Cutting Station UNLOCKS** (+20 pts bonus).

#### Step 2: Chop Vegetables at Cutting Station
1. Walk to the **Cutting Station** (`(-1000, -2000)`).
2. Press **`E`** or **Left Click** to enter the cutting camera view.
3. Rapidly tap **`Q`** to chop:
   - 3 cuts for Tomato (+15 pts)
   - 3 cuts for Cucumber (+15 pts)
   - 3 cuts for Carrot (+15 pts)
4. When finished (+20 pts bonus), the camera automatically returns to normal view and the **Plating Station UNLOCKS**.

#### Step 3: Plating the Salad
1. Walk over to the **Plating Station** (`(2000, 0)`).
2. Press **`E`** or **Left Click** **3 times** to plate all chopped salad portions (+35 pts).
3. **Level 1 Complete!** Press **`2`** to start Level 2.

---

### Level 2: Burger & French Fries Preparation

#### Step 1: Prepare the French Fries
1. Walk to Storage Table and collect the **Potato**.
2. Go to the **Cutting Station**, press **`E`** or **Left Click** to begin cutting, then press **`Q`** 4 times to cut into strips (+35 pts).
3. Walk to the **Stove Station** and press **`E`** / **Left Click** on the pot to boil the potato strips.
4. Watch the boiling progress reach **100%** (+20 pts).
5. Press **`E`** / **Left Click** on the frying pan to start the **4-Direction Frying Minigame**:
   - An on-screen target direction (`↑`, `→`, `↓`, `←`) will appear.
   - Hit the matching direction using **Arrow Keys**, **`W/A/S/D`**, or **Mouse Clicks** on the screen!
   - Successfully complete 6 directions (+35 pts).

#### Step 2: Fry the Burger Patty
1. Walk to Storage and collect the **Frozen Patty**.
2. Go to the **Stove Station** and press **`E`** / **Left Click** to place the patty on the frying pan.
3. **Watch the frying percentage meter on the HUD:**
   - **0% – 59% (Undercooked):** Do not remove yet (-10 pts penalty if removed early).
   - **60% – 115% (PERFECT COOKED SWEET SPOT):** Press **`E`** or **Left Click** to remove the patty safely (+25 pts)!
   - **>115% (BURNT):** If you wait too long, the patty burns (-20 pts penalty and must retry).

#### Step 3: Burger Assembly (First-Person Prep Minigame)
1. After Patty and Fries are ready, collect the assembly ingredients from Storage:
   - **Bottom Bun**, **Cheese**, **Tomato**, **Cucumber**, **Top Bun**.
2. Walk to the **Prep Table** (`(-2000, 0)`) and press **`E`** / **Left Click** to enter First-Person Assembly view.
3. Assemble in the exact order shown on the HUD checklist:
   1. Bottom Bun
   2. Cooked Patty
   3. Cheese Slice
   4. Tomato Slice
   5. Cucumber Slice
   6. Top Bun
4. Look directly at each ingredient on the table and press **`E`** or **Left Click** to place it (+10 pts per step, +30 pts bonus).

#### Step 4: Plate Burger & Fries
1. Walk to the **Plating Station** (`(2000, 0)`).
2. Press **`E`** / **Left Click** to plate the Burger (+15 pts).
3. Press **`E`** / **Left Click** to plate the French Fries (+15 pts).
4. **Level 2 Complete!** (+30 bonus pts). Press **`3`** to start Level 3.

---

### Level 3: Gourmet Pizza Preparation

#### Step 1: Sausage Cutting
1. Walk to Storage Table and collect the **Sausage**.
2. Go to the **Cutting Station**, press **`E`** / **Left Click** to enter cutting view, and press **`Q`** 4 times to chop the sausage into slices (+40 pts).

#### Step 2: Dough Making
1. Walk to the **Mixing Station** (`(2000, -2000)`).
2. Press **`E`** or **Left Click** **5 times** to mix the dough in the bowl (+5 pts per mix, +25 pts bonus when done).

#### Step 3: Pizza Topping Assembly
1. Walk to the **Prep Table** (`(-2000, 0)`).
2. Press **`E`** or **Left Click** to apply toppings in order:
   - **1st Click:** Apply Tomato Sauce (+10 pts)
   - **2nd Click:** Apply Cheese (+10 pts)
   - **3rd Click:** Place Cut Sausage slices (+35 pts)
3. Raw Pizza is now fully prepared!

#### Step 4: Bake Pizza in the Oven
1. Walk to the **Oven Station** (`(2000, -1000)`).
2. Press **`E`** or **Left Click** to put the raw pizza inside the oven.
3. The oven lights up, glowing coals heat up, and the baking progress starts counting from 0% to 150%.
4. **Watch the Baking Timer on the HUD:**
   - **0% – 59% (Undercooked):** Do not remove (-10 pts penalty).
   - **60% – 115% (GOLDEN BAKED READY):** Press **`E`** or **Left Click** to pull out the freshly baked pizza (+30 pts)!
   - **>115% (BURNT):** Pizza burns (-20 pts penalty and must retry).
5. **Level 3 Complete! GAME VICTORY!**

---

## 4. Scoring & Penalty Rules

| Action | Score Change |
| :--- | :--- |
| Collecting Correct Ingredient | **+1 pt** |
| Collecting Wrong Ingredient | **-1 pt** |
| All Required Ingredients Collected Bonus | **+20 pts** |
| Individual Knife Chop (`Q`) | **+5 pts** |
| Stage Completion Bonus (Chopping / Mixing) | **+20 to +25 pts** |
| Perfect Patty Frying (60%–115%) | **+25 pts** |
| Perfect Pizza Baking (60%–115%) | **+30 pts** |
| Undercooked Penalty (<60%) | **-10 pts** |
| Burnt Penalty (>115%) | **-20 pts** |
| Level Clear Bonus | **+30 pts** |

---

## 5. Pro Tips for High Score

1. **Use `E` for Smooth Movement:** Keep your left hand on `W/A/S/D` and tap `E` with your index finger to interact with stations seamlessly without reaching for the mouse.
2. **Toggle Camera (`F`):** Use Third-Person mode for navigating between stations, and First-Person mode (`F`) when aligning items at the prep table.
3. **Timer Management:** While the Potato Strips are boiling at the stove, you can walk over and prepare other tasks.
4. **Inventory Full?** If you accidentally pick up unnecessary items, press **`R`** to immediately clean out your inventory slots.
5. **Adjust Display Resolution:** If the window is too large or small for your screen, open [Tutul.py](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Tutul.py#L20-L21) and change `WINDOW_WIDTH` and `WINDOW_HEIGHT` at lines 20–21 (see [Resolution_Guide.md](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Resolution_Guide.md)).
