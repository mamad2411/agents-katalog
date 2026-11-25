---
name: vuln-scanner-access-secrets
description: Audit application-layer RBAC/access control, hardcoded secrets vs. secrets-manager usage, and collect evidence requests for cloud console MFA and PII resource tagging. Writes plans to .plans/access-secrets/. Read-only. Invoke manually with /vuln-scanner-access-secrets; not triggered automatically.
user-invocable: true
disable-model-invocation: true
argument-hint: "[lang=es]"
allowed-tools: Read Grep Glob Write Bash(date:*) Bash(git rev-parse:*)
disallowed-tools: Edit NotebookEdit
metadata:
  version: "1.8.0"
---

# Vuln Scanner — Access & Secrets

Audits application-layer access control and secret handling, and produces evidence requests for the cloud-account-level controls that cannot be verified from a repository checkout.

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
2. Follows the control-specific instructions at `<repo>/packs/access-secrets.md`.
3. Uses `<repo>/references/nestjs-typescript.md` for RBAC/guard detection patterns.
4. Reuses `.plans/discover/00-index.md` if it exists; otherwise detects stack inline per `<repo>/references/stack-detection.md`.
5. Writes results under `.plans/access-secrets/` in the audited repository, creating the folder if it does not exist.

## Controls covered

1. Access restriction — RBAC/IAM at the application layer (in scope; cloud IAM is not)
2. Secrets in KMS/Secrets Manager vs. hardcoded in source
3. MFA on cloud console — evidence only, always `Not verifiable from repository`
4. Resource tagging `DataType=PII` — evidence only, always `Not verifiable from repository` unless in-scope IaC is present

## Constraints

- No code is modified. Only Markdown plans are written.
- If a tracked `.env` file with real values is found (not `.env.example`), report it as a critical `Confirmed in code` finding.
- Controls 3 and 4 are expected to be short files dominated by an evidence request table (`<repo>/templates/evidence-request.md`) — this is correct, not a shortcut to avoid.
- Cloud infrastructure (IAM policies, KMS key configuration, account-level MFA) is out of scope for direct verification per the shared protocol's Section 1.

## Output

`.plans/access-secrets/00-index.md`, `01-rbac-application-layer.md`, `02-secrets-management.md`, `03-mfa-cloud-console.md`, `04-resource-tagging-pii.md`.

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

Summarize in chat: RBAC coverage gaps found, any hardcoded secrets or tracked `.env` files (flag prominently if found), and the evidence requests raised for MFA/tagging. Do not paste full file contents — the files are the deliverable.

Close with one line on what the user now has: `.plans/access-secrets/` is a prioritized map of this repository's weaknesses and deserves the same handling as any other security finding. If `.plans/` is not already in the audited repository's `.gitignore`, recommend adding it — and only recommend it, per `packs/shared-protocol.md` Section 12.3.
