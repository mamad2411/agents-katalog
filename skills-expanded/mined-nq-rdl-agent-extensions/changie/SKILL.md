---
name: changie
license: CC-BY-4.0
description: >-
  Changelog fragments with Changie. Use when writing a changelog entry, adding a
  change fragment under `.changes/`, recording what shipped, or checking that
  fragments follow the project's `.changie.yaml` (kinds, length cap) and Keep a
  Changelog voice. Covers non-interactive `changie new`, shell-safe bodies,
  issue links and hand-edited fragments.
compatibility: >-
  changie 1.x (tested 1.26.0, 2026-09-29).
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Changie

Write one fragment per logical change, in release-note voice, with the kinds
and limits the project's `.changie.yaml` defines.

## Read the project's config first

- **Kinds** are the `kinds[].label` values in `.changie.yaml`, matched exactly.
  `changie init` creates the six Keep a Changelog kinds (`Added`, `Changed`,
  `Deprecated`, `Removed`, `Fixed`, `Security`), but projects rename or replace
  them; `changie new` rejects others (`invalid kind`). Each kind's `auto:` bump
  matters only to `changie batch auto`.
- **Length:** `body.maxLength`, if set, is a hard cap. The issue reference
  counts toward it.
- Match the style of existing fragments in `.changes/unreleased/` and recent
  `.changes/<version>.md` files when they differ from the defaults below.

## Create the fragment

```bash
changie new --interactive=false --kind Added \
  --body 'New `report --json` flag prints machine-readable output (#12)'
```

- `--interactive=false` makes a missing value fail instead of waiting for a
  prompt. `--dry-run` prints the fragment without writing it.
- **Quote bodies containing backticks with single quotes.** In double quotes the
  shell runs the backticked text as a command and splices its output into the
  body. For a body with both backticks and an apostrophe, use `$'…'` and escape
  the apostrophe as `\'`.
- Run `changie new` once per change. Split a body that joins two changes with
  "also" or "and".

## Write the body

- Lead with what a user can now do or what was fixed, not how it was built:
  ``New `changie` skill writes fragments non-interactively``, not
  `Added changie skill with SKILL.md and references dir`.
- Present tense and active voice (`Adds`, `Fixes`, `Removes`, or noun-first
  ``New `foo` ``); backticks around commands, flags, files and identifiers;
  ` — ` (space, em dash, space) to add the "so what".
- Append `(#NNN)` for the issue or PR; read it with `gh issue view NNN` first.
  GitHub links bare `#NNN` references.
- Leave root cause, helper names and mechanics to the commit or PR.
- **No trailing period** (house style): bodies render as `* <body>` bullets.
  No tool enforces this, so follow the project's existing fragments if they
  differ.

## Hand-edited fragments

A fragment is YAML (`kind`, `body`, `time`). Editing one directly bypasses the
checks in `changie new`:

- Quote the body when it contains `: ` or starts with a backtick or another
  YAML indicator. An unquoted `body: uses effort: high` fails to parse.
- `changie batch <version> --dry-run` (for example `batch major --dry-run`)
  catches invalid YAML and unknown kinds but **not** `body.maxLength`; check the
  length yourself or use the project's own linter.

## Releases

Run `changie batch` and `changie merge` only when the user asks for a release,
and follow the project's release process (many batch in CI from an explicit
version). `changie batch v0.2.0` keeps the `v` and writes `.changes/v0.2.0.md`;
use whatever naming the existing `.changes/<version>.md` files use.

## References

- [references/keep-a-changelog.rst](references/keep-a-changelog.rst): what
  belongs in a changelog and what does not.
- [references/ci-integration.rst](references/ci-integration.rst): validating
  fragments in CI with `changie-action`.
