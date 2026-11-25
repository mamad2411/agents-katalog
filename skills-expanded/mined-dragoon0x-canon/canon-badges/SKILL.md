---
name: canon-badges
description: Use when designing, auditing, or refactoring badges, pills, chips, tags, status indicators, count badges, notification dots, or any small piece of UI metadata. Covers when a badge is appropriate, sizing, color coding for status, count formatting, the "dot vs number" decision, accessibility for notifications, and the difference between badges, chips, and tags. Trigger when the user mentions badge, pill, chip, tag, label, status pill, count, or notification dot.
---

# CANON · Badges

Small metadata shapes. Badges, chips, pills, and tags are all adjacent concepts; the right name matters less than the right behavior.

## What belongs in a badge

| Appropriate | Not appropriate |
|---|---|
| Status ("Active", "Draft") | Full sentences |
| Count (3, 99+) | Paragraph-length content |
| Category or tag (frontend, urgent) | Primary actions |
| Labels on entities (beta, new) | Navigation links |
| Version numbers ("v2.1") | Buttons |

Badges are metadata. If users click a badge and something changes, they expected a button.

## Badges vs chips vs tags

| Pattern | Interactive? | Use |
|---|---|---|
| **Badge** | Usually no | Display-only metadata (status, count, version) |
| **Chip** | Yes | Selected filters, removable tokens, multi-select |
| **Tag** | Optional | Categorization; either display or selectable |
| **Notification dot** | No | Unseen-items indicator |

Most are the same visual shape (rounded rectangle) but different behavior. Don't make display-only badges look clickable — confuses users.

## Sizing

| Size | Height | Padding | Font |
|---|---|---|---|
| XS | 16–18px | 4–6px horizontal | 10–11px |
| **SM** | 20px | 6–8px | 11–12px |
| MD | 24px | 8–10px | 12–13px |
| LG | 28–32px | 10–14px | 13–14px |

Most UI badges are SM or MD. XS only for dense tables and inline markers.

Border radius: 4–6px for rectangular feel, `999px` for pill. Stay consistent within a UI.

## Color coding — status conventions

Users learn color semantics. Respect the conventions.

| Intent | Color | Examples |
|---|---|---|
| Success / active | Green | "Published", "Active", "Online" |
| Info / neutral | Blue or gray | "Draft", "New", "Info" |
| Warning | Yellow / amber | "Expiring soon", "Review needed" |
| Danger / error | Red | "Failed", "Overdue", "Blocked" |
| Muted / inactive | Gray | "Archived", "Inactive" |

**Color alone is never the only signal.** Pair with the label text. WCAG 1.4.1.

### Tonal badges (preferred)

