# Project Instructions

## Project

This repository contains a War Thunder progression planner and calculator.

The application helps players determine the vehicles, Research Points (RP), Silver Lions (SL), and estimated matches required to reach a target vehicle while respecting research prerequisites and rank unlock requirements.

The backend is built with C# and ASP.NET Core.

## Engineering approach

Prefer a modular monolith unless there is a demonstrated reason to introduce distributed services.

Keep domain/business logic independent from ASP.NET controllers, Entity Framework Core, and presentation concerns.

Do not introduce new frameworks, architectural patterns, abstractions, repositories, libraries, or services without a concrete benefit.

Prefer straightforward, maintainable C# over unnecessary abstraction.

### Domain principles

A Vehicle represents the stable identity of a War Thunder vehicle.

Values that can change between War Thunder updates, such as:

* Research Point cost
* Silver Lion cost
* rank
* tree position
* research availability
* prerequisite relationships

must belong to versioned tech-tree data rather than overwriting the stable Vehicle identity.

Published tech-tree versions should be treated as immutable historical snapshots.

Vehicle progression is a graph. Do not infer progression requirements solely from visual row/column placement.

Visual tree positioning and progression dependencies are separate concepts.

Rank unlock requirements must be data-driven rather than hard-coded.

## Architecture documentation

Use `docs/PRODUCT.md` when behavior or product scope is relevant.

Use `docs/DOMAIN.md` when changing domain concepts or progression rules.

Use `docs/ARCHITECTURE.md` when changing project/module boundaries.

Use `docs/DATABASE.md` when changing persistence models or migrations.

Do not require these documents to be read for unrelated trivial changes.

Use `docs/DECISIONS.md` when you are uncertain about past technical decisions or the project's historical context.

## Project execution model

This repository is an ASP.NET Core HTTP REST API backed by PostgreSQL.
It is not a desktop/GUI application or CLI product.

Use `docs/ROADMAP.md` for implementation sequencing.
Use `docs/WORKFLOW.md` for the batch implementation and verification process.

Verification must be proportional to the change:

- production code: build + relevant tests;
- persistence changes: additionally verify migrations/database behavior;
- HTTP contract changes: manually run the API and call affected REST endpoints only when useful;
- documentation-only work: do not start the API without a concrete reason.

Do not treat executing the generated `.exe` as a generic acceptance test.

## Development behavior

Before making a substantial architectural change, inspect the relevant existing implementation and explain significant tradeoffs.

When refactoring, preserve existing behavior unless the task explicitly changes that behavior.

Prefer incremental, reviewable changes over rewriting unrelated code.

If existing code differs from the intended architecture, identify the discrepancy rather than silently working around it.

Run relevant builds and tests after implementation.

Do not modify generated migration files after they have been applied unless the task explicitly requires correcting an unapplied migration.

## Learning

The repository owner is learning software architecture and C#.

For significant changes, briefly explain:

* what was changed,
* why the previous design was problematic if applicable,
* why the new design is preferable,
* important tradeoffs,
* what concept the owner should understand from the change.

Keep explanations practical and tied to this codebase.