---
name: semantic-micro-interactions
description: Define bounded interface feedback from a real state transition, including accessible visual motion, reduced-motion and input-equivalent behavior, and an optional semantic sound hook without owning audio playback. Use when a control, gesture, validation, progress state, or completion needs meaningful feedback rather than decorative animation. Triggers on micro-interaction, interaction motion, button feedback, state transition, drag settle, satisfying interaction, reduced motion, hover feedback, completion animation, semantic motion.
handoffs:
  - to: sound-effects
    when: an approved interaction map contains an opt-in soundEvent that needs an audio palette and asset
  - to: walkthrough
    when: the mapped interactions have been implemented in an operable interface and need task-context verification
accepts:
  - from: design-tokens
  - from: narrative-scrollytelling
---

# Semantic Micro-interactions

**Announce at start:** "I'm using the humane:semantic-micro-interactions skill to make state changes feel clear without making motion carry the meaning."

A micro-interaction is a bounded response to a meaningful state transition. Start
with what changed and what the person needs to understand; motion, highlight,
status text, haptics, and sound are possible channels after that decision. An
effect with no state change or orientation job is decoration and does not belong
in the interaction map.

## Quick reference

| Need | Read |
| --- | --- |
| Pattern selection, interruption, gesture and status guidance | `references/patterns.md` |
| The interaction-map fields and accessibility invariants | `references/contract.md` |

## Map the transition

For each moment, record:

1. The semantic trigger and the before/after states. Use `activate`, `focus`,
   `hover`, `state-change`, `validation`, `completion`, or `gesture-end`; do not
   make raw DOM events the design contract.
2. The intent: `acknowledge`, `confirm`, `reject`, `reveal`, `connect`,
   `progress`, or `settle`.
3. What already communicates the result without motion or sound. If the answer
   is nothing, repair the state semantics before animating it.
4. The full-motion feedback, its reduced and no-motion substitutions, and every
   equivalent input route.
5. Interruption, cancellation, repetition and rate-limit behavior.

Write the result as an interaction map using `references/contract.md`. When the
user wants a saved artifact, resolve `artifact_path(name,
"semantic-micro-interactions", "json")`; never assemble a `.design` path at the
call site. Validate a saved map with `python3 scripts/validate_map.py <map.json>`.

## Hard boundaries

- Use native controls and platform keyboard conventions before custom gesture
  handling. Hover may enrich; it never reveals required information or the only
  control.
- A press appearance may begin on pointer-down. Navigation, submission,
  destructive actions, and persistent changes commit on activation/pointer-up,
  unless an explicit undo or essential exception makes the alternative safe.
- Dragging has both a keyboard route and a non-dragging single-pointer route.
  Keyboard support alone does not satisfy the latter.
- Motion never moves focus. A reveal preserves logical focus order, and a status
  update is announced only when it is actually a status message.
- Non-essential spatial travel, parallax, scale, path and rotation have a
  reduced-motion substitution. Do not implement reduced motion as a global
  near-zero duration that leaves vestibular movement intact.
- Reject ambient loops, strobing, repeated shake, and effects that delay the
  true state. Feedback is interruptible and settles into the actual state.

These are Humane production policies informed by WCAG, not a claim that every
one is a normative WCAG AA requirement. `references/contract.md` names the
relevant criteria and the scope of each.

## Sound is a hook, not a layer

An interaction map may emit one semantic identifier such as
`action.confirmed` or `panel.settled`. It never contains a file path, prompt,
provider, autoplay flag, volume, preload or mixer configuration. Sound is off
until the person opts in, silent operation preserves the same meaning, and rapid
events are deduplicated.

Hand an approved `soundEvent` to `humane:sound-effects`; that skill owns the
palette, generated asset, receipt and playback guidance. Do not add a sound
merely because the interface moves.

## Verification and handoff

Before calling the map implemented, check it with keyboard, pointer and touch
where supported; full, reduced and no-motion modes; sound off; interruption
mid-transition; rapid repeat; and error/slow states. Record what was actually
observed and mark the rest **Not verified**.

Then hand the operable interface to `humane:walkthrough`. This skill specifies
feedback behavior; `walkthrough` decides whether the feedback actually helps a
person complete the task.

## What this skill does not own

| Concern | Owner |
| --- | --- |
| Duration, dimension, color and typography values | `design-tokens` |
| Narrative order, sticky stages and scroll activation | `narrative-scrollytelling` |
| Sound prompts, providers, files and playback layer | `sound-effects` |
| Task success in the working interface | `walkthrough` |
| Framework-specific animation craft and accessibility engineering depth | `interfaces` when installed; otherwise mark the implementation depth Not reviewed |
