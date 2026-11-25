---
name: research-opportunity-graph-skill
description: Use when generating or evaluating research ideas, performing literature-grounded brainstorming, exploring PhD or project topics, planning paper extensions, stress-testing novelty, positioning work for a venue, mapping a research landscape, or finding cross-domain research opportunities.
---

# Research Opportunity Graph

## Purpose

Turn current literature into research ideas that are easy to understand, clearly different from prior work, and specific enough to test.

Do not jump directly to brainstorming. First build a temporary internal map of the evidence:

```text
existing result -> limitation or contradiction -> missing knowledge -> testable opportunity
```

Use that map to reason, but do not expose graph IDs, relation codes, or technical graph notation unless the user explicitly asks for them.

## Core Rules

- Search before giving substantive research advice when search tools are available.
- If search is unavailable, ask the user for papers, abstracts, links, or a literature summary.
- Never invent citations, results, dates, venues, or paper contents.
- Explain specialist terms the first time they appear.
- Use short sentences and concrete examples.
- Separate facts from your interpretation.
- Treat novelty as a comparison with the closest work, not as a confident adjective.
- Prefer a small number of well-developed ideas over a long list of vague directions.
- Include negative, failed, abandoned, or stalled directions when evidence is available.
- Do not call a new application domain a contribution unless it creates a new technical problem.
- Never imply that the temporary map is persistent memory or a database-backed knowledge graph.

## Step 1: Understand the User's Situation

Identify:

- the field and specific topic
- whether the user wants idea generation, idea evaluation, a literature map, a paper extension, or a proposal
- target venue or ambition level, if provided
- time, compute, data, expertise, collaboration, and risk constraints
- how much background explanation the user needs

If the request is broad, narrow it to one concrete task, setting, or failure mode. If the user appears unfamiliar with the topic, explain the field before discussing research gaps.

## Step 2: Search the Evidence

Use a dated evidence snapshot. Search the most relevant evidence buckets:

| Evidence type | Why it matters |
|---|---|
| Recent papers and preprints | Shows where the frontier is moving |
| Surveys | Defines the field and summarizes known problems |
| Closest prior work | Determines whether the idea is genuinely different |
| Negative or stalled work | Shows what has already failed and why |
| Benchmarks and datasets | Reveals what current evaluation does and misses |
| Official project pages and repositories | Shows implementation details and active research signals |

For every important source, record:

- title, year, and link
- what the work actually did
- the specific result or limitation used in the analysis
- whether it is peer reviewed, a preprint, or an informal signal

Do not say "no one has done this." Say "I did not find this in the searched evidence" and state the search limits.

## Step 3: Build the Temporary Evidence Map Internally

Extract only information that can change the recommendation:

- important papers
- research problems
- methods
- assumptions
- datasets and benchmarks
- evaluation metrics
- limitations
- failure cases
- open questions
- future-work statements

Connect them by asking plain questions:

- What problem does this work solve?
- What assumption does it rely on?
- Where does it fail?
- What setting has not been tested?
- Which papers disagree?
- What evaluation is missing?
- What old bottleneck may have changed?
- What method from another field could transfer, and what new obstacle appears?

Do not show raw map notation by default. Translate the result into a user-facing Opportunity Map:

| What we know | What is still missing | Why the missing piece matters | Evidence strength |
|---|---|---|---|

## Step 4: Find Worthwhile Opportunity Types

Look for:

- an important method-setting combination that has not been tested
- two credible findings that contradict each other
- a previously failed direction whose original bottleneck has changed
- a benchmark that misses an important real-world behavior
- a method that can transfer from another field but faces a new technical obstacle
- an assumption that may no longer be valid
- a mismatch between the claimed goal and the evaluation metric
- an unclear mechanism behind an observed improvement
- a result that is difficult to reproduce
- a gap between laboratory results and deployment conditions
- a gap between theory and observed practice

Reject an opportunity when:

- it is merely "use method X in domain Y"
- the closest work already answers the main question
- the proposed experiment cannot distinguish the new claim from a simpler explanation
- the required data or compute is unrealistic for the user
- the idea depends on evidence that is too weak or speculative

