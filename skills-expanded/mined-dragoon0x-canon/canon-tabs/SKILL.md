---
name: canon-tabs
description: Use when designing, auditing, or refactoring tabs, tab bars, tab panels, or any pattern switching between views without leaving the page. Covers when tabs are appropriate, active state, keyboard behavior (the roving tabindex WAI-ARIA pattern), mobile responsive behavior, overflow handling, and nested tabs. Trigger when the user mentions tabs, tab bar, tabbed interface, segmented control, or tab switcher.
---

# CANON · Tabs

Tabs group related views that share the same page scope. Users switch between them to see alternate views of the same thing. Not a substitute for navigation.

## When tabs are appropriate

| Appropriate | Not appropriate |
|---|---|
| Same entity, different views (Profile: Overview, Posts, Followers) | Unrelated pages |
| Filtering by category within a single view (All, Active, Archived) | Forms split across tabs |
| Settings organized into groups | Multi-step workflows (use stepper) |

**Forms in tabs are almost always wrong.** Users might submit without visiting a tab, or fill one and lose it on switch.

**Multi-step processes aren't tabs.** Linear flows use a stepper, not tabs.

## Max tab count

| Count | OK? |
|---|---|
| 2–4 tabs | Ideal |
| 5–7 tabs | OK if labels are short |
| 8+ tabs | Redesign — use a sidebar or dropdown |

If tabs start overflowing the container, either the tabs are too many or the container is too narrow. Fix the cause, not the symptom.

## Tab styles

| Style | Use |
|---|---|
| **Underline tabs** | Default for most UIs. Active tab has bottom border. |
| Filled / pill tabs | Segmented controls, mobile-native feel |
| Outlined tabs | Less common; works in dense dashboards |
| Icon + label tabs | When icons help scanning |
| Icon-only tabs (mobile tab bar) | 3–5 primary destinations (see canon-navigation) |

Underline tabs are the web default. Pill tabs often signal "filter control" more than navigation.

## Active state — not optional

Active tab is **unmistakable at a glance**. Combine signals:
- Position (underline below, or filled background)
- Weight shift (medium → semibold on active)
- Color change (muted → strong on active)

Color alone fails colorblind users. Always pair.

Active text contrast ≥ 4.5:1. Inactive text contrast ≥ 4.5:1 — tabs are text, not decoration. "Inactive looks disabled" is a bug, not a style.

## Keyboard behavior — WAI-ARIA tab pattern

This pattern is strict. Follow it exactly.

| Key | Behavior |
|---|---|
| Tab | Move focus **into** the tab list (focuses the active tab), then past it to the panel |
| Shift+Tab | Reverse |
| Arrow Right / Left (horizontal tabs) | Move focus between tabs, activating on focus (automatic) or on Enter (manual) |
| Arrow Up / Down (vertical tabs) | Same, along the vertical axis |
| Home | First tab |
| End | Last tab |
| Enter / Space | (Manual activation only) Activate the focused tab |

### Automatic vs manual activation

- **Automatic activation**: arrow keys change tabs immediately. Use when switching is cheap (client-side).
- **Manual activation**: arrow keys move focus only; Enter activates. Use when switching is expensive (network fetch) or content changes destructively.

Default to automatic. Go manual only when there's a good reason.

### Roving tabindex

Only the active tab has `tabindex="0"`. All others have `tabindex="-1"`. This keeps the tab list from trapping all tab stops.

```html
<div role="tablist" aria-label="Account sections">
  <button role="tab" aria-selected="true" tabindex="0" id="tab-overview" aria-controls="panel-overview">
    Overview
  </button>
  <button role="tab" aria-selected="false" tabindex="-1" id="tab-posts" aria-controls="panel-posts">
    Posts
  </button>
</div>

<div role="tabpanel" id="panel-overview" aria-labelledby="tab-overview" tabindex="0">
  ...
</div>

<div role="tabpanel" id="panel-posts" aria-labelledby="tab-posts" tabindex="0" hidden>
  ...
</div>
```

## Required ARIA attributes

| Element | Attribute | Value |
|---|---|---|
| Tab list | `role` | `"tablist"` |
| Tab list | `aria-label` or `aria-labelledby` | Describes the purpose |
| Tab (the button) | `role` | `"tab"` |
| Tab | `aria-selected` | `"true"` on active, `"false"` on inactive |
| Tab | `aria-controls` | id of the panel it controls |
| Tab | `tabindex` | `"0"` on active, `"-1"` on inactive (roving) |
| Panel | `role` | `"tabpanel"` |
| Panel | `aria-labelledby` | id of the controlling tab |
| Panel | `tabindex` | `"0"` so the panel is focusable (useful for scrollable content) |
| Inactive panel | `hidden` or `aria-hidden="true"` | Actually hide, not just visually |

