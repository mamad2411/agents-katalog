---
name: implement-refactor
version: 1
description: >-
  This skill should be used when the user wants to execute one resumable unit of a Clean Architecture refactor plan. Triggers: "apply the clean plan", "continue the migration", "do the next slice/layer", "execute the refactor", "run the next resumable unit", `/implement-refactor`. Refactor-only — behaviour-preserving; writes characterization tests first when no green baseline exists. One unit per invocation, one atomic commit per unit.
---

# Implement-refactor

Execute exactly **one resumable unit** of a Clean Architecture refactor plan. Output is real, behaviour-preserving production code plus an implementation report. The plan lives under `.plans/clean/` (Feature-Driven flavour, FDD) or `.plans/clean-bob/` (Uncle-Bob layer-first flavour). The skill leaves the working tree on a clean atomic commit per unit and never amends. This skill is **self-contained** — it reads the audit-plan files directly and does not invoke any other skill.

## Inputs and outputs

- **Source plan:** `.plans/clean/<feature>/progress.md` (Feature-Driven flavour) or `.plans/clean-bob/<layer>/progress.md` (Uncle-Bob layer-first flavour). Each unchecked `- [ ]` is a candidate unit.
- **Code output:** edits to project source — moves, extractions, dependency inversions; never new product behaviour.
- **Report output:** `.plans/<root>/<feature_or_layer>/implementations/<NNN>.md` where `<root>` is `clean` or `clean-bob` and `<NNN>` is a zero-padded serial picked at write time (`001.md`, `002.md`, …).
- **State updates:** `STATE.md`, `progress.md`, `CONTEXT.md` (also read during the loop for vocabulary lookup), and `docs/adr/NNNN-*.md` when a load-bearing decision is reached.

## Core rules

1. **Behaviour preservation is the contract.** Refactors must not change observable behaviour. If existing tests don't cover the touched code, write **characterization tests** first (capture current behaviour, including bugs), commit them separately, then refactor.
2. **One resumable unit per invocation.** Stop after a single unit; ask the user to re-invoke for the next one. Do not chain.
3. **Honour the audit's vocabulary.** Use the slice / layer / port / gateway / adapter / entity terms defined in the source plan and `CONTEXT.md`. Do not invent synonyms ("service," "module," "boundary").
4. **Honour ADRs.** `docs/adr/NNNN-*.md` is load-bearing. If a unit contradicts an existing ADR, hard-stop and surface the conflict — let the user reopen it before proceeding.
5. **Atomic commits.** One commit per unit, scoped to files that satisfy that unit (plus the state files updated in this loop). Never `git add -A`. Never amend or `--no-verify` without explicit user authorization (see What NOT to do).
6. **No new behaviour.** This skill does not add features, fix bugs, or change public APIs. If a unit cannot be completed without a behaviour change, hard-stop and tell the user to handle that work through their normal feature-implementation flow — not this refactor loop.

## Layers and vocabulary

Both audit-plan flavours share four concentric layers and the same dependency rule. This section is the refactor skill's self-contained reference — you do not need to read the audit skills to understand what each layer means.

### The Dependency Rule

Source code dependencies point **inward only**. An outer layer may import inner ones; an inner layer must never name an outer one. Every action in this skill preserves this rule. If a move would create an inward-pointing import, invert the dependency through a port first (Action 3).

### Four layers, two vocabularies

