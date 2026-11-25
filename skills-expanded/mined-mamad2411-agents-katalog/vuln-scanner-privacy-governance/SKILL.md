---
name: vuln-scanner-privacy-governance
description: Detect evidence of consent management integration, determine whether real cross-border data transfers exist and reference applicable Chilean law if so, and check for ARCO-style data subject rights implementation. Evidence detection only — never drafts consent flows, DPAs, or legal clauses. Writes plans to .plans/privacy-governance/. Invoke manually with /vuln-scanner-privacy-governance; not triggered automatically.
user-invocable: true
disable-model-invocation: true
argument-hint: "[lang=es]"
allowed-tools: Read Grep Glob Write Bash(date:*) Bash(git rev-parse:*)
disallowed-tools: Edit NotebookEdit
metadata:
  version: "1.8.0"
---

# Vuln Scanner — Privacy Governance

Detects evidence of privacy governance mechanisms and proposes how to request missing evidence. Never designs consent flows, drafts DPAs, or writes legal clauses — that is explicitly out of scope.

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

1. Reads the shared audit protocol at `<repo>/packs/shared-protocol.md` in full.
2. Follows the control-specific instructions at `<repo>/packs/privacy-governance.md`.
3. Uses `<repo>/references/chile-privacy-framework.md` to determine applicable law and, critically, whether a real cross-border transfer exists before citing transfer-related obligations.
4. Uses `<repo>/references/otel-coralogix.md` to check whether the logging/telemetry destination constitutes a cross-border data flow.
5. Reuses `.plans/discover/00-index.md` if it exists for the list of orchestrated/external services.
6. Writes results under `.plans/privacy-governance/` in the audited repository, creating the folder if it does not exist.

## Controls covered

1. Consent management (OneTrust or equivalent) integration evidence
2. Cross-border data transfer: determine if a real transfer exists; if so, cite Ley 21.719 and describe phases only — never generate clause templates or DPA text
3. ARCO-style data subject rights implementation evidence

## Constraints

- No code is modified. Only Markdown plans are written.
- For cross-border transfers: first investigate whether any orchestrated service, cloud region, or telemetry destination is outside Chile. If none is found, mark the control "Does not apply" with justification — do not assume a transfer exists by default, and do not assume one doesn't without checking.
- Never draft contractual clauses, DPA text, or consent banner copy. Only cite the applicable law and describe implementation phases.
- Never design a new ARCO rights workflow — only report what evidence exists or request it.

## Output

`.plans/privacy-governance/00-index.md`, `01-consent-management.md`, `02-cross-border-transfers.md`, `03-arco-rights.md`.

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

Summarize in chat: whether a real cross-border transfer was found (and why/why not), consent integration evidence status, and ARCO rights evidence status. Do not paste full file contents — the files are the deliverable.

Close with one line on what the user now has: `.plans/privacy-governance/` is a prioritized map of this repository's weaknesses and deserves the same handling as any other security finding. If `.plans/` is not already in the audited repository's `.gitignore`, recommend adding it — and only recommend it, per `packs/shared-protocol.md` Section 12.3.
