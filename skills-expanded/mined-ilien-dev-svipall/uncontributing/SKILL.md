---
name: uncontributing
description: Use before opening an issue, creating a branch, committing for a pull request, or writing a pull request title or description in the Svipall repository (ilien-dev/svipall), even when the user only says "open a PR", "send this upstream" or "make a branch". Walks through CONTRIBUTING.md (one change per PR, <type>/ branch names, Conventional Commit titles that decide the version, the short PR format, measured changes, screenshots) and checks the result with .github/scripts/check-pr.cjs.
---

# Contributing to Svipall

`CONTRIBUTING.md` is the source of truth and `.github/repo-rules.json` holds every limit;
this skill is the order to apply them in. If they disagree, follow `CONTRIBUTING.md` and point
out the difference. The check script decides, not this text: run it.

## 1. In scope, and new?

- Svipall lets an AI agent read the web from the operator's own machine: it fetches, crawls and searches pages, gets past anti-bot walls by evading them, never by breaking access controls, and answers captchas locally. If the change does not serve that, say so and stop: it will be rejected.
- Search before writing anything:
  ```
  gh pr list --repo ilien-dev/svipall --state all --search "<keywords>"
  gh issue list --repo ilien-dev/svipall --state all --search "<keywords>"
  ```
  If a PR or issue already covers it, report it to the user instead of duplicating it.

## 2. One thing only

Name the single change in one sentence. If it needs an "and", it is two PRs. Propose the split
to the user and do the first one. Unrelated fixes you notice: mention them, leave them out.

## 3. Measure first

A `feat`, `fix` or `perf` change to what users get goes in only when the numbers show it adds value or
at least that nothing gets worse. Take the reading on `main` before changing code, since
it is lost afterwards. How to measure here:

- A fix: the test that fails on `main` and passes on your branch, and the command that runs just it (`cargo test -p <crate> --test <file>`).
- A change to what a page returns, how often a wall stops it, or how fast it answers: `bench` on `main` and on your branch, run exactly as `bench/baseline/README.md` says. It counts only when the median leaves the previous range; publish the runs that improved nothing too.

If nothing can show the effect, tell the user the change will likely be declined, before doing
the work.

## Branch and title

- Pick the Conventional Commit type that tells the truth: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `style` or `revert`.
- Branch: that type, a slash, 1 to 5 lowercase words joined by hyphens
  (`feat/export-cover-image`). Never `feature/`.
- Title: the same type, at most 72 characters, lowercase after the type, no final period
  (`feat: export the cover image`). It becomes the commit on `main` and decides the
  version: `feat` minor, `fix`/`perf`/`revert` patch, `!` major, the rest none.
- A change to `crates/*/src/**`, `crates/*/Cargo.toml`, `crates/*/build.rs`, `crates/*/models/**`, `crates/*/assets/**`, `Cargo.toml`, `Cargo.lock`, `plugins/**`, `skill/**`, `skills/**`, `integrations/**`, `packaging/npm/**`, `packaging/templates/**`, `tools/**`, `server.json`, `Dockerfile`, `Dockerfile.slim`, `docker-entrypoint.sh`, `install.sh` and `install.ps1` reaches users, so it must be `feat`, `fix`, `perf` or `revert`.
- Never edit a version number or `CHANGELOG.md`: the release workflow writes them.

## Before committing

```
cargo test --workspace
scripts/qc.sh
```

Every command must pass; CI runs them again on the pull request.

Report failures with their output; do not open the PR while one fails.

## Description

Copy `.github/pull_request_template.md` and fill every section, deleting the comments. Plain
sentences: what changed, not how hard it was. No other headings, no summary at the end.

- **What** (280): the one change. **Why** (280): the problem; `Closes #N`.
- **How** (500): the approach and main files. **Risk** (200): what could break, how to undo it.
- **Measurement** (500): `main` → branch, with numbers.
- **Evidence** (300 of text): how you checked it and how the reviewer can, in a minute.
- **Checklist**: tick only what is true; if one is not, say why instead of ticking it.

**Screenshots** are optional. Never take them unasked: ask the user "Do you want screenshots
for this PR?" and take them only on a yes; for a visual change, propose before and after. On a
no, take none. Capture only that window or page (a headless
browser screenshot of the URL, or the window by its handle), never the whole screen. Save them
in a temporary folder, not the repository. GitHub has no API to attach images to a PR: open the
PR, give the user the absolute paths and ask them to drag the files into the description; put
`Screenshots: to be attached.` in Evidence meanwhile.

## Check, then open

```
node .github/scripts/check-pr.cjs --branch <branch> --title "<title>" --body-file <file> --files-from-git main
gh pr create --title "<title>" --body-file <file>
```

Fix every problem the check lists before opening; CI runs the same check as `PR rules`. Do not
merge: every PR needs an approval from someone with write access.
