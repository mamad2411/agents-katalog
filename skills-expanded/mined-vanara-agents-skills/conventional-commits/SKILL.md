---
name: conventional-commits
description: Write Conventional Commits — the type(scope)!: subject + body + footer spec — so history is readable and changelogs and SemVer bumps can be derived automatically. Use when committing, configuring commitlint, designing release tooling, or deciding feat vs fix vs breaking change.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# Conventional Commits

A commit message is the only documentation guaranteed to travel with a change forever. Conventional
Commits turn that prose into a **structured, machine-parseable record**: a tool can read your history and
derive the next version number and a categorized changelog without a human touching either. This skill is
the deep reference for the spec, the trade-offs, and the failure modes. Heavy detail lives in
`references/`; copy-paste config in `examples/`; a runnable linter in `scripts/`.

## Mental model

Every commit answers three questions, and the format maps one-to-one onto them:

| Question | Where it lives |
|---|---|
| What kind of change? | the **type** (`feat`, `fix`, …) |
| Where, narrowly? | the optional **scope** (`feat(auth):`) |
| Does it break callers? | the `!` marker and/or `BREAKING CHANGE:` footer |
| Why, in prose? | the **body** |
| What does it reference/close? | the **footer** (`Refs:`, `Closes:`) |

The header is for machines and scanners; the body is for the next human. Get the header structurally
correct and your release tooling does the rest for free.

## The spec

```
<type>(<optional scope>)<optional !>: <subject>
<blank line>
<optional body — wrapped prose explaining the why, may span paragraphs>
<blank line>
<optional footer(s) — BREAKING CHANGE: …, Refs: #123, Closes: #456, Co-Authored-By: …>
```

Rules that the linter enforces (see `scripts/lint-commit.mjs`):

1. **Type** is required, lowercase, from the allowed set below.
2. **Scope** is optional, in parentheses, a lowercase noun for the affected area (`api`, `auth`, `deps`).
3. **`!`** before the colon flags a breaking change.
4. **Subject** follows `: ` (colon-space), is imperative mood, lowercase, no trailing period, and the
   whole header is **≤ 72 characters** (50 is the ideal — it keeps `git log --oneline` and GitHub from
   truncating).

The full grammar, footer tokens, and revert/merge conventions are in `references/spec.md`.

## Allowed types

| Type | Use for | SemVer impact |
|---|---|---|
| `feat` | a new user-facing feature | **MINOR** |
| `fix` | a bug fix | **PATCH** |
| `docs` | documentation only | none |
| `style` | formatting, whitespace, no code change | none |
| `refactor` | code change that neither fixes a bug nor adds a feature | none |
| `perf` | a performance improvement | PATCH |
| `test` | adding or correcting tests | none |
| `build` | build system or dependencies | none |
| `ci` | CI configuration and scripts | none |
| `chore` | maintenance, no production code change | none |
| `revert` | reverts a previous commit | varies |

Any commit with a `!` or `BREAKING CHANGE:` footer is a **MAJOR** bump, regardless of type. Keep the set
small and team-agreed — inventing per-developer types defeats the automation. See
`references/breaking-changes-semver.md` for the precise type → version mapping.

## Why bother (the automation payoff)

The structure is not bureaucracy — it unlocks tooling you'd otherwise hand-maintain:

- **Automated versioning:** `semantic-release` / Changesets read the commits since the last tag and pick
  MAJOR / MINOR / PATCH from the types. No more "what should this version be?" debates.
- **Generated changelogs:** commits group by type into a categorized `CHANGELOG.md` with links to PRs and
  issues, written from the footers.
- **Scannable history:** filtering by type answers "what features shipped this quarter?" in one command:

```bash
git log --oneline --grep '^feat' v1.4.0..HEAD   # every feature since the last release
git log --oneline --grep 'BREAKING CHANGE'      # every breaking change, ever
```

- **Reviewable diffs:** one logical change per commit means reviewers and `git bisect` operate on
  coherent units instead of tangled mega-commits.

## Scoping commits (one logical change)

A perfect message on a tangled commit is still a bad commit. Each commit should be **one coherent change**
that builds and passes tests on its own — don't mix a refactor with a feature, or a fix with a formatting
sweep. This makes `git revert`, `git bisect`, and cherry-picks surgical instead of all-or-nothing. The
discipline of staging hunks (`git add -p`) to separate concerns is covered in `references/scoping-commits.md`.

## Common pitfalls and failure modes

- **Past tense / capitalized subject** (`Added login`) — the convention is imperative, lowercase: `add
  login`. A useful test: the subject should complete the sentence "If applied, this commit will ___".
- **A scope that's really a type** (`feat(fix):`) — scope is a *place* (`auth`), not a kind of change.
- **Forgotten breaking-change marker** — renaming a public field as a plain `refactor:` ships a MAJOR
  break as a no-bump release and silently breaks downstream consumers. Always add `!` + a `BREAKING
  CHANGE:` footer explaining the migration.
- **Junk-drawer `chore:`** — using `chore` for everything erases the signal. A dependency bump that fixes
  a CVE is a `fix`; a new capability is a `feat`.
- **Header over 72 chars** — it truncates in `git log --oneline`, GitHub, and changelog output. Move
  detail into the body.
- **Mega-commits** ("WIP", "fixes") — unparseable by tooling and impossible to revert cleanly.
- **Enforcing only on the final squash** — if you squash-merge, the *PR title* becomes the commit; lint
  that, not just local commits, or the rule has no teeth.

## When NOT to use / trade-offs

- **Solo throwaway prototypes** — the changelog/versioning payoff is zero; the ceremony is pure overhead.
- **Squash-merge-only teams** — per-commit discipline matters less; instead enforce the convention on PR
  titles via a CI check and let local commits be messy.
- **Non-software repos** (docs sites, infra-as-data) — the type vocabulary often doesn't fit; a lighter
  convention may serve better.
- **The cost:** it adds friction and requires a `commitlint` gate plus team buy-in to stay consistent.
  Half-adopted, it's worse than nothing because the automation can't trust the data. Adopt it fully (with
  the `commit-msg` hook in `examples/commitlint.config.js`) or not at all.

## Files in this package

- `references/spec.md` — full grammar: header, body, footers, revert/merge, FAQ
- `references/breaking-changes-semver.md` — `!` vs `BREAKING CHANGE:` and exact type → SemVer mapping
- `references/scoping-commits.md` — splitting work into atomic commits with `git add -p`
- `examples/commit-examples.md` — annotated good and bad messages across every type
- `examples/commitlint.config.js` — zero-config-friendly commitlint setup + husky `commit-msg` hook
- `scripts/lint-commit.mjs` — runnable Node linter for a commit header, with `--selftest`

Pairs with the `ci-pipeline-design` skill (gate commits in CI), the `changelog-writing` skill (turn the
history into release notes), and the `code-reviewer` agent. See the
[Conventional Commits spec](https://www.conventionalcommits.org/) for the canonical wording.
