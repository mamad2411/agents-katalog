---
name: productize-managerial-finance-dcf
description: >-
  Productize Finance engine for time value of money, DCF, NPV, IRR, payback, free cash flow,
  terminal value, project valuation, mutually exclusive investments, and whether growth
  creates or destroys value.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Managerial Finance DCF

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

- **Skill**: `managerial-finance-dcf`
- **Lifecycle**: Measure
- **Category**: Finance
- **Primary artifact**: DCF investment-decision analysis with cash-flow timing, NPV, supporting metrics, decision rule, interpretation, and warnings

## Purpose

Core investment-decision skill for evaluating projects and cash-flow streams.
Use it when comparing investments, building free cash flow forecasts, calculating
NPV/IRR/payback, estimating terminal value, or judging whether growth creates value.

## Core Formulas

- `FV_t = C_0 * (1 + r)^t`
- `PV = C_t / (1 + r)^t`
- `PV stream = sum(C_t / (1 + r)^t)`
- `NPV = -I_0 + sum(C_t / (1 + r)^t)`
- `NPV with TV = -I_0 + sum(FCF_t / (1 + r)^t) + TV_N / (1 + r)^N`
- `0 = -I_0 + sum(C_t / (1 + IRR)^t)`
- `Profitability Index = PV of Future Cash Flows / Initial Investment`
- `FCF = EBIT * (1 - T_c) + Depreciation - CapEx - Delta NWC`
- `NOPAT = EBIT * (1 - T_c)`
- `TV_N = FCF_{N+1} / (r - g)` with `r > g`
- `ROIC = NOPAT / Invested Capital`
- `Reinvestment Rate = (CapEx - Depreciation + Delta NWC) / NOPAT`
- `g = ROIC * Reinvestment Rate`

## Decision Rules

- Independent projects: accept if `NPV > 0`; reject if `NPV < 0`.
- Mutually exclusive projects: choose the highest NPV.
- IRR supports the decision, but warn when cash flows change sign more than once,
  projects differ in scale or timing, or multiple/no real IRRs exist.
- Growth creates value only when `ROIC > WACC`; it destroys value when `ROIC < WACC`.

## Required Functions

Use `$finance-modeling-kernel` functions for PV/FV, streams, NPV, IRR, payback,
discounted payback, annuities, perpetuities, free cash flow, terminal value,
ROIC, reinvestment rate, and sustainable growth.

## Required Validation

- Warn if comparing undiscounted cash flows across time.
- Warn if terminal growth exceeds long-run economic growth.
- Reject `g >= r` in growing perpetuity.
- Warn if IRR conflicts with NPV.
- Warn if payback is used as the final decision rule.
- Warn if sunk costs, financing cash flows, non-incremental overhead, cannibalization,
  or opportunity cost are mishandled.

## Required Output

Return Inputs, Assumptions, Formula used, Calculation, Result, Interpretation, and
Warnings. Make NPV the primary investment decision rule.
