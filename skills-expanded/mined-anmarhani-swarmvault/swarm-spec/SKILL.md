---
name: swarm-spec
description: Requirements phase — a clarifying, options-first stakeholder interview that removes confusion and assumptions (not a relentless grilling) and produces a validated SRS + per-feature specs with EARS acceptance criteria and ISO 25010 NFRs. Use to start a new project's requirements, gather/analyze/specify/validate requirements, stress-test a plan, or mine requirements from an existing codebase (brownfield). Also handles requirement changes after validation.
---

# swarm-spec — requirements phase

Quality here is leverage: every later phase builds on this document. Expect the strongest
available model — if this session runs a lesser tier, say so and let the user decide.

## Pick a planning mode first

Requirements work isn't an interrogation — the goal is to **remove confusion and unstated
assumptions**, not to make the user answer a hundred questions. Before diving in, offer how
much to involve them (recommend **hybrid**; they can switch anytime):

- **ask-each** — put every genuinely uncertain requirement to the user before locking it.
  Maximum control, slowest.
- **recommend-all** — proceed on your recommendations/assumptions for *all* features, record
  each assumption, and surface them together for one batch review. Fastest.
- **hybrid** *(default)* — ask on the high-stakes or truly ambiguous decisions; assume sensible
  defaults on the rest and log them. The user may also scope it ("ask me about auth and
  billing, assume the rest").

Whatever the mode, **every assumption is recorded** (in the question queue, status `ASSUMED`)
so the closing summary can show exactly what you decided for them.

## Clarify, don't grill

Only *decisions* go to the user; *facts* are looked up (codebase, vault, web). For each
decision surfaced: **lead with a recommendation**, state the assumption behind it, list the
alternatives, and accept any free-text answer. If something is only mildly uncertain and the
mode allows, assume the sensible default and note it rather than asking.

**The question queue** — `30 Plans/<P>/question-queue.md` (machine lane) — keeps a long
conversation honest across sessions and compaction:

- Every item gets an ID + status: `OPEN / ASKED / ANSWERED / ASSUMED / PARTIAL / PARKED`.
- An answer that resolves other items: cross-mark them with the answer's ID.
- The user changes topic or adds a requirement mid-stream: APPEND a new branch; the main track
  is never dropped. Return to open items before the phase can complete.
- Re-read the queue on resume — it, not the transcript, is the memory.

Probe the quality dimensions explicitly, even unprompted (offer defaults so this stays light):
performance, security, usability, reliability (ISO 25010: functional suitability, performance
efficiency, compatibility, usability, reliability, security, maintainability, portability). Ask
about interfaces (Web/Mobile/Desktop/TUI/CLI/none), stakeholders, constraints (budget, stack,
compliance), and what is explicitly OUT of scope.

## Brownfield mode (existing code)

Mine first, ask second — the repo is a stakeholder whose answers are already written down.
Reverse-engineer requirements from README/docs/tests/code into specs marked
`status: mined-draft`, each statement carrying provenance (`file:line`). Present for batch
validation; interview only gaps, conflicts, and low-confidence items. Never re-ask what
the sources answer.

## Outputs (human lane, in repo `docs/`, mirrored to vault `30 Plans/`)

- **`docs/SRS.md`** — vision, stakeholders, scope in/out, constraints, FR index with
  MoSCoW priorities, NFRs in EARS notation, traceability scheme, build milestones,
  changelog, glossary.
- **`docs/specs/FR-XX-<slug>.md`** per feature — story, details, acceptance criteria
  (EARS), edge cases, `requires:` dependencies. Template: `90 Templates/spec.md`.

EARS patterns: ubiquitous ("The X shall…"), event ("WHEN … shall…"), state ("WHILE …"),
unwanted ("IF … THEN …"), optional ("WHERE …"). Every FR: unique ID, priority, ≥1
testable criterion, edge cases considered.

## Validation gate (ends the phase)

Don't make the user read the whole SRS to approve it. First present a **review summary** they
can skim in a minute, then point them at the full doc for anything they want to drill into:

- **What we're building** — one plain-language paragraph.
- **Features** — each FR as one line: `FR-07 — resume any project from cold state (Must)`.
- **Key decisions** — the choices that shape the build (stack, interfaces, scope boundaries).
- **Assumptions I made for you** — every `ASSUMED` item, so a wrong guess is easy to catch.
- **Explicitly out of scope** — so silence isn't mistaken for agreement.
- **Open questions** — anything still `OPEN/PARKED`.

Invite a quick "OK" or targeted changes. On approval, flip `status: draft → validated`. Then
ask the **mode question**: gated (user verifies each milestone) or auto (sweeps self-verify, no
stops) — record in flow-state along with `phase: design`.

## Changes after validation (requirements management)

New/changed requirement → tracker entry + SRS changelog + version bump + propagate to
every artifact that mentions it (specs, design, tickets) via FR-ID references. Flag
impacted downstream work; never edit silently.

---
*Influences: Pocock's grilling & to-spec; superpowers brainstorming; Jeffallan's
feature-forge & spec-miner; ISO 25010; EARS; workingsoftware.dev NFR guide — see
CREDITS.md.*
