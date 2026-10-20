---
name: dev-visual-verdict
description: Visual regression testing — capture before/after screenshots of UI changes and compare. Use when a UI change might have unintended visual impact across components.
---

# Dev Visual Verdict

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Visual regression testing. Capture before/after screenshots of UI components, compare them, and flag unintended visual impact.

## Use When
- CSS / styling change that might cascade to other components
- Component refactor where the visual output should remain identical
- Theme change that needs to be verified across the app

## Do Not Use When
- Backend-only changes
- Intentional redesigns (use `@canvas-designer` instead)
- Single-component changes with obvious visual outcome

## Workflow

1. **Identify scope** — which components could be affected
2. **Capture baseline** — screenshot current state of each affected component
3. **Apply change** — let `@bolt-executor` make the modification
4. **Capture after** — screenshot post-change state
5. **Compare** — flag any visual differences (pixel-level or layout-level)
6. **Verdict** — IDENTICAL / EXPECTED CHANGES / UNEXPECTED REGRESSION

## Output
Saved to `workspace/development/verifications/[C]visual-{component}-{date}.md`:

```markdown
## Visual Verdict — {component}

### Scope
- Components checked: [list]

### Comparison
| Component | Before | After | Diff | Verdict |
|---|---|---|---|---|
| Header | ![](before-1.png) | ![](after-1.png) | 0% | IDENTICAL |
| Footer | ![](before-2.png) | ![](after-2.png) | 12% | UNEXPECTED |

### Verdict
{IDENTICAL | EXPECTED CHANGES | UNEXPECTED REGRESSION}

### Unexpected Regressions
- Footer color shifted from #1A1A1A to #2A2A2A — investigate cascade
```

## Pairs With
- `@canvas-designer` (when regression is intentional)
- `@hawk-debugger` (when regression is unintended)
- `@oath-verifier` (final visual verification)
