---
name: game-tutorial
description: Audits, adds, or reworks a game's first-time-player tutorial. Use when players cannot identify the controls, goal, failure conditions, or a non-obvious rule; new players quit before completing the core loop; onboarding presents too much at once; or an explicit tutorial or first-run improvement is requested. Separates first-action essentials from later guidance, prefers in-flow or staged first-run teaching, provides a skippable fallback and reusable help, and verifies behavior from clean, completed, and skipped states.
---

# Game Tutorial

Teach the next meaningful action at the moment it becomes relevant, while keeping full
rules available as reference.

## 1. Inspect the project and request

Identify the engine or runtime, entry flow, run command, input-binding system, tutorial
state storage, and string organization. Determine whether the user requested an audit
or implementation; an audit ends with findings and a proposed form.

## 2. Audit the first-time experience

Play from a clean state and learn only from what a new player can see, try, and receive
as feedback. If the game cannot run, trace the displayed entry flow from source and mark
the result inferred.

Inventory controls, goal and failure conditions, score meaning, and non-obvious rules.
Classify every gap:

- **First-action essential** — needed before the player can take a meaningful action.
- **Contextual** — teach when the mechanic or input first becomes relevant.
- **Reference** — useful but not needed in the active flow.
- **Discoverable** — safe experimentation and feedback already teach it.

Teach the first three classes in their proper channel. Leave discoverable behavior
alone so necessary guidance is not buried under the obvious.

## 3. Choose the form

Use the least intrusive form the existing game can support:

1. **Guided first steps.** Attach one prompt to an existing level, wave, encounter, or
   event when the action first matters.
2. **Staged first run.** Script the opening of an existing mode to expose mechanics in
   sequence, for example by delaying pressure until the first action succeeds. Preserve
   the normal mode and ask before changing level or encounter design.
3. **Contextual hints.** Observe state, show a hint on first relevance, and dismiss it
   after the player performs the action.
4. **Instruction screen.** When gameplay has no usable hook, show the first-action
   essentials from step 2 before play on a screen the player can dismiss.

Provide a reachable “How to Play” or equivalent reference for rules that do not belong
in the active flow. Reference depth may match the game; it is not constrained by the
first-action gate.

## 4. Build the state and guidance

Represent at least **unseen**, **in progress**, **completed**, and **skipped**. Persist
completed and skipped states, and provide an intentional reset or replay path when the
project has settings or help UI.

- Show the actual bound key, button, gesture, or control for the active input.
- Present one required action at a time and dismiss it on successful action rather than
  on a timer.
- Make skipping available in one action without removing access to reference help.
- Keep prompts correct when the active input changes among supported capabilities.
- Store player-facing tutorial text in the existing string catalog; if none exists,
  centralize it with stable identifiers instead of scattering literals through scenes.
- Preserve the normal pace after the guided or staged portion completes.

## 5. Verify

Test these paths:

- clean state → guidance appears in order and completes;
- skip → active guidance stops, the state persists, and reference help remains usable;
- completed state → the tutorial does not block a returning player;
- reset or replay → guidance can be intentionally reached again;
- each supported input → prompts show actions the capability can perform;
- smallest supported viewport → prompt and instruction text remains legible;
- interruption or restart during progress → state resumes or restarts deliberately.

If the project cannot run, deliver these as verification steps and mark implementation
behavior unverified.

## Constraints

- Teach the core loop in the gate and defer depth progressively. A game can have many
  valid rules without being a design defect.
- Keep tutorial prompts skippable and reference help reachable.
- Propose changes to level, encounter, difficulty, or core rules and apply them only
  with user approval.
