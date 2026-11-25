---
name: eop-forge
description: >
  The design-time Elevation of Privilege (EoP) skill — threat-model a system before the code
  exists, and extend the deck with an AI/agent suit. Use this skill to "threat model this
  design", walk STRIDE against a proposed design, RFC, or architecture sketch and write the
  threats into the design doc before implementation (shift-left), or to "add the AI suit" — a
  co-authored seventh suit covering prompt injection, tool/agent abuse, training-data and
  context poisoning, and over-broad agent permissions (a literal elevation of privilege).
  Trigger on "threat model this design", "shift-left threat modeling", "model this RFC for
  security", "walk STRIDE against our design", "add the AI/agent suit", or "threat model our
  agent/LLM system". Builds on eop-deck; emits an eop-session/1 that eop-referee can turn into
  backlog.
license: CC-BY-3.0-US (deck content © 2009 Microsoft Corporation; AI suit CC BY 4.0, Stacey Vetzal 2026)
metadata:
  version: "0.1.0"
  author: Stacey Vetzal
---

# eop-forge — model the design before the code exists

The cheapest threat to fix is the one you catch before you write a line of code. `eop-forge`
is the EoP suite's **shift-left** surface: it walks the deck against a *proposed* design — a
design doc, an RFC, an architecture diagram, even a verbal sketch — and writes the threats
**into the design** before implementation begins. It also carries the deck forward: a
co-authored **AI & Agent suit** for the systems we're building now, where the trump card —
elevation of privilege — has become literal.

Builds on **`eop-deck`** for grounding, the deck, and the bug-test. Its output is an
**`eop-session/1`**, so the same accepted threats can flow into **`eop-referee`**'s
`render_backlog.py` as tickets — `eop-forge` does not re-implement backlog rendering.

## Two things this skill does

1. **Shift-left threat modeling** — ground a proposed design (no code yet) and walk STRIDE
   (plus, for AI systems, the AI suit) against it, recording threats as design changes folded
   back into the design doc. Procedure: [`references/shift-left.md`](references/shift-left.md).
2. **The AI & Agent suit** — a seventh, optional suit extending the deck for model/agent
   systems. Data lives in `eop-deck` ([`assets/ai-suit.json`](../eop-deck/assets/ai-suit.json));
   rationale and play guidance: [`references/ai-suit.md`](references/ai-suit.md).

## Shift-left — the design ritual

When asked to "threat model this design" / "model this RFC" / "do security on this before we
build it":

### 1. Ground the *design* (via eop-deck, `kind: "design"`)

Use `eop-deck`'s grounding procedure, but against the proposed design instead of a repo. Draw
the **intended** data-flow / trust-boundary diagram from the design and ground each card onto
*planned* components. Produce an `eop-grounded-deck/1` with `target.kind: "design"` (the schema
explicitly supports this). Cards that can't be tied to the planned design are **wild**.

### 2. Decide whether to shuffle in the AI suit

If the design involves a model, retrieval/RAG, tools, or an autonomous agent, include the
**AI & Agent suit** (`eop-deck/assets/ai-suit.json`). If it's a conventional system, the
six STRIDE suits are enough. See [`references/ai-suit.md`](references/ai-suit.md).

### 3. Walk the deck against the design

Suit by suit, for each grounded card ask the **bug-test in design tense**: *"would we change
the design for that?"* Work the **Aces** and the **AI suit** hardest — pre-code is exactly
where novel and AI-era threats are cheapest to design out. Record each accepted threat as an
`eop-session/1` per-threat object whose `artifact` speaks design, not code:

- `candidate_fix` → the **design change** (a boundary moved, a privilege scoped, a control
  added) — not a code patch.
- `candidate_test` → the **acceptance check** the eventual implementation must pass.

The full method, design-tense bug-test, and a worked example:
[`references/shift-left.md`](references/shift-left.md).

### 4. Write the threats back into the design doc

The deliverable is a **Threat model section inside the design doc** — so the threats live with
the design, reviewed before code. Render it:

```bash
python3 .claude/skills/eop-forge/assets/render_design_threats.py <session.json> [--out <path.md>]
```

Save the `eop-session/1` under the repo's `.threat-model/` folder (the suite's shared
artifact location — see `eop-deck`'s "Where artifacts go"). With no `--out`, the renderer
writes the fragment into `.threat-model/` (created if missing); run it from the repo root.
It writes a markdown `## Threat model` fragment (paste/append into the design doc): a headline
**Novel & AI-era** block first (Aces + AI suit — the shift-left payoff), then accepted threats
by suit as *design risk → design change → acceptance check*, and a compact *Considered &
deferred* list for rejected ones. Stdlib only; auto-locates both `deck.json` **and**
`ai-suit.json`; warns-not-fails. The same `<session.json>` also feeds `eop-referee`'s
`render_backlog.py` if you want tickets too.

## The deliverable (plan's "done when")

A forward-looking deck (STRIDE + the AI suit) and a design ritual: pointing this at a proposed
design yields a threat-model section written into the design doc before any code exists, plus an
`eop-session/1` ready to become backlog.

## The guardrail (from the whitepaper)

AI grounds candidate threats against the proposed design and removes the blank-page friction —
but it does **not** replace the humans arguing over whether a threat is real and worth a design
change. The argument is the learning. `eop-forge` surfaces concrete, named, design-tense
candidates; people and the bug-test decide. Keep it in that supporting role.

## Provenance

The base deck is © 2009 Microsoft Corporation, CC BY 3.0 US, via `eop-deck`. The AI & Agent
suit is an original co-authored extension (CC BY 4.0, Stacey Vetzal, 2026), informed by the
OWASP Top 10 for LLM Applications and emerging agentic-system risks. Never paraphrase a card —
quote it from `eop-deck`'s assets.
