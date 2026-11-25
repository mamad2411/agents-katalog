---
name: harness-repo-knowledge
description: >-
  Builds a short repo map so agents find the right files instead of wandering.
  Use when the agent explores the whole tree, edits the wrong module, or
  keeps asking where things live.
---

# Harness Repo Knowledge

## What this does for you

- **Faster start** — the agent reads a map, not the entire tree
- **Fewer wrong-folder edits** — “where X lives” is on disk
- **Progressive disclosure** — root map is short; details stay in `docs/`

`harness-instructions` writes the rules. This skill writes the **map** those rules should point to.

Based on Lesson 04 (map, not manual) and the context-engineering pattern (SELECT + progressive disclosure).

## When to use

- Agent lists or greps the whole repo before every change
- Changes land in the wrong package or folder
- New sessions re-discover architecture from scratch
- `AGENTS.md` is already short but the agent still cannot find code
- `harness-diagnose` attributed the failure to the **context** layer

## Inspect first

Infer the map from the repo. Do not invent modules.

1. Top-level directories (skip `node_modules`, `.git`, `dist`, `build`)
2. Package manifests (`package.json` workspaces, `pyproject.toml`, `go.mod`)
3. Entry points (`scripts/cli.mjs`, `src/main.ts`, `app/`, `cmd/`)
4. Existing docs (`README`, `docs/`, `AGENTS.md`)

Ask only what you cannot infer: which folder is the product vs tooling, and which paths are off-limits.

## Repo map contract

Create `docs/REPO_MAP.md` (or `docs/architecture.md` if that already exists). Keep it **under ~80 lines**.

Required sections:

```markdown
# Repo map

## What this repo is
One sentence.

## Where to look

| If you need… | Open |
|--------------|------|
| CLI entry | `scripts/cli.mjs` |
| Skills | `skills/<name>/SKILL.md` |

## Do not touch (unless the feature says so)
- generated / vendor / lockfile-only paths

## How to load more
- Deep docs: `docs/…` (read only when the feature needs them)
- Do not dump the whole tree into context
```

Template: [templates/repo-map.md](../../templates/repo-map.md)

## Progressive disclosure

```
Tier 1 (always):  AGENTS.md + feature_list.json + this map
Tier 2 (on skill): SKILL.md body
Tier 3 (on demand): module README, API docs, examples
```

Rules for the agent:

- Read the map **before** a broad `find` / recursive grep
- Search inside the folder the map names
- Do not open every file in a directory “just in case”

## AGENTS.md pointer

Add one line under Structure or Detailed documentation — do not paste the whole map:

```markdown
- Repo map: `docs/REPO_MAP.md` (read before exploring)
```

If `AGENTS.md` is already over ~100 lines, move directory lists into the map instead of growing the root file.

## Workflow

1. Inspect layout and entry points
2. Write or update `docs/REPO_MAP.md` from the template
3. Link it from `AGENTS.md`
4. Remove duplicate tree dumps from `AGENTS.md` / README if they drifted
5. Check: a new agent can name the file to edit for one typical change using only the map

## This skills repo (example)

| If you need… | Open |
|--------------|------|
| CLI | `scripts/cli.mjs` |
| Install / uninstall | `scripts/lib/install-skills.mjs`, `uninstall-skills.mjs` |
| Skill body | `skills/<name>/SKILL.md` |
| Templates | `templates/` |
| Course notes | `references/course/` |

## Anti-patterns

- Pasting `tree` output into `AGENTS.md`
- A 400-line architecture essay nobody opens
- Map that lists every file instead of **jobs → paths**
- Letting the agent explore `node_modules` or `dist`
- Updating the map only in chat

## Related skills

- `harness-instructions` — short rules; this skill is the map they link to
- `harness-diagnose` — context-layer failures (“wrong pattern / wrong folder”)
- `harness-scaffold` — create harness files first if the repo has none
- `harness-environment` — how to *run* the repo; this skill is how to *navigate* it

## Templates

- [templates/repo-map.md](../../templates/repo-map.md)

## Course reference

- Lesson 04: Why a giant instruction file fails
- Context engineering: SELECT, progressive disclosure, JIT loading
