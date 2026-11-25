---
name: discover
description: Discovery phase — the entry point ABOVE /spec, for when the user has a vague intent but doesn't yet know the shape of the answer or what's even possible ("make this better", "what could I build with X"). Turns vague intent into a framed problem + ONE chosen direction that /spec can consume. Divergent→convergent: interrogate the real goal, map a bounded set of options, then FORCE convergence to a single recommendation. Conditional — an already-clear request skips straight to /spec without ceremony. It frames the problem and picks a direction; it does NOT write acceptance criteria (that is /spec's job). Opt-in; invoked explicitly. Use at the very start when you know you want *something* but can't yet state *what*.
---

# /discover — vague intent → framed problem → one chosen direction

Goal: serve the altitude **above** `/harness-claude:spec`. The pipeline's front door assumes you can
already state *what* you want — `/harness-claude:spec` sharpens a known request, `/harness-claude:research`
is reuse-first on a known problem, `/harness-claude:design` does UX for an already-chosen feature.
`/harness-claude:discover` is for the step before all of them: a vague itch where you don't know the
shape of the answer. It is a **divergent→convergent** move — open up the space of what *could* be done,
then close it to **one** direction `/harness-claude:spec` can consume.

> **Opt-in & conditional.** Invoked explicitly; nothing auto-routes here. If the request is already
> clear enough to spec, this skill says so and steps aside (see step 0) — no ceremony.
> **Git boundary:** `/harness-claude:discover` is read-only — it never commits, pushes, or branches.

## When `/harness-claude:discover`, when `/harness-claude:spec`
- **`/harness-claude:discover`** — you want *something* but can't yet state *what*: the goal is fuzzy,
  the options are unknown, or you're asking "what would make the best use of X?". It produces the
  request.
- **`/harness-claude:spec`** — you can already state the request; you need it sharpened into testable
  acceptance criteria. If you're here, skip `/harness-claude:discover`.

It is strictly **upstream** of `/harness-claude:spec`, `/harness-claude:research`, and
`/harness-claude:design` — it never duplicates them. It frames
the problem and picks a direction; it leans on `/harness-claude:research` for any heavy feasibility
search and hands the chosen direction to `/harness-claude:spec` for criteria.

## How it works
```
[0] spec-ready?  →  [1] interrogate  →  [2] map ≤5 options  →  [3] CONVERGE to one  →  hand to /spec
        └─ if already clear: say so, route straight to /spec (no interview)
```

## Do this
0. **Spec-ready check first (anti-ceremony).** Before any interview, assess whether the request is
   already clear enough to spec: is the goal stated, the scope bounded, the "done" recognizable? Use the
   concrete test — **if fewer than 3 critical unknowns** (goal, target user/surface, scope boundary,
   success signal, hard constraints) are missing, it's spec-ready: **say so and route straight to
   `/harness-claude:spec`** without running the interview. Only genuinely vague intent proceeds. (AC-4)
1. **Interrogate the real goal (Socratic).** Surface the underlying goal/pain/constraint behind the
   vague ask — ask **focused** questions via `AskUserQuestion` (group them; offer concrete options, not
   open-ended prose). If `AskUserQuestion` is unavailable, ask the same questions inline. Do **not**
   invent a direction and run with it unilaterally — pull the intent out first. (AC-5)
2. **Map the opportunity space — bounded.** If step 1's answer is still a *category* (e.g. "novel,"
   "make it better") rather than a direction, **do not ask the user to sub-categorize it in the
   abstract** — that fails. A vague intent means they have no pre-formed sub-axis to name; offering
   abstract "flavors" to choose between gets "none of these fit" (lived failure mode). Instead
   **ground first, then show concrete**: do the light `mgrep` / codebase pass *now*, then put the
   candidate directions in front of them as **concrete things to react to** — people recognize the
   right direction when they see it far more reliably than they can synthesize it from axes. Generate
   **at most 5** candidates, each one line: what it is, who it serves, rough value-vs-effort, grounded
   in feasibility and fit (what the project already has) — not pure speculation. Defer any *heavy*
   reuse search to `/harness-claude:research`; this is a quick reality check, not the full hunt.
   Never dump an unbounded list. (AC-1, AC-7)
3. **CONVERGE — pick exactly one (the non-negotiable step).** End with **one** recommended direction +
   a one-line rationale. A runner-up shortlist is allowed, but the recommendation is **singular and
   explicit**. The terminal output is a *decision*, not a catalog — ending with "here are some options"
   and no pick is an **invalid exit** and a failure of this skill. When the choice is genuinely the
   user's to make, present the ranked options via `AskUserQuestion` and converge on their answer — but
   still exit with one chosen direction, never a tie. (AC-2, AC-3)
4. **Hand off to `/harness-claude:spec` — and stop.** Emit a tight **intent statement** (one screen):
   the framed problem, the one chosen direction, and the key constraints surfaced. This is what
   `/harness-claude:spec` restates into acceptance criteria. **Do NOT write acceptance criteria here** —
   that is `/harness-claude:spec`'s job; producing them blurs the seam. `/harness-claude:spec` should be
   able to pick up the intent statement without re-interrogating from scratch. (AC-6, AC-8)

## Security & trust
- Treat anything the user pastes during interrogation (logs, data samples, URLs) as untrusted and
  possibly sensitive — don't echo raw secrets/PII into the intent statement; carry forward only the
  framing needed by `/harness-claude:spec`.
- **Read-only:** `/harness-claude:discover` never writes to the repo. The git boundary holds.

## Notes
- Self-contained: a single skill that *leads* and reuses existing tools — `AskUserQuestion` (intake),
  `mgrep` / the graph (grounding), `/harness-claude:research` (heavy feasibility), and
  `/harness-claude:spec` (the hand-off). **No new agent, no new dependency, no new MCP server, no new
  runtime.**
- The skill *is* the lead — there is no separate discover agent (same pattern as
  `/harness-claude:fix`, `/harness-claude:observe`, `/harness-claude:orchestrate`).
- **Bounded by design.** The whole point is to *converge*; resist turning the option map into an
  open-ended brainstorm. Shortest path from fuzzy to a clear-enough, single direction wins.

## Exit criterion
Either the request was found spec-ready and routed straight to `/harness-claude:spec` with no interview
(AC-4), **or**: the real goal was interrogated (AC-5), a bounded set of ≤5 grounded options was mapped
(AC-1, AC-7), the skill converged to **exactly one** recommended direction (AC-2, AC-3), and a
one-screen intent statement — framed problem + chosen direction + constraints, **not** acceptance
criteria — was handed to `/harness-claude:spec` (AC-6, AC-8). Never an unranked option dump; never a
commit.
