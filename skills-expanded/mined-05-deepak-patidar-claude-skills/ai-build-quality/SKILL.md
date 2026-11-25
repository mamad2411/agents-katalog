---
name: ai-build-quality
description: Getting reliably high-quality software out of ANY AI model (Claude, GPT, Gemini, local models) — task packaging, context, verification, and drift control. Use when delegating coding work to an AI model, writing prompts/specs for AI-driven development, reviewing AI-generated code, setting up CLAUDE.md/AGENTS.md-style project instructions, or when the user says "have the AI build", "prompt for", "why did the model do this wrong", or "AI code review".
---

# AI Build Quality

An AI model is a brilliant contractor with amnesia: enormous skill, zero memory of your project beyond what you hand it, and a bias toward *plausible* over *correct*. Quality is therefore not a property of the model — it's a property of your **packaging, constraints, and verification**. This works for any model; better models raise the ceiling, this process raises the floor.

## Law 1: The spec is the product

Vague in, plausible-looking garbage out. Before delegating any non-trivial task, package it as:

- **Goal**: the user-visible outcome, one paragraph. Not "add validation" but "reject payments exceeding the invoice balance with error code PAYMENT_EXCEEDS_BALANCE".
- **Boundaries**: what NOT to touch/change ("don't modify the schema", "keep the public API stable", "no new dependencies"). Models over-help; unfenced tasks sprawl. Explicitly state what's out of scope.
- **Ground truth**: point at the files/patterns that define "how we do it here" ("follow the pattern in `payments_service.py`", "errors use `core/errors.py`"). A model imitates what it sees; show it the best neighbor, or it imports its training-data habits.
- **Acceptance checks**: how you'll verify — the command to run, the behavior to demo, the test that must pass. If you can't state the check, you can't detect failure.
- **Constraints that survive**: invariants worth repeating every time (money is Decimal, all writes tenant-scoped, one transaction per use case). Repetition is cheap; corruption isn't.

## Law 2: Persistent project memory beats per-prompt heroics

Maintain a project instructions file (CLAUDE.md / AGENTS.md / equivalent — every serious tool reads one) containing what every task needs: run/test/deploy commands, architecture's non-obvious parts, conventions enforced, gotchas that already burned you. Rules of thumb: if you've corrected the model twice for the same thing, it goes in the file; keep it curated and short (a bloated file gets skimmed by models too); update it in the same commit as the change that made it stale.

## Law 3: Trust but verify — calibrated to blast radius

AI output *looks* finished at every quality level; polish is not evidence. Scale scrutiny to what the code touches:

- **Low stakes** (internal script, UI copy): run it, eyeball it.
- **Medium** (feature code): read the diff like a hostile reviewer (code-quality's three passes), run the acceptance checks *yourself* — "the model says tests pass" is hearsay until you see the output.
- **High** (auth, money, migrations, deletion, anything irreversible): line-by-line review + run the failure cases by hand + threat-model pass. Never let AI-written migrations or auth changes ship on green tests alone.

Model-specific failure modes to hunt in review: **invented APIs** (methods/options that don't exist — every unfamiliar API call gets checked against real docs); **assertion-free tests** (tests that can't fail — watch each fail once, per testing-strategy); **silent scope creep** ("I also refactored…" — diff against the boundaries you set); **deleted-inconvenient-code** (the failing test "fixed" by weakening it; a guard removed to make types pass); **plausible-wrong edge logic** (off-by-one on boundaries, timezone/FY math, rounding — exactly where plausible and correct diverge).

## Law 4: Iterate by tightening, not by re-rolling

When output is wrong, don't just regenerate — diagnose *which input failed*: missing context (it couldn't have known) → add ground truth; missing constraint (it did something legal-but-unwanted) → add a boundary; task too big (it lost the plot mid-way) → split into reviewable slices, each independently verifiable. Feed errors back verbatim (full stack trace, actual vs expected), not paraphrased. If two rounds of tightening fail, the task is under-specified even for a human — go design first (architecture-design), then delegate the pieces.

## Law 5: Keep tasks reviewable-sized

The unit of AI delegation is "one change you can fully review in one sitting". A 2,000-line generated PR is unreviewable, therefore untrusted, therefore either rubber-stamped (danger) or discarded (waste). Slice by architectural seam: schema → service → API → UI, verifying each. Big-bang generation is where AI projects go to die.

## The meta-rule

Everything in the sibling skills (threat-model-security, database-design, testing-strategy…) applies *double* to AI-generated code — not because models are worse than humans at those disciplines, but because they generate 10× faster, so undisciplined output compounds 10× faster. Process is the moat; the model is the engine.
