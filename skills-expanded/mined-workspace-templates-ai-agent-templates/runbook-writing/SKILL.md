---
name: runbook-writing
description: Turns an operational task or alert into a runbook with symptoms, checks and exact commands, so on-call can act at 3am without guessing.
---

# Runbook writing

Write for the person on call who did not build this system.

## Steps

1. Identify the scenario: the alert name or task, who triggers it, and the impact on users. Read the alert rule, deploy config, Terraform or compose files and scripts to learn the real service names, hosts, ports and log locations.
2. Open with a three-line summary: what this runbook is for, severity, and expected time to resolve.
3. Write the **Symptoms** section: what the alert says, what users see, and the dashboard or log query that confirms it.
4. Write **Diagnose** as numbered checks, cheapest first. Each check has the command, the output that is normal, and the output that points to a cause with the jump to the matching fix.
5. Write **Fix** per cause. Label every command `[read-only]` or `[changes state]`. For anything that changes state, add the rollback command and a verification command.
6. End with **Escalate**: when to stop, who to page, and what facts to hand them (time, commands run, outputs).

## Rules

- One action per step, in the order to run them.
- Commands must be copyable with no hidden edits; show variables in `<ANGLE_BRACKETS>` and say where to find them.
- Never include secrets or production credentials.
- Do not write "check the logs" without the exact query.
- Date the runbook and name its owner.

## Report

The file path, the commands you could not verify, and gaps where the repository gave no answer.
