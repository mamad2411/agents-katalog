---
name: validate-code
description: Run the full code quality validation suite for this codebase. Use this skill when you have finished implementing code changes and want to verify they are clean before committing, when told to "validate", "check quality", or "run linting", or before invoking the submit-changes skill. Runs lint-code (format, lint, typecheck, knip, spell-check) using the write configuration to auto-fix what it can, then checks that nothing remains.
license: MIT
---

# Validate Code

Run the codebase's full automated quality suite against your changes **before committing**. This prevents pre-commit hook failures, failed CI jobs, and wasted triage cycles.

## When to Use This Skill

- After finishing implementation of any task — TypeScript, Python, Markdown, YAML, JSON
- Before invoking the [submit-changes skill](../submit-changes/SKILL.md)
- When asked to "validate", "check code quality", "run linting", or "verify changes are clean"
- Anytime you add new dependencies, exports, or files (Knip detects unused ones)

## What `lint-code` Covers

The `lint-code` Nx target hangs every quality tool off `dependsOn`, so one invocation builds one task graph:

| Tool | Purpose | Configuration |
| ---- | ------- | ------------- |
| `oxfmt` + `prettier` | Code formatting | `configuration/oxfmt.config.ts`, `configuration/prettier.config.ts` |
| `eslint` + `oxlint` | Linting (TS/JS) | project `eslint.config.ts`, `configuration/oxlint.config.ts` |
| `ruff` | Format + lint (Python) | `pyproject.toml` |
| `tsc --noEmit` | TypeScript type checking | project `tsconfig.json` → `configuration/tsconfig.base.json` |
| `pyright` + `ty` | Python type checking | `pyproject.toml` |
| `knip` | Unused TS files, exports, deps | `configuration/knip.config.ts` |
| `fallow dead-code` | The same, workspace-wide in one pass | `configuration/fallow.config.jsonc` |
| `vulture` | Unused Python code | `configuration/vulture_whitelist.py` |
| `cspell` | Spell checking | `configuration/cspell.config.yaml` |
| `markdownlint` | Markdown linting | `configuration/.markdownlint-cli2.jsonc` |
| `yamllint` | YAML linting | `configuration/yamllint.yaml` |

## Validation Workflow

### Step 1 — Auto-fix

Run `lint-code` in `write` mode to automatically fix all auto-fixable issues (formatting, linting, unused-code whitelist entries, sync checks):

```bash
pnpm exec nx affected --target=typecheck-code,lint-code,format-code,deprecate-code,guard-code --configuration=write --base=main
```

> For new/untracked files that `nx affected` won't detect, target the relevant project(s) directly:
>
> ```bash
> pnpm exec nx run <project>:typecheck-code,lint-code,format-code,deprecate-code,guard-code --configuration=write
> ```

Review the changes made. If any files were modified, inspect them to ensure the auto-fixes are correct.

### Step 2 — Verify

Run `lint-code` in `check` mode to confirm no issues remain:

```bash
pnpm exec nx affected --target=typecheck-code,lint-code,format-code,deprecate-code,guard-code --configuration=check --base=main
```

**All checks must pass before proceeding.** If any fail, triage each failure:

- **Format/lint**: Fix the reported violations manually, then re-run.
- **Typecheck**: Fix type errors — see [write-typescript skill](../write-typescript/SKILL.md) for patterns.
- **Spell-check**: Either fix the typo, or add the word to the appropriate dictionary in `configuration/.cspell/`.
- **Knip (unused code)**: Remove the unused export/file/dependency, or add an exception in `configuration/knip.config.ts`.
- **Fallow dead-code (unused code)**: The same finding from the other direction — `knip` runs once per workspace, `fallow` once over all of them. The two configurations are kept in step, so fix the code and both pass; if an exception is genuinely warranted, add it to `configuration/fallow.config.jsonc` _and_ its counterpart in `configuration/knip.config.ts`, or the next run of the other tool reports what you just excused. Prefer `overrides` to `ignorePatterns` when suppressing a file: `ignorePatterns` also drops what that file imports out of the module graph, which makes reachable files read as dead.
- **Sync checks**: Run the failing synchronization's own `write` configuration (e.g., `nx run synchronization:conventional-config:write`), or `nx run-many --targets=conformetry-generators,conventional-config,devcontainer-configuration,pull-request-template,skill-exclusions --configuration=write` for every derivation at once.
- **Check skill exclusions**: Add the exclusion lines the failure names to `configuration/.prettierignore`, `configuration/.codometerignore`, and `.gitattributes`. This leaf has no `write` variant.

