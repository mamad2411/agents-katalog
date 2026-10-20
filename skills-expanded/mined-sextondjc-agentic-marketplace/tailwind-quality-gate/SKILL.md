---
name: tailwind-quality-gate
description: Use when a TailwindCSS implementation needs an expert, evidence-first quality decision covering bundle size, accessibility, design token conformance, and Core Web Vitals before merge or promotion.
---

# TailwindCSS Quality Gate

## Specialization

Produce one deterministic, evidence-first go or no-go decision for a TailwindCSS implementation — covering CSS bundle health, design token conformance, accessibility compliance, Core Web Vitals impact, and build-pipeline correctness.

This skill reviews completed implementations. It does not implement or fix components; it produces findings and a signed disposition. Remediation is owned by the implementing team.

## Trigger Conditions

- A TailwindCSS implementation is ready for merge or promotion to staging or production.
- A component library update introduces new utilities, tokens, or Headless UI patterns.
- A v3 → v4 migration is complete and needs a gate check before deployment.
- A performance regression is suspected from a CSS delivery change.
- A design system audit requires Tailwind token conformance verification.

## When Not to Use

- Initial project setup or build-pipeline configuration (use `tailwind-setup`).
- Component design pattern work (use `tailwind-component-design`).
- Source freshness verification before starting work (use `tailwind-source-curation`).

## Inputs

- Implementation scope: component files, CSS entry, config file, and build output.
- Target environment and deployment context (CDN delivery, SSR, static export).
- Accessibility requirement level (default: WCAG 2.2 AA).
- Performance budget: CSS bundle target, Core Web Vitals thresholds.
- Framework and TailwindCSS version in use.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Bundle health verdict | CSS output size, purge effectiveness, and content-scan completeness assessed |
| Token conformance verdict | All color, spacing, and font utilities traced to `@theme` tokens; no raw arbitrary values without justification |
| Accessibility verdict | Contrast, focus-visible, reduced-motion, and touch-target checks with zero unresolved critical findings |
| Core Web Vitals verdict | CLS, LCP, and INP impact from CSS delivery assessed; regressions flagged |
| Build-pipeline verdict | Content scanning correct; no unused classes retained; CSP alignment confirmed |
| Findings table | All findings severity-tagged; owner assigned per finding |
| Gate recommendation | `GO`, `GO-WITH-CONDITIONS`, or `NO-GO` with explicit reason and evidence reference |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Spot Check | Fast bundle and config sanity check | Bundle size and content-scan correctness confirmed |
| L2 Release Gate | Full pre-merge or pre-promotion review | All five verdict dimensions complete; gate recommendation issued |
| L3 Design System Audit | Token conformance and visual consistency across a component library | All tokens traced; no drift between design spec and implementation |
| L4 Governance Baseline | Establishes recurring quality policy for a project or team | Repeatable checklist and threshold policy documented for CI integration |

## Gate Dimensions and Checks

### 1. Bundle Health

| Check | Pass Criterion | Failure Risk |
|---|---|---|
| CSS output size | ≤ 50 KB (gzip) for a typical app; justified exception if larger | CLS, render-blocking, LCP regression |
| Content-scan completeness | All template file extensions and paths are in Tailwind config or auto-detected by v4 | Unused class leakage or under-purging |
| No development-only classes in production build | Build output does not include dev utilities (`debug-screens`, etc.) | Bundle bloat |
| Dynamic class construction | No string-concatenated class names; full class names only or safeList entry justified | Classes purged in production |

### 2. Design Token Conformance

| Check | Pass Criterion | Failure Risk |
|---|---|---|
| No raw hex/RGB values in utilities | `text-[#3b82f6]` pattern absent; token used instead | Dark mode breakage, design drift |
| Semantic token naming | `color-brand-*`, `color-surface-*`, `color-text-*` used; raw palette names (`blue-500`) only in token definitions | Maintenance debt |
| `@theme` completeness | All custom colors, fonts, and spacing in `@theme` block; no JS config remnants (v4) | Config model inconsistency |
| Token coverage for dark mode | Every light token has a dark-mode counterpart in `@media (prefers-color-scheme: dark)` or `.dark {}` | Broken dark mode |

