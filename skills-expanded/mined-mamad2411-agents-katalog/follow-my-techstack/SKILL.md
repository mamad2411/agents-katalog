---
name: follow-my-techstack
description: Use the canonical tech stack catalog as the default choice when selecting or using dependencies in a project
argument-hint: "[category-or-need]"
related:
  - deep-review-codebase
  - use-lib-effective
  - deep-research
  - list-raindrop-favorite
  - search-raindrop
  - run-install
  - ask-me

---

## Goal

Select and use dependencies/tools per the user's canonical tech stack so every project uses the same stack, drift is reduced, and new lib decisions aren't made without need

## Scope

Use when a task must pick a library/tool/service for one need (e.g. validator, HTTP client, ORM, testing, styling) — whether installing fresh or using what exists

- Canonical catalog: `../follow-my-techstack/references/techstack-catalog.md` — the single source of truth, never copy its content here
- Review a whole project's stack against the catalog → `/deep-review-codebase`
- Find packages not yet in the catalog → `/deep-research dependencies`
- Install a package → `/run-install`

## Execute

### 1. Read Catalog

> Goal: get the Default pick for the wanted category

1. Read `../follow-my-techstack/references/techstack-catalog.md`
2. Find the category matching the need (e.g. "Validator", "HTTP Client", "ORM")
3. Take the `Default` column of the ecosystem matching the project (TS / Rust / Vue / TanStack / Cloudflare / Third-Party)

### 2. Apply Selection Rules

> Goal: get the choice that fits the context

1. Always use the `Default` — unless a `(→ ...)` condition in `Alternatives` matches the project (e.g. `Hono` → CF Workers)
2. If the project already has a lib in that category → keep using it; don't switch to match the default without reason
3. If the project uses a non-default with no reason → flag the drift for the user to decide via `/ask-me`; don't migrate on your own
4. If the wanted lib isn't in the catalog → run `/deep-research dependencies`, then propose a catalog update

### 3. Consult Preference Signals

> Goal: know whether the user has extra preferences beyond the catalog

1. Run `/list-raindrop-favorite` when comparing several alternatives — favorites are a curated preference signal
2. Run `/search-raindrop "<library>"` — if a candidate is bookmarked → its preference weight rises

### 4. Install And Use

> Goal: use the pick in practice, following best practices

1. Install with `/run-install` per the project's package manager
2. If there is a `follow-lib-*` / `follow-tool-*` / `follow-service-*` skill for the chosen one → invoke that skill to use it correctly (never guess the API)
3. If there is no dedicated skill → read the official docs via `/learn-from-web` or context7

## Rules

### 1. Catalog Is Source Of Truth

- Read only from `../follow-my-techstack/references/techstack-catalog.md`; never hardcode a duplicated list
- If the catalog is found outdated → propose updating the catalog, not fixing it inside this skill

### 2. Existing Before New

- A lib already installed in the manifest matters more than the default pick — switch only with a clear reason (EOL, security, broken)
- Never add a new dependency when an existing dep can do it

### 3. No Silent Drift

- A choice conflicting with the default must have a recordable reason (comment, ADR, or a `(→ ...)` condition in the catalog)
- High-risk or unclear decision → `/ask-me`
- Use /use-lib-effective if needed

## Expected Outcome

- Every lib choice traces back to the catalog or the user's preference signals
- No unintentional dependency drift
- The chosen lib is used per the matching `follow-lib-*`/`follow-tool-*`/`follow-service-*` skill
