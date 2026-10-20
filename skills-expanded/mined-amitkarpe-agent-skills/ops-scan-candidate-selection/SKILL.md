---
name: ops-scan-candidate-selection
description: Select safe EC2 candidates for Ops/GovTech/Kishore scans such as Nessus Manager, patch, CIS, VA, or validation scans. Use when Amit asks which EC2s to send for scan, whether Nessus Manager is linked, or needs a compact Ops-ready target table with read-only evidence.
---

# Ops Scan Candidate Selection

Use this skill to choose scan targets and avoid sending the wrong hosts.

## Default

Read-only evidence first. Do not relink, restart, install, patch, reboot, or
change AWS resources.

## Use when

- Amit asks which EC2s Ops/Kishore should scan
- Nessus Manager link/readiness needs confirmation
- scan targets must be selected from DEV/PROD validation hosts
- hosts need sorting into `ready`, `not ready`, `cleanup after scan`, or `retain`
- cleanup host candidates must be tagged for handoff to the owning cleanup runner

## Read first

- repo `AGENTS.md`
- repo `SPEC.md` if present
- `/home/dev/.codex/AWS.md`
- scan-specific context, if relevant:
  - `/home/dev/.codex/AWS_INSPECTOR_CIS.md` for Inspector/CIS

## Evidence root

Use:

```text
~/.AGENTS-temp/<repo>/ops-scan-candidates/<YYYYMMDD-HHMMSS>/
```

Save raw JSON and SSM outputs.

## Minimum checks

For each candidate:

- account/profile/region
- instance id, Name, state, private IP, public IP
- AMI ID
- TTL, cleanup, purpose, phase, environment tags
- SSM PingStatus
- scan-specific readiness

For Nessus Manager readiness, read only:

```bash
rpm -q NessusAgent || true
systemctl is-active nessusagent || true
systemctl is-enabled nessusagent || true
if command -v /opt/nessus_agent/sbin/nessuscli >/dev/null 2>&1; then
  /opt/nessus_agent/sbin/nessuscli agent status || true
elif command -v nessuscli >/dev/null 2>&1; then
  nessuscli agent status || true
else
  echo nessuscli-not-found
fi
```

Never print link keys or secrets.

## Candidate buckets

- `scan-ready`: running, private-only, SSM Online, scan agent ready/linked
- `not-ready`: missing agent, SSM Offline, not linked, service inactive, wrong env
- `cleanup-after-scan`: temporary scan host retained only for scan evidence
- `retain`: durable workload or data host
- `needs-owner-confirmation`: old/stopped/ambiguous host

Special handling:

- For `cleanup-after-scan`, prefer a repo-owned Terraform/Terragrunt cleanup
  workflow instead of one-off AWS commands.
- Shared IAM roles/policies should stay `retain` unless explicit approval says
  otherwise and ownership is clear.

Prefer PROD scan targets when Ops needs PROD scan evidence. Do not substitute DEV
hosts as PROD evidence unless Amit explicitly accepts that.

## Output

Write `RESULT.md` with:

- accounts/profiles/regions checked
- scan-ready table
- not-ready table
- cleanup-after-scan table
- blockers/cautions
- draft Ops/Kishore message

When cleanup candidates are identified:

- if owned by Terraform/Terragrunt, pass candidates to `terraform-terragrunt-cleanup`
  with approved stack context.
- if in AMI Factory and owned by repository cleanup command, pass to that command
  after review approval.

Keep chat summary short and point to `RESULT.md`.

## Safety

- no relink/restart/install/update/remove
- no Patch Manager install or reboot
- no SSM document publish/update
- no AWS mutation
- if identity/env is unclear, stop and record blocker
