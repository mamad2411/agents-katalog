---
name: ux-essentials
description: Use when evaluating or designing UI — Nielsen's 10 heuristics, mobile-first constraints, error messaging, information architecture.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [ux-wcag-a11y, frontend-design-essentials]
---

# UX Essentials

**Iron Law: Nielsen's 10 heuristics are the floor, not the ceiling. Mobile-first because constraints clarify.**

## Nielsen's 10 (the floor)

Walk every screen against these. Each violation is a bug.

| #   | Heuristic            | Pass                                          | Fail                                        |
| --- | -------------------- | --------------------------------------------- | ------------------------------------------- |
| 1   | Visibility of status | Spinner + "Loading…" on slow fetch            | Click, nothing happens, user clicks again   |
| 2   | Match real world     | "Trash", "Send"                               | `EACCES on /var/lib/x`                      |
| 3   | User control         | Undo send, soft delete                        | Modal with no close, no back                |
| 4   | Consistency          | `Cmd+S` saves everywhere                      | "Delete" / "Remove" / "Trash" — same action |
| 5   | Error prevention     | Date picker, disabled submit until valid      | Free text + regex shout                     |
| 6   | Recognition > recall | Recent files, autocomplete                    | "Type the exact name"                       |
| 7   | Flexibility          | Mouse path + `Cmd+K` shortcut                 | 47 clicks, no hotkey                        |
| 8   | Minimalist           | Show now, details one click                   | Every metric on one screen                  |
| 9   | Recover from errors  | "Email already registered. [Sign in] [Reset]" | "Error 500"                                 |
| 10  | Help & docs          | Inline `?`, searchable docs                   | 200-page PDF nobody opens                   |

Rule of thumb on (1): >100ms → show something; >1s → progress; >10s → ETA + cancel.

## Mobile-first (because constraints clarify)

The phone over Slow 4G is the default; desktop is the enhanced experience.

**Non-negotiable:**

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

Never disable user-scaling — breaks accessibility.

**Write CSS mobile-first** (`min-width` queries, not `max-width`). Base styles target the phone; layer on tablet/desktop.

**Touch targets:** 44×44 CSS px minimum (Apple HIG, Material, decade of research converge). If the visible element is smaller, pad to reach 44×44. ≥8px gap between adjacent targets.

**Performance budget** (mid-tier Android, Slow 4G, CPU 4× slowdown):

| Metric            | Budget          |
| ----------------- | --------------- |
| LCP               | < 2.5s          |
| INP               | < 200ms         |
| CLS               | < 0.1           |
| JS shipped        | < 200KB gzipped |
| Images first view | < 500KB         |

Measure on the _Mobile_ Lighthouse preset. Desktop Lighthouse lies about mobile.

**Other mobile rules:** no hover-only interactions; set `inputmode` (`numeric`, `email`, `tel`) so the right keyboard shows; use `env(safe-area-inset-*)` for notches with `viewport-fit=cover`.

## Error messages: actionable, recoverable, no codes

Three-part formula: **what happened, why (only if it changes action), what now**.

| Bad                              | Good                                                                                 |
| -------------------------------- | ------------------------------------------------------------------------------------ |
| "Something went wrong."          | "We couldn't save — your email is already registered. [Sign in] or [Reset password]" |
| "Error 422."                     | "3 fields need attention" + scroll to first                                          |
| "Invalid date."                  | "Use MM/DD/YYYY (e.g., 03/15/2026)."                                                 |
| "Password requirements not met." | "Add at least one number."                                                           |
| "Failed to save."                | "Your session expired. [Sign in again]"                                              |

**Hide status codes from end users.** Log the code + correlation id; show the human message. Optionally surface the id ("Reference: abc-123") for support.

| Code        | Hide; show instead                                         |
| ----------- | ---------------------------------------------------------- |
| 401         | "Your session expired. [Sign in again]"                    |
| 403         | "You don't have access. [Request access] [Back]"           |
| 404         | "We couldn't find that. [Home] [Search]"                   |
| 409         | Specific: "Name taken." / "Someone edited this — [Reload]" |
| 429         | "Too many requests. Try in N seconds."                     |
| 500/502/503 | "Something on our end broke. We've been notified. [Retry]" |

