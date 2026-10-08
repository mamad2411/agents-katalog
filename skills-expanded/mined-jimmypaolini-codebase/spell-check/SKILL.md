---
name: spell-check
description: Run and triage cspell in this codebase. Use when spell-check fails in lint-staged, nx affected, or nx run-many, when cspell reports Unknown word entries, or when adding domain vocabulary to the correct dictionary under configuration/.cspell. Covers full-workspace checks, project-targeted checks, and dictionary update validation.
license: MIT
---

# Spell Check

Use this skill to run cspell consistently in this codebase and fix failures by updating the correct dictionary files.

## When to Use This Skill

- `nx run-many --target=spell-check` fails.
- `nx affected --target=spell-check` fails in CI or pre-commit workflows.
- `Unknown word (...)` appears in `last-lint-staged-output.log`.
- You need to add approved vocabulary (Latin terms, project acronyms, Postgres catalog columns, etc.) to cspell dictionaries.

## Repository-Specific CSpell Configuration

- Main config file: `configuration/cspell.config.yaml`
- Dictionary folder: `configuration/.cspell/`
- Active custom dictionaries:
  - `configuration/.cspell/lexico.txt`
  - `configuration/.cspell/affirmations.txt`
  - `configuration/.cspell/ai.txt`
  - `configuration/.cspell/astronomy.txt`
  - `configuration/.cspell/ics.txt`
  - `configuration/.cspell/infrastructure.txt`
  - `configuration/.cspell/nasa-horizons.txt`
  - `configuration/.cspell/python.txt`
  - `configuration/.cspell/tooling.txt`

Important: In this repository, use `configuration/.cspell/*` as the source of truth for dictionary updates.

## Workflow

### 1. Reproduce

Run full spell-check across projects:

```bash
pnpm exec nx run-many --target=spell-check
```

For focused checks, run one project:

```bash
pnpm exec nx run <project>:spell-check
```

Or run directly on specific files with the repository config:

```bash
pnpm exec cspell --config configuration/cspell.config.yaml --no-progress <file1> <file2>
```

### 2. Extract Unknown Words

If output is large, collect just unknown words:

```bash
rg -o "Unknown word \([^)]*\)" <log-file> \
  | sed -E 's/Unknown word \((.*)\)/\1/' \
  | sort -u
```

Use the exact casing reported by cspell when adding dictionary words.

### 3. Choose the Correct Dictionary

Select dictionary by domain:

- Lexico, Latin, lexico-ingestion, lexico-entities: `configuration/.cspell/lexico.txt`
- Astronomy or caelundas domain terms: `configuration/.cspell/astronomy.txt`
- Infrastructure/Kubernetes/Terraform terms: `configuration/.cspell/infrastructure.txt`
- Python toolchain terms: `configuration/.cspell/python.txt`
- Generic build/dev tooling terms: `configuration/.cspell/tooling.txt`

When in doubt for Lexico-family projects, prefer `configuration/.cspell/lexico.txt`.

### 3.1 Break Out a New Dictionary File

Create a new dictionary `.txt` file only when vocabulary is clearly domain-bounded and continuing to use an existing file would reduce maintainability.

Use this decision rule:

- Keep using an existing dictionary when:
  - The words are one-off additions or small batches.
  - The terms fit naturally in an existing domain dictionary.
- Create a new dictionary file when all are true:
  - At least one stable domain/team boundary exists (for example, a new app, subsystem, or external dataset family).
  - Expected volume is sustained (roughly 30+ domain terms now, or recurring additions over multiple PRs).
  - Ownership is clear (a specific project/team can curate it).
  - Reuse in other domains would be low.

If you create a new dictionary:

1. Add `configuration/.cspell/<new-domain>.txt`.
1. Register it in `configuration/cspell.config.yaml` under `dictionaryDefinitions`.
1. Add it to the `dictionaries` list in the same config.
1. Re-run:

```bash
pnpm exec nx run-many --target=spell-check
```

Editing a skill doc needs no synchronization run of its own — the command that regenerated a skills table of contents was retired with the table. The one exception is the generated types and scopes tables that several skill docs carry between marker comments: those come from [configuration/conventional.config.cjs](../../../configuration/conventional.config.cjs), so if a word landed inside one, change the config and regenerate rather than editing the table.

```bash
pnpm exec nx run synchronization:conventional-config:write
pnpm exec nx run synchronization:conventional-config:check
```

### 4. Add Words Safely

- Add only validated domain words, not typos.
- Keep one word per line.
- Preserve existing file style and ordering conventions used in that dictionary.
- Avoid adding broad or ambiguous words unless necessary.

### 5. Validate

Re-run the exact failing scope first, then the full target:

```bash
pnpm exec nx run <project>:spell-check
pnpm exec nx run-many --target=spell-check
```

Success criteria:

- No `Unknown word` errors remain.
- `nx run-many --target=spell-check` succeeds for all projects.

## Troubleshooting

- Config not picked up:
  - Always pass `--config configuration/cspell.config.yaml` when invoking cspell directly.
- Wrong dictionary edited:
  - Confirm dictionary paths in `configuration/cspell.config.yaml` under `dictionaryDefinitions`.
- Large output is truncated:
  - Pipe output to a file and post-process unknown words with `rg` and `sed`.
- Case-sensitive failures:
  - Add the exact capitalization that appears in source, or both variants if needed.

## Completion Checklist

- Reproduced the failure with Nx spell-check.
- Added only necessary words to the correct `configuration/.cspell/*.txt` file.
- Re-validated project-level spell-check (if applicable).
- Re-validated full workspace spell-check successfully.
