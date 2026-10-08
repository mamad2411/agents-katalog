---
name: pm-brain
description: Initialize a PM Brain — a markdown-native second brain for a product operator (PM, product lead, founder, or anyone accountable for one product or initiative) doing judgment-heavy work with scattered inputs. Detects greenfield vs. migration mode, runs a focused interview, copies the deterministic scaffold into the working directory, populates placeholders from interview answers, runs a self-test, and commits. Use when invoked via `/pm-brain` or when the user asks to set up a PM Brain.
---

# PM Brain — Skill

This skill scaffolds and initializes a PM Brain in the current working directory. The scaffold is deterministic (static files copied as-is from `scaffold/`). The reasoning is adaptive (loaded from `prompts/` per phase).

## Architectural split

| Layer | Where it lives | Why |
| --- | --- | --- |
| **Static structure** — schemas, CLAUDE.md, INDEX.md, folder tree, file templates | `scaffold/` | Deterministic. Same every time. No generation needed. |
| **Adaptive reasoning** — mode detection, migration, interview, post-scaffold self-test | `prompts/` | Probabilistic. Depends on what's in the directory and what the PM says. |
| **Orchestration** — when to do what | This file | Glue. |

Behavior evolves independently from structure. Schemas can change without touching reasoning. Reasoning can improve without rewriting schemas.

## When to invoke

- Operator runs `/pm-brain` (or pastes a setup request like "set up a PM Brain here").
- Operator asks to add a PM Brain to an existing directory of PM artifacts.

Do **not** invoke this skill for routine PM Brain operations after init (ingestion, prep, review). Those are handled by the seeded `CLAUDE.md` operating manual in the target repo.

## Workflow

### 1. Detect mode

Load `prompts/mode-detection.md`. Inspect the current working directory. Decide: **greenfield** (empty), **migration** (PM artifacts present), or **active-repo** (working repo — pause and ask).

Announce the detected mode to the operator in one line. For active-repo mode, do not proceed without confirmation.

### 2. If migration mode

Load `prompts/migration.md`. **Copy** (do not move) pre-existing PM artifacts into a `source/` folder. Bulk-ingest with epistemic caution. Record cross-document conflicts for the post-scaffold contradictions block.

### 3. Run the interview

Load `prompts/interview.md`. Ask the 5 batches (greenfield) or only the gaps not covered by source artifacts (migration). Confirm back what you heard before scaffolding.

### 4. Copy the scaffold

Copy **every file and folder** from `scaffold/` into the current working directory — including the hidden `.claude/` directory (hooks + per-brain settings) and dotfiles (`.gitignore`, `.gitkeep`). Preserve structure.

Use the form of copy that picks up dotfiles by default:

