---
name: decision-log
description: Structured product decision engine -- takes signal scan output and operator preferences, applies the Signal-to-Decision Pipeline (SDP) framework, and produces a scored, filtered, bias-checked decision record with pre-mortem analysis and kill criteria. Use when choosing which opportunity to pursue from a completed signal scan.
license: MIT
metadata:
  context: fork
  openclaw:
    emoji: "\u2696\uFE0F"
---

# Decision Log

Take signal scan output and operator preferences, run them through the Signal-to-Decision Pipeline (SDP), and produce a structured decision record. Scores opportunities across 6 dimensions, applies strategic filters, checks for cognitive bias, runs a pre-mortem, and outputs a fully logged decision with kill criteria and a next-step hint for persona-extract.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Pipeline Position

```
signal-scan -> **decision-log** -> persona-extract -> offer-scope -> hunter-log
```

This skill consumes the output of `signal-scan` and feeds into `persona-extract` for deep persona research on the chosen opportunity.

## When to Use

- Choosing which opportunity to pursue from a completed signal scan
- Recording a product decision with full rationale and alternatives
- Applying structured scoring to signal-derived opportunities
- Running a pre-mortem before committing to build
- Setting kill criteria and revisit dates for a product bet

## Trigger Phrases

- "Which opportunity should I pursue?"
- "Help me decide what to build from this scan"
- "Run a decision log on [signal scan output]"
- "Log a decision for [opportunity]"
- "/decision-log [signal scan output]"

---

## Prerequisites

Before starting, the following must be available:

