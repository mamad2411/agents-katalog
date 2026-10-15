---
name: byte-start
description: Start a Your ByteDance / Byte OS project from a rough idea. Use when creating a product from zero, initializing `.byte-os/`, combining discovery and research into the first foundation step, or restarting early-stage product discovery with a ByteDance-inspired project team.
---

# Byte Start

Start creates the Your ByteDance project foundation. It combines project initialization, discovery, market research, competitor research, early user assumptions, and transparent OKRs into one user-visible step.

## Inputs

Use the user's product idea. If the idea is missing, ask one concise question for it. Otherwise make reasonable assumptions and label them.

Useful optional details:

- Target user
- Delivery format, such as web app, mobile app, API, plugin, CLI, SaaS, or internal tool
- Business goal
- Known competitors
- Constraints, stack, budget, deadline

## Workflow

1. Create `.byte-os/` if missing:

```text
.byte-os/
  plans/
  reviews/
  iterations/
  users/
```

2. Discover the product:

- Clarify the problem.
- Identify target users.
- Identify the current substitute behavior.
- Define the first valuable outcome.
- Record assumptions and unknowns.
- Draft an Objective and 3-5 measurable Key Results.

3. Research the market:

- Use current web search for competitor, pricing, trend, and market claims.
- Prefer official websites, docs, changelogs, pricing pages, app stores, review sites, and credible articles.
- Cite links in the research files.
- Do not claim "latest" or current facts without checking current sources.

4. Run the project-group foundation pass:

- Product Manager: problem, users, MVP hypothesis.
- Market Researcher: competitors and alternatives.
- UX Researcher: likely user journey and friction.
- Tech Lead: feasibility and obvious risks.
- Growth Analyst: adoption, retention, monetization signals.
- Product Director: final foundation summary.

Use the Your ByteDance style: keep the foundation direct, evidence-led, and Day 1 simple. Label facts, assumptions, and open questions separately.

Use actual subagents only when explicitly authorized by the user or auto workflow. Otherwise run these roles inline.

## Artifacts

Write or update:

```text
.byte-os/BYTE.md
.byte-os/STATUS.md
.byte-os/OKRS.md
.byte-os/DECISIONS.md
.byte-os/RESEARCH.md
.byte-os/COMPETITORS.md
.byte-os/USER_ASSUMPTIONS.md
```

`BYTE.md` must include:

- Product name or working title
- One-sentence product concept
- Target users
- Core problem
- Delivery format
- Current stage
- Success criteria

`OKRS.md` must include:

- One ambitious but concrete Objective
- 3-5 measurable Key Results
- Current baseline if known
- Evidence needed to validate progress

`STATUS.md` must include:

- Mode: step or auto
- Stage: started
- Current command: byte-start
- Next recommended command: byte-shape
- Open blockers
- Last updated date

`DECISIONS.md` must start a decision log with timestamped decisions and assumptions.

## Completion Criteria

The step is complete when Byte OS has enough foundation context to shape the product without asking the user to repeat the same idea again.

End with the next command:

```text
byte-shape
```