Instead of saturated-fill badges (loud), use tonal:
- **Light background** (10–15% of the hue's lightness zone) +
- **Dark text** (60–70% of the hue's lightness zone).

```css
.badge-success {
  background: oklch(95% 0.03 145);
  color: oklch(35% 0.10 145);
}
```

Tonal badges integrate into interfaces without screaming. Reserve saturated fills for genuine alerts.

Ensure 4.5:1 contrast between badge text and badge background.

## Count badges

```
Inbox  3
Inbox  99+
```

- Show 1–99 as the exact number.
- Over 99 → "99+".
- 0 count → usually **don't show the badge at all**. An empty badge signals nothing.
- Position: trailing the label, not leading.
- If overlaid on an icon (notification on bell icon): top-right corner with slight offset.

## Notification dot vs count

| Use dot | Use count |
|---|---|
| Binary "something's here" signal | User needs to know how many |
| Mobile tab bar badges | Email inbox |
| Icon buttons with unseen items | Task list with unread items |

Dots are less informative but cleaner. Pick per context.

## Notification badge on an icon

```
   🔔
   ●
```

- 8–10px dot for binary presence.
- Small numeric badge (14–16px) with value when count is meaningful.
- Top-right corner of the icon, offset 0–4px.
- Ring around the badge matching the background — separates from the icon.

```css
.icon-badge::after {
  content: '';
  position: absolute;
  top: -2px;
  right: -2px;
  width: 8px;
  height: 8px;
  background: var(--color-danger);
  border: 2px solid var(--surface-bg);
  border-radius: 50%;
}
```

## Accessibility for notification badges

Visual-only badges are invisible to screen readers.

```html
<button aria-label="Notifications (3 unread)">
  <svg aria-hidden="true">...</svg>
  <span class="badge" aria-hidden="true">3</span>
</button>
```

- `aria-label` on the button includes the count in words.
- `aria-hidden` on the visual badge to prevent double-announcement.
- Or use `aria-live="polite"` on the count element to announce changes as they happen.

## Chip (interactive, removable)

```
┌─────────────────────┐
│  urgent     ✕       │
└─────────────────────┘
```

- Clickable region (whole chip selects, or toggles).
- Remove button inside (✕ icon).
- Clear hover, focus, and selected states.
- `<button>` semantics for the whole chip, or `<button>` for the X inside.
- Min hit target 44×44 on mobile (even if visual size is smaller, padding covers it).

## Filter chips

```
[All] [Active] [Draft] [Archived]
```

- Horizontal row, scrollable on mobile.
- Selected chip visually distinct (filled vs outlined).
- Single-select or multi-select behavior should be obvious from the context.
- For multi-select: toggle on click, show count of selected if many.

## Tag

- Usually categorical, lower-visibility than status badges.
- Multiple tags per item is common.
- Colors can be author-chosen (GitHub labels) or deterministic (hashed from tag name for consistency).
- Content is short — 1–3 words max.

## Placement conventions

| Context | Placement |
|---|---|
| List item with status | Trailing right |
| Card header | Top-right corner |
| Inline with heading | Right after the heading text |
| Navigation item with count | Trailing |
| User avatar with role | Below or beside |
| Version label | Beside product name |

Be consistent across the app.

## Truncation

Badge content stays short. If a tag or label genuinely can't fit, truncate with ellipsis and reveal full text on hover/focus. But usually the right answer is shorter labels.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Badge with sentence-long text | Defeats the "glance" purpose |
| Color as the only signal ("the red one is broken") | Colorblind fail |
| Showing "0" count badges | Noise; badge means "something here" |
| Saturated red/yellow/green fills everywhere | Alert fatigue |
| Badge styled identical to an actionable button | Users click expecting action |
| Counts inside a `<span>` without live-region or label | Screen reader silent when count changes |
| Badge position varies across list items | Visual instability |
| No contrast check on tonal colors | Quiet contrast fails |
| Over-decorated badges (shadows, gradients) | Visual noise |
| Interactive chip with no hover state | Users don't know they can click |
| Mixing chips and badges interchangeably | Users learn one pattern, get confused by another |

## Decision tree

```
Is this interactive?
  ├─ No → Badge
  └─ Yes → Chip

What does it represent?
  ├─ Status/state → Status badge, semantic color
  ├─ Category/tag → Tag, optional color
  ├─ Count → Count badge
  ├─ Binary presence → Notification dot
  └─ Selection in a filter → Filter chip

Is color the only signal?
  └─ Always pair with text or shape — never color-only
```

## Audit checklist

- [ ] Text is short (1–3 words or a count)
- [ ] Color paired with text label (never color-only)
- [ ] Contrast ≥ 4.5:1 between badge text and background
- [ ] Tonal backgrounds used instead of saturated for passive states
- [ ] Count badges show "99+" above 99
- [ ] Zero counts hidden
- [ ] Notification badges on icons include count in `aria-label`
- [ ] Non-interactive badges don't look clickable
- [ ] Interactive chips have hover/focus/selected states
- [ ] Chip remove buttons have `aria-label`
- [ ] Placement consistent across the UI
- [ ] Mobile hit target ≥ 44px on interactive chips

## Sources

- WCAG 2.2 · 1.4.1 Use of Color, 1.4.3 Contrast (Minimum), 4.1.3 Status Messages
- Material Design 3 · Chip, Badge
- Apple HIG · Badges, Tags
- GitHub Primer · Label / Badge guidance
