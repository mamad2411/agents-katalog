---
name: tokens
description: "Design system governance - versioning, documentation, tokens"
---

# Nathan Curtis - Design System Governance

Design systems die without governance. Documentation, versioning, and maintenance keep systems alive.

## Core Philosophy

### The System is a Product
A design system is not a side project. It needs:
- Dedicated owners
- Release schedule
- User feedback loops
- Deprecation paths

### Documentation is Interface
If it's not documented, it doesn't exist. Docs are how users interact with your system.

### Tokens are Contracts
Design tokens are the API of your visual language. Changes break consumers.

## Design Tokens

### Token Hierarchy

```
Global → Semantic → Component

/* Global: raw values */
--color-blue-500: #3b82f6;
--space-4: 16px;
--font-size-base: 16px;

/* Semantic: purpose-driven aliases */
--color-primary: var(--color-blue-500);
--space-component: var(--space-4);
--font-size-body: var(--font-size-base);

/* Component: specific usage */
--button-padding: var(--space-component);
--button-color: var(--color-primary);
--button-font-size: var(--font-size-body);
```

### Token Categories

```css
/* Color tokens */
--color-gray-{50-900}    /* Neutral scale */
--color-primary          /* Brand action */
--color-success          /* Positive feedback */
--color-warning          /* Caution */
--color-error            /* Negative feedback */

/* Spacing tokens */
--space-{1-12}           /* 4px base: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96 */

/* Typography tokens */
--font-family-{sans,mono}
--font-size-{xs,sm,base,lg,xl,2xl,3xl,4xl}
--font-weight-{normal,medium,semibold,bold}
--line-height-{tight,normal,relaxed}

/* Border tokens */
--radius-{sm,md,lg,xl,full}
--border-width-{1,2}

/* Shadow tokens */
--shadow-{sm,md,lg,xl}

/* Motion tokens */
--duration-{instant,fast,normal,slow}
--ease-{in,out,in-out}
```

### Token File Format

```json
// tokens.json (source of truth)
{
  "color": {
    "primary": {
      "value": "#3b82f6",
      "description": "Primary brand color for actions",
      "type": "color"
    }
  },
  "space": {
    "4": {
      "value": "16px",
      "description": "Standard component spacing",
      "type": "dimension"
    }
  }
}
```

## Documentation Structure

### Component Documentation

Every component needs:

```markdown
# Button

Primary action element.

## Usage

Use buttons to trigger actions. One primary button per view.

## Variants

| Variant | Use Case |
|---------|----------|
| Primary | Main action |
| Secondary | Alternate action |
| Ghost | Subtle action |
| Destructive | Delete/remove |

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| label | string | required | Button text |
| variant | enum | primary | Visual style |
| disabled | boolean | false | Disables interaction |

## States

- Default
- Hover
- Active
- Focus
- Disabled
- Loading

## Accessibility

- Requires visible focus state
- Use `aria-disabled` over `disabled` attribute
- Loading state needs `aria-busy="true"`

## Examples

[Live examples with code]

## Changelog

- 2.1.0: Added loading state
- 2.0.0: Breaking - removed `size` prop (use CSS)
- 1.0.0: Initial release
```

### System Documentation

```
docs/
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── migration.md
├── foundations/
│   ├── color.md
│   ├── typography.md
│   ├── spacing.md
│   └── motion.md
├── components/
│   ├── atoms/
│   ├── molecules/
│   └── organisms/
├── patterns/
│   ├── forms.md
│   ├── navigation.md
│   └── data-display.md
└── contributing/
    ├── proposing-changes.md
    ├── component-checklist.md
    └── release-process.md
```

## Versioning

### Semantic Versioning

```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1  PATCH: Bug fix, no API change
1.0.0 → 1.1.0  MINOR: New feature, backward compatible
1.0.0 → 2.0.0  MAJOR: Breaking change
```

### Breaking Changes

**Breaking:**
- Removing a component
- Removing a prop
- Changing prop type
- Renaming a token
- Changing token value significantly

**Not Breaking:**
- Adding a component
- Adding a prop with default
- Bug fixes
- Adding a token

### Deprecation Path

```html
<!-- Phase 1: Warn -->
<Button size="large">  <!-- Console warning: size prop deprecated, use CSS -->

<!-- Phase 2: Document alternative -->
Before: <Button size="large">
After:  <Button className="btn-lg">

<!-- Phase 3: Remove in next major -->
v2.0.0: size prop removed
```

## Release Process

### Checklist

```markdown
## Release Checklist

### Pre-release
- [ ] All changes documented
- [ ] Breaking changes identified
- [ ] Migration guide written (if major)
- [ ] Visual regression tests pass
- [ ] Accessibility audit complete
- [ ] Token changes reviewed

### Release
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Package published
- [ ] Documentation updated
- [ ] Announcement sent

### Post-release
- [ ] Monitor for issues
- [ ] Respond to feedback
- [ ] Track adoption metrics
```

## Contribution Process

### Proposing Changes

```markdown
## Component Proposal

### Problem
[What problem does this solve?]

### Solution
[Proposed component/change]

### Scope
- [ ] New component
- [ ] Component modification
- [ ] Token change
- [ ] Documentation only

### Impact
- Teams affected:
- Breaking changes: Yes/No
- Migration required: Yes/No

### Alternatives Considered
[Other approaches and why rejected]
```

### Review Criteria

```markdown
## Component Review Checklist

### Design
- [ ] Follows design system patterns
- [ ] Uses existing tokens
- [ ] Has documented variants and states
- [ ] Responsive behavior defined

### Development
- [ ] Accessible (WCAG 2.1 AA)
- [ ] Tested in target browsers
- [ ] No external dependencies
- [ ] Follows naming conventions

### Documentation
- [ ] Usage guidelines
- [ ] Props documented
- [ ] Examples provided
- [ ] Changelog entry
```

## Metrics

Track system health:

| Metric | Target | Why |
|--------|--------|-----|
| Adoption | >80% of projects | System is useful |
| Token coverage | 100% | No magic numbers |
| Doc completeness | 100% | Usable without asking |
| Issue response time | <48hrs | Responsive to users |
| Breaking changes/year | <2 | Stability |

## Anti-Patterns

| Bad | Why | Fix |
|-----|-----|-----|
| No versioning | Can't track changes | Semantic versioning |
| Undocumented changes | Surprise breaks | Changelog required |
| One-off exceptions | System erosion | Add to system or reject |
| No deprecation period | Sudden breaks | Major version + migration |
| No ownership | System rots | Dedicated maintainer |

## Curtis Score

| Score | Meaning |
|-------|---------|
| 10 | Full governance, documented, versioned |
| 7-9 | Good documentation, some process gaps |
| 4-6 | Components exist but no process |
| 0-3 | No documentation, no versioning |

## Integration

Combine with:
- `/components` - Component structure this governs
- `/handoff` - Handoff process this documents
- All other UI skills - This governs their output
