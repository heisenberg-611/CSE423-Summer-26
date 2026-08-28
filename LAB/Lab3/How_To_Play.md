# Cooking Academy 3D — Complete Gameplay & Keybindings Guide

A comprehensive guide explaining all controls, keybindings, kitchen stations, minigames, cooking timers, and a complete step-by-step walkthrough for all 3 Levels in **Cooking Academy 3D** ([Tutul.py](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Tutul.py)).

---

## 1. Quick Controls & Keybindings Reference

| Key / Input | Action / Function | Context / When to Use |
| :--- | :--- | :--- |
| **`W`** | **Move Forward** | Walks forward along the chef's facing direction vector |
| **`S`** | **Move Backward** | Walks backward |
| **`A`** | **Turn Left** | Rotates chef counter-clockwise |
| **`D`** | **Turn Right** | Rotates chef clockwise |
| **`E`** or **`Space`** | **Universal Interact / Action** | Pick up items, mix dough, operate fryer/stove/oven, assemble ingredients, plate dishes |
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

Every kitchen station features **high-contrast 3D nameplates with golden trim** and **dynamic live floating timer badges** visible from anywhere in the kitchen:

```
                            [ Customer Counter (0, 2000) ]
                                          |
[ Prep Table (-2000, 0) ]                 |               [ Plating Station (2000, 0) ]
                                          |
[ Storage Table (-2000, -1000) ]          |               [ Baking Oven (2000, -1000) ]
                                          |
[ Cutting Station (-1000, -2000) ]        |               [ Mixing Station (2000, -2000) ]
               \                          |                        /
        [ Stove Station (0, -2000) ] ---------- [ Deep Fryer (1000, -2000) ]
```

### Station Functions:
- **Storage Table `(-2000, -1000)`:** Contains persistent crates with 3D ingredient models and crisp floating name tags (`Frozen Patty`, `Tomato`, `Onion`, `Carrot`, `Sausage`, `Potato`, `Bun`, `Cheese`, `Cucumber`).
- **Cutting Station `(-1000, -2000)`:** Bamboo chopping board with animated chef knife for slicing vegetables, potato strips, and sausage.
- **Stove Station `(0, -2000)`:** 4-burner stovetop with a stainless-steel pot for **Potato Boiling** and a frying pan for **Patty Frying**.
- **Deep Fryer `(1000, -2000)`:** Commercial twin-basket deep fryer with bubbling hot oil and steam for **French Fries Deep Frying**.
- **Mixing Station `(2000, -2000)`:** Stainless steel mixing bowl with animated electric paddle for Level 3 pizza dough kneading.
- **Prep Table `(-2000, 0)`:** Stainless prep table with cutting mats for Level 2 **Burger Assembly** and Level 3 **Pizza Toppings**.
- **Baking Oven `(2000, -1000)`:** Heavy commercial pizza oven with glowing heating interior and glass window.
- **Plating Station `(2000, 0)`:** Porcelain serving platters and garnish cutting boards to present completed dishes.

---

## 3. Cooking Timers & Sweet-Spot Mechanics

Cooking in **Cooking Academy 3D** uses real-time continuous timers with sweet-spot timing:

| Station / Food | Timer Duration | Undercooked Penalty (<60%) | Perfect Sweet Spot (60%–115%) | Burnt Penalty (>115%) |
| :--- | :--- | :--- | :--- | :--- |
| **Stove Pot (Boiling Potato)** | **6.0 Seconds** | Strips remain raw in water | Automatically finishes at 100% (+20 pts) | N/A |
| **Stove Pan (Patty Frying)** | **8.0 Seconds** | **-10 pts** (4.8s / undercooked) | **+25 pts** (4.8s – 9.2s / perfectly seared) | **-20 pts** (patty incinerated) |
| **Deep Fryer (French Fries)** | **7.0 Seconds** | **-10 pts** (4.2s / soggy strips) | **+35 pts** (4.2s – 8.0s / crispy golden fries) | **-20 pts** (fries burnt to crisp) |
| **Baking Oven (Pizza Baking)**| **8.0 Seconds** | **-10 pts** (4.8s / raw dough) | **+30 pts** (4.8s – 9.2s / bubbly crust & melted cheese) | **-20 pts** (pizza burnt) |

