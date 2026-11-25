# Project Overview
[cite_start]Role: Senior XR UX / Unity Take-Home Assessment [cite: 1] for Axon.
[cite_start]Hardware: Oculus Quest 1 (Targeting Android/APK [cite: 34]).
[cite_start]Framework: Unity3D[cite: 50], XR Interaction Toolkit (XRI), OpenXR.
[cite_start]Goal: Build a VR prototype where a user interacts with a security door and successfully passes through it[cite: 3, 7].
[cite_start]Focus: XR interaction design craft [cite: 19][cite_start], systems thinking [cite: 20][cite_start], usability, comfort, and edge cases[cite: 5].

# Code Architecture & Reusability
- [cite_start]Use event-driven architecture to demonstrate "reusable foundations"[cite: 22].
- Create an `InteractableScanner` script that utilizes `UnityEvents` (e.g., `OnScanComplete()`, `OnScanFailed()`, `OnScanProgress()`).
- Wire up the door state, audio, and visual feedback via the Unity Inspector rather than hardcoding dependencies. [cite_start]This demonstrates a strong understanding of technical UX design for cross-functional teams[cite: 16].

# Core Interaction Loop
1. Spawn: User spawns in a small, room-scale space. No locomotion system required (prevents scope creep; desk and door within physical stepping distance).
2. Retrieve Keycard: A security keycard rests on a desk within arm's reach. 
3. Scan Keycard: User grasps the keycard and holds it against a keypad next to the door for 3 seconds.
    - Feedback: A visual circular countdown appears on the keycard. [cite_start]Clear user feedback for success, failure, or invalid interaction[cite: 13].
    - Haptics: Continuous, subtle controller rumble while scanning.
4. [cite_start]State Change[cite: 12]: 
    - [cite_start]Success: Door state changes to Unlocked[cite: 12]. Sign above door changes from Red to Green. Audio plays: "Access Granted."
    - Incomplete: If the card is removed before 3 seconds, the countdown resets and an "Access Denied" buzzer plays.
5. [cite_start]Open Door: User pushes the physical pushbar on the door with their open hands to swing the hinged door open[cite: 9, 10].
    - Haptics: Short rumble upon hand collision with the pushbar.
6. End State: Upon walking through the door threshold, the user enters a small alcove and reads resume content museum-style — World Space panels on the walls (headshot, name, role, education/logos), walking up to each exhibit rather than carrying a tablet.

# Edge Case Handling
- [cite_start]Basic handling for common edge cases[cite: 14].
- "VR Ghosting" (Walking through locked door): If the user's headset camera collider passes through the locked door, trigger a black vignette fade and play a visual/audio warning. Fade to black until they step back.
- Dropped/Lost Keycard: If the keycard falls below the floor line, is thrown out of reach, or is unequipped for more than 10-15 seconds, it automatically respawns at its original position on the desk.
- Pushbar Physics Tunneling: Implement the push interaction using XRI Poke Interactors or simple trigger colliders driving joint limits to prevent the user's hand from violently clipping and breaking the physics simulation.

# Art & Environment Guidelines
- [cite_start]Keep assets simple; primitives and placeholder visuals are completely fine[cite: 52]. 
- [cite_start]Do NOT spend time on high-end art polish [cite: 27] [cite_start]or large environments[cite: 28].
- UI elements (Locked/Unlocked sign, Keycard timer, VR Resume) should be simple World Space canvases that are diegetic and readable in VR.

# Deliverables Checklist
Ensure the final build includes:
- [cite_start]Unity project source repository[cite: 33].
- [cite_start].apk file that runs on consumer hardware[cite: 34].
- [cite_start]A 2-5 minute video walkthrough[cite: 35, 36]. [cite_start]Note any AI-assisted tooling used[cite: 37].
- [cite_start]A brief README [cite: 38] covering: 
    [cite_start]a) Run instructions [cite: 39]
    b) Intended interaction model [cite: 40]
    c) Key design decisions (e.g., UnityEvents for reusability, no artificial locomotion) [cite: 41]
    d) Technical tradeoffs (e.g., using triggers vs heavy rigidbodies for the pushbar) [cite: 42]
    e) Future improvements [cite: 43]