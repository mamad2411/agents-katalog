---
name: eval-brief
description: Design evals as the definition of done for an AI surface. Use when the user says eval, golden set, quality bar, LLM-as-judge, acceptance criteria for an agent, or "how do we know this is good enough to ship."
---

# Eval Brief

Turn "the AI should be good" into a testable quality bar. For AI surfaces, evals are acceptance criteria — not a later QA step.

## When to use

- New AI feature or agent job
- Prompt, model, tool, or retrieval change
- "What does done mean?" on an LLM surface
- After a production miss (add the miss to the set)

## Process

### 1. Name the jobs

List end-to-end jobs, not model capabilities. One row per job: user, done looks like, forbidden.

### 2. Pick 3–5 dimensions

Default set for most copilots:

| Dimension | Why |
|-----------|-----|
| Faithfulness | Did it invent facts? |
| Boundary | Did it take a forbidden action? |
| Usefulness | Did it complete the job? |
| Failure honesty | Did it admit unknowns? |

Add latency/cost if the job is interactive or loops.

### 3. Build a small set from reality

Start with ~20 cases:

- Golden (ideal)
- Edge (missing evidence, conflict)
- Adversarial ("just make up a number")
- At least one real production miss, as soon as you have one

A pass is evidence about **known** failures. It is not a claim of general quality.

### 4. Choose judges you can afford

| Judge | Use for |
|-------|---------|
| Heuristic / regex / tool-trace | Boundaries, schema, forbidden tools |
| LLM-as-judge | Faithfulness, tone — calibrate on human labels |
| Human | Disagreements and new failure modes |

If PM and eng disagree on labels, the eval is the product conversation. Resolve it before scaling the judge.

### 5. Write the brief

Save to `knowledge/products/<product>/evals.md`. If the file does not exist, copy `knowledge/products/_template/evals.md`.

Also log a decision if this eval **gates a ship** or **blocks autonomy**.

## Rules

- Do not wait for a platform. A spreadsheet is a valid v1.
- Re-run on every prompt/model/tool/context change.
- When production fails, add a case the same day. That is the improvement loop.
- Never use "helpfulness" as the only dimension.
- Claims in launches and sales must match the last eval run (date + conditions).

## Output

A filled `evals.md` plus, if asked, a 10-case starter table the user can label this week.
