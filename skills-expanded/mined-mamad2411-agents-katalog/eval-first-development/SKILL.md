---
name: eval-first-development
description: "Build the golden set and the automated scorer before touching the prompt, model, or pipeline. Use whenever an AI output's quality will need to be measured, extraction, RAG, agents, classification."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [evals, golden-set, measurement, define]
    related_skills: [spec-first-ai-feature, error-analysis-50, prompt-suite-versioning]
    program_weeks: [6, 11]
---

# Eval-First Development

## 1 · Purpose

Guarantee that every later change to a prompt, model, or pipeline is judged by a
fixed measuring stick, so "better" is a number, not a feeling.

## 2 · When to use

- Before writing or optimizing any prompt, choosing any model, or tuning any
  retrieval pipeline whose output quality matters.
- When a team is debating two prompts/models with no score to cite.

Do **not** use for throwaway scripts and one-off data pulls. Use it the moment the
output will be shown to anyone as "working".

## 3 · Inputs

- A spec with a metric and gate (`spec-first-ai-feature`), or permission to define
  the metric here.
- At least 20 real or realistic inputs. If fewer exist, generate the rest
  synthetically and label them `synthetic: true`.

## 4 · Procedure

1. Create the golden-set file (e.g. `golden.jsonl`): one JSON object per case with
   `input`, `expected`, and `tags` (the failure classes you anticipate). Start with
   20 cases; 50 is better. Include the hard cases you hope never occur.
2. Write the scorer as code, a function `score(output, expected) -> dict` that
   returns per-field or per-case results. Exact match where possible; rubric-graded
   LLM-as-judge only where correctness is fuzzy, and calibrate the judge against
   10 human-graded cases before trusting it.
3. Add the score report: one line per case plus an aggregate, written to
   `evals/results/<timestamp>.json`. A score you cannot diff is a story.
4. Run the scorer against the current system (or a trivial baseline) and record the
   **baseline score** in the spec file.
5. Freeze the golden set. Changes to it are commits with a message, never silent
   edits, the measuring stick must not move while the system is being measured.
6. Wire the scorer so one command runs it (script, make target, or notebook cell).
   If running the eval takes more than one command, it will not get run.
7. Only now touch the thing being improved, prompt, model, chunking, tools.
   Every subsequent change reports: score before, score after, one-line reason.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "I'll build the eval after the first version works." | Then "works" will be defined by whatever the first version does. Baseline first. |
| "The task is too fuzzy to score." | Then it is too fuzzy to ship. Write a rubric and grade it, fuzzy is a judge prompt away from measurable. |
| "20 cases is too few to matter." | 20 cases catch the classes that hurt. Zero cases catch nothing. |
| "We can eyeball a few outputs." | Eyeballing sees the cases you remember. The golden set sees all of them, every time. |

## 6 · Red flags

- The golden set has only happy-path cases.
- The scorer lives in someone's head ("I check the outputs myself").
- Scores are quoted without the golden-set version they were measured against.
- The eval takes so long to run that people batch changes before running it.

## 7 · Verify

- `golden.jsonl` (or equivalent) exists with ≥ 20 cases, tagged, version-controlled.
- One command runs the scorer and writes a diffable results file.
- A baseline score is recorded in the spec.
- Every subsequent experiment in the log has score-before, score-after, reason.

## 8 · ZoroLogistics example

Week 6 builds `golden_bol.jsonl`: 20 bills of lading with per-field answers
(shipper, consignee, ports, weights, terms), tagged `scan-noise`, `multi-line`,
`missing-field`. The scorer does exact-match per field after normalization. Baseline
for the naive prompt: 0.61. Every prompt version in the week then reports against
this set, which is how "v3 clears 0.90" stops being a claim and becomes a row in
`evals/results/`.

---
© 2026 Zorost Intelligence LLC · zorost.com