> [!TIP]
> **Live Floating 3D Badges:** While cooking, live timer badges float directly above the cooking stations (e.g. `PATTY FRYING: 65% (5.2s / 8.0s)` or `FRYER SIZZLING: 72% (5.0s / 7.0s)`), and the HUD displays real-time seconds remaining!

---

## 4. Step-by-Step Level Walkthrough

---

### Level 1: Fresh Salad Preparation

#### Step 1: Collect Required Ingredients
1. Walk to the **Storage Table** using `W/A/S/D`.
2. Pick up the 3 required ingredients by pressing **`E`** (or **Left Click**):
   - **Tomato** (Red sphere)
   - **Cucumber** (Green cylinder)
   - **Carrot** (Orange cylinder)
3. *Tip:* Avoid collecting wrong items (like Onion). If you pick up a wrong item, press **`R`** to discard it.
4. Once all 3 required vegetables are collected, the **Cutting Station UNLOCKS** (+20 pts bonus).

#### Step 2: Chop Vegetables at Cutting Station
1. Walk to the **Cutting Station** (`(-1000, -2000)`).
2. Press **`E`** or **Left Click** to enter cutting view.
3. Press **`Q`** repeatedly to chop:
   - 3 cuts for Tomato (+15 pts)
   - 3 cuts for Cucumber (+15 pts)
   - 3 cuts for Carrot (+15 pts)
4. When all vegetables are sliced (+20 pts bonus), camera returns to normal and the **Plating Station UNLOCKS**.

#### Step 3: Plating the Salad
1. Walk to the **Plating Station** (`(2000, 0)`).
2. Press **`E`** or **Left Click** **3 times** to plate the salad portions (+35 pts).
3. **Level 1 Complete!** Press **`2`** to start Level 2.

---

### Level 2: Burger & French Fries Preparation

#### Step 1: Prepare the French Fries
1. Collect the **Potato** from the Storage Table.
2. Go to the **Cutting Station**, press **`E`** / **Left Click** to enter cutting view, then press **`Q`** 4 times to cut into strips (+35 pts).
3. Walk to the **Stove Station** (`(0, -2000)`) and press **`E`** / **Left Click** on the pot to boil the strips.
4. Watch the pot boil to **100%** / 6.0s (+20 pts).
5. Carry the boiled strips to the **Deep Fryer** (`(1000, -2000)`) and press **`E`** / **Left Click** to start deep frying:
   - Hot oil bubbles and steam rises as the **7.0s Frying Timer** starts ticking.
   - Play the **Frying Direction Mini-Game**: press matching **Arrow Keys** (`↑`, `→`, `↓`, `←`), **WASD**, or click the screen to keep quality at 100%.
   - When the timer reaches the **60% – 115% sweet spot** (4.2s – 8.0s), press **`E`** or **Left Click** to lift the golden crispy fries out (+35 pts)!

#### Step 2: Fry the Burger Patty
1. Collect the **Frozen Patty** from the Storage Table.
2. Go to the **Stove Station** (`(0, -2000)`) and press **`E`** / **Left Click** to place the patty into the frying pan.
3. Watch the pan sizzle with steam as the **8.0s Patty Timer** ticks:
   - **0% – 59% (Undercooked):** Leave it on the pan.
   - **60% – 115% (PERFECT SWEET SPOT / 4.8s – 9.2s):** Press **`E`** or **Left Click** to pull the cooked patty (+25 pts)!
   - **>115% (BURNT):** Patty burns to ash (-20 pts penalty; collect a new patty).

#### Step 3: Burger Assembly
1. Collect burger ingredients from Storage Table:
   - **Bottom Bun**, **Cheese**, **Tomato**, **Cucumber**, **Top Bun**.
2. Walk to the **Prep Table** (`(-2000, 0)`) and press **`E`** / **Left Click** to begin assembly.
3. Assemble in the exact order shown on the HUD checklist:
   1. Bottom Bun
   2. Cooked Patty
   3. Cheese Slice
   4. Tomato Slice
   5. Cucumber Slice
   6. Top Bun
4. Look at each ingredient on the table and press **`E`** / **Left Click** to stack it (+10 pts per step, +30 pts bonus).

