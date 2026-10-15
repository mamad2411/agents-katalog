---
name: clean-with-bob
version: 2
description: >-
  Audit a codebase against Uncle Bob's classical Clean Architecture and plan migration toward framework-free business logic in a layer-first folder hierarchy. Use when the user asks to audit for clean architecture violations, plan a migration, check a diff for violations, or review layer structure. Modes: `whole`, `layer <name>`, `diff`. Language-agnostic across 12 languages. Audit-and-plan only — never modifies production code.
---

# Clean with Bob

Audit and plan migration toward **Uncle Bob's classical Clean Architecture**, in **any language**, with a **layer-first** folder hierarchy (no feature slicing, no shared kernel) and framework- and third-party-agnostic business logic. This skill **only audits and plans** — never writes production code. State is persisted so a session can resume mid-workflow. Code examples are mostly TypeScript for concreteness; rules apply to every supported language (per-language idioms in [OOP-FP.md](OOP-FP.md)). This skill is **self-contained** — every rule, threshold, layer definition, and audit checklist it needs lives inside this directory. It does not invoke or depend on any other skill.

## Core rules

1. **Four concentric layers, in this exact taxonomy.** Entities (enterprise business rules) → Use Cases (application business rules) → Interface Adapters (controllers, presenters, gateways) → Frameworks & Drivers (web, DB, external interfaces). Names are not negotiable — they're the canonical vocabulary the rest of the audit speaks. See [LAYERS.md](LAYERS.md).
2. **The Dependency Rule.** Source code dependencies point **inward only**. An outer layer may import inner ones; an inner layer must never name an outer one. Cross this rule and the rest of the architecture is theatre.
3. **Layer-first folders, no feature slicing.** One global hierarchy per project: `<src>/entities/`, `<src>/use_cases/`, `<src>/interface_adapters/`, `<src>/frameworks_and_drivers/`. Files inside each layer can be grouped by domain concept (`entities/order/`, `use_cases/billing/`) but the **layer is the top-level partition**, not the feature. See [STRUCTURE.md](STRUCTURE.md).
4. **No shared kernel.** Entities **are** the shared layer. Anything reused across use cases lives in `entities/` if it's a domain concept, or in `interface_adapters/` (e.g. a generic gateway) if it's an integration concept. Don't introduce `shared/`, `common/`, or `core/` folders.
5. **Frameworks live only in Frameworks & Drivers.** Any web framework, ORM, mailer, queue client, or HTTP-server import found in entities or use cases is a violation. Interface Adapters reference framework **types** only as needed to translate at the boundary (e.g. an HTTP controller takes a `Request` type) — they hold no framework configuration.
6. **Third parties cross the boundary at gateways.** ORMs, payment SDKs, HTTP clients live in `interface_adapters/gateways/` (translation) and `frameworks_and_drivers/` (configuration & instantiation). Never in entities or use cases.
7. **Classes allowed; OOP discipline depends on the language.** OOP-native languages (Java, Kotlin, C#, Swift, Ruby, PHP) use idiomatic classes — concrete final classes (or sealed interfaces / sealed classes for sum-typed entities and state machines) for entities, interfaces for ports, concrete classes for adapters. FP-leaning languages (JS/TS, Python, Go, Rust, Elixir) favour functions + closures + records, even though their syntax permits classes. See [OOP-FP.md](OOP-FP.md).
8. **Errors are values in entities and use cases** when the language supports it ergonomically (`Result<T, E>`, `Either`, `(T, error)`, `OneOf<T, E>`, sum-type return). Throwing/raising is reserved for exceptional bugs, never for control flow. OOP-native languages may use checked exceptions at the use-case boundary if that is the platform norm — see [OOP-FP.md](OOP-FP.md) for the per-language stance.

Full vocabulary in [LANGUAGE.md](LANGUAGE.md). Use these terms exactly — don't drift into "service," "module," "boundary," "feature," or "slice." This skill is **not** about feature slices.

## Modes

- `whole` — audit the entire repo against the four-layer taxonomy, list every detected layer (or implicit one), output a global migration plan ordered by leverage.
- `layer <name>` — audit one layer end-to-end (`entities`, `use_cases`, `interface_adapters`, or `frameworks_and_drivers`).
- `diff` — check the current git diff for Clean Architecture violations.

All modes are **audit + plan only**. Output is written under `.plans/clean-bob/<run>/` (one directory per invocation — `STATE.md`, per-layer `progress.md`, and `adr/`), plus the repo-level `CONTEXT.md`. No production code is modified.

### Choosing a mode (cadence guide)

This skill is safe to invoke repeatedly. Pick the mode that matches the cadence:

- **After each change / before commit** → `diff`. Scoped to what just changed; cheap, focused, no noise from pre-existing violations. Recommended default for per-change gating.
- **Working on a known layer** → `layer <name>`. Scoped to the layer you just touched.
- **Initial onboarding or periodic deep audit** (e.g. once per sprint, or before a major release) → `whole`. Expensive on large codebases and will repeatedly surface the same legacy violations every run; do **not** use it after every change.

## Workflow

### 1. Init

- **Always scan `.plans/clean-bob/*/STATE.md` first.** If any run directories exist, read the most recent one before doing anything else and offer to resume from its last checkpoint. See [RESUMING.md](RESUMING.md). Only proceed to fresh detection when there is no run directory.
- For a fresh run, mint the run directory: `mkdir -p ".plans/clean-bob/$(bash scripts/run-id.sh)"`. Everything this invocation writes (`STATE.md`, per-layer `progress.md`, ADR records) lives under it. These plan files are not gitignored — if the user wants to exclude them from version control, add `.plans/clean-bob/` to `.gitignore`.
- Detect language(s) and framework(s). Read whichever manifests are present: `package.json`, `pyproject.toml`/`requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`/`build.gradle(.kts)`, `*.csproj`/`*.sln`, `Gemfile`, `composer.json`, `mix.exs`, `Package.swift`, etc. Classify as frontend / backend / fullstack / general. Save to `.plans/clean-bob/<run>/STATE.md`.
- Ensure `CONTEXT.md` (repo-level domain glossary) and `.plans/clean-bob/<run>/adr/` exist; create lazily if needed.

### 2. Explore

Walk the codebase to detect the current shape vs the target four-layer taxonomy. Look for:

- **Framework leaks** in entities/use-case code (any framework import in those layers is a flag — see [MIGRATION.md](MIGRATION.md) for per-language signal lists).
- **Third-party leaks** in entities/use-case code (ORMs, SDKs, HTTP clients).
- **Disallowed coupling** for the language — for FP-leaning languages, classes outside Interface Adapters / Frameworks & Drivers are flagged for replacement; for OOP-native languages, framework-bound base classes (`@Service`, `extends Controller`, ORM model classes with business logic) inside entities/use cases are flagged.
- **Layer crossings** that violate the Dependency Rule (entities importing from interface_adapters, etc.).
- **Folder shapes that contradict layer-first** — e.g. `src/features/<x>/` slices, `src/shared/`, `src/common/` folders that hold business logic. Flag and propose a layer-first migration.
- **Exception-based error paths** in entities or use cases where the language can express errors as values.

See [MIGRATION.md](MIGRATION.md) for the full audit checklist.

### 3. Present plan

Output a numbered migration plan. For each item:

- **Layer** — entities / use_cases / interface_adapters / frameworks_and_drivers.
- **Domain concept** — the noun the change centres on (`order`, `payment`, `user`); use CONTEXT.md vocabulary, add new terms as you find them.
- **Files** — current locations.
- **Violation** — which core rule is broken.
- **Action** — what the migration does (move file across layers, extract entity, invert dependency through a gateway, replace framework-bound class with plain entity + adapter pair, etc.).
- **Resumable unit** — a single commit-sized chunk; recorded as a task in `.plans/clean-bob/<run>/<layer>/progress.md`.

Do **not** modify code. Ask the user which item to commit to first.

### 4. Persist state

After every meaningful decision, update:

- `.plans/clean-bob/<run>/STATE.md` — current focus, project type, pending layers, decisions log.
- `.plans/clean-bob/<run>/<layer>/progress.md` — per-layer checklist (entity audit → use-case audit → adapter audit → framework audit).
- `CONTEXT.md` — new domain terms (repo-level; persists across runs).
- `.plans/clean-bob/<run>/adr/NNNN-*.md` — load-bearing decisions worth preserving.

If a candidate contradicts an existing ADR, surface it only when friction warrants reopening the decision; mark clearly (_"contradicts ADR-0007 — but worth reopening because…"_).

### 5. Resume

On any later session, read the most recent `.plans/clean-bob/<run>/STATE.md` first. Re-orient to the current layer and the last completed checkpoint before doing anything else. See [RESUMING.md](RESUMING.md).

## Scripts

- `scripts/run-id.sh` — prints the run-directory id (colon-free UTC ISO 8601, minute precision, e.g. `2026-05-12T1432Z`). Used in step 1 to mint a fresh run: `mkdir -p ".plans/clean-bob/$(bash scripts/run-id.sh)"`. Pass `--seconds` if a run dir already exists for the current minute. Pure — prints to stdout, creates nothing.

## Glossary

Full definitions: [LANGUAGE.md](LANGUAGE.md).
