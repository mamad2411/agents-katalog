---
name: unity-systematic-debugging
description: The definitive framework for resolving bugs, exceptions, and bottlenecks in Unity. Use ALWAYS when unexpected behavior, console errors, or FPS drops are reported. Enforces the scientific method.
---

# Skill: Unity Systematic Debugging

The definitive framework for resolving bugs, exceptions, and bottlenecks in Unity. Use ALWAYS whenever the user reports unexpected behavior, console errors, or FPS drops—even if they don't explicitly ask for technical help. This skill prevents superficial fixes and ensures the root cause is found before writing a single line of solution code.

---

## ⚖️ The Iron Laws

As an AI agent, you are FORBIDDEN from breaking these rules during a Unity debugging session:

1. **Zero Tolerance for "Witch Doctor Debugging":** NEVER propose "blind fixes" or guess-and-check. If you do not understand the root cause, your response must be a question or an experiment to uncover it.
2. **Code is only 50% of the truth:** Never assume the state of a `GameObject` based only on the `.cs` script. Unity bugs often live in the Inspector, execution order, corrupted Prefabs, or ScriptableObjects. Always ask to verify the environment.
3. **Strict Scientific Method:** You must formulate an explanatory hypothesis and propose an experiment (test) that validates or invalidates said hypothesis before writing any solution code.
4. **Mandatory Human Validation:** AI-generated patches require human validation against the domain's business logic. Force the user to confirm the results of empirical tests.

---

## 🔬 Systematic Debugging Phases

Guide the user through these phases in strict order. Omitting data in early phases guarantees failure.

### Phase 0: Feedback Loop and Persistent Context

Before theorizing, we must know if the ground is solid. **Without a fast, deterministic feedback loop, looking at code is useless.**

* **Build the Feedback Loop:** Require the user to isolate the problem. Can a Test Scene be created where the bug occurs in under 5 seconds? Can it be reproduced via a `[ContextMenu]` button in the Inspector?
* **Verify Reproducibility:** Does the bug occur 100% of the time in the loop? If it is intermittent, forbid code changes and prioritize increasing the reproduction rate.
* **Persistent Debug Log:** Create or update a `debug_report.md` on disk. Record every failed experiment and every confirmed data point. This prevents "forgetting" progress across long sessions.

### Phase 1: Problem Definition and "Is / Is Not" Analysis

The goal is not to guess what's failing, but to isolate the problem space by establishing clear boundaries.

* **Identify the Exact Symptom:** Ask for the full stack trace, visual behavior, or performance metric (e.g., FPS, GC Alloc).
* **Apply "Is/Is Not" Analysis:**
  * *Where* does it occur vs. *Where not* (e.g., specific level or all levels?).
  * *When* does it happen vs. *When not* (e.g., in `Awake` or on collision?).
  * *Execution Context:* Editor, Play Mode, or a Build (Mono vs. IL2CPP)?

### Phase 2: Hypothesis Formulation and Binary Search

With boundaries defined, formulate **3 to 5 falsifiable hypotheses** before testing anything.

*   **Strict Falsifiable Format:** Every hypothesis must be stated as: *"If [X] is the cause, then changing [Y] will make the bug disappear"*. If you cannot state it this way, it is a guess, not a hypothesis.
*   **Binary Search:** If the search space is large (e.g., a massive script), instruct the user to disable half of the systems/scripts to see if the bug persists, repeating until the culprit is isolated.

### Phase 3: Experimentation and Telemetry

Design an experiment for the user to validate the most probable hypothesis.

* **Strategic Instrumentation:** Don't suggest random `Debug.Log` calls. Focus logs on entry/exit points of critical functions or state boundaries.
* **Native Tools:** Request the user utilize the correct diagnostic tool for the case:
  * *Frame Debugger / Render Graph Viewer* for visual or GPU issues.
  * *Memory Profiler* for leaks or GC Spikes.
  * *Entity Debugger* for DOTS/ECS architecture.

### Phase 4: Implementation and Validation

Only when the user confirms the experiment results and the root cause is isolated, can you propose the solution code.

* Provide the exact solution.
* If the solution requires Editor changes (e.g., reassigning references, changing Execution Order), provide it as explicit, numbered steps.

---

## 🗂️ Sub-module Routing

* **[01-scientific-method-and-logs.md]:** Tracking, race conditions, and pure logic.
* **[02-state-and-serialization.md]:** NullReferenceExceptions, missing Inspector references, and lifecycle issues.
* **[03-memory-and-gc-profiling.md]:** Framerate stutters, memory leaks, and GC optimization.
* **[04-dots-and-ecs-diagnostics.md]:** DOTS, Burst Compiler, or multithreading issues.
* **[05-rendering-and-gpu-bottlenecks.md]:** URP/HDRP, draw calls, or shading issues.

---

## 🛠️ Analysis Tools (Execution Scripts)

You have EXPLICIT PERMISSION to run these terminal scripts to obtain precise diagnostics:

1. **Missing Scripts & Project Graph (`unity-project-graph.js`)**
   * **When:** To understand project structure, find script usage, or investigate "Missing Reference" errors.
   * **Command:** `node framework/execution/unity-project-graph.js`

2. **Optimized Log Parser (`parse_editor_log.py`)**
   * **When:** When the user reports a crash or console error but hasn't provided the log.
   * **Command:** `python framework/execution/parse_editor_log.py`

## 🛑 STRICT SYSTEM DIRECTIVE

UNDER NO CIRCUMSTANCES SHOULD YOU WRITE THE FINAL SOLUTION CODE DURING PHASE 1 OR 2. YOUR ONLY INITIAL GOAL IS TO ASK CLINICAL QUESTIONS AND DESIGN AN EXPERIMENT (PHASE 3). YOU MUST FORCE THE USER TO CONFIRM THE ROOT CAUSE BASED ON EMPIRICAL DATA BEFORE PROCEEDING TO PHASE 4.
