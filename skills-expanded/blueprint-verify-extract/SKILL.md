---
name: blueprint-verify-extract
description: "Extract every dated event, time and amount from the named documents into .blueprint/facts.json, each with a quotation it was read from — deciding nothing yet."
---

# Extract the dates, times and amounts

`.blueprint/answers.json` names the documents (`documents`, one path per line), what kind they are (`kind`),
the year to use for dates written without one (`year`, may be empty) and what the person is worried about
(`focus`). Read every document in full, starting with `focus`.

This step only reads and copies values out. It does **not** judge whether anything is wrong. That is decided by
machine in the next step, so do not skip an entry because it looks wrong. A wrong weekday or a wrong total is
exactly what must be extracted as written. Change nothing in the repository: the documents stay exactly as
they are. Write only under `.blueprint/`. A person reads the table you write before the machine judges it, so a
missed event is theirs to catch.

## Write `.blueprint/facts.json`

```json
{
  "events": [
    {
      "id": "day1-depart",
      "date": "2026-10-01",
      "weekday": "木",
      "start": "09:00",
      "end": "11:30",
      "title": "東京駅から新大阪駅（のぞみ）",
      "citation": { "source": "itinerary.md", "address": "h2.1", "quote": "10月1日（木）9:00 東京駅発 → 11:30 新大阪駅着" }
    }
  ],
  "amounts": [
    { "id": "hotel", "label": "宿泊費", "value": 24000, "unit": "円", "citation": { "source": "estimate.md", "address": "h2.2", "quote": "宿泊費 24,000円" } }
  ],
  "totals": [
    { "id": "grand-total", "label": "合計", "value": 36000, "unit": "円", "parts": ["hotel", "train"], "citation": { "source": "estimate.md", "address": "h2.2", "quote": "合計 36,000円" } }
  ],
  "products": [
    { "id": "hotel-line", "label": "宿泊費", "value": 24000, "unit": "円", "of": ["hotel-rate", "hotel-nights"], "citation": { "source": "estimate.md", "address": "h2.2", "quote": "宿泊費 12,000円 × 2泊 = 24,000円" } }
  ]
}
```

- **One event per thing that happens at a time**: a departure, a check-in, a meeting. Keep them **in the order
  the document gives them**, because the next step reads that order as the intended sequence.
- `date` is `YYYY-MM-DD`. When the document omits the year, use `year` from the answers. If that is empty too,
  write the date as `MM-DD` (`"10-01"`) and give it no `weekday`: a weekday without a year cannot be checked,
  and the check refuses one.
- `weekday` is copied **as written** (「木」「(木)」「Thu」). Leave it out when the document gives none. Never add
  one the document does not have, and never correct one.
- `start` / `end` are `HH:MM`, 24-hour. Leave out what the document does not say. A range that writes AM/PM once
  covers both times: `1:00–5:00 PM` is 13:00–17:00, `午後1時〜5時` is 13:00–17:00.
- `amounts` are the lines that add up; `totals` are the lines that claim to be their sum (合計, 小計, Total),
  with `parts` naming the amount ids they add up. A subtotal that is itself part of a grand total is both: list it
  as an amount too, under another id, and name that id in the grand total's `parts`.
- `products` are the lines that claim to be a product: a line's amount that is its unit price times its quantity
  (単価 × 数量), a tax that is a subtotal times a rate. `of` names the amount ids multiplied, two or more: the price
  and the quantity (`unit` 台, 泊, 個, pcs — as written), or the subtotal and the rate (`value` 10, `unit` `%`).
  Like a subtotal, a line that is also added into a total is listed as an amount too, under another id. Extract a
  product only where the document gives every factor; a line with no quantity written is not one.
- `value` is a plain number (`24000`, not `"24,000円"`); `unit` is the currency or unit as written (円, USD).
- `id`: lower-case letters, digits and `-`, unique across the whole file.
- `citation.quote` is copied character for character from the document and **must contain every value of its
  entry**: the month and day, the weekday, each time, the amount. A quote may run over a line break (for a
  date in a heading above the times, quote from the heading through the line). `address` uses `chaff tree`'s
  addresses (`sh <base pack>/checks/chaff.sh tree <document>`).

## Done when

`node <usecase pack>/checks/extract.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the pack folders
from your prompt) passes. It fails on a value that is not in its own quotation (a misread), on a quotation
`chaff cite` cannot find in the document, and on a malformed entry. Fix the extraction, not the check.
