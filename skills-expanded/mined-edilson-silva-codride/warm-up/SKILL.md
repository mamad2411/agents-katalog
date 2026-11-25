---
name: warm-up
description: Load product and engineering context before starting work
---

# Warm-up

Load both the product and engineering context for this project before starting work — not everything, just the entry points, so you know what exists and can pull in the rest later as the need arises.

## 1. Project preferences (`docs/PROJECT_PREFERENCES.md`)

Read `docs/PROJECT_PREFERENCES.md` if it exists, and apply its settings for the rest of this session — e.g. the language for any `docs/` or `.codex/work/` artifact you write (`context.md`, `architecture.md`, `plan.md`, business-context files, etc.). This doesn't affect conversational language — keep replying in whatever language the human writes in, as usual.

If it doesn't exist yet, say so and skip this step — it can be generated with `meta-preferences`.

## 2. Product context (`docs/business-context/`)

Read `docs/business-context/index.md` if it exists. Keep in mind what it points to (product strategy, customer personas, competitive landscape, feature catalog, etc.) without reading those files yet.

If `docs/business-context/` doesn't exist yet, say so and skip this step — it can be generated with `bootstrap-business-docs`.

## 3. Engineering context (`docs/technical-context/`)

This folder can take two different shapes depending on which skill generated it — read whichever of these exists:
- `docs/technical-context/project-briefing.md` — from `engineer-discover`. Compact (~150 lines), meant to be read in full.
- `docs/technical-context/index.md` — from `bootstrap-tech-docs`. Points to a fuller set (project charter, ADRs, codebase guide, business logic, API spec, etc.) — read the index, not everything it links to.

Keep in mind what other files it points to (ADRs, conventions, tech stack) without reading those yet either.

If `docs/technical-context/` doesn't exist yet, say so and skip this step — it can be generated with `engineer-discover` (lightweight) or `bootstrap-tech-docs` (comprehensive).

## 4. Project overview

Read the root `README.md`. Keep a list of the files under `docs/` in context so you can refer to them later as needed, without reading all of them up front.

If the user named a specific project (in a monorepo or multi-project workspace), focus this warm-up on that project.
