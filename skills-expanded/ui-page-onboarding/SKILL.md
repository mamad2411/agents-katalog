---
name: ui-page-onboarding
description: "First-run and onboarding: getting a new user to the product's first real result quickly, what to ask and what to skip, progress, sample data marked as sample, checklists, empty states that teach, and why tours rarely help. Read before building sign-up follow-ups, setup flows or a first-run experience."
---

# Onboarding and first run

The generated first run is a welcome modal, a carousel of benefits, a survey
about company size and how you heard of us, a tour of eight popovers
pointing at the sidebar, and then a dashboard of zeroes. None of it brings
the user closer to what they signed up for. Onboarding has one job: the
product's first real result, for this user, in minutes. The steps pattern
is in `ui-part-steps`, teaching empty screens in `ui-part-empty-states`,
the sign-in page in `ui-page-sign-in`, the measures in `ui-layout`.

## 1. Name the first real result

- Write it down in the product's words before designing anything: the
  first invoice sent, the first site deployed, the first report built from
  their own numbers, the first booking received. It is something the user
  makes with the product, not something they read about it.
- List the steps between sign-up and that result. Everything not on the
  list moves later or goes.
- Where the product has analytics, reaching that result (activation) is
  the event to watch. Without real data, do not quote drop-off rates or
  promise "under two minutes".

## 2. The skeleton

```
sign up ─▶ verify email (not blocking) ─▶ setup, 1 to 3 short steps ─▶ first result ─▶ home + checklist
                                              └── Skip setup ──────────────────────────────▲
```

A setup step:

```
│ [Logo]                                         Step 1 of 3 · Skip setup │
│                                                                         │
│   Where do you sell?                                         (h1)       │
│   We use it to set your currency and tax.                    the reason │
│                                                                         │
│   Country    [ Indonesia                  ▾ ]   from the browser        │
│   Currency   [ IDR ▾ ]                                                  │
│                                                                         │
│   [ Continue ]                                                          │
```

The checklist on the product's home:

```
┌ Get set up · 2 of 5 ─────────────────────────────────── [Hide] ┐
│ ✓ Create your shop                                              │
│ ✓ Add your first product                                        │
│ ○ Connect a payment provider                       [ Connect ]  │
│ ○ Set delivery rates                                            │
│ ○ Invite a teammate (optional)                                  │
└─────────────────────────────────────────────────────────────────┘
```

Setup screens have no app shell: a slim top bar with the logo, the progress
and "Skip setup", one column of 480 to 560px, left-aligned or centred as
one block.

## 3. What to ask, and what to skip

- Ask only what changes what the user sees next: the use case that picks a
  template, the country that sets currency and tax, the workspace's name.
  Each question has one line under it saying why.
- Fill in what you already know: the name from the sign-up provider, the
  language and time zone from the browser, a workspace name suggested from
  the email's domain.
- Defer everything else to the moment it is needed: photo, job title,
  phone number, billing details, preferences, notification settings.
- A marketing question (company size, how did you hear about us): at most
  one, optional, after the first result.
- No card for a trial unless the business truly needs one, and then said on
  the sign-up page, not discovered during setup.

## 4. The setup steps

- 1 to 3 steps of one question or one small group each, with "Step 1 of 3"
  (`ui-part-steps`); Back keeps answers; every step that is not required
  can be skipped.
- "Skip setup" is always visible and lands on a working product whose empty
  screens teach, not on a dead end.
- Answers are saved on the server as they go, so a closed tab or another
  device resumes where the user left.
- Work that takes time (creating a workspace, importing data) says what is
  happening and roughly how long, with real progress where it exists, and
  lets the user start while an import runs in the background, with a
  notification when it is done.
- The last step leads straight into the first result (the editor with the
  chosen template open, the draft invoice, the import running), not to a
  "You're all set!" page.

## 5. Sample data and templates

- When the product means nothing empty (analytics, a CRM, a dashboard),
  offer a demo project with sample data: a "Sample" badge on the project
  and its records, a banner ("You are looking at sample data. Start with
  your own"), and removal in one action.
- Sample data lives apart (its own project or workspace), never mixes into
  real reports, exports, billing or usage, and can never be sent to anyone
  (a sample invoice cannot be emailed).
- A template beats a blank page: start from the template for the use case
  chosen in setup, with real structure and placeholder content that says
  it is a placeholder.

## 6. The checklist

- On the product's home (or in the sidebar), 3 to 6 tasks that lead to
  real use, ordered by value, the optional ones marked optional.
- Each item names a task and has the one action that does it. It ticks
  itself when the task is done anywhere in the product, never because the
  user clicked the item.
- Progress in words and a bar ("2 of 5"); no points, badges or percentages
  that mean nothing.
- Dismissible ("Hide"), and reachable again from the help or account menu.
  When everything is done it shows a one-line done state once, then goes.

## 7. Teach in place, not in a tour

- Every screen a new user reaches says what will be there and the first
  action (`ui-part-empty-states`); this teaches more than any tour.
- A one-line hint beside a control the first time it matters ("Drafts stay
  private until you publish"), dismissible, one at a time, remembered.
- Tours of popovers rarely help: people skip them to get to work and forget
  what they were shown. If one earns a place (a dense editor, a new feature
  in a busy screen): 3 steps at most, started by the user or on the first
  visit to that screen only, Skip on every step and Escape to leave, no
  scrim and no focus trap, each step pointing at a real control with one
  sentence, and remembered as seen on the server. Driver.js and Shepherd.js
  exist if one is needed; check keyboard and screen reader use either way.
- Never a tour on every sign-in, never a modal on page load, never a tour
  on phones.

## 8. Invites and email verification

- Invite teammates after the first result, when there is something to show
  them, never as step one: skippable, by link or by email, with the role
  each gets explained.
- Verification does not block exploring when that is safe: the user starts
  working, and what reaches other people or costs money (sending,
  publishing, inviting, paying) waits for it. A banner says so: "Confirm
  your email: we sent a link to [email]. Resend", with 30 to 60 seconds
  between resends. A code field uses `autocomplete="one-time-code"` and
  `inputmode="numeric"`.
- Products where an unverified account is a risk (payments, health data)
  verify first and say why (`backend-auth`).

## 9. States, phone, accessibility

- A setup error keeps the answers and says what to do; a failed import says
  which rows and why, and imports the rest.
- On a phone: steps full width, Continue full width at the bottom, the
  checklist as a compact card with the next task and "2 of 5", no tours.
- Focus moves to each step's heading; everything works from the keyboard;
  no slides that advance by themselves; nothing moves under reduced motion
  (`motion-comfort`); the checklist is a list whose items say "done" or
  "not done" in text.
- Onboarding sits behind sign-in: `noindex`, no public SEO.

## Check it

- Sign up with a fresh account and count the screens, fields and minutes to
  the first result; cut what is not needed.
- Skip everything: the product still works, and its empty screens teach.
- Close the tab in the middle of setup and sign in from another browser:
  the progress is kept.
- Load the sample data, then remove it: nothing of it remains in reports,
  counts or exports.
- `preview` with `login` at 360, 768 and 1440px on every setup step and on
  the home with the checklist; walk the whole flow by keyboard.

## Avoid

A welcome modal; a carousel of benefits; a survey before any value; tours
of eight steps, or on every sign-in; verification that blocks everything
without a reason; invites as step one; sample data that looks real or will
not go away; a checklist the user ticks by hand; a dashboard of zeroes
after setup; "You're all set!" with confetti instead of the first result;
questions whose answers the product never uses.
