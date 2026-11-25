---
name: ui-part-dates
description: "Dates and times in interfaces: showing them in the reader's locale and time zone, relative times, date and time inputs, calendars and range pickers with presets, disabled dates with reasons, time zones, durations, and the libraries to use. Read before showing or asking for a date or a time."
---

# Dates and times

The naive version prints `03/04/26` (March or April?), shows the server's
time zone to everyone, stores a birthday as midnight UTC so it appears a day
early in America, says "2 hours ago" with no way to see when, and asks for a
date of birth with a calendar that opens on this month. This skill shows
dates so nobody misreads them, stores them so they do not shift, and asks
for each kind of date the way it is best entered. Words and plurals are in
`i18n`, the API's date format in `backend-api`.

## 1. Showing a date

- Format with `Intl.DateTimeFormat` in the reader's locale (the app's
  language, else the browser's) and time zone (their profile's, else
  `Intl.DateTimeFormat().resolvedOptions().timeZone`).
- The month as a word: "12 Mar 2026" or "Mar 12, 2026", as the locale
  writes it (`dateStyle: "medium"`). Never an all-number date where people
  from more than one country read it; ISO `2026-03-12` only in technical
  places (logs, exports, file names).
- The year when it is not the current one; the weekday when people plan
  with it ("Thu 12 Mar"); the time in the locale's own clock, 12 or 24
  hours, never forced.
- In tables: right-aligned, tabular numbers, never wrapped
  (`ui-part-tables`). Build formatters once and reuse them.

```ts
const day = new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeZone: zone });
const at = new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short", timeZone: zone });
const plan = new Intl.DateTimeFormat(locale, {
  weekday: "short", day: "numeric", month: "short", timeZone: zone,
});
day.format(new Date("2026-03-12T09:30:00Z")); // en-GB "12 Mar 2026", en-US "Mar 12, 2026"
```

- `dateStyle` and `timeStyle` cannot be mixed with fields like `weekday`
  (the constructor throws); list the fields instead, as in `plan`.
- Server rendering: a date formatted in the server's zone and again in the
  reader's does not match, and React reports a hydration error. Format on
  the server in the user's saved zone, or send the ISO value in a `time`
  element and format it in the browser.

## 2. Relative times

- For recent events in feeds, comments and activity: "now" under a minute,
  then "5 minutes ago", "3 hours ago", "yesterday", and the date from about
  a week on.
- The exact time one step away: a `time` element with the ISO value, and
  the full date on hover and focus (`ui-part-tooltips`) or in the detail
  view. A `title` alone never reaches touch or keyboard users.
- One shared timer updates every relative time every 30 to 60 seconds, not
  a timer per row, and it pauses while the tab is hidden.
- Absolute, not relative, in anything kept or compared: emails, exports,
  audit logs, invoices, print, and deadlines ("Due Fri 3 Oct, 17:00", with
  "in 2 days" beside it when that helps).

```ts
const rtf = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
const units: [Intl.RelativeTimeFormatUnit, number][] = [
  ["day", 86400], ["hour", 3600], ["minute", 60],
];
export function ago(date: Date, now = Date.now()): string {
  const s = Math.round((date.getTime() - now) / 1000);
  for (const [unit, size] of units) {
    if (Math.abs(s) >= size) return rtf.format(Math.round(s / size), unit);
  }
  return rtf.format(0, "second"); // "now"
}
// <time datetime="2026-09-29T08:15:00Z">{ago(date)}</time>
```

## 3. Storing dates, and time zones

- An instant (when something happened) is stored in UTC (`timestamptz` in
  Postgres) and sent as ISO 8601 with its offset: `2026-09-29T08:15:00Z`.
- A calendar date with no time (a birthday, a due date, a holiday) is a
  plain date, `"2026-03-12"`, never midnight UTC: `new Date("2026-03-12")`
  is UTC midnight and shows as 11 March west of Greenwich. Keep it a string
  or a `Temporal.PlainDate`; if it must pass through a `Date`, format it
  with `timeZone: "UTC"`.
- A future local event (a meeting at 09:00 in Jakarta next year, a weekly
  class) is stored as the local date and time plus the IANA zone
  (`Asia/Jakarta`): daylight saving rules change, so the instant is worked
  out when needed.
- Show the zone whenever people in different places read the time:
  bookings, meetings, deadlines, live events. "14:00 WIB" or "14:00 Jakarta
  time", with the reader's own time beside it when theirs differs. A zone
  picker lists cities with their offset, searchable, the detected one first.
- Arithmetic in the zone, not in milliseconds: "tomorrow" or "in a month"
  across a daylight saving change is not a multiple of 86,400 seconds away.

## 4. Libraries

- Display: `Intl` alone (`DateTimeFormat`, `RelativeTimeFormat`, and
  `DurationFormat` where the runtime has it). No library needed.
- Calculation and zones: Temporal where the runtime ships it (check
  `typeof Temporal`; `temporal-polyfill` or `@js-temporal/polyfill`
  otherwise); in existing code date-fns with `@date-fns/tz`, Day.js with
  its `utc` and `timezone` plugins, or Luxon. Not Moment.js in new code (in
  maintenance, heavy), and no hand-written date maths.
