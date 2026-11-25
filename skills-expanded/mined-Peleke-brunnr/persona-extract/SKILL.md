---
name: persona-extract
description: Persona extraction engine -- takes decision-log output and signal scan data, then produces deep persona research with real stories, decision points, Four Forces analysis, and offer mapping. Uses web search to find real evidence. Use when converting validated market signals into evidence-based buyer personas grounded in real stories.
license: MIT
metadata:
  context: fork
  openclaw:
    emoji: "\U0001F464"
---

# Persona Extract

Transform decision-log output and signal scan data into deep, evidence-based buyer personas using the Signal-to-Story Pipeline. Produces structured JSON and human-readable markdown with real pain stories, success stories, decision point maps, Four Forces analysis, and next-step hints for offer-scope.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Pipeline Position

```
signal-scan -> decision-log -> **persona-extract** -> offer-scope -> hunter-log
```

This skill consumes the output of `decision-log` (and references `signal-scan` data), and feeds into `offer-scope` for product scoping.

## When to Use

- Converting validated market signals into buyer personas
- Building evidence-based archetypes from real community stories
- Mapping decision points where a product could intervene
- Understanding who is in a market, what they want, and how they buy
- Preparing persona data for offer-scope to generate a build spec

## Trigger Phrases

- "Extract personas for [opportunity]"
- "Who is the buyer for [domain/opportunity]?"
- "Run persona extraction on this decision"
- "Build personas from this signal scan"
- "/persona-extract [decision-log output]"

---

## Prerequisites

Before starting, the following must be available:

1. **Decision-log output** -- A completed decision-log result with domain, opportunity title, and supporting signal data
2. **Signal data** -- Pain signals, spend signals, and behavior signals from the upstream signal scan
3. **Ship candidates** -- Candidate products identified by the signal scan or decision log

If any of these are missing, prompt the user to run the upstream skill first or provide the data manually.

---

## Input

The skill expects the following input structure (typically assembled from upstream skill outputs):

```typescript
interface PersonaExtractInput {
  decision: DecisionLogOutput         // or relevant subset
  domain: string
  opportunity_title: string
  pain_signals: PainSignal[]
  spend_signals: SpendSignal[]
  behavior_signals: BehaviorSignal[]
  ship_candidates: ShipCandidate[]
}
```

---

## Workflow

```
Decision-Log Output + Signal Data (from upstream skills)
    |
Phase 1: Opportunity Definition (frame the research)
    |
Phase 2: Evidence Collection (web search -- real data REQUIRED)
    |
Phase 3: Pain Story Collection (verbatim quotes, real attributions)
    |
Phase 4: Success Story Collection (what winners did differently)
    |
Phase 5: Decision Point Mapping (forks in the road)
    |
Phase 6: Four Forces Analysis (Moesta's push/pull/anxiety/habit)
    |
Phase 7: Persona Clustering (3-4 evidence-based archetypes)
    |
Phase 8: Offer Mapping (decision points -> product interventions)
    |
Phase 9: Next-Step Hint Generation (prepare input for offer-scope)
    |
Output: JSON + Markdown -> vault
```

---

## Phase 1: Opportunity Definition

Start with the decision-log output. Extract and confirm:

- **Domain**: The space being explored (e.g., "DevOps education")
- **Opportunity**: The specific opportunity title from the decision log
- **Hypothesis**: Who might care about this and why (drawn from signal data)
- **Research targets**: Which communities, subreddits, forums, and platforms to search

Present a research plan to the user before proceeding. This prevents wasted search effort on the wrong communities.

---

## Phase 2: Evidence Collection

**This phase requires extensive web search. No hallucinated evidence. No personas from memory.**

Search systematically across the following sources for the domain and opportunity:

