---
name: project
description: Create and manage the project structure - projects, sub-projects, and work packages (WPs). Actions - new project, new subproject, new WP, overview. Hierarchy depth (2 or 3 levels) is fixed at creation. All work happens in WPs; projects and sub-projects are pure structure.
---

# Task

Execute the requested action: $ARGUMENTS

Calling rule: `/project <action> <arguments>`.

If the requested action is ambiguous or contradictory (matches multiple actions, arguments conflict with the action, or the intent is unclear), do NOT guess: flag the ambiguity and ask for clarification before executing.

Core principle: **work is done at WP level only.** Projects and sub-projects are organizational structure. If the user asks for work on a project or sub-project that has no suitable WP, suggest creating one first.

**Tier check (read `axiom-config.md` first):** in **simple** tier, every project is 2-level — do not ask the depth question, do not mention 3-level structure, and manage numbering/IDs silently (apply them consistently; explain only when asked). In **advanced** tier, follow the depth rules below in full.

---

## Hierarchy depth (advanced tier — read before any action)

Every project is either **2-level** or **3-level** (root CLAUDE.md, Hierarchy Protocol). The depth is chosen when the project is created and recorded in its registry as `Levels: **2**` or `Levels: **3**`.

| Depth | Chain | Sub-projects | Task ID |
| :--- | :--- | :--- | :--- |
| 2-level | Project → WP → Task | Not allowed | `XX-WW-TT` |
| 3-level | Project → Sub-project → WP → Task | Mandatory — every WP lives in one | `XX-SS-WW-TT` |

Before any action other than "new project": read `vault/projects/<project>/ids.md`, take `Levels`, and obey it.

**The depth is locked.** This skill never converts a project between 2 and 3 levels — that renumbers WPs and rewrites every task ID in the project. If the user asks for it, refuse and point to `/setup new` (Setup Protocol): the change is drafted as a setup file, executed once, and archived to `setup/done/`.

---

## If action is empty

Describe this skill: its purpose and the actions table from "overview". Do not execute anything.

## If action is "overview" (or unknown)

Show all options in tabular form:

| Argument | Action |
| :--- | :--- |
| `new project` | Create a new project (all steps, including the depth choice in advanced tier) |
| `new subproject <project>` | Create a sub-project under `<project>`. Advanced tier, 3-level projects only. No project named: ask which one |
| `new WP <project> - <subproject>` | Create a work package inside the sub-project (3-level projects) |
| `new WP <project>` | Create a work package directly under the project (2-level projects) |
| `overview` | This table |

If the action was unknown, say so first, then show the table.

---

## If action is "new project"

1. Ask for anything missing: name and overall goals. Derive the kebab-case folder name (Latin alphabet only — transliterate other scripts) and confirm it if it differs from what the user typed.
2. **Depth.** Simple tier: 2-level, silently. Advanced tier: **ask for the hierarchy depth (2 or 3 levels)** — show the table above and state plainly that the choice is fixed for the project's life and can only be changed later through a setup file. Do not default silently.
3. **Creation mode.** Ask how the structure should be built (in simple tier use plain words: "build as we go" vs. "plan the full structure now from your deliverables"):
   - **Agile** (default) — create the project shell now; sub-projects and WPs are added incrementally via `new subproject` / `new WP` as the work unfolds. Continue with the steps below unchanged.
   - **Predictive** — plan the whole structure upfront from the deliverables. Interview for the **work breakdown structure (WBS)**: the deliverables, their groupings, and known work items (accept a pasted WBS or build it through questions). Analyze it and map it to the hierarchy — 3-level: WBS branches → sub-projects, leaves → WPs; 2-level: leaves → WPs; flag WBS levels that don't fit the fixed depth and propose merges/splits. Present the full proposed tree with final names (kebab-case, acronym and number prefixes per the naming convention) and **wait for approval**. Then scaffold everything in one pass: all registry rows allocated in order, all folders, all vault mirror nodes (`goals.md` per unit, `tasks.md` per WP — WP goals seeded from the WBS deliverable).
4. Derive a project **acronym** (2 uppercase letters, per the Task ID Protocol). Confirm it with the user and check it is **globally unique** — scan every `vault/projects/*/ids.md` (`Acronym:` line) **and** every `vault/workstations/*/areas.md` (`Acronym:` line); projects and workstations share one namespace. The acronym must be globally unique so task IDs are unique and folder prefixes never collide.
5. Create `projects/<ACR>-<name>/` — the confirmed acronym as an uppercase prefix, then the kebab-case name (e.g. `PW-personal-website`) — containing only:
   - `CLAUDE.md` — sums up the rules for this project. Sections: **Identity** (what this project is, what routes here — state the depth here too), **Goals** (link to the vault goals page, no duplication), **Structure** (sub-projects and WPs as they are created), **Workflow** (project-specific rules).
   - No resources/ or outputs/ — those exist only in WPs.
6. Vault (mirrors the structure, same `ACR-` prefix): create `vault/projects/<ACR>-<name>/` with `goals.md`, `status.md`, and `ids.md`. Frontmatter + [[wiki links]]. The registry shape follows the depth:

   **2-level** — one counter for WPs:

   ```text
   Acronym: **PW**
   Levels: **2**
   Next WP: **01**

   | WW | WP (folder) | Next task | Next output |
   | -- | ----------- | --------- | ----------- |
   ```

   **3-level** — a sub-project counter, plus one WP counter per sub-project:

   ```text
   Acronym: **PW**
   Levels: **3**
   Next sub-project: **01**

   | SS | Sub-project | Next WP |
   | -- | ----------- | ------- |

   | ID | WP (folder path) | Next task | Next output |
   | -- | ---------------- | --------- | ----------- |
   ```

   `Next task` counts task IDs (Task ID Protocol), `Next output` the running number in produced filenames (Output Hygiene & Naming). Both start at `01` / `001` in every new WP.

