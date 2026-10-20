---
name: eop-race
description: >
  The adversarial Elevation of Privilege (EoP) skill — race the machine to the novel attack.
  Use this skill to run a timed contest where the table and an adversarial agent each generate
  novel exploit hypotheses (Ace-class — the kind with no CVE yet) against a design or repo,
  blind to each other, then reveal and score: the table scores for threats it names before the
  agent surfaces them, the agent scores for what it finds first, and the visible speed gap is
  the lesson. Trigger on "race my design", "race this repo", "beat the machine to the threat",
  "run an EoP race", or "generate novel attacks against this design on a timer". Builds on
  eop-deck; hands accepted attacks to eop-referee.
license: CC-BY-3.0-US (deck content © 2009 Microsoft Corporation)
metadata:
  version: "0.1.0"
  author: Stacey Vetzal
---

# eop-race — beat the machine to the novel attack

This is the skill the gen-AI tempo shift justifies. The threat that matters most now is the **Ace** —
"you've invented a new attack" — the novel, un-cataloged exploit that generative AI can
formulate before the security community can assemble and publish a defense. `eop-race` makes
that tempo argument *visceral*: the table and an adversarial agent both hunt novel attacks
against the same system, on the same clock, blind to each other — and then you see how many
the machine found in seconds that the table missed in minutes.

Builds on **`eop-deck`** for the grounding and the bug-test. Accepted novel attacks hand off
to **`eop-referee`** as backlog (the renderer emits a ready-made `eop-session/1`).

## Running a race — procedure

### 1. Ground the target (via eop-deck)

Ground the design or repo with `eop-deck`'s procedure so both sides attack the *same*,
*named* system — components, data flows, trust boundaries. A shared diagram is the level
playing field. Reuse an existing `eop-grounded-deck/1` if one exists.

### 2. Set the clock and go blind

Pick a window (5 minutes is a good demo). Start it for both sides **at once**. The table
brainstorms novel attacks (especially the six **Aces** — one novel attack per STRIDE suit).
The agent does the same — and **must not reveal anything until the window closes.** Holding
back is the whole contract: an agent that narrates its findings live just hands the table the
answers and destroys the measurement. Generate blind; reveal at the buzzer. Method and the
honesty contract: [`references/race-protocol.md`](references/race-protocol.md).

### 3. Generate genuinely novel hypotheses (the agent's job)

As the adversary, generate Ace-class exploit hypotheses — past the printed 74 cards, the
attack classes with no CVE yet: confused-deputy and non-human-principal spoofing, control-plane
tampering, aggregation/inference disclosure, algorithmic-complexity DoS, and especially the
AI-era **elevation of privilege** (prompt injection into tool use, over-broad agent
permissions, training/context poisoning). Mechanism-level and tied to a named component, or it
doesn't count. The attacker mindset and the per-suit angle vocabulary (shared with
`eop-referee`'s Ace seeds): [`references/adversary.md`](references/adversary.md).

### 4. Reveal, match, and adjudicate with the bug-test

Reveal both lists. Match them: a hypothesis is `human` (table only), `agent` (machine only),
or `both`. Then apply `eop-deck`'s **bug-test** to each — *fast and wrong still loses*, so a
machine hypothesis only scores if it survives the same scrutiny a human one does. The table
argues every one; the argument is the learning.

### 5. Render the scoreboard

Record the round as an `eop-race/1` object (saved under the repo's `.threat-model/` folder —
the suite's shared artifact location, see `eop-deck`'s "Where artifacts go") and render:

```bash
python3 .claude/skills/eop-race/assets/render_scoreboard.py <race.json> [--out <path-without-ext>]
```

With no `--out`, it writes into `.threat-model/` (created if missing); run it from the repo
root. It writes `<out>.md` — the scoreboard, led by the speed-gap headline ("in 5:00 the
table found X; the machine found Y in ~22s, including Z you never saw"), then your wins, the
ties, and the **machine-only misses** (the point). It also writes `<out>.session.json`, an
`eop-session/1` of the accepted attacks, so `eop-referee`'s `render_backlog.py` turns them
into tickets (suppress with `--no-session`). Stdlib only; auto-locates `deck.json`;
warns-not-fails. Schema and scoring: [`references/scoreboard-schema.md`](references/scoreboard-schema.md).

## The deliverable (plan's "done when")

A demo that makes the gen-AI threat-tempo argument visceral: a scoreboard showing real novel
attacks the machine surfaced at machine speed — including ones a capable table missed entirely
— and a backlog of those attacks ready to fix.

## The guardrail

The agent is the adversary and the stopwatch, not the judge. It generates novel candidates
fast; the **table and the bug-test decide what's real**, and the human-only column proves the
humans still find what the machine misses. The race dramatizes *why* threat modeling must run
at this tempo — it doesn't replace the human argument that does the modeling. The argument is
the learning.

## Provenance

Deck content © 2009 Microsoft Corporation, CC BY 3.0 US, via `eop-deck`.
