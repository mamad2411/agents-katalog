---
name: prioritising-accessibility-fixes
description: Use this skill to prioritise a set of accessibility issues for remediation based on severity, user impact, and effort. Triggers when triaging an accessibility backlog, deciding what to fix first after an audit, planning an accessibility sprint, or asking which accessibility issues matter most.
compatibility: Works best when issues already have effort estimates (from estimating-accessibility-effort) but can assess effort independently.
---

# Prioritising Accessibility Fixes

Given a set of accessibility issues, produce a prioritised remediation order based on severity, user impact, and effort. The output is a ranked list that helps decide what to fix first, what to batch together, and what can wait.

This skill works on a set of known issues. It does not find new issues (use `reviewing-accessibility` for that), estimate effort from scratch (use `estimating-accessibility-effort` for that, or provide estimates as input), or implement fixes (use `fixing-accessibility-issues` for that). If issues arrive without effort estimates, assess effort by reading the affected code before prioritising.

## Inputs

A set of accessibility issues, ideally with:

- Description of the problem
- WCAG success criterion
- Severity (Blocker / Critical / Serious / Moderate / Minor)
- Affected pages or components
- Effort estimate (XS / S / M / L / XL)
- Reach (Systemic / Multi-page / Single page) — optional, most useful for projects with shared components

If effort estimates are missing, read the affected code and estimate before prioritising. Do not prioritise without understanding effort — a "Critical" issue that takes 5 minutes should be fixed immediately, while a "Critical" issue requiring an architectural redesign needs different planning.

### Effort sizes

If the project defines its own effort estimation convention (e.g. story points, T-shirt sizes with different definitions, time-based estimates), use that convention for display and map it to the Low / Medium / High effort scoring bands in the scoring model. For example, if the project uses story points, treat 1–2 points as Low effort (score 3), 3–5 as Medium (score 2), and 8+ as High (score 1) — adjusting the boundaries to match the project's scale definitions.

If issues arrive without effort estimates and `estimating-accessibility-effort` is not available, use this fallback scale:

| Size | Typical scope |
|------|--------------|
| **XS** | Single attribute or property change, one file |
| **S** | Localised change within one component, a few attributes |
| **M** | Changes to one component plus its consumers, or 2-5 files |
| **L** | Structural changes affecting multiple components or a shared layout |
| **XL** | Architectural changes affecting routing, state management, or component library |

## Pre-scoring overrides

Before scoring, run each issue through these filters in order. If a filter matches, assign the tier directly — do not score the issue.

- [ ] **Complete AT blocker on a critical path?** Assistive technology users cannot complete a core user flow (navigation, authentication, checkout, primary actions). → **Tier 1**.
- [ ] **Legal or regulatory mandate?** The issue is covered by an active legal obligation, settlement, regulatory deadline, or formal complaint applicable to this project. → **Tier 1**.
- [ ] **User-reported barrier?** A real user has reported this specific barrier. Real-world evidence of harm outranks theoretical audit findings at the same severity level. → **Tier 1**, or promote by one tier if the report describes inconvenience rather than a blocker.
- [ ] **Regression?** A feature that was previously accessible and has regressed. Regressions indicate a process gap that will recur. → Promote by one tier from wherever scoring would place it, minimum **Tier 2**.
- [ ] **Dependency blocker?** The issue blocks remediation of two or more other issues (e.g. "build focus-management utility" is a prerequisite for five focus fixes). → Promote by one tier.

Issues that do not match any filter proceed to scoring.

## Scoring model

Each issue is scored on three dimensions. The priority score determines the remediation order.

### Severity (functional impact)

Severity measures how badly the user's experience is degraded. It is defined by functional impact, not WCAG conformance level — though the two often correlate.

| Rating | Definition | Score |
|--------|-----------|-------|
| Blocker | Assistive technology users cannot access or operate the feature at all. Typically a WCAG Level A failure. | 5 |
| Critical | The feature is technically operable but so degraded that most AT users will abandon the task. | 4 |
| Serious | Significant friction or confusion. Users can complete the task but with considerable difficulty. Often a WCAG Level AA failure. | 3 |
| Moderate | Noticeable inconvenience but the task is completable without major difficulty. | 2 |
| Minor | Best practice or AAA improvement. Marginal polish rather than a barrier. | 1 |

