---
name: aris-idea-creator
description: Generate and rank research ideas given a broad direction. Use when user says "brainstorm ideas", "generate research ideas", "what can we work on", or wants to explore a research area for publishable directions. Ported from wanshuiyin/Auto-claude-code-research-in-sleep (ARIS) — methodology only, Claude-Code-specific MCP/CLI/GPU deps stripped for VS Code Copilot.
---

# Research Idea Creator

Generate publishable research ideas for the research direction the user provides.

## Overview

Given a broad research direction from the user, systematically generate, validate, and rank concrete research ideas. This skill runs the full pipeline inline: landscape survey → idea generation → feasibility filtering → self-review validation → ranked report.

## Constants

- **OUTPUT_DIR = `idea-stage/`** — All idea-stage outputs go here. Create the directory if it doesn't exist.

## Workflow

### Phase 1: Landscape Survey (5-10 min)

Map the research area to understand what exists and where the gaps are.

1. **Scan local paper library first**: Check `papers/` and `literature/` in the project directory for existing PDFs. Read first 3 pages of relevant papers to build a baseline understanding before searching online. This avoids re-discovering what the user already knows.

2. **Search recent literature** using WebSearch:
   - Top venues in the last 2 years (NeurIPS, ICML, ICLR, ACL, EMNLP, etc.)
   - Recent arXiv preprints (last 6 months)
   - Use 5+ different query formulations
   - Read abstracts and introductions of the top 10-15 papers

3. **Build a landscape map**:
   - Group papers by sub-direction / approach
   - Identify what has been tried and what hasn't
   - Note recurring limitations mentioned in "Future Work" sections
   - Flag any open problems explicitly stated by multiple papers

4. **Identify structural gaps**:
   - Methods that work in domain A but haven't been tried in domain B
   - Contradictory findings between papers (opportunity for resolution)
   - Assumptions that everyone makes but nobody has tested
   - Scaling regimes that haven't been explored
   - Diagnostic questions that nobody has asked

### Phase 2: Idea Generation (brainstorm)

Generate 8-12 concrete research ideas using the landscape and gaps from Phase 1.

For each idea:
1. One-sentence summary
2. Core hypothesis (what you expect to find and why)
3. Minimum viable experiment (what's the cheapest way to test this?)
4. Expected contribution type: empirical finding / new method / theoretical result / diagnostic
5. Risk level: LOW (likely works) / MEDIUM (50-50) / HIGH (speculative)
6. Estimated effort: days / weeks / months

Prioritize ideas that are:
- Testable with moderate compute
- Likely to produce a clear positive OR negative result (both are publishable)
- Not "apply X to Y" unless the application reveals genuinely surprising insights
- Differentiated from the 10-15 papers surveyed

Be creative but grounded. A great idea is one where the answer matters regardless of which way it goes.

### Phase 3: Mechanical consolidation + objective feasibility gate

> This phase does NOT judge idea quality, novelty, or impact. Those are verdicts reserved for Phase 4 self-review. Phase 3 only drops ideas that are objectively out of budget.

1. **Objective feasibility gate**: drop an idea ONLY on a mechanical, budget-based fact:
   - estimated compute exceeds what the user has available, OR
   - requires a dataset that is provably unavailable.
   Do NOT drop on "implementation looks complex" — annotate complexity instead.

2. **Novelty signal — ANNOTATE, do not eliminate**: for each surviving idea, do 2-3 targeted web searches and attach a `prior_work` note (what looks related, with links). This is input for Phase 4, not a filter.

3. **Impact signal — ANNOTATE, do not eliminate**: attach a one-line `so_what` note (why the result would matter either way).

Every feasible, non-duplicate idea — carrying its `prior_work`, `so_what`, and `effort_note` annotations — proceeds to Phase 4.

### Phase 4: Deep Validation (self-review)

Act as a skeptical reviewer and evaluate the full annotated candidate set from Phase 3.

1. **Devil's advocate review**: For each candidate, critically assess:
   - What's the strongest objection a reviewer would raise?
   - What's the most likely failure mode?
   - Is the prior_work note a real novelty problem, or differentiable?
   - How would you rank these for a top venue submission?
   - Which 2-3 would you actually work on, and why?

2. **Novelty check**: For the top-ranked ideas, do a thorough multi-source literature search (multiple query formulations, recent venues) to verify novelty. Be brutally honest — false novelty claims waste months of research time.

3. **Select top ideas**: Take the top 2-3 ideas that survive both the self-review and the novelty check.

### Phase 5: Output — Ranked Idea Report

Write a structured report to `idea-stage/IDEA_REPORT.md`:

**Lead every recommended idea with its method, in plain language.** Before any hypothesis, novelty score, or claim, state in 2-4 concrete steps what we actually build / train / run — no jargon, no claim-IDs. The reader must understand *what we do* before *what we claim*.

```markdown
# Research Idea Report

**Direction**: [user's research direction]
**Generated**: [date]
**Ideas evaluated**: X generated → Y survived filtering → Z recommended

## Landscape Summary
[3-5 paragraphs on the current state of the field]

## Recommended Ideas (ranked)

### Idea 1: [title]
- **Method (what we actually do)**: [2-4 concrete steps in plain language]
- **Hypothesis**: [one sentence]
- **Minimum experiment**: [concrete description]
- **Expected outcome**: [what success/failure looks like]
- **Novelty**: X/10 — closest work: [paper]
- **Feasibility**: [compute, data, implementation estimates]
- **Risk**: LOW/MEDIUM/HIGH
- **Contribution type**: empirical / method / theory / diagnostic
- **Reviewer's likely objection**: [strongest counterargument]
- **Why we should do this**: [1-2 sentences]

### Idea 2: [title]
...

## Eliminated Ideas (for reference)
| Idea | Reason eliminated |
|------|-------------------|
| ... | Already done by [paper] |
| ... | Requires unavailable compute/dataset |

## Suggested Execution Order
1. Start with Idea 1 (lowest risk, clearest signal)
2. Idea 2 as backup
...

## Next Steps
- [ ] Scale up Idea 1 to full experiment
- [ ] If confirmed, iterate with review loops
```

## Key Rules

- The user provides a DIRECTION, not an idea. Your job is to generate the ideas.
- Quantity first, quality second: brainstorm broadly, then filter ruthlessly.
- A good negative result is just as publishable as a positive one. Prioritize ideas where the answer matters regardless of direction.
- Don't fall in love with any idea before validating it. Be willing to kill ideas.
- Always estimate compute cost. An idea that needs 1000 GPU-hours is not actionable for most researchers.
- "Apply X to Y" is the lowest form of research idea. Push for deeper questions.
- Include eliminated ideas in the report — they save future time by documenting dead ends.
- **Anti-hallucination**: Never fabricate paper titles, authors, or arXiv IDs. Every cited paper must be verified via web search. If uncertain, tag `[UNVERIFIED]`.

## Composing with Other Skills

After this skill produces the ranked report, the user can:
- Run `aris-novelty-check` on the top idea for deep novelty verification
- Run `aris-research-lit` for a broader literature survey
- Implement the top idea and iterate
