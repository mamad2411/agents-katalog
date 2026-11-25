---
name: competitive-battlecard
description: "Creates sales-ready competitive battlecards with objection handling, win/loss patterns, feature comparison grids, and tactical talk tracks. Designed to be used in live sales conversations, deal reviews, and competitive displacement campaigns."
category: gtm
default_depth: standard
---

# Competitive Battlecard

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Creates sales-ready competitive battlecards with objection handling, win/loss patterns, feature comparison grids, and tactical talk tracks. Designed to be used in live sales conversations, deal reviews, and competitive displacement campaigns.

## When to Use

- Sales team encounters a specific competitor frequently
- Preparing for a competitive displacement deal
- New competitor enters the market
- Quarterly competitive intelligence refresh
- Sales kickoff or enablement sessions

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick prep before a single deal or call | Quick Reference, Feature Comparison |
| **Standard** | Recurring competitor across multiple deals | All sections |
| **Deep** | Competitive displacement campaign or SKO prep | All sections + customer-sourced verbatim quotes, trap-question roleplay scripts, segment-specific variants |

**Omit rules:** At Light depth, skip Competitor Overview, Win/Loss Patterns, Landmines, and Recent Intelligence. Produce only the Quick Reference card and Feature Comparison grid.

## Framework

### Battlecard Structure

```markdown
# Competitive Battlecard: [Our Product] vs. [Competitor]
**Last updated:** [date]
**Confidence level:** [High / Medium, based on data freshness]

---

## Quick Reference (for live calls)

### When you hear "[Competitor]," say:
"[1-2 sentence positioning statement that acknowledges competitor and pivots to our strength]"

### Our 3 biggest advantages:
1. **[Advantage 1]:** [One-line proof point]
2. **[Advantage 2]:** [One-line proof point]
3. **[Advantage 3]:** [One-line proof point]

### Their 2 biggest advantages (be honest):
1. **[Their strength 1]:** [How we counter it]
2. **[Their strength 2]:** [How we counter it]

---

## Competitor Overview

### Company Profile
- **Founded:** [year]
- **Funding / Revenue:** [estimate]
- **Headcount:** [estimate]
- **Target market:** [who they sell to]
- **Pricing:** [model and range]
- **Sales motion:** [PLG / Enterprise / Hybrid]

### Their Positioning
**Tagline:** "[their headline]"
**Key claim:** [what they say makes them different]
**Reality check:** [how accurate is their claim, with evidence]

---

## Feature Comparison

| Capability | Us | [Competitor] | Why It Matters |
|---|---|---|---|
| [Capability 1] | ● Strong | ◐ Partial | [Buyer impact] |
| [Capability 2] | ◐ Partial | ● Strong | [Buyer impact] |
| [Capability 3] | ● Strong | ○ None | [Buyer impact] |

**Legend:** ● Strong | ◐ Partial/Limited | ○ Not available

---

## Objection Handling

### "Why not just use [Competitor]?"
**Response:**
> "[Competitor] is [genuine acknowledgment of what they do well]. Where we differ is [specific differentiator]. For teams that care about [buyer priority], this matters because [concrete outcome]. For example, [customer name or anonymized case] switched from [Competitor] to us and saw [specific result]."

### "[Competitor] is cheaper."
**Response:**
> "On sticker price, [Competitor] starts lower. But when you factor in [hidden cost 1, e.g., implementation time], [hidden cost 2, e.g., missing feature requiring workaround], and [hidden cost 3, e.g., scaling costs], the total cost of ownership is actually [comparable / higher]. [Customer X] estimated they saved [$Y] over [timeframe] by choosing us because [reason]."

### "[Competitor] has [feature we don't have]."
**Response:**
> "You're right, they do offer [feature]. We've intentionally [chosen a different approach / have it on our roadmap because]. Our customers tell us that [alternative approach] actually delivers better results because [reason]. [Customer X] found that [proof point]."

### "We're already using [Competitor]."
**Response:**
> "Many of our best customers came from [Competitor]. The switching cost is [description, ideally low]. What typically triggers the switch is [common trigger]. Would it be helpful to see how [similar company] made the transition?"

---

## Win/Loss Patterns

### We tend to WIN when:
- [Pattern, e.g., "The buyer prioritizes [capability] over [capability]"]
- [Pattern, e.g., "There's a technical evaluator in the process"]
- [Pattern, e.g., "They've experienced [pain point] with [Competitor]"]

### We tend to LOSE when:
- [Pattern, e.g., "Price is the only criterion"]
- [Pattern, e.g., "They're deeply embedded in [Competitor's ecosystem]"]
- [Pattern, e.g., "Decision is made without a trial/POC"]

### Trap questions they might set:
- "[Question designed to highlight their strength]", Reframe: [how to redirect]

---

## Landmines to Plant

Questions to ask the prospect that expose competitor weaknesses:

1. "How important is [capability where we're strong and they're weak] to your workflow?"
2. "Have you evaluated how [competitor] handles [scenario where they struggle]?"
3. "What's your expected growth over the next 12 months? I ask because [scaling concern with competitor]."

---

## Recent Intelligence
- [Date]: [Notable move, funding, launch, pricing change, key hire, loss]
- [Date]: [Customer feedback about competitor]
```