### User impact

User impact measures how many people are affected and how severely their experience is degraded. This is distinct from WCAG severity — a Serious (AA) issue that affects every keyboard user on every page has higher user impact than a Critical (A) issue on a rarely visited admin screen.

| Rating | Definition | Score |
|--------|-----------|-------|
| Pervasive | Affects a core user flow AND appears across many pages/views. Multiple disability groups impacted. | 5 |
| High | Affects a core user flow on specific pages, or a secondary flow across many pages. Multiple groups or a large single group impacted. | 4 |
| Medium | Affects a secondary flow or a specific page. One disability group primarily impacted. | 3 |
| Low | Affects a rarely used feature or a non-critical edge case. | 2 |
| Minimal | Cosmetic or very minor inconvenience. Almost no users will notice. | 1 |

### Effort (used as divisor — lower effort increases priority)

Lower effort means faster delivery of accessibility improvement. All else being equal, fix the easy things first.

| Rating | Effort sizes | Score |
|--------|-------------|-------|
| Low effort | XS, S | 3 |
| Medium effort | M | 2 |
| High effort | L, XL | 1 |

### Reach modifier (optional)

For projects with shared components, templates, or design-system tokens that propagate across multiple pages, apply a reach modifier to the final score. Skip this modifier for small sites or single-page applications where reach differentiation adds no value.

| Reach | Definition | Modifier |
|-------|-----------|----------|
| Systemic | Shared component / template / design token reused across many pages or in a design system | × 1.5 |
| Multi-page | Appears on several distinct pages or views | × 1.25 |
| Single page | Isolated to one page or view | × 1.0 (no change) |

If reach is not assessed, use the base priority score as the final score.

### Priority score

Severity and user impact are weighted and summed, then divided by effort to ensure difficult fixes cannot outrank critical barriers.

```
Priority = (Severity × 2 + User Impact × 1.5) / Effort
```

Where Effort uses the existing inverse scale (Low effort = 3, Medium = 2, High = 1) but now acts as a **divisor**, not an addend. Higher scores = higher priority. Effort makes easy fixes rise but can never push a low-severity issue above a high-severity one.

If using the reach modifier: `Final Priority = Priority × Reach Modifier`

Round to one decimal place for display. Issues with the same rounded score are ordered by severity first, then user impact, then effort.

## Priority tiers

Group scored issues into tiers for practical planning:

### Tier 1 — Fix immediately (score 6.0+)

High severity and impact issues, especially those that are quick to fix. These deliver the most accessibility improvement per unit of effort. Fix these first. Also includes all issues routed here by pre-scoring overrides.

### Tier 2 — Plan for next cycle (score 3.0–5.9)

Significant issues that need more effort or planning. These should be scheduled, not deferred indefinitely. Typical examples: implementing keyboard navigation for a custom widget, adding focus management to modal flows, building an error handling pattern for forms.

### Tier 3 — Schedule when capacity allows (score below 3.0)

Low-impact or high-effort issues. Still worth fixing, but other work delivers more accessibility value per effort. Examples: AAA contrast improvements, optimising for edge-case assistive technology combinations, progressive enhancement of already-functional features.

If the formula weights are adjusted, recalibrate these thresholds by scoring a few representative issues at each tier and checking that the boundaries still produce sensible groupings.

## Batch related fixes

After scoring, identify issues that should be fixed together because:

- **Same component** — three accessibility issues in the same dialog are one task, not three.
- **Same pattern** — adding `aria-describedby` to 12 form fields is one effort with the pattern established on the first.
- **Dependency** — the focus management utility must exist before individual focus fixes can use it.

Present batches as grouped items with a combined effort estimate and a note on why they belong together.

## Validate before reporting

After scoring all issues and assigning tiers, run a quick validation pass:

