---
name: long-term-campaigns
description: Persist, schedule, resume, and hand off monitoring or ownership campaigns that outlive one agent session or disposable workspace. Use when work must be checked repeatedly over days, when creating a new long-term campaign, when transferring ongoing work to a future agent, or when producing a delayed evidence-based report.
---

# Long-Term Campaigns

Treat `/Users/igor/work/long-term-campaigns` as the durable source of truth. Agent sessions, workspaces, and VMs are disposable workers around it.

## Campaign isolation

- Create one new subfolder for every new objective: `<ticket-or-system>-<short-slug>`.
- Reuse a folder only when the new request continues the same objective and completion criteria.
- Never place campaign state directly in the root and never mix unrelated campaigns.
- Inspect existing subfolders before creating one. Do not modify sibling campaigns.

## Access from an agent session

- In a local Conductor workspace, read and update the folder directly.
- In a cloud workspace, use Conductor's Mac command bridge. Explain that the durable files exist only on the user's Mac.
- Never copy credentials, tokens, cookies, or raw secrets into a campaign folder, prompt, snapshot, log, or report.

## Required tool and credential policy

- Treat every tool, connector, CLI session, credential, and permission declared
  required by a campaign's runbook as expected to work on every scheduled run.
- Preflight every required dependency before collecting evidence or taking
  campaign actions. Exercise the actual access path when a nominal login can be
  stale; for example, make a harmless authenticated GCP request rather than
  trusting that `gcloud auth list` shows an account.
- If any required preflight fails, expires, or cannot refresh non-interactively,
  stop that campaign run immediately. Do not continue with a partial collector,
  silently degrade to fewer sources, or reinterpret missing evidence as healthy.
- Persist the failed preflight as raw evidence, mark the campaign `blocked`,
  update its next check, release its lock, and fail loudly with the exact class
  of access that must be restored. Never record secret values.
- A periodically expiring CLI session, including GCP authentication, is a
  blocker to renew, not an expected condition to work around.

## Required campaign layout

Create at least:

```text
<campaign>/
├── CAMPAIGN.md
├── RUNBOOK.md
├── state.json
├── logs/
├── prompts/
│   └── DAILY.md
├── reports/
└── snapshots/
```

`CAMPAIGN.md` records the stable contract:

- objective and why it matters;
- scope and explicit exclusions;
- authoritative links and identifiers;
- expected outcome and plausible regressions;
- observable completion criteria;
- observation window, minimum evidence, and expiry policy;
- actions an unattended agent may take. Default to read-only.

`RUNBOOK.md` records the reproducible procedure:

- credential and tool preflights;
- exact collection commands or scripts;
- interpretation rules, thresholds, and comparison windows;
- how to distinguish unknown/no-data from healthy;
- escalation conditions and recovery steps;
- where the final report belongs.

`state.json` records only current machine-readable state. Include the campaign phase, last successful run, next check, latest immutable snapshot, consecutive failures, current blocker, and final-report status. Keep history in snapshots and reports, not by growing this file indefinitely.

`prompts/DAILY.md` tells a fresh agent how to perform one bounded observation turn. Describe capabilities and outcomes rather than requiring a specific model or coding client.

## Hand off a campaign

1. Read this skill and inspect the root for an existing campaign with the same objective.
2. Create a new subfolder when the objective is new.
3. Summarize decisions and verified facts; do not dump an entire chat transcript as the primary handoff.
4. Record timestamps, environments, commit SHAs, rollout boundaries, queries, and source links needed to reproduce each claim.
5. Write the exact current phase and next action into `state.json`.
6. Put reusable deterministic collection in scripts. Keep agent judgment in the daily prompt and report.
7. Define when the scheduler should stop. A recurring campaign without an end condition is incomplete.
8. Validate that a fresh agent with only the campaign folder can continue without asking what happened previously.

## Run a daily observation

1. Acquire a per-campaign lock so two runs cannot update state concurrently.
2. Preflight every required tool, credential, connector, and permission before
   collection, including a harmless authenticated request for refreshable CLI
   sessions.
3. If any preflight fails, follow the required tool and credential policy:
   persist the blocker, stop the run, and fail loudly.
4. Collect evidence deterministically and write a new dated, immutable snapshot.
5. Compare against the declared baseline, rollout boundary, expectations, and prior snapshot.
6. Update `state.json` atomically and write a short daily report only when evidence or phase changed materially.
7. Escalate a breached guardrail with the evidence and first failing boundary. Do not mutate production or external systems unless `CAMPAIGN.md` explicitly authorizes that action.

Prefer a fresh agent invocation for each run. Durable files carry continuity; chat memory does not.

## Complete a campaign

- Mark it complete only when its observable completion criteria and minimum evidence window are satisfied.
- Write a final report stating what changed, what the evidence proves, what it cannot prove, sample sizes, regressions checked, and any remaining owner/action.
- Disable its schedule while retaining the folder and immutable evidence.
- If evidence is insufficient, extend the campaign explicitly rather than reporting success or failure from no data.
