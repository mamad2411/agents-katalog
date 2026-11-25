---
name: productize-valuation-and-deal-pricing
description: >-
  Main Productize Finance orchestrator for company valuation, project valuation, enterprise
  value, equity value, price per share, VC ownership, dilution, deal pricing, comparable
  multiples, precedent transactions, sensitivity tables, and investment attractiveness
  decisions.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Valuation And Deal Pricing

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

- **Skill**: `valuation-and-deal-pricing`
- **Lifecycle**: Strategize
- **Category**: Finance
- **Primary artifact**: Valuation and deal-pricing memo with method, assumptions, EV, equity value, price per share, sensitivities, recommendation, and warnings

## Purpose

Main valuation skill. Use it to answer:

- What is this company worth?
- What is this project worth?
- What should we pay?
- What ownership should we receive?
- Is this investment attractive?
- What is the enterprise value, equity value, or price per share?

## Depends On

- `$finance-modeling-kernel` for formulas, validation, and acceptance-tested calculations.
- `$managerial-finance-dcf` for project DCF, FCF, NPV, IRR, payback, terminal value, and growth value creation.
- `$risk-return-cost-of-capital` for beta, CAPM, WACC, and project-specific discount rates.
- `$capital-structure-financing` for EV-to-equity bridges, leverage, APV, tax shields, debt, preferred, and warrants.
- `$venture-capital-deal-modeling` for VC method, cap tables, dilution, notes, SAFEs, option pools, and preferred stock.
- `$financial-markets-context` for public-market context, comparables, index weights, and market-cap assumptions.

## Scope

1. Intrinsic valuation.
2. Relative valuation.
3. Project valuation.
4. Company valuation.
5. VC and startup valuation.
6. Deal pricing.
7. Enterprise value to equity value bridge.
8. Share price and dilution analysis.

## Core Formulas

- `PV = C_t / (1 + r)^t`
- `FV_t = C_0 * (1 + r)^t`
- `PV stream = sum(C_t / (1 + r)^t)`
- `NPV = -I_0 + sum(FCF_t / (1 + r)^t)`
- `EV = sum(FCF_t / (1 + WACC)^t) + TV_N / (1 + WACC)^N`
- `Equity Value = Enterprise Value - Debt - Preferred Stock - Noncontrolling Interest + Cash + Nonoperating Assets`
- `Price per Share = Equity Value / Diluted Shares Outstanding`
- `TV_N = FCF_{N+1} / (WACC - g)` with `WACC > g`
- `TV_N = Exit Multiple * Metric_N`
- `Implied Value = Comparable Multiple * Company Metric`

## Required Functions

Use kernel functions for:

- `value_project_dcf`
- `value_company_dcf`
- `calculate_terminal_value_gordon`
- `calculate_terminal_value_exit_multiple`
- `bridge_enterprise_to_equity_value`
- `calculate_price_per_share`
- `run_comparable_company_valuation`
- `run_precedent_transaction_valuation`
- `calculate_implied_multiple`
- `calculate_implied_value`
- `run_sensitivity_table`
- `run_scenario_analysis`

## Required Validation

- Reject Gordon growth if `g >= WACC`.
- Warn if terminal value is more than 70 percent of enterprise value.
- Warn if WACC is used for a project with different risk from the company.
- Warn if book values are used instead of market values.
- Warn if equity value is negative.
- Warn if using EBITDA multiples for companies with very different capex intensity.
- Warn if using revenue multiples without checking gross margin and growth.

## Required Output

1. Valuation method used.
2. Key assumptions.
3. Enterprise value.
4. Equity value.
5. Price per share.
6. Sensitivity to WACC and growth.
7. Sensitivity to exit multiple.
8. Decision or recommendation.
9. Warnings.

Always include the Finance output format: Inputs, Assumptions, Formula used,
Calculation, Result, Interpretation, Warnings.
