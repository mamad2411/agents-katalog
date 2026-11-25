---
name: conventional-commits
license: CC-BY-4.0
description: >-
  Provides guidance on writing commit messages using the Conventional Commits
  specification. Trigger this skill when writing commit messages, generating
  changelogs, or when the user asks about commit message formatting,
  conventional commits, semantic versioning based on commits, or needs to
  categorize a change (e.g., feat vs fix vs chore).
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
  spec_url: https://www.conventionalcommits.org/en/v1.0.0/
---

# Conventional Commits

The Conventional Commits specification is a lightweight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of. This convention dovetails with Semantic Versioning (SemVer), by describing the features, fixes, and breaking changes made in commit messages.

## How commits map to a changie release flow

In projects that record changes as **changie** fragments, commits feed fragments,
not the changelog directly. A commit's type should match the changie `kind` you
create with `changie new` (bumps below are changie's default `auto:` values; check
the project's `.changie.yaml`):

| Commit type | changie kind | SemVer bump (`auto:`) |
|---|---|---|
| `feat:` | `Added` | minor |
| `fix:` | `Fixed` | patch |
| `feat!:` / `BREAKING CHANGE` (remove/rename a plugin, skill, or public path) | `Removed` or `Changed` | **major** |
| Visible change to existing behavior that is not a defect fix | `Changed` | major |
| Behavior-preserving `refactor:`/`perf:`, `docs:`/`chore:`/`ci:`/`test:` | usually **no** fragment | — |

The kind classifies the change; it does not by itself pick the release version.
Changie derives a version from kinds only via `auto` (`changie batch auto`); many release
flows (including a release-prepare workflow that takes an explicit version input)
have the release manager choose it. Follow the project's release docs. If CI
requires a fragment on every PR, a no-fragment change still needs the project's
documented bypass (e.g. a `skip-changelog` label) — a missing fragment does not
pass on its own.

### Calls models get wrong
- A user-visible behavior change with no new feature is `fix:` only if it
  corrects a defect; otherwise it's `feat:` (with `!` if it breaks existing use).
  `refactor:` is for behavior-preserving changes. Don't default to `chore:`.
- Removing or renaming a published plugin/skill is **breaking** (`!` + `Removed`/`Changed` → major), even if "just cleanup."
- A commit that is genuinely two changes → split it; one type per commit.

Spec reference: see `metadata.spec_url` — do not restate it here.
