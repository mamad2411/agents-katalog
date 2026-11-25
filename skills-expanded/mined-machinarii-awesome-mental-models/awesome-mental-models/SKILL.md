---
name: awesome-mental-models
description: Use when the user wants help thinking through a decision, problem, strategy, plan, evaluation, communication, or any open-ended judgment call where a mental model or framework would sharpen the analysis. Triggers include "help me decide", "how should I approach this", "I'm stuck on", "which mental model fits", "apply a framework to this", "think through this with me", "what am I missing". Also trigger on hard tradeoffs, prioritization debates, post-mortems, pre-launches, and when the user is rationalizing or asking "am I thinking about this right?"
---

# Awesome Mental Models

Pick the right mental model for the user's situation, then guide them through it as a working session — not a lecture.

The model files live at `{{REPO_ROOT}}/mental-models/<slug>.md`. The category index is at `{{REPO_ROOT}}/mental-models.md`. Each file has Overview, How to Use It, Example, Takeaway, Source. Use **How to Use It** as the spine of facilitation.

**Order of operations: run Phase 0 FIRST — before consulting When-to-Use, When-NOT-to-Use, or any selection table. Even if the user's words match trigger phrases, Phase 0 runs first.**

## Phase 0 — Stakes Check (silent, gating)

**Before doing anything else, silently answer:**

- (a) Is this **reversible** within a week with no lasting cost?
- (b) Is the cost of being wrong **less than an afternoon** of work?
- (c) Is the user **not asking for a framework** — they want a quick take?

**If (a) AND (b) are both YES, OR (c) is YES → bypass the protocol.** Do NOT load a model.

Reply directly in 2–3 sentences answering the underlying question. Mention the framework option *only if asked*; do not narrate the bypass — just answer.

Only proceed to Phase 1 if a model would actually earn its keep.

## When to Use

- User describes a real situation needing structured judgment
- Words like: decide, plan, prioritize, evaluate, fix, understand, communicate, learn, negotiate
- User explicitly asks for a model or framework
- User seems stuck, rationalizing, or asking "am I thinking about this right?"

## When NOT to Use

- Pure factual questions ("what's X?")
- User has already named a model and wants the file content — just open `mental-models/<slug>.md`
- Cheap, reversible, low-stakes choice — running a model is overkill

## The 5-Phase Protocol

1. **Frame** — Restate the situation explicitly capturing all four:
   - **Goal** (what is the user trying to do?)
   - **Stakes & reversibility** (1-way door or 2-way door? Cost of being wrong?)
   - **Deadline** (when must this be decided/done?)
   - **Decider / who's involved** (solo, team, stakeholders, adversary?)

   Confirm the frame before continuing. If reversibility surfaces this as a 2-way door with low stakes, return to Phase 0 and bypass.

2. **Triage** — Ask 1–3 questions to place the situation in a category: Decide, Solve, Strategize, Plan, Evaluate, Understand, Create, Risk, Communicate, Learn, or Compete.
3. **Select** — Match category + signals to ONE model. Alternative only if near-tie. State why it fits in one line. Use `selection-tables.md`.
4. **Confirm** — "Want me to walk you through `<Model>`?" Wait for explicit yes.
5. **Facilitate** — Open `mental-models/<slug>.md`. Walk the "How to Use It" steps interactively against the user's actual problem.

## Triage Lead Question

> "Are you trying to **decide something, solve a problem, design a strategy, plan execution, evaluate options, understand a system, generate ideas, manage risk, communicate, learn, or out-compete someone?**"

For situational triggers like "we keep firefighting" or "I have to give a board update tomorrow," use `cheat-sheet.md`.

## Disambiguators (only if needed)

- **Decide vs. Evaluate:** Choosing between options you have, or first need to score them?
- **Solve vs. Understand:** Need to fix it, or first make sense of why it keeps happening?
- **Plan vs. Strategize:** Goal known and need execution, or still deciding what game to play?
- **Risk vs. Plan:** Worried about failure modes, or coordination?

## Facilitation Rules

For each "How to Use It" step in the chosen model:

1. State the step in one sentence.
2. Translate it into a question or prompt about the user's situation.
3. Wait for their answer.
4. Reflect what you heard. Probe once if thin.
5. Move on. Don't skip silently — name skipped steps and why.

End the session with:

- One thing to do **today**.
- One thing to **revisit** (with a trigger or date).
- An optional next model to stack (see `selection-tables.md` for stacking pairs).

## Hard Rules

- Never recommend a model without first restating the situation back and getting agreement.
- Never dump multiple models. Pick one. Mention an alternative only if near-tie.
- Never lecture from the file. Convert every step into a question about *their* problem.
- **Stacking pairs are offered AFTER Phase 5 facilitation completes — never bundled upfront.** If the user is wavering or anxious, that is a signal to facilitate the chosen model *more carefully*, not to add models.
- **Early exit is a hard stop.** If the user declines the framework ("just tell me", "never mind", "skip the model") at any point, drop it immediately and answer the underlying question in plain prose. Do not negotiate to keep the framework alive.
- If no model fits, say so. Suggest reframing or use `cynefin-framework.md` to diagnose what kind of problem this is.
- If the user names a model, skip Triage and Select — go straight to Confirm and Facilitate.

## Common Failure Modes

| Failure | Fix |
|---|---|
| Picked a flashy model when a 5-min chat would do | Run Phase 0 first. 2-way door + low stakes = bypass, no model. |
| Lectured from the file | Convert every "How to Use It" step into a question about their situation. |
| Recommended 3 models "to try" | Pick one. State it. Confirm. Stacking is post-Phase-5 only. |
| Bundled stacking pair upfront because user seemed anxious | Wavering ≠ permission to stack. Facilitate one model carefully first. |
| Negotiated to keep framework alive after user said "just tell me" | Drop it. Answer in plain prose. Do not relitigate. |
| Skipped Confirm | No facilitation without explicit yes. |
| Used the file's example | Apply to user's actual problem, not the textbook one. |
| Ended without an action | Always close with one thing-to-do-today and one to revisit. |

## Defaults When Truly Unsure

- Decision-shaped: `decision-matrix.md`
- Problem-shaped: `five-whys.md`
- Strategy-shaped: `swot-analysis.md`, then `porters-five-forces-analysis.md`
- Plan-shaped: `objectives-and-key-results-okr.md`
- Risk-shaped: `pre-mortem-analysis.md`
- Communication-shaped: `bluf-bottom-line-up-front.md`
- Diagnosis-shaped: `cynefin-framework.md`

Always state: "Defaulting to `<X>` because the situation is under-specified — once we run it, we'll know if a sharper model fits."

## Reference Files

- `selection-tables.md` — per-category trigger → model tables (Phase 3 routing)
- `cheat-sheet.md` — common situations → likely model (fast path)
