---
name: vantage
description: >
  Autonomous, artifact-driven SAST (Static Application Security Testing) for
  web AND mobile app repositories, plus optional code-level remediation. Use
  whenever the user asks to security-review, pentest, audit, or scan a
  codebase for vulnerabilities — web (SQLi, XSS, IDOR/BOLA, auth bypass,
  SSRF, XXE, hardcoded secrets, vulnerable dependencies, business logic
  flaws) or mobile/Android/iOS (OWASP Mobile Top 10 2024: improper
  credential usage, insecure data storage, insecure communication,
  insufficient cryptography, etc.) — via static code analysis, never by
  running the app, installing it, or sending requests. Also use when the
  user asks to fix, patch, or remediate a finding this framework produced,
  or to check a single commit/PR/MR for newly introduced vulnerabilities
  without a full repo scan. Drives a 6-phase scan pipeline (recon, mapping,
  testing, validation, PoC, reporting) through the vantage plugin's
  specialized subagents, branching on platform, plus a separate on-demand
  fix step and a fast incremental commit/PR/MR check.
---

# Pentest SAST — Orchestration Skill

This skill is the entry point for the `vantage` plugin. It covers **both**
the web and mobile **scan** pipelines, and the separate **fix** capability.
It is intentionally short: everything phase-specific lives in
`${CLAUDE_PLUGIN_ROOT}/agents/{web,mobile,others}/*.md`, read on demand.
Cross-phase control (gates, parallelism, resume) lives in
`${CLAUDE_PLUGIN_ROOT}/workflow/orchestration.md`.

## Two roots — do not confuse them

- **Plugin assets** (`workflow/`, `agents/`, `schemas/`, `templates/`,
  `knowledge/`, `examples/`, `START-HERE.md`, `TIMESTAMPS.md`) live at
  `${CLAUDE_PLUGIN_ROOT}` — always resolve them from there, never from the
  target project's working directory.
- **Artifacts** (scope, endpoints, findings, PoCs, reports, fixes) are
  per-engagement output, always written under `./.vantage/artifacts/...`
  **relative to the target project currently open** — never inside the
  plugin's own install directory.

## Golden rules (non-negotiable)

1. **SAST only during scanning.** Analyze source code, configuration, and
   dependencies. Never run the application, never install a mobile build,
   never send requests, never exploit live systems. (Live verification of a
   PoC is a separate, human-run manual step.)
2. **One exception: `fix-agent`.** Every scan-phase agent is strictly
   read-only. `fix-agent` — invoked only by `/vantage:fix-issue`,
   `/vantage:fix`, or `/vantage:fix-diff`, never automatically — is the sole
   agent allowed to edit the target repository's source code, and only to
   implement an already-validated finding's remediation. See "Fixing
   findings" below.
3. **Artifacts are the single source of truth.** Every phase reads the
   previous phase's artifact and writes its own — no shared memory between
   agents.
4. **Validate before reporting or fixing.** No finding reaches a report, and
   no finding gets fixed, without passing `validator-agent` first.
5. **Impact-first.** Critical → High → Medium before Low/Informational.
6. **Never block on the user.** If `scope.json` is missing, auto-generate it
   from `${CLAUDE_PLUGIN_ROOT}/artifacts/recon/scope.json.template` (a plugin
   asset) with sane defaults and proceed. If the user's request implies a
   platform ("this is an Android app", "review this iOS codebase" → mobile;
   otherwise → web), set `platform` accordingly instead of always defaulting
   to web.

Full detail: `${CLAUDE_PLUGIN_ROOT}/START-HERE.md` (golden rules §1, universal
agent loop §5, quality bar §8) and cross-phase control (gates, parallelism,
platform routing, resume, failure handling) in
`${CLAUDE_PLUGIN_ROOT}/workflow/orchestration.md`.

## The scan pipeline

Phases 01-03 route by `scope.json.platform`; phases 04-06 are shared. Each
agent file is self-contained — there is no separate phase file to read.

| # | Phase | `platform: "web"` | `platform: "mobile"` |
|---|-------|--------------------|------------------------|
| 01 | Recon | `recon-agent` | `mobile-recon-agent` |
| 02 | Mapping | `mapper-agent` | `mobile-mapper-agent` |
| 03 | Testing | `auth-agent`, `authorization-agent`, `api-agent`, `sqli-agent`, `xss-agent`, `upload-agent`, `business-logic-agent`, `injection-agent`, `dependency-agent`, `secrets-agent`, `misconfiguration-agent` (parallel) | `credential-usage-agent`, `supply-chain-agent`, `mobile-auth-agent`, `mobile-validation-agent`, `mobile-network-agent`, `privacy-agent`, `binary-protection-agent`, `mobile-config-agent`, `mobile-storage-agent`, `mobile-crypto-agent` (parallel; M1-M10) |
| 04 | Validation | `validator-agent` — same agent, either platform | |
| 05 | PoC | `poc-agent` — same agent, either platform | |
| 06 | Reporting | `report-agent` — same agent, either platform | |

