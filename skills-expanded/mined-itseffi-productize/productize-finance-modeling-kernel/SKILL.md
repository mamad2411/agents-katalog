---
name: productize-finance-modeling-kernel
description: >-
  Shared Productize Finance calculation and validation kernel for exact formulas, input
  normalization, assumption checks, units, warnings, and acceptance-tested finance math used
  by valuation, DCF, cost-of-capital, capital-structure, VC deal, and market-context skills.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Finance Modeling Kernel

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

- **Skill**: `finance-modeling-kernel`
- **Lifecycle**: Measure
- **Category**: Finance
- **Primary artifact**: Validated finance calculation with inputs, assumptions, formula, calculation, result, interpretation, and warnings

## Purpose

Shared calculation and validation library used by all Productize Finance skills.
Use this skill when a finance workflow needs exact formulas, normalized inputs,
assumption checks, error handling, units, or validation before making a recommendation.

## Kernel Modules

- `finance-modeling-kernel/time_value.py`: PV, FV, annuities, perpetuities, spot-rate streams.
- `finance-modeling-kernel/dcf.py`: NPV, IRR, payback, free cash flow, terminal value, ROIC, growth.
- `finance-modeling-kernel/returns.py`: realized returns, expected return, variance, volatility, covariance, correlation.
- `finance-modeling-kernel/risk.py`: portfolio variance, covariance, correlation, beta, regression beta.
- `finance-modeling-kernel/capm.py`: CAPM, unlevered beta, relevered beta.
- `finance-modeling-kernel/wacc.py`: WACC with market-value weights.
- `finance-modeling-kernel/apv.py`: tax shields and APV.
- `finance-modeling-kernel/valuation.py`: DCF valuation, terminal value, EV-to-equity bridge, multiples, sensitivities.
- `finance-modeling-kernel/capital_structure.py`: EV, equity value, leverage, MM, tax shields, APV.
- `finance-modeling-kernel/bond_math.py`: bond price, yield to maturity, current yield, credit spread.
- `finance-modeling-kernel/vc_method.py`: burn, runway, VC target multiple, pre/post-money, shares.
- `finance-modeling-kernel/cap_table.py`: fully diluted shares, ownership, dilution, cap table sum checks.
- `finance-modeling-kernel/convertible_notes.py`: note conversion amount, discount price, cap price, shares.
- `finance-modeling-kernel/safes.py`: SAFE conversion price, SAFE shares, post-money SAFE ownership.
- `finance-modeling-kernel/preferred_stock.py`: liquidation preference and preferred payoff waterfalls.
- `finance-modeling-kernel/option_pools.py`: investor-friendly and founder-friendly option pool math.
- `finance-modeling-kernel/market_context.py`: market cap, weights, listing changes, CAGR.
- `finance-modeling-kernel/validation.py`: shared validation errors and warning helpers.
- `finance-modeling-kernel/tests/`: acceptance tests for the minimum formula examples.

## Finance Output Format

All Productize Finance agents must return:

1. **Inputs**
2. **Assumptions**
3. **Formula used**
4. **Calculation**
5. **Result**
6. **Interpretation**
7. **Warnings**

## Global Guardrails

1. Never compare cash flows at different dates without compounding or discounting.
2. Use market values, not book values, for valuation and WACC weights whenever possible.
3. Match discount rates to cash-flow risk.
4. Do not use a company WACC for a project with materially different risk.
5. Do not mix financing cash flows into operating free cash flow.
6. Use NPV as the primary investment decision rule.
7. Treat IRR, payback, and multiples as supporting tools, not final truth.
8. For VC deals, always state whether share counts are basic or fully diluted.
9. For option pools, always state whether the pool is investor-friendly or founder-friendly.
10. For convertible notes and SAFEs, always read the conversion definition before calculating.
11. For preferred stock, model the payoff waterfall, not only the ownership percentage.

## Workflow

1. Identify the finance problem and the cash-flow timing, units, currency, and risk basis.
2. Choose the exact module and function; do not invent ad hoc formulas when a kernel function exists.
3. Validate formula preconditions, especially `r > g`, positive denominators, share-count basis, and market-value weights.
4. Calculate transparently enough that the user can audit the math.
5. Return the standard Finance output format and warnings.

## Acceptance Tests

Run:

```sh
python3 skills/finance-modeling-kernel/finance-modeling-kernel/tests/test_acceptance.py
```

The test suite covers DCF NPV, growing perpetuity, CAPM, WACC, VC target multiple,
post-money/pre-money, convertible note discount conversion, investor-friendly option
pool, and non-participating preferred payoff.
