---
name: aria-validation
description: Validate WAI-ARIA usage so assistive tech announces the right role, name, state, and relationships. Use when reviewing custom widgets, dynamic UI, or fixing screen-reader bugs against WCAG 2.2 AA / EN 301 549.
source: self
date_added: 2026-05-01
---

# ARIA Validation

Most accessibility regressions come from misusing ARIA — not from missing it. This skill enforces the ARIA Authoring Practices (APG 1.3, 2025) and WAI-ARIA 1.3 spec so each interactive element exposes a correct **role + accessible name + state**, with valid relationships and no role/native-semantics conflicts.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Spec | WAI-ARIA 1.3, ARIA in HTML, APG 1.3 patterns |
| Static lint | eslint-plugin-jsx-a11y, axe-linter (VS Code), Biome a11y rules |
| Runtime audit | axe-core 4.10, Lighthouse 12, Pa11y 8, Accessibility Insights for Web |
| Tree inspection | Chrome DevTools Accessibility pane, Firefox Accessibility Inspector |
| Screen readers | NVDA 2025.x + Firefox/Chrome, JAWS 2025 + Chrome, VoiceOver (macOS 15 / iOS 18), TalkBack (Android 15) |
| Test harness | Playwright + @axe-core/playwright, Cypress-axe, Vitest + jsdom + jest-axe |

## When to Use

- Building or reviewing a custom widget (combobox, tabs, dialog, tree, grid).
- Adding `role`, `aria-*`, or `tabindex` to existing markup.
- Diagnosing a screen-reader bug ("nothing announced", "wrong state", "reads twice").
- PR gate for design-system components.

## First Principles (the only ARIA rules that matter)

1. **No ARIA is better than bad ARIA.** Prefer native HTML (`<button>`, `<dialog>`, `<details>`, `<input type="checkbox">`).
2. **Every interactive element needs role + name + state.** If any of the three is missing or wrong, AT users are blocked.
3. **Don't change native semantics.** `<h1 role="button">` and `<a role="heading">` are bugs.
4. **All ARIA relationships use IDREFs that exist** (`aria-labelledby`, `aria-controls`, `aria-describedby`, `aria-owns`).
5. **Required owned/parent roles must be present.** `role="tab"` requires a `role="tablist"` parent; `role="option"` requires `role="listbox"`.

## Validation Workflow

1. **Static lint** — run `eslint-plugin-jsx-a11y` (`recommended` + `strict`) and Biome `a11y/*`. Catches invalid roles, abstract roles, missing `alt`, missing `htmlFor`, redundant roles.
2. **Run axe** in component tests and on every page in E2E. Treat `serious` and `critical` as blockers.
3. **Inspect the accessibility tree** in DevTools — confirm role, name, description, value, states for each interactive node.
4. **Walk the APG pattern** for the widget you built (combobox, dialog, menu, tree, etc.) and tick each required key, role, and ARIA attribute.
5. **Smoke test with one screen reader per platform** (NVDA + VoiceOver minimum) — focus, activate, change state; confirm announcement matches intent.

## Code Examples

### Component test with jest-axe + Testing Library

```ts
// Dialog.test.tsx
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import userEvent from '@testing-library/user-event';
import { Dialog } from './Dialog';

expect.extend(toHaveNoViolations);

test('dialog exposes role, accessible name, and modal state', async () => {
  const { container } = render(
    <Dialog open titleId="dlg-title" onClose={() => {}}>
      <h2 id="dlg-title">Delete project?</h2>
      <p>This cannot be undone.</p>
      <button>Cancel</button>
      <button>Delete</button>
    </Dialog>,
  );

  const dlg = screen.getByRole('dialog', { name: 'Delete project?' });
  expect(dlg).toHaveAttribute('aria-modal', 'true');
  expect(await axe(container)).toHaveNoViolations();

  // Focus trap and Escape
  await userEvent.tab();
  expect(screen.getByRole('button', { name: 'Cancel' })).toHaveFocus();
});
```

### E2E axe scan with Playwright

```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('no serious/critical ARIA violations on checkout', async ({ page }) => {
  await page.goto('/checkout');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa', 'best-practice'])
    .disableRules(['color-contrast']) // covered separately
    .analyze();
  const blocking = results.violations.filter(v => ['serious', 'critical'].includes(v.impact!));
  expect(blocking, JSON.stringify(blocking, null, 2)).toEqual([]);
});
```

### Combobox name/state pattern (APG)

```html
<label id="cmb-lbl">Country</label>
<div role="combobox"
     aria-labelledby="cmb-lbl"
     aria-controls="cmb-listbox"
     aria-expanded="true"
     aria-activedescendant="opt-de"
     tabindex="0">United States</div>
<ul id="cmb-listbox" role="listbox" aria-labelledby="cmb-lbl">
  <li id="opt-us" role="option" aria-selected="true">United States</li>
  <li id="opt-de" role="option" aria-selected="false">Germany</li>
</ul>
```

## Common Pitfalls

| Pitfall | Why it fails | Fix |
| --- | --- | --- |
| `role="button"` on `<div>` without keyboard handlers | No Space/Enter, no focusability | Use `<button>`; if not possible add `tabindex="0"` and key handlers |
| `aria-label` on a non-interactive `<div>` | Ignored; not exposed in name calc | Apply on the interactive element or use visible text |
| `aria-hidden="true"` on a focusable element | Focus reachable but invisible to AT | Also set `tabindex="-1"` and remove from tab order |
| `aria-labelledby="x"` where `#x` doesn't exist | Empty accessible name | Validate IDREFs; jest-axe + axe rule `aria-valid-attr-value` |
| `role="presentation"` on an `<img>` with meaningful alt | Strips semantics from real content | Use empty `alt=""` only for decorative images |
| Toggle button without `aria-pressed` | State not announced | Add `aria-pressed="true|false"`, not `aria-checked` |
| Live region added at runtime | NVDA/JAWS often miss the first announcement | Render `aria-live` container at load; mutate its text |
| `tabindex` > 0 | Breaks natural tab order | Use `0` or `-1` only |

## Output Format

When auditing, emit a per-component table:

```
Component: ProductCardMenu
  Role:           menu        ✅
  Accessible name: "More actions for Acme Mug" via aria-label   ✅
  State:           expanded   ✅ (aria-expanded mirrors open)
  Keyboard:        Enter/Space/Esc/Arrows   ✅
  APG conformance: menu pattern §3.16   ✅
  axe violations:  0 critical / 0 serious / 1 moderate (color)
  AT smoke:        NVDA ✅  VoiceOver ✅  JAWS ⚠ (re-announces on close)
```

## References

- W3C — WAI-ARIA 1.3: <https://www.w3.org/TR/wai-aria-1.3/>
- W3C — ARIA Authoring Practices Guide (APG): <https://www.w3.org/WAI/ARIA/apg/>
- W3C — ARIA in HTML: <https://www.w3.org/TR/html-aria/>
- Deque — axe-core rules: <https://dequeuniversity.com/rules/axe/>
- WCAG 2.2 (W3C Recommendation): <https://www.w3.org/TR/WCAG22/>
- EN 301 549 v3.2.1: <https://www.etsi.org/deliver/etsi_en/301500_301599/301549/>
