---
name: stg-extracting-insights
description: Processes governor-provided expert sources into structured, tier-labeled insights that feed the hypothesis register as evidence. Use when governor provides a book, article, video, or podcast for processing.
serves: strategist
domain: knowledge-extraction
affects: all-hypotheses
depends-on: none
produces: tier-labeled evidence items for register integration
---

# Insight Extraction

Process governor-provided expert sources into structured, tier-labeled insights. Every extracted claim carries a tier label and maps to a specific hypothesis. Behavioral vs hypothetical evidence distinction maintained throughout.

## Procedure

### Step 1: Ingest Source [S]

Read: source URL, file, or transcript (governor-provided).

- If URL: WebFetch to retrieve content.
- If file: Read file content.
- If transcript: Read transcript.

Identify structure (chapters, sections, speakers). Capture metadata: date, author, platform, publication context.

Produce: raw content + metadata.

**Gate:** `source_ingested: bool` -- content retrieved, metadata captured (date, author).
- Pass: Step 2.
- Fail: If URL returns error, report to governor. If content is gated/paywalled, report: "Cannot access -- governor must provide content directly."

### Step 2: Extract Claims and Frameworks [K-grounded]

**Grounded in:** raw content from Step 1.

Identify and extract:

| Category | What to Look For | Example |
|----------|-----------------|---------|
| Frameworks | Mental models, decision structures | "The 4 properties of a good problem" |
| Principles | Universal rules, guidelines | "Never price below 10x the cost of the alternative" |
| Tactics | Specific actions, playbooks | "Use 5-second tests to validate landing page messaging" |
| Data points | Benchmarks, metrics, statistics | "Average PLG conversion rate is 3-5%" |
| Warnings | Anti-patterns, failure modes | "Teams that skip problem validation fail 3x more often" |

For each: state the claim, cite the specific quote or passage (with location/timestamp if applicable), note the context.

Produce: extracted claims list.

**Gate:** `claims_extracted: bool` -- at least 3 claims extracted, each with specific citation from source.
- Pass: Step 3.
- Fail: If source is too thin for 3 claims, extract what exists and note: "Source produced limited actionable claims."

### Step 3: Tier-Label Each Claim [R]

For each claim, apply the operational test: "What new data would I need to see to change my mind about this?"

| Answer | Tier | Example |
|--------|------|---------|
| "None -- this is definitional or from cited data" | T1 | "SaaS gross margins are typically 70-85%" (from benchmark report) |
| "Validate the reasoning chain" | T2 | "Teams with this problem spend 40% of time on workarounds" (expert estimate) |
| "Customer/market data I don't have" | T3 | "Customers will pay 10x for this solution" (expert opinion about WTP) |

Also distinguish:
- **Behavioral evidence:** "We observed X happen" -- stronger
- **Hypothetical evidence:** "X should work because Y" -- weaker

Produce: tier-labeled claims.

**Gate:** `claims_labeled: bool` -- every claim has tier label and behavioral/hypothetical classification.
- Pass: Step 4.
- Fail: Claims without clear tier are likely T2 or T3. Default to T2 for reasoning, T3 for predictions.

### Step 4: Map to Hypotheses [R]

For each claim, determine which hypothesis it supports or challenges:

| Mapping Target | Evidence About |
|---------------|---------------|
| Problem hypothesis | Pain existence, frequency, severity, alternatives |
| Segment hypothesis | Who has the problem, observable characteristics |
| Unit Economics hypothesis | Pricing, costs, conversion rates, benchmarks |
| Solution Design | Features, growth architecture, MVP approach, positioning, differentiation, jobs-to-be-done |
| General | Domain knowledge, not hypothesis-specific |

Explicitly search for claims that contradict current register. Challenging evidence is more valuable than confirming evidence.

Produce: hypothesis-mapped claims.

**Gate:** `claims_mapped: bool` -- every claim mapped to at least one hypothesis or marked "General."
- Pass: Step 5.
- Fail: If all claims map to "General," the source may not be relevant to current strategy work. Report to governor.

### Step 5: Write Outputs [S]

For hypothesis-specific insights: format as EvidenceItems:
- [{TYPE: WEB_RESEARCH or OBSERVATION}] [{T1|T2|T3}] {date} -- {source}: {detail}
- Note which hypothesis they should be added to

For general insights: write to `knowledge/` as standalone file if source is broadly relevant.

The agent integrates evidence items into the register on the next BUILD/CHALLENGE pass.

Produce: evidence items for register integration + optional knowledge file.

**Gate:** `outputs_written: bool` -- evidence items formatted for register integration, each with hypothesis target.
- Pass: Done.
- Fail: Ensure every output has the required format fields: type, tier, date, source, detail.

## Quality Criteria

- Every extracted claim cites specific passage from source (not paraphrased without reference)
- Tier labels applied to every claim with justification
- Behavioral vs hypothetical distinction maintained (quotes about what happened vs what should happen)
- Claims mapped to specific hypotheses (not all dumped as "general")
- Source metadata complete (date, author, URL if applicable)

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Uncritical extraction | All claims extracted as T1 or all labeled as important | Apply tier test rigorously. Expert opinion about what customers want is still T3. Expert frameworks are T2. Only cited data is T1 |
| Confirmation bias in extraction | Only insights supporting existing hypotheses extracted; challenging insights omitted | Explicitly search for claims that contradict current register. Challenging evidence is more valuable than confirming evidence |
| Quote without context | Extracted quote is stripped of qualifying language that changes its meaning | Include surrounding context. "This works" may have been preceded by "In enterprise markets above $50K ACV" -- the qualifier matters |

## Boundaries

**In scope:** Source ingestion (URL, file, transcript), claim extraction (frameworks, principles, tactics, data points, warnings), tier labeling, behavioral/hypothetical classification, hypothesis mapping, evidence item formatting.

**Out of scope:** Autonomous web research (strategist does this directly), competitive analysis (stg-analyzing-competition), market sizing (stg-sizing-markets), hypothesis construction (skills handle their own domains).
