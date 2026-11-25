---
name: matilha-pack
description: Use when user wants to extract reusable artifacts from this project into a pack — skills, templates, methodology pages, companion opportunities for future projects.
category: matilha
version: "1.0.0"
optional_companions: []
---

## When this fires

Project/milestone complete AND user wants to reuse learnings. Produces a scaffold for a new pack in `packs/<pack-name>/` or an update to an existing pack.

## Preconditions

- `project-status.md` exists.
- At least one `docs/matilha/den/*.md` exists.

## Execution Workflow

1. Read den files via Glob + Read.
2. Prompt user for pack destination (new pack name, or "extend existing").
3. Scaffold pack skeleton following `docs/matilha/pack-authors.md` — create `packs/<name>/` dir with `.claude-plugin/plugin.json`, `skills/`, `README.md`, `CHANGELOG.md`, `LICENSE`.
4. Copy relevant den content into skills within the pack (one skill per coherent den topic).
5. Generate pack's `plugin.json` with `matilha-pack` keyword.
6. Emit final message: "Pack scaffolded at <path>. Follow docs/matilha/pack-authors.md to publish."

## Rules: Do

- Scaffold independently (don't modify matilha core).
- Preserve citation wikilinks from den files in pack skills.
- Follow `pack-authors.md` strictly.

## Rules: Don't

- Bundle secrets or project-specific data into reusable pack.
- Duplicate matilha core skills.

## Expected Behavior

User gets a new pack repo scaffolded locally. Tests + publish are user's own responsibility.

## Quality Gates

- Pack directory exists with valid `plugin.json`.
- At least one skill in `pack/skills/`.
- `matilha-pack` keyword in keywords array.

## Companion Integration

No companion integrations in Wave 4a.

## Output Artifacts

- `packs/<pack-name>/` directory with `.claude-plugin/plugin.json`, `skills/`, `README.md`.

## Example Constraint Language

- Use "must" for: `plugin.json` includes `matilha-pack` keyword.
- Use "should" for: cite den source wikilinks in pack skills.
- Use "may" for: scaffold multiple pack skills from a single den file.

## Troubleshooting

- **"no den files"**: Run `/matilha-den` first to distill knowledge.
- **"pack name collision"**: Pick an unclaimed prefix (check `docs/matilha/naming-conventions.md`).

## CLI shortcut (optional)

> `matilha pack <name>` (future CLI command; not shipped yet).
