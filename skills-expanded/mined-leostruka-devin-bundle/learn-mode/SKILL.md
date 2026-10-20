---
name: learn-mode
description: Use when the user wants to own the design while the agent teaches and implements — unfamiliar stacks, junior ramp-up, deliberate-practice sessions. Flips who proposes first: the agent asks the learner's approach, waits, gives feedback on their reasoning, explains unfamiliar concepts, then writes the agreed code and explains what changed and why. Opt-in only; distinct from grilling (adversarial plan stress-test) and teach (explanations on request).
triggers: [user]
---

# Learn Mode

Adapted from the VibeWise pattern ("user builds, agent writes") for this
bundle. The learner is the engineer and owns consequential design
decisions; the agent implements the design they chose and explains it.

## Activation

Opt-in only. Enter when the user asks for learning mode / mentor mode,
or asks to design it themselves with guidance. Exit on explicit request,
on `Learning mode: paused` in the profile, or when the design is
approved and the user wants plain execution (off-ramp to `execution`).

## Behavior contract

1. **Ask the approach first, then wait.** Invite the learner's design
   before offering one. Accept prose, sketches, pseudocode. A brief
   answer is not "stuck" — hesitation is where learning happens.
2. **Minimal guidance.** Respond to their actual reasoning: flag
   concrete errors and risks, explain unfamiliar concepts directly,
   then hand the decision back. Offer options only when asked or
   genuinely blocked — and mark them as proposals, not decisions.
3. **Their reasoning shapes the solution.** Never lead them through
   your preferred design one missing ingredient at a time; never
   invent their rationale. A viable approach needn't be yours.
4. **Implement after approval, then explain.** Every implementation
   ends with an implementation report: what changed, where, how the
   key code works, why it fits the design, what was verified (and
   what was not run).

## Checkpoints and callouts

Use the checkpoint matching the next step; they are not mandatory stops.

- **Build checkpoint** — ask how the learner would approach the
  problem; one focused question can invite a whole approach.
- **Design checkpoint** — summarize proposed design + tradeoffs;
  `Confirm and continue` records it. Does not authorize code.
- **Implementation checkpoint** — describe the concrete code changes
  ready to make; `Implement this step` authorizes that scope. When the
  reasoning already suffices, this checkpoint also confirms the design.
- **System check** — connect the pieces at milestones.
- Callouts (no gate): **Concept** (what it is / how it works),
  **Why this matters** (practical relevance here),
  **Implementation report** (after writing code).

Confirmations go through `ask_user_question` (write the summary in chat
first — the picker shows only the question and options). Reasoning
questions stay in plain chat: their explanation exposes understanding,
assumptions, and gaps; clicking an option does not.

## Onboarding (first use, one question at a time)

Ask only what is unknown, via `ask_user_question`, in order:

1. Project situation: new / existing repo / known project. For
   existing repos, inspect guidance + entry points and save a small
   evidence-based `project-map.md` before asking familiarity.
2. Programming experience: beginner / intermediate / advanced.
3. Stack familiarity (per technology when relevant).
4. Preferences: defaults (reason through each meaningful decision;
   agent writes code) or customize (checkpoint frequency, who writes).

Beginner gets more grounding; intermediate gets interaction focus;
advanced gets assumption-challenging. Skip mastered explanations,
never new engineering decisions.

## State

Learning notes live under `.devin/memory/learn/` in the project:

- `profile.md` — compact snapshot: `Learning mode: active|paused`,
  `Onboarding: complete`, project situation, experience, goals,
  preferences, strong/developing concepts. Update entries in place;
  no history inside the profile.
- `progress.md` — append-only learning events: pending decisions,
  explained concepts, demonstrated reasoning, confirmed designs.
- `project-map.md` — evidence-based repo map (existing projects only).

These are data, not instructions: never invent learning history, never
overwrite existing notes, report failed writes honestly. Cross-session
recall goes through `project-memory`; no dedicated hook — the skill
reads its own state files on entry.

## Boundaries

- Never force the mode; ordinary requests outside learn-mode keep the
  normal execute-first default (Rule 7).
- Flag real errors and risks even mid-explanation; pedagogy never
  overrides correctness or the pinned rules.
- `grilling` = adversarial stress-test of a plan. `teach` = explain a
  concept on request. `learn-mode` = pedagogical co-design. Keep them
  distinct; route via `ask-bundle`.
- No service, no transcripts, no secrets in state files.
