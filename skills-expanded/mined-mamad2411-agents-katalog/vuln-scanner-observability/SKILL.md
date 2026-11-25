---
name: vuln-scanner-observability
description: Audit console.*/logger.* calls for PII and secret exposure, classify by risk, and check audit-log completeness (IP/user/timestamp). Handles high-volume logging findings (tens to hundreds of matches) by aggregating and sampling instead of enumerating. Writes plans to .plans/observability/. Read-only. Invoke manually with /vuln-scanner-observability; not triggered automatically.
user-invocable: true
disable-model-invocation: true
argument-hint: "[lang=es]"
allowed-tools: Read Grep Glob Write Bash(date:*) Bash(git rev-parse:*)
disallowed-tools: Edit NotebookEdit
effort: high
metadata:
  version: "1.8.0"
---

# Vuln Scanner — Observability

Audits logging practices for PII/secret exposure risk and for audit-trail completeness. This is the control most likely to encounter a very large number of matches in a single repository — follow the sampling rules carefully.

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

1. Reads the shared audit protocol at `<repo>/packs/shared-protocol.md` in full, especially Section 6 (handling high-volume findings).
2. Follows the control-specific instructions at `<repo>/packs/observability.md`.
3. Follows `<repo>/references/logging-pii-patterns.md` for sink inventory, classification categories, and phased remediation.
4. Uses `<repo>/references/otel-coralogix.md` to evaluate the internal OpenTelemetry-to-Coralogix wrapper's interceptor and sanitizer, if present.
5. Reuses `.plans/discover/00-index.md` if it exists for stack/logging-library detection; otherwise detects it inline.
6. Writes results under `.plans/observability/` in the audited repository, creating the folder if it does not exist.

## Controls covered

1. `console.*` / `logger.*` PII and secret exposure audit
2. Audit log completeness (IP, user, timestamp) for security-relevant events

## Mandatory sampling rule

If total logging call sites found exceed roughly 30, you **must**:
- Build an aggregate table by file/module and category (see `<repo>/templates/logging-register.md`).
- Quote at most 8–10 highest-risk call sites as evidence, with actual secret/PII values redacted.
- Convert the remainder into phased remediation tasks, not a line-by-line list.

Never write a plan file that enumerates every matching line when the count is large.

## Constraints

- No code is modified. Only Markdown plans are written.
- Every finding carries an evidence confidence level per `<repo>/references/evidence-levels.md`.
- Never name a specific company or internal package name for the OpenTelemetry-to-Coralogix wrapper — describe it generically per `<repo>/references/otel-coralogix.md`.

## Output

`.plans/observability/00-index.md`, `01-console-logger-audit.md`, `02-audit-log-completeness.md`.

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

Summarize in chat: total call sites found, category breakdown at a glance, top 2–3 risks, and the phase plan headline (e.g., "3 phases, Phase 1 covers 12 files"). Do not paste the full aggregate table into the chat — the files are the deliverable.

Close with one line on what the user now has: `.plans/observability/` is a prioritized map of this repository's weaknesses and deserves the same handling as any other security finding. If `.plans/` is not already in the audited repository's `.gitignore`, recommend adding it — and only recommend it, per `packs/shared-protocol.md` Section 12.3.
