---
name: vuln-scanner-discover
description: Build a technical and documentation inventory of the current repository (stack, persistence, messaging, logging/telemetry, external services, CI/CD) and write it to .plans/discover/. Read-only, no compliance judgment. Invoke manually with /vuln-scanner-discover; not triggered automatically.
user-invocable: true
disable-model-invocation: true
argument-hint: "[lang=es]"
allowed-tools: Read Grep Glob Write Bash(date:*) Bash(git rev-parse:*)
disallowed-tools: Edit NotebookEdit
metadata:
  version: "1.8.0"
---

# Vuln Scanner — Discover

Run this skill first when auditing a new repository. It builds the shared inventory that every other `vuln-scanner-*` skill reuses, so you don't repeat stack detection and documentation reading in each one.

## Where the shared files live

Paths below are written as `<repo>/…`, where `<repo>` is the root of the basic-vulnerability-scanner repository. Resolve it once, taking the first of these that actually contains `packs/shared-protocol.md` — check, do not assume:

1. `${CLAUDE_PLUGIN_ROOT}` — set when these skills are installed as a plugin.
2. `${CLAUDE_SKILL_DIR}/../..` — the repository root under a symlink install, on macOS and Linux.
3. **The symlink's physical target, then two levels up.** On Windows, step 2 does not work: both PowerShell and the bundled bash normalize `..` lexically instead of following the link first, so it resolves to `~/.claude/` rather than to the repository. Read where the link actually points — `readlink -f "${CLAUDE_SKILL_DIR}"` in a Unix-like shell, `(Get-Item <path>).Target` in PowerShell — and take that path's parent's parent.

If none of the three resolves, the installation is broken. Stop and tell the user, per Section 0 of the shared protocol — do not continue with a partial audit. The usual cause is a skill folder that was copied instead of symlinked, which cannot reach the shared `packs/`, `references/`, and `templates/` folders at all.

## Before anything else — run context

Capture these two values first. They fill the `Generated (UTC)` and `Commit` fields of `00-index.md`, and the `Commit` value is what later packs compare against to decide whether this discovery output is still current.

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
git rev-parse --short HEAD
```

Both are pre-approved in this skill's `allowed-tools`, so neither prompts. If either fails — the audited directory is not a git repository, the shell is unavailable, or a deny rule blocks it — record `unknown` for that field with a one-clause reason and carry on. Never invent a date or a SHA, and never abort the audit over this.

## What this does

1. Reads the shared audit protocol at `<repo>/packs/shared-protocol.md`. Follow it in full — output contract, evidence levels, investigation order, high-volume handling, tool/agent usage, stack detection, and independence rules all apply here.
2. Follows the discovery-specific instructions at `<repo>/packs/discover.md`.
3. Uses `<repo>/references/stack-detection.md` to detect language/framework/ORM/logging stack.
4. Writes results under `.plans/discover/` in the **repository currently being audited** (not in this skills repository), creating the folder if it does not exist.

## Before you start

- If a `find-skills` skill (or equivalent) is available in this environment, use it to check whether other installed skills can accelerate this inventory, and invoke them if useful.
- If a Graft MCP server or `graft/` folder exists in the audited repository, prefer its repository-map and code-search tools over manual file traversal. If Graft is absent, continue without it and note the recommendation to install it — never install or configure it yourself.
- This skill only writes Markdown under `.plans/discover/`. It never modifies application source code.

## Output

- `.plans/discover/00-index.md`
- `.plans/discover/01-inventory-detail.md`

Both follow the structures defined in `packs/discover.md` and `templates/index.md`.

## Language

Invocation arguments: `$ARGUMENTS`

Resolve the output language **once**, before writing anything, per `packs/shared-protocol.md` Section 10.1. Take the first rule that applies:

1. `lang=es` or `lang=en` in the arguments above.
2. An explicit request in the conversation to write the plans in a given language.
3. A stated preference in the audited repository's `CLAUDE.md`.
4. The `Output language` field of any existing `.plans/*/00-index.md` in this repository.
5. The predominant language of the repository's own documentation — README, `docs/`, `CLAUDE.md`, and comments already seen while investigating. Do not run a separate scan for this; the signal is already in front of you.
6. English.

If rule 5 is a genuine tie — documentation split between two languages, with nothing above it to decide — ask once which language to use. Never ask when rules 1 to 4 already resolved it.

Record the choice in `00-index.md` as `Output language: <code> (<why>)`, and state it in the closing summary along with how to override it. Fixed section headings and the controls-table columns stay in English regardless: `vuln-scanner-report` parses them.

## When you're done

Give the user a short summary in chat: stack detected, confidence level, which documentation sources were read, whether Graft was available, and which inventory categories (persistence, messaging, logging, external services, CI/CD) were found. Do not paste the full file contents into the chat — the files are the deliverable.

Close with one line on what the user now has: `.plans/discover/` is an inventory, not a set of findings — this pack judges nothing — but it maps the repository's attack surface in one place and deserves the same handling as the packs that do produce findings. If `.plans/` is not already in the audited repository's `.gitignore`, recommend adding it — and only recommend it, per `packs/shared-protocol.md` Section 12.3.
