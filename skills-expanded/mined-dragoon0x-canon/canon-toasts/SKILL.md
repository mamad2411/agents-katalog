---
name: canon-toasts
description: Use when designing, auditing, or refactoring toast notifications, snackbars, banners, inline alerts, or any transient feedback. Covers when to use a toast vs modal vs banner, duration, positioning, stacking, the Undo pattern, accessibility (live regions), and the most common toast-as-catchall anti-pattern. Trigger when the user mentions toast, snackbar, notification, alert, banner, or feedback message.
---

# CANON · Toasts

A toast is cheap feedback for safe actions. It is not the answer to every UI question. Before reaching for a toast, ask whether an inline message, banner, or silence would serve better.

## When to use a toast

| Use a toast | Don't use a toast |
|---|---|
| Confirm a reversible action with optional Undo | Confirm a destructive action (use modal) |
| Show a background success ("Message sent") | Show a critical error needing action (use inline or modal) |
| Report completion of an async operation | Communicate persistent state (use banner) |
| Flash a brief info message ("Copied to clipboard") | Give instructions ("Now do step 2") |
| Surface a non-blocking error ("Couldn't save draft") | Confirm something users must definitely see |

**Rule of thumb**: toasts should never interrupt and never be required for the user to see. If users must see it, it's not a toast.

## Toast vs banner vs inline vs modal