## Step 5: Develop Research Ideas in Depth

Generate at most three main ideas unless the user requests more.

For each idea, include:

### Title

A concrete title that names the problem and contribution.

### Research Question

One sentence that could be answered by an experiment.

### Why It Matters

Explain the practical or scientific consequence in plain language.

### Evidence Trail

Explain, without graph codes:

1. what existing work has established
2. what limitation or contradiction remains
3. how that missing piece leads to this idea

### What Is Actually New

State the smallest defensible difference from the closest work. Distinguish:

- a new problem
- a new method
- a new mechanism explanation
- a new evaluation protocol
- a new setting that introduces a real technical obstacle

### Proposed Method

Describe the system or study in enough detail that a researcher could begin implementing it.

### Minimum Experiment

Specify:

- datasets or data collection
- strongest relevant baselines
- evaluation metrics
- important controls
- expected result if the idea is correct
- result that would disprove or seriously weaken the idea
- approximate compute, time, or data requirements when possible

### Main Risks

Name novelty, methodological, engineering, data, and scope risks.

## Step 6: Run a Reviewer Stress Test

For each top idea, answer:

| Reviewer question | Required response |
|---|---|
| Why could this become a useful paper? | Give the strongest evidence-backed argument |
| Why might reviewers reject it? | Name the most serious novelty or significance problem |
| Is there a simpler explanation? | Identify the strongest simple baseline |
| Could the evaluation be misleading? | Check leakage, confounding, metrics, statistics, and dataset bias |
| Is it practical to execute? | Check data, compute, latency, implementation, and reproducibility |
| Is the paper story clear? | State the one problem, one contribution, and one decisive result |
| What result would kill the idea? | Give a concrete stop condition |

Do not write generic advice such as "run more experiments." Name the missing comparison, dataset, metric, or control.

## Step 7: Explain Novelty Clearly

Use this comparison:

| Closest work | What it already does | What it does not answer | Proposed difference | Risk that the difference is too small | How to defend it |
|---|---|---|---|---|---|

Use three to five closest works when making a strong novelty claim. If the search is incomplete, call the assessment provisional.

## Step 8: Produce a Detailed Research Plan

For the best idea, include:

- Title
- One-sentence pitch
- Background in plain English
- Precise research question
- Why the opportunity exists
- Closest three to five works
- Exact novelty claim
- Method, step by step
- Data and preprocessing
- Baselines
- Metrics
- Controls and ablations
- Expected result
- Failure or stop condition
- Reviewer concerns
- How to strengthen the work
- Two-week pilot with weekly artifacts
- Full-paper expansion path
- Venue fit

The two-week pilot must end with evidence for a go/no-go decision, not merely an implementation milestone.

## Step 9: Rank and Recommend

Score ideas from 1 to 5 on:

- novelty
- feasibility
- evidence support
- execution speed
- publishability
- reviewer defensibility

Use equal weights unless the user specifies priorities. Explain the ranking in normal language. Do not let a numerical score hide weak evidence.

## Default Output Structure

Unless the user asks for a shorter answer, use:

1. Plain-English Summary
2. What Existing Research Has Done
3. Research Opportunity Map
4. Best Research Ideas
5. Reviewer Stress Test
6. What Is Actually New?
7. Detailed Plan for the Best Idea
8. Final Recommendation

For a short answer, compress the sections but preserve:

- source-backed evidence
- the path from existing work to the opportunity
- closest-work comparison
- a concrete experiment
- an honest failure condition

## Final Quality Check

Before answering, verify:

- A non-expert can understand why the opportunity exists.
- Every idea has a plain-language evidence trail.
- Important technical terms are explained.
- The closest prior work is directly compared.
- The proposed experiment includes baselines, metrics, and a failure condition.
- The answer names uncertainty and missing evidence.
- Negative prior results are included when relevant.
- The recommendation respects the user's constraints.
- No raw graph IDs or relation codes are shown unless requested.
- No persistent graph or memory functionality is claimed.

## Tone

Be rigorous without being obscure. Be skeptical without being dismissive. Explain before judging. Prefer concrete research questions, experiments, and decisions over compressed academic jargon.
