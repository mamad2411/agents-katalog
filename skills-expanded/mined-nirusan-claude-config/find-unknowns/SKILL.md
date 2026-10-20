---
name: find-unknowns
description: Surface the gaps between the prompt and the real task (map vs territory) before, during, and after implementation. Runs the right technique — blindspot pass, brainstorm/prototype, interview, reference hunt, implementation plan, deviation log, explainer, or quiz — based on the phase and the type of unknown.
triggers:
  - "/find-unknowns"
  - "blindspot pass"
  - "unknown unknowns"
  - "find my unknowns"
  - "interview me"
  - "quiz me on"
  - "aide-moi à trouver mes angles morts"
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch
user-invocable: true
---

# Find Unknowns

The prompt is the map; the codebase and real-world constraints are the territory. The gap between them is made of unknowns, and work quality is bottlenecked by how early they get surfaced. This skill picks and runs the right discovery technique for the current phase.

## Step 1: Ask for Starting Point Context

Before any technique, get (or infer from the conversation) the user's starting point:
- How familiar are they with this part of the codebase / this domain?
- Where are they in their thought process (vague idea, rough spec, ready to build)?
- What have they already tried or decided?

Never skip this. The same question ("add an auth provider") needs a completely different pass for a codebase veteran vs. someone new to the module.

## Step 2: Classify the Dominant Unknown

| Quadrant | Signal | Technique |
|----------|--------|-----------|
| Known knowns | Already in the prompt | Nothing to do |
| Known unknowns | "I haven't decided X yet" | **Interview** |
| Unknown knowns | "I'll recognize it when I see it" | **Brainstorm + prototype**, or **Reference** |
| Unknown unknowns | New domain, new module, "don't know what to ask" | **Blindspot pass** |

## Step 3: Run the Technique for the Current Phase

### Pre-implementation

**Blindspot pass** (unknown unknowns)
Search the codebase and relevant docs, then report back: what questions the user should be asking, what "good" looks like in this domain, historical decisions and potholes in this area, and concretely how to prompt better for this task. Teach, don't just list.

**Brainstorm + prototype** (unknown knowns)
Produce several genuinely different directions (not variations of one idea) as cheap disposable artifacts — a single HTML file with fake data, a mock, a throwaway script. No backend wiring, no state management. The goal is a reaction, not a foundation. For design, 3-4 wildly different directions beats 1 polished one.

**Interview** (known unknowns)
Ask one question at a time. Prioritize questions whose answer would change the architecture or data model; drop questions that only affect mechanical details. Stop when remaining ambiguities no longer change the approach.

**Reference hunt** (can't articulate what they want)
Ask for or find source code that already does it — a library, a vendored crate, a component on a site they like — even in another language. Read the implementation, extract the semantics, reimplement in the project's stack. Source code beats screenshots and descriptions.

**Implementation plan** (ready to build)
Write the plan ordered by likelihood of change: data model and type interfaces first, UX flows next, mechanical refactoring last. The top of the plan is what the user must review; the bottom is what they trust you on.

### During implementation

**Deviation log**
Keep a temporary `implementation-notes.md`. When an edge case forces a deviation from the plan: pick the conservative option, log it under `## Deviations` (what was found, what was chosen, why), and keep going. Do not stop to ask for each one. These notes feed the next planning session.

### Post-implementation

**Explainer / pitch**
Package prototype + spec + implementation notes into one document a reviewer can read cold. Lead with the demo and the decisions; anticipate the unknowns and failure points an expert reviewer would probe.

**Quiz**
Produce a report of what actually changed (context, intuition, behavior — not just the diff) ending with a quiz the user must pass before merging. Questions should target behavior that depends on existing code paths, i.e. what the diff alone doesn't show.

## When to Skip

- The task is mechanical and fully specified (rename, dependency bump, applying a settled decision).
- The user is deeply familiar with the area and just wants execution — respect an explicit "just do it".
- A brainstorm/plan for this exact scope already exists — reuse it instead of re-running discovery.

## Anti-patterns

- **Interviewing when a prototype would answer faster.** If the user "will know it when they see it", show options, don't ask questions.
- **One design direction with three color tweaks.** Directions must differ structurally.
- **Prototypes that touch the real app.** Discovery artifacts are disposable by construction.
- **Batching 10 interview questions at once.** One at a time; each answer reshapes the next question.
- **Silently absorbing plan deviations.** Unlogged deviations are unknowns pushed onto the next session.
- **Following the plan off a cliff.** If the territory contradicts the map mid-task, surface it: a pivot found during implementation is this skill's success case, not a failure.
- **Skipping the quiz after a long session.** A big diff read quickly is a pile of fresh unknown unknowns.
