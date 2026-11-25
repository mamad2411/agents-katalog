---
name: unity-architecture-and-best-practices
description: Master orchestrator for designing scalable systems in Unity. Use ALWAYS when creating new systems, refactoring code, or structuring complex mechanics. Enforces SOLID principles and strict decoupling.
---

# Skill: Unity Architecture & Clean Code

The master orchestrator for designing scalable systems in Unity. Use ALWAYS when the user asks to create a new system, refactor code, or structure complex mechanics. This skill ensures the project does not turn into "spaghetti code" by applying SOLID principles and strict decoupling from the very first sketch.

## 🛑 Negative Constraints (When NOT to use)
*   Do not use for simple syntax fixes (missing semicolons, etc.).
*   Do not use for purely aesthetic changes that don't involve component logic.
*   Do not use if the user explicitly requests a "dirty" quick fix and has rejected pro architecture after being warned (respect their decision, but warn once).

---

## ⚖️ The Iron Laws of Architecture

As an AI agent, you are FORBIDDEN from writing code without first validating these architectural rules:

1. **Simulation vs. Presentation:** Keep business/data logic strictly separate from visual representation (VFX, Animations, Audio, UI). A `Health.cs` script should know nothing about the blood particle system.

2. **Death to God Classes:** Forbidden to create monolithic scripts (e.g., a `PlayerController.cs` handling input, physics, animations, and audio). Apply the Single Responsibility Principle (SRP). Break into small, composable components.

3. **Decoupling by Default:** Minimize direct references between independent systems. Prefer Events (C# Events, UnityEvents), the Observer Pattern, or ScriptableObject-based architecture for communication. Use Singletons (`public static Instance`) only for strictly necessary global Managers.

4. **Performance-First Design:** Avoid architectures that generate garbage (GC.Alloc) in `Update`. Promote Object Pooling for frequently instantiated objects and use Non-Allocating APIs/collections.

---

## 🏗️ Architectural Design Phases

Guide the user through these 4 phases before writing the final code implementation.

### Phase 1: Requirements and Scope Gathering
Understand what the system must do within the context of the full game.
* What are the system's inputs and outputs?
* Which other systems does it need to talk to?
* Is it scene-specific or persistent across the entire game?

### Phase 2: Component Design and Decoupling
Propose a component structure. Explain the separation before writing code.
* Define which script handles Data, Logic (Controller), and Visual Feedback (View).
* Define communication (e.g., *"Health.cs will emit an OnDamageTaken event, and VFXManager.cs will listen to it"*).

### Phase 3: Design Pattern Selection
Evaluate if a standard pattern solves the problem cleanly.
* Mention if a *State Machine* (for AI/Player states), a *Factory/Object Pool* (for projectiles), or a *Strategy Pattern* (for weapon types) applies.

### Phase 4: Interface and Skeleton Proposal
Present class signatures, interfaces, and exposed variables (`[SerializeField]`).
* Let the user review the structure. Once approved, generate the detailed implementation.

---

## 🗂️ Sub-module Routing

Apply specific rules from these sub-modules based on the context:

* **[01-planning-and-workflow.md]:** Task planning, version control, and rapid prototyping (Grayboxing).
* **[02-clean-code-and-conventions.md]:** Naming conventions, access modifiers, and encapsulation (Structs vs Classes).
* **[03-core-design-patterns.md]:** State Machines, Observers, Event Channels (ScriptableObjects), and Factories.
* **[04-modular-systems-and-glue-code.md]:** Connecting components without spaghetti, explicit dependencies (`[RequireComponent]`).
* **[05-ui-and-presentation-architecture.md]:** Decoupling game logic from menus (MVP/MVC) using UGUI or UI Toolkit.
* **[06-combat-and-vfx-decoupling.md]:** Action mechanics, hitboxes, FixedUpdate determinism, and safe animation triggers.
* **[07-performance-coding-patterns.md]:** Efficient micro-architecture: avoiding GetComponent in Update, caching, and non-allocating APIs.

---

## 🛠️ Audit Tools & Scaffolding (Executable Scripts)

As a Software Architect, NEVER blindly trust legacy or freshly written code. You have EXPLICIT PERMISSION to run these diagnostic tools in the terminal:

1. **Clean Code "Police" (`unity-doctor.js`)**
   * **When:** BEFORE proposing performance refactors or during Code Reviews.
   * **Command:** `node framework/execution/unity-doctor.js` (Note: adjust path if needed).
   * **Action:** Analyzes for "God Classes", Update-loop allocations, and UI Toolkit violations.

2. **Architecture Scaffolder (`scaffold_repo.py`)**
   * **When:** At project start or when organizing `Assets/`.
   * **Command:** `python framework/execution/scaffold_repo.py`
   * **Action:** Creates the mandatory folder structure (Core, Gameplay, UI, etc.) in `Assets/_Project/`.

3. **Package & Security Auditor (`package-audit.js`)**
   * **When:** Importing 3rd-party assets or fixing rendering issues (Pink Shaders).
   * **Command:** `node framework/execution/package-audit.js`

## 🛑 STRICT SYSTEM DIRECTIVE

WHEN THE USER REQUESTS A NEW SYSTEM, YOUR FIRST RESPONSE MUST NOT BE THE COMPLETE CODE. IT MUST BE AN ARCHITECTURAL BREAKDOWN (PHASES 1, 2, AND 3) EXPLAINING THE "WHY" BEHIND EACH DECISION. ONLY WHEN THE USER VALIDATES THE APPROACH SHOULD YOU GENERATE SCRIPTS. THIS PREVENTS TECHNICAL DEBT.