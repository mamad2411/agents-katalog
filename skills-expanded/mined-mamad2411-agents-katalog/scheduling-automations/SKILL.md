---
name: scheduling-automations
description: How to run the Automations plugin's slash commands on a schedule in Caeros (recurring goals, missions, and cloud runs), with sensible cadence defaults per automation. Use when the user wants an automation to run daily, weekly, or on a recurring basis.
---

# Scheduling Automations

The Automations plugin's commands (/fix-ci, /daily-digest, /vuln-scan, /triage-issues, /gen-docs, /add-tests, /autofix-review-comments, /flag-cleanup) are one-shot prompts. To run them recurrently, wrap them in Caeros's scheduling surfaces rather than ad-hoc timers.

## Mechanisms

Caeros offers two ways to run work on a schedule; point the user at the product UI rather than hand-rolling cron:

1. **Recurring goals / missions**: create a goal or mission in the Caeros goals UI whose instruction is the slash command (plus any arguments), and set its recurrence there. Each cycle runs the command fresh against the repo's current state and reports into the goal's history. Best when the user wants an ongoing outcome with memory across runs (e.g. "keep CI green").
2. **Scheduled cloud runs**: schedule a cloud run from the Caeros scheduled-runs UI with the slash command as the run prompt. Each run is independent, executes server-side, and drops its report where the user can review it. Best for stateless report-style automations like digests and scans.

Guidance when setting these up for a user:

- Put the exact slash command, with arguments, as the scheduled instruction, e.g. `/vuln-scan focus on the payments service`. The command body already contains the full playbook, so the schedule stays a one-liner.
- Preserve the commands' report-first contract. Scheduled runs should end in a report; PR creation stays a human-triggered follow-up unless the user has explicitly opted into automatic PRs for that schedule.
- One automation per schedule. Chaining several commands in one scheduled prompt makes failures ambiguous and reports muddy.
- Make sure the schedule targets the right repository (workspace or repo selection in the scheduling UI); the commands are repo-agnostic and operate on whatever repo the run opens.
- Anything needing GitHub state (`gh`) requires the scheduled environment to have GitHub auth; verify that once with a manual run before trusting the schedule.

## Cadence defaults

Good starting points; tune to repo activity:

| Automation | Default cadence | Notes |
|---|---|---|
| /daily-digest | Every weekday morning | Before the team's workday starts; the 24h window matches daily runs. |
| /fix-ci | On demand, or a few times per day on busy repos | Most useful shortly after merges; skip quiet repos. |
| /triage-issues | Daily on active OSS repos, weekly otherwise | Aligns with maintainer triage sessions. |
| /autofix-review-comments | On demand per PR | Poor fit for blind scheduling; run when reviews land. |
| /vuln-scan | Weekly | Also worth a manual run before releases. |
| /add-tests | Weekly | The 14-day change window tolerates weekly gaps. |
| /gen-docs | Weekly or biweekly | Docs drift slowly; avoid daily noise. |
| /flag-cleanup | Monthly | Flags go stale slowly; monthly keeps the inventory fresh without churn. |

## Anti-patterns

- Scheduling write-heavy automations (add-tests, autofix-review-comments) unattended without a human reviewing output between runs.
- High-frequency schedules for slow-moving signals (hourly flag-cleanup produces identical reports and burns runtime).
- Stacking every automation at the same time on the same repo; stagger them so reports arrive digestibly and runs do not contend.
