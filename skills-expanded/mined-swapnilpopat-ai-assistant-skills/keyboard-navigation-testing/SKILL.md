---
name: keyboard-navigation-testing
description: Validate that every interactive element is reachable, operable, and visible to keyboard-only users per WCAG 2.2 (2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 2.5.7, 2.5.8). Use when auditing pages, custom widgets, or fixing focus-trap and tab-order bugs.
source: self
date_added: 2026-05-01
---

# Keyboard Navigation Testing

A systematic protocol for proving a UI is fully usable without a mouse — covering reachability, focus order, focus visibility, focus management, and the new WCAG 2.2 success criteria (Focus Not Obscured, Dragging Movements, Target Size).

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Spec | WCAG 2.2 (2.1.1, 2.1.2, 2.1.4, 2.4.3, 2.4.7, 2.4.11/12, 2.5.7, 2.5.8), APG 1.3 patterns |
| Manual aids | Visual focus highlighter (Accessibility Insights "Tab stops"), Polypane keyboard view |
| Automated | Playwright `keyboard.press`, Cypress `cy.tab()` (cypress-plugin-tab), @axe-core focus rules, Storybook `@storybook/addon-a11y` |
| Devices | External USB keyboard (not just laptop), iPadOS Magic Keyboard, Android Bluetooth keyboard, switch device (where applicable) |

## When to Use

- Pre-merge check on any new interactive component or page.
- Regression after CSS refactors (`outline: none`, z-index, overflow).
- Fixing reported focus traps, skipped controls, or "I can't close this dialog".
- Preparing for VPAT / EN 301 549 evidence.

## The 12-Step Manual Protocol

Use a real keyboard. Disconnect/ignore the mouse.

1. **Tab from URL bar** to the start of the page. First stop should be a visible "Skip to main" link (2.4.1).
2. **Tab through every interactive element** — links, buttons, inputs, custom widgets, iframes. Each must receive focus.
3. **Focus order matches visual/reading order** (2.4.3). No surprise jumps.
4. **Focus indicator visible at all times** (2.4.7) — ≥ 2 px outline, ≥ 3:1 contrast vs. adjacent (2.4.11/12).
5. **Focus never obscured** by sticky headers, footers, cookie banners (2.4.11 AA / 2.4.12 AAA).
6. **Activate** controls: Enter on links/buttons, Space on buttons/checkboxes, Arrow keys on radios, sliders, menus, tabs, listboxes, trees (per APG).
7. **Composite widgets** behave per APG (Tab in/out; arrows within). Tabs use roving tabindex; menus close on Esc and return focus to trigger.
8. **Modals/dialogs trap focus** while open, restore focus on close, close on Esc.
9. **No keyboard traps** outside intentional dialogs (2.1.2). Shift+Tab always works.
10. **Custom drag interactions have a single-pointer / keyboard alternative** (2.5.7 — Dragging Movements, AA).
11. **Target size ≥ 24×24 CSS px** for pointer targets (2.5.8 AA) — keyboard users still benefit when targets group correctly.
12. **No content requires character-key shortcut without an off switch** (2.1.4).

## Automated Checks

### Playwright tab-order assertion

```ts
import { test, expect } from '@playwright/test';

test('checkout: tab order matches visual order', async ({ page }) => {
  await page.goto('/checkout');
  const expected = [
    'Skip to main content',
    'Email',
    'Card number',
    'Expiry',
    'CVC',
    'Place order',
  ];
  for (const name of expected) {
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => {
      const el = document.activeElement as HTMLElement | null;
      return el ? (el.getAttribute('aria-label') || el.innerText || (el as HTMLInputElement).labels?.[0]?.innerText || '').trim() : '';
    });
    expect(focused).toBe(name);
  }
});

test('dialog traps focus and restores on close', async ({ page }) => {
  await page.goto('/projects');
  await page.getByRole('button', { name: 'Delete' }).focus();
  await page.keyboard.press('Enter');
  // Tab cycles only inside dialog
  for (let i = 0; i < 6; i++) await page.keyboard.press('Tab');
  await expect(page.locator('role=dialog')).toContainText('Delete project?');
  // Esc closes and returns focus
  await page.keyboard.press('Escape');
  await expect(page.getByRole('button', { name: 'Delete' })).toBeFocused();
});
```

### Storybook visual focus story

```ts
// Button.stories.ts
export const FocusVisible = {
  parameters: { pseudo: { focusVisible: true } },
  play: async ({ canvasElement }) => {
    const btn = canvasElement.querySelector('button')!;
    btn.focus();
  },
};
```

### Focus-visible CSS contract

```css
:where(a, button, [role='button'], input, select, textarea, [tabindex]):focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
  border-radius: inherit;
}
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| `outline: none` with no replacement | Use `:focus-visible` with a 2 px ring meeting 3:1 contrast |
| `tabindex="-1"` on a primary action to hide it | Hide via `inert` attribute on the wrapper instead |
| Click-only handlers on `<div>` | Use `<button>` (or add `role`, `tabindex`, key handlers, and disabled state) |
| Modal opens but focus stays on background | Move focus to first focusable inside; trap until close |
| Dropdown opens on hover only | Add click + keyboard activation; arrow keys to navigate |
| Focus jumps off-screen behind sticky header | Add `scroll-padding-top` or scroll into view on focus |
| Carousel auto-advances mid-tab | Pause on focus / hover (2.2.2) |
| Cookie banner intercepts every Tab | Render last in DOM and focus-trap only when open |

## Output Format

```
Page: /checkout
Tab stops: 14 expected, 14 found, order ✅
Focus visible: ✅ (2px #1F6FEB on all stops; contrast 4.6:1 vs neutrals)
Focus not obscured: ✅
Focus traps:
  - Cancel dialog: trap ✅, Esc ✅, restore ✅
Composite widgets:
  - Country combobox (APG): keys ✅, aria-activedescendant ✅
WCAG 2.2 new SC:
  2.4.11 Focus Not Obscured: ✅
  2.5.7 Dragging Movements: N/A
  2.5.8 Target Size: 1 violation (icon button 20×20)
```

## References

- WCAG 2.2 Recommendation: <https://www.w3.org/TR/WCAG22/>
- APG keyboard interaction patterns: <https://www.w3.org/WAI/ARIA/apg/patterns/>
- WebAIM — Keyboard Accessibility: <https://webaim.org/techniques/keyboard/>
- MDN — `:focus-visible`: <https://developer.mozilla.org/docs/Web/CSS/:focus-visible>
- Accessibility Insights — Tab Stops: <https://accessibilityinsights.io/docs/web/getstarted/fastpass/>
