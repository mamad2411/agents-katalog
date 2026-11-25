---
name: ws
description: Create and run workstations - permanent areas for routine, repeated work (independent of projects). Actions - new WS, new subWS, new area, new routine, run, from project, list, overview. Hierarchy depth (2 or 3 levels) is fixed at creation.
---

# Task

Execute the requested action: $ARGUMENTS

Calling rule: `/ws <action> <arguments>`.

If the requested action is ambiguous or contradictory, do NOT guess: flag it and ask for clarification before executing.

Core principle: **work is done at work-area level only.** Workstations and sub-workstations are organizational structure for routines — the same rule work packages carry on the project side (root CLAUDE.md, Hierarchy Protocol). Projects are for temporary activity (done once); workstations are for repeated activity.

**Tier check (read `axiom-config.md` first):** in **simple** tier, every workstation is 2-level — do not ask the depth question, do not mention 3-level structure, and manage numbering silently. In **advanced** tier, follow the depth rules below in full.

---

## Hierarchy depth (advanced tier — read before any action)

Every workstation is either **2-level** or **3-level**. The depth is chosen when the workstation is created and recorded in its registry as `Levels: **2**` or `Levels: **3**`.

| Depth | Chain | Sub-workstations | Addressing |
| :--- | :--- | :--- | :--- |
| 2-level | Workstation → Work Area (WA) | Not allowed | `<ws> - <area>` |
| 3-level | Workstation → Sub-workstation → Work Area (WA) | Mandatory — every WA lives in one | `<ws> - <sub> - <area>` |

Before any action other than "new WS": read `vault/workstations/<workstation>/areas.md`, take `Levels`, and obey it. WA numbers restart at 01 inside each sub-workstation, so at 3 levels a WA is identified only together with its sub-workstation — always address it that way.

**The depth is locked.** This skill never converts a workstation between 2 and 3 levels. If the user asks for it, refuse and point to `/setup new` (Setup Protocol): the change is drafted as a setup file, executed once, and archived to `setup/done/`.

---

## If action is empty

Describe this skill: its purpose and the actions table from "overview". Do not execute anything.

## If action is "overview" (or unknown)

| Argument | Action |
| :--- | :--- |
| `new WS` | Create a workstation (structure + rules, including the depth choice in advanced tier) |
| `new subWS <workstation>` | Create a sub-workstation. Advanced tier, 3-level workstations only |
| `new area <workstation>[ - <sub>]` | Create a work area — the work unit |
| `new routine <area>` | Create or revise the routine definition (vault `routine.md`) |
| `run <area>` | Execute the routine per its definition and record the run |
| `from project <project>` | Derive a workstation from an existing project |
| `list` | All workstations: areas, cadence, last run |
| `overview` | This table |

If the action was unknown, say so first, then show the table.

---

## If action is "new WS"

1. Ask for anything missing: name and purpose. Derive the kebab-case folder name (Latin alphabet only) and confirm if it differs.
2. **Depth.** Simple tier: 2-level, silently. Advanced tier: **ask for the hierarchy depth (2 or 3 levels)** — show the table above and state plainly that the choice is fixed and can only be changed later through a setup file. Do not default silently.
3. **Creation mode.** Ask how the structure should be built (in simple tier use plain words: "build as we go" vs. "map out all routines now"):
   - **Agile** (default) — create the workstation shell now; sub-workstations and work areas are added incrementally via `new subWS` / `new area` as routines emerge. Continue with the steps below unchanged.
   - **Predictive** — map the full routine landscape upfront: interview for the complete inventory of recurring activities — what is repeated, how the activities group, cadence per activity (accept a pasted list or build it through questions). Analyze it and map it to the hierarchy — 3-level: groups → sub-workstations, activities → WAs; 2-level: activities → WAs; flag groupings that don't fit the fixed depth and propose merges/splits. Present the full proposed tree with final names (kebab-case, acronym and number prefixes per the naming convention) and **wait for approval**. Then scaffold everything in one pass: all registry rows allocated in order, all folders, all vault mirror nodes (`runs.md` per WA, purpose seeded from the inventory). Routine definitions are **not** written in bulk — after scaffolding, offer `new routine` area by area.
