---
name: define-platform-vision
description: >
  Define a platform vision, strategy, and OKRs for an Internal Developer Platform.
  Use when starting a new platform initiative, aligning stakeholders on direction,
  or formalizing an existing platform's purpose. Produces a platform charter document
  with vision statement, strategic pillars, OKRs, capability priorities, and a
  Now/Next/Later roadmap outline.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "2"
---

# Define Platform Vision

## Skill Type

Design

## Your Goal

Produce a **platform charter** — a single document that articulates why the platform exists, what it will achieve, and how success will be measured. The charter should be concrete enough to present to leadership and actionable enough to guide the platform team's first quarter of work.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Organization profile**: Industry, size (number of engineers), number of product/stream-aligned teams, cloud provider(s) in use.
- **Current state**: How do teams deploy today? What tools exist? Where are the biggest pain points? Is there an existing platform or infrastructure team?
- **Business drivers**: What is pushing the organization toward a platform? (e.g., scaling engineering, reducing time-to-market, compliance requirements, cost optimization, reliability concerns)
- **Constraints**: Budget, timeline, team size available for platform work, political or cultural factors (e.g., teams resistant to change, recent failed initiatives).
- **Company objectives**: What are the organization's top-level goals this year? The platform's objectives must cascade from these.

If the user cannot answer all questions, proceed with what is available and note assumptions explicitly in the output.

## Process

### Step 1 — Assess Engineering Momentum

Before proposing a vision, gauge the organization's resistance to change. Consider:

- **Mass**: How many teams, how much legacy tooling, how many entrenched processes?
- **Velocity**: How much delivery pressure exists? Are teams mid-sprint on critical deadlines?

High momentum means the charter must emphasize incremental adoption and quick wins. Low momentum (e.g., a startup or a greenfield initiative) allows for bolder moves. Document the momentum assessment — it shapes everything that follows.

### Step 2 — Draft the Vision Statement

Write a vision statement that is:

- **Inspiring** — it should motivate, not just describe
- **Concise** — one to two sentences maximum
- **Developer-focused** — center it on the people who will use the platform, not the technology

Use this pattern: *"Enable [who] to [do what] by [how], so that [business outcome]."*

Produce two to three variants and explain the trade-offs (developer-centric vs. business-centric framing). Let the user choose or blend.

### Step 3 — Define Strategic Pillars

Identify three to five strategic pillars that support the vision. Each pillar should map to a capability area. Common pillars include:

- **Developer Self-Service** — reduce dependency on centralized teams
- **Security by Default** — bake compliance and security into the platform, not bolt it on
- **Observability as a Foundation** — ensure every service is observable from day one
- **Incremental Adoption** — meet teams where they are, provide golden paths, don't mandate

For each pillar, write one sentence explaining *why* it matters for this specific organization (not generic reasons).

### Step 4 — Write OKRs

Define two to four Objectives, each with two to three Key Results. Follow these rules:

- **Objectives** are qualitative and inspiring. They describe *what* you want to achieve.
- **Key Results** are quantitative and measurable. They describe *how* you know you achieved it.
- Every Key Result must have a current baseline (or "unknown — measure first") and a target.
- OKRs must cascade from the company objectives gathered in the input.

Example structure:

> **Objective**: Reduce the friction of shipping software
>
> - KR1: Deployment lead time drops from 5 days to 1 day (p50)
> - KR2: 80% of teams use the platform's CI/CD pipelines (up from 0%)
> - KR3: Developer satisfaction score for "ease of deployment" reaches 4/5

Flag any OKR where the baseline is unknown and recommend how to measure it.

### Step 5 — Prioritize Capabilities

Using the five capability areas (Infrastructure & Resources, Integration & Delivery, Observability, Security & Compliance, Developer Experience), create a priority matrix:

- **Start here** (MVP): The one or two capabilities that address the biggest pain points.
- **Build next**: Capabilities that unlock the most value once the MVP is adopted.
- **Defer**: Capabilities that matter but can wait until the platform has traction.

Justify each placement based on the pain points and business drivers from the input.

### Step 6 — Sketch the Roadmap

Produce a Now/Next/Later roadmap outline:

- **Now** (first 1–2 months): Specific deliverables that demonstrate value quickly. These should be achievable with the current team and address the top pain point.
- **Next** (months 3–6): Expand capabilities based on adoption and feedback from Now.
- **Later** (6+ months): Strategic direction informed by what you learn.

Each item should trace back to an OKR. If an item doesn't support a Key Result, question whether it belongs.

### Step 7 — Define Roles

Based on the available team size, recommend:

- Which core roles to fill first (platform engineer, engineering manager, product-minded lead)
- Whether supporting roles (developer advocate, technical writer) are needed now or later
- Operational responsibilities: who handles on-call, support channels, incident management

Be realistic about small teams — one person often covers multiple roles. Name the roles, not the hats.

### Step 8 — Review and Refine

Present the complete charter to the user. Ask:

- Does the vision resonate? Is the framing right (developer-centric vs. business-centric)?
- Are the OKRs ambitious enough? Too ambitious?
- Does the capability prioritization match your intuition about what hurts most?
- Is the roadmap realistic given your team and constraints?

Iterate based on feedback until the user is satisfied.

## Output Format

Produce a single Markdown document named `platform-charter.md` with this structure:

```markdown
# Platform Charter

## Vision
[One to two sentence vision statement]

## Engineering Momentum Assessment
[Brief assessment of organizational inertia and its implications for adoption strategy]

## Strategic Pillars
1. **[Pillar Name]** — [Why it matters for this organization]
2. ...

## Objectives and Key Results
### O1: [Objective]
- KR1: [Key Result] (baseline → target)
- KR2: ...

### O2: [Objective]
- ...

## Capability Priorities
| Priority | Capability | Rationale |
|----------|-----------|-----------|
| Start here | ... | ... |
| Build next | ... | ... |
| Defer | ... | ... |

## Roadmap
### Now (months 1–2)
- ...

### Next (months 3–6)
- ...

### Later (6+)
- ...

## Team and Roles
[Role recommendations based on available team size]

## Assumptions and Open Questions
[Anything that was assumed or needs further investigation]
```

## Principles to Apply

- **Platform as product**: The charter should read like a product strategy document, not an infrastructure plan. The customer is the developer.
- **Explicit and implicit needs**: Balance what developers ask for (self-service, speed) with what the organization needs (security, compliance, cost control).
- **Voluntary adoption**: The roadmap must earn trust through value, not mandate usage. Start with the pain that hurts most and deliver relief quickly.
- **The easy path is the right path**: Every capability should be framed around golden paths — opinionated defaults that make the secure, scalable choice the easiest one.
- **Engineering momentum**: Respect inertia. High-momentum organizations need gentle, continuous force — not abrupt turns.

## Related Chapter(s)

This skill is grounded in **Chapter 2: Internal Developer Platform** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
