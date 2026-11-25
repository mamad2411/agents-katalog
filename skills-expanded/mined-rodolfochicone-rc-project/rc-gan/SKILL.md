---
name: rc-gan
description: "Runs an adversarial generator-evaluator loop to drive subjective quality (UI/UX, design, copy, CLI ergonomics, prose) up to a target score — exercising the running artifact, scoring it against a weighted rubric, and iterating until the threshold or a plateau. Use to refine quality a pass/fail gate cannot capture. Do not use for correctness or security defects (rc-code-review)."
model: opus
effort: high
argument-hint: "[target] [--threshold 7.0] [--max-iterations 8]"
---

# GAN Harness (generator ↔ evaluator)

`make verify` proves a change is *correct*. It says nothing about whether a UI is well-designed, a CLI is pleasant, or copy lands. This skill closes that gap with an adversarial loop: a **generator** builds/improves the artifact, an independent **evaluator** exercises the *running* result and scores it against an explicit rubric, and the loop iterates on the evaluator's concrete feedback until the score clears a threshold or stops improving. The two roles are kept separate on purpose — nothing grades its own work, and the evaluator is fresh each round so it never anchors on the last verdict.

## Required Inputs

- **Target**: what to build or improve (a feature, a screen, a command's UX, a document).
- Optional **rubric**: dimensions + weights. If absent, derive one in Phase 0.
- Optional **--threshold** (default `7.0` on a 1–10 scale) and **--max-iterations** (default `8`).

## Phase 0 — Spec & rubric

Before iterating, write down what "good" means so scoring is not vibes:

1. Expand the target into a short spec: what it must do and the quality bar it must hit.
2. Define a **weighted rubric** of 3–5 dimensions summing to 1.0. Pick dimensions that fit the artifact, e.g. for a UI: `design 0.3 · craft 0.3 · functionality 0.2 · originality 0.2`; for a CLI: `ergonomics 0.4 · clarity 0.3 · correctness 0.2 · discoverability 0.1`. Each dimension scored 1–10; final = Σ(score × weight).
3. State how the artifact will be **exercised** (run it for real): a web UI via a browser/dev server, a CLI by running commands, a doc by reading it against its goal. Evaluation is of the running thing, never of the source alone.

## The loop

Repeat until stop condition. Track score per iteration.

1. **Generate** — implement or improve the artifact to satisfy the spec and address the previous iteration's feedback. Keep it real and runnable; leave the artifact in a runnable state. Run the project's correctness gate (`make verify` or equivalent) so quality work never ships a broken build.
2. **Evaluate (fresh & independent)** — spawn a *separate* reviewer (a subagent / fresh context — do not reuse the generator's reasoning). It must:
   - Actually exercise the running artifact against the "how to exercise" plan from Phase 0.
   - Score each rubric dimension 1–10 with one concrete justification each, then compute the weighted total.
   - Write **specific, addressable defects** ("the primary button has no hover state", "`--help` doesn't list the `sync` subcommand"), not vague notes. Penalize generic AI-slop (default gradients, lorem-ipsum, boilerplate layouts).
3. **Decide**:
   - **Pass** — weighted score ≥ threshold → stop, report success.
   - **Plateau** — score improved by < 0.3 for 2 consecutive iterations → stop; report the plateau and the best version (more iterations won't help; escalate to the user).
   - **Cap** — reached `--max-iterations` → stop; report the best version and remaining gaps.
   - Otherwise feed the evaluator's defects into the next **Generate**.

## Output

Report: the rubric, the score progression (e.g. `iter1 4.2 → iter2 5.8 → iter3 7.4`), whether it passed / plateaued / hit the cap, the final artifact location, and any remaining gaps. Keep each iteration's evaluator feedback so the progression is auditable.

## Critical Rules

- The rubric and weights are fixed at Phase 0; do not move the goalposts mid-loop to manufacture a passing score.

## Boundaries

Opt-in, for subjective quality only. Pairs with `rc-code-review` (correctness/security) and the build's verification gate (binary pass/fail) — this skill owns the axis those cannot measure.
