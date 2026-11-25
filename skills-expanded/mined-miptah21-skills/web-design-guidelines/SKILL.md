---
name: web-design-guidelines
description: Fetch and apply modern web interface design guidelines to review UI code. Use when building or reviewing frontend components, layouts, or user-facing pages.
---

# Web Design Guidelines

## When to Invoke

- Building new UI components or pages
- Reviewing frontend code for quality
- User asks for "better design" or "modern UI"
- Before shipping user-facing features

## Process

### Step 1: Read Guidelines

Read the vendored guidelines file:

```
view_file: .agent/skills/web-design-guidelines/guidelines.md
```

> **Note:** Guidelines vendored from [vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines). Last updated: 2026-04-11.
> To update, re-fetch from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`.

If the file is missing, use the embedded principles below as fallback.

### Step 2: Review Code Against Principles

Scan the target files using `grep_search` and `view_file`, checking for violations of:

1. **Responsiveness** — Does it work across viewport sizes?
2. **Accessibility** — Are semantic elements, ARIA labels, keyboard navigation present?
3. **Performance** — Are images optimized? Lazy loading? Avoiding layout shifts?
4. **Progressive Enhancement** — Does it work without JS where possible?
5. **Motion** — Are animations purposeful? Respect `prefers-reduced-motion`?
6. **Typography** — Proper hierarchy? Readable line lengths? System font stack or loaded fonts?
7. **Color** — Sufficient contrast? Dark mode support? Consistent palette?
8. **Spacing** — Consistent spacing scale? No magic numbers?
9. **Interactivity** — Hover/focus/active states? Touch targets ≥ 44px?
10. **Error States** — Are empty states, loading states, and error states handled?

### Step 3: Output Findings

```markdown
## Web Design Review: [Component/Page Name]

### ✅ Good
- [What's done well]

### ⚠️ Issues
| # | Category | Issue | File:Line | Severity |
|---|----------|-------|-----------|----------|
| 1 | [category] | [description] | [location] | 🔴/🟡/🟢 |

### 🛠️ Recommendations
1. [Actionable fix with code example]
```

## Fallback Principles (if URL unavailable)

Core web interface guidelines:

1. **Every interaction should feel instant** — use optimistic UI, skeleton loading
2. **Respect the platform** — native scrolling, system fonts, platform conventions
3. **Design for the keyboard** — all interactive elements must be keyboard-accessible
4. **Reduce motion for those who prefer it** — `@media (prefers-reduced-motion: reduce)`
5. **Use semantic HTML** — `<button>` not `<div onclick>`, `<nav>` not `<div class="nav">`
6. **Design for failure** — empty states, error boundaries, offline handling
7. **Color is not the only indicator** — use icons, text, patterns alongside color
8. **Touch targets ≥ 44×44px** — fingers are imprecise
9. **Content should be scannable** — clear hierarchy, whitespace, visual grouping
10. **Test with real content** — not "Lorem ipsum", use realistic data lengths
