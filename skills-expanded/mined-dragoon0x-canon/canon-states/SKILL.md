---
name: canon-states
description: Use when designing or auditing empty states, loading states, error states, success states, skeleton screens, zero-data states, or any UI state that isn't the happy path. Trigger when the user mentions empty state, loading state, error state, skeleton, no data, zero state, or asks what to show when something isn't there yet.
---

# CANON · States

Every screen has at least 4 states beyond "happy path". Most products ship 1 or 2 and call it done. The states below are the contract: when reality breaks the pattern, the UI handles it gracefully.

## The Four Required States

For any data-driven screen (list, table, dashboard, feed):

| State | When | Required |
|---|---|---|
| **Initial / Loading** | Data being fetched | Always |
| **Empty** | No data exists | Always |
| **Error** | Fetch failed | Always |
| **Populated** | Data present (happy path) | The default everyone designs |

For interactive components (button, form, modal):

| State | When |
|---|---|
| **Default** | Idle |
| **Loading** | In-flight |
| **Success** | Completed |
| **Error** | Failed |

## Loading States

| Wait time | Pattern |
|---|---|
| 0–400ms | Show nothing. Below this threshold, perceived as instant. |
| 400ms–1s | Spinner appears at 400ms |
| 1s–10s | Skeleton screen OR determinate progress |
| > 10s | Progress + status + estimated remaining |

### Skeleton Screens

Skeletons reserve layout space and reduce perceived wait. Better than spinners for content that has a known shape.

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface) 0%,
    var(--color-surface-hover) 50%,
    var(--color-surface) 100%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1500ms infinite linear;
  border-radius: 4px;
}

@keyframes skeleton-shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; }
}
```

| Property | Value | Source |
|---|---|---|
| Animation duration | 1000–2000ms | Slower = calmer |
| Color contrast (skeleton vs surface) | 1.2:1 to 1.5:1 | Subtle, never high |
| Shape | Match the content shape | Don't use circles for text |
| Stop on data load | Yes (don't keep animating) | |

**Don't skeleton everything.** Skeletons are for primary content. Don't skeleton secondary chrome (sidebars, headers) that users already know.

### Spinners

Use spinners when:
- Content shape is unknown
- Action is short (1–3s)
- Inline within a button or icon

```html
<button disabled>
  <span class="spinner" aria-hidden="true"></span>
  <span class="sr-only">Saving…</span>
</button>
```

**Spinner rules:**
- Delay 400ms before showing (avoid flash for fast loads)
- Animate at 1000–1500ms per rotation (not too frenetic)
- Use brand accent color
- 16–24px size for inline; 40–48px for full-region

### Progress Bars

Use determinate progress when total is known. Indeterminate when not.

| Type | When |
|---|---|
| Determinate | File upload, multi-step wizard, known operation |
| Indeterminate | Server processing, unknown duration |
| Step indicator | Multi-step form (3 of 5) |

```html
<progress value="32" max="100">32%</progress>

<!-- Or ARIA for custom -->
<div role="progressbar"
     aria-valuemin="0"
     aria-valuemax="100"
     aria-valuenow="32"
     aria-label="Uploading file">
</div>
```

## Empty States

The empty state is the user's **first impression** of an unused feature. Treat it as onboarding.

### Three Empty State Types

| Type | When | Pattern |
|---|---|---|
| **First-time empty** | User has never created anything | Onboarding-quality: explanation + clear CTA + (optional) example/template |
| **User-cleared empty** | User deleted everything | Brief confirmation + restore option if applicable |
| **Filtered empty** | Filters/search returned nothing | "No results for X" + suggestions to refine |

### First-time Empty State Structure

```
┌─────────────────────────────────┐
│         [icon or illo]          │
│                                 │
│   You don't have any projects   │
│                                 │
│   Projects help you organize    │
│   work into separate spaces.    │
│                                 │
│   [+ Create your first project] │
│   [Browse templates]            │
│                                 │
└─────────────────────────────────┘
```

| Element | Purpose | Length |
|---|---|---|
| Visual | Quick recognition, brand presence | One icon or small illustration |
| Headline | What's empty (and a slight reframe to positive if possible) | 4–8 words |
| Description | Why this matters, what to do | 1–2 sentences |
| Primary action | The expected next step | Single button |
| Secondary action | Alternative path (browse templates, learn more) | Optional |

### Search Empty State

```
No results for "octopus"

Try a different search, or:
- Check your spelling
- Use fewer keywords
- Search in [different scope]

[Clear search]
```

### Filter Empty State

```
No results match your filters

