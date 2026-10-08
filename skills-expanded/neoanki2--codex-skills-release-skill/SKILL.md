---
name: release
description: Release NeoAnki2 end to end through its authenticated GitHub CLI, attested candidate, protected checks, GitHub Release, official Homebrew tap, verified app upgrade, and exact-path launch. Use when asked to release, ship, publish, merge-and-release, update the Homebrew cask, install the new NeoAnki2 version, or resume an interrupted NeoAnki2 release.
---

# Release NeoAnki2

Use the repository's single resumable release command. Do not reconstruct its
remote steps manually.

## Prepare

1. Work from a clean `codex/*` feature branch based on current `main`; preserve
   unrelated changes and stop if the worktree is dirty.
2. Confirm the intended change is committed and `gh auth status` succeeds.
3. Write a concise PR body to `.build/release-pr.md`.
4. Keep NeoAnki2 running. Local validation, CI, merge, publication, and tap
   refresh do not require downtime.
5. For UI-bearing changes, run the relevant targeted journey and the complete
   `./Scripts/run-ui-tests.sh` suite before release. If desktop policy or local
   permissions prevent UI verification, stop before push and report it as the
   blocker.

## Run

Run the complete release transaction:

```bash
./Scripts/release.sh \
  --title "Concise release title" \
  --body-file .build/release-pr.md
```

For this project, “release” always means push, PR, CI, attested candidate,
merge, GitHub publication, tap update, Homebrew upgrade, signature and revision
verification, and one exact-path launch. The command stops a running app only
immediately before replacement and launches `/Applications/NeoAnki2.app` once.
Use `--no-install` or `--no-launch` only when the user explicitly requests that
narrower outcome.

When screenshot-backed sources changed, the command waits for the
**Documentation screenshots** workflow to capture and validate the full set on
isolated macOS CI and commit it to the pull-request branch. The command starts
or reconciles required checks for that promoted revision, including known bot-owned
`action_required` runs or dispatches missing exact-head fallbacks. Candidate
packaging must use the resulting PR head and starts only after documentation
and every required macOS UI shard passes. Stale screenshots have no release
deferral or bypass.

Allow the command to wait for CI. Send compact progress updates when waiting;
do not replace the wait with repeated manual GitHub operations.

## Resume

After interruption or a corrected check, resume the same transaction:

```bash
./Scripts/release.sh --pr NUMBER
```

The command detects and skips completed candidate, merge, publication, tap, and
installation phases while preserving the full-release default. When the clean
local branch is the PR branch and contains committed ahead-only corrections,
resume reruns local preflight, pushes that head, and waits for the PR to expose
it before reconciling workflows. It refuses divergent local history.
If the exact screenshot run ended in a retryable infrastructure failure, the
resumed command starts and watches one new attempt. It never retries an
approval-required run automatically.

## Guardrails

- Use authenticated `gh` only; never use a GitHub connector.
- Treat `release-candidate.json` as authoritative for version, revision,
  artifact, and SHA-256. Never type or infer a checksum.
- Never merge before required checks and the attested candidate succeed.
- Never package or merge a revision while CI still requires a documentation
  screenshot capture.
- Never approve an unknown `action_required` workflow manually. The release
  command may approve only its allowlisted bot-owned workflows for the exact PR
  head; every other approval request is a blocker.
- Never run the recovery **Release** workflow alongside the candidate path.
- Never edit the tap cask by hand.
- Never quit NeoAnki2 before the release command's just-in-time install phase.
- Allow the command's verified `SIGTERM` fallback after the normal quit grace
  period. Never use `SIGKILL` to force installation.
- Never use `open -a NeoAnki2`; it can select a debug build.
- Never retry a GUI launch. The script makes at most one absolute-path launch
  and verifies the running executable.
- Never report failure solely because a valid release took longer than a target.

## Report

Return the PR URL/number, release tag and URL, source revision, tap version,
installed version and embedded revision when installed, signature result, and
whether the verified `/Applications` executable is running. If blocked, name
the exact failed invariant and the emitted `RELEASE_PHASE`; preserve the
`RELEASE_*` and `SHIP_*` timing lines for audit, then use the resume command
after the invariant is corrected.