- **Bash:** `cp -R scaffold/. <dest>/`  (the trailing `/.` is what makes dotfiles come along)
- **PowerShell:** `Copy-Item -Recurse -Force scaffold\* <dest>\` followed by `Copy-Item -Recurse -Force scaffold\.* <dest>\` (the second pass picks up `.claude/` and `.gitignore`; `Copy-Item -Recurse scaffold\*` alone *will* silently drop them)

After copying, verify the install by listing the destination — `.claude/`, `.gitignore`, and every top-level area folder (`hypotheses/`, `decisions/`, `source/`, `ingestion/`, `knowledge/`, `stakeholders/`, `rules/`, `maintenance/`, `docs/`) must all be present. If `.claude/` is missing the hook won't fire on agent writes and schema violations will go uncaught — re-do the copy.

**Critical rules:**
- Copy in place. The current working directory **is** the project root. Do not create a nested subfolder.
- Preserve `.gitkeep` files in empty folders.
- Preserve `.claude/hooks/validate_brain_file.py` and `.claude/settings.json` exactly as shipped — they're what makes schema enforcement happen in-loop as the agent edits brain files.
- Do not modify scaffold files at the source. If you need to change a template permanently, edit `scaffold/` and re-version the skill.

### 5. Populate placeholders from interview answers

Walk the copied files and substitute interview answers. Use the full **Batch → file mapping** in [`prompts/interview.md § What the answers feed`](./prompts/interview.md) — that table is the canonical destination map. Every Batch answer has a documented home; do not silently drop any.

Highlights:

- `knowledge/strategy.md` — north-star metric, priorities (Batch A). Non-goals start empty if PM didn't volunteer them; flag in next moves.
- `knowledge/product/features/<slug>.md` — one file per active feature (Batch C Q1), populated from the feature schema.
- `knowledge/product/roadmap.md` — Now / Next sections from Batch C.
- `stakeholders/<slug>.md` — one file per stakeholder (Batch B Q1); influence + friction tagged from Batch B Q2.
- `knowledge/org/team.md`, `knowledge/org/rituals.md`, `knowledge/org/tools.md` — from Batch B Q3 + Batch D Q1.
- `knowledge/market/landscape.md` and/or `trends.md` — from Batch D Q3.
- `rules/discovery.md`, `rules/data.md` — from Batch D Q1-2.
- `CLAUDE.md § Operating preferences` — autonomy mode + maintenance cadence (Batch E Q1-2).
- `CLAUDE.md § Off-limits` — Batch E Q3.

For schema-templated files: copy the schema structure as-is, fill in what the interview provided, leave the rest with the placeholder comments intact.

**Provenance:** every populated field should be traceable back to either a Batch question or a source artifact. When a value came from a source artifact, link to it inline.

### 6. Post-scaffold self-test

Load `prompts/post-scaffold.md`. Run:

1. Routing self-test (can you route each of the 4 ingestion modes?).
2. Link verification (walk every internal markdown link, fix broken ones).
3. Surface 3-5 immediate next moves.
4. Surface 1-3 contradictions found during scaffolding (or say explicitly "none found").
5. Print the self-test receipt.

### 7. Commit

- Run `git rev-parse --is-inside-work-tree` in the **current working directory**.
- If already a repo: stage all scaffolded files. Single commit titled `feat: initialize PM brain`.
- If not a repo: `git init` in the current working directory, then stage and commit.
- **Never push remotely.** PM controls publication.
- If any git step fails, surface the error and stop. No destructive recovery.

### 8. Hand off

Lead with the habit loop, not the scaffold. See `prompts/post-scaffold.md § 7` for the exact ordering:

1. The three habit actions (ingest today / prep next 1:1 / `/review` Friday) — specific slug + day.
2. 1-3 contradictions surfaced (or "none found").
3. 2-3 scaffold gaps worth filling.
4. One paragraph on what was built.

Do not lead with a folder map or "your scaffold is ready." Lead with what produces value in the next 24 hours.

Then stop and wait for the operator's first real task.

## Anti-patterns

- **Regenerating scaffold content.** The whole point of `scaffold/` is that it's deterministic. If you find yourself rewriting `CLAUDE.md` or a schema from scratch during init, stop — copy from `scaffold/` instead.
- **Creating a nested `pm-brain/` subfolder.** The current working directory **is** the project root.
- **Skipping the self-test.** Broken links are memory corruption, not cosmetic.
- **Inventing contradictions.** If migration mode found no genuine conflicts, say so. Don't fabricate.
- **Pushing remotely.** PM controls when and where this gets published.

## Files in this skill

```
pm-brain-skill/
├── SKILL.md              # This file. Orchestration.
├── scaffold/             # Deterministic static structure. Copy as-is.
│   ├── .claude/          # Per-brain Claude Code config (hooks + settings)
│   │   ├── hooks/
│   │   │   └── validate_brain_file.py   # PostToolUse schema validator
│   │   ├── commands/     # Slash commands shipped with the brain
│   │   └── settings.json # Wires the hook to Write|Edit
│   ├── .gitignore
│   ├── CLAUDE.md
│   ├── INDEX.md
│   ├── README.md
│   ├── knowledge/        # strategy, product, users, market, org
│   ├── stakeholders/
│   ├── hypotheses/
│   ├── decisions/
│   ├── rules/
│   ├── source/           # Verbatim audit anchors
│   ├── ingestion/        # Synthesized records
│   ├── maintenance/
│   └── docs/
└── prompts/              # Adaptive reasoning. Loaded per phase.
    ├── mode-detection.md
    ├── migration.md
    ├── interview.md
    └── post-scaffold.md
```