Try removing some filters or:
[Clear all filters]
```

**Always offer "Clear filters" when filters caused the empty state.** Users often forget filters are active.

## Error States

### Error Categories

| Category | Examples | Pattern |
|---|---|---|
| **Network / connectivity** | Offline, fetch failed | Retry button, calm tone |
| **Server / 500** | Backend error | "Something went wrong", retry, support link |
| **Not found / 404** | Page or resource missing | Friendly explanation + ways forward |
| **Permission denied / 403** | Auth or authorization issue | Sign-in prompt or "Request access" |
| **Validation** | User input wrong | Specific message at the field |
| **Rate limit / 429** | Too many requests | Wait time + retry-after info |

### Error State Structure

```
┌─────────────────────────────────────┐
│           [error icon]              │
│                                     │
│   We couldn't load your projects    │
│                                     │
│   Check your internet connection    │
│   or try refreshing the page.       │
│                                     │
│   [Try again]                       │
│   [Contact support]                 │
│                                     │
└─────────────────────────────────────┘
```

| Element | Required |
|---|---|
| Headline (what failed) | Yes |
| Cause (if known and helpful) | If helpful |
| Recovery action (Try again / Refresh / Sign in) | Yes |
| Escape hatch (Contact support / Go home) | If applicable |

**Tone: calm, not alarming.** "Something went wrong" beats "FATAL ERROR". Don't apologize excessively. Don't blame the user.

### Inline vs Full-screen Errors

| Scope | Pattern |
|---|---|
| Single field | Inline message below field |
| Single component / card | Replace component content with error state |
| Full page | Full-screen error |
| Recoverable action | Toast: "Couldn't save. Retry?" |

## Success States

Success states confirm an action without blocking.

| Pattern | When |
|---|---|
| Toast (auto-dismiss in 3–5s) | Default for routine actions |
| Inline message | When user is still on the form |
| Full-page success | Multi-step flows (signup complete, payment received) |
| Animation | Subtle: button checkmark, list item checkmark |

```
Toast structure:
[icon] [message]                          [×]
       (optional secondary action)

Examples:
✓ Saved
✓ Project created
✓ 5 items moved to Archive  [Undo]
```

### Undo Pattern

For destructive or significant actions, prefer **action + Undo toast** over **confirmation dialog + action**.

```
Before: "Are you sure you want to delete? [Cancel] [Delete]"
After:  Item deleted. [Undo]   (toast, 5-second window)
```

Undo is the more humane pattern. Reserve dialogs for irreversible actions.

## Offline State

If your app needs the network:

```
Banner at top of viewport:
⚠ You're offline. Changes will sync when you reconnect.
```

| Pattern | When |
|---|---|
| Read-only mode | Cached data viewable, edits queued |
| Banner persistent | While offline |
| Toast on reconnect | "Back online. Synced 3 changes." |

## Permission / Auth States

| State | Pattern |
|---|---|
| Unauthenticated | "Sign in to view this" + sign-in CTA |
| Wrong account | "This belongs to another account. Switch accounts." |
| No permission | "You don't have access. Request access from [admin]." |
| Plan limit | "You've reached your plan's limit. Upgrade to add more." |

**Never show a blank screen or generic 403.** Always explain why and what's next.

## Loading Inside Loaded

When a sub-region of a populated page loads (filter change, pagination):

| Pattern | When |
|---|---|
| Skeleton replacing only the changing region | Default |
| Subtle dim + spinner overlay | Brief operations |
| Disabled state on filter controls | While re-fetching |

**Don't reset scroll position** when loading new data into an existing page. Maintain context.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| No empty state designed | First impression is "broken" | Design it from day one |
| Empty state is just "No data" | No path forward | Add explanation + CTA |
| Skeleton that doesn't match content shape | Misleading | Match the actual shape |
| Spinner without delay (fires at 0ms) | Flash of spinner on fast loads | Delay 400ms |
| Spinner spinning at 200ms per rotation | Frenetic, anxiety-inducing | 1000–1500ms |
| Generic 500 page | User stuck | Specific message + recovery |
| Error with no recovery action | User stuck | Always offer next step |
| Error tone alarming ("FATAL") | Anxiety | Calm, "Something went wrong" |
| Confirmation dialog for everything | Friction | Use Undo toasts for reversible actions |
| Success toast that blocks the next action | UX block | Toast doesn't block |
| Loading state that obscures previous content | Lost context | Skeleton or inline loader |
| Search empty without "Clear search" | User trapped in dead end | Always offer escape |
| Filter empty without "Clear filters" | Same trap | Always offer escape |
| Offline mode that loses data | Trust killer | Queue changes, sync on reconnect |
| Error state that disappears if user clicks anywhere | Race condition | Persistent until resolved |

## Decision Tree

```
Building a screen?
├─ List its 4 states: loading, empty, error, populated
├─ Loading state: skeleton if shape known, spinner otherwise, 400ms delay
├─ Empty state: headline + description + primary action
├─ Error state: what failed + recovery action
└─ Populated: the happy path

Building an action?
├─ Loading: button shows spinner, disabled, label changes to present-continuous
├─ Success: toast or inline acknowledgement, present past-tense
├─ Error: inline message at the field or toast with retry
└─ Undo: offer for destructive actions (5s window)
```

## Audit Checklist

1. For each list/table/dashboard, all 4 states (loading, empty, error, populated) implemented?
2. Empty states have headline + description + primary action?
3. Error states have a recovery action (try again, contact support)?
4. Loading delays of 400ms in place to avoid flashing spinners?
5. Skeletons match the shape of the content?
6. Skeletons stop when data loads (no infinite shimmer)?
7. Filter/search empty states offer "Clear" actions?
8. Destructive actions use Undo toast or require explicit confirmation?
9. Offline state designed if network is required?
10. Auth/permission failures explain and offer next steps?

## Citations

- Material Design 3 Communication (Loading): https://m3.material.io/components/progress-indicators/overview
- Apple HIG Loading: https://developer.apple.com/design/human-interface-guidelines/loading
- Nielsen Norman Group, Skeleton Screens: https://www.nngroup.com/articles/skeleton-screens/
- Refactoring UI, Working With Empty States
- Andrew Coyle, *Designing Better Empty States*: https://uxdesign.cc/designing-better-empty-states
- Web Almanac on Performance Indicators
