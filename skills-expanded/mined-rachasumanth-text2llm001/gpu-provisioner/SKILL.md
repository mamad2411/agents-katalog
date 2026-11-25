---
name: gpu-provisioner
description: Provision and manage cost-efficient GPU instances for from-scratch LLM training with strict spend confirmation gates.
---

# GPU Provisioner

Use this skill to source and manage training compute across cloud GPU providers.
Default behavior is cheapest viable hardware that satisfies training requirements.

## Providers

Support provider CLI/API workflows for:

- RunPod
- Vast.ai
- Lambda
- Kaggle

## Core Workflow

1. Gather workload requirements (model size, seq length, batch target, precision, wall-clock goal).
2. Query available instances from supported providers.
3. Rank by total expected run cost, not hourly price only.
4. Present top options with tradeoffs and recommendation.
5. Wait for explicit user approval before provisioning.
6. Provision selected instance, configure access, and set auto-termination.

## Cheapest Instance Finder Logic

Evaluate each candidate using:

- VRAM fit and expected utilization
- Expected throughput for target training stack
- Hourly rate + storage + egress + startup overhead
- Reliability signals (availability, preemption risk, region constraints)

Report at least two options when available:

- best cost-efficiency option
- best stability option

## Cost Estimation

Always estimate before provisioning:

- hourly cost
- expected total run cost
- checkpoint/storage cost
- safety buffer for retries and restarts

If uncertainty is material, provide best-case / expected / worst-case range.

## Spend Confirmation Gate (Mandatory)

- Never provision paid resources without explicit user confirmation.
- Always request explicit confirmation for any spend action.
- If estimated spend for a single action exceeds $100 USD, require a clear confirmation message before continuing.
- If projected spend drifts above estimate during runtime, pause and re-confirm.

## SSH + Instance Management

- Configure SSH keys for secure access to new instances.
- Validate login and GPU visibility after provisioning.
- Provide lifecycle actions: start, stop, restart, terminate.
- Keep a project-local inventory of active instances and endpoints.

## Auto-Termination Safety

Set idle/timeout-based auto-shutdown by default:

- training completed
- no heartbeat for defined interval
- explicit budget cap reached

Surface countdown and termination policy in status updates.

## Kaggle Provisioning

For Kaggle, "provisioning" means verifying quota and kernel availability:

1. Run `kaggle kernels list` to check for active kernels.
2. Run `kaggle hardware` (if available) or assume P100/T4 quota is available if not exceeded.
3. Warning: Kaggle kernels have a 30h weekly limit for GPU. Check `kaggle competitions list` to ensure API is working.

## Required Environment Variables

- RUNPOD_API_KEY
- VAST_API_KEY
- KAGGLE_USERNAME
- KAGGLE_KEY

Optional provider credentials may be added per user environment when needed.

## Cost Ledger (Cross-Skill)

Maintain a project-level `cost_ledger.json` that all cost-incurring skills can read and append to:

- Each entry: `{"skill", "provider", "action", "amount_usd", "timestamp", "notes"}`
- GPU provisioner writes entries for instance creation, hourly charges, and termination.
- Training-runner and cloud-storage should append their own cost entries.
- Provide a `cost_summary.md` on request with total spend, per-skill breakdown, and budget status.

## Preflight Validation

Before any provisioning action, validate:

- Required env vars are set: `RUNPOD_API_KEY`, `VAST_API_KEY`, `KAGGLE_USERNAME`, `KAGGLE_KEY` (as applicable).
- Provider API is reachable and credentials are valid.
- Report clear error identifying which credentials are missing and where to set them.

## Deliverables

1. `gpu_plan.md` (ranked options + recommendation)
2. `cost_estimate.json` (assumptions + range)
3. `instance_manifest.json` (allocated resources + lifecycle settings)
