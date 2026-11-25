---
name: productize-accessibility-review
description: >-
  Run a WCAG 2.1 AA accessibility audit on a design or page. Use when asked to audit
  accessibility, check a11y, determine whether something is accessible, or review color
  contrast, keyboard navigation, touch target size, or screen reader behavior before handoff.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Accessibility Review

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

- **Skill**: `accessibility-review`
- **Lifecycle**: Design
- **Category**: Design
- **Primary artifact**: Accessibility Review UX/design review with findings, constraints, fixes, and acceptance checks

Audit a design or page for WCAG 2.1 AA accessibility compliance.

## Argument Hint

`<Figma URL, URL, or description>`

## Usage

```text
/accessibility-review $ARGUMENTS
```

## Inputs

Accept:
- Figma design URL.
- Live or local page URL.
- Screenshot.
- Written design description.
- HTML/CSS/component code.

If the input is not inspectable, ask for the minimum missing artifact needed to assess contrast, keyboard behavior, touch targets, or screen reader behavior.

## WCAG 2.1 AA Quick Reference

### Perceivable

- **1.1.1 Non-text Content**: meaningful images and icons need text alternatives.
- **1.3.1 Info and Relationships**: structure must be conveyed semantically, not only visually.
- **1.4.3 Contrast (Minimum)**: normal text at least 4.5:1; large text at least 3:1.
- **1.4.11 Non-text Contrast**: UI components and graphics at least 3:1.

### Operable

- **2.1.1 Keyboard**: all functionality available via keyboard.
- **2.4.3 Focus Order**: focus order is logical.
- **2.4.7 Focus Visible**: keyboard focus indicator is visible.
- **2.5.5 Target Size**: touch targets at least 44x44 CSS pixels where applicable.

### Understandable

- **3.2.1 On Focus**: focus does not trigger unexpected context changes.
- **3.3.1 Error Identification**: errors are clearly identified.
- **3.3.2 Labels or Instructions**: inputs have labels or instructions.

### Robust

- **4.1.2 Name, Role, Value**: UI components expose accessible names, roles, states, and values.

## Testing Approach

Use the strongest available method for the artifact:

1. Automated scan when browser/page tooling is available. Treat this as partial coverage only.
2. Keyboard-only navigation: tab order, Enter/Space behavior, Escape behavior, arrow-key behavior where expected.
3. Screen reader review: accessible names, roles, landmarks, form labels, live regions, and reading order.
4. Color contrast verification for text and non-text UI.
5. Zoom/reflow check at 200 percent.
6. Touch target sizing for mobile or touch-first UI.

If a design tool is connected, inspect color values, typography, spacing, and component dimensions directly. If a browser tool is connected, open the page and verify interactive behavior directly.

If a project tracker is connected, offer to turn findings into tickets with severity, WCAG criterion, repro steps, and recommended fix.

## Common Issues

- Insufficient text or UI contrast.
- Missing form labels.
- Interactive elements unreachable by keyboard.
- Missing alt text for meaningful images.
- Focus traps in modals.
- Missing landmarks or heading structure.
- Auto-playing media without controls.
- Time limits without extension.
- Small or crowded touch targets.
- Icon-only controls without accessible names.

## Severity

- **Critical**: blocks task completion for users with disabilities or violates a core accessibility requirement.
- **Major**: creates significant friction or likely failure for a common assistive technology path.
- **Minor**: improvement needed, but workaround likely exists.

## Output Format

```markdown
## Accessibility Audit: [Design/Page Name]

**Standard:** WCAG 2.1 AA
**Date:** [Date]

### Summary

**Issues found:** [X]
**Critical:** [X]
**Major:** [X]
**Minor:** [X]

### Findings

#### Perceivable

| # | Issue | WCAG Criterion | Severity | Recommendation |
|---|---|---|---|---|
| 1 | [Issue] | [1.4.3 Contrast] | Critical | [Fix] |

#### Operable

| # | Issue | WCAG Criterion | Severity | Recommendation |
|---|---|---|---|---|
| 1 | [Issue] | [2.1.1 Keyboard] | Major | [Fix] |

#### Understandable

| # | Issue | WCAG Criterion | Severity | Recommendation |
|---|---|---|---|---|
| 1 | [Issue] | [3.3.2 Labels] | Minor | [Fix] |

#### Robust

| # | Issue | WCAG Criterion | Severity | Recommendation |
|---|---|---|---|---|
| 1 | [Issue] | [4.1.2 Name, Role, Value] | Major | [Fix] |

### Color Contrast Check

| Element | Foreground | Background | Ratio | Required | Result |
|---|---|---|---|---|---|
| [Body text] | [color] | [color] | [X]:1 | 4.5:1 | Pass/Fail |

### Keyboard Navigation

| Element | Tab Order | Enter/Space | Escape | Arrow Keys |
|---|---|---|---|---|
| [Element] | [Order] | [Behavior] | [Behavior] | [Behavior] |

### Screen Reader

| Element | Announced As | Issue |
|---|---|---|
| [Element] | [What screen reader should announce] | [Problem if any] |

### Priority Fixes

1. **[Critical fix]** - Affects [who] and blocks [what].
2. **[Major fix]** - Improves [what] for [who].
3. **[Minor fix]** - Nice to have.
```

## Rules

- Start with contrast and keyboard access; these catch many high-impact issues.
- Be specific: cite the WCAG criterion, affected element, user impact, and fix.
- Do not claim full compliance from automated checks alone.
- When evidence is limited, say what could and could not be verified.
- Prioritize issues by user impact before cosmetic polish.
