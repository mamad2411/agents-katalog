---
name: gh-aw-compile
description: >-
  Regenerate and post-process all agentic workflows.
  You MUST load this skill when gh-aw is updated, workflow .md files change,
  or when asked to recompile/regenerate workflows.
license: MIT
---

# Recompile Agentic Workflows

Use this skill when you need to regenerate all agentic workflow lock files and verify them.

## IMPORTANT: Verification is required after EVERY lock file change

Any time `.lock.yml` files are regenerated — whether via `gh aw compile`, `gh aw upgrade`, or any other gh-aw
command — you MUST run the repo-standard pre-commit hooks afterward. This is not optional.

## WHEN TO USE

- When you have modified a `.md` GitHub Agentic Workflow file and need to update its `.lock.yml` GitHub Actions file.
- After running `gh aw upgrade` to ensure the repository has the latest action definitions.
- When prompted by the system or another workflow to validate the schema of an agentic workflow.

## WHEN NOT TO USE

- When editing generic GitHub Actions workflows (`.github/workflows/*.yml`) that are not managed by `gh-aw`.
- For compiling application source code (e.g., C++, Java, or TypeScript).
- If you lack write permissions to the repository's `.github/` directory.

## Common Pitfalls

- **Forgetting Pre-Commit**: Compiling the workflow but failing to run `pre-commit run --all-files`, leaving the
  repository in a lint-failed state.
- **Ignoring Validation Errors**: Running `gh aw compile` but missing the schema validation warnings in the output,
  resulting in broken agent features.
- **Direct YAML Edits**: Trying to manually fix the `.lock.yml` file instead of editing the `.md` source and running
  the compile command.

## Steps

### 1. Compile or upgrade workflows

Use whichever command is appropriate:

```bash
# Full upgrade (updates agents, actions, codemods, then compiles)
gh aw upgrade

# Just recompile (when only .md workflow files changed)
gh aw compile
```

If any workflow fails to compile (e.g., due to permission violations), fix the `.md` source file and re-run.

### 2. Run verification

After recompiling, run the pre-commit hooks to ensure everything is valid:

```bash
pre-commit run --all-files
```

## Common Issues

### Strict mode violations

When compiling with `--strict` (or if enforced by the version), gh-aw disallows write permissions like `contents: write`,
`issues: write`, etc. Workflows should use `safe-outputs` for write operations and only request
`read` permissions.

### Discussion category warnings

Warnings about "General" vs "general" discussion category casing are non-blocking.

## Verification

After both steps, run `git diff --stat` to review all changed files. Expect changes in:

- `.github/agents/` - Updated agent files
- `.github/aw/actions-lock.json` - Updated action pins
- `.github/workflows/*.lock.yml` - Regenerated lock files
- `.github/workflows/*.md` - If codemods applied fixes

## References

- [Recompile Skill Reference](https://github.com/github/gh-aw-firewall/blob/main/.claude/skills/recompile-workflows/SKILL.md)
