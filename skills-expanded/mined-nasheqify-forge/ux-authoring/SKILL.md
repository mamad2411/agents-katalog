---
name: ux-authoring
description: >
  Draw out and write the UX of a change a person operates: a look contract (tokens, components) and an experience
  contract (surfaces, states, named-protagonist journeys, voice), with a surface-closure check. Use when the build's
  UX stage fires, or the user asks to design a screen, page, flow or CLI/TUI interaction; NOT for reviewing a UX
  (use spec_board mode=ux) or building the UI (use frontend_ui_engineering).
status: active
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: [spec_authoring, spec_board, frontend_ui_engineering]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: ux-authoring

## Source

BMAD-METHOD (MIT License, © 2025 BMad Code, LLC); Forge's register of adopted methods.

## Purpose

The UX stage of a build (`workflows/runbooks/build/lifecycle.md`) runs this skill. It draws out from the person who
decides about the change (the user, or whoever they name) how it should look and behave for the people who will
operate it, and writes that down as two peer contracts:

- the **look contract**: tokens and components, how it looks;
- the **experience contract**: surfaces, states, journeys, voice, how it behaves.

Both are durable spec carriers (`framework/spec-engineering-implementation-specs.md` §Convention: spec carriers). The
behaviour spec links them and keeps the promised behaviours with their matrix rows. The UX board reviews the
contracts, and `frontend_ui_engineering` builds from them.

The skill elicits; it does not design for the person. Every decision in a contract comes from a source or from the
person's answer. A decision nobody has made yet stays visible as an open slot.

## When to call

- The lifecycle's UX stage fires for the change.
- The user asks to design or rework a screen, page, flow, or a CLI/TUI interaction.

### When not to call

- Reviewing an existing UX → `spec_board` mode=ux.
- Building or refactoring UI code → `frontend_ui_engineering`; tokens of the terminal design system →
  `frontend_design_tty`.
- A documentation site's pages, text or structure → the `docs-rewrite` workflow; a changed string alone → the
  behaviour spec.

## Process

1. **Scope.** Take the surfaces the change adds or changes, and the journeys that reach them. When contracts exist
   for the product, open them and work on that scope. A product without contracts gets contracts for that scope only,
   not for the whole product.
2. **Read before asking.** Read the request, the task's acceptance, the behaviour spec draft, the UI code the change
   touches, and the design system the project names (`frontend_design_tty`, a tokens file, a component library).
   Use the names they use, verbatim. For a surface the change reworks, its current code is a source only for what the
   person confirms keeping: put each value to them as `open: keep <value>?`.
3. **Open the contracts.** When opening the two files, filling a slot or writing the closure table: read and follow
   `skills/ux_authoring/contracts.md` (the files, their slots, the source tag, the closure table). Fill each slot that a
   source settles, with its source tag. Every other slot starts as `open: <question>`.
4. **Elicit.** Ask one open question per message, in this order:
   - the form factor and platform first: the surfaces cannot close before it is settled;
   - then the journeys: the person narrates a real session of a named protagonist (a named person in a situation,
     not "the user"), structured into numbered steps, the step where the need is met (the climax), and the failure
     path;
   - then the surfaces, states, voice, look and the remaining open slots.

   For these slots there are no proposed approaches and no recommended answer. Offer options only when the person
   asks for them or says they cannot answer; the pick is theirs, and the slot records it as their answer. When the
   person hands a decision to Buddy ("you pick"), the slot carries `(delegated: <their words>)` and the decision goes
   on the decisions list (`skills/return_summary/SKILL.md` §Decisions I took for you). A slot nobody settles now
   stays in the experience contract's `## Open` with who answers it and by when; in a run without the person, slots
   stay open.
5. **Close the surfaces.** Fill the closure table (`contracts.md` §Closure):
   - every stated need has a surface that delivers it and the journey step that reaches it;
   - every surface has a journey step that lands there.

   A row without its surface or its journey is a gap. Ask about each gap; do not add a surface, a journey or a step
   the person has not given. A gap closes by the person's answer, or by a ruling to defer it with its reason or owner:
   the person's, or one a spec or task recorded before this run.
6. **Hand on.** Link both contracts from the behaviour spec's header. A behaviour the experience contract promises
   (a state transition, a confirmation, an error path) gets its matrix row in the behaviour spec
   (`skills/testing/SKILL.md` §Test design from the change). Then the board reviews the contracts with the behaviour
   spec (`skills/spec_board/SKILL.md` §Process — mode ux). A brief that builds a covered surface names both
   contracts (`skills/_protocols/mca-brief-template.md` §UX contracts); an open slot it needs is answered before the
   dispatch.

A claim that the surfaces are closed points to the closure table with no open gap row
(`skills/_protocols/evidence-author-claims.md` §8.5, a claim no row names).

## Red Flags

- A colour, layout, component or wording in a contract that no source and no answer gave.
- Journeys written as "the user …" or as a list of features, without a protagonist, a climax or a failure path.
- The surfaces closed while the form factor is open.
- A gap closed by adding a screen or a journey step nobody asked for.
- Rows for surfaces outside the change's scope filled for a small change.
- A mock or wireframe treated as the decision while the contract says otherwise.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know what a good design looks like; I'll propose one." | A proposal the person did not ask for becomes their design by default. Ask; offer options only when asked. |
| "The design system covers the look, so no look contract." | The look contract then names the design system and records only the delta. It stays short, not absent. |
| "The feature list is the journey." | A feature list cannot show where a person stalls or which need is met when. The named session can. |
| "This need obviously belongs on the main screen." | Placing it is the person's decision; until they decide, the closure row stays a gap. |
| "It's a small change, contracts are overkill." | The scope is the surfaces the change touches and the journeys that reach them; for a small change that is a few rows. |

## Contract

### INPUT

- **Required:** the change's request and acceptance; the surfaces it adds or changes.
- **Optional:** existing contracts, the behaviour spec draft, UI code, the project's design system, the person's own
  sketches or mocks.

### OUTPUT

**DELIVERS:**
- `look.md` and `experience.md` per `contracts.md`, every slot filled with its source tag, marked `n/a: <reason>`, or
  `open: <question>`.
- The closure table, with each gap answered or ruled.
- Delegated decisions on the decisions list.

**DOES NOT DELIVER:**
- No rendered mocks or design tool of Forge's own. A sketch or mock the person supplies is linked as a source; the
  contract wins on conflict.
- No UX review → `spec_board` mode=ux.
- No UI code → `frontend_ui_engineering`.

### DONE

- Every slot has a source tag, `n/a`, or an entry in `## Open` with who answers it and by when.
- The closure table has no gap without an answer or a ruling.
- The behaviour spec links both contracts.

### FAIL

- **Retry:** a slot filled without a source → reopen it as `open`.
- **Escalate:** the person's answers contradict the acceptance or another contract → the spec interview or a Council.
- **Abort:** the person declines the UX stage → the route record states it, and the behaviour spec carries the
  surfaces without contracts.

## Standalone justification

`spec_authoring` writes behaviour specs and has no UX slots; the board in mode ux reviews a UX but cannot draw one
out; `frontend_ui_engineering` builds from a design and authors no design system. Drawing out a look and an
experience is its own method with its own artifacts, which those skills consume.
