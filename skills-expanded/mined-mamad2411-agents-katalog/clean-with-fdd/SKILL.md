---
name: clean-with-fdd
version: 2
description: >-
  Audit a codebase against Clean Architecture + Feature-Driven Development and produce a migration plan toward framework-free, third-party-agnostic business logic in feature slices. Use when the user asks to audit for clean architecture violations, plan a migration to feature slices, check a diff for violations, review layer dependencies, or restructure into feature slices. Modes: `whole`, `feature <name>`, `diff`. Language-agnostic. Audit-and-plan only — never modifies production code.
---

# Clean with FDD

Audit and plan migration toward **Clean Architecture + Feature-Driven Development**, in **any language**, with framework- and third-party-agnostic business logic. This skill **only audits and plans** — it never writes production code. State is persisted so a session can resume mid-workflow.

Code examples in these docs are mostly TypeScript for concreteness, but every rule applies to Python, Go, Rust, Java, Kotlin, C#, Ruby, PHP, etc. Per-language guidance lives in [FP-DISCIPLINE.md](FP-DISCIPLINE.md).

## Core rules

1. **Frameworks are delivery only.** Web frameworks (React/Vue/Next/Express/Nest/Hono/Django/Flask/FastAPI/Rails/Spring/ASP.NET/Gin/Axum/etc.) live exclusively in **controllers** (backend) or **presenters** (frontend). Domain and use-cases must compile with zero framework imports.
2. **Third-party-agnostic business logic.** Stripe, Prisma, Mongoose, SQLAlchemy, GORM, Diesel, Hibernate, Axios, etc. are reached through **ports** in the use-case layer; **adapters** live outside the domain.
3. **Favor data + functions over heavy OOP in business logic.** Entities are typed values; use-cases are functions; adapters are constructed via factories or lightweight injection. JS/TS goes further — **no classes at all** because of eslint/biome lint friction. Other languages follow the spirit (small data classes / records / structs are fine; deep inheritance and framework-bound base classes are not). See [FP-DISCIPLINE.md](FP-DISCIPLINE.md).
4. **Sum types + value-typed errors.** Use the language's tagged-union equivalent (TS discriminated unions, Rust enums, Kotlin sealed classes, Python `Literal`-tagged dataclasses or `match` types, Go constant-tagged structs, C# records w/ pattern match). Errors in domain/use-cases are returned as values (`Result<T, E>`, `Either`, `(T, error)`, `Outcome<T>`), not thrown.
5. **Dependency rule.** Inner layers know nothing of outer ones. Imports point inward only. See [LAYERS.md](LAYERS.md).
6. **Feature slices + shared kernel.** `<src>/features/<feature>/` self-contained; `<src>/shared/{domain,ports}/` for cross-feature primitives. See [STRUCTURE.md](STRUCTURE.md).

Full vocabulary in [LANGUAGE.md](LANGUAGE.md). Use these terms exactly — don't drift into "service," "component," "module," "boundary."

## Modes

- `whole` — audit the entire repo, list every feature slice, output a global migration plan.
- `feature <name>` — audit/plan a single feature end-to-end.
- `diff` — check the current git diff for Clean+FDD violations.

All modes are **audit + plan only**. Output is written under `.plans/clean/<run>/` (one directory per invocation — `STATE.md`, per-slice `progress.md`, and `adr/`), plus the repo-level `CONTEXT.md`. No production code is modified.

### Choosing a mode (cadence guide)

This skill is safe to invoke repeatedly. Pick the mode that matches the cadence:

- **After each feature / before commit** → `diff`. Scoped to what just changed; cheap, focused, no noise from pre-existing violations. This is the recommended default for per-feature gating.
- **Working on a known slice** → `feature <name>`. Scoped to the slice just touched or about to be touched.
- **Initial onboarding or periodic deep audit** (e.g. once per sprint, or before a major release) → `whole`. Expensive on large codebases and will repeatedly surface the same legacy violations every run, so do **not** use it after every feature.

## Workflow

### 1. Init