- Parsing: only ISO 8601 from machines. What people type is parsed with an
  explicit format and locale (date-fns `parse(value, "dd/MM/yyyy", new
  Date())`), or not typed as free text at all (section 5). Never
  `new Date("03/04/2026")`.

## 5. Asking for a date or a time

| Need | Use |
|---|---|
| One near date (a delivery day, a filter) | `input type="date"`, or the design system's date picker |
| A date people know (birth, passport expiry) | Day, month and year as three text fields with `inputmode="numeric"`; no calendar |
| A time | `input type="time"` with `step` (900 for 15 minutes), or slot buttons when only some times are free |
| Ranges, unavailable dates, presets | A library picker: react-day-picker (shadcn/ui's Calendar), React Aria `DatePicker` and `DateRangePicker`, Bits UI (Svelte), Reka UI or PrimeVue (Vue), Ark UI, Mantine Dates, MUI X |
| Date and time together | Two fields and the zone named; `datetime-local` carries no zone |

- Native inputs work well on phones and with the keyboard, and their value
  is always `yyyy-mm-dd`. But the display follows the browser, not the
  page, `min` and `max` are the only limits, and there are no ranges.
- A custom picker lets people type as well as pick: segmented fields (React
  Aria's `DateField`) or a text field with the format shown ("DD/MM/YYYY"),
  and a calendar button beside it. The calendar helps; it is not the only
  way in.
- The label names the date ("Delivery date"), the hint gives an example
  when typing ("For example, 27 3 2026"), and errors say what is wrong
  ("Choose a date after today").

## 6. The calendar grid

- Keys, from the APG date picker dialog: arrows move a day (left, right) or
  a week (up, down); Home and End go to the start and end of the week;
  Page Up and Page Down change the month, with Shift the year; Enter or
  Space selects; Escape closes and returns focus to the field or button.
- One tab stop in the grid (roving `tabindex`); each day named in full
  ("Thursday, 12 March 2026"); today marked in words as well as with a
  ring; the selected day `aria-selected="true"`; the month and year as the
  grid's label, and a change of month announced politely.
- The week starts on the locale's day (Monday in most of the world, Sunday
  in the United States and some others); the libraries take it from the
  locale.
- Day cells 40 to 44px (44 on touch); one month about 300 to 340px wide;
  two months side by side for ranges on wide screens, one on phones, where
  the calendar opens in a bottom sheet or full screen; the popup kept
  inside the window by the library's positioning.
- Today and the selection from tokens at 3:1 in both themes (`ui-themes`);
  the popup fades in over 120 to 160ms and months switch at once
  (`motion-interface`, section 2).

## 7. Ranges and presets

- Presets beside the calendar (a list above it on phones): Today,
  Yesterday, Last 7 days, Last 30 days, This month, Last month, This year,
  Custom. Say whether "Last 7 days" includes today, and hold that rule
  everywhere, the query included.
- The trigger shows the range in words ("1 to 28 Sep 2026", "Last 30
  days"); the URL carries plain dates (`?from=2026-09-01&to=2026-09-28`).
- After the first click, hovering previews the range; a click before the
  start restarts it; minimum and maximum lengths are said in the hint.
- Both ends inclusive, and the data queried by the same rule in the
  reader's zone.

## 8. Dates that cannot be chosen

- Say why: a legend (booked, closed, too soon to deliver) and the reason in
  the day's accessible description, as well as the muted style. A greyed
  day with no reason leaves people guessing.
- Offer the way out: "Next available: Tue 14 Oct" as a button, and open on
  the first month with free dates, not on a month of greyed days.
- Times as slot buttons (44px, grouped as Morning, Afternoon, Evening),
  only the free ones, in the place's zone with the zone named.
- The server checks the choice again when booking; if the slot has gone,
  the message offers the nearest free ones.

## 9. Durations and countdowns

- Durations in units people read ("1 h 30 min", "3 days"), with
  `Intl.DurationFormat` where available or `Intl.NumberFormat` with
  `style: "unit"` per part; stored as seconds or ISO 8601 (`PT1H30M`).
- Running timers in tabular numbers (`font-variant-numeric: tabular-nums`)
  so the digits do not jitter.
- Countdowns only to a real deadline (a sale that really ends, a session
  about to time out), from the server's clock, never reset on reload to
  fake urgency; announced at thresholds (5 minutes, 1 minute), not every
  second; a session timeout offers more time (WCAG 2.2.1).

## Check it

- Run the tests and the app in another locale and zone: `TZ=America/Los_Angeles`
  for Node, `locale` and `timezoneId` on a Playwright context, the Sensors
  panel in Chrome DevTools for the browser.
- A birthday shows the same day at UTC-8 and at UTC+9; a weekly 09:00
  event stays at 09:00 across a daylight saving change.
- The picker by keyboard alone: arrows, Page Up, typing a date, Escape
  back to the field.
- `preview` at 360px: the popup fits, day cells are 44px, presets reachable.

## Avoid

All-number dates like 03/04/26; the server's zone shown to everyone; plain
dates stored as midnight UTC; relative times with no exact time reachable;
"0 seconds ago"; a timer per row; a calendar as the only way to enter a
birth date; greyed days with no reason; date maths in milliseconds across
daylight saving; Moment.js in new code; `new Date()` on whatever was typed;
countdowns that reset on reload.
