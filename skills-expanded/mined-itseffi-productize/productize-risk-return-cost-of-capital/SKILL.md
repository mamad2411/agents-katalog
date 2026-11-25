---
name: productize-risk-return-cost-of-capital
description: >-
  Productize Finance engine for expected return, volatility, diversification, beta, CAPM,
  excess-return regression, unlevering/relevering beta, WACC inputs, and project-specific cost
  of capital.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Risk Return Cost Of Capital

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

- **Skill**: `risk-return-cost-of-capital`
- **Lifecycle**: Measure
- **Category**: Finance
- **Primary artifact**: Cost-of-capital analysis with risk basis, beta/CAPM/WACC inputs, calculation, interpretation, and warnings

## Purpose

Discount-rate and risk skill. Use it for cost of equity, beta, WACC inputs, expected
returns, volatility, diversification, and selecting a project-specific discount rate.

## Core Formulas

- `r_{t+1} = (P_{t+1} - P_t + Div_{t+1}) / P_t`
- `E[R] = sum(p_i * R_i)`
- `Var(R) = sum(p_i * (R_i - E[R])^2)`
- `SD(R) = sqrt(Var(R))`
- `E[R_p] = sum(x_i * E[R_i])`
- `Var(R_p) = sum_i sum_j x_i * x_j * Cov(R_i, R_j)`
- `rho_ij = Cov(R_i, R_j) / (sigma_i * sigma_j)`
- `beta_i = Cov(R_i, R_M) / Var(R_M)`
- `r_i = r_f + beta_i * (E[R_M] - r_f)`
- `WACC = E/(D+E) * r_E + D/(D+E) * (1 - T_c) * r_D`

## Required Functions

Use `$finance-modeling-kernel` for realized return, expected return, variance,
standard deviation, historical average return, portfolio expected return, portfolio
variance, covariance, correlation, beta, CAPM cost of equity, regression beta,
unlevered beta, relevered beta, and WACC.

## Required Validation

- Use long-term government bond rates for valuation risk-free rates.
- Use short-term risk-free rates for short-term performance measurement.
- Use excess returns when estimating beta by regression.
- Use market values for debt and equity in WACC.
- Warn if book-value weights are used.
- Warn if beta is estimated from too little data.
- Warn if a company beta is used for a different-risk project.
- Warn if total volatility is treated as priced risk for a diversified investor.
- Warn if the market risk premium and risk-free rate come from inconsistent markets.

## Required Output

Return Inputs, Assumptions, Formula used, Calculation, Result, Interpretation, and
Warnings. State the risk basis and why the discount rate matches the cash flows.
