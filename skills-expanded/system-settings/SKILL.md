---
name: system-settings
description: Housekeeping menu for familiar and the project shell — updating the installation, workspace tidy, project tracks, project closeout, preferences, and optional hooks. Routes to one branch and runs only that one.
disable-model-invocation: true
---

# familiar — System settings

A **menu, not a procedure**. It names the housekeeping operations that maintain familiar and the
project shell rather than doing project work, and hands off to exactly one of them. It reads no
project state itself and writes nothing.

## Context contract

- **Required context:** this menu only
- **Conditional context:** exactly one file under `references/`, only when step 1 selects that branch. The selected branch's own context contract governs from that point; nothing else in `references/` is opened.
- **Excluded context:** `5-System/Memory/`, `4-Trackers/`, `Knowledge`, `Inputs`, other projects, and undeclared extension content — the menu itself opens no project content.
- **Updates:** `nothing`. Every write belongs to the selected branch and is declared in that branch's own contract
- **Capabilities:** file-read. Optional capabilities must degrade as the procedure states.
- **Completion:** One branch is selected, its reference file is loaded, and its procedure runs under its own contract — or the user is told no branch fits and nothing is opened.

## Step 1 — Select the branch

If the user already named one (`/system-settings update`, "tidy the workspace", "close out
this project"), skip the question and go straight to it. Otherwise present these six and ask which:

| Branch | Reference | What it does |
|---|---|---|
| **Update** | `references/update.md` | Bring this project up to a newer release the user downloaded: check versions and schema, run the updater's report, and apply it on a yes. No terminal needed. |
| **Workspace tidy** | `references/tidy-workspace.md` | Survey the workspace for stale drafts and an unstructured knowledge folder, propose a cleanup, act only on what is approved. |
| **Tracks** | `references/tracks.md` | The project's track lifecycle: propose, add, split, merge, retire, or apply tracks to a project running flat. |
| **Project closeout** | `references/project-closeout.md` | Reconcile final state, confirm open obligations, and produce a derived closeout summary. Deletes nothing. |
| **Preferences** | `references/preferences.md` | Show the global (`~/.familiar/`) and project preferences and which wins; set this project's familiar signature, the default signature, or a standing preference, with approval. Writes outside the project only to that one global file. |
| **Hooks** | `references/hooks.md` | List the optional hooks (session titles, guards) a hooks package offers, and install or remove the ones the user picks in this project's host hook file, after a preview and a yes. Writes inside the project only. |

If the request matches none of them, say so and stop. Do not pick the nearest branch, and do not
open a reference file to find out whether it fits — the table above is the whole basis for the
match. Creating a project is **not** on this menu: project identity is established automatically,
by `/project-status` → Check-in's first real run in the project, not through this menu. Registering
the project with the optional fleet hub is not here either: the hub does that itself (`/fleet`).

## Step 2 — Run the selected branch

Load that one reference file. From there its own **Context contract** governs — its Required,
Conditional, Excluded, Updates, Capabilities, and Completion declarations replace this file's, which
covered only the menu. Do not load a second branch. If the work turns out to need one (a tidy that
uncovers untracked work, a closeout that wants a final update), finish the branch you are in, then
tell the user which other branch to run and stop.

## Guardrails

- **Every branch here is user-started.** This skill carries `disable-model-invocation: true`, so a
  route match never opens it and never opens anything under `references/` — `routes.md` Resolution
  rule 3 applies to the menu, which is what keeps it applying to all six branches. Identify the
  branch that fits, tell the user the command, and stop.
- The menu never performs a branch's work itself, never partially applies one, and never substitutes
  a lighter action because a branch looked heavy.
- Nothing under `references/` is a skill. Each is a procedure this menu selects; none is separately
  invocable, and none may be opened without a selection in step 1.
