---
name: commit-code
description: Write commit messages following this codebase's Conventional Commits standard with Gitmoji support. Use this skill when creating commits or when asked about commit message formatting.
license: MIT
---

# Commit Message Conventions

This skill teaches how to write commit messages for this codebase. All commits **must** follow these rules to pass pre-commit checks and CI validation.

## Format

```text
<type>(<scope>): <gitmoji> <subject>
```

**Note:** Footer sections are **forbidden** by commitlint configuration. Body is forbidden unless every line is a `Co-authored-by:` trailer added by a coding agent. The casing is not checked — `Co-authored-by:` and `Co-Authored-By:` are the same trailer to git and to GitHub.

### Structure Rules

1. **Header**: `<type>(<scope>): <gitmoji> <subject>` (required)
   - Must start with gitmoji emoji (`gitmoji-required`, error level 2)
   - Max 128 characters (`header-max-length: 128`)
   - Subject must not be empty (`subject-empty: never`)
2. **Body**: Forbidden unless every line is a `Co-authored-by:` trailer, in any casing (`body-co-authored-only`, error level 2)
3. **Footer**: Forbidden (`footer-empty: always`, error level 2)

## Type

**Required.** Must be one of the allowed types defined in [conventional.config.cjs](../../../configuration/conventional.config.cjs) (enforced by `type-enum` rule, error level 2).

**Case:** Must be lowercase (`type-case: lower-case`, error level 2)

<!-- types-start -->

| Type | Description |
| ---- | ----------- |
| `feat` | A new feature or capability that adds value for users |
| `fix` | A bug fix that addresses a specific issue or problem |
| `docs` | Documentation, AGENTS.md, SKILL.md, README, and planning files |
| `test` | Adding or correcting unit, integration, or end-to-end tests |
| `refactor` | Code restructuring that neither fixes a bug nor adds a feature |
| `style` | Formatting, whitespace, or code structure changes with no semantic effect |
| `perf` | A code change that improves performance (caching, query optimization, etc.) |
| `chore` | Housekeeping that doesn't modify src or test files (gitignore, editor config, etc.) |
| `ci` | GitHub Actions workflows, composite actions, and CI/CD scripts |
| `build` | Build system, Vite/Docker/Helm config, or external dependency integration |
| `revert` | Reverts a previous commit |

<!-- types-end -->

### Release Significance

This repository squash-merges pull requests with `PR_TITLE`, so the **pull request title, not any individual commit, is what semantic-release reads**. [release.config.cjs](../../../release.config.cjs)'s `releaseRules` map each type above to a version bump:

| Types                                                                   | Bump              |
| ----------------------------------------------------------------------- | ----------------- |
| A breaking change (`!` after the scope, or a `BREAKING CHANGE:` footer) | `major`           |
| `feat`                                                                  | `minor`           |
| `fix`, `perf`, `refactor`, `build`, `revert`                            | `patch`           |
| `docs`, `style`, `test`, `ci`, `chore`                                  | none — no release |

**Pick the branch's type before its first commit, not after its last.** The [pull-request-release-significance](../../../tools/validation/src/modules/pull-request-release-significance/pull-request-release-significance.command.ts) check fails the pull request if any commit on the branch is more release-significant than the title ends up being — a `feat` commit on a branch titled `chore` or `ci`, for instance — and separately fails if a commit's scope never appears among the title's scopes. Since the type only has to be _at least as_ significant, `fix` commits on a `feat`-titled branch are fine; the reverse is not.