| Source | What to Collect | Why |
|--------|----------------|-----|
| Reddit (relevant subreddits) | Pain language, "I wish..." posts, rants, workarounds, recommendations | Raw emotional evidence, real language |
| Hacker News | Technical frustrations, tool complaints, career anxiety threads | Senior/experienced perspective |
| DEV.to / Hashnode | Blog posts about struggles, "what I learned" retrospectives | Narrative-rich stories |
| Stack Overflow / forums | Repeated questions, workarounds, duct-tape solutions | Behavior signals |
| Twitter/X | Viral threads, complaints, hot takes, engagement patterns | Real-time sentiment |
| Discord / Slack communities | Direct requests, topic resonance, engagement patterns | Community-specific pain |
| Review sites (G2, Capterra) | 2-3 star reviews especially -- where the nuance lives | Switching intent, feature gaps |
| Amazon reviews | Reviews of competing books/courses in the space | Learning journey pain |

### Collection Rules

- Search for pain language: "I wish...", "I'm so frustrated...", "Why can't someone just...", "I spent X hours trying to..."
- Search for emotional content: anger, desperation, relief, triumph
- Search for specific failures: "I broke production because...", "I failed the interview when..."
- **Every piece of evidence must be a real quote from a real post** -- include username/attribution when available
- Collect at least 15-20 raw stories across sources before proceeding to clustering
- Note the platform, date/recency, and engagement metrics (upvotes, replies) when possible
- Do NOT summarize. Copy verbatim. Their language IS your data.

---

## Phase 3: Pain Story Collection

From the raw evidence, extract structured pain stories. Each story captures one person's struggle.

**Per pain story, capture:**

| Field | Description | Rule |
|-------|-------------|------|
| situation | What was happening when the pain occurred | Specific context, not abstract |
| pain | What hurt -- the actual problem experienced | In their words |
| current_workaround | What they do instead of a real solution | Reveals product opportunity |
| emotional_state | How they feel about it | Use their emotional language |
| evidence | The REAL quote with attribution | Must be an actual quote from an actual post |

### Pain Story Rules

- Minimum 3 pain stories per persona (9+ total across all personas)
- Every story must have a real quote in the evidence field
- Attribution format: `"quote text" -- u/username on r/subreddit (N upvotes)` or `"quote text" -- @handle on Twitter` or `"quote text" -- [platform] user`
- If you cannot find real evidence for a pain story, do not fabricate one. Note the gap and search more.

---

## Phase 4: Success Story Collection

Not everyone is stuck. Find the people who made it through and study what they did differently.

**Per success story, capture:**

| Field | Description | Rule |
|-------|-------------|------|
| situation | Where they started -- what struggle they faced | Must match a pain story pattern |
| what_they_did | The specific actions that led to the breakthrough | Actions, not mindset shifts |
| outcome | What changed as a result | Concrete, measurable when possible |
| evidence | The REAL quote with attribution | Must be an actual quote |

### Success Story Rules

- Minimum 2 success stories per persona
- Look for: "What finally clicked for me was...", "The thing that changed everything was...", "After I stopped X and started Y..."
- Success stories reveal the product intervention point -- the thing that could help stuck people take the success path

---

## Phase 5: Decision Point Mapping

Every journey from struggle to success has forks in the road. Map the critical decision points where some people succeed and others stay stuck.

**Per decision point, capture:**

| Field | Description |
|-------|-------------|
| trigger | What starts the search -- the event that moves someone from passive to active |
| stuck_behavior | What the people who remain stuck do at this fork |
| success_behavior | What the people who break through do at this fork |
| product_intervention | What product could help the stuck person take the success path |

### Decision Point Rules

- Each persona should have at least 2 decision points
- Triggers must be specific events, not vague states ("failed a production deploy" not "feels frustrated")
- Product interventions must be specific enough for offer-scope to act on (format, content type, delivery mechanism)

---

## Phase 6: Four Forces Analysis

Apply Bob Moesta's Four Forces model across all collected evidence. This is a global analysis across all personas, not per-persona.

| Force | Question | Source |
|-------|----------|--------|
| Push | What is wrong with the current situation? | Pain stories, workarounds, emotional language |
| Pull | What attracts them to a solution? | Success stories, aspirational language, desired outcomes |
| Anxiety | What scares them about buying/switching? | Objections, hesitations, past failures, trust concerns |
| Habit | What keeps them doing nothing? | Default behaviors, free alternatives, inertia patterns |

