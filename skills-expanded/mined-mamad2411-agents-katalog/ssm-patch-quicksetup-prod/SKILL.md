---
name: ssm-patch-quicksetup-prod
description: Use when running or repairing AWS SSM Patch Manager Quick Setup for PROD, especially TRUST AL2/AL2023 baselines, scan-only validation, no-reboot install pilots, reboot/rescan closure, compact S3 evidence, and PAT-style patching worker delegation.
---

# SSM Patch Quick Setup PROD

Use this skill for PROD SSM Patch Manager / Quick Setup work where the goal is
to prove patch compliance safely without repeating the same baseline, evidence,
and worker-control research.

## Use when

- reviewing or repairing PROD Quick Setup patch policies
- checking whether Quick Setup uses TRUST baselines instead of AWS predefined baselines
- comparing SSM scan results against Nessus / VA findings
- running scan-only validation across PROD instances
- running a small install pilot with `RebootOption=NoReboot`
- planning a reboot/rescan closure step after install
- delegating PAT or another worker lane for patching work

## Baseline Truth

Default target baselines for TRUST patching:

- Amazon Linux 2: `AL2-TRUST`, baseline id `pb-0bd0869b16759452e`
- Amazon Linux 2023: `AL2023-TRUST`, baseline id `pb-0b9ee1e6c91bb7524`

Expected approval policy:

- `Security`: preserve the repo/account-approved rule.
- `Bugfix`: include it and approve after `0` days.
- Do not add `Newpackage`, `Recommended`, or `Enhancement` by default unless
  Amit explicitly approves the wider package-change surface.

If Quick Setup selects AWS predefined baselines while account defaults point to
TRUST baselines, treat that as drift. Repair Quick Setup selection first, then
run scan-only validation before any install.

## Safe Execution Pattern

1. Confirm target set:
   - running EC2 only
   - SSM online
   - `env=prod` unless Amit names a different target set
   - Name tag and PatchGroup recorded
   - deterministic selection order recorded before AWS response ordering can
     change it
2. Confirm baseline selection:
   - patch policy / Quick Setup manager selects `AL2-TRUST` and `AL2023-TRUST`
   - baseline rules include `Bugfix` with `ApproveAfterDays=0`
3. Run scan-only first.
4. Summarize by count:
   - targets
   - success / failed invocations
   - missing patches
   - failed patches
   - installed pending reboot
5. Install only after approval. A worker goal may count as approval only when
   it names the exact host count or exact target rule, the allowed operation,
   and `RebootOption=NoReboot`.
6. For install pilots, use `AWS-RunPatchBaseline` with:
   - `Operation=Install`
   - `RebootOption=NoReboot`
7. Reboot is a separate approval/window decision.
8. After reboot approval, run reboot/rescan and close the loop.

For one-host or small-batch pilots, write an explicit target guard before
calling `send-command`:

```text
target_guard=pass
target_count=<N>
selected=<instance-id list>
baseline_allowed=<baseline name and id>
reboot_option=NoReboot
```

## Evidence Discipline

Keep evidence compact by default. Save enough to reproduce and explain, not a
full dump of every raw output.

Record:

- local result packet path
- S3 prefix if mirrored
- scan command id
- install command id
- target count and instance ids
- before/after missing, failed, and pending reboot counts
- boundaries held
- exact next step

S3 rule:

- default: keep raw command stdout/stderr local only
- upload compact `RESULT.md`, command ids, target guard, invocation summaries,
  comparison totals, and selected target summary
- do not set `OutputS3BucketName` / `OutputS3KeyPrefix` on `send-command`
  unless Amit asks for raw SSM command output in S3, or the repo's current run
  explicitly requires S3 raw output for audit

Preferred S3 prefixes:

```bash
s3://trust-ssm/patching/quicksetup/<YYYYMMDD-HHMMSS>/
s3://trust-ssm/patching/direct-scan/<YYYYMMDD-HHMMSS>/
s3://trust-ssm/patching/install-pilot/<YYYYMMDD-HHMMSS>/
s3://trust-ssm/patching/reboot-rescan/<YYYYMMDD-HHMMSS>/
```

Keep large raw logs local unless Amit asks for full S3 evidence. If raw S3 was
created by an existing command, do not delete it automatically; record the
prefix and switch future commands back to compact-only unless told otherwise.

## Worker Delegation Pattern

For PAT-style tmux workers, prefer a short prompt file and submit the path
instead of pasting a large prompt:

```text
@/home/dev/git/patching/PAT_<TASK>_<YYYYMMDD>.md
```

After sending through tmux:

1. Capture the pane.
2. If Codex shows a plan modal or the prompt is still in the input, send one
   more `Enter`.
3. Verify the worker moved from input to execution.
4. Save the result path back into compact handoff files.

The prompt file should make approval boundaries concrete:

```text
approved_target_scope=<one instance | exact instance ids | exact tag selector>
approved_operation=<Scan | Install>
reboot_option=NoReboot
max_targets=<N>
stop_if_target_count_differs=yes
```

If those fields are missing or ambiguous, do scan-only and stop before install.

## Interpretation Rules

- `MissingCount=0` and `FailedCount=0` means patch-closed for the selected
  baseline at scan time.
- `InstalledPendingRebootCount>0` means reboot is required to finish the host
  state, but does not grant permission to reboot.
- `PatchBaselineUseDefault=default` is not enough proof by itself. Confirm
  which account default or Quick Setup selected baseline is actually used.
- If a referenced patch baseline id no longer exists, rescan after baseline
  repair before trusting old compliance state.
- A prior `0 missing` result is not proof if Quick Setup associations or async
  executions were failing.
- AWS APIs may return instances in a different order than the preferred list.
  Build a candidate summary, then apply the intended order explicitly before
  selecting the target.
- For repeated pilots, avoid selecting hosts that are already pending reboot
  unless the goal is specifically reboot/rescan closure.

## Guardrails

- Do not run `aws sso login`; Amit handles auth.
- Do not reboot without explicit approval.
- Do not mutate IAM, Quick Setup, baselines, tags, or target selection unless
  the current task explicitly asks for that mutation.
- Do not treat broad phrases like "scan all", "patch prod", or "fix all VA" as
  install approval. Convert them into scan-first inventory or ask for exact
  target scope before install.
- Do not run direct `yum` or `dnf` patching on hosts for this workflow; use SSM
  Patch Manager so the compliance record stays consistent.
- Do not treat `NoReboot` success as final OS closure when pending reboot is
  nonzero. It is patch-closed for missing/failed only.
- Do not copy artifacts to `/tmp/dell` unless Amit explicitly asks.
- For private-only AWS networking, use `aws-private-network-preflight` only for
  VPC/network changes. EC2-only patch work needs no full network preflight.

## Related skills

- `ssm-command-evidence`
- `aws-ssm-run-command`
- `run-worker-goal`
- `prepare-worker-goal`