1. **Signal scan output** -- A completed signal-scan result containing: scan metadata, signals (all 7 types), scored opportunities with ship candidates, and a meta-signal synthesis
2. **Chosen opportunity** -- Which opportunity from the scan the operator wants to pursue (or ask them to choose after presenting the ranked list)
3. **Rationale** -- Why this opportunity over others (the operator's reasoning, beyond the score)
4. **Constraints** -- Concrete limits: "must ship in 1 day", "PDF only", "under $50", etc.
5. **Alternatives rejected** -- Which other opportunities were considered and why they lost

If only the signal scan is provided, present the ranked opportunities and guide the operator through selection before proceeding.

---

## Input

The skill expects the following input structure (typically assembled from signal-scan output and operator conversation):

```typescript
interface DecisionLogInput {
  signal_scan: SignalScanOutput       // full scan output
  chosen_opportunity: string          // title from opportunities array
  rationale: string                   // why this one
  constraints: string[]               // "must ship in 1 day", etc.
  alternatives_rejected: {
    title: string
    reason: string
  }[]
  confidence: "low" | "medium" | "high"
  revisit_by: string                  // ISO date
}
```

---

## Workflow

```
Signal Scan Output + Operator Preferences
    |
Phase 1: Frame the Decision (what exactly are we deciding?)
    |
Phase 2: Present the Options (from scan opportunities, ranked by score)
    |
Phase 3: Apply SDP Scoring (6-dimension RICE-adapted framework)
    |
Phase 4: Strategic Filters (reversibility check, two-way door bias)
    |
Phase 5: Bias Check (wanting vs. data, confirmation bias audit)
    |
Phase 6: Pre-Mortem (imagine failure -- why did it happen?)
    |
Phase 7: Make the Call (record chosen + rejected + rationale)
    |
Phase 8: Set Kill Criteria (when to abandon)
    |
Phase 9: Generate Next-Step Hint (pre-fill persona-extract inputs)
    |
Output: JSON record + Markdown summary -> vault
```

---

## Phase 1: Frame the Decision

**What exactly are we deciding?**

Do not jump to scoring. State the decision explicitly:

- What is the time horizon? ("which opportunity to prototype this week")
- What is the success metric? ("first paying customer within 2 weeks")
- What are the hard constraints? (ship time, format, budget, audience access)

**Produce a decision frame:**

```
Decision: [one-sentence statement of what we are choosing]
Time horizon: [when the bet resolves]
Success metric: [how we know it worked]
Constraints: [non-negotiable limits]
```

Present this to the operator for confirmation before proceeding. A well-framed decision is half-solved.

---

## Phase 2: Present the Options

Pull all opportunities from the signal scan output and present them ranked by their original score.

**For each opportunity, display:**

| Field | Source |
|-------|--------|
| Title | `opportunities[].title` |
| Score | `opportunities[].score` |
| Scoring breakdown | `opportunities[].scoring_breakdown` (all 6 dimensions) |
| Thesis | `opportunities[].thesis` |
| Ship candidate count | `opportunities[].ship_candidates.length` |
| Fastest ship candidate | The ship candidate with the shortest `ship_time` |

Include "do nothing" as an explicit option. It often wins and that is fine.

If the operator has not yet chosen, guide them through selection. If they have already chosen, confirm the choice and proceed.

---

## Phase 3: Apply SDP Scoring

Re-score the chosen opportunity and its top 2-3 alternatives using the Signal-to-Decision Pipeline's 6-dimension framework. This is a fresh scoring pass using the SDP weights, not just a repeat of the signal scan scores.

### SDP Dimensions

| Dimension | Scale | Weight | What It Measures | Evidence Source |
|-----------|-------|--------|------------------|----------------|
| Pain Intensity | 1-5 | 3x | How acute is the problem? Vitamin (1-2) or painkiller (4-5)? | PAIN signals from scan |
| Spend Evidence | 1-5 | 3x | Are people already paying for inferior solutions? | SPEND signals from scan |
| Edge Match | 1-5 | 2x | Does this play to the operator's unique skills? | Operator edge from scan metadata |
| Time to Ship | 1-5 | 2x | How quickly can a testable version reach market? | Ship candidates from scan |
| Competition Gap | 1-5 | 1x | Is there a meaningful opening in the landscape? | COMPETITIVE + SENTIMENT signals |
| Audience Fit | 1-5 | 1x | Does the operator already have access to these people? | AUDIENCE signals from scan |

### SDP Formula

```
SDP Score = (pain x 3) + (spend x 3) + (edge x 2) + (time x 2) + (gap x 1) + (audience x 1)
```

**Range**: 12 (minimum) to 60 (maximum).

### Scoring Rules

- Every dimension score MUST cite specific signals from the scan. No vibes.
- Write one sentence of justification per dimension. Example:
  > Pain Intensity: 4 -- "Three Reddit threads with 100+ upvotes describe spending 4+ hours on this task, with language like 'nightmare' and 'pulling my hair out'"
- Score the chosen opportunity AND the top 2-3 alternatives on the same dimensions for comparison.
- If the chosen opportunity does not score highest, flag this explicitly. The operator may still choose it (edge match, personal interest, strategic positioning), but they should know they are overriding the score.

---

## Phase 4: Strategic Filters

Apply two strategic filters to the chosen opportunity:

### Reversibility Check (Bezos Two-Way Door Test)

**The test**: If this goes wrong, can the operator undo it within 2 weeks with no lasting damage?

For solo creators shipping 1-day builds, the answer is almost always yes. This is a two-way door. Note it explicitly:

> **Reversibility**: Two-way door. A [format] product can be sunset with zero ongoing cost. Bias toward action.

If the answer is no (e.g., the opportunity requires hiring, signing contracts, or building infrastructure), flag it as a one-way door and recommend deeper analysis before committing.

### Power Check (Helmer 7 Powers)

Ask: "If this succeeds, does it create or strengthen a competitive power?"

The most accessible powers for solo creators:
- **Counter-Positioning** -- Does this exploit an incumbent's incentive misalignment?
- **Switching Costs** -- Will users face costs to move away once they adopt?
- **Cornered Resource** -- Is the operator's unique expertise a defensible advantage here?

This is not a veto. Many good first bets create no power at all. But the operator should know whether this builds toward defensibility or is purely a revenue/learning play.

---

## Phase 5: Bias Check

Run an explicit cognitive bias audit. This is the hardest step and the one most people skip.

### Questions to Surface

Present each question and answer it honestly based on the evidence:

1. **Confirmation bias**: "Am I choosing this because the data supports it, or am I highlighting data that supports what I already want to build?"
   - Check: Does the chosen opportunity score highest on SDP? If not, why am I overriding?

2. **Availability bias**: "Am I choosing this because it is top-of-mind or because it is genuinely the best option?"
   - Check: Is this the first opportunity that came to mind, or did it emerge from systematic comparison?

3. **Anchoring**: "Am I anchored to the signal scan's original ranking? Did the SDP re-scoring change anything?"
   - Check: Compare original scan rank to SDP rank. Note any movement.

4. **Excitement bias**: "Would I tell a friend to pursue this, or am I choosing it because I personally find it fun to build?"
   - Check: If the operator's best friend proposed this idea, would the operator honestly say "go for it"?

### Bias Check Output

Summarize as:

```
Bias check: [PASS | FLAG]
Notes: [1-2 sentences on any concerns surfaced]
```

FLAG does not mean stop. It means acknowledge the bias and proceed with eyes open.

---

## Phase 6: Pre-Mortem

Before finalizing, imagine it is 3 months from now and this product has failed. Work backwards: why did it fail?

### Pre-Mortem Rules

- Generate at least 3 distinct failure scenarios
- Each scenario must be specific and plausible, not generic ("the market changed" is too vague)
- At least one scenario must be about execution, not market (e.g., "I ran out of motivation after week 2 because the content was tedious to produce")
- At least one scenario must be about market/demand (e.g., "The pain signals were real but the audience was not willing to pay $29 for a PDF when free blog posts cover 80% of the same ground")
- At least one scenario must be about competition/timing (e.g., "A well-known creator launched a free YouTube series covering the same topic 2 weeks after my launch")

### Pre-Mortem Output

```
Pre-mortem scenarios:
1. [Execution failure]: "..."
2. [Market/demand failure]: "..."
3. [Competition/timing failure]: "..."
[4+. Additional scenarios if warranted]
```

---

## Phase 7: Make the Call

Record the decision formally.

### Decision Record Fields

| Field | Description |
|-------|-------------|
| decision_id | `decision-{domain-slug}-{YYYY-MM-DD}` |
| date | ISO date |
| domain | From signal scan metadata |
| chosen_opportunity | Title of the selected opportunity |
| chosen_opportunity_data | Full opportunity object from the signal scan (title, score, scoring_breakdown, thesis, ship_candidates) |
| rationale | 2-3 sentences on WHY this option won, referencing specific signal data |
| constraints | List of hard constraints provided by the operator |
| alternatives_rejected | Each alternative with: title, rejection reason, SDP score |
| confidence | low / medium / high -- with justification |
| revisit_by | ISO date when the operator will re-evaluate |

### Rationale Rules

- Rationale MUST reference specific signals from the scan (quote, data point, source)
- "It seemed like the best option" is not a rationale
- "It scored highest on pain (4/5 -- three Reddit threads with 100+ upvotes) and spend (5/5 -- Udemy courses at $19-49 with 10K+ students), and I have direct edge from 5 years of DevOps experience" IS a rationale

### Rejection Rules

- Every alternative must have a specific rejection reason
- "It scored lower" is acceptable only if accompanied by which dimensions dragged it down
- If an alternative scored higher on SDP but was not chosen, the rejection reason must explain the override (strategic reasoning, personal constraints, portfolio considerations)

---

## Phase 8: Set Kill Criteria

Define measurable, time-bounded conditions under which the operator abandons this product. These are written BEFORE building so the operator commits to them before emotional investment clouds judgment.

### Kill Criteria Rules

- At least 2 kill criteria, ideally 3-4
- Every criterion must be measurable (a number, a date, or an observable event)
- Every criterion must have a time bound
- Include at least one build-phase criterion (before launch) and one market-phase criterion (after launch)

### Kill Criteria Examples

**Build-phase:**
- "If the prototype takes more than 2 days to build, reduce scope or abandon"
- "If I cannot find 3 real pain quotes to use in positioning copy, the pain signal may be weaker than scored"

**Market-phase:**
- "If the free content post gets fewer than 50 engagements, the audience signal is too weak"
- "If fewer than 5 units sell in the first week at $29, the willingness-to-pay assumption is wrong"
- "If no one emails asking questions or requesting features by day 14, there is no engagement loop"

---

## Phase 9: Generate Next-Step Hint

Pre-fill the inputs for the next pipeline step (persona-extract) so the operator can invoke it immediately without re-assembling context.

### Next-Step Hint Structure

```typescript
{
  next_step: "persona-extract",
  next_step_input_hint: {
    opportunity_title: string,        // chosen opportunity title
    domain: string,                   // domain from scan metadata
    ship_candidates: ShipCandidate[], // ship candidates from chosen opportunity
    key_pain_signals: PainSignal[],   // top 3-5 PAIN signals relevant to chosen opportunity
    key_spend_signals: SpendSignal[]  // top 3-5 SPEND signals relevant to chosen opportunity
  }
}
```

Pull pain and spend signals that are most relevant to the chosen opportunity. These prime persona-extract with the right context to build accurate archetypes.

---

## Output

The decision log produces two files:

### 1. JSON Record

**Vault path**: `Admin/Product-Discovery/Decisions/{domain-slug}-{YYYY-MM-DD}.json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Must validate against that schema.

### 2. Markdown Summary

**Vault path**: `Admin/Product-Discovery/Decisions/{domain-slug}-{YYYY-MM-DD}.md`

Human-readable decision record with the following structure:

```markdown
---
type: decision
date: YYYY-MM-DD
status: active
tags:
  - hunter/decision
  - hunter/domain/{domain-slug}
  - hunter/opportunity/{opportunity-slug}
signal_scan_ref: "{signal-scan-slug}"
---

# Decision: [Chosen Opportunity Title]

**Date**: [date]
**Domain**: [domain]
**Confidence**: [low | medium | high]
**Revisit by**: [date]

## Decision Frame

**Question**: [what exactly we are deciding]
**Time horizon**: [when the bet resolves]
**Success metric**: [how we know it worked]
**Constraints**: [non-negotiable limits]

## Opportunity Ranking (SDP Scores)

| Rank | Opportunity | SDP Score | Pain | Spend | Edge | Speed | Gap | Audience |
|------|------------|-----------|------|-------|------|-------|-----|----------|
| 1 | [name] | [score]/60 | [n] | [n] | [n] | [n] | [n] | [n] |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Chosen: [Opportunity Title] (SDP: X/60)

**Thesis**: [from scan]

**Rationale**: [2-3 sentences referencing specific signal data]

**Ship candidates**:
| Product | Format | Price | Ship Time |
|---------|--------|-------|-----------|
| [name] | [format] | [price] | [time] |

## Strategic Filters

**Reversibility**: [Two-way door | One-way door] -- [reasoning]
**Power potential**: [which power, if any] -- [reasoning]

## Bias Check: [PASS | FLAG]

[Notes on any concerns surfaced]

## Pre-Mortem

1. **[Execution]**: [scenario]
2. **[Market/Demand]**: [scenario]
3. **[Competition/Timing]**: [scenario]

## Alternatives Rejected

### [Alternative 1 Title] (SDP: X/60)
**Rejected because**: [specific reason]

### [Alternative 2 Title] (SDP: X/60)
**Rejected because**: [specific reason]

## Kill Criteria

- [ ] [criterion 1 -- measurable, time-bounded]
- [ ] [criterion 2 -- measurable, time-bounded]
- [ ] [criterion 3 -- measurable, time-bounded]

## Next Step: persona-extract

**Opportunity**: [title]
**Domain**: [domain]
**Key pain signals to investigate**: [top 3-5]
**Key spend signals to anchor**: [top 3-5]

## References

- **Signal Scan**: [[Admin/Product-Discovery/Signal-Scans/{signal-scan-slug}]]
```

---

## Vault Output Contract

Both output files are written to the Obsidian vault (iCloud-synced):

```
${VAULT}/Admin/Product-Discovery/Decisions/
```

- Filename format: `{domain-slug}-{YYYY-MM-DD}.md` and `{domain-slug}-{YYYY-MM-DD}.json`
- If a file already exists at the target path: APPEND under `## Update: {ISO timestamp}`, do NOT overwrite
- Frontmatter MUST include: `type: decision`, `date`, `status: active`, `tags` (minimum: `hunter/decision`)

---

## Resources

### references/

- `output-schema.json` -- JSON Schema for the structured decision log output. Load when producing the JSON file to validate against.

### README.md

- The full Signal-to-Decision Pipeline (SDP) framework reference, including all source frameworks (RICE, Bezos, Vassallo, Duke, Helmer, Kahneman, Torres), detailed case studies, and the complete glossary. Consult for deep framework questions during a decision session.

---

## Quality Checklist

Run this checklist before delivering the decision record:

- [ ] Decision frame explicitly states what is being decided, the time horizon, and the success metric
- [ ] All opportunities from the signal scan are presented with SDP scores (not just the chosen one)
- [ ] Rationale references specific signal data -- quotes, numbers, sources (not vibes)
- [ ] Every alternative has a specific rejection reason (not just "scored lower")
- [ ] SDP dimension scores each have a one-sentence justification citing scan signals
- [ ] If the chosen opportunity did not score highest on SDP, the override is explicitly justified
- [ ] Pre-mortem has at least 3 failure scenarios (execution, market, competition)
- [ ] Kill criteria are measurable and time-bounded (at least one build-phase, one market-phase)
- [ ] Confidence level is justified with reasoning (not just asserted)
- [ ] Revisit date is set and is realistic (not too soon, not too far)
- [ ] Next-step hint is populated with relevant pain and spend signals for persona-extract
- [ ] JSON output validates against `references/output-schema.json`
- [ ] Markdown output has correct frontmatter (type, date, status, tags, signal_scan_ref)
- [ ] Both files are saved to vault `Admin/Product-Discovery/Decisions/`
- [ ] Pipeline kanban updated: move card to "Decision Made" column (see _conventions.md Pipeline Kanban Contract)
