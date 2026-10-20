---
name: flatten-directory
description: Flatten deep/duplicated directories or convert references to flat files
argument-hint: "<path> [--mode refs|code|all] [--depth N]"
related:
  - move-to
  - update-references
  - report-file-structure
  - deep-review-codebase
  - deep-validate
  - report
  - report-progress
  - suggest-next-action
  - scan-codebase
  - check-reference
  - clean-empty-dirs
  - ask-me
  - review-devin-global-harness
---

## Goal

Reduce directory-structure depth and duplication across 3 jobs: collapse over-nested or name-duplicated dirs (`src/components/components/`, single-child chains), convert skill references from `references/<name>/SKILL.md` to flat `references/<name>.md` files, and flatten code directories into a flat structure — updating references on every move

## Scope

- Use when the structure is too deep: `a/a/a/`, long single-child chains, wrapper dirs that add no value
- Use when `references/` holds nested directories that must be converted to flat `.md` files
- Use when code directory nesting must be reduced to simplify imports or prepare a migration
- Destructive-adjacent: actually moves/converts files — always dry-run + user confirm + `/update-references`
- Not for top-level active skills that must keep `<skill-name>/SKILL.md`

## Modes

Select a mode with `--mode` (default: `all`) — each mode uses the same steps but different targets and naming rules

| Mode | Target | Result |
| --- | --- | --- |
| `all` | Both references and code dirs | collapse nesting + flat references + flat code everywhere |
| `refs` | a skill's `references/` | convert `references/<name>/SKILL.md` → `references/<name>.md` |
| `code` | code directories under `<path>` | move files from nested dirs into flat, kebab-case-named files |

## Execute

### 1. Analyze Depth And Structure

> Goal: map the structure and find over-deep or duplicated spots within the selected mode's scope

1. Run `/report-file-structure` to view the current tree, and `/scan-codebase` for mode `code`/`all` to list every file
2. Find patterns: single-child chains (`a/b/c/` where b and c have one child), name repetition (`foo/foo/`, `src/src/`), wrapper dirs holding a single dir only
3. Measure depth per leaf — flag paths deeper than `--depth` (default: >4 from root)
4. For mode `refs`/`all` → use `glob` to find `references/*/SKILL.md` and check that the frontmatter `name` matches the directory name
5. For mode `code`/`all` → identify exclusions: `node_modules`, `.git`, `dist`, `.output`, `target`, `build`, `coverage`, hidden files, and inspect `package.json`, `tsconfig.json`, `Cargo.toml` for path aliases and the build pipeline

### 2. Plan Flattening

> Goal: design the target structure and mapping before moving

1. Run `/deep-review-codebase` — plan relocations that do not break valuable grouping
2. Build the `old path → new path` mapping:
   - mode `refs`: `references/<name>/SKILL.md` → `references/<name>.md`, where `<name>` must match the frontmatter `name`
   - mode `code`: `old/path/file.ext` → `flat-name.ext` in kebab-case, prefixing parent dir names for uniqueness (e.g. `domain-user-service.ts`) — rename index files to `dirname-index.ext`
   - mode `all`: combine both mappings plus single-child collapse of wrapper dirs
3. Flag collisions: duplicate filenames that would clash after flattening → rename or keep nested; never overwrite existing files
4. If a dir in `references/` contains files other than `SKILL.md`, or many moves are involved → ask the user via `/ask-me` with a mapping preview before proceeding — if not confirmed → stop and report

### 3. Execute Moves

> Goal: move and convert files per the confirmed mapping

1. Run `/move-to` following the mapping — group by group for easy rollback; use `git mv` inside a git repo to preserve history
2. For mode `refs`/`all`: write `<name>.md` from the original `SKILL.md` content, verify it `read`s and the frontmatter is intact, then delete the `<name>/` directory — if the dir is not empty after the move → stop and report
3. Remove leftover empty dirs per `/clean-empty-dirs`
4. Run `/update-references` immediately after every move group — no exceptions

### 4. Update All References

> Goal: fix every path referencing the old location to point to the new one

1. mode `refs`/`all`: search the repo for `references/<name>/` and `references/<name>/SKILL.md` and replace with `references/<name>.md` — including the `related` lists of active skills
2. mode `code`/`all`: fix relative imports (`../`, `./`), barrel exports (`index.ts`, `mod.ts`, `lib.rs`), path aliases in config, and `package.json` `exports`/`types`/`main` as needed
3. Search the whole repo for the old paths to catch remaining string references — including README, docs, comments, and test files
4. Repeat `/update-references` until no stale references remain

### 5. Validate

> Goal: no broken references and the new structure works

1. Run `/check-reference` to catch broken path references — if the skills repo changed, also run `/review-devin-global-harness`
2. Run `/deep-validate` — run the project's build / test / lint for mode `code`/`all`
3. If issues are found → fix and re-validate, up to 3 rounds → if still failing, stop and report

### 6. Report

> Goal: summarize the structural change for later review

1. Run `/report table` with columns `No.`, `Old Path`, `New Path`, `Files Moved`, `Refs Updated` plus a before/after depth comparison
2. List any manual follow-ups (docs outside the repo, external links)
3. Run `/report-progress` to summarize done/pending work, then `/suggest-next-action`

## Rules

### 1. Confirm Before Move

- every structural change requires a dry-run preview + user confirm via `/ask-me` first — never flatten without asking
- preserve git history — `git mv`, not copy+delete
- never delete originals until verification passes, and never overwrite existing files
- if the git working tree is dirty → stop and report before converting

### 2. References Always

- run `/update-references` after every move or file conversion — no exceptions
- verify no stale references remain before finishing, via `/check-reference` and `/deep-validate`
- do not change the frontmatter `name` of a converted flat file

### 3. Naming And Exclusions

- flat filenames use kebab-case and keep parent context for uniqueness — do not change extensions
- `references/<name>.md` must match the frontmatter `name` — fix mismatches before flattening
- skip `node_modules`, `.git`, `dist`, `.output`, `target`, `build`, `coverage`, `tmp`, `temp`, `.cache`, hidden files, and binary assets unless an explicit include is given

### 4. Value Preserving

- flatten only valueless nesting — keep meaningful grouping (feature boundaries)
- watch for framework conventions (`app/`, `pages/` that routers expect)
- do not convert top-level active skills that must keep `<skill-name>/SKILL.md`

## Expected Outcome

- A shallower, more meaningful structure — no redundant nesting or unnecessary single-child chains
- No nested `references/<name>/` left — every reference is a `references/<name>.md`
- Code files in scope sit in a flat directory with unique kebab-case names
- All references updated and verified, with no broken references
- Git history preserved via `git mv`, with a complete mapping table reported
