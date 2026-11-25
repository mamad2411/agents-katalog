---
name: "a11y-audit"
description: "Accessibility audit skill for scanning, fixing, and verifying WCAG 2.2 Level A and AA compliance across React, Next.js, Vue, Angular, Svelte, and plain HTML codebases. Use when auditing accessibility, fixing a11y violations, checking color contrast, generating compliance reports, or integrating accessibility checks into CI/CD pipelines."
---

> **Note:** This project uses **cmux** (native macOS CLI with built-in WebKit browser) instead of Playwright/Puppeteer. For browser interaction commands, see `../../references/cmux-browser.md` in the skill library root. Replace any Playwright/Puppeteer commands with cmux equivalents.

# Accessibility Audit

WCAG 2.2 Accessibility Audit and Remediation Skill

## Description

The a11y-audit skill provides a complete accessibility audit pipeline for modern web applications. It implements a three-phase workflow -- Scan, Fix, Verify -- that identifies WCAG 2.2 Level A and AA violations, generates exact fix code per framework, and produces stakeholder-ready compliance reports.

For every violation it finds, it provides the precise before/after code fix tailored to your framework (React, Next.js, Vue, Angular, Svelte, or plain HTML).

**What this skill does:**

1. **Scans** your codebase for every WCAG 2.2 Level A and AA violation, categorized by severity (Critical, Major, Minor)
2. **Fixes** each violation with framework-specific before/after code patterns
3. **Verifies** that fixes resolve the original violations and introduces no regressions
4. **Reports** findings in a structured format suitable for developers, PMs, and compliance stakeholders
5. **Integrates** into CI/CD pipelines to prevent accessibility regressions

## Features

| Feature | Description |
|---------|-------------|
| **Full WCAG 2.2 Scan** | Checks all Level A and AA success criteria across your codebase |
| **Framework Detection** | Auto-detects React, Next.js, Vue, Angular, Svelte, or plain HTML |
| **Severity Classification** | Categorizes each violation as Critical, Major, or Minor |
| **Fix Code Generation** | Produces before/after code diffs for every issue |
| **Color Contrast Checker** | Validates foreground/background pairs against AA and AAA ratios |
| **Compliance Reporting** | Generates stakeholder reports with pass/fail summaries |
| **CI/CD Integration** | GitHub Actions, GitLab CI, Azure DevOps pipeline configs |
| **Keyboard Navigation Audit** | Detects missing focus management and tab order issues |
| **ARIA Validation** | Checks for incorrect, redundant, or missing ARIA attributes |

### Severity Definitions

| Severity | Definition | Example | SLA |
|----------|-----------|---------|-----|
| **Critical** | Blocks access for entire user groups | Missing alt text, no keyboard access to navigation | Fix before release |
| **Major** | Significant barrier that degrades experience | Insufficient color contrast, missing form labels | Fix within current sprint |
| **Minor** | Usability issue that causes friction | Redundant ARIA roles, suboptimal heading hierarchy | Fix within next 2 sprints |

## Usage

### Quick Start

This public skill does not bundle scanner scripts. Run the repository's configured accessibility tools if present, then complete the manual WCAG 2.2 audit with the checklists and reference docs in `references/`.

Common project-local tools:

```bash
npx eslint . --ext .js,.jsx,.ts,.tsx
npx axe http://localhost:3000
npx lighthouse http://localhost:3000 --only-categories=accessibility
```

If those tools are not configured, inspect components manually for semantic HTML, labels, focus order, keyboard operation, ARIA correctness, motion preferences, and color contrast.

### Slash Command

```
/a11y-audit                    # Audit current project
/a11y-audit --scope src/       # Audit specific directory
/a11y-audit --fix              # Audit and auto-apply fixes
/a11y-audit --report           # Generate stakeholder report
/a11y-audit --ci               # Output CI-compatible results
```

### Three-Phase Workflow

**Phase 1: Scan** -- Walk the source tree, detect framework, run configured a11y tooling if available, and apply the manual rule set in `references/testing-checklist.md`.

**Phase 2: Fix** -- Apply framework-specific fixes for each violation.

> See [references/framework-a11y-patterns.md](references/framework-a11y-patterns.md) for the complete fix patterns catalog.

**Phase 3: Verify** -- Re-run the same project-local checks and repeat keyboard, screen reader, and contrast verification to confirm fixes and check for regressions.

## Example: React Component Audit

```tsx
// BEFORE: src/components/ProductCard.tsx
function ProductCard({ product }) {
  return (
    <div onClick={() => navigate(`/product/${product.id}`)}>
      <img src={product.image} />
      <div style={{ color: '#aaa', fontSize: '12px' }}>{product.name}</div>
      <span style={{ color: '#999' }}>${product.price}</span>
    </div>
  );
}
```

