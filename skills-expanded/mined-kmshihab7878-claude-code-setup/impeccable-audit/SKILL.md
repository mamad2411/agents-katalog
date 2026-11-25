---
name: impeccable-audit
description: "Run technical quality checks across accessibility, performance, theming, responsive design, and anti-patterns. Generates a scored report with P0-P3 severity ratings and actionable plan. Use when the user wants an accessibility check, performance audit, or technical quality review."
user-invocable: true
argument-hint: "[area (feature, page, component...)]"
license: Apache 2.0. Based on pbakaus/impeccable audit skill.
---

## MANDATORY PREPARATION

Invoke `/impeccable-design` — it contains design principles, anti-patterns, and the Context Gathering Protocol. Follow the protocol before proceeding — if no design context exists yet, ask the user directly for target audience, use cases, and brand personality first.

---

Run systematic **technical** quality checks and generate a comprehensive report. Don't fix issues — document them for other commands to address.

This is a code-level audit, not a design critique. Check what's measurable and verifiable in the implementation.

## Diagnostic Scan

Run comprehensive checks across 5 dimensions. Score each dimension 0-4 using the criteria below.

### 1. Accessibility (A11y)

**Check for**: Contrast issues (text <4.5:1), missing ARIA labels/roles, keyboard navigation gaps, illogical tab order, semantic HTML issues, missing alt text, forms without labels.

**Score 0-4**: 0=Inaccessible (fails WCAG A), 1=Major gaps, 2=Partial (some a11y, significant gaps), 3=Good (WCAG AA mostly met), 4=Excellent (WCAG AA fully met)

### 2. Performance

**Check for**: Layout thrashing (reading/writing layout props in loops), expensive animations (animating width/height/top/left instead of transform/opacity), missing lazy loading, unnecessary imports, unoptimized re-renders.

**Score 0-4**: 0=Severe issues, 1=Major problems, 2=Partial, 3=Good (mostly optimized), 4=Excellent

### 3. Theming

**Check for**: Hard-coded colors (not using design tokens), broken dark mode, inconsistent token usage, values that don't update on theme change.

**Score 0-4**: 0=No theming, 1=Minimal tokens, 2=Partial, 3=Good (tokens used, minor hard-coded), 4=Excellent (full token system)

### 4. Responsive Design

**Check for**: Fixed widths, touch targets <44×44px, horizontal scroll, text scaling issues, missing breakpoints.

**Score 0-4**: 0=Desktop-only, 1=Major issues, 2=Partial, 3=Good (responsive, minor issues), 4=Excellent

### 5. Anti-Patterns (CRITICAL)

Check against ALL **NEVER** guidelines in impeccable-design. Look for AI slop tells: AI color palette, gradient text, glassmorphism, hero metrics, card grids, generic fonts, rounded rectangles with generic shadows, bounce easing.

**Score 0-4**: 0=AI slop gallery (5+ tells), 1=Heavy AI aesthetic (3-4 tells), 2=Some tells (1-2), 3=Mostly clean (subtle only), 4=No AI tells

## Generate Report

### Audit Health Score

| # | Dimension | Score | Key Finding |
|---|-----------|-------|-------------|
| 1 | Accessibility | ? | [most critical issue or "--"] |
| 2 | Performance | ? | |
| 3 | Responsive Design | ? | |
| 4 | Theming | ? | |
| 5 | Anti-Patterns | ? | |
| **Total** | | **??/20** | **[Rating]** |

**Rating bands**: 18-20 Excellent, 14-17 Good, 10-13 Acceptable, 6-9 Poor, 0-5 Critical

### Anti-Patterns Verdict
**Start here.** Pass/fail: Does this look AI-generated? List specific tells. Be brutally honest.

### Executive Summary
- Audit Health Score: **??/20**
- Issue count by severity: P0/P1/P2/P3
- Top 3-5 critical issues
- Recommended next steps

### Detailed Findings by Severity

Tag every issue with **P0-P3**:
- **P0 Blocking**: Prevents task completion — fix immediately
- **P1 Major**: Significant difficulty or WCAG AA violation — fix before release
- **P2 Minor**: Annoyance, workaround exists — fix in next pass
- **P3 Polish**: Nice-to-fix, no real user impact — fix if time permits

For each issue:
- **[P?] Issue name**
- **Location**: Component, file, line
- **Category**: Accessibility / Performance / Theming / Responsive / Anti-Pattern
- **Impact**: How it affects users
- **Recommendation**: How to fix it
- **Suggested command**: `/impeccable-design` or `/impeccable-polish`

### Systemic Issues
Identify recurring problems: "Hard-coded colors appear in 15+ components — should use design tokens"

### Positive Findings
Note what's working well — good practices to maintain and replicate.

## Recommended Actions

List recommended commands in priority order (P0 first):
1. **[P?] `/impeccable-polish`** — [specific context from audit findings]
2. **[P?] `/impeccable-design`** — [context]

After presenting the summary:
> You can ask me to run these one at a time, all at once, or in any order you prefer.
> Re-run `/impeccable-audit` after fixes to see your score improve.

**NEVER**: Report without impact explanation. Provide generic recommendations. Skip positive findings. Forget to prioritize.
