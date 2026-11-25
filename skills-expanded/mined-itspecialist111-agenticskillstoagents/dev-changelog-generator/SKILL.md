# dev/changelog-generator — skill payload

> Machine-readable contract: [`../changelog-generator.manifest.json`](../changelog-generator.manifest.json).

## What this skill does

Reads a git revision range, groups commits by Conventional-Commit type
(`feat`, `fix`, `docs`, `chore`, `refactor`, `perf`, `test`),
de-duplicates by PR reference, and emits a Keep-a-Changelog-formatted
markdown block ready to paste under a new version heading.

Handles squash-merge commits, multi-line commit bodies, and PR refs in
the form `(#123)`.

## When to use it

- A release is being cut and you need a CHANGELOG entry.
- You want a quick "what changed last sprint" digest.

## When **not** to use it

- The repository doesn't follow Conventional Commits — output will be
  mostly the `chore` bucket and not useful.
- You need a *human* release narrative — use this as a first draft and
  edit, don't ship raw.

## Determinism and risk

Determinism: **high** — git history + commit-message regex is fully
deterministic. Risk: **low** — read-only.

## How it composes

Pure leaf skill; chains with any release-orchestration workflow that
needs the markdown to drop into a tag annotation or GitHub release body.
