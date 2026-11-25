---
name: spec
description: Turn a vague request into a clear, written spec with acceptance criteria before any code. Use at the start of any non-trivial feature, change, or bugfix. First gate of the Plan phase.
---

# /spec — clarify the request into a spec

Goal: eliminate misunderstanding before a line of code. A vague ask becomes a short,
testable spec.

## Do this
1. **Restate** the request in your own words. If anything is ambiguous or
   underspecified, ask the user focused questions — do not guess on load-bearing points.
2. Capture the essentials only (keep it lean):
   - **Problem / why** — the user-visible outcome wanted.
   - **Scope** — what's in, and explicitly what's out.
   - **Acceptance criteria** — concrete, testable bullets ("given X, when Y, then Z"),
     each with a **stable ID** (`AC-1`, `AC-2`, …). The IDs are load-bearing: `/harness-claude:verify`
     builds its coverage matrix against them, so they must not be renumbered later. These
     become the tests in `/harness-claude:implement`.
   - **Constraints** — perf, security, compatibility, deadlines, non-functionals.
   - **Open questions** — anything blocking, with your recommended default.
3. Keep it to one screen. This is a spec, not a novel.

## Output
For non-trivial work, **write the spec to `.claude/planning/<slug>/SPEC.md`** — pick a
short kebab-case `<slug>` for the feature (schema: `docs/state-and-artifacts.md`) — so
later steps and any fresh-context subagent read a file, not the conversation. Also present
it in the conversation. For a trivial/one-file change (lazy reflex), skip the artifact and
say so in one line — a spec in the reply is enough. Format:

```
# Spec: <title>
## Problem
## In scope / Out of scope
## Acceptance criteria
- [ ] AC-1: ...
- [ ] AC-2: ...
## Constraints
## Open questions (with recommended defaults)
```

## State
When you wrote a `SPEC.md`, patch `.claude/STATE.md`: set `slug`, `phase: spec`,
`status: done`, `next_skill: /research` (schema + convention in
`docs/state-and-artifacts.md`). Skip for trivial work.

## Exit criterion
Acceptance criteria are concrete, testable, and ID'd, and no blocking open question
remains. Then proceed to `/harness-claude:research`.
