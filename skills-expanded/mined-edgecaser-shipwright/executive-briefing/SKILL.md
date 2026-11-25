---
name: executive-briefing
description: "Produces single-page executive briefings designed to secure alignment, approval, or resources from senior leadership. Uses the Situation-Complication-Resolution (SCR) framework and Pyramid Principle to deliver maximum impact in minimum reading time. Different from a status update, this is a persuasive artifact with a clear ask."
category: communication
default_depth: standard
---

# Executive Briefing / One-Pager

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Produces single-page executive briefings designed to secure alignment, approval, or resources from senior leadership. Uses the Situation-Complication-Resolution (SCR) framework and Pyramid Principle to deliver maximum impact in minimum reading time. Different from a status update, this is a persuasive artifact with a clear ask.

## When to Use

- Requesting budget, headcount, or executive sponsorship
- Proposing a new initiative, pivot, or strategic shift
- Escalating a decision that requires senior leadership input
- Presenting options that need executive arbitration
- Any time you need to compress a complex argument into one page

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick alignment check or FYI to a sponsor who already has context | SCR Narrative + The Ask |
| **Standard** | Requesting budget, headcount, or a decision from leadership | All sections |
| **Deep** | Board-level ask or cross-org initiative needing full justification | All sections + Appendix with financial model, risk register, and stakeholder map |

**Omit rules:** At Light depth, skip Supporting Evidence and Options Considered. Produce only the SCR narrative and a specific ask.

## Framework

### The SCR Framework

Every executive briefing follows: **Situation → Complication → Resolution**

- **Situation:** What's the context? What do they already know? (Establish common ground)
- **Complication:** What changed? Why does this need attention now? (Create urgency)
- **Resolution:** What should we do? What do you need from them? (Propose action)

### One-Pager Template

```markdown
# [Title, Concise, Descriptive]
**Date:** [date] | **Author:** [name] | **Ask:** [1-sentence summary of what you need]

---

## Situation
[2-3 sentences. Set the context. What's the relevant background the reader needs?
Assume they know the business but may not know the specifics of this topic.]

## Complication
[2-3 sentences. What's changed? What's the problem, risk, or opportunity?
Why does this need attention NOW, not next quarter?]

## Resolution
[2-3 sentences. What are you proposing? Be specific and direct.]

---

## Supporting Evidence

### The Data
[1-2 key data points that support the resolution. Charts or tables if they're compact.]

| Metric | Current | If We Act | If We Don't |
|---|---|---|---|
| [Key metric 1] | [value] | [projected] | [projected] |
| [Key metric 2] | [value] | [projected] | [projected] |

### Options Considered (if seeking a decision)

| | Option A: [Name] | Option B: [Name] | Option C: Do Nothing |
|---|---|---|---|
| **Description** | [1 sentence] | [1 sentence] | [Status quo] |
| **Cost** | [$ or effort] | [$ or effort] | [$0 direct, but...] |
| **Expected outcome** | [Projected impact] | [Projected impact] | [What happens] |
| **Risk** | [Key risk] | [Key risk] | [Risk of inaction] |
| **Timeline** | [Duration] | [Duration] | [N/A] |

**Recommendation:** [Option X] because [1-sentence rationale]

---

## The Ask
[Be explicit. What do you need from the reader?]

- [ ] **Decision needed:** [Approve Option A / Choose between A and B / etc.]
- [ ] **Resources needed:** [Budget: $X / Headcount: N / Executive sponsorship]
- [ ] **Timeline:** [Decision needed by date]

---

## Appendix (optional, for those who want to go deeper)
[Links to detailed PRD, analysis, or supporting documents. NOT required reading.]
```

### Formatting Rules

```markdown
## Executive Briefing Formatting Rules

1. **One page maximum.** If it's longer, you haven't thought hard enough about what matters.
2. **Lead with the ask.** The first line after the title should tell them what you need.
3. **No jargon.** If a term isn't in common use at the exec level, define it or replace it.
4. **Bold the important numbers.** Executives scan; make the key data points impossible to miss.
5. **Include "Do Nothing" as an option.** It makes the cost of inaction explicit.
6. **One recommendation.** Don't present options without a recommendation, that's delegating your job upward.
7. **Specific ask, specific deadline.** "Please approve by Friday" not "Let me know what you think."
```

### Calibration by Ask Type

| Ask Type | SCR Emphasis | Key Content | Tone |
|---|---|---|---|
| Budget request | Complication (cost of inaction) | ROI projections, payback period | Confident, data-driven |
| Strategic pivot | Situation (what changed) | Market evidence, risk of current path | Urgent but measured |
| New initiative | Resolution (the opportunity) | Market sizing, competitive advantage | Ambitious, evidence-backed |
| Escalation | Complication (the blocker) | Impact of delay, options with trade-offs | Direct, solution-oriented |
| Resource request | Complication (capacity gap) | Current vs. needed, impact on commitments | Practical, pragmatic |

## Minimum Evidence Bar

**Required inputs:** The specific ask (decision, budget, or resource), the audience (who will read this), and at least one data point supporting the complication.

**Acceptable evidence:** Internal metrics, customer quotes, market research, competitive intel, financial projections with stated assumptions.

**Insufficient evidence:** If you cannot quantify the cost of inaction or the expected outcome of your recommendation, produce a partial artifact with unanswered sections marked `[TBD, requires: quantified cost-of-inaction analysis or outcome projection]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** The Situation, Complication, and Supporting Evidence data must be grounded in verified facts.
- **Hypotheses:** Projected outcomes in the options table and ROI estimates may be forward-looking, must be labeled with assumptions.

## Output Format

Produce a One-Page Executive Briefing with:
1. **Title & Ask**, immediately clear what this is about and what's needed
2. **SCR Narrative**, Situation, Complication, Resolution
3. **Supporting Evidence**, key data and options comparison
4. **The Ask**, specific, time-bound, actionable

**Shipwright Signature (required closing):**
5. **Decision Frame**, recommended option, trade-off vs. alternatives, confidence level with evidence quality cited, decision owner, decision-by date, revisit trigger
6. **Unknowns & Evidence Gaps**, unvalidated assumptions in projections, missing competitive data, untested customer willingness
7. **Pass/Fail Readiness**, PASS if SCR is complete, ask is specific and time-bound, and at least one data point supports the complication; FAIL if the ask is vague or the complication lacks quantified urgency
8. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Burying the ask**, If the executive has to read the whole page to find out what you want, you've failed
- **Too much background**, They know the business; get to the complication quickly
- **No recommendation**, Presenting options without a recommendation is asking the exec to do your job
- **Weasel words**, "We might want to consider possibly exploring..." → "We should invest $X in Y because Z"
- **Missing the "do nothing" cost**, Executives default to inaction; make the cost of inaction explicit
- **More than one page**, Ruthlessly edit. If you can't say it in one page, you don't understand it well enough yet.

## Weak vs. Strong Output

**Weak:**
> "We might want to consider investing in a new onboarding flow, as we've been hearing some feedback about it."

Vague ask, no data, no urgency, an executive will defer this indefinitely.

**Strong:**
> "We need $120K to rebuild onboarding by Q3. Trial-to-paid conversion has dropped from 18% to 11% since January (source: Amplitude cohort report), costing ~$40K/mo in lost revenue. Doing nothing means $480K lost by year-end."

Specific ask, quantified complication, explicit cost of inaction, forces a decision.
