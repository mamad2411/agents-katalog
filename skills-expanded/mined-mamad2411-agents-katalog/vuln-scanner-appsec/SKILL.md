---
name: vuln-scanner-appsec
description: Audit application-security defects that let an attacker reach data in the first place — input validation and mass assignment, injection, SSRF, path traversal and uploads, JWT/session handling, object-level authorization (IDOR), security headers, rate limiting, supply chain, and secrets in git history. Writes plans to .plans/appsec/. Read-only. Invoke manually with /vuln-scanner-appsec; not triggered automatically.
user-invocable: true
disable-model-invocation: true
argument-hint: "[lang=es]"
allowed-tools: Read Grep Glob Write Bash(date:*) Bash(git rev-parse:*) Bash(git log:*) Bash(git ls-files:*)
disallowed-tools: Edit NotebookEdit
effort: high
metadata:
  version: "1.8.0"
---

# Vuln Scanner — Application Security

Audits the classes of defect that let an attacker reach data, rather than how the data is handled once reached. The other six packs cover the second question; this one covers the first.

## Where the shared files live

Paths below are written as `<repo>/…`, where `<repo>` is the root of the basic-vulnerability-scanner repository. Resolve it once, taking the first of these that actually contains `packs/shared-protocol.md` — check, do not assume:

1. `${CLAUDE_PLUGIN_ROOT}` — set when these skills are installed as a plugin.
2. `${CLAUDE_SKILL_DIR}/../..` — the repository root under a symlink install, on macOS and Linux.
3. **The symlink's physical target, then two levels up.** On Windows, step 2 does not work: both PowerShell and the bundled bash normalize `..` lexically instead of following the link first, so it resolves to `~/.claude/` rather than to the repository. Read where the link actually points — `readlink -f "${CLAUDE_SKILL_DIR}"` in a Unix-like shell, `(Get-Item <path>).Target` in PowerShell — and take that path's parent's parent.

If none of the three resolves, the installation is broken. Stop and tell the user, per Section 0 of the shared protocol — do not continue with a partial audit. The usual cause is a skill folder that was copied instead of symlinked, which cannot reach the shared `packs/`, `references/`, and `templates/` folders at all.

## Before anything else — run context

Capture these two values first. They fill the `Generated (UTC)` and `Commit` fields of `00-index.md`.

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
git rev-parse --short HEAD
```

Both are pre-approved in this skill's `allowed-tools`, so neither prompts. If either fails — the audited directory is not a git repository, the shell is unavailable, or a deny rule blocks it — record `unknown` for that field with a one-clause reason and carry on. Never invent a date or a SHA.

Control 5 additionally reads git history through pre-approved `git log` and `git ls-files` calls. If the audited directory is not a git repository, that control's history findings become `Not verifiable from repository` — say so rather than reporting the repository as clean.

## What this does

1. Reads the shared audit protocol at `<repo>/packs/shared-protocol.md` in full, with particular attention to Section 6 (high-volume findings) — this pack matches more sites than any other except observability.
2. Follows the control-specific instructions at `<repo>/packs/appsec.md`.
3. Follows `<repo>/references/owasp-node-patterns.md` for every detection signal, including the false positive each family produces.
4. Follows `<repo>/references/secrets-history-scan.md` for Control 5's history checks.
5. Uses `<repo>/references/severity-levels.md` and `<repo>/references/evidence-levels.md` to tag every finding on both axes.
6. Reuses `.plans/discover/00-index.md` if it exists and is current; otherwise detects the stack inline per `<repo>/references/stack-detection.md`.
7. Writes results under `.plans/appsec/` in the audited repository, creating the folder if it does not exist.

## Controls covered

1. **Input handling** — global `ValidationPipe` with `whitelist`, mass assignment, SQL/NoSQL/command injection, SSRF, path traversal, file upload
2. **Authentication and session** — `jwt.decode` where `verify` was meant, unpinned algorithms, missing expiration, refresh rotation, secret fallbacks, password hashing, session cookie flags
3. **Authorization and object-level access** — IDOR/BOLA: whether the authenticated caller is entitled to *this record*, not merely authenticated
4. **Exposure surface** — security headers and CSP, CSRF where cookies authenticate, rate limiting on login, reset, OTP and messaging routes
5. **Supply chain and secret history** — lockfile, install scripts, `overrides`, and whether a secret was ever tracked, not only whether it is present now

## Constraints

- No code is modified. Only Markdown plans are written.
- **Detection only, never exploitation.** A finding names the weakness and its location. It never contains a payload, a proof-of-concept request, or a demonstration of the attack. That boundary is what makes this plan safe to attach to a ticket.
- **Never run gitleaks, trufflehog, a history rewrite, or the application.** Control 5 recommends tooling with the command and lets the user decide. Nothing here is verified by issuing a request.
- **A signal is not a finding.** This pack produces more `Indicator`-grade matches than any other, because most of its signals also match innocent code. When a match cannot be resolved by reading, tag it `Indicator` and state the question that would resolve it. Never round it up.
- Establish what the application serves before judging Control 4. Missing CSP and CSRF are real findings for a cookie-authenticated HTML service and pure noise for a bearer-token JSON API.
- Above roughly 30 matches in a control, the aggregate-table-plus-sample approach of Section 6 is mandatory, not optional.
- Cross-link rather than duplicate: guard inventory belongs to `vuln-scanner-access-secrets`, CORS wildcards and CVE tooling to `vuln-scanner-assurance`, PII in logs to `vuln-scanner-observability`.

## Output

`.plans/appsec/00-index.md`, `01-input-handling.md`, `02-authentication-session.md`, `03-authorization-object-access.md`, `04-exposure-surface.md`, `05-supply-chain-secret-history.md`.

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

Summarize in chat: the applicability and severity of each of the five controls, the highest-severity finding with its location, how many findings are `Indicator` rather than confirmed (this pack produces many, and the ratio tells the user how much verification is still owed), and whether any secret was found in git history. Do not paste full file contents — the files are the deliverable.

Close with one line on what the user now has: `.plans/appsec/` is a prioritized map of this repository's weaknesses and deserves the same handling as any other security finding. If `.plans/` is not already in the audited repository's `.gitignore`, recommend adding it — and only recommend it, per `packs/shared-protocol.md` Section 12.3.
