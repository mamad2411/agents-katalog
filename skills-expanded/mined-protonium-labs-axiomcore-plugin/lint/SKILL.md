---
name: lint
description: Health checks for the vault, the hierarchy structure, and all markdown files. Actions - all (every check), markdown (style only), vault (delegates to vault-gardener agent), structure (hierarchy depth and numbering), overview.
---

# Task

Execute the requested action: $ARGUMENTS

Calling rule: `/lint <action>`.

If the requested action is ambiguous or contradictory, do NOT guess: flag it and ask for clarification before executing.

---

## If action is empty

Describe this skill: its purpose and the actions table from "overview". Do not execute anything.

## If action is "overview" (or unknown)

| Argument | Action |
| :--- | :--- |
| `all` | Markdown style check + vault health check + structure check |
| `markdown` | markdownlint across all .md files, auto-fix what is safe |
| `vault` | Full vault audit via the vault-gardener agent: freshness, links, orphans, index, structure mirror, frontmatter, contradictions |
| `structure` | Hierarchy: declared depth vs actual nesting, numbering, registry vs filesystem, naming convention |
| `overview` | This table |

If the action was unknown, say so first, then show the table.

---

## If action is "markdown" (also part of "all")

1. Run `npx --yes markdownlint-cli2 --fix "**/*.md"` from the workspace root (config: `.markdownlint.json`, shipped with the workspace; if it is missing, create it with defaults and MD013 disabled).
2. Report anything not auto-fixed and fix those manually.

## If action is "vault" (also part of "all")

1. Delegate to the **vault-gardener** subagent. It owns the check list, the severity report, and the safe-fix rules.
2. Relay its report to the user unchanged.
3. For every "Needs your decision" item the user approves, apply the proposed fix, then re-run the affected check to confirm.

## If action is "structure" (also part of "all")

Checks the hierarchy rules of root CLAUDE.md (Hierarchy Protocol, Output Hygiene & Naming, Task ID Protocol) against what is actually on disk. Registries are the source of truth: `vault/projects/<project>/ids.md` for projects, `vault/workstations/<workstation>/areas.md` for workstations.

1. **Depth declared.** Every project and workstation must carry a `Levels: **2**` or `Levels: **3**` line in its registry. Missing → report it; do not guess the depth from the folders.
2. **Depth respected.**
   - 2-level: no sub-unit folders at all; every WP/WA sits directly under the project or workstation.
   - 3-level: no WP/WA directly under the project or workstation; every one of them sits inside a numbered sub-unit.
   A violation is never auto-fixed — moving a WP renumbers it and rewrites task IDs, which is a `/setup` migration. Report and stop there.
3. **Numbering.** Every sub-unit, WP and WA folder carries a zero-padded numeric prefix. Numbers are unique within their parent — duplicates inside one sub-project are an error; the same number reused across two sub-projects is correct and expected at 3 levels.
4. **Naming convention.** Every generated folder and file name is Latin-alphabet kebab-case (fixed-name and prefix exceptions per root CLAUDE.md). Report violations; renaming is a user decision.
5. **Registry vs filesystem.** Every registry row has a matching folder and every folder a matching row, in both the working tree and the vault mirror. Each counter must exceed the highest number actually used — a counter that has fallen behind will hand out a duplicate on the next allocation.
6. **Mirror symmetry.** For every WP and WA, the vault path matches the working-tree path exactly, acronym and number prefixes included.
7. **Task IDs match location.** In each WP's `tasks.md`, every task ID's prefix must equal that WP's own numbers (`XX-WW` at 2 levels, `XX-SS-WW` at 3) and its part count must match the project's declared depth. Report mismatches; renumbering is a migration, not a lint fix.
8. **Work only in WP/WA.** No `resources/` or `outputs/` folder anywhere except inside a WP or a work area.
9. **Produced filenames.** Every file you produced inside a WP or work area matches `<acr>-<address>-<NNN>-<name>.<ext>`, with `<acr>` and `<address>` equal to the unit it sits in — a file carrying another unit's address is in the wrong folder. Setup files match `su-<NNN>-<name>.md`. Report: numbers duplicated within a unit (legitimate only for one document exported in several formats, same name part), a `Next output` / `Next setup` counter at or below the highest number in use, leftover date or version strings in a filename, and markdown deliverables missing the header block or the `## Changelog` section. Feature documents (`<acr>-<address>-f###-<slug>.md`) are exempt from the number, the header and the changelog. **User uploads are never checked** — only files you produced; when authorship is unclear, report nothing.

---

## After any action

- Append summary to `vault/log.md`.
- Report: fixed automatically vs needs user decision, as two short lists.

## Notes

- Never delete pages (root CLAUDE.md hard rule); deprecate with a note instead.
- `vault/sources/` is excluded from all checks (read-only).
- The structure check **reports, it does not repair**. Every fix for a depth or numbering violation moves folders and rewrites IDs, which belongs in a `/setup` migration file. Correcting a registry typo is the one safe exception.