| Position | FDD term | Bob term | What lives here | What never lives here |
|---|---|---|---|---|
| Innermost | Domain | Entities | Entity types, value types, factory functions, pure domain functions, domain error types | Framework imports, third-party imports, I/O, implicit time/randomness/env |
| 2nd | Use-case | Use Cases | Orchestration functions (one per user action), port definitions, input/output types, use-case error types | Framework imports, third-party imports, direct I/O, concrete adapter references |
| 3rd | Adapters | Interface Adapters | Port implementations. Third-party libs live here. Translation between clean types and external formats. (Bob also places controllers and presenters here; FDD keeps them in Delivery) | Business decisions, entity type definitions |
| Outermost | Delivery | Frameworks & Drivers | Controllers, presenters (FDD). HTTP handlers, UI components, DB client construction, middleware, composition root (both). (Bob's controllers/presenters are in the 3rd layer) | Business logic, entity type definitions |

### Folder mapping

```
FDD:                                  Bob:
src/features/<name>/                   src/
  domain/                                entities/<concept>/
  use-cases/                             use_cases/<concept>/
    ports.<ext>                            ports.<ext>
  adapters/                              interface_adapters/
    (port implementations)                 gateways/   (port implementations)
  controllers/                             controllers/
  presenters/                              presenters/
  wire.<ext> (composition root)          frameworks_and_drivers/
src/shared/                                 main.<ext>  (composition root)
  domain/  (Result, Money, etc.)
  ports/   (Clock, Logger)
```

### Composition root

Both flavours have exactly one composition root — the single place where every concrete dependency is constructed and wired. Use cases never reach it through a service locator; adapters are passed in.

- **FDD:** `features/<name>/wire.<ext>` (one per slice) + application entry point imports each.
- **Bob:** `frameworks_and_drivers/main.<ext>` (one per project).

### OOP / FP discipline

The source plan specifies the paradigm. Do not re-litigate here.

- **FP-leaning languages (JS/TS, Python, Go, Rust, Elixir):** favour functions + closures + records. Classes outside the outermost two layers are flagged by the audit for replacement. When the plan says "replace class with factory function," use Action 5.
- **OOP-native languages (Java, Kotlin, C#, Swift, Ruby, PHP):** idiomatic classes throughout. Final/sealed classes for entities, interfaces for ports, concrete classes for adapters. Framework annotations (`@Service`, `@Component`, `@Repository`, `@RestController`) belong only in the outermost two layers — never in domain/entities or use-cases.

## Mandatory preconditions

Run **before** writing any code, in this order:

1. **Detect the audit-plan flavour.** Glob `.plans/clean/STATE.md` and `.plans/clean-bob/STATE.md`. Bind `<root>` to whichever exists. **Hard-stops:**
   - Neither exists → tell the user no audit plan was found at either path and stop. The user must produce one before this skill can run.
   - Both exist → AskUserQuestion which plan to drive from. Do not silently pick.
2. **Read STATE.md.** Identify project type, language(s), pending features (FDD flavour) or layers (Bob flavour), and the decisions log. If STATE flags an in-progress unit from a prior session, surface it and offer to resume that unit before picking a new one — see [RESUMING.md](RESUMING.md).
3. **Pick the feature/layer.** Read every `<root>/<feature_or_layer>/progress.md`. List each with its count of unchecked (`- [ ]`) units. AskUserQuestion which to drive. If the user named one in the prompt, use it. Hard-stop if none has unchecked units — tell the user the plan is fully migrated.
4. **Pick the unit.** List the unchecked units of the chosen feature/layer in plan order. AskUserQuestion which one (default: the first unchecked). The unit's text is the migration **Action** verbatim — full action catalogue and safe-move recipes in [ACTIONS.md](ACTIONS.md).
5. **Verify the working tree is clean.** Run `git status --short`. If anything is staged, modified, or relevantly untracked, surface the diff and **hard-stop** — do not absorb unrelated work into the refactor commit.
6. **Establish the green baseline.** Identify the smallest existing automated check that covers the files this unit touches (unit, integration, contract, or end-to-end). Run it; record that it passes. If none exists or none passes, **switch to characterization-test mode**: write the smallest test that pins current behaviour, commit it as `test: <feature_or_layer> characterize <subject>` (separate commit, before the refactor), then continue.

Only proceed to the refactor loop after 1–6 are clean.

## Refactor loop

For the chosen unit:

1. **Re-confirm the tree is clean** before staging — formatters / generated files / hooks can dirty it between steps.
2. **Apply the migration action.** Recipes per action kind in [ACTIONS.md](ACTIONS.md). Keep the diff minimal — moves and renames only; do not opportunistically reformat or inline-clean unrelated code.
3. **Honour the layer discipline.** Follow the OOP/FP paradigm and layer rules from the Layers section above. Match what the source plan specifies; do not re-litigate.
4. **Re-run the green baseline from precondition 6.** It must still pass. If it fails, the refactor changed behaviour — revert, narrow the unit, and try again. Do not "fix forward" by editing tests.
5. **Tick the unit in `progress.md`** from `- [ ]` to `- [x]`. Use `[~] — <reason>` only when the unit was deliberately skipped (e.g. superseded by an ADR change); never use `[~]` to hide a failure.
6. **Update `STATE.md`** — clear the in-progress flag and append to the decisions log if a non-trivial choice was made.
7. **Update `CONTEXT.md`** if a new domain term surfaced. Open `docs/adr/NNNN-*.md` only when this unit cemented a load-bearing decision (rare per-unit; common per-feature/layer).
8. **Commit atomically.** Stage only the files this unit touched plus `progress.md` / `STATE.md` / `CONTEXT.md` / any new ADR file. Message format: `refactor(<root>) <feature_or_layer>: <verb-led summary>`. Example: `refactor(clean) billing: extract Invoice entity from BillingService`. Include the unit's text verbatim in the commit body.
9. **Never amend.** If a hook fails, fix the underlying issue and create a **new** commit. Do not `--no-verify` without explicit user authorization.

When the unit is committed, write the implementation report and stop. Do not push, do not start the next unit.

## Implementation report

Write to `.plans/<root>/<feature_or_layer>/implementations/<NNN>.md`. Pick `<NNN>` as the next zero-padded serial in that directory (`001.md`, `002.md`, …). Include:

- **Unit** — the action text verbatim and its position in `progress.md`.
- **Commit SHA(s)** — refactor commit. If a characterization-test commit was made first, list both, in order.
- **Files touched** — moves, renames, edits.
- **Behaviour-preservation evidence** — which test ran for the green baseline, before/after both green, and any new characterization tests written.
- **Decisions** — vocabulary additions, ADR conflicts surfaced or resolved, deviations from the planned action.
- **Open follow-ups** — anything that should become a new unit on the parent `progress.md`. Always include this section; if nothing surfaced, write "None.".

## What NOT to do

- **Don't run more than one unit per invocation.** If asked to "do the next two units," do only the lowest-ordered one and hard-stop.
- **Don't add features or fix bugs.** Behaviour preservation is the contract. Surface bug discoveries to the user; let them go through their normal feature-implementation flow.
- **Don't edit existing tests to make them pass after a refactor.** If a green test goes red, the refactor changed behaviour — revert.
- **Don't invoke any other skill.** Read the audit-plan files directly. Surface ambiguity to the user; do not delegate.
- **Don't reformat or inline-clean unrelated code** in a refactor commit. Keep the diff minimal — the resumable unit is the contract.
- **Don't `git add -A`** or commit unrelated working-tree changes. Stage only the files that satisfy the current unit plus the state files this loop updates.
- **Don't amend, force-push, or use `--no-verify`** without explicit user authorization. "Explicit" means the user types something unambiguous like `yes, bypass hooks`. Always create a new commit when fixing a hook failure.
- **Don't skip the green baseline.** If no test exists, write a characterization test first and commit it separately. Refactoring without behavioural coverage is a coin flip.

## Companion files

- [ACTIONS.md](ACTIONS.md) — catalogue of migration actions (move file across layers, extract entity, invert dependency through port/gateway, replace class with closure factory, decompose framework-coupled service, replace exception with Result/Either) and safe-move recipes per kind.
- [RESUMING.md](RESUMING.md) — STATE.md / progress.md schemas, three-state checkbox protocol, in-progress flag, ADR-conflict handling.
