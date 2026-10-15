---
name: git-release-workflow
description: >
  Automated git versioning and release workflow for Node.js/TypeScript repositories.
  Use this skill whenever the user wants to set up automated releases, configure semantic-release,
  create conventional commits, manage changelogs, or establish a CI/CD release pipeline on GitHub.
  Also triggers for questions about commitlint, Husky, semantic versioning, or commit message
  formatting in any project context — even if the user doesn't mention "release" or "CI/CD" explicitly.
  This skill provides two ready-to-use Claude Code slash commands that work together as a complete workflow.
---

# Git Release Workflow

A complete automated versioning and release pipeline for Node.js/TypeScript repositories,
built around **Conventional Commits**, **semantic-release**, and **GitHub Actions**.

## What This Skill Provides

Two Claude Code slash commands that work together:

| Command | Purpose | When to run |
|---------|---------|-------------|
| `/setup-release` | One-time repo configuration | Once per repository |
| `/commit` | Daily commit + push workflow | Every commit |

## How the Pipeline Works

```
dev writes code
  → /commit: lint → split by concern → conventional commit → push
    → GitHub Actions: semantic-release analyzes commits
      → bumps version → creates tag → generates changelog → publishes GitHub Release
```

Versioning is fully automatic. No manual version bumps or changelog edits ever.

## Version Bump Rules

| Commit type | Bump | Example |
|-------------|------|---------|
| `fix:` | patch | `1.0.0` → `1.0.1` |
| `feat:` | minor | `1.0.1` → `1.1.0` |
| `feat!:` or `BREAKING CHANGE` | major | `1.1.0` → `2.0.0` |

If a push to `main` contains no `feat` or `fix` commits since the last release, no release is created.

## Command Reference

Both commands are bundled in `commands/`. Read the relevant file before executing:

- **`commands/setup-release.md`** — full instructions for `/setup-release`
- **`commands/commit.md`** — full instructions for `/commit`

### When to read which file

- User runs `/setup-release` or asks to configure a repo → read `commands/setup-release.md`
- User runs `/commit` or asks to commit/push → read `commands/commit.md`
- User asks how the pipeline works or what to set up first → explain the overview above, then suggest `/setup-release`

## Compatibility

- **Package managers:** pnpm (preferred), npm
- **CI:** GitHub Actions
- **Node.js:** 18+
- **Yarn:** not supported — instruct the user to configure manually if detected

## Key Constraints (enforce always)

- Commit descriptions follow **the user's language** (detected from conversation), not English
- `type(scope):` prefix is always in English; scope names match codebase conventions
- No emojis, no signatures, no trailers in any commit message
- `wip` is not a valid commit type
- Never bump versions or edit `CHANGELOG.md` manually
- Never push before all local commits are finalized