Keeping a branch scoped to one project or module (see the root [AGENTS.md](../../../AGENTS.md#work-scope)) is what keeps this easy to satisfy — the fewer concerns a branch carries, the less likely a later commit outranks the type chosen at the start. If one does, either retitle the pull request to the more significant type, or move that commit to its own branch.

## Scope

**Required.** Must be one of the allowed scopes defined in [conventional.config.cjs](../../../configuration/conventional.config.cjs) (enforced by `scope-enum` rule, error level 2).

**Case:** Must be lowercase (`scope-case: lower-case`, error level 2)

<!-- scopes-start -->

| Scope | Description |
| ----- | ----------- |
| `ic-suite` | In-house code measurement and validation toolchains (Callidescope, Codependix, Codometer, Conformetry) and their shared conventions |
| `affirmations` | Python Jupyter notebook application for LangGraph affirmation generation |
| `caelundas` | Node.js CLI for astronomical calendar generation (NASA JPL ephemeris) |
| `configuration` | Workspace root config files (tsconfig, eslint, vitest, nx.json, etc.) |
| `conformetry` | Code generator templates and validation tests for generated instances |
| `dependencies` | Dependency version changes (upgrades, additions, removals via pnpm) |
| `deployments` | GitHub Actions workflows and CI/CD pipeline configuration |
| `documentation` | Markdown docs, skills, planning files, and AGENTS.md files |
| `infrastructure` | Helm charts, Terraform configs, and Kubernetes resources |
| `JimmyPaolini` | Static GitHub profile README project (markdown and assets) |
| `lexico` | TanStack Start SSR Latin dictionary web app with Supabase backend |
| `lexico-components` | Shared React/shadcn component library |
| `lexico-entities` | Shared TypeORM entities and GraphQL types |
| `lexico-ingestion` | Data ingestion scripts for Lexico |
| `meanderaw` | Greek meander (key/fret) SVG generator CLI and the composable motif/modifier library it reads |
| `sempientor` | Lexical gap discovery CLI that surveys English for morphological, phonotactic, and semantic gaps and coins words to fill them |
| `callidescope` | Call stack tracing and linting CLI, the configuration package it reads, and the packages that build and render its call graph |
| `codependix` | Dependency graph export CLI, the configuration package it reads, and the package that judges the graphs against declared rules |
| `codometer` | Code statistics measurement CLI, the configuration package it reads, and the packages that diff and render its pull request change report |
| `no-release` | Escape hatch: suppress semantic-release for any commit type |
| `release` | Version bumps and release commits generated by semantic-release |
| `reporting` | Pull request change report generation and the packages that diff and render it |
| `scripts` | Shell and TypeScript scripts in scripts/ (sync, setup, utilities) |
| `testing` | Vitest configuration, shared test utilities, and coverage setup |
| `synchronization` | Synchronization application and commands for automating workflows |
| `validation` | Validation CLI and the checks it runs, such as pull request metadata |

<!-- scopes-end -->

### Scope Selection Guidelines

1. **Single project change**: Use project scope (`caelundas`, `lexico`, etc.)
2. **Multiple projects of same type**: Use category scope (`applications`, `packages`)
3. **Workspace config**: Use `configuration`
4. **CI/CD**: Use `deployments`
5. **Docs**: Use `documentation`
6. **Dependencies**: Use `dependencies`

## Subject

**Required.** The subject line must:

- **Start with gitmoji** (`gitmoji-required`, error level 2) - see Gitmoji section below
- Be **lowercase** after the emoji (`subject-case: lower-case`, error level 2)
- Use **imperative mood** (`tense/subject-tense: imperative`, error level 2)
  - ✅ "add feature" ✅ "fix bug" ✅ "update docs"
  - ❌ "added feature" ❌ "fixes bug" ❌ "updating docs"
- Be **under 72 characters** (best practice for readability with emoji)
  - Hard limit is 128 chars total for entire header (`header-max-length: 128`)
  - See **Character Budget** section below for calculating available space
- **Not end with a period** (`subject-full-stop: never`, error level 2)
- **Not be empty** (`subject-empty: never`, error level 2)
- Be **concise and descriptive**
- **Describe ONE logical change** — never list multiple changes with commas or "and"

### Character Budget & Multi-Change Commits

The prefix `type(scope): <gitmoji>` eats into the 128-character header limit. Long scopes like `infrastructure` (~27 characters) or `lexico-components` (~35 characters) leave as few as **93–101 characters** for the subject. Always count the full header.

When a commit touches multiple concerns, **summarize or split** — never list changes with commas/"and":

```text
# ❌ BAD — lists multiple changes with commas/"and"
feat(infrastructure): 🏗 migrate lint-staged configuration to new file, add sync scripts for VS Code extensions and conventional commit scopes

# ✅ Summarize at a higher level
feat(infrastructure): 🏗 add lint-staged config and sync scripts

# ✅ Or split into separate commits
feat(infrastructure): 🏗 migrate lint-staged to standalone config
feat(scripts): ✨ add vscode extension sync script
feat(scripts): ✨ add conventional scopes sync script
```

### Examples

✅ **Good:**

```text
feat(lexico): ✨ add user profile page
fix(caelundas): 🐛 correct aspect angle calculation
docs(codebase): 📝 update nx workspace guide
chore(dependencies): ⬆️ upgrade react to v19
```

❌ **Bad:**

```text
feat(lexico): add user profile page             # Missing gitmoji
feat(lexico): ✨ Added profile page.             # Wrong tense, period
Fix(Caelundas): 🐛 fix bug                       # Wrong case (type)
fix(caelundas): 🐛 Fix bug                       # Wrong case (subject)
docs: 📝 updated docs                            # Missing scope, wrong tense
chore(deps): ⬆️ bump                             # Invalid scope (use 'dependencies')
feat(infrastructure): 🏗 add config, scripts, and sync tools  # Too verbose, lists multiple changes
```

## Gitmoji

**Required.** Must add a gitmoji emoji at the start of the subject line (`gitmoji-required`, error level 2). Use either the emoji glyph or short code.

Format: `<type>(<scope>): <gitmoji> <subject>`

### Common Gitmojis

| Emoji | Code                    | Type         | Meaning                  |
| ----- | ----------------------- | ------------ | ------------------------ |
| ✨    | `:sparkles:`            | `feat`       | Introduce new features   |
| 🐛    | `:bug:`                 | `fix`        | Fix a bug                |
| 📝    | `:memo:`                | `docs`       | Add/update documentation |
| ✅    | `:white_check_mark:`    | `test`       | Add/update tests         |
| ♻️    | `:recycle:`             | `refactor`   | Refactor code            |
| 💄    | `:lipstick:`            | `style`      | UI and style files       |
| 🎨    | `:art:`                 | `style`      | Improve code structure   |
| ⚡️    | `:zap:`                 | `perf`       | Improve performance      |
| 🔧    | `:wrench:`              | `chore`      | Configuration files      |
| 👷    | `:construction_worker:` | `ci`         | CI build system          |
| ⬆️    | `:arrow_up:`            | `chore`      | Upgrade dependencies     |
| 🗃️    | `:card_file_box:`       | `feat`/`fix` | Database changes         |

See [gitmoji.dev](https://gitmoji.dev) for the complete emoji list.

## Body and Footer

**Footer**: Forbidden. Footer sections are not allowed in commit messages in this repository.

**Body**: Forbidden unless every line is a `Co-authored-by:` trailer, in any casing, which coding agents add automatically. Human contributors must not add a body.

If you need to provide:

- **Issue references**: Link the PR to issues in GitHub UI, or use commit description in GitHub
- **Breaking changes**: Prefix subject with 💥 gitmoji
- **Detailed explanations**: Add to PR description instead of commit message

## Full Examples

### Simple Feature

```text
feat(caelundas): ✨ add moon phase calculations
```

### Bug Fix

```text
fix(lexico): 🐛 prevent crash on null user data
```

### Breaking Change

```text
feat(lexico): 💥 migrate to new auth API
```

## Git CLI Usage

### Committing from the Command Line

Since footer sections are forbidden, commits should not include footers. Body must be omitted unless it consists entirely of `Co-authored-by` trailers, whose casing is not checked.

Commits must also be GPG-signed and verified:

```bash
export GPG_TTY="$(tty)"
git commit -S -m "feat(codebase): ✨ add new feature"
git verify-commit HEAD
```

Use `-S` and fail immediately if `git verify-commit HEAD` does not succeed.

> ✅ **Best practice:** Let Husky run signing checks automatically in normal workflows. The pre-commit hook runs `check-commit-signing-configuration.sh` and the pre-push hook runs `check-push-commit-signatures.sh`.
>
> ⚠️ **Warning:** Avoid manually running `scripts/git/check-push-commit-signatures.sh` in routine command-line flows. It is intended for pre-push hook stdin data and may fail or appear to hang when called directly.

### Common Pitfalls

❌ **Avoid:** Using multiple `-m` flags or newlines:

```bash
# This will fail - no body allowed
git commit -m "feat(codebase): ✨ add feature" \
           -m "This is the body paragraph"

# This will also fail
git commit -m "feat(codebase): ✨ add feature
This is the body"
```

### Tips

- Use `git commit --amend` to edit the last commit message
- Test commit messages locally before pushing: `git log --oneline -1`
- Put detailed explanations in the PR description, not the commit message

## Commitlint Rules Summary

All rules defined in [../commitlint.config.ts](../../../configuration/commitlint.config.ts):

**Error (level 2) - Will fail commit:**

- `gitmoji-required`: Must start with valid gitmoji
- `tense/subject-tense`: Must use imperative tense ("add" not "added")
- `type-enum`, `type-case`: Valid lowercase type required
- `scope-enum`, `scope-case`: Valid lowercase scope required
- `subject-case`: Subject must be lowercase
- `subject-full-stop`: No period at end
- `subject-empty`: Subject cannot be empty
- `header-max-length`: Max 128 characters
- `body-co-authored-only`: Body must be empty or contain only `Co-authored-by:` trailers
- `footer-empty`: Footer is forbidden

## Validation

Commit and signing policies are validated by:

1. **Husky pre-commit hook** — Validates signing configuration and staged-file checks before commit
2. **Husky commit-msg hook** — Runs commitlint locally for commit message format
3. **Husky pre-push hook** — Validates branch naming and rejects unsigned or unverifiable commits
4. **GitHub Actions CI** — Validates commits and branch/PR conventions in pull requests

Configuration files:

- [../../../commitlint.config.ts](../../../configuration/commitlint.config.ts) — Complete rules and validation config
- [../../../configuration/.husky/commit-msg](../../../configuration/.husky/commit-msg) — Git hook script

## Quick Reference

```bash
# Basic format
<type>(<scope>): <gitmoji> <subject>    # Required (single line only)

# Rules (all enforced at error level 2)
- Gitmoji: required at start of subject
- Tense: imperative mood (add/fix/update, not added/fixed/updated)
- Type: lowercase, from allowed list
- Scope: lowercase, from allowed list
- Subject: lowercase, imperative, no period, <72 chars
- Header: <128 chars total (count prefix + subject!)
- Signing: commit with `-S`, then verify `HEAD` using `git verify-commit`
- Body: forbidden (only `Co-authored-by` trailers allowed, added automatically by tools)
- Footer: forbidden
- NEVER list multiple changes with commas/"and" — summarize or split commits

# Common patterns
feat(project): ✨ add feature
fix(project): 🐛 fix bug
docs(documentation): 📝 update docs
chore(dependencies): ⬆️ upgrade deps
test(project): ✅ add tests
refactor(project): ♻️ refactor code
```

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Gitmoji Guide](https://gitmoji.dev)
- [commitlint](https://commitlint.js.org/)
- [check-commit-signing-configuration.sh](../../../scripts/git/check-commit-signing-configuration.sh) — Validates signing prerequisites before commit
- [check-push-commit-signatures.sh](../../../scripts/git/check-push-commit-signatures.sh) — Validates pushed commits are signed