7. Add a routing map row to root CLAUDE.md (using the prefixed folder name).
8. Suggest the next structural step — agile mode: a sub-project for 3-level projects, the first WP for 2-level ones (without a WP no work can be performed in this project); predictive mode: the structure already exists — point to the first WP to start working in instead.
9. If the Todos module (M3) is active: offer a board/task setup for the project (`/todos board <name>` in Notion mode) — offer only, never create it unasked. Best after the first WP exists.

---

## If action is "new subproject `<project>`"

1. Simple tier: explain that sub-projects belong to advanced mode and offer `/axiom tier advanced`. Do not create anything.
2. If no project is named: list existing projects and ask which one. If the named project does not exist: ask (do not create it implicitly).
3. **Check the depth.** Read `Levels` from `vault/projects/<project>/ids.md`. If the project is **2-level**, refuse: a 2-level project has no sub-projects. Offer the two legitimate paths — create a WP directly under the project, or convert the project to 3 levels via `/setup new`. Never create the sub-project anyway.
4. Ask for anything missing: sub-project name (kebab-case) and purpose.
5. Allocate the sub-project number **first** (the folder is named after it): read `Next sub-project` from `ids.md`, use it as this sub-project's `SS`, then add its row (number, name, `Next WP: 01`) and bump `Next sub-project` (monotonic, never reused).
6. Create `projects/<project>/<SS>-<sub>/` directly in the project (no `sub-projects/` wrapper) — pure structure, no CLAUDE.md, no resources/outputs.
7. Vault: create `vault/projects/<project>/<SS>-<sub>/` with `goals.md`. Update the project CLAUDE.md **Structure** section.
8. Suggest creating the first WP inside it.

---

## If action is "new WP `<project> - <subproject>`" or "new WP `<project>`"

1. Parse $ARGUMENTS and read `Levels` from `vault/projects/<project>/ids.md`. Verify the parents exist; if not, ask instead of creating implicitly. Then check the form against the depth:
   - **3-level, no `- <subproject>` given** → refuse. Every WP must live in a sub-project. List the project's sub-projects and ask which one, or offer `new subproject` first.
   - **2-level, a `- <subproject>` given** → refuse. A 2-level project has no sub-projects; the WP goes directly under the project.
2. Ask for details: WP name (kebab-case) and purpose (one sentence minimum).
3. Allocate the WP number **first** (the folder is named after it), from the counter that matches the depth (Task ID Protocol):
   - **2-level**: read `Next WP` from `ids.md`, use it as `WW`, add the row (number, WP folder, `Next task: 01`, `Next output: 001`), bump `Next WP`.
   - **3-level**: read `Next WP` from the **owning sub-project's row**, use it as `WW`, add the WP row (ID `<SS>-<WW>`, folder path, `Next task: 01`, `Next output: 001`), bump that sub-project's `Next WP`. WP numbers restart at 01 in every sub-project, so they are unique only together with `SS`.
4. Create `<WW>-<wp>/` directly in the owning unit (no `work-packages/` wrapper) with `resources/` and `outputs/` — the `WW` prefix from step 3, two digits, then the kebab-case name (e.g. `02-seo-optimization`). The WP is the smallest unit and the only place work is performed.
5. Vault (mirrored node): `vault/projects/<project>/[<SS>-<sub>/]<WW>-<wp>/` — same numbered folder — with `goals.md` (the purpose) and `tasks.md` (open tasks). New task lines carry the full task ID (`XX-WW-TT` or `XX-SS-WW-TT`) and consume the WP's `Next task` counter.
6. Update the project CLAUDE.md **Structure** section.

---

## After any action

- Append to `vault/log.md`, update `vault/index.md`.
- Report the created/changed structure as a tree.

## Notes

- CLAUDE.md exists at project level only. Sub-projects and WPs are structure, not rule carriers.
- Never create resources/ or outputs/ outside a WP.
- Tasks have no folders: they live in the WP's `tasks.md`.
- The **project folder itself carries the acronym prefix** — `<ACR>-<name>`, in `projects/` and in the vault mirror. In the actions above, `<project>` therefore means the acronym-prefixed folder name. Only the name part may later be renamed — the acronym prefix is fixed for the project's life.
- Sub-project folders carry the `SS-` number prefix, WP folders the `WW-` prefix, both nested inside the acronym-prefixed project folder in `projects/` and in the vault mirror. Only the name part may later be renamed — the prefixes are fixed for the unit's life, and a freed number is never reused.
- **In a 3-level project, WP numbers are not unique on their own** (each sub-project restarts at 01). Always address a WP together with its sub-project — in this skill, in `/todos`, and in conversation.
- Work areas under `workstations/` carry their own `AA-` prefix and workstations their own acronym — different registry, see the `/ws` skill.
- All created folder and file names follow the Latin-alphabet kebab-case convention (root CLAUDE.md, Output Hygiene & Naming); the uppercase acronym prefix is the one exception, alongside the numeric `SS-`/`WW-` prefixes.
