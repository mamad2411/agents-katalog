---
name: itinerary-intake
description: Capture a multi-segment international itinerary into itinerary.yaml — flights, dates, marketing and operating carriers, ticket grouping, cabin and fare brand. Use when the user gives their flights, pastes a booking confirmation, or asks to start planning packing for a trip. Everything downstream (allowances, the pack, the excess-baggage costs) depends on getting the ticket grouping and fare brand right here.
allowed-tools: Read, Write, Edit, Bash(python3 *), Bash(ls *), Grep, Glob
---

# Itinerary Intake

`$TPA` below is this plugin's `new-workspace` skill directory — the folder holding its `SKILL.md`,
`scripts/`, `schema/`, `typst/` and `template/`. Find it by name in your tool's skills folder (some
tools prefix it, e.g. `travel-packing-assistant__new-workspace`) and set `TPA` once per session.

Turns whatever the user has — a pasted confirmation email, a screenshot, a sentence — into
`itinerary.yaml`. Runs inside a trip workspace.

## Take the document, don't interrogate

If the user has a booking confirmation, ask for it before asking anything else. An e-ticket
receipt carries the fare basis, the operating carrier and the ticket number, which are exactly
the fields a person cannot recall and exactly the fields that decide the allowance.

Accept it in any of these forms and read it directly rather than making the user retype:

- A pasted email body or an `.eml` file in the workspace.
- A PDF e-ticket — open it directly (models with vision read PDFs and images).
- A screenshot — open it directly (models with vision read PDFs and images).
- A confirmation in the user's mailbox — if a Gmail/Workspace MCP is available, search for the
  booking reference or the airline name around the booking date.

## The four fields that actually matter

Everything else in `itinerary.yaml` is context. These four change the answer:

1. **Ticket grouping.** Which segments were issued on one ticket. Bags are through-checked
   across segments on a single ticket; on separate tickets the traveller collects, re-checks,
   and pays a **second** carrier's allowance from scratch. Two flights bought in one
   transaction on one website are not necessarily one ticket — check for one booking reference
   and one ticket number, or ask.

2. **Fare brand.** "Economy" is not an allowance. Light/Basic/Saver fares routinely include no
   checked bag at all, including on long-haul, and sometimes no cabin bag beyond a personal
   item. If the user does not know their fare brand, that is the first thing to look up on the
   airline's "manage booking" page — do not proceed on the assumption of a standard economy
   allowance.

3. **Marketing vs operating carrier.** On a codeshare the ticket says one airline and a
   different one flies it. Record both. The allowance usually follows the ticket; the person
   with the sizer at the gate works for the operator.

4. **Status and cards.** Frequent-flyer tier, alliance status and some co-branded credit cards
   add pieces or kilograms, sometimes a lot. Ask once: "any frequent flyer status or airline
   credit card on this booking?" — and record which traveller holds it, because on many
   carriers the benefit extends to companions on the same booking and on others it does not.

## Procedure

1. Read `itinerary.yaml` — if it already has segments, ask whether to amend or replace.
2. Ingest whatever document the user provides. Extract segments in order.
3. Fill `segments[]` per `docs/data-model.md`. Use IATA codes for airports and carriers; if the
   user gives a city, resolve to the specific airport — allowance research is route-dependent
   and "London" is five airports.
4. Fill `tickets[]`. If ticket grouping is genuinely unknown after reading the document, write
   what you know, set the ticket's `booking_ref` to the reference you have, and record an
   explicit note in the file that grouping is unconfirmed. Do not guess it silently — an
   itinerary wrongly recorded as one ticket produces an allowance that is wrong by a whole bag.
5. Ask about status/cards. One question, once.
6. Write the file. Validate:
   ```bash
   python3 $TPA/scripts/validate.py . --json
   ```
7. Summarise back as a table — date, flight, route, cabin, fare brand, ticket — and name the
   next step: `/travel-packing-assistant:policies`.

## Return journeys

A return trip is one workspace, both directions, with `trip.direction: round-trip`. Keep the
return segments in the same file: the return allowance is frequently different (different fare
brand, different aircraft, sometimes a different carrier), and the whole point of the plan is
that a bag that flew out legally also flies home legally. Where the outbound and return limits
differ, the **return** limit is usually the binding one, because the trip has added weight.
