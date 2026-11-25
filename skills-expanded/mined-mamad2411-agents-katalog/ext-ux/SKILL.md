---
name: ext-ux
description: Extension UX specialist. Owns popup, options page, onboarding, permission-request timing, and in-page UI design. Auto-invoked for popup / options / onboarding / page-overlay work.
---

# Browser Extension UX

The popup is a tiny, transient moment; the options page is where power users
live; in-page UI has to not look like malware. Each surface has different rules,
and putting a feature on the wrong one is the most common extension UX failure.

## When to reach for this

- Designing the popup, options page, or first-run/onboarding flow
- Deciding which surface a feature lives on (popup, options, side panel, in-page)
- Choosing the timing and copy for a permission request
- Injecting UI into host pages without clashing with them

## Principles

1. **One primary action per popup.** Practical width is ~360–400 px (hard max
   800×600), and the popup closes on any click outside it — never put multi-step
   flows or losable state there; everything secondary moves to options.
2. **Value before ask.** Let the extension do something useful before requesting
   optional permissions; trigger `permissions.request()` from the gesture that
   needs it and add one line of your own copy explaining what it unlocks — the
   browser's native dialog explains nothing.
3. **In-page UI must not clash.** Shadow DOM for style isolation, unique
   element/class prefixes, a deliberate z-index strategy, and respect for the
   host page's light/dark scheme. (Shadow DOM isolates styles, not security —
   that boundary belongs to `ext-security`.)
4. **Escape hatches everywhere.** Every overlay needs a dismiss, a way to
   reopen, and a per-site *and* global disable — that is the felt difference
   between a tool and malware.
5. **Accessibility survives the small surface.** Focus the primary control on
   popup open, full keyboard nav, visible focus rings, labels on icon-only
   buttons. Popups get skipped in a11y passes precisely because they're small.
6. **Onboarding is one screen with a skip.** A first-run tab covering what it
   does and the single permission ask that matters — multi-page carousels get
   skipped and burn the one moment of attention an install grants.

## Surface decision table

| Surface | Use for | Avoid for |
|---|---|---|
| Popup | status + one primary action | multi-step flows (closes on blur) |
| Options page | settings, account, advanced config | anything needed mid-task |
| Side panel (Chrome 114+) | persistent companion UI alongside the page | quick one-shot actions |
| In-page overlay | act-on-this-page features | settings; anything fragile without shadow DOM |
| Dedicated tab | onboarding, complex workflows | frequent quick access |
| Badge text | ambient status, ≤ 4 characters | anything that needs explanation |

## Pitfalls

- Async or multi-step flows in the popup that lose state when it closes on blur
- Permission asks at install/onboarding instead of at the moment of use
- Injected UI inheriting host-page CSS (no shadow DOM) or losing the z-index war
- No empty state — the popup shows a blank panel on pages where the extension
  has nothing to do
- Options page without "reset to defaults" or any indication of what changed
- Icon-only buttons with no label or tooltip in a 360 px popup
- Light-mode-only injected UI glowing white inside dark host pages

---
*Related: `ext-permissions` (what to ask for and when it's allowed),
`ext-security` (isolation of injected UI), `ux-design` (general UI critique),
`common-a11y` for deep accessibility passes · domain agent: `ext-architect` ·
output/ADR format: `playbook-conventions`*
