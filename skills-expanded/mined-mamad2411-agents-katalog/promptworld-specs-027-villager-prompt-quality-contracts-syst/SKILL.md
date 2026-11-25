# Contract: Villager System Prompt Frame

**Feature**: 027-villager-prompt-quality | **Date**: 2026-07-23

The villager system prompt is an internal interface between the mind
(`internal/mind`) and every model on the serving chain. This contract pins what
any rewrite must hold; tests in `internal/mind/prompt_test.go` enforce it.

## C1 — Purity / cacheability

`systemPrompt(name, personaText)` is deterministic: identical inputs render
byte-identical output, across calls and across processes. The rendered string is
sent as the single `system` block that carries the `cache_control: ephemeral`
breakpoint (`internal/llm/providers.go` buildParams); therefore the frame contains
NO dynamic world state (no tick, needs, positions, memories — those belong to
`userPrompt`).

**Test**: render twice with same inputs → `==`; render with distinct names →
outputs differ only where the identity statement differs plus persona.

## C2 — Single naming

The frame text (everything except the interpolated `personaText`) contains the
agent's name exactly once. Verified with a collision-proof sentinel name.

**Test**: `strings.Count(frameWithoutPersona, sentinelName) == 1`.

## C3 — Doctrine (meaning-pinned, wording-free)

The frame must instruct, in whatever wording:

1. **Acting-tool-only**: the decision is made by calling exactly ONE acting tool.
2. **Read-then-act**: read-only tools may be called first, then one acting call
   finishes the decision.
3. **Muse-is-an-action**: musing/planning are themselves actions with the
   explicit opportunity-cost framing (a beat spent thinking is a beat not spent
   doing — this exact idea, not necessarily these exact words).
4. **No free-text path**: the frame never invites answering in prose/JSON text;
   no output-format instructions for a text action exist.

**Test**: keyword/meaning assertions (e.g. mentions "exactly one", references the
acting-tool contract, contains no "respond with JSON"-style text path). The
scripted-stub suites in `internal/toolloop` + `internal/mind` remain the deep
behavioral check.

## C4 — Persona block

`personaText` appears verbatim, as its own block between identity and task
framing. Empty persona renders a clean frame: no doubled blank lines, no dangling
separator.

**Test**: render with `personaText=""` → no `\n\n\n` and frame parts still
ordered; render with persona → persona substring present verbatim.

## C5 — Exemplar constraints (only if the exemplar variant ships)

The exemplar is part of the static frame (C1 applies), uses no real villager
name (C2 unaffected — sentinel test still counts 1), shows no literal tool-call
JSON arguments, and does not feature `muse` as its chosen action.

**Test**: static assertions on the frame when the exemplar is present.

## Consumers

- `internal/mind/mind.go` `plan()` — `job.system` for every planner decision.
- All providers on the planner chain (local Ollama tier first) via
  `llm.Request.System`.
- NOT the meeting-phrasing prompt (`meeting.go` builds its own) and NOT Metatron.
