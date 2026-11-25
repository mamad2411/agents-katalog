---
name: stg-analyzing-competition
description: Maps competitive landscape, identifies positioning gaps, and assesses competitor response capability for red-team input. Use when researching competition during BUILD phase 1 or feeding destruction phase.
serves: strategist
domain: competitive-analysis
affects: problem-hypothesis, unit-economics-hypothesis, solution-design-section
depends-on: none
produces: competitive landscape notes and red-team intelligence for hypothesis register
---

# Competitive Analysis

Map competitive landscape, identify positioning gaps, and assess competitor response capability. All competitive claims carry tier labels. Output feeds hypothesis evidence across the register.

## Procedure

### Step 1: Build Competitive Frame [K-grounded]

**Grounded in:** problem candidates, segment candidates.

Define competitive frame from problem + segment intersection. Competition is framed by what problems you solve for whom, not by technology similarity.

Produce: competitive frame definition (problem domain x target segment = competitive arena).

**Gate:** `frame_defined: bool` -- competitive frame states problem and segment, not just technology category.
- Pass: Step 2.
- Fail: If problem/segment not yet defined, use governor's problem space as initial frame. Note that competitive frame may need revision after hypothesis construction.

### Step 2: Identify Direct Competitors [S]

WebSearch for companies solving the same problem for the same segment.

Search strategies:
- "[Problem] software"
- "[Problem] solution for [segment]"
- "Alternative to [known competitor]"
- G2/Capterra category pages
- Product Hunt searches
- Crunchbase industry filters

Data sources: G2, Capterra, Product Hunt, Crunchbase, company websites.

For each competitor:
- Positioning (headline/tagline from website)
- Target segment (from marketing copy)
- Pricing model (from pricing page)
- Key differentiators (from feature pages)

All claims cite source URL. Label T1 (directly observable on website).

Produce: direct competitor profiles.

**Gate:** `direct_competitors_identified: bool` -- at least 3 direct competitors identified with source URLs, or documented that fewer exist with evidence of search exhaustion.
- Pass: Step 3.
- Fail: Widen search. Try adjacent categories, broader problem framing. If genuinely no direct competitors, document: "No direct competitors found -- this is either a new category or the search missed them."

### Step 3: Identify Indirect Competitors [R]

Classify alternatives into types:

| Type | Example | Evidence Source |
|------|---------|----------------|
| Manual process | Spreadsheets, email, paper | Forum posts, job descriptions |
| Adjacent product | Feature in larger platform | Product feature pages |
| Service provider | Consultants, agencies | Service marketplace listings |
| DIY solution | Internal tools, scripts | GitHub repos, forum posts |
| Status quo | Do nothing | Inferred from lack of solution adoption |

For each: how used, why inadequate. Label T1 for existence, T2 for inadequacy assessment.

Produce: indirect competitor map with all 5 types evaluated (even if "not applicable" for some).

**Gate:** `indirect_competitors_mapped: bool` -- all 5 types evaluated.
- Pass: Step 4.
- Fail: The most common "competitor" is doing nothing or using spreadsheets. Always evaluate status quo and DIY alternatives. If these are missing, add them.

### Step 4: Build Positioning Matrix [K-grounded]

**Grounded in:** direct competitor profiles, problem candidates.

For each direct competitor, map:
- Which problems they address
- Which segments they target
- Price range
- Key strength
- Key weakness

Identify gaps:
- Problems unaddressed by any competitor
- Segments underserved by existing solutions
- Price points uncovered (premium or value end)

Produce: positioning matrix with gap analysis. Label T1 for observable facts, T2 for gap identification.

**Gate:** `matrix_built: bool` -- at least 1 gap identified, or documented "no gaps found -- market is saturated" as a finding.
- Pass: Step 5.
- Fail: If no gaps visible, the market may genuinely be saturated. This is a finding, not a failure. Report it.

### Step 5: Assess Competitor Response Capability (Red-Team Input) [K-grounded]

**Grounded in:** top 2-3 direct competitors from Step 2.

For each:
- **Resource level:** Funding raised, team size (from Crunchbase, LinkedIn). Label T1.
- **Product velocity:** Feature release frequency (from changelogs, Product Hunt, release notes). Label T1.
- **Strategic focus:** Inferred from hiring patterns (LinkedIn jobs), blog posts, conference talks. Label T2.

This feeds the strategist's destruction phase red-team mechanism: "You are the incumbent. A startup launched with this VP targeting your customers. What do you do in 90 days?"

Produce: competitor response profiles. Label T2 (inferred from public signals).

**Gate:** `response_capability_assessed: bool` -- at least 2 competitors profiled with resource level, product velocity, and strategic focus.
- Pass: Done.
- Fail: If competitor data is thin, note: "Competitor response assessment is low-confidence (T2-T3). Red-team should assume capable response."

## Quality Criteria

- Minimum 3 direct competitors identified (or documented that fewer exist with evidence)
- All 5 indirect competitor types evaluated (even if "not applicable" for some)
- Every competitor claim cites a specific source with URL
- Positioning matrix identifies at least 1 gap (or documents "no gaps found -- market is saturated" as a finding)
- Competitor response profiles include resource level, product velocity, and strategic focus
- Tier labels on every claim (T1 for observable facts, T2 for inferred strategy)

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Fabricated competitors | Competitor names that return no results on WebSearch | Remove. Only include verifiable competitors |
| Straw man competitors | All competitors described as weak, slow, or poorly positioned | Re-evaluate with adversarial frame: "What would a smart investor see as the incumbent advantage?" Report competitor strengths honestly |
| Missing the real competition | Competitor list is only direct SaaS competitors; status quo and manual processes ignored | The most common "competitor" is doing nothing or using spreadsheets. Always evaluate status quo and DIY alternatives |

## Boundaries

**In scope:** Direct competitor identification, indirect competitor mapping (5 types), positioning matrix with gap analysis, competitor response capability assessment, source citation, tier labeling.

**Out of scope:** Market sizing (stg-sizing-markets), segment definition (stg-segmenting-customers), problem scoring (stg-scoring-problems), pricing design (stg-designing-pricing).