## URL sync

Tabs should sync to the URL for deep-linking and back-button behavior.

```
/account          → overview tab
/account#posts    → posts tab
/account?tab=followers → followers tab
```

- On tab change: update URL (`history.replaceState` or `router.replace`).
- On page load: read URL, activate matching tab.
- Back button moves between tabs the user actually visited (use `pushState` if that's the intent).

Skipping URL sync costs deep-linking and breaks the back button — users will complain.

## Overflow handling

When tabs don't fit:

| Strategy | Use |
|---|---|
| **Horizontal scroll** | Default on mobile, works on desktop for 5–8 tabs |
| Scroll with arrow buttons | Desktop with 8+ tabs |
| Overflow menu (... → dropdown) | When some tabs are clearly primary and others secondary |
| Wrap to second line | Last resort, often looks broken |

On scroll, active tab should auto-scroll into view. Users shouldn't have to hunt.

## Mobile

On mobile, tabs compress. Options:
- Shorten labels ("Followers" → "People").
- Icon-only for common tabs, label underneath on mobile.
- Horizontal scroll with momentum.
- Convert to a dropdown if truly too many.

Never stack horizontal tabs vertically on mobile — that becomes navigation, not tabs.

## Nested tabs — avoid

Tabs within tabs is confusing. Two competing "you are here" signals.

If nesting feels necessary:
1. Reconsider the information architecture.
2. Use tabs at the outer level, and a different pattern (accordion, sidebar, dropdown) for the inner.
3. Or use tabs + a sub-filter chip row.

## Content transition

When switching tabs, content changes. Options:

- **Instant** (no animation): fastest, feels responsive, always works.
- **Fade** (100–150ms): smooths the change for heavy content.
- **Slide** (avoid): looks fancy, but confuses users about spatial position.

Default to instant. Fade only when content volume is large enough that the flash is jarring.

## Loading tab content

If a tab loads its panel on activate (lazy):

- Show a skeleton inside the panel for 200ms+ loads.
- Cache previously-loaded panels so switching back is instant.
- Don't reset scroll position on re-entry (remember per-panel).

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Forms split across tabs | Users submit without seeing all fields |
| Multi-step flow as tabs | Users don't know it's linear; use a stepper |
| Active tab indicated by color only | Colorblind-fail |
| No keyboard arrow support | WCAG 2.1.1 fail |
| All tabs have `tabindex="0"` | Tab key gets stuck traversing the list |
| `aria-selected` missing or on the panel | Screen readers don't know which tab is active |
| No URL sync | No deep-linking, back button broken |
| 10+ tabs in a row | Sidebar is the correct pattern |
| Inactive tabs at low contrast (looking disabled) | Users don't realize they're clickable |
| Tabs that scroll horizontally without indicator | Users don't know there's more |
| Nested tabs | Confusing hierarchy |

## Decision tree

```
Same entity, alternate views?
  ├─ No → Use navigation, filters, or pages
  └─ Yes → Tabs may work

How many?
  ├─ 2–7 with short labels → Tabs fit
  ├─ 5–7 long labels → Consider sidebar or dropdown
  └─ 8+ → Sidebar or grouped navigation

Forms or multi-step?
  ├─ Form → Single page, sectioned
  ├─ Multi-step → Stepper
  └─ Read-only views → Tabs

Desktop or mobile first?
  └─ Plan for both: horizontal on desktop, scroll or dropdown on mobile
```

## Audit checklist

- [ ] `role="tablist"` on container with `aria-label`
- [ ] `role="tab"` on each tab button
- [ ] `aria-selected` on tabs
- [ ] `aria-controls` linking tabs to panels
- [ ] `role="tabpanel"` on each panel
- [ ] `aria-labelledby` linking panels to tabs
- [ ] Inactive panels hidden with `hidden` attribute
- [ ] Roving `tabindex`
- [ ] Arrow keys cycle between tabs
- [ ] Home / End keys jump to first / last
- [ ] Active state visible (not color-only)
- [ ] Active text contrast ≥ 4.5:1
- [ ] Inactive text contrast ≥ 4.5:1
- [ ] URL syncs to active tab
- [ ] Mobile strategy (scroll, shorten, dropdown)
- [ ] No nested tabs
- [ ] Cache + scroll position preserved on tab re-entry

## Sources

- WAI-ARIA Authoring Practices · Tabs pattern (authoritative)
- WCAG 2.2 · 2.1.1 Keyboard, 2.4.3 Focus Order, 1.4.11 Non-Text Contrast
- Material Design 3 · Tabs
- Apple HIG · Segmented Controls, Tab Views
