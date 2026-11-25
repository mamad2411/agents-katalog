---
name: check-version
description: Use when the user asks whether the duolog version is consistent, what
  version this repository states, or whether a release tag matches it, and before
  cutting a release tag. Do not use to change the version; bump-version does that.
compatibility: Requires uv. Run from the duolog repository.
argument-hint: "[tag]"
arguments: [tag]
---

# Check the version

## Arguments

- `$tag` - a release tag such as `v1.2.3`. It is optional. Without it, the places
  are compared with each other.

## Communication

- Reply in the language the user writes in.
- Write files, comments and reports in English, ASCII only.
- Use simple English: short sentences, common words, simple grammar.

## Models

- The current model does all of it. The script decides, so a small model is enough.

## Before you start

- Run `uv --version`. If it fails, stop and ask the user to install uv:
  https://docs.astral.sh/uv/getting-started/installation/
- A sandbox can stop uv from writing its cache. If a later `uv run` reports that,
  set the variable `UV_CACHE_DIR` to `.cache/uv`, which git ignores, and run it
  again. In a read-only sandbox, say that it needs write access and stop. Do not
  call Python directly, and do not read the files by hand instead.

## Steps

1. Run the check. Add `--tag $tag` only when the user gave a tag.

   ```sh
   uv run scripts/version/version.py check --format json
   ```

1. Read the JSON. `version` is what the repository states, `consistent` is the
   result, and `problems` names each place that is wrong.

1. Report the version and the result in one line. List every problem as it is.

   Example of a pass: `Version 1.0.0: every place agrees.`

   Example of a failure: `Version 1.0.0: plugin/codex/plugin.json states 0.9.0.`

1. If a place is wrong, say that the bump-version skill sets every place. Do not
   edit a file: this skill only reports.

## Done when

- The script ran, and you reported its exit code truthfully: 0 means consistent, 1
  means a place differs, 2 means a wrong call such as a tag with no `v`.
