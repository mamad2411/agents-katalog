---
name: chat-app-handoff-to-repo
description: >
  Convert a Claude chat-app project download into a standards-aligned git repo:
  de-baggage the download, add OpenSSF baseline files, build pyproject from the
  cookiecutter template source of truth, wire pre-commit, and make a signed init
  commit. Use when you have a downloaded chat-app project handoff in the dev tree
  that needs to become a working, org-compliant repository. Triggers on: chat-app
  handoff, chat app download, convert project download to repo, scaffold repo from
  handoff, Zone.Identifier cleanup, standards-align downloaded project.
user-invocable: true
---

# chat-app-handoff-to-repo

Internal skill. Converts a Claude chat-app project download (a handoff folder in
the dev tree) into a working, org-standards-aligned git repository.

The happy-path steps are easy; the value of this skill is the set of non-obvious,
iteration-costing gotchas encoded below. Follow the phases in order, and read each
gotcha before the phase it belongs to.

## Source of truth

The executable source of truth for org tool config is the cookiecutter template,
NOT the prose in global CLAUDE.md:

```
~/dev/cookiecutter-python-template/{{cookiecutter.project_slug}}/
```

Read tool config (pyproject, pre-commit, gitignore) from the rendered template
files there. The prose standards docs lag the template. Concretely: uv (not
Poetry), BasedPyright (not Mypy), and the full PyStrict Ruff `select` list all
live in the template, and should be copied from it rather than reconstructed from
memory.

## Phases

### Phase 1: De-baggage the download

1. **Remove mark-of-the-web files.** Chat-app downloads on Windows carry
   `*:Zone.Identifier` alternate-data-stream files. Delete them:
   `find . -name '*:Zone.Identifier' -delete` (or `*Zone.Identifier*` if the
   colon is escaped on the host filesystem).
2. **Flatten double-nesting.** Downloads frequently arrive double-nested
   (`project/project/...`) with a wrapper dir plus duplicated root files. Confirm
   the real project root (the one with the source package), then move its contents
   up one level and remove the empty wrapper. Reconcile duplicated root files
   (keep the inner, authoritative copies).

### Phase 2: OpenSSF baseline files

Add the required baseline files if absent: `LICENSE`, `SECURITY.md`,
`CONTRIBUTING.md`, `CHANGELOG.md`, `README.md`. Org community-health files may
already satisfy some of these at the org level; per-repo copies are still expected
for a standalone repo.

### Phase 3: pyproject from the template

Build `pyproject.toml` by copying tool config from the cookiecutter template
(see Source of truth above), not from CLAUDE.md prose. Pull the dependency
manager (uv), type checker (BasedPyright), and the complete PyStrict Ruff
`select` list from the rendered template.

**Gotcha A: pin validate-pyproject.** The `validate-pyproject` pre-commit hook
must be pinned to v0.24.1 or newer (SHA `78f5e0f...`). Older versions reject
PEP 735 `[dependency-groups]` and fail the commit.

### Phase 4: pre-commit wiring

Copy `.pre-commit-config.yaml` from the template, then apply these fixes:

**Gotcha B: interrogate passes filenames.** The `interrogate` hook passes
filenames to the tool, which bypasses its config `exclude`. Test files then tank
docstring coverage. Set `pass_filenames: false` and give it explicit paths
(`src scripts`) so it honors the intended scope.

**Gotcha C: Ruff S replaces standalone bandit.** Ruff's `S` rule group covers
what standalone bandit checks. Running both duplicates findings under two separate
suppression configs. Pick Ruff `S`; do not also wire standalone bandit.

**Gotcha D: regenerate the detect-secrets baseline after any rev edit.**
`detect-secrets` flags SHA-pinned hook `rev` values as high-entropy strings. After
editing any pre-commit `rev` (including the validate-pyproject pin in Gotcha A),
regenerate `.secrets.baseline` or the hook fails.

### Phase 5: .gitignore directory skeletons

**Gotcha E: `dir/` blocks `!dir/.gitkeep`.** A bare `dir/` ignore rule blocks the
`!dir/.gitkeep` negation, so empty-directory skeletons are not preserved. Use the
`dir/*` + `!dir/.gitkeep` pattern instead. Watch for conflicting bare `dir/` rules
already present in the template gitignore and replace them.

### Phase 6: docs reconciliation

Reconcile any docs the handoff brought against the repo's docs tree conventions
(frontmatter, no duplicate H1 where the tree's gate requires the title in
frontmatter). Born-compliant beats fix-on-commit.

### Phase 7: git init + signed commit

1. `git init` (if not already a repo).
2. Stage the reconciled tree.
3. Run `pre-commit run --all-files` and resolve until clean.
4. Make a signed initial commit (`git commit -S`), Conventional Commits message.

## Pre-flight verification

Before declaring done, re-read the seven gotchas (A through E plus the two source-of-truth
rules) and confirm each was applied:

- [ ] Zone.Identifier files removed and nesting flattened
- [ ] OpenSSF baseline files present
- [ ] pyproject tool config copied from the template, not reconstructed
- [ ] validate-pyproject pinned to v0.24.1+ (Gotcha A)
- [ ] interrogate uses `pass_filenames: false` + explicit paths (Gotcha B)
- [ ] no standalone bandit alongside Ruff `S` (Gotcha C)
- [ ] detect-secrets baseline regenerated after rev edits (Gotcha D)
- [ ] gitignore uses `dir/*` + `!dir/.gitkeep`, no conflicting bare `dir/` (Gotcha E)
- [ ] `pre-commit run --all-files` clean, signed init commit made
