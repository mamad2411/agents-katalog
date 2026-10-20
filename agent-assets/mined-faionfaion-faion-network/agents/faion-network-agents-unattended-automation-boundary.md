# Unattended Automation Boundary

## Summary

**One-sentence:** Produces an Unattended Automation Record that decides whether an automation runtime is warranted at all — the honest answer is usually "install nothing" — and, when one is, which of three surfaces is the cheapest that can actually express the trigger.

**One-paragraph:** Visual automation tools are bought as a general capability and are in fact a narrow one: they exist to make something happen when nobody is there. If every trigger in your system fires while you are present, your agent's own hooks and the scheduler already on the machine cover the whole surface, and adding a workflow builder buys a second orchestration layer whose only durable effect is drift between the two. So the gate is a single question — does anything have to fire with no human present — and most systems fail it. When something does pass, the escalation order is fixed: agent hooks, then the operating system's scheduler, then a self-hosted workflow runtime, and each step up must name what the step below could not express. The exec question decides the last step outright, because most of these tools cannot run a local binary at all: n8n can, self-hosted only, with the node disabled by default; Make's cloud cannot and its on-premise path is an HTTP bridge on an enterprise plan; Dify cannot even self-hosted, because its sandbox blocks exec; Flowise's custom function runs in a VM with process spawning removed.

**Ефективно для:**

- Anyone about to install n8n, Make, Zapier, Dify or Flowise because automation is the next obvious step.
- Solo operators whose "automation" is really an agent session they start themselves.
- A system that already has one scheduler and is about to grow a second.
- Any workflow that must shell out to a local binary — that requirement alone eliminates three of the four tools.

## Applies If (ALL must hold)

- Some piece of work is a candidate for running without you starting it.
- You control what gets installed, and installing something has a real cost — money, a machine, an update surface, a second place to look when something breaks.
- The triggers can be enumerated: you can list what would start each run and when.

## Skip If (ANY kills it)

- The runtime is already chosen for you by an employer or a client — you are operating it, not deciding it. Use the cron and job-operation methodologies instead.
- Nothing in the system is time- or event-triggered; everything begins with you typing.
- You are debugging or monitoring a job that already exists — see `cronjob-overrun-monitoring` and `cron-automation`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 is the gate most systems fail; R2 fixes the escalation order and R3 the exec constraint. |
| `content/02-output-contract.xml` | The Unattended Automation Record: trigger inventory, the `no-surface` stop, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six ways an automation layer becomes the problem it was bought to solve. |
| `content/06-decision-tree.xml` | Routing from the trigger inventory and the exec requirement to a surface, or to none. |
| `scripts/validate-unattended-automation-boundary.py` | Validates a record; enforces the gate, the escalation justifications and the per-tool exec capability table. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/unattended-automation-record.yaml` | Fill-in record for a warranted surface; ships valid against the contract. |
| `templates/unattended-automation-record-none.yaml` | The gate-stop record — the most common correct outcome, and it installs nothing. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `cron-automation` — how to write and operate the job once this record says a scheduler is the right surface.
- `cronjob-overrun-monitoring` — what to watch after an unattended job exists; this methodology decides whether it should.
- `scheduled-job-decommission-checklist` — the other end of the lifecycle, for the surface this record retired.

## Capability facts, dated

Exec capability was assessed 2026-08-04 against vendor documentation and the projects' own issue trackers: n8n Execute Command runs on self-hosted instances only, is unavailable on n8n Cloud, and is excluded by default so it must be explicitly re-enabled; Make (and Maia) cannot execute a local binary — the On-Premise Agent is an HTTP bridge and an enterprise-plan feature; Dify cannot execute a local binary even self-hosted, because its code sandbox applies a seccomp policy that blocks exec syscalls; Flowise's Custom Function runs inside a JavaScript VM sandbox with `child_process` unavailable. Re-check before relying on any of these — this is exactly the class of fact that changes in a minor release.
