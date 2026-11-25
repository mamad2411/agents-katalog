---
name: stg-segmenting-customers
description: Generates strategic customer segment definitions with observable filters, pain scoring, and compression-model elimination. Use when constructing segment hypothesis during BUILD phase 2.
serves: strategist
domain: customer-segmentation
affects: segment-hypothesis
depends-on: none
produces: segment hypothesis in register format
---

# Customer Segmentation

Generate segment hypothesis using compression model: enumerate candidates, score, eliminate, carry alternatives. All segments defined by observable filters with tier-labeled evidence.

## Procedure

### Step 1: Load Context [S]

Read: market sizing notes (TAM/SAM/SOM), governor problem space description, research signals from BUILD phase 1.

Produce: segment generation parameters (industry focus, market scope, problem type).

**Gate:** `context_loaded: bool` -- market data and problem space available.
- Pass: Step 2.
- Fail: Report which inputs are missing. If market sizing is unavailable, proceed with governor input and research signals, noting reduced confidence.

### Step 2: Enumerate Candidate Segments (Minimum 3) [K-grounded]

**Grounded in:** market data, problem space, research signals.

From market research, identify 3-5 potential customer groups. For each:
- Who they are (role, company type, industry)
- Why they might have the problem (structural reason)
- Rough size from TAM/SAM data

WebSearch for segment-specific signals if needed (job postings, forum activity, tool adoption patterns).

Produce: candidate segment list with initial evidence.

**Gate:** `candidates_enumerated: bool` -- at least 3 candidates identified, each with structural rationale for why they might have the problem.
- Pass: Step 3.
- Fail: If fewer than 3 candidates, broaden scope (adjacent industries, different company sizes, different roles). If still <3, document why the market may be narrower than expected.

### Step 3: Define Observable Filters for Each Candidate [R]

For each segment, identify 2-4 searchable criteria.

| Valid Filters (Observable) | Invalid Filters (Reject) |
|---------------------------|-------------------------|
| Company size (employees, revenue) | "Innovative companies" |
| Industry (NAICS code, vertical) | "Growth-minded founders" |
| Technology used (specific tools, platforms) | "Tech-savvy teams" |
| Geography (region, country) | "Forward-thinking" |
| Behavioral signals (job postings, tool usage) | Any psychographic or subjective filter |
| Funding stage (from Crunchbase) | "Quality-focused" |

For invalid filters, replace with observable proxies:
- "Tech-savvy" -> "uses [specific tools]"
- "Growth-oriented" -> "raised funding in last 12 months" or "headcount grew >20% YoY"

Produce: filtered candidate list. Candidates with only invalid filters are weakened but not eliminated -- flag for governor input.

**Gate:** `filters_defined: bool` -- each candidate has at least 2 observable, searchable filters.
- Pass: Step 4.
- Fail: Candidates without observable filters cannot be targeted. Flag as "segment hypothesis requires governor input to operationalize."

### Step 4: Score Pain Intensity for Each Candidate [R]

For each segment, assess pain signal strength from public data:

| Score | Level | Evidence Required |
|-------|-------|-------------------|
| 5 | Hair-on-fire, actively buying solutions | G2 reviews, competitor traction, job postings for manual workaround roles |
| 4 | Recognized pain, some buying | Forum complaints, budget line items, partial solutions adopted |
| 3 | Latent pain, workarounds common | DIY tools, spreadsheet solutions, occasional complaints |
| 2 | Mild inconvenience | Mentioned but not prioritized |
| 1 | Unaware or accepting | No public signal |

Every score requires cited evidence. No score without signal. If no signal found, score = 1 with note: "no public signal found -- T3 assumption."

Tier labels: scores based on direct observation of behavior (reviews, job postings) = T1. Scores inferred from indirect signals = T2. Scores assumed without signal = T3.

Produce: scored candidate list, each score with evidence and tier label.

