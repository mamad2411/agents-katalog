---
name: product-narrative
description: "Produces long-form persuasive product narratives in the style of Amazon's 6-pager or shorter 2-pager memos. Used for complex product decisions that require deep reasoning, multi-stakeholder alignment, and a permanent record of the thinking process. Unlike a one-pager (which is a pitch), a narrative is an argument."
category: communication
default_depth: standard
---

# Product Narrative / Memo

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Produces long-form persuasive product narratives in the style of Amazon's 6-pager or shorter 2-pager memos. Used for complex product decisions that require deep reasoning, multi-stakeholder alignment, and a permanent record of the thinking process. Unlike a one-pager (which is a pitch), a narrative is an argument.

## When to Use

- Major product bets that need cross-functional buy-in
- Complex decisions where a one-pager can't capture the nuance
- Annual/quarterly product strategy documentation
- When the decision requires the reader to change their mental model
- Building institutional knowledge around a pivotal decision

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | 2-pager for a decision within existing strategy | Introduction + The Argument + Recommendation |
| **Standard** | Full 6-pager for a significant product bet or strategic shift | All sections |
| **Deep** | Company-level strategic pivot or board-facing memo | All sections + extended Appendix with financial model, customer research corpus, and competitive teardown |

**Omit rules:** At Light depth, skip Background & Context, Counterarguments & Risks, and Appendix. Produce only the thesis, core argument, and recommendation.

## Framework

### Memo Formats

**The 2-Pager:** For significant decisions within existing strategic direction.
**The 6-Pager:** For strategic pivots, new products, or company-level bets.

Both follow the same structure; the 6-pager goes deeper on each section.

### Narrative Structure

```markdown
# [Title, Assertion, Not Question]

> **Example titles:**
> - "We Should Build a Self-Serve Analytics Product for Mid-Market SaaS"
> - "Why Our Current Onboarding Funnel Will Cap Growth at $10M ARR"
> - "The Case for Pivoting from Per-Seat to Usage-Based Pricing"

**Author:** [name]
**Date:** [date]
**Status:** [Draft / Final]
**Reading time:** [N] minutes

---

## 1. Introduction (½ page)

[State the thesis clearly in the opening paragraph. The reader should know your conclusion before they read your argument.]

"This memo argues that [thesis]. I'll present evidence that [supporting points], address the strongest counterarguments, and recommend [specific action] with [timeline and investment]."

[Briefly describe the current situation and why this decision matters now.]

---

## 2. Background & Context (½ - 1 page)

[Provide the context necessary to understand the argument. Assume a smart reader who knows the business but may not be close to this specific area.]

### What's happened
[Recent developments, data trends, or events that set the stage]

### What we've tried
[Previous efforts, experiments, or approaches and their results]

### What's changed
[Why the status quo is no longer tenable, new data, market shift, customer signal]

---

## 3. The Argument (1 - 2 pages)

[This is the core of the memo. Present your reasoning in a logical sequence. Each paragraph should build on the previous one.]

### [Point 1, Strongest argument]
[Reasoning + evidence. Use data, customer quotes, competitive intel, or first-principles logic.]

### [Point 2, Supporting argument]
[Reasoning + evidence.]

### [Point 3, Supporting argument or implication]
[Reasoning + evidence.]

**Key data:**

| Evidence | Source | Implication |
|---|---|---|
| [Data point 1] | [Source] | [What it means for the argument] |
| [Data point 2] | [Source] | [What it means] |

---

## 4. Counterarguments & Risks (½ - 1 page)

[This is what separates a good memo from a pitch deck. Steel-man the strongest objections, then address them honestly.]

### Counterargument 1: "[Strongest objection]"
[Present it fairly, as strongly as an opponent would.]

**Response:** [Your rebuttal, with evidence or reasoning. If you can't fully rebut it, acknowledge the residual risk.]

### Counterargument 2: "[Second strongest objection]"
[Present it fairly.]

**Response:** [Your rebuttal.]

### Risks we're accepting
[Be honest about the risks inherent in your recommendation. This builds trust.]

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [Risk 1] | [H/M/L] | [H/M/L] | [How we'll manage it] |
| [Risk 2] | [H/M/L] | [H/M/L] | [How we'll manage it] |

---

## 5. Recommendation (½ page)

[State the recommendation clearly, including specific actions, timeline, investment, and success criteria.]

### What we should do
[Specific action, not "explore" or "consider" but "invest $X in Y starting Z"]

### What this requires
- **Investment:** [Budget, headcount, opportunity cost]
- **Timeline:** [Key milestones]
- **Organizational changes:** [New team, new process, etc., if any]

### How we'll know it's working
| Metric | Baseline | Target | Timeframe |
|---|---|---|---|
| [Metric 1] | [current] | [target] | [when] |
| [Metric 2] | [current] | [target] | [when] |

### How we'll know it's NOT working (kill criteria)
- [Condition 1] → [Action: pause, pivot, or kill]
- [Condition 2] → [Action]

---

## 6. Appendix (as needed)

[Detailed data, methodology notes, competitive analysis, financial models. Reference from the main narrative but keep the main body clean.]

- Appendix A: [Detailed financial model]
- Appendix B: [Customer research summary]
- Appendix C: [Competitive analysis]
```