4. Derive a workstation **acronym** (2 uppercase letters). Confirm it with the user and check it is **globally unique** — scan every `vault/workstations/*/areas.md` (`Acronym:` line) **and** every `vault/projects/*/ids.md` (`Acronym:` line); workstations and projects share one namespace, so folder prefixes never collide across `workstations/` and `projects/`.
5. Create `workstations/<ACR>-<name>/` — the confirmed acronym as an uppercase prefix, then the kebab-case name (e.g. `MK-marketing`) — containing only `CLAUDE.md` — sections: **Identity** (what this workstation is, what routes here — state the depth here too), **Goals** (link to vault goals page), **Work Areas** (table: area, routine, cadence — filled as areas are created), **Rules** (workstation-specific).
6. Vault (same `ACR-` prefix): create `vault/workstations/<ACR>-<name>/` with `goals.md`, `status.md`, and `areas.md` — the registry, the WS analogue of a project's `ids.md`. Frontmatter + [[wiki links]]. The shape follows the depth:

   **2-level** — one counter for work areas:

   ```text
   Acronym: **MK**
   Levels: **2**
   Next area: **01**

   | AA | Work area (folder) | Next output |
   | -- | ------------------ | ----------- |
   ```

   **3-level** — a sub-workstation counter, plus one area counter per sub-workstation:

   ```text
   Acronym: **MK**
   Levels: **3**
   Next sub-workstation: **01**

   | SS | Sub-workstation | Next area |
   | -- | --------------- | --------- |

   | ID | Work area (folder path) | Next output |
   | -- | ----------------------- | ----------- |
   ```

   `Next output` is the running number in produced filenames (Output Hygiene & Naming); it starts at `001` in every new work area. There are no task IDs on the workstation side.

7. Add a routing map row to root CLAUDE.md (using the prefixed folder name).
8. Suggest the next structural step — agile mode: a sub-workstation for 3-level workstations, the first work area for 2-level ones; predictive mode: the structure already exists — offer `new routine` for the first area instead.

---

## If action is "new subWS"

1. Simple tier: explain that sub-workstations belong to advanced mode and offer `/axiom tier advanced`. Do not create anything.
2. Check $ARGUMENTS: workstation name required; if missing or unknown, list workstations and ask.
3. **Check the depth.** Read `Levels` from `vault/workstations/<workstation>/areas.md`. If the workstation is **2-level**, refuse: it has no sub-workstations. Offer the two legitimate paths — create a work area directly under the workstation, or convert to 3 levels via `/setup new`. Never create it anyway.
4. Ask for anything missing: sub-workstation name (kebab-case) and purpose.
5. Allocate the number **first** (the folder is named after it): read `Next sub-workstation` from `areas.md`, use it as `SS`, add its row (number, name, `Next area: 01`), bump the counter (monotonic, never reused).
6. Create `workstations/<workstation>/<SS>-<sub>/` — pure structure, no CLAUDE.md, no resources/outputs.
7. Vault: create `vault/workstations/<workstation>/<SS>-<sub>/` with `goals.md`. Update the workstation CLAUDE.md **Work Areas** table.
8. Suggest creating the first work area inside it.

---

## If action is "new area"

1. Check $ARGUMENTS and read `Levels` from `areas.md`. Workstation required; if missing or unknown, list workstations and ask. Then check the form against the depth:
   - **3-level, no sub-workstation given** → refuse. Every WA must live in one. List the sub-workstations and ask which, or offer `new subWS` first.
   - **2-level, a sub-workstation given** → refuse. The area goes directly under the workstation.
2. Ask for the area name (kebab-case) and purpose.
3. Ask: are runs dated? (If yes, each run reads from / writes to `YYYY-MM-DD/` subfolders.)
4. Allocate the area number **first** (the folder is named after it), from the counter that matches the depth:
   - **2-level**: read `Next area` from `areas.md`, use it as `AA`, add the row (`Next output: 001`), bump `Next area`.
   - **3-level**: read `Next area` from the **owning sub-workstation's row**, use it as `AA`, add the area row (ID `<SS>-<AA>`, folder path, `Next output: 001`), bump that sub-workstation's `Next area`. Area numbers restart at 01 in every sub-workstation.

   Numbers are monotonic and never reused. Create `workstations/<workstation>/[<SS>-<sub>/]<AA>-<area>/` with `resources/` and `outputs/`.
5. Vault: create `vault/workstations/<workstation>/[<SS>-<sub>/]<AA>-<area>/` — same numbered folder — with `runs.md` (empty history). Update the workstation CLAUDE.md **Work Areas** table.
6. Offer to continue with `new routine` — without a routine, `run` has nothing to execute.

