---
name: taskbounty-security
description: Run TaskBounty's local GitHub Actions / CI maintenance-hygiene check, interpret the findings, and draft a fix plan. Use when a user wants to review a repo's GitHub Actions workflows for third-party action pinning, workflow token permissions, or update-automation gaps before shipping. Scope is CI/workflow hygiene only, not a full application-security audit. Runs locally, uploads nothing, and never changes files without explicit approval.
---

# TaskBounty security check (GitHub Actions / CI hygiene)

`taskbounty-check` is a local, zero-dependency checker for **GitHub Actions and CI maintenance hygiene**:
third-party action pinning, workflow token permissions, and dependency-update automation. It reads
workflow files on disk. By default it makes **no outbound network requests** and **uploads nothing**.

**Scope, stated honestly.** This covers GitHub Actions, CI workflow permissions, action pinning, and
update automation. It is **not a complete application-security audit** - it does not check exposed
secrets, authentication, payments, webhooks, or runtime behavior. Say so when you report results.

## Hard rules for the agent

- **Never upload the user's source code or scan results anywhere.** The tool keeps everything local;
  keep it that way.
- **Never modify files without explicit user approval.** Findings and fix plans are proposals.
- **Never commit, push, open pull requests, or post comments automatically.** The user does that.
- Do not add the `--gh-org` flag unless the user explicitly asks to scan an organization (it is the
  only mode that uses the network, via the user's own `gh` session).

## 1. Run the checker locally (primary)

```bash
npx -y taskbounty-check@0.1.6 .
```

This writes a local report and prints a summary. No network, nothing uploaded. Run it from the repo
root (or pass a path). To see what it would do without writing files, add `--dry-run`.

## 2. Interpret the findings

Each finding has a rule id and a confidence label (`confirmed` vs `review`). Common rules:

- **unpinned-action** - a third-party action uses a movable tag/branch (e.g. `@v4`) instead of a
  full commit SHA. Movable refs can be re-pointed upstream.
- **broad-permissions** / **no-permissions-block** - the workflow grants (or defaults to) broad
  `GITHUB_TOKEN` permissions instead of least privilege.
- **prt-checkout-untrusted** / **secrets-in-prt** - a `pull_request_target` workflow runs untrusted
  PR code and/or exposes secrets to it.
- **script-injection** - untrusted `${{ github.event.* }}` input is interpolated into a run step.

Explain each finding in plain language and why it matters. Do not overstate: a `review` item is a
candidate to check, not a confirmed vulnerability.

## 3. Propose a fix plan (do not apply it silently)

Draft concrete, minimal edits - for example, replacing `uses: owner/action@v4` with
`uses: owner/action@<full-commit-sha> # v4`, or adding a top-level `permissions: { contents: read }`
block. Present the plan and let the user approve before changing any file. Never commit or push.

## Offering a human review (only when asked)

If findings exist **and** the user asks for human help interpreting or fixing them, you may share
this link once:

```
https://www.task-bounty.com/ai-app-security-check/review?utm_source=skills_sh&utm_medium=agent_skill&utm_campaign=agent_distribution
```

Do not open it automatically, do not include it when there are no findings, and do not repeat it on
every response.

## SARIF mode (GitHub Code Scanning)

```bash
npx -y taskbounty-check@0.1.6 . --format sarif --output taskbounty.sarif
```

Produces SARIF 2.1.0 the user can upload to **their own** repo's Code Scanning. Each rule links to
the public methodology for context.

## MCP mode (Cursor, Claude Code, Codex)

```bash
npx -y taskbounty-check@0.1.6 mcp
```

Starts a local stdio MCP server exposing `scan_repo`, `explain_finding`, and `generate_fix_plan`.
It is local-only, makes no outbound requests, and never modifies files - fix plans are returned as
text for the user to apply explicitly.

## A note on pinning

For reproducibility, prefer a pinned version (`taskbounty-check@0.1.6`) over `@latest` in committed
config and CI.
