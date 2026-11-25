---
name: verification-witness
description: Produce a machine-readable verification witness for a fix/change: files changed, commands run, results, commit/issue links, and residual risk.
output_contract: |
  - witness .md and .json both written
  - JSON contains: files_changed, commands_run, results, verdict, timestamp
  - verdict is PASS / PARTIAL / FAIL
---

# Verification Witness Skill

Use this after bug fixes, refactors, releases, deployments, or cron/RSI repairs when the user needs evidence that the work actually landed.

Inspired by Ruflo's verification manifests and witness files.

## Witness location

Prefer project-local:

- `verification/witnesses/<YYYYMMDD-HHMMSS>-<slug>.md`
- `verification/witnesses/<YYYYMMDD-HHMMSS>-<slug>.json`

If no project context exists, use persistent OpenCrabs project storage under `~/.opencrabs/projects/<slug>/files/`.

## Required fields

- Objective
- Timestamp UTC
- Repository / working directory
- Git branch and commit SHA if available
- Files changed
- Commands run
- Command exit codes
- Test/lint/build results
- Linked issue/PR/proposal if any
- Risks / unverified areas
- Final verdict: verified / partially verified / not verified

## Tool routing

- Use `bash` for `git status`, `git rev-parse`, and test command capture.
- Use `write_file` for project-local witnesses.
- Use `write_opencrabs_file` only for OpenCrabs-home artifacts.
- Do not fabricate command outputs. If a command was not run, mark it as not run.

## Output

Report witness path and final verdict.