---

## If action is "new routine"

Creates or revises the routine definition for a work area. Nothing is executed here. A work area holds exactly **one** routine — the routine is a document inside the WA, not a level of its own.

1. Check $ARGUMENTS: the work area, addressed per the workstation's depth (`<ws> - <area>` at 2 levels, `<ws> - <sub> - <area>` at 3); resolve or ask.
2. Interview, one block at a time, only what is open:
   - What are the steps? (concrete, numbered — tools, sources, checks)
   - Cadence: how often, triggered by user or by schedule later?
   - Parameters: what varies per run?
   - Expected outputs: what is produced, format, where?
   - Comparisons: what should each run be compared against (previous run, baseline, threshold)?
3. Write `vault/workstations/<workstation>/[<SS>-<sub>/]<AA>-<area>/routine.md`: frontmatter + sections Definition, Steps, Cadence, Parameters, Outputs, Comparisons.
4. If revising an existing routine.md: show the diff, get approval, keep a change note in the file.

---

## If action is "run"

1. Check $ARGUMENTS: the work area, addressed per the depth; resolve or ask. If no `routine.md` exists: suggest `new routine` first.
2. **Prepare.** Read `routine.md` and the recent entries of `runs.md`. If runs are dated: create `outputs/YYYY-MM-DD/` (and read `resources/YYYY-MM-DD/` if inputs are dated); else use the folders directly. The dated folder is the one place a date belongs — files inside it still follow the naming rule (`<acr>-<address>-<NNN>-<name>`, number from the area's `Next output`), never a date prefix.
3. **Execute** the steps as defined. Ask only when a parameter is undefined.
4. **Compare** against previous runs per the Comparisons section (trends, anomalies).
5. **Record:**
   - Append to `runs.md`: date, parameters, result summary, anomalies, link to output folder.
   - Promote durable insights to `vault/knowledge/` pages, cross-linked from the run entry.
   - Update workstation `status.md`.
6. **Improve.** If the run revealed a better way, propose a change to `routine.md` — apply only with user approval.

---

## If action is "from project"

1. Check $ARGUMENTS: project name; resolve against `projects/` or ask.
2. Clarify: which activity of the project becomes the routine? What carries over?
3. Execute "new WS" — the depth is asked fresh (advanced tier), not inherited from the origin project, and it gets its **own** acronym (globally unique, so it cannot reuse the origin project's). Then "new area" (and "new subWS" first if 3-level) and "new routine", using the project's vault knowledge (goals, decisions, WP outputs) as input.
4. Cross-link: workstation vault pages reference the origin project's pages. The project itself is not modified or deleted.

---

## If action is "list"

Table: workstation | depth | work areas (with sub-workstation where 3-level) | cadence (from routine.md) | last run (from runs.md) | status note.

---

## After any action

- Append to `vault/log.md`, update `vault/index.md` if pages changed.
- Report the created/changed structure as a tree (structure actions) or the run summary (run).

## Notes

- Never create resources/ or outputs/ outside a work area.
- `routine.md` is procedural memory, `runs.md` episodic, promoted insights semantic (vault/knowledge/). Do not bury durable knowledge in runs.md.
- Workstations are independent of projects; "from project" copies knowledge, never moves it.
- The **workstation folder itself carries the acronym prefix** — `<ACR>-<name>` (e.g. `MK-marketing`), in `workstations/` and in the vault mirror. The acronym lives in the workstation's `areas.md` and is globally unique across projects and workstations. In the actions above, `<workstation>` means the acronym-prefixed folder name. Only the name part may later be renamed — the acronym prefix is fixed.
- Sub-workstation folders carry the `SS-` number prefix, work-area folders the `AA-` prefix, both nested inside the acronym-prefixed workstation folder in `workstations/` and in the vault mirror. Only the name part may later be renamed; the prefixes are fixed, and a freed number is never reused.
- **In a 3-level workstation, area numbers are not unique on their own** (each sub-workstation restarts at 01). Always address a WA together with its sub-workstation.
- There are no tasks and no task IDs on the workstation side — that protocol is project-only.
- All created folder and file names follow the Latin-alphabet kebab-case convention (root CLAUDE.md, Output Hygiene & Naming); the uppercase acronym prefix is the one exception, alongside the numeric `SS-`/`AA-` prefixes.
