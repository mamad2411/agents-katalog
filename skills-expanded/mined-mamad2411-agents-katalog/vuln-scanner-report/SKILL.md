---
name: vuln-scanner-report
description: Consolidate the audit plans already written under .plans/ into a single .plans/00-summary.md — controls ranked by severity across packs, top risks, evidence requests grouped by who can answer them, and which packs have not been run yet. Runs no audit and reads no source code. Invoke manually with /vuln-scanner-report; not triggered automatically.
user-invocable: true
disable-model-invocation: true
argument-hint: "[lang=es]"
allowed-tools: Read Glob Write Bash(date:*) Bash(git rev-parse:*)
disallowed-tools: Edit NotebookEdit Grep
metadata:
  version: "1.8.0"
---

# Vuln Scanner — Report

Turns the folders under `.plans/` into one view. Run it after any number of audit skills, in any order, at any time.

This skill **audits nothing**. It reads what the audit packs already wrote and consolidates it. It never opens application source code, never re-runs a pack, and never produces a finding that is not already in a control plan.

## Where the shared files live

Paths below are written as `<repo>/…`, where `<repo>` is the root of the basic-vulnerability-scanner repository. Resolve it once, taking the first of these that actually contains `packs/shared-protocol.md` — check, do not assume:

1. `${CLAUDE_PLUGIN_ROOT}` — set when these skills are installed as a plugin.
2. `${CLAUDE_SKILL_DIR}/../..` — the repository root under a symlink install, on macOS and Linux.
3. **The symlink's physical target, then two levels up.** On Windows, step 2 does not work: both PowerShell and the bundled bash normalize `..` lexically instead of following the link first, so it resolves to `~/.claude/` rather than to the repository. Read where the link actually points — `readlink -f "${CLAUDE_SKILL_DIR}"` in a Unix-like shell, `(Get-Item <path>).Target` in PowerShell — and take that path's parent's parent.

If none of the three resolves, the installation is broken. Stop and tell the user, per Section 0 of the shared protocol — do not continue with a partial audit. The usual cause is a skill folder that was copied instead of symlinked, which cannot reach the shared `packs/`, `references/`, and `templates/` folders at all.

## Before anything else — run context

Capture these two values first. They fill the `Generated (UTC)` and `Commit` fields of the summary, and the commit is what the consistency check compares each pack's stamp against.

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
git rev-parse --short HEAD
```

Both are pre-approved in this skill's `allowed-tools`, so neither prompts. If either fails — the audited directory is not a git repository, the shell is unavailable, or a deny rule blocks it — record `unknown` for that field with a one-clause reason and carry on. Never invent a date or a SHA.

## What this does

1. Reads the shared audit protocol at `<repo>/packs/shared-protocol.md` — Sections 2.1 (re-runs), 4 and 4.1 (the two tagging axes), and 12 (sensitivity of the output) govern this pack too.
2. Follows the instructions at `<repo>/packs/report.md`.
3. Uses `<repo>/references/severity-levels.md` for the severity ordering, and `<repo>/templates/summary.md` for the output structure. Section 10 of the protocol governs the summary's language, resolved as described under "Language" below.
4. Lists the subfolders of `.plans/` and reads the `00-index.md` of each pack that has been run.
5. Opens individual control files **only** for `Critical` and `High` controls, to pull one line of description each.
6. Writes `.plans/00-summary.md`.

## What the summary covers

1. **Coverage** — which packs ran, when, against which commit, and which have not been run, with the command that would produce each.
2. **Controls** — every control from every pack that ran, sorted by severity across pack boundaries.
3. **Top risks** — the `Critical` and `High` rows, at most ten, one line each.
4. **Evidence requested** — every `Not verifiable from repository` item, grouped by who can answer it rather than by the pack that raised it.
5. **Consistency** — included only when packs describe different commits, a pack is behind `HEAD`, severity data is missing, packs were written in different languages, or a pack reported stale files.

## Constraints

- No code is modified, and no application source is read. The only input is `.plans/`.
- `Grep` is removed from this skill's tool pool: there is nothing in the audited repository for it to search that this pack is allowed to look at.
- Never add, reclassify, or soften a severity. If a control plan says `Critical`, the summary says `Critical`. Consolidation is not a second opinion.
- If `.plans/` does not exist, or contains no folder with a `00-index.md`, say so and stop. Do not write an empty summary — the fix is to run an audit skill first, and the user needs to hear that rather than receive a file.
- A partial audit is the normal case, not an error. Summarize what exists and name what is missing.

## Output

`.plans/00-summary.md`, per `<repo>/templates/summary.md`.

## Language

Invocation arguments: `$ARGUMENTS`

Resolve the output language **once**, before writing anything, per `packs/shared-protocol.md` Section 10.1. Take the first rule that applies:

1. `lang=es` or `lang=en` in the arguments above.
2. An explicit request in the conversation to write the plans in a given language.
3. A stated preference in the audited repository's `CLAUDE.md`.
4. The `Output language` field of the pack indexes being consolidated. When they disagree, use the most common value and record the disagreement in the summary's "Consistency" section.
5. The predominant language of the pack plans themselves, when their indexes carry no `Output language` field.
6. English.

This pack never reads application source, so it has no repository documentation to judge — rule 5 of Section 10.1 resolves against the plans it is consolidating instead. If those are genuinely split with nothing above to decide, ask once which language to use. Never ask when rules 1 to 4 already resolved it.

Record the choice in `00-summary.md` as `Output language: <code> (<why>)`, and state it in the closing summary along with how to override it. Keep the fixed section headings and the controls-table columns in English regardless, so a later run of this skill can still parse what this one wrote.

## When you're done

Summarize in chat: how many packs were consolidated and how many are still missing, the count of Critical and High controls, and the single highest risk. Point the user at `.plans/00-summary.md` rather than repeating its tables — the file is the deliverable.

Close with one line on what the user now has: `.plans/00-summary.md` ranks this repository's weaknesses in priority order in a single file, which makes it the most sensitive artifact these skills produce. If `.plans/` is not already in the audited repository's `.gitignore`, recommend adding it — and only recommend it, per `packs/shared-protocol.md` Section 12.3.
