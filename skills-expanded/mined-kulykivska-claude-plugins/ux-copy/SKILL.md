---
name: ux-copy
description: >-
  Write or fix product microcopy: empty states, errors, loading, success and
  confirmation messages, buttons and labels that replace jargon with plain
  words (for example "average error in places" instead of "MAE"), and dates
  and times in the viewer's local time and a human format. Final text always
  goes through the humanizer skill; never em dashes or emojis. Trigger on
  "write the copy", "microcopy", "error message", "empty state", "rename this
  label", "this text sounds robotic", "UX writing", or when a screen ships
  new user-facing strings.
---

# UX copy

**Product name.** `{{app}}` here and in the references stands for the user's product. Take its name from the project (README title, package.json, app.json, Info.plist) or ask once, then write every example with that name and the product's own screens.

Interface text is part of the interface. It tells people where they are,
what just happened and what to do next, in words they would use themselves.

## Step 1: inventory

List every user-facing string on the screen or flow, including the ones
nobody writes on purpose: button labels, placeholders, validation messages,
toasts, alerts, accessibility labels, notification text, the email that
follows. Mark each with its state: default, empty, loading, error, success,
offline, permission denied, locked (Pro).

A state with no string is a finding: a blank area where the empty state
should be, a spinner with no timeout message.

## Step 2: write by pattern

Patterns and examples for each are in `references/patterns.md`.

- **Empty state**: what will be here, why it is empty, the one action that
  fills it. "No followed drivers yet. Follow a driver to see their chances
  on the home screen. [Choose drivers]"
- **Error**: what happened in plain words, whether their data is safe, what
  to do now. No codes in the headline, no blame, no "Oops". "We could not
  load qualifying. Your picks are saved. [Try again]"
- **Loading**: say what is loading when it takes over a second; after about
  ten seconds say it is taking longer and offer a way out.
- **Success**: confirm the result, not the action. "Alert set for
  qualifying, Saturday 16:00" beats "Success!".
- **Destructive confirmation**: the verb and the object on the button.
  "Delete league" and "Cancel", never "Yes" and "No".
- **Labels**: nouns users know, verbs for actions, sentence case, no
  internal names.

## Step 3: replace jargon

Keep a glossary per product and apply it everywhere. Examples:

| Internal | User-facing | Note |
|----------|-------------|------|
| MAE | Average error in places | "Off by 2.1 places on average" |
| Brier score, calibration | How often our percentages come true | Link to a plain explainer |
| Probability 0.34 | 34% chance | Whole numbers unless the difference matters |
| LORO backtest | Tested on past seasons it had not seen | Methodology page only |
| DNF | Did not finish | Abbreviation is fine for F1 fans in tables, spell it out in sentences |
| Model v3.2 | Updated prediction | Version numbers only in a changelog |
| Entitlement, SKU | Plan | |
| Sync failed | Could not save your changes | Say what the user lost or did not |

Rule: a term that needs a tooltip on a screen for newcomers is the wrong
term for that screen.

## Step 4: dates, times and numbers

- Store and transmit in UTC; **render in the viewer's local time zone**,
  resolved on the device at render time (they may be travelling).
- Human format by distance from now:
  - under an hour: "in 25 minutes", "12 minutes ago"
  - today or tomorrow: "Today, 16:00", "Tomorrow, 07:00"
  - this week: "Sat 16:00"
  - further: "Sun 12 Oct, 15:00"
  - include the year only when it is not the current one.
- Follow the locale's 12 or 24 hour clock and date order; do not hard-code
  "HH:mm".
- For events elsewhere, the user's time comes first; the venue time is
  optional and labelled: "Sun 07:00 (15:00 in Suzuka)".
- Numbers: locale grouping and decimals, units spelled once ("2.1 places").
- Web: `Intl.DateTimeFormat` and `Intl.RelativeTimeFormat` with the
  browser's locale and no fixed `timeZone`. iOS: `Date.formatted(date:time:)`
  and `Text(date, style: .relative)`, which follow the device settings.

## Step 5: voice rules

- Plain, specific, calm. Say "we" for the product, "you" for the user.
- Sentence case for everything, including buttons and titles.
- One idea per sentence; the most important words first (screens are
  scanned, not read).
- **No em dashes and no en dashes** as punctuation: use a comma, a colon,
  parentheses or a full stop. **No emojis.** No exclamation marks except in a
  real celebration, and at most one.
- No confirm-shaming or guilt in any dismiss or cancel label (see the
  forbidden list in `paywall-and-pricing`).
- Localise: strings go through the project's i18n layer; leave room for
  German and Ukrainian text being up to 40% longer.
- Accessibility labels describe purpose, not shape: "Follow Leclerc", not
  "Star button".

## Step 6: humanize, then hand back

Pass the final strings through the **`humanizer`** skill (from the `content`
plugin) before handing them over, then check the result again for em
dashes and emojis, which the humanizer does not add but a later edit might.
If the `content` plugin is not installed, apply its core checks by hand: no
inflated words ("seamless", "unlock", "elevate", "delve"), no rule-of-three
padding, no filler ("simply", "just"), no vague praise.

## Output

A table the developer can paste from: `key | state | before | after | note`,
with keys in the project's i18n naming style. Then the glossary additions,
then **Open questions** (legal wording, translations to commission, strings
that depend on data the screen does not have).
