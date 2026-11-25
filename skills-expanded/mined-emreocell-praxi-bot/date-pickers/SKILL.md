---
name: date-pickers
description: Enter dates in text inputs and calendar popups, including format and month navigation pitfalls.
version: 0.1.0
when:
  keywords: [calendar, datepicker, check-in, birthday, deadline]
---
# Date pickers

1. Snapshot first. If the field is a text input (placeholder like `DD/MM/YYYY`), fill it with `browser_fill` in exactly the placeholder format, then press Tab.
2. Native date inputs: fill with ISO format `YYYY-MM-DD` regardless of how the browser displays it.
3. Calendar popups: click the field, then read the shown month and year in the snapshot. Use the next/previous buttons until the target month is visible; re-snapshot after each click. Click the day cell (match the day number, ignoring greyed-out days of adjacent months).
4. Year jumps: click the month/year header to switch to a year grid when available.
5. Range pickers: click the start date, then the end date; check both are highlighted.
6. Verify the field value after the popup closes. Ambiguous formats (03/04) must follow the site locale; ask the user if unclear.

Never guess a date the user did not give; use `ask_user`.
