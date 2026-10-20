---
name: eop-deck
description: >
  Shared foundation for the Elevation of Privilege (EoP) threat-modeling skill suite.
  Use this skill whenever you need the EoP / STRIDE deck data, need to ground a repo or
  design against the 74 STRIDE threat cards, need to draw a trust-boundary / data-flow
  diagram for threat modeling, or need to apply the "would we take a bug for that?"
  adjudication test. Also use when another EoP skill (eop-deal, eop-referee, eop-sentinel,
  eop-race, eop-forge) needs the deck or a grounded deck object. Trigger on mentions of
  STRIDE, Elevation of Privilege, threat cards, trust boundaries, data-flow diagrams for
  security, or "ground these cards against my code."
license: CC-BY-3.0-US (deck content © 2009 Microsoft Corporation)
metadata:
  version: "0.1.0"
  author: Stacey Vetzal
---

# eop-deck — Elevation of Privilege foundation

The dependency for the whole EoP suite. It carries the deck, draws the diagram, grounds
the cards against real systems, and exposes the bug-test. The five gamified skills
(`eop-deal`, `eop-referee`, `eop-sentinel`, `eop-race`, `eop-forge`) all build on what
this skill produces.

## What this skill provides

1. **The deck** — all 74 STRIDE threat cards as structured data in
   [`assets/deck.json`](assets/deck.json). Suit, rank, rank value, threat text,
   open-threat (Ace) flag, and trump flag.
2. **Grounding** — a procedure to turn a repo (or proposed design) into a
   trust-boundary/data-flow diagram and a *grounded deck* mapping each card onto real
   components. See [`references/grounding.md`](references/grounding.md).
3. **The bug-test** — the reusable adjudication judgment ("Would we take an actionable
   bug, feature request, or design change for that?"). See
   [`references/bug-test.md`](references/bug-test.md).
4. **The grounded-deck contract** — the schema every downstream skill consumes. See
   [`references/grounded-deck-schema.md`](references/grounded-deck-schema.md).
5. **The AI & Agent suit (optional extension)** — a co-authored seventh suit for
   AI/agent systems in [`assets/ai-suit.json`](assets/ai-suit.json). Additive and
   opt-in; it does **not** change the canonical 74. See
   [`references/ai-suit-extension.md`](references/ai-suit-extension.md). Authored and
   used by `eop-forge`.

## The deck at a glance

Six suits map to STRIDE; **Elevation of Privilege is the trump suit**. Play starts with
the **3 of Tampering**. Each suit's **Ace is an open-threat card** — the player must name
a novel attack not printed on any card. In the gen-AI reframing, the Ace ("you've invented
a new attack") is the most important card in the deck.

| Suit | STRIDE | Cards | Ranks |
|------|--------|-------|-------|
| Spoofing | S | 13 | 2–10, J, Q, K, A |
| Tampering | T | 12 | 3–10, J, Q, K, A |
| Repudiation | R | 13 | 2–10, J, Q, K, A |
| Information Disclosure | I | 13 | 2–10, J, Q, K, A |
| Denial of Service | D | 13 | 2–10, J, Q, K, A |
| Elevation of Privilege | E (trump) | 10 | 5–10, J, Q, K, A |

74 cards total. Rank values: 2–10 face value, J=11, Q=12, K=13, A=14.

## Using the deck data

Read [`assets/deck.json`](assets/deck.json) directly. It is the single source of truth for
card text — never paraphrase a card from memory; quote it from the asset. Each card:

```json
{ "id": "S-3", "suit": "Spoofing", "stride": "S", "rank": "3", "rank_value": 3,
  "is_trump": false, "is_open_threat": false,
  "threat": "An attacker could try one credential after another and there's nothing to slow them down (online or offline)." }
```

Card `id` is `<STRIDE letter>-<rank>` (e.g. `T-Q`, `E-A`). Downstream artifacts reference
cards by `id` and join back to this file for text.

## Grounding a repo (the core behavior)

When asked to ground a system — "map the deck onto `<repo>`", "draw the threat-model
diagram", or as a prerequisite for another EoP skill:

1. **Survey** the system for entry points, data stores, external dependencies, processes,
   and trust boundaries.
2. **Draw** a Mermaid data-flow diagram with trust boundaries as subgraphs.
3. **Ground** each of the 74 cards onto named components, or flag it **wild** if it can't
   be honestly tied to the system.
4. **Assemble** a grounded-deck object conforming to
   [`references/grounded-deck-schema.md`](references/grounded-deck-schema.md).

Full procedure and examples: [`references/grounding.md`](references/grounding.md).

**Done when** pointing this at a repo yields a diagram plus a grounded deck object that
every other skill can consume.

## Applying the bug-test

When a threat is contested or you need to decide whether a claim counts, apply the
bug-test from [`references/bug-test.md`](references/bug-test.md): restate the threat against
a named component, ask *"would we take an actionable bug, feature, or design change for
that?"*, and record an `accepted`/`rejected` verdict with a one-line rationale.

## Where artifacts go — `.threat-model/` (shared convention)

Every skill in the suite writes its artifacts into a **`.threat-model/` directory at the
root of the target repo** (the system being modeled) — grounded decks, dealt HTML decks and
score cards, session backlogs, race scoreboards, design-threat fragments, and the Sentinel
ledger/board. One predictable home, so artifacts travel with the project via git and the
skills can find each other's output.

- Grounded deck: `.threat-model/eop-<name>.grounded.json`
- Everything else: the bundled renderers default their `--out` into `.threat-model/` and
  create the folder if it's missing. Pass an explicit `--out` only to override.
- Commit what you want to keep (the Sentinel ledger especially, so standings persist).

When grounding, save the grounded-deck JSON there. Downstream skills read it back from the
same place.

## The guardrail (from the whitepaper)

AI removes the blank-page friction and grounds threats in real code — but it does **not**
replace the humans arguing over whether a threat is real. The argument is the learning.
Grounding produces *candidates*; people and the bug-test adjudicate. Keep this skill in
that supporting role: surface concrete, named, testable candidates and let the table decide.

## Provenance

Deck content is the original *Elevation of Privilege* game, © 2009 Microsoft Corporation,
licensed under Creative Commons Attribution 3.0 United States (CC BY 3.0 US). Card text in
`assets/deck.json` is reproduced from `source/` under that license.