### 3. Accessibility

| Check | Pass Criterion | Source |
|---|---|---|
| Text contrast (normal) | ≥ 4.5:1 against background | WCAG 2.2 SC 1.4.3 |
| Text contrast (large / bold ≥ 18.66px) | ≥ 3:1 against background | WCAG 2.2 SC 1.4.3 |
| Focus ring visible | `focus-visible:ring-*` present on all interactive elements; not suppressed with `outline-none` without replacement | WCAG 2.2 SC 2.4.11 |
| Touch target size | Interactive targets ≥ `h-11 w-11` (44×44 CSS px) on mobile | WCAG 2.2 SC 2.5.8 |
| Reduced motion | Animations wrapped in `motion-safe:` or `motion-reduce:`; no forced animation on `prefers-reduced-motion: reduce` | WCAG 2.2 SC 2.3.3 |
| Headless UI usage | All interactive ARIA components (dialog, menu, combobox) use Headless UI; no custom ARIA re-implementation | WAI-ARIA APG |

### 4. Core Web Vitals

| Check | Pass Criterion |
|---|---|
| CLS | No layout shift caused by CSS loading or font loading; Tailwind font utilities paired with `font-display: swap` |
| LCP | CSS delivery does not block LCP resource; critical CSS inlined or preloaded where required |
| INP | No Tailwind-driven animation or transition blocking interaction; `will-change` used conservatively |

### 5. Build Pipeline

| Check | Pass Criterion |
|---|---|
| Tailwind CDN absent from production | No `cdn.tailwindcss.com` script tag in production HTML |
| PostCSS / Vite plugin correctly registered | Build output confirms Tailwind processing ran |
| Prettier plugin active | CI formatter check passes; no unordered class sequences committed |
| CSP compatible | No `unsafe-inline` required solely for Tailwind styles |

## Findings Severity Taxonomy

| Severity | Definition | Gate Impact |
|---|---|---|
| Critical | WCAG AA violation, production CDN usage, or broken purge config | Blocks GO recommendation |
| High | Token conformance failure, CLS regression, or focus ring absent | Blocks GO unless exception approved |
| Medium | Suboptimal but non-blocking: bundle slightly over target, minor drift | GO-WITH-CONDITIONS allowed |
| Low | Style-only or advisory: ordering inconsistency, redundant utility | Logged; does not block gate |

## Gate Recommendation Rules

- `GO`: all Critical and High checks pass; no unresolved findings above Medium.
- `GO-WITH-CONDITIONS`: one or more Medium findings remain; conditions and owners explicitly named.
- `NO-GO`: one or more Critical or High findings are unresolved; re-review required after remediation.

## Findings Table Template

| ID | Dimension | Severity | Check | Finding | Owner | Status |
|---|---|---|---|---|---|---|
| TWQ-001 | Accessibility | Critical | Focus ring | `<Button>` uses `outline-none` with no replacement focus ring | Frontend lead | Open |
| TWQ-002 | Bundle Health | Medium | CSS output size | Gzip output 72 KB; exceeds 50 KB target | Frontend lead | Open |

## Done Criteria

- [ ] All five gate dimensions evaluated with explicit verdicts.
- [ ] Findings table complete; all findings severity-tagged and owner-assigned.
- [ ] Gate recommendation (`GO`, `GO-WITH-CONDITIONS`, or `NO-GO`) issued with evidence reference.
- [ ] No Critical or High findings left unresolved for a `GO` recommendation.
- [ ] Any exceptions are documented with approver and rationale.

## References

- [Source Catalog](./references/source-catalog.md)