### Four Forces Rules

- Every force must have at least 3 entries
- Each entry should trace back to specific evidence from the collection phase
- For a switch to happen: Push + Pull must exceed Anxiety + Habit
- The analysis should reveal what to amplify (push, pull) and what to reduce (anxiety, habit) in the eventual offer

---

## Phase 7: Persona Clustering

Group the collected stories into 3-4 distinct persona archetypes. These are behavioral archetypes, NOT demographic groups.

**Per persona, define:**

| Field | Description |
|-------|-------------|
| persona_name | Descriptive name encoding the emotional state or behavior pattern |
| archetype | Short label -- e.g., "The Reluctant Senior", "The Copypaste Engineer", "The Midnight Firefighter" |
| demographics.job_titles | Common job titles for this archetype |
| demographics.experience_range | Years of experience range |
| demographics.salary_range | Approximate salary range (for WTP anchoring) |
| demographics.company_size | Typical company size |
| emotional_state | The dominant emotional experience of this archetype |
| pain_stories[] | 3+ pain stories with real evidence (from Phase 3) |
| success_stories[] | 2+ success stories with real evidence (from Phase 4) |
| decision_points[] | 2+ decision points with interventions (from Phase 5) |
| buying_triggers[] | Specific events that would cause them to search and purchase |
| objections[] | What would make them hesitate, with evidence-based counters |
| willingness_to_pay | Price range, evidence (anchored to SPEND data), and anchor products |
| channels[] | Where they spend time, their behavior on each platform, estimated reach |

### Clustering Rules

- Minimum 3 personas, maximum 4
- Personas must be distinct -- if two personas have the same pain stories and decision points, merge them
- Every persona must have at least 3 pain stories with real evidence
- Archetype names should be memorable and encode the behavioral pattern
- Demographics serve WTP anchoring and channel targeting -- they are NOT the primary clustering dimension

---

## Phase 8: Offer Mapping

For each persona's decision points, map potential product interventions.

**Per intervention, consider:**

- **Format**: Must match the persona's consumption context (2 AM incident = checklist, not course)
- **Language**: Use the persona's exact pain language from collected evidence
- **Price anchor**: Derived from SPEND data and the persona's willingness-to-pay
- **Channel**: Where the persona would discover this product

This phase produces the raw material that offer-scope will refine into a full build spec.

---

## Phase 9: Next-Step Hint Generation

Generate a structured hint for the downstream offer-scope skill. This selects the highest-value path from the persona data.

**The hint must include:**

| Field | Description |
|-------|-------------|
| top_persona | The persona with the strongest pain + highest WTP -- the best first target |
| top_decision_point | The single decision point with the highest composite of pain intensity, urgency, and WTP |
| willingness_to_pay | The WTP data for the top persona, anchored to SPEND evidence |
| best_channel | The channel where the top persona is most reachable and most receptive |

---

## Output

The extraction produces two files:

### Vault Output

Save to: `Admin/Product-Discovery/Personas/{domain-slug}-{YYYY-MM-DD}.md`

Vault path: `${VAULT}/Admin/Product-Discovery/Personas/`

### 1. JSON: `persona-extract-[domain-slug]-[date].json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Must validate against that schema.

### 2. Markdown Summary

Human-readable report with the following sections:

```markdown
---
type: persona
date: YYYY-MM-DD
status: complete
tags:
  - hunter/persona
  - hunter/domain/{domain-slug}
  - hunter/opportunity/{opportunity-slug}
decision_ref: "{decision-slug}"
signal_scan_ref: "{signal-scan-slug}"
---

# Persona Extract: [Opportunity]

**Date**: [date]
**Domain**: [domain]
**Opportunity**: [opportunity]

## Meta Insight

[The overarching persona insight -- what connects all these people]

## Persona Summary

| Persona | Archetype | Emotional State | Top Pain | WTP |
|---------|-----------|-----------------|----------|-----|
| [name] | [archetype] | [state] | [pain] | [range] |
| ... | ... | ... | ... | ... |

## Personas

### 1. [Persona Name] -- "[Archetype]"

**Demographics**: [job titles] | [experience] | [salary] | [company size]
**Emotional State**: [description]

#### Pain Stories

**Story 1**: [situation]
- **Pain**: [pain]
- **Workaround**: [current workaround]
- **Emotional State**: [how they feel]
- **Evidence**: "[real quote]" -- [attribution]

[... repeat for each story]

#### Success Stories

**Story 1**: [situation]
- **What they did**: [actions]
- **Outcome**: [result]
- **Evidence**: "[real quote]" -- [attribution]

#### Decision Points

| Trigger | Stuck Behavior | Success Behavior | Product Intervention |
|---------|---------------|-----------------|---------------------|
| [trigger] | [stuck] | [success] | [intervention] |

#### Buying Triggers

| Trigger | Urgency | Channel |
|---------|---------|---------|
| [trigger] | [level] | [channel] |

#### Objections

| Objection | Counter |
|-----------|---------|
| [objection] | [counter] |

#### Willingness to Pay

**Range**: [range]
**Evidence**: [evidence]
**Anchor Products**: [list]

#### Channels

| Platform | Behavior | Estimated Reach |
|----------|----------|----------------|
| [platform] | [behavior] | [reach] |

### 2. [Next persona...]

## Four Forces Analysis

### Push (What is wrong now)
- [push factor 1]
- [push factor 2]
- [push factor 3]

### Pull (What attracts them to a solution)
- [pull factor 1]
- [pull factor 2]
- [pull factor 3]

### Anxiety (What scares them about buying)
- [anxiety factor 1]
- [anxiety factor 2]
- [anxiety factor 3]

### Habit (What keeps them doing nothing)
- [habit factor 1]
- [habit factor 2]
- [habit factor 3]

## Next Step: offer-scope

**Top Persona**: [name]
**Top Decision Point**: [trigger + intervention]
**Willingness to Pay**: [range + evidence]
**Best Channel**: [platform + behavior]

## References

- **Decision Log**: [[Admin/Product-Discovery/Decisions/{decision-slug}]]
- **Signal Scan**: [[Admin/Product-Discovery/Signal-Scans/{signal-scan-slug}]]
```

---

## Resources

### references/

- `output-schema.json` -- JSON Schema for the structured persona extraction output. Load when producing the JSON file to validate against.

### README.md

- Full methodology reference: The Signal-to-Story Pipeline, Four Forces model, Sales Safari, JTBD, 5 Rings of Buying Insight, buyer psychology glossary, case studies. Load when you need deeper context on frameworks or terminology.

---

## Quality Checklist

Run this checklist before delivering the extraction:

- [ ] All personas have real evidence -- every pain/success story includes an actual quote with attribution
- [ ] No hypothetical personas -- all archetypes are derived from observed stories, not imagination
- [ ] Web search was used in Phases 2-4 -- this skill cannot work from memory alone
- [ ] Minimum 3 personas, each with minimum 3 pain stories with evidence
- [ ] Four Forces analysis covers all 4 quadrants with at least 3 entries each
- [ ] Decision points map to specific product interventions (format + content type + delivery)
- [ ] Buying triggers include the channel where the persona would be when triggered
- [ ] Objections have evidence-based counters, not generic dismissals
- [ ] Willingness to pay is anchored to SPEND data from the signal scan, not guesses
- [ ] Channels include specific platforms with behavior descriptions and reach estimates
- [ ] Next-step hint is populated with the highest-value persona, decision point, WTP, and channel
- [ ] JSON output validates against `references/output-schema.json`
- [ ] Markdown output includes correct frontmatter (type, date, status, tags, refs)
- [ ] Markdown is saved to vault at `Admin/Product-Discovery/Personas/`
- [ ] All upstream references (decision_ref, signal_scan_ref) are linked
- [ ] Pipeline kanban updated: move card to "Persona Researched" column (see _conventions.md Pipeline Kanban Contract)