| Pattern | Persistence | Location | Use |
|---|---|---|---|
| **Toast** | Auto-dismiss | Edge of viewport | Transient feedback |
| **Banner** | Stays until action or dismissed | Top of page/section | Persistent system state (you're offline, your subscription expired) |
| **Inline** | Attached to related element | Within flow | Validation errors, field-level hints |
| **Modal** | Blocks until resolved | Overlay | Critical decisions |

Wrong pattern picks waste attention. Offline? Banner, not toast. Form field error? Inline, not toast.

## Duration

| Toast length | Duration |
|---|---|
| Short (1–4 words) | 3 seconds |
| **Default** (short sentence) | 4 seconds |
| With action (has Undo/Retry button) | 5–7 seconds |
| Persistent (on user demand) | Until dismissed |

The timer **pauses on hover and focus** — critical for screen reader + motor-impaired users.

Material snackbar default is 4 seconds without action, 10 seconds with action. Modern practice trends shorter (4–6).

## Position

| Position | Use |
|---|---|
| **Bottom-center** | Mobile, single-column apps |
| Bottom-right | Desktop web, dashboards |
| Top-right | Desktop apps that use bottom for primary content |
| Top-center | Safari mobile back button conflict, avoid |

Pick one position per app. Consistency matters.

Offset from edge: 16–24px. On mobile, account for safe-area-inset.

## The Undo pattern

**Undo toast is almost always better than "Are you sure?"**

```
┌──────────────────────────────────────┐
│ 3 items moved to trash      [Undo]   │
└──────────────────────────────────────┘
```

- Do the action immediately.
- Show a toast with an Undo button.
- Duration: 5–7 seconds (long enough to catch misclicks).
- Undo reverses the action.
- Timer pauses on hover/focus.

This is dramatically faster than a confirmation modal for the 99% case, and catches the 1% misclick.

When Undo is **not** appropriate:
- Truly irreversible actions (account deletion, payment capture).
- Actions with side effects that can't be rolled back.

For those, use a confirmation modal (see `canon-modals`).

## Stacking

- Max 3 toasts visible at once. Beyond that, collapse into a single "3 updates" toast.
- New toasts push old ones up (or down, depending on direction).
- Each toast has its own timer.
- Dismissing one doesn't affect others.

## Accessibility — ARIA live regions

Toasts must be announced by screen readers, or they're invisible.

```html
<div role="status" aria-live="polite" aria-atomic="true" class="toast">
  Message sent.
</div>
```

- `role="status"` for routine feedback.
- `role="alert"` for errors (more urgent, interrupts current SR reading).
- `aria-live="polite"` with status, `aria-live="assertive"` with alert.
- `aria-atomic="true"` so the whole message is announced, not just the change.
- The **live region container** should exist on page load, empty. Content is injected; don't mount/unmount the region itself.

Buttons inside the toast (Undo, Retry) are keyboard-focusable. Pressing Escape inside the toast moves focus back to the triggering element.

## Structure

```
┌─────────────────────────────────────────┐
│ [icon] Message sent            [X]     │
│                                [Undo]  │
└─────────────────────────────────────────┘
```

- **Optional icon** (leading): success, warning, error, info.
- **Message** (body).
- **Action button** (trailing, when applicable): one max per toast.
- **Close button** (trailing): optional; if duration is short, close button adds clutter.

## Size

| Dimension | Value |
|---|---|
| Max width | 400–560px |
| Min height | 40–48px |
| Padding | 12–16px horizontal, 10–12px vertical |
| Font size | 14px |
| Border radius | 4–8px |

## Colors by intent

Follow `canon-color` semantic tokens:

| Intent | Token |
|---|---|
| Success | `--toast-success-bg`, `--toast-success-fg` |
| Info | `--toast-info-bg`, `--toast-info-fg` |
| Warning | `--toast-warning-bg`, `--toast-warning-fg` |
| Error | `--toast-error-bg`, `--toast-error-fg` |
| Neutral | `--toast-default-bg`, `--toast-default-fg` |

Modern practice: dark-themed toasts by default (work on both light and dark themes), with colored accent via left border or icon.

## Animation

| Phase | Duration | Easing |
|---|---|---|
| Enter | 250–350ms | ease-out |
| Exit | 200–250ms | ease-in |
| Direction | Slide from edge + fade | — |

Honor `prefers-reduced-motion` with fade-only.

## Copy

| Bad | Good |
|---|---|
| Success! | Message sent |
| Operation completed successfully | Changes saved |
| Failed | Couldn't save — connection lost |
| Error: ERR_NETWORK | Couldn't reach the server. [Retry] |
| OK | Done |

- Present tense for completed actions: "Message sent" not "Message has been sent".
- Past tense acceptable if past is the natural voice: "File deleted".
- Specific > generic.
- Errors explain what + how to recover.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Toast for form validation errors | Wrong pattern; validation is inline |
| Critical errors in toasts | Users miss them, they auto-dismiss |
| Toast with no dismiss AND persists forever | Stuck UI |
| Toast replaces modal confirmation for destructive action | No clear commit moment |
| 10+ stacked toasts | Blocks content, alarm fatigue |
| No live region | Screen readers don't announce |
| Duration < 3s | Unreadable before auto-close |
| "Success!" with no specifics | Users don't know what succeeded |
| Timer doesn't pause on hover | Accessibility trap |
| Toast covering primary content | Blocks the thing users are trying to interact with |
| Centered modal-like toasts | Interrupt pattern, should be a modal |
| Banner-style persistent toasts for system state | Use a banner, don't abuse toast |

## Decision tree

```
Is the feedback critical to user's next step?
  ├─ Yes → Inline or modal, not toast
  └─ No → Toast may be appropriate

Is it a persistent state (offline, locked, expired)?
  ├─ Yes → Banner
  └─ No → Continue

Is it reversible?
  ├─ Yes → Toast with Undo
  └─ No → Consider modal confirmation first

Is it an error requiring action?
  ├─ Yes → Inline error or modal
  └─ No → Toast with context ("Couldn't load — Retry")
```

## Audit checklist

- [ ] Live region present (`role="status"` or `role="alert"`)
- [ ] Timer pauses on hover and focus
- [ ] Duration between 3–7 seconds
- [ ] Max 3 toasts stacked at once
- [ ] One action max per toast
- [ ] Position is consistent across app
- [ ] Mobile accounts for safe-area-inset
- [ ] Animation honors `prefers-reduced-motion`
- [ ] Not used for form validation errors
- [ ] Not used for critical blocking info
- [ ] Undo provided for reversible destructive actions
- [ ] Error toasts name what failed + recovery

## Sources

- WAI-ARIA Authoring Practices · Alert, Status, Live regions
- WCAG 2.2 · 2.2.1 Timing Adjustable, 2.2.3 No Timing, 4.1.3 Status Messages
- Material Design 3 · Snackbar (4s default, 10s with action)
- Apple HIG · Notifications (platform-native patterns)
- Reply (Gmail team research) · "Undo beats confirm"
