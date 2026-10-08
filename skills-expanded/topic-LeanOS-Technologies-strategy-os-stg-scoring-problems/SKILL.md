---
name: stg-scoring-problems
description: Scores problem candidates using four-property framework (frequency, severity, breadth, alternatives' inadequacy) with compression-model elimination. Use when constructing problem hypothesis during BUILD phase 2.
serves: strategist
domain: problem-validation
affects: problem-hypothesis
depends-on: none
produces: problem hypothesis in register format
---

# Problem Scoring

Score problem candidates using four-property framework with compression-model elimination. Every score carries a tier label and cited evidence. Output is a problem hypothesis, not a canvas section.

## Procedure

### Step 1: Load Context [S]

Read: segment hypothesis (or candidates if segment not yet finalized), governor's problem space description, research signals from BUILD phase 1.

Produce: problem generation parameters anchored to segment.

**Gate:** `context_loaded: bool` -- segment context and problem space available.
- Pass: Step 2.
- Fail: Report missing inputs. If no segment data, proceed with governor input alone, noting reduced confidence.

### Step 2: Enumerate Candidate Problems (Minimum 5) [K-grounded]

**Grounded in:** segment context, governor's problem description, research signals.

For the target segment, identify 5-7 candidate problems from:
- Governor input (what they believe the problem is)
- Public signals (forums, reviews, job postings, support tickets)
- Competitive analysis (what alternatives solve -- implies the problem)
- Adjacent segment patterns (problems common in related segments)

WebSearch for segment-specific pain signals.

Produce: candidate problem list.

**Gate:** `candidates_enumerated: bool` -- at least 5 candidates identified from at least 2 different sources.
- Pass: Step 3.
- Fail: If fewer than 5, broaden search to adjacent problem categories. If still <5, document the search strategy used and proceed with available candidates.

### Step 3: Score Each Problem on Four Properties [R]

For each problem, score:

**Frequency (1-5):**

| Score | Meaning | Evidence Type |
|-------|---------|---------------|
| 5 | Multiple times daily | T1 if from workflow analysis; T2 if inferred |
| 4 | Daily | Cite: job descriptions mentioning task, forum post frequency |
| 3 | Weekly | |
| 2 | Monthly | |
| 1 | Rarely | |

**Severity (1-5):**

| Score | Meaning | Evidence Type |
|-------|---------|---------------|
| 5 | Business stops | T2 from public signals; T3 for actual pain intensity |
| 4 | Significant loss | Cite: quantified cost (time, money, risk) if available |
| 3 | Notable pain | Qualitative signal if no quantification |
| 2 | Mild annoyance | |
| 1 | Trivial | |

**Breadth (1-5):**

| Score | Meaning | Evidence Type |
|-------|---------|---------------|
| 5 | >1M potential buyers | T1 if from market sizing; T2 if estimated |
| 4 | 100K-1M | Cross-reference with segment size from stg-segmenting-customers |
| 3 | 10K-100K | |
| 2 | 1K-10K | |
| 1 | <1K | |

**Alternatives' Inadequacy (1-5):**

| Score | Meaning | Evidence Type |
|-------|---------|---------------|
| 5 | No alternatives | T1 for observable alternative landscape |
| 4 | Poor alternatives | T2 for inadequacy assessment |
| 3 | Adequate but painful | Cite specific alternatives and their gaps |
| 2 | Good alternatives exist | |
| 1 | Well-served | |

**Composite** = Frequency x Severity x Breadth x Alternatives_Inadequacy (max 625, useful for ranking, not absolute).

Produce: scored problem matrix with per-property tier labels.

**Gate:** `problems_scored: bool` -- every candidate scored on all four properties, each score cites evidence and carries tier label.
- Pass: Step 4.
- Fail: Scores without evidence are invalid. WebSearch for missing evidence or assign score 1 with "no evidence found" note.

### Step 4: Eliminate Weak Candidates (Compression) [R]

Eliminate problems that score 1-2 on 2+ properties. Record elimination rationale.

If governor's stated problem is eliminated, flag explicitly -- do not silently drop it. Report: "Your stated problem scored [X] but was eliminated because [rationale]. Evidence for alternative [Y] is stronger because [evidence]."

Produce: surviving problems + elimination log.

**Gate:** `compression_complete: bool` -- elimination rationale documented, governor's problem status explicitly stated.
- Pass: Step 5.
- Fail: If all problems eliminated, broaden candidate generation. If governor's problem is the only survivor despite weak evidence, flag potential confirmation bias.

### Step 5: Write Hypothesis [S]

Primary = highest composite score. Write in register format:

- **Claim:** State the problem independent of any solution. "Customers struggle with X" not "customers need a tool that does Y." One paragraph.
- **Evidence:** Tier-labeled evidence items from scoring (per-property evidence).
- **Possibility Space:** All candidates considered, eliminated candidates with rationale, alternatives carried.
- **Assumptions:** What must be true for this problem to be worth solving (each with tier, load-bearing flag, blast radius).
- **Kill Condition:** What would prove this problem is not worth solving. Must reference specific observable thresholds. Example: "Interviews reveal <2/5 people in the segment experience this problem weekly" or "existing alternative achieves >80% satisfaction."

Produce: complete problem hypothesis in register format.

**Gate:** `hypothesis_written: bool` -- claim is solution-independent, kill condition references observable thresholds, possibility space records all candidates.
- Pass: Done.
- Fail: If claim contains solution language, rewrite as pain statement. If kill condition is vague, add specific thresholds.

## Quality Criteria

- Minimum 5 candidate problems enumerated
- Each problem scored on all four properties with tier labels
- Every score cites specific evidence (not "likely high frequency")
- Governor's stated problem is evaluated honestly (not auto-promoted)
- Composite score used for ranking, not as false-precision metric
- Kill condition references specific observable thresholds
- Problem statement is independent of solution ("customers struggle with X" not "customers need a tool that does Y")

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Solution-shaped problem | Problem statement includes solution language ("need a tool", "need a platform") | Rewrite as pain: "teams spend 40 hours building design systems" not "teams need an automated design system generator" |
| Governor's problem auto-promoted | Governor's stated problem has highest score despite weak evidence | Explicitly compare evidence quality between governor's problem and alternatives. If governor's problem has weaker evidence but higher score, flag: "Your stated problem scored highest but evidence is thinner than alternative X. This may be confirmation bias." |
| All problems score similarly | Top 3 problems within 20% of each other | This is useful information, not a failure. Carry all 3 as alternatives. Recommend governor input to distinguish |

## Boundaries

**In scope:** Problem enumeration, four-property scoring with evidence, compression-model elimination, possibility space recording, hypothesis writing in register format.

**Out of scope:** Market sizing (stg-sizing-markets), segment definition (stg-segmenting-customers), competitive mapping (stg-analyzing-competition), solution design (stg-designing-solutions).