#### Step 4: Plate Burger & Fries
1. Walk to the **Plating Station** (`(2000, 0)`).
2. Press **`E`** / **Left Click** to plate the Burger (+15 pts).
3. Press **`E`** / **Left Click** to plate the French Fries (+15 pts).
4. **Level 2 Complete!** (+30 bonus pts). Press **`3`** to start Level 3.

---

### Level 3: Gourmet Pizza Preparation

#### Step 1: Sausage Slicing
1. Collect the **Sausage** from the Storage Table.
2. Go to the **Cutting Station**, press **`E`** / **Left Click** to enter cutting view, and press **`Q`** 4 times to slice the sausage (+40 pts).

#### Step 2: Dough Mixing
1. Walk to the **Mixing Station** (`(2000, -2000)`).
2. Press **`E`** or **Left Click** **5 times** to mix the dough in the electric bowl (+5 pts per mix, +25 pts bonus when done).

#### Step 3: Pizza Topping Assembly
1. Walk to the **Prep Table** (`(-2000, 0)`).
2. Press **`E`** or **Left Click** to apply toppings:
   - **1st Click:** Apply Tomato Sauce (+10 pts)
   - **2nd Click:** Apply Cheese (+10 pts)
   - **3rd Click:** Scatter Sliced Sausage (+35 pts)
3. Raw Gourmet Pizza is now prepared!

#### Step 4: Bake Pizza in the Oven
1. Walk to the **Baking Oven** (`(2000, -1000)`).
2. Press **`E`** or **Left Click** to slide the raw pizza inside.
3. The oven glows bright orange as the **8.0s Baking Timer** starts:
   - **0% – 59% (Raw):** Leave in oven.
   - **60% – 115% (GOLDEN BAKED READY / 4.8s – 9.2s):** Press **`E`** or **Left Click** to remove the bubbly pizza (+30 pts)!
   - **>115% (BURNT):** Pizza burns to charcoal (-20 pts penalty).
4. **Level 3 Complete! CONGRATULATIONS CHEF — GAME VICTORY!**

---

## 5. Scoring & Penalty Table

| Action | Score Change |
| :--- | :--- |
| Collecting Correct Ingredient | **+1 pt** |
| Collecting Wrong Ingredient | **-1 pt** |
| All Required Ingredients Collected Bonus | **+20 pts** |
| Individual Knife Chop (`Q`) | **+5 pts** |
| Stage Completion Bonus (Chopping / Mixing) | **+20 to +25 pts** |
| Boiling Potato Strips (100% / 6.0s) | **+20 pts** |
| Perfect Patty Frying (60%–115% / 4.8s–9.2s) | **+25 pts** |
| Crispy French Fries Deep Frying (60%–115% / 4.2s–8.0s) | **+35 pts** |
| Perfect Pizza Baking (60%–115% / 4.8s–9.2s) | **+30 pts** |
| Undercooked Early Removal Penalty (<60%) | **-10 pts** |
| Burnt Food Overcooked Penalty (>115%) | **-20 pts** |
| Level Clear Bonus | **+30 pts** |

---

## 6. Pro Tips for High Score

1. **Use `E` / `Space` for Rapid Kitchen Navigation:** Keep your left hand over `W/A/S/D` and tap `E` with your index finger or `Space` with your thumb to interact with stations effortlessly without reaching for the mouse.
2. **Watch the 3D Live Timer Badges:** Check the real-time badges floating over the Deep Fryer, Stove, and Oven to multitask across stations without burning your food.
3. **Toggle First-Person (`F`):** Use Third-Person for moving around the kitchen, and press `F` for immersive First-Person view when chopping, frying, and assembling.
4. **Clean Inventory Fast (`R`):** If you accidentally pick up unneeded items, tap **`R`** to clear wrong items instantly.
5. **Screen Resolution:** If the window is too large or small for your screen, adjust `WINDOW_WIDTH` and `WINDOW_HEIGHT` at the top of [Tutul.py](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Tutul.py#L20-L21) (see [Resolution_Guide.md](file:///Users/dhrubojyoti/Documents/Media/Books/BRACU/8th%20Semester/CSE423/LAB/Lab3/Resolution_Guide.md)).
