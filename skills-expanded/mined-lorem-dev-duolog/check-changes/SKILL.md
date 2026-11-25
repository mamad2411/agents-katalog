---
name: check-changes
description: Use when the user asks to write, update or check the changelog or
  CHANGES.md, or before bumping the version. Do not use to set the version;
  bump-version does that. Do not use to read past release notes aloud.
compatibility: Requires uv and git. Run from the duolog repository.
---

# Check the changelog

## Communication

- Reply in the language the user writes in.
- Write files, comments and reports in English, ASCII only.
- Use simple English: short sentences, common words, simple grammar.

## Models

- The current model does all of it. Deciding what a user would notice takes
  judgement, so prefer `opus` on Claude or `gpt-6.1-sol` on Codex, high effort. If a
  model is not available, use the current one.

## Before you start

- Run `uv --version`. If it fails, stop and ask the user to install uv:
  https://docs.astral.sh/uv/getting-started/installation/
- A sandbox can stop uv from writing its cache. If a later `uv run` reports that,
  set the variable `UV_CACHE_DIR` to `.cache/uv`, which git ignores, and run it
  again. Do not call Python directly, and do not check the limits by hand instead.

## Steps

1. Read the comment at the top of `CHANGES.md`. Its rules decide what goes in.

1. Find the last release: the newest commit whose message starts with `release:`,
   or the newest `v*` tag. List the commits since then:

   ```sh
   git log --oneline <last release>..HEAD
   ```

1. For each commit, decide if a user would notice it. A fix needs an entry only if
   a released version had the bug: check that before you report a gap.

1. Compare with `## Development`. Report what is missing, and any entry for
   something that no longer exists. Add or correct entries if the user asked for
   that. Merge related entries instead of adding a long one.

1. Run the check. It enforces the limits:

   ```sh
   uv run scripts/version/version.py check
   ```

   Example of a failure: `CHANGES.md:51: bullet has 170 characters, the limit is 160`.
   Shorten the entry or link to the docs. Never change a limit to make an entry fit.

## Done when

- `version.py check` exits with 0, and every commit that a user would notice has an
  entry in `## Development`.