| # | WCAG | Severity | Issue |
|---|------|----------|-------|
| 1 | 1.1.1 | Critical | `<img>` missing `alt` attribute |
| 2 | 2.1.1 | Critical | `<div onClick>` not keyboard accessible |
| 3 | 1.4.3 | Major | Color `#aaa` on white fails contrast (2.32:1, needs 4.5:1) |
| 4 | 1.4.3 | Major | Color `#999` on white fails contrast (2.85:1, needs 4.5:1) |
| 5 | 4.1.2 | Major | Interactive element missing role and accessible name |

```tsx
// AFTER: src/components/ProductCard.tsx
function ProductCard({ product }) {
  return (
    <a href={`/product/${product.id}`} className="product-card"
       aria-label={`View ${product.name} - $${product.price}`}>
      <img src={product.image} alt={product.imageAlt || product.name} />
      <div style={{ color: '#595959', fontSize: '12px' }}>{product.name}</div>
      <span style={{ color: '#767676' }}>${product.price}</span>
    </a>
  );
}
```

> See [references/examples-by-framework.md](references/examples-by-framework.md) for Vue, Angular, Next.js, and Svelte examples.

## Tooling Checklist

Use tools already present in the target repository where possible:

| Tool type | Examples | Use |
|-----------|----------|-----|
| Static lint | eslint-plugin-jsx-a11y, template linters | Missing labels, invalid ARIA, interactive anti-patterns |
| Browser audit | axe DevTools, axe CLI, Lighthouse | Runtime WCAG checks and page-level report |
| Keyboard smoke | Browser or cmux interaction | Focus order, skip links, modal traps, menu operation |
| Screen reader smoke | VoiceOver, NVDA, JAWS | Names, roles, announcements, landmarks |
| Contrast check | WebAIM calculator, browser DevTools, design tokens | Foreground/background ratios for normal and large text |

Record tool versions, page/component scope, findings, fixes, and verification evidence in the report template.

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|------------------|
| `role="button"` on a `<div>` | Use native `<button>` -- includes keyboard handling for free |
| `tabindex="0"` on everything | Only interactive elements need focus; use native elements |
| `aria-label` on non-interactive elements | Use `aria-labelledby` pointing to visible text |
| `display: none` for screen reader hiding | Use `.sr-only` class instead |
| Color alone to convey meaning | Add icons, text labels, or patterns alongside color |
| Placeholder as only label | Always provide a visible `<label>` |
| `outline: none` without replacement | Always provide a visible focus indicator via `focus-visible` |
| Empty `alt=""` on informational images | Informational images need descriptive alt text |
| Skipping heading levels (h1 -> h3) | Heading levels must be sequential |
| `onClick` without `onKeyDown` | Add keyboard support or prefer native elements |
| Ignoring `prefers-reduced-motion` | Wrap animations in `@media (prefers-reduced-motion: no-preference)` |

## Related Skills

| Skill | Relationship |
|-------|-------------|
| **senior-frontend** | Frontend patterns used in a11y fixes |
| **code-reviewer** | Include a11y checks in code review workflows |
| **senior-qa** | Integration of a11y testing into QA processes |
| **playwright-pro** | Automated browser testing with accessibility assertions |
| **epic-design** | WCAG 2.1 AA compliant animations and scroll storytelling |
| **tdd-guide** | Test-driven development patterns for a11y test cases |

## Reference Documentation

| Reference | Description |
|-----------|-------------|
| [wcag-quick-ref.md](references/wcag-quick-ref.md) | WCAG 2.2 Level A & AA criteria quick reference |
| [wcag-22-new-criteria.md](references/wcag-22-new-criteria.md) | New WCAG 2.2 success criteria (Focus Appearance, Target Size, etc.) |
| [aria-patterns.md](references/aria-patterns.md) | ARIA patterns, keyboard interaction, and live regions |
| [framework-a11y-patterns.md](references/framework-a11y-patterns.md) | Framework-specific fix patterns (React, Vue, Angular, Svelte, HTML) |
| [color-contrast-guide.md](references/color-contrast-guide.md) | Color contrast checker details, Tailwind palette mapping, sr-only class |
| [ci-cd-integration.md](references/ci-cd-integration.md) | GitHub Actions, GitLab CI, Azure DevOps, pre-commit hook configs |
| [audit-report-template.md](references/audit-report-template.md) | Stakeholder-ready audit report template |
| [testing-checklist.md](references/testing-checklist.md) | Manual testing checklist (keyboard, screen reader, visual, forms) |
| [examples-by-framework.md](references/examples-by-framework.md) | Full audit examples for Vue, Angular, Next.js, and Svelte |

## Resources

- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA Authoring Practices 1.2](https://www.w3.org/WAI/ARIA/apg/)
- [Deque axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)
