---
name: modular-refactor
description: Refactor an existing repo or set of files into multiple small, loosely coupled files with one component/responsibility per file, so the code is more readable, testable and scalable. Use this skill whenever the user asks to split, break up, modularize, decouple, restructure, reorganize, or clean up a codebase; mentions "god files", huge files, spaghetti code, tight coupling, separation of concerns, "one component per file", or scalable folder structure; or says code is hard to read or maintain. Trigger even if they don't say "refactor" explicitly - e.g. "this file is too long", "make this repo cleaner", "organize my project".
---

# Modular Refactor

Turn large, tangled files into small, focused, loosely coupled modules - without changing what the code does.

The goal is not "more files". The goal is that a developer can open any file, understand its single purpose in seconds, change it without breaking unrelated things, and add a new feature by adding files rather than editing many. Splitting for its own sake produces a maze; splitting along real responsibility boundaries produces a codebase that scales.

## Core rules

1. **Preserve behavior.** A refactor moves and reshapes code; it never changes logic, outputs, or public APIs. If you spot a bug, note it in the report but don't fix it in the same pass - mixing the two makes regressions impossible to trace.
2. **One responsibility per file.** One React/Vue component, one class, one route handler group, one service, one data model per file. A file that needs "and" to describe it (e.g. "fetches users *and* formats them *and* renders them") should be split.
3. **Depend inward, never sideways or in circles.** Dependencies flow from high-level (UI, routes, entry points) toward low-level (services, utilities, types). No circular imports. See `references/coupling-and-layering.md`.
4. **Depend on abstractions at the seams.** Where a module talks to something volatile (database, HTTP, filesystem, third-party SDK, clock), pass it in (parameter, constructor, or interface) instead of importing a concrete instance. This is what makes code testable and swappable.
5. **Keep the public surface stable.** Existing import paths used elsewhere should keep working - via re-exports (`index.ts`, `__init__.py`) - unless the user approves a breaking move.
6. **Don't over-split.** Three 10-line helpers used only by each other belong together. Split when responsibilities differ or a file exceeds roughly 200-300 lines, not to hit a file count.
7. **Follow the repo's existing conventions** (naming, casing, test layout, formatter). Consistency beats theoretical purity.

## Workflow

Work through these phases in order. Do not skip the plan; users trust a refactor far more when they've seen and approved the target structure first.

### Phase 1 - Survey

- Identify language(s), framework, package manager, test runner, and build/lint commands (check `package.json`, `pyproject.toml`, `pom.xml`, `go.mod`, `Makefile`, CI config).
- If a terminal is available, run the scanner to find refactor candidates quickly:
  `python <skill-dir>/scripts/scan_repo.py <repo-path>`
  It ranks files by size and number of top-level definitions and flags likely multi-responsibility files. If you can't run it, do the same by hand: list the largest files and skim for mixed concerns.
- Establish a **safety net**: run existing tests/build/lint and record the baseline. If there are no tests, tell the user, and offer to add a few characterization tests (tests that pin down current behavior) for the riskiest files before refactoring.
- Read `references/language-patterns.md` for the section matching the repo's stack.

### Phase 2 - Diagnose

For each candidate file, name its responsibilities in plain words. Look for the smells in `references/coupling-and-layering.md` (mixed layers, hidden global state, circular imports, feature envy, shotgun-surgery risk, etc.). This diagnosis drives the split - each distinct responsibility becomes a module.

### Phase 3 - Plan (present before editing)

Produce a plan in this format and **ask the user to confirm before changing files**:

```
## Refactor plan

### Current problems
- <file>: <N lines>, mixes <A>, <B>, <C>

### Target structure
<tree of the proposed layout, marking [new] / [moved] / [unchanged]>

### Move map
| From (symbol @ file)        | To (new file)                  | Reason              |
|-----------------------------|--------------------------------|---------------------|

### Decoupling changes
- <what dependency is inverted/injected and why>

### Risks & compatibility
- <public imports preserved via re-exports, anything that needs user decision>

### Order of work
1. <smallest/safest first> ...
```

For small requests (one file, obvious split) a short plan is fine. For anything touching many files, keep the plan complete.

### Phase 4 - Execute in small, verifiable steps

- Refactor **one module at a time**, leaf/low-level code first (types, constants, utils), then services, then UI/routes. Leaves have few dependents, so mistakes are cheap.
- Use `git mv` when a file is moved wholesale, so history follows it.
- After each step: update imports, then run type-check/build/lint/tests. Fix before moving on. Never leave the repo in a broken state between steps.
- Extract, don't rewrite: cut the code into its new home and adjust only what's needed (imports, exports, injected parameters). Resist "improving" logic while moving it.
- Add re-exports from the old location when other code (or external consumers) import from it, and mark them with a short comment so they can be retired later.
- Keep each new file cohesive: imports at top, one primary export, private helpers below or in a sibling `*.helpers` file if they grow.

### Phase 5 - Verify

- Run the full test/build/lint suite and compare with the Phase 1 baseline.
- Check there are no circular imports (tools listed in `references/coupling-and-layering.md`), no unused imports, and no leftover dead code from the split.
- Confirm the public API is unchanged.

### Phase 6 - Report

Give the user a concise summary:
- Before/after: file count, largest file size, structure tree.
- What was decoupled and how (injection points, layer boundaries).
- Verification results (tests/build/lint status vs. baseline).
- Follow-ups you noticed but deliberately did not do (bugs, missing tests, naming, deeper redesigns).

## Naming and layout guidance

- Name files after their single export (`UserCard.tsx`, `user_repository.py`, `OrderService.java`). If a good name is hard to find, the file probably has two responsibilities.
- Group by **feature/domain first**, layer second, for anything beyond a small app (`features/orders/{components,services,types}` scales better than global `components/`, `services/`, `utils/` buckets). For small repos, layer-based is fine - don't reorganize a working small structure just to be fashionable.
- Avoid dumping-ground files: `utils`, `helpers`, `common`, `misc`. If something lands there, give it a specific name (`date_format`, `retry`, `currency`).
- Keep shared code shared *by need*, not by guess: leave code local until a second consumer actually appears.
- Put types/interfaces/constants in their own small files when several modules share them; keep them next to the code when only one module uses them.

## When to stop or ask

- No tests and high-risk logic (payments, auth, migrations): pause and confirm approach with the user.
- Framework conventions dictate file layout (e.g. Next.js `app/` routing, Django `models.py` expectations, Rails autoloading): follow the framework, and split *within* its rules.
- A split would require breaking a public API or changing a database/wire format: stop and ask.
- Generated code, vendored dependencies, lockfiles, build output: leave untouched.

## Anti-patterns to avoid

- Splitting by *type of syntax* (all interfaces in one file, all functions in another) instead of by responsibility.
- Creating a file per function regardless of cohesion.
- Introducing abstractions (interfaces, factories, DI containers) where there is only one implementation and no seam that needs testing or swapping.
- Barrel files that re-export everything and create hidden circular dependencies - export only the intended public API of each module.
- Big-bang refactors committed as a single change. Prefer a sequence of small, reviewable commits.