**Gate:** `candidates_scored: bool` -- every candidate has a pain score with cited evidence and tier label.
- Pass: Step 5.
- Fail: Candidates without evidence get score 1 (unaware). Do not assign higher scores without signals.

### Step 5: Eliminate Weak Candidates (Compression) [R]

Eliminate candidates that fail on 2+ of:
- Pain score < 3
- Observable filters are insufficient (cannot find them)
- Market size too small (segment x estimated ARPU < operating costs)
- No public signal of the problem in this segment

Record elimination rationale with evidence for each eliminated candidate.

Produce: surviving segments + elimination log.

**Gate:** `compression_complete: bool` -- elimination rationale documented for every eliminated candidate.
- Pass: Step 6.
- Fail: If all candidates eliminated, broaden search. If only 1 survives, note the closest eliminated candidate as "weak alternative."

### Step 6: Select Primary and Carry Alternatives [K-grounded]

**Grounded in:** scored candidates from Steps 4-5.

Primary = highest pain score with adequate market size.

If two segments tie, carry both and flag as governor decision.

At least 1 alternative must survive. If all but one eliminated, note the closest eliminated candidate as "weak alternative."

Produce: segment hypothesis with possibility space (primary, alternatives, eliminated).

**Gate:** `selection_complete: bool` -- primary identified, at least 1 alternative carried.
- Pass: Step 7.
- Fail: If no alternative can be carried, document: "Single viable segment identified. Compression model produced no alternatives. This is a concentration risk."

### Step 7: Write Hypothesis [S]

Write complete segment hypothesis in register format:

- **Claim:** One paragraph -- who has this problem acutely, observable characteristics. Use behavioral language, not demographic generalization.
- **Evidence:** Tier-labeled evidence items from scoring.
- **Possibility Space:** Candidates considered, eliminated (with rationale), alternatives carried.
- **Assumptions:** What must be true about this segment (each with tier label, load-bearing flag, blast radius).
- **Kill Condition:** What would prove this is the wrong segment. Must be specific and observable (not "segment doesn't work"). Example: "Interviews with 5 [segment] companies reveal <2/5 experience this problem weekly."

Produce: complete segment hypothesis in register format.

**Gate:** `hypothesis_written: bool` -- all fields populated, kill condition is specific and observable.
- Pass: Done.
- Fail: Fix the missing or vague field.

## Quality Criteria

- Minimum 3 candidate segments considered (possibility space recorded)
- At least 1 alternative carried (not just the winner)
- Every segment defined by observable, searchable filters (no psychographics)
- Pain scores backed by cited evidence with tier labels
- Elimination rationale documented for every eliminated candidate
- Kill condition is specific and observable (not "segment doesn't work")
- Claim uses behavioral language, not demographic generalization

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Single-player assumption | Primary segment matches governor's own profile exactly | Flag to governor: "You may be designing for yourself. Is this segment defined by your characteristics or by market evidence?" Carry an alternative that explicitly differs from governor profile |
| Psychographic filters masquerading as observable | Filters include "tech-savvy", "growth-oriented", "innovative" | Replace with observable proxies: "tech-savvy" -> "uses [specific tools]"; "growth-oriented" -> "raised funding in last 12 months" or "headcount grew >20% YoY" |
| Pain score without evidence | Score assigned but evidence field is empty or says "likely" / "probably" | WebSearch for specific signals. If no signals found, score = 1 (unaware) with note: "no public signal found -- T3 assumption" |
| Anchoring on first segment | First segment listed gets highest score; alternatives feel perfunctory | Re-score with the second segment as the assumed primary. Does the scoring change? If not, anchoring is not the issue. If yes, the scores are framing-dependent -- carry both |

## Boundaries

**In scope:** Segment enumeration, observable filter definition, pain scoring with evidence, compression-model elimination, possibility space recording, hypothesis writing in register format.

**Out of scope:** Market sizing (stg-sizing-markets), problem scoring (stg-scoring-problems), competitive analysis (stg-analyzing-competition), customer validation interviews.
