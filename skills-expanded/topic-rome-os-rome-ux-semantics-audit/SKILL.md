---
name: ux-semantics-audit
description: Audit an existing UI/UX design (React/JSX/TSX components, HTML, or generated app code) against a tiered ruleset of verifiable UX principles, and produce structured, evidence-cited findings that a coding agent can act on to fix the design. Use this skill whenever the user asks to review, evaluate, critique, audit, or lint a UI, screen, view, form, dialog, dashboard, or frontend codebase for UX quality, design problems, redundancy, confusing labels, missing states, or accessibility of status indicators — even if they don't say the word "audit". Also use it when a coding agent's generated UI needs a quality check before shipping, or when the user asks "is this a good design?" about code.
---

# UX Audit

Evaluate UI code against a curated set of verifiable UX rules and emit findings a coding agent can directly act on. This is a *linter for UX semantics*, not an aesthetic critique: the goal is high-precision, evidence-backed findings, not a wall of vague suggestions.

## Design philosophy (read this — it shapes every judgment call)

1. **Precision over recall.** A false positive costs more than a miss: the consuming coding agent will "fix" a non-problem and degrade the design. When in doubt, don't flag.
2. **No evidence, no finding.** Every finding must cite the exact file, line range, and quoted code snippet that demonstrates the violation. If you cannot point at the code, the finding does not exist.
3. **Exceptions are where precision lives.** Each rule in `references/rules.md` has an enumerated exceptions list. Before flagging, check the exceptions. A candidate that matches an exception is a pass, not a "borderline flag."
4. **Severity is trust calibration.** `block` findings are mechanical and near-certain — the agent should fix all of them. `warn` findings involve judgment — the agent should consider them and may reasonably decline with a reason. Never promote a judgment call to `block`.
5. **Feedback must be constructive and specific.** Every finding includes a concrete suggested fix expressed in terms of the actual code, not a restatement of the rule.

## Workflow

### Step 1 — Scope the audit

Identify the unit of analysis: the **view**. A view is a screen, page, route, dialog, drawer, or self-contained form — the thing a user perceives at one time. Enumerate the views in scope:

- If given a whole repo/directory: find view-level components (pages, routes, dialogs, modals). List them and confirm scope with the user if there are more than ~10.
- If given a single component/file: that component and its rendered children are the view.
- If given a screenshot or design description alongside code, the code is the source of truth for findings; the image is context.

Composition matters: a rule like one-primary-action applies to the *rendered view*, not each source file. Trace child components far enough to know what actually renders together.

### Step 2 — Load the ruleset

Read `references/rules.md` in full. It contains every rule's definition, detection procedure, enumerated exceptions, severity, and a violation/pass example pair. Do not audit from memory of the rule names.

### Step 3 — Build a per-view inventory

For each view, before checking any rule, build a short inventory. This forces the semantic resolution the rules depend on and prevents lazy pattern-matching:

- **Data slots**: each distinct datum displayed, where, and at what hierarchy level (e.g., `order.total → header badge; also → summary table row`).
- **Actions**: every button/link/menu item, its label, visual variant (primary/secondary/ghost/destructive), and its outcome (what actually happens on activation — trace the handler).
- **Async states**: for each async data source, which of {loading, empty, error} branches exist in the code.
- **Status indicators**: anything conveying state (badges, dots, colored text) and the channels used (color / icon / text).

### Step 4 — Run Tier 1 (mechanical) checks

Check each Tier 1 rule against the inventory: single-source-of-truth, one-primary-action, state-completeness, color-not-sole-channel, focus-initial-attention, emphasis-budget. These are decidable from code structure. Severity: `block` (except where rules.md says otherwise).

### Step 5 — Run Tier 2/3 (semantic and judged) checks

Check consistent-terminology and consequence-proximity (Tier 2, cross-view where relevant), then the judged rules: label-outcome-clarity, destructive-action-safety, error-recovery-path, progressive-disclosure, and the experimental rules if enabled. Severity: `warn` unless rules.md specifies otherwise. For these, re-read the rule's exceptions and examples before each flag — they are the rubric.

### Step 6 — Self-review pass (false-positive sweep)

Before emitting the report, re-examine every finding and drop any that:
- matches an enumerated exception,
- lacks a concrete code citation,
- depends on an assumption about code you did not read (e.g., "the child component probably also shows this"),
- would require the fix to violate another rule.

If a finding survives but you have genuine uncertainty, keep it at `warn` and say what would confirm it.

### Step 7 — Emit the report

Use exactly this structure:

```markdown
# UX Audit: <scope>

## Summary
<2-4 sentences: overall assessment, count of block/warn findings, the single highest-leverage fix.>

## Findings

### [BLOCK|WARN] <rule-id>: <one-line title>
- **View**: <view/component name>
- **Evidence**: `<file>:<lines>`
  ```<lang>
  <minimal quoted snippet>
  ```
- **Why it matters**: <1-2 sentences tied to this specific UI, not a generic rule recital>
- **Suggested fix**: <concrete change in terms of this code; include a code sketch when it fits in a few lines>
- **Confidence**: high | medium (warn-tier only; include what would confirm a medium)

## Passes worth keeping
<Bulleted list of 2-5 things the design does right that a refactor should preserve. This prevents the coding agent from regressing good decisions while fixing findings.>

## Not flagged (borderline)
<Candidates you examined and declined to flag, each with the exception or reason. Include only genuinely borderline cases. This section teaches the consuming agent the boundaries and builds trust in the flags that remain.>
```

Order findings: all `block` first, then `warn`, each group ordered by leverage (user impact × fix cheapness). If there are zero findings, say so plainly and fill in "Passes worth keeping" — a clean audit is a valid result, not a failure to try hard enough.

### Step 8 — Build the shareable report (Rome surfaces)

When the audit covers a Rome surface and the user wants something to look at, share, or triage — rather than findings in chat — build it with the report app in **`report/`**, beside this file. Do not hand-author an HTML page: the chrome, filtering, triage and prompt export already exist and are the same every time.

The whole job is two files:

1. **`findings.tsx`** — rewrite it against the `AuditReport` type in `types.ts`. Prose fields take Markdown inline syntax (`` `code` ``, `**bold**`), because the same strings render on the page *and* serialize into the hand-off prompt.
2. **`repros.tsx`** — one component per finding, built from real `@rome-os/ui` primitives.

Then `node .claude/skills/ux-semantics-audit/report/build.mjs` emits a single self-contained `dist-report/index.html`.

Read **`references/report-app.md`** before writing either file — it carries the authoring contract and the rules that keep reproductions honest.

## Interaction with the consuming coding agent

The report is designed to be handed to a coding agent as-is. Findings are independent work items: each contains everything needed to fix it (location, evidence, fix). Do not bundle multiple rule violations into one finding. If two findings share a root cause (e.g., a missing design-token discipline causes both an emphasis-budget and a color-not-sole-channel violation), note the shared root cause in the Summary rather than merging the findings.

## What this skill does NOT do

- Aesthetic judgments (spacing taste, color palette beauty, typography pairing) — out of scope.
- Full WCAG conformance — only color-not-sole-channel (1.4.1) is in the ruleset; recommend axe-core for the rest.
- Information architecture / navigation-model critique — the rules operate at view level, not sitemap level.
- Rewriting the UI itself — emit findings; the consuming agent makes the changes.
