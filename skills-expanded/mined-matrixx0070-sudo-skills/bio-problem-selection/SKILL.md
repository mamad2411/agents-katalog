---
name: bio-problem-selection
version: 1.0.0
description: Select, ideate, and de-risk life-sciences research problems by importance, tractability, and neglectedness, ending in a pursue/park/kill call with kill criteria.
author: matrixx0070
tags: [research-strategy, ideation, de-risking, prioritization, planning, go-kill]
capabilities: []
---

## When to use

Use this when the user is choosing what to work on next, generating project ideas, or unsticking a stalled program and wants structured judgment rather than gut feel. Apply at project inception or at a go/kill decision point.

**Not for:** ranking already-chosen drug targets (use bio-target-prioritization), designing the experiment once a project is picked (use bio-experiment-design), or literature synthesis (use bio-literature-review).

## Method

1. Clarify the goal and constraints: scientific aim, timeline, budget, platform, and what "success" concretely produces.
2. Generate candidates widely before judging — combine unmet needs, new tools/datasets, and adjacent-field transfers. Breadth first; do not filter while ideating.
3. Score each on Importance (impact if true), Tractability (progress with current tools), Neglectedness (crowding). Add a personal-fit/capability multiplier.
4. Identify each candidate's crux: the single assumption that, if false, kills it. **Decision:** rank by how cheaply that crux can be tested, not by raw excitement — a cheap crux beats a marginally more important but untestable idea.
5. **Decision (stuck project):** diagnose the failure mode — wrong hypothesis, wrong model system, underpowered, or execution/tooling — and propose the smallest experiment that discriminates between them.
6. Recommend pursue, park, or kill, each with a next de-risking step and an explicit kill criterion.

## Example

A lab weighs three ideas. Idea 1 (high importance, but crux = "the biomarker is stable in serum," testable for $200 in a week) beats Idea 2 (higher importance, crux = a two-year cohort). Idea 3 is a stuck project: the phenotype won't replicate. Diagnosis narrows to model system vs underpowered; the discriminating step is a single high-n replicate in a second cell line before any mechanism work. Recommendation: pursue 1, park 2, run the discriminator on 3 with kill criterion "no effect at n=20."

## Pitfalls

- Scoring importance while ignoring tractability — chasing the most important problem you cannot make progress on.
- Judging ideas during brainstorming, which kills the weird transfer ideas that become the best bets.
- Naming no crux, so the project drifts without a cheap early test.
- Recommending "pursue" with no kill criterion — projects then run on sunk cost forever.

## Output format

```
# Problem Selection — <goal>
Constraints: aim / timeline / budget / platform / success =

## Candidate table
| Idea | Importance | Tractability | Neglectedness | Fit | Crux |

## Top pick(s)
- <idea> — cheapest crux test: <experiment> | expected info gain: <one line>

## Stuck project (if any)
diagnosed failure mode: <...>  discriminating next step: <...>

## Recommendations
<idea>: pursue/park/kill — next de-risk step — KILL IF <criterion>
```
Flag assumptions as ASSUMED and any untested claim as UNVERIFIED.

## Reference

### The ITN framework (Importance × Tractability × Neglectedness)

Adapted from the cause-prioritization literature (80,000 Hours / Open Philanthropy). The three factors are roughly multiplicative — a project that is important and neglected but intractable still yields near-zero expected progress, which is why "chase the most important problem" is a classic failure mode.

Expected value ≈ Importance × Tractability × Neglectedness, then modulated by a **personal-fit / capability** multiplier (do *you* have the platform, skills, and access to move it).

| Factor | Question it answers | Proxy metric |
|--------|---------------------|--------------|
| **Importance** | How big is the impact if the hypothesis is true? | Patients/DALYs affected, breadth of downstream science unlocked, effect magnitude |
| **Tractability** | How much progress per unit effort with today's tools? | % of problem solved per \$1M or per year; is there a cheap decisive experiment? |
| **Neglectedness** | How crowded is the space? | # active labs/programs, funding flowing in, recent publication density |
| **Personal fit** (multiplier) | Can *this* team execute uniquely well? | Platform/reagents in hand, prior data, unfair access/skill advantage |

### Scoring anchors (score each 1–5, multiply)

| Score | Importance | Tractability | Neglectedness |
|:-:|-----------|-----------|-----------|
| 1 | Marginal / incremental | Needs tools that don't exist | Hot field, dozens of labs, well funded |
| 3 | Meaningful for a subfield | Doable in 1–2 yr with a stretch | Some competition, a handful of groups |
| 5 | Field-changing / large patient impact | Decisive experiment is cheap & fast | Almost no one working on it; overlooked |

Multiply for a 1–125 composite, then apply fit. Do not average — a 1 on any axis should visibly sink the score, which multiplication enforces.

### Worked example

| Idea | Imp | Tract | Negl | Product | Fit | Crux |
|------|:-:|:-:|:-:|:-:|:-:|------|
| 1 Serum biomarker | 4 | 5 | 3 | 60 | high | "Biomarker stable in serum" — \$200, 1 wk |
| 2 Longitudinal cohort | 5 | 2 | 4 | 40 | med | "Signal appears pre-symptom" — 2-yr cohort |
| 3 Stuck mechanism | 3 | 3 | 3 | 27 | high | Phenotype won't replicate |

Idea 1 wins not on raw importance (Idea 2 is higher) but on tractability × a **cheap, decisive crux**. Rank by how cheaply the crux can be tested, not by excitement.

### Crux thinking & value of information

The **crux** is the single load-bearing assumption that, if false, kills the project. A good crux test maximizes *value of information per dollar*: high probability of changing your decision × low cost. Prefer a \$200 one-week experiment that could kill the idea over a marginally more important idea whose crux needs two years — early cheap falsification dominates.

### Stuck-project failure-mode ladder

Diagnose before you iterate; propose the *smallest experiment that discriminates* between causes:

1. **Wrong hypothesis** — biology isn't what you think → orthogonal readout / independent line of evidence.
2. **Wrong model system** — real effect, wrong context → replicate in a second cell line / primary cells / in vivo.
3. **Underpowered / noisy** — effect real but n too small or assay too variable → one high-n replicate; re-power (see bio-experiment-design).
4. **Execution / tooling** — reagent, batch, protocol drift → positive control, reagent QC, batch audit.

### Decision output: pursue / park / kill

Every recommendation carries a **next de-risking step** and an **explicit kill criterion** (e.g. "KILL IF no effect at n=20, α=0.05"). A "pursue" with no kill criterion is how programs run on sunk cost forever. **Park** = promising but the crux is currently too expensive; revisit when a cheaper test or new tool appears. Reversible, cheap, information-rich bets beat expensive irreversible ones — sequence work so the cheapest killer experiment runs first.
