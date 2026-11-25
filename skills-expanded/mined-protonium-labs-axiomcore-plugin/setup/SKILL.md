---
name: setup
description: Owns the setup/ area and makes the system adaptable. Actions - new (draft a capability setup file via guided interview), run (execute a pending setup file), list, overview. Also owns structural migrations - changing the hierarchy depth of a project or workstation. First-run onboarding is owned by /axiom, not here.
---

# Task

Execute the requested action: $ARGUMENTS

Calling rule: `/setup <action> <arguments>`.

If the requested action is ambiguous or contradictory, do NOT guess: flag it and ask for clarification before executing.

First-run onboarding and module activation are owned by `/axiom` — if the user asks for initial setup, point them to `/axiom start`.

---

## If action is empty

Describe this skill: its purpose and the actions table from "overview". Do not execute anything.

## If action is "overview" (or unknown)

| Argument | Action |
| :--- | :--- |
| `new <capability idea>` | Guided interview + structure analysis → draft a new setup file in `setup/` |
| `run <name>` | Execute a pending setup file and archive it to `setup/done/` |
| `list` | Show pending and installed capabilities |
| `overview` | This table |

If the action was unknown, say so first, then show the table.

---

## If action is "new"

Goal: turn a capability idea into a reviewable setup file — nothing is implemented in this action.

1. Check $ARGUMENTS (after "new"): the capability idea. If empty: ask what capability the user wants. **If the idea is a hierarchy-depth change** for an existing project or workstation, skip the capability interview and follow "Structural migrations" below instead — the file has a fixed content list.
2. **Interview**, one block at a time, only what the idea leaves open:
   - Goal: what should the capability do, for whom, how often (recurring or one-off)?
   - Inputs: what arrives, where does it land (folder, MCP, email)?
   - Outputs: what is produced, where does it go?
   - Integrations: which MCPs/services are needed?
   - Additions: new skills, agents, vault areas?
3. **Analyze the current structure**: root CLAUDE.md rules (hierarchy, WP-only work, vault mirroring), existing projects, `vault/index.md`, installed capabilities in `setup/done/`. The capability must fit the system rules — e.g. a "drop folder for bills" becomes a WP `resources/` folder inside a finance project, not a foreign folder.
4. **Draft** `setup/su-<NNN>-<name>.md` (kebab-case name, no `-setup` suffix — the folder and the acronym already say it): sections Capability, Prerequisites, Installs (concrete list), Open decisions (what remains to clarify at run time), Definition (detailed behavior). Status: pending. Allocate `<NNN>` **here, at drafting**, from `Next setup` in `setup/README.md` and bump the counter — monotonic, never reused; a discarded draft does not free its number. Setup files are deliverables: the file carries the standard header block and changelog (`.claude/templates/output-document-template.md`, acronym `SU`) and keeps its name when it is later archived to `done/` — the number is how it is cited afterwards.
5. Read the draft back to the user; iterate until approved. Lint the file.

---

## If action is "run"

1. Check $ARGUMENTS (after "run"): match against files in `setup/` (not `done/`). No match or empty: run "list" and ask which one.
2. Read the file. Verify prerequisites; if one is missing (e.g. MCP not configured), stop and tell the user what to do first.
3. Clarify all open decisions with the user.
4. Implement what "Installs" defines. Workflow discipline applies: present the implementation plan from the file, get approval, execute step by step. For a hierarchy-change file the folder map and registry rewrite take the place of "Installs" — follow the execution rules in "Structural migrations" below.
5. Record the decisions and results in the setup file, bump its version and add a changelog row, set Status: installed with date, then **move it to `setup/done/` under its own name** — archiving never renames a setup file.
6. Lint all changed .md files.

---

## If action is "list"

Show two tables: **Pending** (files in `setup/`, excluding README) and **Installed** (files in `setup/done/`, with installation date from the file). One line per capability: name, what it installs, prerequisites state if known.

---

## Structural migrations (hierarchy depth)

`/project` and `/ws` refuse to change the hierarchy depth of an existing unit and send the user here. Such a change renumbers folders and — on the project side — rewrites every task ID in the project, so it is drafted as a file, reviewed, executed once, and archived to `setup/done/` as the record of what was migrated. (Advanced tier only; from simple tier, `/axiom tier advanced` comes first.)

Name the file `su-<NNN>-<acr>-hierarchy-change.md` (e.g. `su-004-pw-hierarchy-change.md`) — the unit prefix rides inside the name part, the number comes from `setup/README.md` as for any setup file. Beyond the standard sections it MUST contain:

1. **Unit and direction** — which project or workstation, its current `Levels` value (read from `ids.md` / `areas.md`), and the target.
2. **Complete folder map** — every sub-project/sub-workstation and every WP/WA, old path → new path, with the numbers each receives. No "and so on": the map is the instruction, and anything missing from it does not get moved.
3. **Registry rewrite** — the new `ids.md` / `areas.md` in full: `Levels`, the sub-unit counter, and each sub-unit's own `Next WP` / `Next area`.
4. **Task ID map** (project side) — old ID → new ID for every task. Task numbers (`TT`) are preserved; only the prefix changes.
5. **Reference sweep** — the list of files holding paths or IDs that must follow: `[[wiki links]]` across the vault, `vault/index.md`, the project `CLAUDE.md` Structure section, the root routing map, `board.md` where the Todos module runs in Notion mode.
6. **Board policy** (Notion mode only) — state explicitly whether cards are repushed or left untouched. Leaving them stale is a valid choice; leaving it unstated is not.
7. **Rollback** — what to restore if the migration is interrupted midway.

Execution rules for these files:

- The "monotonic, never reused" guarantee (Task ID Protocol) is **suspended for this one migration** and only here. Say so in the file, so the executed copy in `done/` explains why numbers moved.
- Show the user the complete diff before writing anything. This is the one setup file whose blast radius is the whole project.
- Move folders and rewrite references in one pass, then run `/lint all` — broken wiki links are the expected failure mode.

## After any action

- Append to `vault/log.md`, update `vault/index.md` if pages changed.
- Update the `Last updated` date in every file changed.

## Notes

- Never overwrite a filled `soul.md` or `brand-config.md` without explicit confirmation — those are owned by `/axiom`.
- "new" never implements; "run" never drafts. Keep the lifecycle clean: idea → file (new) → capability (run) → archive (done/).
