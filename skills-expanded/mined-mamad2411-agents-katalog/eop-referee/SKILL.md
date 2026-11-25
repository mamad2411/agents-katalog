---
name: eop-referee
description: >
  The adjudicator and riff engine for a live Elevation of Privilege (EoP) threat-modeling
  session. Use this skill during play to rule on a contested threat with the bug-test ("rule
  on this threat: …"), to unstick a player frozen on an Ace by seeding three novel-attack
  starting points, to run the 60-second riff variant, or to convert accepted threats into
  backlog — ticket titles, repro sketches, candidate fixes and tests. Trigger on "rule on
  this threat", "is this a real threat?", "we're stuck on the Ace", "riff on this", "turn
  these threats into tickets", or "referee our EoP game". Builds on eop-deck and pairs with
  eop-deal.
license: CC-BY-3.0-US (deck content © 2009 Microsoft Corporation)
metadata:
  version: "0.1.0"
  author: Stacey Vetzal
---

# eop-referee — adjudicator & riff engine

The teacher/judge at the table. `eop-deal` sets up the game; `eop-referee` keeps it moving
at the two hard moments — when a threat starts an argument, and when a player draws an Ace
and freezes — and turns everything accepted into **backlog**. The deliverable is play that
produces tickets, with no stalls.

Builds on **`eop-deck`** (the bug-test, the deck, the grounded deck). Consumes the
grounded-deck object that `eop-deck` / `eop-deal` produce, joining on `card_id` for card
text and component context.

## Four jobs

### 1. Adjudicate contested threats — fast

When asked to rule on a threat, apply the bug-test from `eop-deck`'s
`references/bug-test.md`:

1. Restate the claim in one sentence, grounded in a **named component**.
2. Ask: *"Would we take an actionable bug, feature request, or design change for that?"*
3. Give a **one-line rationale** and a verdict: `accepted` or `rejected`.
4. Record it and move on — aim for under a minute. The argument is the learning; the
   verdict just ends it so play continues.

Record verdicts in the per-threat shape from `references/artifacts.md`.

### 2. Seed the Aces — un-freeze the novel attack

When a player is stuck on an Ace (open threat), give them **three concrete, system-specific
starting points** for a novel attack in that suit — framed as prompts, not answers. Method
and per-suit seed angles (including the AI-era classes the 6th suit will formalize) are in
[`references/ace-seeds.md`](references/ace-seeds.md). Novel attacks are the session
headline; surface them first in the backlog.

### 3. Run the 60-second riff

After a threat is accepted, open a 60-second window for related threats. Prime the pump if
the table stalls, adjudicate each riff in one line, time-box hard at 60s, and capture each
accepted riff as its own small artifact linked via `riff_of`. Procedure and prompt patterns:
[`references/riff.md`](references/riff.md).

### 4. Convert threats into artifacts

Every accepted threat becomes a four-field artifact: **ticket_title**, **repro_sketch**,
**candidate_fix**, **candidate_test**. Short and actionable — momentum over a finished spec.
Schema and the `eop-session/1` container: [`references/artifacts.md`](references/artifacts.md).

## Producing the backlog

Collect the session's threats (accepted and rejected, with artifacts and riffs) into an
`eop-session/1` JSON object saved under the repo's `.threat-model/` folder (the suite's
shared artifact location — see `eop-deck`'s "Where artifacts go"), then render:

```bash
python3 .claude/skills/eop-referee/assets/render_backlog.py <session.json> [--out <path.md>]
```

With no `--out`, it writes the backlog into `.threat-model/` (created if missing); run it
from the repo root. It joins against `eop-deck`'s `assets/deck.json` (auto-located) and
writes a markdown backlog: **Novel attacks (Aces)** first, then accepted threats grouped by
STRIDE suit as tickets with repro / fix / test, riffs nested under their parent, and rejected
threats listed compactly with rationale so the reasoning isn't lost. Dependency-free (stdlib
only).

## The deliverable (plan's "done when")

Play that produces backlog, with no stalls at the hard moments — contested threats get a
fast bug-test ruling, frozen Aces get three seeds, and accepted threats leave the table as
tickets a team can pick up.

## The guardrail

The referee rules and seeds and converts — it does **not** replace the table's argument
over whether a threat is real. Seeds are prompts the players develop; verdicts end
arguments rather than pre-empt them. Keep the human judgment central.

## Provenance

Deck content © 2009 Microsoft Corporation, CC BY 3.0 US, via `eop-deck`.