- [ ] Does any Tier 3 issue match a pre-scoring override that was missed? If so, re-run the overrides for that issue.
- [ ] Is every critical-path AT blocker in Tier 1? If not, something is wrong — review the pre-scoring overrides.
- [ ] If structural (L/XL) issues exist, is at least one scheduled in Tier 2? If all large items landed in Tier 3, promote the highest-impact one.
- [ ] Do any batched items span multiple tiers? If so, assign the batch to the highest tier of its members.

## Report format

```markdown
## Accessibility Prioritisation - [scope]

### Tier 1 — Fix Immediately

| # | Issue | WCAG | Severity | Impact | Effort | Reach | Score |
|---|-------|------|----------|--------|--------|-------|-------|
| 1 | ... | ... | ... | ... | ... | ... | ... |

### Tier 2 — Plan for Next Cycle

| # | Issue | WCAG | Severity | Impact | Effort | Reach | Score |
|---|-------|------|----------|--------|--------|-------|-------|
| 1 | ... | ... | ... | ... | ... | ... | ... |

### Tier 3 — Schedule When Capacity Allows

| # | Issue | WCAG | Severity | Impact | Effort | Reach | Score |
|---|-------|------|----------|--------|--------|-------|-------|
| 1 | ... | ... | ... | ... | ... | ... | ... |

### Batches

- **[batch name]**: [issue A], [issue B], [issue C] - [combined effort] - [why batched]

### Recommended Order

[Numbered list of the specific order to tackle fixes, accounting for dependencies, batches, and tier placement. This is the actionable output — a developer should be able to start at #1 and work down.]

### Summary

- Tier 1: [n] issues ([n] quick wins, [n] via pre-scoring overrides)
- Tier 2: [n] issues
- Tier 3: [n] issues
- Total: [n] issues
- Systemic reach: [n] issues | Multi-page: [n] | Single page: [n]
```

Omit empty tiers. Omit the Reach column and the reach summary line if reach was not assessed.

If the project defines its own priority labels (e.g. P0–P3, Critical/High/Medium/Low), add a brief mapping note at the top of the report — for example: "This project uses P0–P3. Tier 1 corresponds roughly to P0/P1, Tier 2 to P2, Tier 3 to P3." Do not replace the tier structure with the project's scale; the tiers reflect accessibility-specific scoring that a general priority scale does not capture. The mapping note bridges the two systems so the team can see where accessibility priorities sit within their existing workflow.

## Gotchas

- **Severity alone is not priority.** A Blocker issue requiring an XL architectural redesign will still score high because effort is a divisor, not an equal weight — but an easy Serious fix will often deliver more value in the short term and should be tackled first within the same tier. The scoring model exists to prevent severity-only triage, which leads to large Critical items blocking all other progress.
- **User impact requires judgment, not just WCAG mapping.** Two issues can both violate 2.1.1 (Keyboard) — one on the main navigation (High impact, every user on every page) and one on a settings toggle (Low impact, rare interaction). Same criterion, very different priority.
- **Quick wins are disproportionately valuable.** A batch of 10 XS/S fixes might take less time than one L fix but improve accessibility across more pages and for more users. Always surface quick wins prominently.
- **Do not defer all large items.** If the scoring model puts all L/XL items in Tier 3, the project will never fix structural accessibility problems. Ensure at least one L or XL item is scheduled in Tier 2 per planning cycle if structural issues exist.
- **Priorities change.** A Tier 3 issue becomes Tier 1 when a user reports it, when a legal requirement emerges, or when a dependent fix promotes it. Revisit prioritisation periodically rather than treating it as a one-time exercise.
- **Do not invent impact assessments.** If the project has analytics, use them — a page with 10,000 daily visits has higher impact than one with 10. If there are no analytics, assess based on the feature's centrality to the product's purpose, not assumptions about traffic.
- **Accessibility debt compounds.** Five Moderate issues in the same component often indicate a pattern problem. Consider whether fixing the pattern (one M/L task) is more effective than five individual fixes.
- **Scores are a decision aid, not a decision.** The model produces a number but cannot account for context it was not given — internal politics, upcoming redesigns, capacity constraints, or user research findings. Treat tier placement as a strong default that can be overridden with a stated reason.