**Placement tiers** — match UI to recoverability:

| Tier                                         | When                              |
| -------------------------------------------- | --------------------------------- |
| Inline (under field, `aria-describedby`)     | Validation, format errors         |
| Form-level banner                            | Multi-field, server validation    |
| Page-level banner                            | "You're offline. We'll sync."     |
| Toast (≤6s, dismissible if it has an action) | Non-blocking with retry           |
| Modal                                        | Data-loss risk, requires decision |
| Full-page                                    | 404/500 on a route                |

**Don't use a modal where a toast would do.** Don't auto-dismiss errors with an action — the user might miss [Retry].

**Tone:** calm, plain (sixth-grade), brief, human. Not cute ("Whoopsie!" is patronizing when work was lost). Never blame the user — "We need this in MM/DD/YYYY format" beats "You entered an invalid date."

## Information architecture

The skeleton. Get it wrong and no UI polish saves it.

**Start from the user's mental model, not the org chart.** If your top nav reads like `/teams/`, redo it.

**Card sort** for grouping: 30-50 concept cards, 5-10 users, open or closed. Cards that always cluster → group in UI. Cards users can't categorize → name is unclear. Categories users invent → adopt their labels.

**Hierarchy:** broad-shallow beats narrow-deep. Users prefer scanning siblings over drilling levels. ~3 clicks to anything important.

| Pattern     | Use when                                                  |
| ----------- | --------------------------------------------------------- |
| Top nav     | 5-7 sections, desktop-primary                             |
| Side nav    | Many sections, app-like                                   |
| Hamburger   | Mobile only — hiding nav on desktop hurts discoverability |
| Tabs        | Switching views of the _same_ object                      |
| Breadcrumbs | Deep hierarchies, deep links                              |
| Bottom nav  | Mobile apps, 3-5 destinations                             |

**Never two primary navs.** Decide.

**Search vs browse:** most apps need both. Search forgives typos, shows results as you type for catalogs, highlights matches. If users search for things in your nav, your labels are wrong.

**Labels** are load-bearing. Use the user's words (cards, search logs, support tickets). Concrete over clever — "Pricing" beats "Plans & Possibilities."

**URLs are IA:** readable (`/products/blue-widget` not `/p?id=4827`), hierarchical, lowercase-hyphenated, stable, 301-redirect renames.

## Anti-patterns

- "Something went wrong." in any user-facing surface
- Desktop-first design, mobile bolted on later
- Infinite nesting menus ("Other" / "More" / "Tools" graveyards)
- Status codes visible to end users (`Error 500`, `NullReferenceException`)
- Disabling user-scaling on mobile
- Hover-only interactions (touch has no hover)
- Placeholder as label
- Auto-dismiss on an error that has a [Retry]
- 12+ top-level nav items by accretion
- Free-text date fields with regex validators after submit
- Nav routed by the org chart (`Billing Team`, `Identity Team`)

## Red flags

| Excuse                                | Reality                                                                          |
| ------------------------------------- | -------------------------------------------------------------------------------- |
| "Users will learn it"                 | They won't. They churn.                                                          |
| "It's how we've always done it"       | Heuristic #4 isn't "consistent with our bad past."                               |
| "The error is technically accurate"   | Accurate to _you_, not the user.                                                 |
| "Desktop traffic is most of ours"     | Mobile is the majority globally. Your mobile bounce explains your desktop ratio. |
| "We added search, nav doesn't matter" | Most users still browse. Search is the fallback.                                 |
| "Power users want it dense"           | Dense _and_ friendly. Both.                                                      |

## Hand-off

For accessibility (WCAG 2.1 AA, keyboard, screen readers, contrast): `Skill(ux-wcag-a11y)`. For design tokens, theming, component architecture, typography, colour: `Skill(frontend-design-essentials)`.
