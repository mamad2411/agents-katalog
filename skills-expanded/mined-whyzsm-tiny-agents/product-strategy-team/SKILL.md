---
name: product-strategy-team
description: "Product strategy expert-team router for product management work: PRD and feature specs, requirement analysis, user research synthesis, competitive analysis, product metrics review, roadmap planning, sprint planning, stakeholder updates, and end-to-end product strategy delivery. Coordinates requirement analysis, user research, competitive intelligence, product data analysis, and roadmap planning."
metadata:
  short-description: Product strategy expert team router
---

# Product Strategy Team

Use this skill as the expert-team entry point for product strategy and product management tasks. It converts the imported product-strategy expert package into the same lightweight router shape as `harmony-expert-team`: coordinate capability paths in this bundle instead of requiring the original plugin runtime, avatars, or member Markdown files.

Team mode: `internal-router-labels`. The role names below are internal capability labels handled inside `$product-strategy-team`; they are not standalone `$requirement-analyst`, `$user-researcher`, `$competitive-analyst`, `$data-analyst`, or `$roadmap-planner` skills unless separate top-level packages are created later.

## Expert Roles

- `requirement-analyst`: PRD writing, feature specs, requirement breakdown, acceptance criteria, scope control, goals, non-goals, milestones, and open questions.
- `user-researcher`: interview, survey, usability, NPS, support ticket, review, and behavior data synthesis; theme coding, insight extraction, user segments, and evidence tables.
- `competitive-analyst`: competitor research, feature comparison, positioning analysis, pricing and packaging review, market landscape, SWOT, battle cards, and strategic recommendations.
- `data-analyst`: product KPI review, AARRR metrics, North Star metrics, funnels, cohorts, retention, anomaly diagnosis, and data-driven product recommendations.
- `roadmap-planner`: roadmap management, RICE or weighted prioritization, Now/Next/Later planning, sprint planning, dependency and risk analysis, and stakeholder communications.

## Routing

Classify the task before acting. Use these labels as internal routing paths within `$product-strategy-team`, not as separate top-level skill invocations:

1. Use `requirement-analyst` when the user asks for a PRD, feature spec, requirement document, user stories, acceptance criteria, MVP scope, or scope management.
2. Use `user-researcher` when the task includes user interviews, surveys, usability tests, NPS/CSAT, support tickets, app reviews, behavior data, or feedback synthesis.
3. Use `competitive-analyst` when the user asks for competitive analysis, competitor comparison, positioning, pricing or packaging review, market landscape, or battle cards.
4. Use `data-analyst` when the task asks about metrics, KPI dashboards, metric drops, product health, funnels, retention, activation, revenue, or data-backed product decisions.
5. Use `roadmap-planner` when the user asks for roadmap planning, prioritization, sprint planning, quarterly planning, stakeholder updates, or cross-functional communication.
6. For mixed tasks, run the flow in phases. Example: `user-researcher` and `competitive-analyst` gather evidence, `data-analyst` reviews metrics, `requirement-analyst` writes the PRD, then `roadmap-planner` builds the roadmap and communication plan.

## Product-First Workflow

When a task depends on a product idea, product area, or product document:

1. Inspect the available product context before producing artifacts: target users, problem statement, business goal, product stage, constraints, timeline, existing metrics, competitor list, and intended audience.
2. Separate confirmed facts from assumptions. Ask only for missing context that blocks the next useful deliverable.
3. Choose the smallest useful role set. Do not generate a full product strategy package when the user only needs one artifact.
4. Use evidence labels for research, competitor, and metric claims. Mark inferred or unverified conclusions clearly.
5. Keep the output decision-ready: measurable goals, explicit non-goals, prioritization logic, risks, dependencies, and next actions.
6. If the user asks for a saved full report, write it under `deliverables/product-strategy/` in the current workspace and report the saved relative path.

## Product Delivery Checklist

For product strategy tasks, make sure the final work accounts for:

- Problem statement, target users, goals, non-goals, and success metrics.
- User evidence, competitor evidence, metric evidence, confidence level, and known gaps.
- PRD or feature spec sections, including user stories, requirements, acceptance criteria, technical and design considerations, milestones, and open questions.
- Prioritization method such as RICE, MoSCoW, ICE, or value/effort scoring, with visible tradeoffs.
- Roadmap, sprint plan, dependencies, risks, owners, and stakeholder-specific communication when relevant.
- Final TL;DR, core decision, action list, assumptions, risks, and next steps.

## Output Style

- Be explicit about which product expert path you selected and why.
- Separate confirmed product facts from assumptions and recommendations.
- When creating files, summarize changed or generated files, validation commands, and remaining risks.
- When answering without files, keep the response concrete, concise, and product-specific; use tables only when they make decisions easier to compare.
