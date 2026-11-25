---
name: ssm-command-evidence
description: Run one AWS Systems Manager command or document on one instance, wait for completion, capture stdout/stderr/status, and save durable evidence. Use for repeated one-host AWS CLI plus SSM loops, Patch Manager scan/install pilots, and before/after evidence bundles that are broader than CIS-specific document workflows.
---

# SSM Command Evidence

Use this skill for the generic one-instance SSM operator loop when you want a
durable local evidence bundle, not just a command result.

## Use when

- running one shell command on one EC2 instance through SSM
- running one existing SSM document and saving evidence
- collecting stdout, stderr, status, and timing for one host
- proving whether a host-side change succeeded before wider rollout
- saving a repeatable evidence bundle under `~/.AGENTS-temp/<repo>/...`
- running a small Patch Manager scan/install pilot where before/after state must be compared

## Preferred workflow

1. Confirm target instance is SSM online.
2. Save the exact command or document input in a dedicated output directory.
   Reuse that directory to reconcile the same intent; use a new directory only
   for a separately authorized new intent.
3. For `AWS-RunShellScript`, use `aws-ssm-run-command` as the core send/wait/get-output engine.
4. For an existing SSM document, keep the same durable evidence flow and use the shared wait/get-output helpers.
5. Save:
   - command id
   - status
   - stdout
   - stderr
   - target instance id
   - profile / region
6. Record the next action: success, exact-ID readback/wait, stop for unknown
   outcome, or an explicitly authorized rollback/new attempt. A failed or
   interrupted wrapper is not permission to resend.

`scripts/run.sh` retains `command-id.txt`. An existing ID is read back, not
resent; a `PENDING`/empty marker means the send outcome is unknown and blocks a
repeat until provider reconciliation. See the five-case decision examples in
[`aws-ssm-run-command`](../aws-ssm-run-command/references/examples.md).

## Patch Manager pilot pattern

For SSM patch scan/install pilots, keep the first pass to 2-3 instances.

Use this interpretation for Patch Manager counts:

- `MissingCount=0` and `FailedCount=0` means patch-closed for the approved
  baseline at scan time.
- `InstalledPendingRebootCount>0` means reboot is still required to finish the
  OS/runtime state, but it is not permission to reboot.
- Reboot remains a separate approval/window decision.

For each instance:

1. Save identity and targeting context:
   - instance id
   - Name tag
   - `env`
   - PatchGroup
   - OS/platform
   - baseline id/name from patch state or baseline lookup
2. Save before state:
   - `describe-instance-patch-states`
   - recent association/command ids if relevant
3. Run scan-only first.
4. Save after-scan state and command/association output.
5. Run install only when approved, with `RebootOption=NoReboot` unless the user explicitly approves reboot.
   The approval must identify the exact instance ids, exact tag target, or a
   bounded host count plus selection rule.
6. Save after-install state.
7. Write one comparison row per instance:
   - before missing
   - after scan missing
   - after install missing
   - failed
   - installed pending reboot
   - reboot needed
   - evidence path

S3 mirror convention when requested:

```bash
s3://trust-ssm/patching/<instance-id>/<YYYY-MM-DD-HHMMSS>/
```

For multi-host install pilots, use a run-level prefix:

```bash
s3://trust-ssm/patching/install-pilot/<YYYYMMDD-HHMMSS>/
```

Prefer uploading compact summaries and command metadata first. Keep large raw
logs local unless the user asks for full S3 evidence.

For Patch Manager pilots, do not set `OutputS3BucketName` /
`OutputS3KeyPrefix` on `send-command` by default. Those fields upload raw
plugin stdout/stderr to S3. Prefer local raw output plus compact S3 files
unless the user or repo policy explicitly requires raw SSM output in S3.

## Typical AWS CLI pattern

```bash
aws ssm send-command ...
aws ssm get-command-invocation ...
aws ssm list-command-invocations ...
```

## Save evidence under

```bash
~/.AGENTS-temp/<repo>/ssm-command-evidence/<timestamp>-<instance_id>/
```

## Rules

- prefer one instance at a time first
- save the exact command input, not only the output
- do not widen to many instances until one-host proof is clean
- before install, write a small target guard with selected ids, target count,
  operation, and reboot option
- treat rollback as a documented next step, not an implied chat action
- treat this skill as the durable wrapper around `aws-ssm-run-command`, not a competing SSM engine
- use `cis-ssm-apply-validate` instead when the task is specifically:
  - publish/update SSM document
  - pin default version
  - apply and validate the CIS document workflow end to end

## Related skills

- `aws-ssm-run-command`
- `cis-ssm-apply-validate`
- `ami-validation-ssm`
