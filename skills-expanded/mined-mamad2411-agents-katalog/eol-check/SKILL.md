---
name: eol-check
description: 'End-of-life detection for runtimes (Node, Python, Java, Go, .NET) and key packages — surfaces past-EOL items, items reaching EOL within 90 days, and EOL base images for containers. Use when planning a runtime upgrade, auditing for unsupported versions, gating a deploy against EOL deps, or producing a remediation roadmap.'
license: Apache-2.0
allowed-tools: Bash(vulnetix:*) Read Grep Glob
argument-hint: "[--strict]"
user-invocable: true
model: sonnet
metadata:
  outputBudget: short
  cooldown: per-session
  chain: "dep-resolve, fix"
---
# Vulnetix EOL Check Skill

## Use when

- Quarterly upgrade planning: which runtimes hit EOL in the next 90 days?
- Audit: any past-EOL runtimes in production?
- CI gate: block deploys if any EOL runtime is detected.
- Container base-image EOL check (alpine 3.16, debian 10, etc.).
- Cross-reference: an EOL runtime + an unpatched CVE = critical priority.

## Don't use for

- Vulnerability scanning — use `vulnetix scan --sca` or `repo-impact`.
- License auditing — use `license-check`.

## Conventions

Follows `skills/_lib/contract.md`. In short: use the `vulnetix_*` MCP tools when the agent has them and the CLI otherwise — both shape their own output, so there is no jq step any more. Independent calls go out as concurrent Bash tool calls in one message. One trailing suggestion, not a playbook. See the contract for surface selection, output style and memory writes.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Use `derived.primary_package_manager` and `repo.dockerfile` to decide which surfaces to scan.

## Step 2: Run gated scan

```bash
vulnetix scan --block-eol -o json
```

Exit code is non-zero on EOL hits. Capture findings.

## Step 3: Cross-check runtimes

For each detected runtime, fetch authoritative dates:

```bash
vulnetix vdb product "<runtime>" -o json   # node, python, java, golang, dotnet
```

## Step 4: Render

```
| Runtime / package | Installed | EOL date | Days past EOL | Action |
| Node.js          | 16.x      | 2023-09-11 | 600          | upgrade to 20 LTS |
```

If `--strict`, also flag versions reaching EOL within 90 days.

## Memory update

`event: eol-check` with EOL items per vuln entry (or a top-level `runtimes` block in memory.yaml if entries don't exist).

## Edge cases & gotchas

- `vulnetix scan --block-eol` exits non-zero on EOL hits — wrap with `|| true` to capture without aborting.
- EOL dates are from `vulnetix vdb product` — authoritative for major runtimes, less complete for niche libraries.
- `--strict` mode flags items reaching EOL within 90 days. Default mode only flags past-EOL.
- Container base images need a Dockerfile/Containerfile in the repo; the skill cannot scan a `--image` registry tag without one.
- For runtimes with overlapping LTS schedules (Node 18 vs 20), EOL dates can shift; re-run periodically rather than caching.
- Output flags EOL but does not propose an upgrade path — pair with `dependency-choice` for the recommended target.
