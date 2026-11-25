---
name: ui-part-notifications
description: "Notifications: choosing between a toast, an inline alert, a banner and a notification centre, their anatomy and severity colours, timing, undo and stacking, live regions and roles, the words, and placement on phones. Read before showing any message about what just happened or what needs attention."
---

# Notifications: toasts, inline alerts, banners

The generated version: a green "Success!" toast after every click, a red
toast that disappears with the only copy of an error, five toasts piled
over the page's own buttons, a banner that returns on every visit, and a
bell whose count never goes down. A notification says what happened to
what, in the place and for the time the message needs. The principles are
in the `ui` skill, where messages go in `ui-layout` (section 4), the motion
in `motion-interface` (section 6).

## 1. Choose the kind

| Kind | For | Where | Stays |
|---|---|---|---|
| Toast | a short confirmation of something the user just did, often with Undo | bottom right; bottom centre on phones | a few seconds, paused on hover and focus |
| Inline alert | this form, region or record: a failed save, a warning about the data | top of the region, or beside the cause | until fixed or dismissed |
| Banner | a state that affects the whole page or account: offline, a plan that expired, maintenance tonight | below the header, full width | until resolved; dismissible when it only informs, and remembered |
| Notification centre | what happened while the user was away: mentions, assignments, finished exports | a bell in the header opening a panel | a history, read and unread |
| Dialog | a decision needed before going on | centred | until answered (`ui-part-dialogs`) |

- An error that needs action stays: inline next to its cause, with
  `role="alert"`, until it is fixed. Never an error in a toast that
  vanishes.
- Form validation errors go under their fields and in a summary at the top
  of the form (`ui-part-forms`), never in a toast.
- No toast when the result is already visible where the user is looking:
  a row that disappears, a switch that flips, a count that changes.
  "Copied" belongs on the copy button for 2 seconds, not in a toast.
- No toast for every trivial action.

## 2. Anatomy and measures

- **Toast**: 320 to 420px wide (full width minus 16px on phones), 12 to 16px
  of padding, the overlay radius, `--surface` with a border and a soft
  shadow; a 20px icon in the severity colour; a title at 14px weight 600
  and an optional line in the muted colour; one action as a text button
  (Undo, View); a close button named "Dismiss" (32px, 44px on touch).
  16 to 24px from the screen's edges plus the safe area, 8px between
  toasts, above any sticky bar (a tab bar, a save bar, a cookie notice).
- **Inline alert**: the width of its region, 12 to 16px of padding, the
  icon, a title and a sentence, one action; a tinted background (the
  severity at 8 to 12% over the surface) with a border or a 3 to 4px bar at
  the start; the text in the normal text colour, so it keeps 4.5:1.
- **Banner**: 40 to 56px tall, the message and one action inside the page's
  container, a close button at the end when it can be dismissed. A
  promotional strip above the header scrolls away (`ui-part-header`); a
  banner about the page's state sits below the header.
- **Severity tokens**: `--info`, `--success`, `--warning`, `--danger`, each
  with a subtle background token and its own icon from the product's set.
  Text first, colour and icon second: the words still work in greyscale.

## 3. Behaviour

- **Toasts** are dismissed after four to six seconds for a few words (5s by
  default), about a second more for every ten words, 8 to 10s when they
  carry Undo. The timer pauses while the pointer is over the toasts, while
  focus is inside them, and while the tab is hidden. A toast whose action
  the user must take does not dismiss itself.
- **Stacking**: at most three visible, older ones collapsing behind or
  leaving; a repeat of the same message replaces the one showing. A
  growing stack of toasts over the page is the thing to avoid.
- **Undo** when the action can be undone: it runs (or waits until the toast
  closes), and Undo restores it and says so. For reversible actions, undo
  beats a confirmation dialog.
- **Dismissal**: a close button always, swipe on touch, Escape while focus
  is inside.
- **Focus**: toasts never take it. A hotkey moves focus to them (F8 in
  Radix Toast, Alt+T in Sonner), and an action in a toast has another way
  to reach it for someone who cannot catch it in time (Radix asks for it as
  `altText`).
- **Banners**: a dismissal is remembered per banner and version (local
  storage for visitors, the account for signed-in users), so the same one
  stays away and a new one still shows. A banner about something the user
  must fix (a failed payment) is not dismissible, only resolved.
