---
name: productize-financial-markets-context
description: >-
  Productize Finance context skill for market capitalization, market weights, index
  concentration, listed-firm trends, public-company comparables, sector shifts, and CAPM
  market-portfolio assumptions.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Financial Markets Context

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `financial-markets-context`
- **Lifecycle**: Measure
- **Category**: Finance
- **Primary artifact**: Financial Markets Context calculation memo with formulas, assumptions, result, interpretation, and warnings

## Purpose

Market context skill. Use it to interpret public-market facts, index concentration,
listed-firm trends, market capitalization, comparable-company assumptions, sector
shifts, and market portfolio assumptions in CAPM.

## Core Formulas

- `Market Cap_i = Share Price_i * Shares Outstanding_i`
- `Weight_i = Market Cap_i / Total Market Cap`
- `Index Weight_i = Market Cap_i / sum(Market Cap of All Index Constituents)`
- `Global Weight_i = index weight * index share of country market * country share of world market`
- `Change in Listings = Listings_End - Listings_Start`
- `% Change = (End / Start - 1) * 100`
- `CAGR = (Ending Value / Beginning Value)^(1 / Years) - 1`

## Interpretation Rules

- Fewer listed firms does not necessarily mean a smaller equity market.
- Market capitalization can rise even if listings fall.
- This can happen because public firms become larger, smaller firms delist, and mergers concentrate value.
- Index concentration matters because the CAPM market portfolio is value-weighted.
- Public comparables may be biased if the target is much smaller, less mature, less profitable, or in a different sector.
- Sector composition changes over time, so historical index returns may reflect sector shifts, not only broad economic growth.

## Required Validation

- Warn if equal weighting is confused with value weighting.
- Warn if index concentration is ignored.
- Warn if public comparables are used for a startup without maturity adjustments.
- Warn if global market assumptions use only one domestic index.
- Warn if stale market weights are used.

## Required Output

Return Inputs, Assumptions, Formula used, Calculation, Result, Interpretation, and
Warnings. Separate market fact, valuation implication, and comparability risk.