See [triage-integration](../triage-integration/SKILL.md) for detailed per-tool fix instructions.

### Step 3 — Done

Once both `write` and `check` pass cleanly, code quality is confirmed. Proceed to commit or hand off.

### Step 4 — Coverage Gate (when required)

`lint-code` does not enforce Vitest coverage thresholds. If the task, project, or CI requires a coverage target, run the coverage configuration explicitly after Step 3:

```bash
pnpm exec nx run <project>:vitest --configuration=coverage
```

If the threshold fails by a small margin, prioritize adding targeted tests for uncovered guard branches (`if (!value)`, fallback paths, sparse/undefined handling) instead of broad test rewrites.

### Step 5 — Type Coverage Gate (TypeScript projects with target)

If a touched TypeScript project defines a `type-coverage` target, treat it as a required gate and run it explicitly after Step 3.

```bash
pnpm exec nx run <project>:typecheck
pnpm exec nx run <project>:type-coverage
```

> ✅ **Best practice:** Run `typecheck` and `type-coverage` back-to-back for the same project while stabilizing changes to avoid late iteration loops.

## Common Patterns

### New TypeScript files added

```bash
# Target the specific project since affected may not pick up new files
pnpm exec nx run <project>:typecheck-code,lint-code,format-code,deprecate-code,guard-code --configuration=write
pnpm exec nx run <project>:typecheck-code,lint-code,format-code,deprecate-code,guard-code --configuration=check
```

### Refactor-heavy test changes

```bash
# 1) Auto-fix + quality checks
pnpm exec nx run <project>:typecheck-code,lint-code,format-code,deprecate-code,guard-code --configuration=write
pnpm exec nx run <project>:typecheck-code,lint-code,format-code,deprecate-code,guard-code --configuration=check

# 2) Re-verify coverage gates explicitly
pnpm exec nx run <project>:vitest --configuration=coverage

# 3) If available, enforce type coverage gate too
pnpm exec nx run <project>:typecheck
pnpm exec nx run <project>:type-coverage
```

### New skill added

A skill is one directory, `.agents/skills/<skill-name>/SKILL.md`. `.claude/skills` and `.github/skills` are symlinks to `.agents/skills`, so that one copy already serves both harnesses — there is no second copy to create and no table of contents to regenerate. AGENTS.md deliberately does not list the skills; agents are handed the installed set directly.

The only extra command applies to a skill installed from another repository, which `skills update` records in `skills-lock.json`:

```bash
# Regenerate the exclusion blocks that keep locked skills out of prettier,
# codometer, Linguist, cspell, and markdownlint
pnpm exec nx run synchronization:skill-exclusions:write
```

### AGENTS.md edited

The types and scopes tables in AGENTS.md are generated between marker comments from [configuration/conventional.config.cjs](../../../configuration/conventional.config.cjs). Edit the config, never the table, then regenerate:

```bash
pnpm exec nx run synchronization:conventional-config:write
pnpm exec nx run synchronization:conventional-config:check
```

Everything outside those markers is hand-written and needs no synchronization run.

## Resources

- [triage-integration skill](../triage-integration/SKILL.md) — Detailed per-tool fix instructions for pre-commit failures
- [write-typescript skill](../write-typescript/SKILL.md) — TypeScript strict mode patterns