- **Always scan `.plans/clean/*/STATE.md` first.** If any run directories exist, read the most recent one before doing anything else and offer to resume from its last checkpoint. See [RESUMING.md](RESUMING.md). Only proceed to fresh detection when there is no run directory.
- For a fresh run, mint the run directory: `mkdir -p ".plans/clean/$(bash scripts/run-id.sh)"`. Everything this invocation writes (`STATE.md`, per-slice `progress.md`, ADR records) lives under it.
- Detect language(s) and framework(s). Read whichever manifests are present: `package.json`, `pyproject.toml`/`requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`/`build.gradle(.kts)`, `*.csproj`/`*.sln`, `Gemfile`, `composer.json`, `mix.exs`, `Package.swift`, etc. Classify as frontend / backend / fullstack / general. Save to `.plans/clean/<run>/STATE.md`.
- Ensure `CONTEXT.md` (repo-level domain glossary) and `.plans/clean/<run>/adr/` exist; create lazily if needed.

### 2. Explore

Use the Agent tool with `subagent_type=Explore` to walk the codebase. Look for:

- **Framework leaks** in domain/use-case code (any framework import in a use-case is a flag — see [MIGRATION.md](MIGRATION.md) for per-language signal lists).
- **Disallowed OOP** for the language — for JS/TS, any `class` outside delivery; for other languages, deep inheritance, framework-bound base classes, or business logic on ORM model classes.
- **Layer crossings** that violate the dependency rule (adapter importing from controller, etc.).
- **Implicit features** — clusters of files that should become a slice but currently sprawl across folders.
- **Exception-based error paths** in business logic where the language can express errors as values.

See [MIGRATION.md](MIGRATION.md) for the full audit checklist.

### 3. Present plan

Output a numbered migration plan. For each item:

- **Slice** — feature name (use CONTEXT.md vocabulary; add new terms as they are found).
- **Layer** — domain / use-case / adapter / controller-or-presenter.
- **Files** — current locations.
- **Violation** — which core rule is broken.
- **Action** — what the migration does (move, extract, invert dependency, replace class with closure factory, etc.).
- **Resumable unit** — a single commit-sized chunk; recorded as a task in `.plans/clean/<run>/<feature>/progress.md`.

Do **not** modify code. Ask the user which slice to commit to first.

### 4. Persist state

After every meaningful decision, update:

- `.plans/clean/<run>/STATE.md` — current focus, project type, pending slices, decisions log.
- `.plans/clean/<run>/<feature>/progress.md` — per-slice checklist (entities → use-cases → ports → adapters → controllers/presenters).
- `CONTEXT.md` — new domain terms (repo-level; persists across runs).
- `.plans/clean/<run>/adr/NNNN-*.md` — load-bearing decisions worth preserving.

If a candidate contradicts an existing ADR, surface it only when friction warrants reopening the decision; mark clearly (_"contradicts ADR-0007 — but worth reopening because…"_).

### 5. Resume

On any later session, read the most recent `.plans/clean/<run>/STATE.md` first. Re-orient to the current slice and the last completed checkpoint before doing anything else. See [RESUMING.md](RESUMING.md).

## Scripts

- `scripts/run-id.sh` — prints the run-directory id (colon-free UTC ISO 8601, minute precision, e.g. `2026-05-12T1432Z`). Used in step 1 to mint a fresh run: `mkdir -p ".plans/clean/$(bash scripts/run-id.sh)"`. Pass `--seconds` if a run dir already exists for the current minute. Pure — prints to stdout, creates nothing.

## Glossary (compact)

- **Slice** — a feature: domain + use-cases + ports + adapters + delivery, all in one folder.
- **Domain** — entities, value types, invariants. Pure. Framework-free. Free of disallowed OOP for the language.
- **Use-case** — application logic. A function (or smallest equivalent) over ports. Framework-free.
- **Port** — interface that a use-case depends on (function type, record of functions, language interface, trait, protocol, abstract base — whichever is idiomatic).
- **Adapter** — concrete implementation of a port. May import third-party libs.
- **Controller** — backend delivery (HTTP handler, queue worker, gRPC service). Framework lives here.
- **Presenter** — frontend delivery (page, view-model). Framework lives here.
- **Shared kernel** — `<src>/shared/{domain,ports}/` — primitives reused across slices.

Full definitions: [LANGUAGE.md](LANGUAGE.md).
