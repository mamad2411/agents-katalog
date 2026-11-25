---
name: release
description: Cut and tag a release — decide the next version and write that release's notes and changelog from all commits since the last tag. Use to cut or prepare a release, tag or bump a version, decide the next version number, or assemble the release notes. Not a single CHANGELOG entry during development, deploy monitoring (deploy-watch), or incident handling (incident-response).
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Release (phase workflow)

The release phase of the SDLC spine: turn the merged work since the last tag into a proposed
**semver version** and a **Keep-a-Changelog** changelog, emit a `release` handoff artifact, and —
only when asked — tag. The deterministic logic lives in the plugin's `bin/af.py`;
this skill wires it to the repo and renders the result. (Design: ADR 0021 and
`docs/architecture/quality-ops.md` in the agentic-forge repository — not shipped with the plugin.)

## When to use

When the task is to cut/prepare a release, write release notes, assemble a changelog from merged
work, or decide the next version. **Not** for adding the per-PR `CHANGELOG` entry while developing
(that is docs discipline), monitoring a rollout (`deploy-watch`), or handling an incident
(`incident-response`).

## Process

The release commands print one JSON object each and need nothing installed:

```
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" release-commits --repo .
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" release-commits --repo . | python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" release-summarize --current <version> --messages-json -
```

1. **Find the current version + the commits.** The current version is the latest tag
   (`git describe --tags --abbrev=0`) or the project manifest (`pyproject.toml` / `package.json`).
   Collect the commit messages since that tag with `release-commits` — or, when you are
   handed an explicit commit list/file, give `release-summarize` those lines as a JSON array of strings
   instead.
2. **Pick the repo's version scheme.** `release-summarize` takes CalVer `<year>.<month>.<inc>`,
   with **today's UTC year/month**, when the current version looks like it; otherwise semver. If the
   repo documents CalVer (agentic-forge itself does, ADR 0055) but the current version does not
   show it, pass it:
   `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" release-commits --repo . | python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" release-summarize --current <version> --scheme calver --messages-json -`.
3. **Summarise.** `release-summarize` returns the proposed `version` (semver: breaking → major,
   `feat` → minor, else patch, pre-1.0 breaking → minor; CalVer: the next `<year>.<month>.<inc>`,
   inc restarting each month), the semantic `bump` level, the changelog `groups`
   (Keep-a-Changelog: Added / Changed / Deprecated / Removed / Fixed / Security), and the
   `breaking` descriptions. Conventional-commit prefixes drive the grouping; `chore`/`docs` and
   other uncategorised commits are kept out of the changelog as noise, and returned as
   `uncategorised`. **When `groups` is empty, list those subjects under Changed, unedited**, since an
   artifact needs a changelog and nothing may be invented. **If there are none at all, say there is
   nothing to release and stop.** Under CalVer a breaking
   change does NOT alter the version — it must be flagged prominently in the notes instead.
4. **Render the artifact.** Write a `release` handoff artifact (frontmatter `type` (= `release`),
   `feature`, `status`, `version`, `changelog`, `breaking`) plus human-readable notes, then validate
   it (the read-back below; see
   [handoff.md](../../patterns/handoff.md)). Flag every breaking change prominently. Do not invent
   entries beyond the commits.
   Then **read the file back** — `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type release` — and fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).
5. **Tag only on request.** Never create or push a tag unless explicitly asked; propose the
   command and let the user run it. Never rewrite history.

## Output

A `release` handoff artifact: the proposed version, the grouped changelog, and the breaking
changes — ready for the user to review and tag. Nothing is tagged or pushed without an explicit ask.

## Definition of done

- The proposed version follows the repo's scheme: semver applies the correct bump for the commits
  (breaking → major, `feat` → minor, else patch; pre-1.0 breaking → minor); CalVer applies the
  correct `<year>.<month>.<inc>` for today's UTC date (ADR 0055).
- The changelog is grouped into Keep-a-Changelog sections; breaking changes are called out;
  uncategorised commits (chore/docs) are omitted, unless they are all there is.
- The artifact validates as a `release` type (version + non-empty changelog); nothing fabricated.
- **Eval cases that have never executed are named in the release notes.** A case added but never
  run is not coverage — it is an untested assertion that *reads* like coverage. List them under a
  "Not validated" heading with the same weight as a skipped test (the "inspect content, not counts"
  rule from [fan-out-fan-in.md](../../patterns/fan-out-fan-in.md#output-discipline), applied to our
  own gate).
- No tag is created or pushed without an explicit request.
