---
name: product-ux-quality
description: Making software feel finished — UI states, forms, mobile, errors users can act on, accessibility, and the polish gap between "works" and "quality product". Use when building any user-facing screen or flow, reviewing UX, handling forms/validation, or when the user says "polish", "UX", "user experience", "looks unfinished", "empty state", "mobile", or "make it production quality".
---

# Product & UX Quality

Users never see your architecture; they see whether the button did something. "High quality product" is decided in the last 20% — the states, edges, and moments most developers (and most AI models) skip because the happy path already demos well. This skill is that 20%, as a checklist you don't get to skip.

## The Five States rule — every screen, no exceptions

Any view that shows data has five states, and shipping fewer is shipping a bug:

1. **Loading** — skeleton matching the final layout (not a lone spinner, never a blank flash).
2. **Empty** — a designed moment, not "No data": say what this screen will show and give the action that creates the first item ("No invoices yet → Create your first invoice"). Empty states are the new user's entire first impression of your product.
3. **Error** — human words + a retry action. Never a raw error code, never a dead end.
4. **Partial/short data** — 1 item, 3 items: does the layout still look intentional?
5. **Overflow** — 10,000 items, a 60-character name, a ₹9,99,99,999 amount: pagination, truncation with tooltip, layout survives.

Build all five *while building the screen* — a shared query-state component makes state 1–3 free forever; retrofitting is 5× the cost.

## Forms — where products win or lose users

- Validate inline, on blur, with the message *next to the field* — not an alert after submit, and never only server-side (but always also server-side; client validation is UX, not truth).
- Error messages say how to fix: "Mobile number must be 10 digits" not "Invalid input".
- Submit buttons: disabled while submitting with a working indicator (prevents the double-submit that idempotency guards against — fix it at both layers), and the label says what happens ("Create Invoice", not "Submit", not "OK").
- Never lose user input: failed submits keep the form filled; destructive navigation away from a dirty form asks; long forms save drafts if abandonment costs real work.
- Smart defaults everywhere: today's date pre-filled, last-used values remembered, focus in the first field, Enter submits.

## Feedback — the app must answer every action

Every user action gets an acknowledgment within 100ms (pressed state, spinner, optimistic update) and a completion signal (toast for background outcomes, navigation or visible state change for foreground ones). Silent success is indistinguishable from failure — users retry, and now you have duplicates. Destructive actions (delete, cancel, void) get a confirm that names the object ("Delete invoice INV-042?") and, where feasible, undo instead of confirm.

## Errors users can act on

Map every failure to: what happened (in domain language) + what to do now. "Payment couldn't be recorded — the invoice was modified by someone else. Refresh and retry." Categories worth distinct handling: offline/network (detect and say so), permission (explain, don't just hide), validation (fix-it guidance), server fault (apologize, retry button, and *you* got the Sentry event — never ask users to report codes).

## Mobile & real-world conditions

Test every screen at 360px width before calling it done — tables become cards or scroll containers deliberately, tap targets ≥ 44px, no hover-only affordances, correct keyboard types (`inputmode="numeric"` for amounts/OTP), and the layout survives the on-screen keyboard. Then throttle to slow 3G once: does the app communicate, or hang blankly? Your users' network is worse than your office's.

## Accessibility — the 20% of effort that's non-negotiable

Semantic HTML (real `<button>`, real `<label for>` on every input, headings in order), keyboard-completable flows (tab order, visible focus, Esc closes modals and traps focus within), alt text on meaningful images, 4.5:1 text contrast, and never color as the only signal (paid=green/overdue=red also needs the word). Screen-reader-announce async updates (aria-live for toasts). This list catches ~80% of failures and costs minutes when done inline.

## Consistency & microcopy

One term per concept everywhere (pick "Party" or "Customer" or "Client" — once); one date/number/currency format (₹1,23,456.00 Indian grouping if that's the market — locale is a product decision, not a library default); the same action in the same place on every screen. Capitalization, button order (primary right or left — just *pick*), and spacing scale consistent app-wide. Inconsistency reads as carelessness, and users extrapolate carelessness to your handling of their money.

## The finish-line test

Before calling a flow done, run it as a hostile new user on a phone with bad network: double-click everything, submit garbage, go back mid-flow, refresh mid-submit, resize wildly. What breaks embarrasses you *now*, cheaply — or later, expensively.