Phases run strictly in order 01→06; a phase only starts once its gate
(defined in `${CLAUDE_PLUGIN_ROOT}/workflow/orchestration.md`) is
satisfied. Phase 03's testing agents (11 web / 10 mobile, whichever platform's set) run in parallel
and each write their own `raw-findings.<agent-name>.json` — never a shared
file, and never mix web and mobile agents in the same Phase 03 run.

## How to operate — scanning

1. Determine platform **once**: read `scope.json.platform` if it exists, or
   infer it from the user's request/repo structure (Android/iOS project
   layout → mobile; otherwise → web) when generating a fresh `scope.json`.
   Every phase after this dispatches the matching agent set from the table
   above instead of assuming web.
2. Determine scope: if the user named a specific phase or vulnerability
   class, dispatch only the relevant agent(s) (via Task). Otherwise run the
   full pipeline, phase by phase.
3. Before each phase, check its gate in
   `${CLAUDE_PLUGIN_ROOT}/workflow/orchestration.md` and
   confirm/auto-generate `./.vantage/artifacts/recon/scope.json` if needed.
4. Dispatch the owning agent(s) for that phase (see table above) via the Task
   tool — each subagent reads its own
   `${CLAUDE_PLUGIN_ROOT}/agents/{web,mobile,others}/<name>.md` for full
   methodology.
5. After Phase 03, merge all `raw-findings.*.json` before Phase 04 validates
   (this works identically whether they came from the web or mobile agent set).
6. Append one line per agent run to `./.vantage/artifacts/run-log.md`.
7. Stop and report using the exact artifact paths — never invent alternate
   filenames (e.g. no `SAST-REPORT.md`).

Slash-command equivalent: `/vantage:scan-web` or `/vantage:scan-mobile` —
each forces its platform and runs phases 01-06 in one go. Both accept
`--fast` and `--min-severity=medium|high|critical`; if the user asks for a
quick/fast scan or only high-severity results, set `scope.json.scan_mode`
the same way — see `${CLAUDE_PLUGIN_ROOT}/workflow/orchestration.md`
"Fast Mode & Severity Threshold".

## Fast incremental check — one commit or PR/MR, not the full pipeline

For "does this commit/PR introduce a vuln" instead of a full repo review,
use `/vantage:scan-diff [commit-hash | PR/MR number]`
(`${CLAUDE_PLUGIN_ROOT}/commands/scan-diff.md`) — **not** part of Phases
01-06. It diffs the change, dispatches the platform's testing agents
scoped to just the changed lines, validates, and generates a PoC per
Medium-Critical finding — all under a self-contained
`artifacts/commit-scans/<id>/`. No `report.md` is produced; results are
reported directly in chat. A clean result only means that diff is clean, not
the whole app.

## Fixing findings — separate from scanning, and destructive by design

`fix-agent` (`${CLAUDE_PLUGIN_ROOT}/agents/others/fix-agent.md`) applies a
validated finding's remediation directly to the target repository's source
code. This is **never** triggered automatically by a scan — only by explicit
request, matching `/vantage:fix-issue <id>` (one finding), `/vantage:fix`
(all validated findings, dispatched **sequentially**, never in parallel,
since fixes may touch the same file), or `/vantage:fix-diff <commit-scan-id>
<finding-id>` (a finding from `scan-diff` instead of the main pipeline).

1. Confirm the finding exists and `validated: true` in
   `artifacts/findings/validated-findings.json` (or
   `artifacts/commit-scans/<id>/validated-findings.json` for `fix-diff`);
   skip if its fix record already exists (already handled).
2. Dispatch `fix-agent` via Task. It re-locates the vulnerable pattern in the
   current source (it may have moved), applies the minimal targeted edit, and
   writes a fix record — or marks the finding `not_auto_fixable` with a
   reason instead of guessing.
3. `fix-agent` never runs a build, test suite, or the application — always
   tell the user to review `git diff` and run their own tests before committing.

Slash-command equivalent: `/vantage:fix-issue <id>`, `/vantage:fix`, or
`/vantage:fix-diff <commit-scan-id> <finding-id>`.
