---
name: product-strategy-session
description: "Facilitates a structured product strategy workshop covering vision, positioning, strategic bets, and success criteria. Inspired by Marty Cagan's \"Inspired\" and \"Empowered\" frameworks for product-led organizations."
category: strategy
default_depth: standard
---

# Product Strategy Session

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Facilitates a structured product strategy workshop covering vision, positioning, strategic bets, and success criteria. Inspired by Marty Cagan's "Inspired" and "Empowered" frameworks for product-led organizations.

## When to Use

- Annual or quarterly product strategy development
- New product or product line launch planning
- Team alignment on strategic direction
- Preparing for a strategy offsite or leadership review

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick alignment check or prep for a leadership conversation | Product Vision, Strategic Bets (thesis only) |
| **Standard** | Quarterly or annual strategy cycle | All sections |
| **Deep** | New product launch, pivot, or board-level strategy review | All sections + competitor bet mapping, assumption stress-test per bet, scenario analysis (base/bull/bear) |

**Omit rules:** At Light depth, condense Strategic Context and review cadence. Retain the vision, falsifiable bet theses, key assumptions, scope boundaries and kill criteria; do not imply investment approval from an alignment sketch.

## Framework

### Step 1: Product Vision

Define the aspirational future state your product enables.

**Good product visions are:**
- Inspirational (motivates the team)
- Directional (helps say no to things)
- Customer-centric (describes value to users, not business metrics)
- Durable (valid for 3-5 years)

**Template:**
```
For [target customer], who [key need/opportunity],
[Product name] will [key benefit].
Unlike [current alternatives],
our product [key differentiator].
```

### Step 2: Strategic Context

Assess where you are before deciding where to go:

```markdown
## Strategic Context

### Current State
- Product stage: [Vision / MVP / Growth / Maturity / Renewal]
- Key metrics (trailing): [metric: value, metric: value]
- Biggest recent win: [description]
- Biggest current challenge: [description]

### Market Context
- Market trajectory: [Growing / Stable / Contracting]
- Key trends: [1-3 trends affecting your space]
- Competitive pressure: [Low / Medium / High]

### Customer Context
- Primary persona: [description]
- Core job-to-be-done: [job statement]
- Current satisfaction: [NPS, CSAT, or qualitative assessment]
- Top unmet needs: [from research]
```

### Step 3: Strategic Bets

A product strategy is a set of bets, informed choices about where to invest, grounded in your theory of how you win.

**For each bet:**
```markdown
### Bet: [Name]
**Thesis:** We believe that [action] will result in [outcome] because [evidence/reasoning].
**What would have to be true:** [Key assumptions that must hold]
**Investment level:** [Major / Moderate / Exploratory]
**Time horizon:** [This quarter / This half / This year]
**Success metric:** [How we'll know this is working]
**Kill criteria:** [When we'd abandon this bet]
```

**Rules:**
- 2-4 major bets maximum, strategy is about focus
- Each bet must have a falsifiable thesis
- Include at least one "what would have to be true" assumption per bet
- Assign kill criteria upfront to avoid sunk cost fallacy

### Step 4: What We're NOT Doing

Equally important as what you invest in:

```markdown
## Strategic Boundaries
### We will NOT:
- [Decision 1], Rationale: [why]
- [Decision 2], Rationale: [why]
- [Decision 3], Rationale: [why]

### We will DEFER:
- [Item 1], Revisit: [when/trigger]
- [Item 2], Revisit: [when/trigger]
```

### Step 5: Success Criteria & Review Cadence

```markdown
## Success Criteria
| Bet | Leading Indicator (4 weeks) | Lagging Indicator (quarter) | Target |
|---|---|---|---|
| [Bet 1] | [metric] | [metric] | [target] |
| [Bet 2] | [metric] | [metric] | [target] |

## Review Cadence
- Weekly: [What we check]
- Monthly: [What we assess]
- Quarterly: [Full strategy review, keep/adjust/kill each bet]
```

## Minimum Evidence Bar

**Required inputs:** Target customer definition, at least one known competitive alternative, and enough market context to articulate why now.

**Acceptable evidence:** Customer research (interviews, surveys, usage data), market reports, competitive intel, internal metrics (retention, NPS, revenue trends), prior experiment results.

**Insufficient evidence:** If no customer input exists (zero interviews, no usage data, no support signal), stop and recommend running customer discovery research before attempting this skill. Do not produce strategic bets without customer grounding.

**Hypotheses vs. findings:**
- **Findings:** Strategic Context (current metrics, market trajectory), customer satisfaction assessments
- **Hypotheses:** Strategic Bets (theses are inherently speculative), kill criteria assumptions, must be labeled with "we believe" framing and falsifiability conditions

## Output Format

When an automated handoff or benchmark explicitly requests structured output, also read `docs/structured-artifacts.md` and the matching schema from the Shipwright installation root. Append the validated envelope and keep it consistent with the visible artifact. Ordinary chat output needs no JSON duplicate.

Produce a Product Strategy Document with:
1. **Product Vision**, aspirational north star
2. **Strategic Context**, where we are today
3. **Strategic Bets**, 2-4 focused bets with theses
4. **Strategic Boundaries**, what we're not doing and why
5. **Success Criteria**, metrics and review cadence

**Shipwright Signature (required closing):**
6. **Decision Frame**, Primary strategic bet recommendation with trade-off (focus vs. optionality), confidence with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, Unvalidated assumptions behind bets, missing customer evidence, market data gaps
8. **Pass/Fail Readiness**, PASS if bets have falsifiable theses, explicit boundaries, evidence-backed assumptions and kill criteria. Light depth may condense the evidence and cadence; FAIL if customer grounding or kill criteria are missing.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Strategy as a feature list**, A roadmap is not a strategy; a strategy explains *why* you're building what you're building
- **Too many bets**, If everything is a priority, nothing is
- **No kill criteria**, Without pre-committed exit conditions, every bet becomes permanent
- **Vision too vague**, "Be the best platform" is not a vision; it needs a customer and a differentiated outcome
- **Skipping "what we're NOT doing"**, The power of strategy is in the choices you make *against*

## Weak vs. Strong Output

**Weak:**
> "Bet: Expand to mobile. Thesis: Mobile is growing so we should be there."

No falsifiable claim, no evidence, no kill criteria, this is a wish, not a strategic bet.

**Strong:**
> "Bet: Mobile-first onboarding. Thesis: We believe that shipping a mobile onboarding flow by Q3 will increase Day-7 retention from 35% to 50% because 62% of signups now originate on mobile devices (GA data, Feb 2026). Kill criteria: If Day-7 retention stays below 40% after 6 weeks post-launch, deprioritize and redirect to web activation."

Testable claim, quantified baseline, named data source, pre-committed exit condition.