### Writing Principles

```markdown
## Narrative Writing Rules

1. **Write in complete sentences and paragraphs.** Bullet points are for appendices, not arguments.
2. **Lead with the conclusion.** Academic papers build to a conclusion; business memos start with one.
3. **Use specific numbers.** "Significant growth" → "47% YoY growth in enterprise segment"
4. **Steel-man objections.** If you present a weak version of the counterargument, the reader won't trust your thinking.
5. **Be honest about uncertainty.** "We don't know X yet, but we believe Y because Z" is stronger than pretending you know everything.
6. **One idea per paragraph.** Each paragraph should make one point with evidence.
7. **Write for the skeptic.** Assume the reader starts by disagreeing with you.
8. **Active voice.** "We should invest" not "An investment should be considered"
9. **No weasel words.** "We recommend" not "We might want to consider"
10. **Cite your sources.** Every data point should be traceable.
```

### The Reading Meeting Protocol

For 6-pagers, follow Amazon's reading meeting format:

```markdown
## Reading Meeting Format
1. **Silent reading (20 minutes):** Everyone reads the memo in silence. No prior distribution.
2. **Comments and questions (10 minutes):** Readers note their questions and reactions.
3. **Discussion (30 minutes):** Work through questions, starting with the most fundamental challenges.
4. **Decision or next steps (10 minutes):** Reach a decision or agree on what's needed to decide.

**Why silent reading works:**
- Everyone actually reads it (unlike pre-reads that get skimmed or skipped)
- Discussion starts from a shared understanding
- The quality of the writing is the quality of the thinking
```

## Minimum Evidence Bar

**Required inputs:** A specific thesis (not a question), at least two supporting data points with sources, and at least one steel-manned counterargument (Standard and Deep only; at Light depth, counterargument input is recommended but not required).

**Acceptable evidence:** Customer research (interviews, surveys, usage data), market data with cited sources, competitive intel, internal metrics, experiment results.

**Insufficient evidence:** If the argument rests on a single anecdote or unsourced market claim, stop and recommend running the **discovery-interview-prep** or **metrics-dashboard** skill to gather targeted evidence before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** Data in the Argument section and Background must cite verifiable sources.
- **Hypotheses:** Forward-looking projections in the Recommendation section (targets, timelines, kill criteria thresholds), must be labeled with underlying assumptions.

## Output Format

Produce a Product Narrative with:
1. **Thesis statement**, clear, specific, in the opening paragraph
2. **Context**, background and what's changed
3. **Argument**, logical, evidence-based reasoning
4. **Counterarguments**, steel-manned and addressed
5. **Recommendation**, specific action, investment, success criteria, kill criteria

**Shipwright Signature (required closing):**
6. **Decision Frame**, recommended course of action, trade-off vs. alternatives considered, confidence level with evidence quality cited, decision owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, untested assumptions in the argument, missing customer segments, unvalidated market sizing
8. **Pass/Fail Readiness**, PASS if thesis is falsifiable, at least one counterargument is steel-manned, and kill criteria are defined; FAIL if the memo lacks a clear thesis or presents no counterarguments. **Light-depth exception:** At Light depth, PASS requires only a falsifiable thesis and a clear recommendation; counterarguments and kill criteria are not evaluated.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Memo as data dump**, A narrative makes an argument; a data dump presents information without a thesis
- **Weak counterarguments**, If the reader can think of a stronger objection than you addressed, the memo fails
- **No kill criteria**, Proposing a bet without pre-committed exit conditions invites sunk cost fallacy
- **Bullet point soup**, Narratives require prose; bullets are a crutch that hides weak reasoning
- **Memo too late**, Write the narrative BEFORE the decision, not after to rationalize what you already chose

## Weak vs. Strong Output

**Weak:**
> "Customers have expressed interest in self-serve analytics, and the market is growing, so we should build it."

No specific data, no source, no quantified opportunity, this is an assertion dressed as an argument.

**Strong:**
> "In 14 of 20 mid-market churn interviews (Q4 research deck, slide 12), customers cited 'waiting for an analyst to pull data' as a top-3 frustration. The self-serve BI market grew 34% YoY (Gartner, 2024). We estimate a $2.1M ARR expansion opportunity based on current mid-market seat count."

Cited sources, specific sample size, quantified opportunity, a skeptical reader can verify every claim.
