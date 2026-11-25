# Skill: rialto-visual-diff-review

When a visual regression spec fails, triage and resolve.

## Problem Patterns

1. Visual diff shows intentional design change (new component, updated styling)
2. Visual diff shows regression (broken layout, missing element)
3. Screenshot stale (component changed but screenshot not updated)

## Triage Workflow

### Step 1: Review the Diff

```bash
# Open the failing spec
pnpm test:visual

# Review diff PNGs in apps/rialto-web/e2e/screenshots/
# Compare light-*.png vs light-*-diff.png
```

### Step 2: Classify the Change

| Pattern                    | Action                                   |
| -------------------------- | ---------------------------------------- |
| Intentional design change  | Update screenshot, update spec if needed |
| Regression (broken layout) | File issue or fix immediately            |
| Stale screenshot           | Update screenshot                        |

### Step 3: Update Screenshots (if intentional)

```bash
# Update specific screenshot
npx playwright test apps/rialto-web/e2e/visual.spec.ts --update-snapshots

# Verify the updated screenshot looks correct
open apps/rialto-web/e2e/screenshots/<updated>.png
```

### Step 4: File Issue (if regression)

```bash
# Create issue with screenshot attached
gh issue create --repo mattbutlerengineering/mattbutlerengineering \
  --title "Visual regression: <component> <description>" \
  --label "bug,acmm-rialto-web" \
  --body "Visual diff shows <description>. Screenshot attached." \
  --attach apps/rialto-web/e2e/screenshots/<file>-diff.png
```

## Prevention

- Run `pnpm test:visual` before claiming UI work is complete
- New components require a visual spec in `e2e/visual.spec.ts`
- Always review diff PNGs, not just pass/fail status