- **Notification centre**: a bell button named with its count
  ("Notifications, 3 unread"), the badge capped at 99+; newest first,
  grouped by day; unread marked by a dot, weight and visually hidden text;
  each item a link to what it is about; "Mark all as read"; an empty state
  ("You're all caught up"); a link to notification settings.

## 4. Roles and announcements

- A toast is announced with `role="status"`, which is polite; so are most
  messages.
- `role="alert"` only for urgent errors that must interrupt: a failed save,
  a lost connection. Never for a success.
- The live region exists in the page before a message is put in it: a
  region inserted with its text already inside is often not announced.
  Toast libraries keep one region mounted; do the same by hand.
- An inline alert already there when the page loads needs no live role;
  one that appears after an action does.
- After a failed form submission, move focus to the error summary rather
  than relying on an announcement (`frontend-accessibility`).

## 5. Words

- Say what happened to what: "Invoice INV-0192 sent to the client", "3 files
  moved to Archive". Not "Success!" with nothing about what succeeded, not
  "Done".
- Errors: what failed, why if it is known, and what to do, in the user's
  terms: "Couldn't save: the connection dropped. Your changes are kept
  here; try again." Not "Error 500", "Oops" or "Something went wrong" on
  its own (`writing`).
- Sentence case, no exclamation marks, no emoji; past tense for
  confirmations; two lines at most in a toast.
- Names and numbers from the real data; the notification centre says who
  did what and when (`ui-part-dates` for relative times).

## 6. Phones, themes and motion

- Phones: toasts at the bottom centre, full width minus 16px, above the tab
  bar and the home indicator (`env(safe-area-inset-bottom)`); banners wrap
  to two lines with the action still in view; the notification centre as
  a full-screen sheet.
- Themes: severity colours and tints chosen per theme, not the light tint
  laid on the dark page; text on a tint at 4.5:1 in both (`ui-themes`).
- Motion: a toast rises 12px and fades in over 240ms, leaves with a fade and
  8px in 160ms, and pushes the others with a transform; under reduced
  motion it only fades (`motion-interface`, section 6).

## 7. A sketch

```tsx
// Sonner in React; svelte-sonner and vue-sonner port it to Svelte and Vue.
import { Toaster, toast } from "sonner";

<Toaster position="bottom-right" visibleToasts={3} closeButton />;

function archive(invoice: Invoice) {
  archiveInvoice(invoice.id);
  toast(`Invoice ${invoice.number} archived`, {
    duration: 8000,
    action: { label: "Undo", onClick: () => restoreInvoice(invoice.id) },
  });
}
```

```html
<div class="alert" data-tone="danger" role="alert">
  <svg class="alert-icon" aria-hidden="true">…</svg>
  <div>
    <p class="alert-title">Payment failed</p>
    <p>The card on file was declined. Update it to keep the plan active.</p>
  </div>
  <a class="alert-action" href="/billing">Update card</a>
</div>
```

```css
.alert {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: var(--space-2) var(--space-3);
  padding: var(--space-3) var(--space-4);
  color: var(--text);
  background: var(--danger-subtle);
  border: 1px solid var(--danger);
  border-radius: var(--radius);
}
.alert-action { grid-column: 2; justify-self: start; }
```

## Check it

- Trigger every notification the product has: each says what happened to
  what; errors stay until fixed; Undo undoes.
- Keyboard: the toast's action is reachable (the library's hotkey), the
  timer pauses while focus is inside, Escape dismisses.
- A screen reader hears each confirmation once, politely, and an urgent
  error at once; nothing is announced twice.
- `preview` at 360px: toasts and banners inside the screen and above the
  tab bar, close buttons in "touch targets under 44px" if too small,
  tinted alerts in "text below AA contrast" in either theme.
- `ui_check`: emoji in messages (a green tick emoji in a toast), generic
  actions such as "Submit".

## Avoid

Errors as toasts that vanish; a stack of toasts; "Success!" with nothing
about what succeeded; a toast for every click; validation errors in
toasts; `role="alert"` on confirmations; toasts covering the page's own
buttons or the tab bar; a banner that returns after it was dismissed; a
bell whose count never clears; coloured text on a coloured tint below
4.5:1; colour as the only difference between success and error.
