---
name: competitive-analysis-frameworks
description: Structured frameworks for competitive intelligence, gap analysis, and market positioning. Use when mapping the competitive landscape, building feature comparison matrices, or defining differentiation strategy.
---

# Competitive Analysis Frameworks

Competitive analysis done poorly produces a table of features and a shrug. Done well, it produces a clear picture of where the market is going, where gaps exist, and where to play. This skill covers the core frameworks for structured competitive intelligence.

## When to Use This Skill

- Mapping the competitive landscape before defining product strategy
- Identifying feature gaps against specific competitors
- Positioning a product against alternatives in the market
- Assessing whether a market is attractive to enter or expand in
- Evaluating the defensibility of a current product position

## Core Concepts

### 1. Table Stakes vs. Differentiators

Every feature falls into one of three categories:

- **Table stakes:** Features every competitor has. Not having them is a dealbreaker; having them wins nothing.
- **Differentiators:** Features that drive preference when table stakes are met. These are where to compete.
- **Unique advantages:** Features only you have, especially if hard to copy.

Focus competitive analysis on differentiators and unique advantages — not on catching up on table stakes unless you're currently below the competitive floor.

### 2. Direct vs. Indirect Competitors

- **Direct:** Same target user, same core job-to-be-done, similar solution
- **Indirect:** Different solution to the same job-to-be-done, or same solution targeting a different segment
- **Substitutes:** Non-product alternatives (spreadsheets, manual processes, doing nothing)

Include substitutes. Users don't always switch from product to product — sometimes they stop using products altogether.

### 3. Point-in-Time vs. Trajectory

A competitor's current feature set matters less than where they're going. Analyze:
- What have they shipped in the last 6–12 months?
- What are their job listings signaling about investment areas?
- What do their pricing changes suggest about business model evolution?

## Feature Comparison Matrix

### Construction

1. Define the feature dimensions (rows) — group by capability area, not individual features
2. List competitors (columns) — include your product
3. Score each cell: ✓ (has it), ~ (partial), ✗ (missing), ? (unknown)
4. Add a "Weight" column: High / Medium / Low importance to target user

```
| Capability         | Weight | Us | Competitor A | Competitor B | Competitor C |
|--------------------|--------|----|--------------|--------------|--------------|
| [Feature group 1]  | High   | ✓  | ✓            | ~            | ✗            |
| [Feature group 2]  | High   | ✗  | ✓            | ✓            | ✓            |
| [Feature group 3]  | Medium | ✓  | ✗            | ✗            | ✓            |
| [Feature group 4]  | Low    | ~  | ✓            | ✗            | ~            |
```

### Gap Scoring

For each gap (where Us = ✗ or ~ and competitors = ✓):
- **Gap severity:** Critical (blocking deals), Important (losing deals), Nice-to-have
- **Effort to close:** High / Medium / Low
- **Strategic priority:** Should we close this gap, leapfrog it, or accept it?

## Porter's Five Forces

Use to assess market attractiveness before entering or expanding.

| Force | Key Questions | Implication |
|-------|--------------|-------------|
| **Competitive rivalry** | How many competitors? How differentiated? Price competition? | High rivalry = margin pressure |
| **Threat of new entrants** | How hard to enter? Capital requirements? Switching costs? | Low barriers = future competition risk |
| **Threat of substitutes** | Can users meet their need another way? | High substitutability = pricing ceiling |
| **Supplier power** | Do key vendors / platforms have leverage over you? | High supplier power = cost risk |
| **Buyer power** | Can customers easily switch? Are they concentrated? | High buyer power = margin pressure |

## Positioning Map

Plot competitors on two axes most relevant to the target segment. Common axis pairs:

- **Price vs. Capability** — where are the premium and budget tiers?
- **Breadth vs. Depth** — generalists vs. specialists
- **Self-serve vs. Managed** — automation vs. human service
- **Enterprise vs. SMB** — segment focus

```
                    High Capability
                          │
              B           │        C
                          │
  Low Price ──────────────┼────────────── High Price
                          │
              A           │        Us
                          │
                    Low Capability
```

Identify whitespace — positions no competitor currently occupies that your target users would value.

## Competitive Intelligence Sources

| Source | Signal Type | Reliability |
|--------|-------------|-------------|
| Product itself (sign up, use it) | Feature capabilities, UX quality | High |
| Pricing pages | Business model, tier structure | High |
| Job listings | Investment areas, tech stack, scale | Medium-High |
| App store reviews | User pain points, satisfaction | Medium |
| G2 / Capterra / Trustpilot | Strengths, weaknesses, comparison reasons | Medium |
| Press releases / blog posts | Strategic direction, partnerships | Medium |
| LinkedIn employee count trend | Growth/contraction trajectory | Medium |
| Crunchbase funding history | Resources, investor expectations | Low-Medium |

## Structured Output: Competitive Brief

```
# Competitive Brief: [Market/Feature Area]

## Competitive Landscape
[3-5 sentence summary of the market structure]

## Competitor Profiles
### [Competitor Name]
- Positioning: [1 sentence]
- Strengths: [2-3 bullet points]
- Weaknesses: [2-3 bullet points]
- Recent moves: [what they've shipped or announced]

## Gap Analysis
| Gap | Severity | Effort | Recommendation |
|-----|----------|--------|----------------|
| [Gap 1] | Critical | High | Close — required to compete |
| [Gap 2] | Important | Low | Close — quick win |
| [Gap 3] | Nice-to-have | Medium | Deprioritize |

## Our Position
- Current advantages: [what we have that others don't]
- Vulnerable areas: [where we're exposed]
- Recommended strategy: [where to play and how to win]
```

## Best Practices

1. **Date your data** — competitive data goes stale; always note when it was collected
2. **Don't copy everything** — a gap doesn't always need to be closed; sometimes it's a strategic choice
3. **Validate with users** — feature parity gaps matter more if customers are actually asking for them
4. **Track trajectory** — update the matrix quarterly; a static snapshot misleads
5. **Include substitutes** — users switching away from your category is a competitive threat too
