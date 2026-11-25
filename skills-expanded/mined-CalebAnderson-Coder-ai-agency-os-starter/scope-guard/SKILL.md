---
name: scope-guard
description: Check any client request against the contracted scope, flag out-of-scope work, and draft a polite change order with price and timeline. Use whenever a client asks for something new, "quick", "small", "extra", or "while you're at it".
---

# Scope Guard

Stops unpaid scope creep without damaging the client relationship. Drafts only — never sends anything.

## Inputs
- `clients/<slug>/SCOPE.md` — contracted deliverables, monthly quantities, revisions, "Not included" list, hourly rate.
- `clients/<slug>/CHANGES.md` — previous requests this month.
- The client's request (pasted email, Slack message or call note).

If `SCOPE.md` is missing or empty, stop and ask for the SOW. Do not guess the scope.

## Procedure
1. Read `SCOPE.md` and `CHANGES.md`. Count what was already delivered or approved this month.
2. Split the request into individual asks (one client message often hides 2–3 asks).
3. Classify each ask:
   - **IN SCOPE** — cite the exact SCOPE.md row.
   - **OVER QUANTITY** — in scope but above the monthly quantity (e.g. 5th post of 4).
   - **OUT OF SCOPE** — not in SCOPE.md, or listed under "Not included".
   - **UNCLEAR** — write ONE clarifying question; do not quote yet.
4. For over/out-of-scope asks: estimate hours (state assumptions), price = hours × rate from SCOPE.md (round up to the nearest 0.5 h), earliest delivery date that does not push contracted deadlines.
5. Draft the reply in the client's voice (`brand/voice.md` if it exists). Offer two options: paid add-on, or swap for an in-scope item this month.
6. Append one row per ask to `CHANGES.md`: date, request, class, quote, status (`quoted` / `approved` / `declined` / `swapped` / `free-goodwill`).

## Output format
```
## Scope check — <client> — <date>
| Ask | Class | Evidence | Hours | Quote |
|---|---|---|---|---|

### Draft reply (not sent)
<reply>

### CHANGES.md rows added
<rows>
```

## Draft reply pattern
> Happy to help with this. [In-scope part] is already covered and will ship by [date]. [Extra part] is outside our current plan (we have [X] included) — it's about [hours] h, so [price], delivered by [date]. Want me to add it? Or we can swap it for [in-scope item] this month at no extra cost.

## Rules
- Never say "no". Always give a path to yes (paid or swap).
- Never invent a rate — use SCOPE.md. If none is defined, ask.
- Goodwill freebies are allowed but must be logged as `free-goodwill` with hours.

## Monthly
Summarize CHANGES.md: approved extras billed, goodwill hours given, swaps. If goodwill hours > 10% of contracted hours, recommend a scope or price change at renewal.

## Example
See `examples/acme-plumbing/` in the repo: a real SCOPE.md, a client request, and the expected output.
