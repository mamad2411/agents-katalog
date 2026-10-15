---
name: using-godot-skills
description: Index and precedence rules for the godot-agent-skills pack, and how it composes with other installed Godot skill packs (GodotPrompter, awesome-gamedev, Randroids-Dojo). Consult when a Godot task could be served by more than one installed skill, when two packs give conflicting API advice, or when you need to know which pack owns a given concern. Use whenever a request involves Godot, GDScript, .tscn or .tres files, game feel, game balance, or planning game development work.
category: router
---

# Using godot-agent-skills

This pack is deliberately small. It covers the things no other Godot skill pack covers, and
delegates everything else. If you are looking for GDScript idiom, node/scene structure,
physics, UI, shaders, audio, export, or optimization, those live in the other installed
packs — see the delegation table below.

## The standing rules do not live here

The rules this pack exists to enforce are injected by hooks on every prompt, not by this
skill. That is deliberate: a router skill only routes if it wins a triggering contest
against every other pack's router, and two of them advertise harder than this one does.

See `hooks/` in the pack root. What it does:

| Hook | Event | Effect |
|---|---|---|
| `godot-context.sh` | `UserPromptSubmit` | Injects the standing rules and the project's actual engine version into every prompt |
| `guard-scene-files.py` | `PreToolUse` | Denies structural `.tscn`/`.tres` edits — ids, `load_steps`, `uid://`, node blocks |
| `require-verify.sh` | `Stop` | Blocks ending the turn while Godot source changed and nothing was verified |
| `verify-baseline.sh` | `SessionStart` | Marks the verification baseline for the session |

If the hooks are not installed, this skill is the fallback and you should apply its rules
by hand. `scripts/install-hooks.sh` wires them into `settings.json`.

## What this pack owns

| The request involves | Load |
|---|---|
| Editing, repairing, or merging `.tscn` / `.tres`, or a broken `uid://` | `godot-scene-surgery` |
| Writing or reviewing GDScript that may carry Godot 3 API | `godot4-api-guard` |
| Running, testing, or claiming something works | `godot-verify` |
| A feature request touching 3+ files | `write-plan` first — a phased plan, then `build-loop` per phase |
| Multi-step implementation | `build-loop` |
| "Critique this", "poke holes in this", "which approach should I take" | `grill-me` |
| A staged changeset before commit, "review this", second opinion | `codex-review` (explicit invocation only) |
| Stopping, resuming, "where are we" | `session-handoff` |
| "Feels floaty / mushy / unresponsive" | `game-feel-review` |
| Progression, currency, upgrades, balance | `loop-and-economy` — plus `grill-me` when a design decision is on the table |

Rows compose — load every skill whose trigger matches, not just the best one. The standing
combo: an economy or progression *design* still being decided loads `loop-and-economy` for the
domain critique **and** `grill-me` to force it to a decision, ideally before `write-plan`
records the outcome.

The first two are the reason this pack exists: across the ~140 skills in the other Godot
packs, none covers scene-file surgery and none covers Godot 3 → 4 translation.

## What this pack delegates

| Concern | Owner |
|---|---|
| GDScript idiom, typing, lifecycle, signals | `godot-gdscript` (awesome-gamedev), `gdscript-patterns` / `gdscript-advanced` (GodotPrompter) |
| Scene tree structure, composition, autoloads | `godot-nodes-scenes`, `scene-organization`, `component-system` |
| Physics, UI, animation, audio, shaders, tilemaps, 3D, multiplayer | the per-topic skills in either pack |
| Performance and profiling | `performance-optimization`, `godot-optimization` |
| Export, CI, distribution | `godot-export` (awesome-gamedev), `export-pipeline` (GodotPrompter) |
| Actually running tests — GdUnit4, PlayGodot, E2E | the `godot` skill (Randroids-Dojo) |

`godot-verify` states the rule; the Randroids skill supplies the machinery. Prefer its
`run_tests.py` / `validate_project.py` over hand-rolled scripts when it is installed.

## Precedence when packs disagree

1. **Engine version wins.** Read `config/features` in `project.godot` before trusting any
   API detail. awesome-gamedev pins Godot 4.7; GodotPrompter targets 4.3+. A skill written
   for a different minor version is advisory, not authoritative, and its API names need
   checking against the project's version.
2. **Scene files and Godot 3 → 4 translation are this pack's call**, because nothing else
   covers them.
3. **Everything technical otherwise defers to the specialist skill**, which is version-pinned
   and more detailed than anything here.
4. **Never resolve a disagreement by picking the more confident-sounding answer.** Check it:
   `godot --version`, or the class reference for the project's exact minor version.

## Categories

Each skill carries a `category:` field. What it tells you is how fast the contents rot:

- **engineering** — engine-specific. Goes stale with releases; check against the project.
- **productivity** — workflow discipline. Engine-agnostic, ages well.
- **design** — game design judgment. Not Godot-specific and largely version-proof.
