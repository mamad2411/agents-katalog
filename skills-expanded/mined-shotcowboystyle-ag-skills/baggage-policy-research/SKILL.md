---
name: baggage-policy-research
description: Research the actual checked, cabin and personal-item baggage allowance for every segment of an itinerary, from each carrier's own published policy, and compute the binding limit that governs the whole journey. Use when the user asks what they are allowed to bring, what their allowance is, whether a bag will be accepted, or after entering an itinerary. Writes allowances.yaml with a source URL, a quote and a confidence level per figure.
allowed-tools: Read, Write, Edit, Bash(python3 *), Bash(mkdir *), Bash(ls *), WebFetch, WebSearch, Grep, Glob
---

# Baggage Policy Research

`$TPA` below is this plugin's `new-workspace` skill directory — the folder holding its `SKILL.md`,
`scripts/`, `schema/`, `typst/` and `template/`. Find it by name in your tool's skills folder (some
tools prefix it, e.g. `travel-packing-assistant__new-workspace`) and set `TPA` once per session.

Produces `allowances.yaml`: what each segment permits, where the number came from, and which
single set of limits the traveller should actually pack to.

## The one rule

**A number without a source is not an allowance.** Every figure written to `allowances.yaml`
carries `source.url`, `source.fetched_on`, and `source.quote` — the sentence it came from. If
you cannot get the sentence, the figure's `confidence` is not `confirmed`, and it must be
visibly flagged everywhere it appears downstream.

This is not pedantry. Baggage allowances are the most-copied, least-maintained numbers on the
web: aggregator sites, travel blogs and old forum posts return confident, well-formatted,
years-out-of-date tables that look exactly like current policy. An allowance sourced from one
of those is indistinguishable from a correct one right up until the check-in desk.

Airline pages are also fare-brand-conditional and route-conditional, so the top-level
"Baggage" page frequently does not describe the user's ticket. Prefer, in order:

1. The **manage-booking / my-trip page for this specific booking**, which states the allowance
   for the actual ticket. If the user can reach it and paste what it says, that beats every
   other source and should be recorded as `confirmed`.
2. The carrier's own baggage page **for the relevant route and fare family**.
3. The carrier's conditions of carriage or fare-rules PDF.
4. Anything else — lead only, never a source.

## Fetch routing

Airline sites are heavily bot-walled and often geo-fenced. Escalate; do not give up:

1. Plain page fetch — the default. Try it first on every URL.
2. If blocked (403, bot wall, empty render), a server-side fetcher on a residential IP. In this
   environment that is `mcp__gateway__geo-egress__fetch_markdown`, with `egress` set to the
   country whose version of the site you need — pricing and allowance pages differ by
   point-of-sale country, and the wrong egress returns a plausible page for the wrong market
   with no error.
3. A real browser (`playwright`, or `claude-in-chrome` when the user is present) for pages that
   render allowances only under JavaScript, or that sit behind the booking login.
4. Ask the user to open the page and paste it. This is a normal outcome for manage-booking
   pages and is the *highest*-quality source, not a failure.

Save the fetched page to `research/<carrier>-<yyyy-mm-dd>.md` before extracting from it. When
the figure is later disputed at an airport, the saved page is the evidence.

## What to determine per segment

### Piece or weight

Two incompatible systems:

- **Piece concept** — an allowance of N bags, each under its own weight cap (commonly 23 kg)
  and a linear-dimension cap (commonly 158 cm). Typical on transatlantic and North/South
  American routes.
- **Weight concept** — a total pooled allowance in kilograms across an unspecified number of
  bags (commonly 20–40 kg), with a per-bag maximum for handling. Common on many routes within
  and out of Asia, the Middle East and Africa.

Which system applies changes the optimisation completely: under a weight concept, splitting
across two bags buys nothing; under a piece concept, it doubles the allowance. Establish this
before doing any arithmetic.

### The numbers

For each segment record: checked pieces and per-piece weight and dimension caps; the hard
maximum weight above which a bag is refused regardless of fee; cabin bag count, weight and
dimensions; personal item; and the excess-baggage prices (prepaid online and at the airport,
extra piece and overweight band) in the carrier's own currency.

The **hard maximum** deserves its own attention. Most carriers refuse a single bag above 32 kg
outright as a manual-handling limit — no excess fee will make it acceptable, and a traveller
who has budgeted for an overweight charge but built a 35 kg bag is repacking on the terminal
floor. Some carriers set that ceiling at 23 kg for economy. Find it; if you cannot, write
`hard_max_weight_kg: 32` with `confidence: assumed` and flag it.

### Enforcement, separately from policy

Published cabin allowances and enforced cabin allowances are different quantities. Record what
is published in the numbers, and what is actually enforced in `cabin.enforced` and `notes`:
whether the carrier weighs cabin bags at the gate, whether the route is one where gate-checking
is routine. This is legitimately soft information — say in the notes that it is, and never let
it move a published figure.

## Computing the binding limit

The traveller packs to **one** set of limits, not five. Compute `binding` as follows:

- **Segments on one ticket, through-checked**: in principle one carrier's rules govern the
  whole journey under the interline baggage rules the industry uses to resolve exactly this
  conflict. In practice application is uneven, and the agent at the first counter often applies
  their own employer's policy. So: compute the tightest per-segment limit across the ticket,
  and use that as `binding`. Record in `binding.rationale` which segment set it and what the
  looser limits were.
- **Separate tickets**: there is no single binding limit — the traveller re-checks and faces
  each carrier's rules in turn. Set `binding` from the tightest, and add a warning naming the
  airport where bags must be collected and re-checked.
- Cabin and personal item are almost always enforced by the operating carrier of the segment
  being boarded, so take the tightest cabin figure across all segments regardless of ticketing.

Packing to the tightest limit costs a little capacity and removes an entire category of
airport failure. When the difference is large enough to matter — say the tightest segment
allows 20 kg and the rest allow 32 — surface it explicitly and let the user decide whether to
carry the risk, rather than deciding for them.

## Procedure

1. Read `itinerary.yaml`. Group segments by (marketing carrier, fare brand, cabin, route type)
   — one research pass per distinct group, not per segment.
2. For each group, fetch and read the carrier's policy by the routing above. Save the page.
3. Write the segment entries with source, quote and confidence.
4. Compute and write `binding`.
5. Validate: `python3 $TPA/scripts/validate.py . --json`. Fix anything it
   flags; `UNVERIFIED_ALLOWANCE` warnings are expected and are the list you report.
6. Report as a table: per segment, checked / cabin / personal, and a confidence column. Then
   state the binding limit in one sentence, and list every figure that is not `confirmed` with
   the specific thing the user would have to do to confirm it.

Do not proceed to `/travel-packing-assistant:plan` while the checked allowance for any segment is
`assumed`. Say so and say what is needed.
