---
name: local-check
description: Writes or updates `scripts/local-check.sh`, the one local command that runs what the project's CI runs (quick mode for what changed, full mode for what CI runs), with a summary and the result OK / FAILED / INCOMPLETE. Use when a project has no local check or only the seeded skeleton, when its CI workflows changed, or when the local check and CI disagree.
argument-hint: "[workflow file, default: every workflow that runs on pull requests]"
---

# Write the local check

Workflows: $ARGUMENTS (default: every workflow of `.github/workflows/` triggered by `pull_request` or `push`).
Reference: `.harness/docs/CI-BASELINE.md` §3 (otherwise `${CLAUDE_PLUGIN_ROOT}/docs/CI-BASELINE.md`).

1. **Start from the skeleton**: `scripts/local-check.sh` (seeded by the harness sync; otherwise copy the harness's
   `templates/scripts/local-check.sh`). Its engine (options, summary, exit codes 0 OK / 1 FAILED / 2 INCOMPLETE)
   stays as is: only the region between `# >>> steps` and `# <<< steps` belongs to the project. A project that
   already has an equivalent command (`make check`, `cargo xtask ci`…) keeps it: check it against points 3 and 4
   and name it in `CLAUDE.md` instead.
2. **Read the CI, not memory**: each job and each `run:` step of the workflows, and the manifests they rely on
   (`Package.swift`, `Cargo.toml`, `package.json`, `pyproject.toml`, `Makefile`, lock files) for the commands and
   versions.
3. **One `step` per CI step**, same name, same command, same order:
   `step "<CI step name>" "<tools>" "<paths>" <<'CMD'` … `CMD`.
   - `<tools>`: every command the step needs; a missing one makes the result **INCOMPLETE**, never green.
     `docker` also needs a running daemon.
   - A step that cannot run on this host (macOS build from Linux): `os:Darwin` in `<tools>`; it is listed as
     skipped with the reason, and the result is INCOMPLETE.
   - `<paths>`: globs of the files the step checks, for `--quick`; `""` for a fast step or one that reads
     everything (tests, secret scan).
   - Event data of CI (`${{ github.event… }}`) becomes a local value computed from git (merge base), never a
     secret. A step that needs a secret, deploys or pushes is left out, with a comment saying why.
   - Not added: CI runner emulation (act…), linters the CI does not run.
4. **Make drift visible**: if the project has tests, one that compares the step names and commands of the
   workflow with those of the script (the harness's `scripts/tests/test_local_check.py` is a model).
5. **Run it**: `scripts/local-check.sh` then `scripts/local-check.sh --quick`; read the summary. A step that fails
   on a clean branch is a CI finding to report in an issue, not a step to remove.
6. **Name it**: `CLAUDE.md` › Build and tests says `scripts/local-check.sh` (before every push; `--quick` while
   working). `/lot-finish` step 1 runs it.

Propose the diff to the operator; the script is the project's file from then on, the harness sync never rewrites it.
