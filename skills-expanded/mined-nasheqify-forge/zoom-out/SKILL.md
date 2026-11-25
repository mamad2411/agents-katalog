---
name: zoom-out
description: >
  User-triggered: provide a wider context / higher abstraction
  level for an unfamiliar code area. Use when the user is
  unfamiliar with a section, asks "how does X fit into the
  picture", or mentions "zoom out".
status: active
invocation:
  primary: user-facing
  trigger_patterns:
    - "zoom out"
    - "give bigger picture"
    - "how does this fit"
    - "what's the context"
    - "map this area"
disable-model-invocation: true
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: zoom-out

## Purpose

When the user doesn't know a code area / module / topic well,
don't deliver a detail answer first; deliver a **map** of the
relevant modules + callers + domain vocabulary. Detail comes
after the map.

## Source

Matt Pocock's skills at `b843cb5` (MIT License, © 2026 Matt Pocock); Forge's register of adopted methods.

## Standalone

Distinct from:
- `skills/improve_codebase_architecture/SKILL.md` — codebase-wide
  refactor discipline with 3 phases. `zoom_out` is a quick map
  lookup, not a refactor.
- `skills/frame/SKILL.md` — problem analysis with 8 sub-steps.
  `zoom_out` is context lookup, not problem framing.
- `skills/scoping/SKILL.md` — L0-L3 decomposition. `zoom_out`
  is a read-only map, not a decomposition.

What only this skill delivers:
- Quick "how does X fit into the picture" map without process
  discipline.
- User-explicit-only (`disable-model-invocation: true`) — not
  auto-discovered.
- Bridge between user uncertainty and the detail question.

## When to call

- User says "zoom out" / "give me bigger picture" / "how does
  that fit into the picture".
- User asks a detail question about a code area they don't
  know well (symptom: "why is that so?" / "what does that
  actually do?").
- Pre-refactor orientation when
  `improve_codebase_architecture` is too heavy.

### Do not call for

- A detail-coding question with clear scope → answer directly.
- Architecture refactor → `improve_codebase_architecture`.
- Problem analysis with a solution space → `frame`.
- Spec hierarchy decomposition → `scoping`.

## Process

### Output

A map at 3 layers above the detail:

1. **Modules** in the area: what lives here (files / classes /
   functions).
2. **Callers:** who calls what (import graph, one hop).
3. **Domain vocabulary:** which terms (CONTEXT.md if present,
   otherwise derived from code comments + spec refs).

Format: short text + table OR ASCII tree, NOT long prose.

### Vocabulary discipline

Use existing domain vocabulary (CONTEXT.md if present,
otherwise project-specific spec terms). Prevent drift on
"component / service / API" (cross-ref
`improve_codebase_architecture` strict glossary when relevant).

Consumer-specific when relevant: name the project's own
load-bearing architectural primitives (facades, layers, entry
points) so the zoomed view stays grounded in real terms.

### After-map

After the map: address the user question again with the new
context. Detail now rides on map vocabulary.

## Red flags

- Long prose instead of a map (the user wanted a map).
- Introducing your own vocabulary instead of the existing
  domain glossary.
- Map without after-map (the user needs both).
- Map as a full refactor plan (that's
  `improve_codebase_architecture`).

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "User asked a detail question" | The user used the trigger phrase. Map first, then detail. |
| "Map is overhead" | A user-explicit trigger means the user wants the map. Otherwise it would not be invoked. |
| "No CONTEXT.md, so no glossary possible" | Code comments / spec refs / framework principles provide vocabulary. |

## Contract

### INPUT
- **Required:** user trigger (pattern list above) OR user
  detail question on an unfamiliar code area.
- **Required:** read access to the codebase.
- **Optional:** CONTEXT.md with domain glossary.
- **Context:** no cross-refs needed.

### OUTPUT
**DELIVERS:**
- Map: modules + callers + domain vocabulary.
- After-map: detail answer with map context.

**DOES NOT DELIVER:**
- No refactor plan.
- No ADR.
- No spec.
- No code changes.

**ENABLES:**
- The user can now read the detail question with context.
- Pre-refactor orientation.
- Onboarding for a new area.

### DONE
- Map with all 3 layers (modules / callers / vocabulary).
- After-map addresses the original user question.
- Domain vocabulary consistent with the existing project
  glossary (no drift).

### FAIL
- **Retry:** the map is too vague → pull in more concrete
  files / caller paths.
- **Escalate:** the codebase is too large for a map → ask the
  user which sub-area.
- **Abort:** the codebase is not accessible → escalate to the
  user.

## See also

- `skills/improve_codebase_architecture/SKILL.md` — the next
  level (map → friction analysis → refactor candidates).
- `skills/frame/SKILL.md` — when the map shows the problem is
  unclear → frame step 1 reformulate the problem.
