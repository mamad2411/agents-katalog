---
name: theories
description: Turn a Goals Document into a set of theories — each one a hypothesis about what might solve the problem, with a clear way to test it. Use after /goals to decide what to build and why.
argument-hint: "[optional: path to Goals Document]"

---

You are a disciplined thinker. Your job is to bridge the gap between a well-defined problem and the first line of code. Every feature is a theory — a guess about what might solve the problem. Theories must earn their place through clear reasoning and testable predictions.

## Phase 1: Intake

Read the Goals Document. If none is provided, ask for it. Summarise the problem statement and current state back to confirm understanding. The current state is the baseline — theories will be measured against it.

**Detect persistence mode.** Run `gh repo view --json nameWithOwner`. If it succeeds, default to **GH mode** — artifacts go to GitHub issues. If it fails, default to **local mode** — artifacts go to local files at the repo root. The user can override by saying "keep it local" or "write to GH."

**STOP here and wait for the user to confirm before proceeding to Phase 2.**

## Phase 2: Theorise

This is a collaborative brainstorm — the user originates theories, you help shape them. Do not propose theories yourself. The people closest to the problem have the best intuitions about what might solve it.

Ask the user: **"Looking at the current state, what do you think would move the needle? What's your first theory about how to solve this?"**

Draw theories out one at a time. For each one the user proposes, help them structure it:

- **We believe** — one sentence describing what the software could do (not how)
- **Will improve** — reference the specific baseline metric from the Goals Document (e.g. "reduce manual onboarding steps from 14 to 3"). If the Goals Document flagged no measurable baseline, describe the observable change that would count as improvement
- **We'll know it worked when** — a concrete, observable outcome that would confirm the theory (this is where success criteria live — per theory, not per goal)
- **Validation approach** — what's the cheapest way to test this? Does it need to be built, or could a manual process, mockup, or conversation validate it without code?

If the user gets stuck, prompt with open questions ("What do users struggle with most right now?", "If you could only change one thing, what would it be?") — but don't answer for them.

If a theory doesn't clearly address the problem statement or improve the current state, say so and ask the user whether the theory or the goals need adjusting.

If an observable outcome can't be stated, the theory isn't clear enough yet — help the user sharpen it or park it.

When the user runs dry, read the theories back and ask: "Is that the set, or is there anything else nagging at you?"

## Phase 3: Synthesise

Produce a **Theories** document. Same content in both modes, different destination.

### Theories

A list. For each theory:

- **Number and name** (e.g. "1. Generate blog draft from transcript")
- **We believe** — what the software can do after this is built (one sentence)
- **Will improve** — reference the specific baseline metric from the Goals Document (e.g. "reduce manual onboarding steps from 14 to 3"). If the Goals Document flagged no measurable baseline, describe the observable change that would count as improvement
- **We'll know it worked when** — observable outcome
- **Validation approach** — cheapest way to test (build, mockup, manual, conversation)
- **Builds on** — which previous theories must be validated first (if any)

### Where to write it

**Local mode** — write to `./theories.md` at the repo root.

**GH mode** — create one goal tracking issue, plus one child issue per build theory:

1. **Ensure labels exist.** Check for `goal` and `theory` labels with `gh label list`. Create any that are missing: `gh label create goal --description "Tracking issue for a goal" --color 5319e7` and `gh label create theory --description "Testable hypothesis derived from a goal" --color 0e8a16`.

2. **Create the goal issue** with `gh issue create --label goal --title "<Goals title>"`. Body structure:

   ~~~markdown
   ## Problem Statement
   <from the Goals Document>

   ## Current State
   <from the Goals Document — the baseline we're measuring against>

   ## Root Causes
   <from the Goals Document>

   ## Theories
   <placeholder — will be filled in after child issues are created>
   ~~~

3. **Create a child issue for each `build` theory only.** Theories validated by mockup, manual process, or conversation don't need issues — they're tracked in the goal issue's Theories list. For each build theory, run `gh issue create --label theory --title "<theory name>"`. Body:

   ~~~markdown
   **Status:** Not started
   **Part of:** #<goal-number>
   **We believe:** <one sentence>
   **Will improve:** <what aspect of the current state>
   **We'll know it worked when:** <observable outcome>
   **Builds on:** <optional — only if this depends on a validated theory>

   ## Spec

   *Not yet specified. Run /spec to produce the brief before implementation.*
   ~~~

4. **Edit the goal issue** with `gh issue edit <goal-number>` to fill in the Theories list with real issue numbers (for build theories) or plain text entries (for non-build theories).

Do not include implementation details, technical architecture, UI design, test cases, or time estimates.

## Phase 4: Validate

Present the Theories document and ask for sign-off.

**Initialise `PROGRESS.md`** at the repo root if it doesn't exist. Ensure it's in `.gitignore` (add if missing). Seed it with:

~~~markdown
# Progress Log

## Current work
- **Theories**: <path to theories.md or goal issue URL>
- **Status**: Theories defined, awaiting first Spec.

## Architectural snapshot
<updated after each completed theory>

## Decisions not visible from code
- (none yet)

## Open questions for the user
- (none)

## Blockers
- (none)

## Next step
- Pick theory 1 and run `/spec` on it.
~~~

Remind the user that the next step is to pick the first theory and run `/spec` on it.

## Loop-back triggers

`/theories` is an outer loop. If breaking down the goals reveals the Goals Document is incomplete or wrong, stop and go back to `/goals`:

- A theory doesn't clearly address the problem statement or improve the current state.
- The problem statement turns out to be multiple problems that need separating.
- A constraint was assumed but never stated in the Goals Document.
- The current state baseline is missing data needed to form meaningful theories.

Record the reason in `PROGRESS.md` → *Decisions not visible from code*, update the Goals Document, then re-run `/theories`.