## Minimum Evidence Bar

**Required inputs:** Competitor name, your product's key differentiators, and at least one source of competitive data (website, G2 reviews, win/loss interviews, or sales call recordings).

**Acceptable evidence:** Public pricing pages, analyst reports, verified customer reviews, CRM win/loss notes, sales call transcripts, competitor documentation.

**Insufficient evidence:** If no win/loss data or direct customer feedback exists, produce a partial artifact with unanswered sections marked `[TBD, requires: win/loss interview data from 3-5 recent deals]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Feature Comparison ratings, pricing data, and Competitor Overview must be sourced.
- **Hypotheses:** Win/Loss Patterns and Landmines may be hypothesized from limited data, must be labeled "Hypothesis, validate with sales team."

## Output Format

Produce a Competitive Battlecard with:
1. **Quick Reference**, pocket card for live conversations
2. **Competitor Overview**, company profile and positioning
3. **Feature Comparison**, honest capability matrix
4. **Objection Handling**, scripted responses to top 4-5 objections
5. **Win/Loss Patterns**, when we win and when we lose
6. **Landmines**, questions that expose competitor weaknesses
7. **Recent Intelligence**, latest competitive signals

**Shipwright Signature (required closing):**
8. **Decision Frame**, recommended competitive positioning stance, trade-off acknowledged, confidence level with source quality, owner (product marketing or sales enablement), decision date, revisit trigger (competitor launch or pricing change)
9. **Unknowns & Evidence Gaps**, unverified feature claims, missing win/loss data, pricing tiers not yet confirmed
10. **Pass/Fail Readiness**, PASS if the Quick Reference, Feature Comparison, and every included objection handler are evidence-backed. Cover each material objection supported by win/loss or customer evidence; do not invent handlers where no objection evidence exists, and name that evidence gap. FAIL if feature ratings are unverified or no win/loss patterns exist. **Light-depth exception:** At Light depth, PASS requires only an evidence-backed Quick Reference and Feature Comparison; win/loss patterns and objection handlers are not evaluated.
11. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Trashing the competitor**, Buyers respect honesty; acknowledge strengths and pivot
- **Stale information**, Update quarterly at minimum; pricing and features change fast
- **No win/loss data**, Without pattern recognition, battlecards are guesswork
- **Too long for live use**, The quick reference section must fit on one screen
- **Ignoring their strengths**, If sales is surprised by a competitor advantage, the battlecard failed

## Weak vs. Strong Output

**Weak:**
> "We are better than Competitor X in most areas and offer a superior product overall."

Vague claim with no specific differentiators, no evidence, and nothing a rep can say on a call.

**Strong:**
> "Our 3 biggest advantages: 1. Sub-200ms API response (their median is 800ms per G2 benchmarks, Dec 2025). 2. Native SSO, they charge $5k/yr add-on. 3. SOC 2 Type II certified since 2023; they have Type I only."

Specific, sourced, and immediately usable in a live conversation.
