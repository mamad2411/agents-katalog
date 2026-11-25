---
name: community-ops-automation-workflow
description: Use when designing, reviewing, or documenting community-operations automation, including recurring data collection, report assembly, activity reminders, draft generation, status-board updates, skill/version checks, AI/bot/operator handoffs, execution states, post-action verification, dry-runs, audit trails, owner approval gates, and safe delegation of repeated work to tools.
---

# Community Ops Automation Workflow

## Overview

Use this skill to turn repeated community-ops work into a safe automation workflow. The default model is:

```text
repeated task -> durable input -> automated collection/draft/check
-> human approval gate -> bounded execution -> read-back verification
-> state writeback -> review/update
```

Automation should reduce repeated labor and improve review quality. Keep public, financial, permission, reward, role, and official-claim actions under explicit human approval.

Read [platform-agent-patterns.md](references/platform-agent-patterns.md) when the workflow spans an operator, AI skill, scheduler, bot, API, or platform integration.

## Project Inputs

Get the exact repeated action, input source, durable source of truth, tools or platform adapters, existing permission scope, trigger or frequency, approval owner, expected output, completion evidence, retry limit, and stop conditions from the user or approved project documentation.

The skill supplies the handoff and verification method. It does not include a configured bot, scheduler, API, channels, permissions, credentials, or standing approval. Never borrow integrations or targets from examples. Do not request or store tokens, webhook URLs, passwords, or unnecessary private data; refer to existing secure configuration by name or controlled path.

## Workflow

### 1. Name The Repeated Task

Start by identifying the actual operator action:

- collect community signals;
- prepare a daily or weekly report;
- draft activity/reminder/result copy;
- compare skill versions or stale modules;
- update a local status board;
- prepare a creator or high-value user follow-up list;
- check risk, permissions, rewards, or benefit claims.

Do not automate a vague goal such as "increase engagement." Turn it into a concrete repeated task first.

### 2. Split The Workflow

For each task, define:

- **inputs**: channels, posts, files, reports, metrics, user-provided notes, or prior skill files;
- **source of truth**: the durable record that owns the latest confirmed state;
- **allowed automation**: read, collect, summarize, classify, draft, compare, prepare reminders, create non-destructive local archives, or produce a checklist;
- **human gate**: what the owner must review before execution;
- **execution roles**: what the operator, AI/skill, scheduler, and platform adapter each do;
- **current state**: observed, prepared, pending approval, approved, executed, verified, recorded, blocked, ambiguous, cancelled, or data gap;
- **output**: report, draft, checklist, version diff, action list, or archive note;
- **evidence**: IDs, links, timestamps, counts, source files, or "data missing";
- **success criteria**: what must be true for the workflow to be complete;
- **stop/question condition**: when to stop, ask, or return a structured data gap;
- **retry limit**: which transient failure may be retried and how many times;
- **failure mode**: missing source, stale data, ambiguous target, permissions risk, or public-action risk.

### 3. Choose The Execution Route

Use bounded code or batch tool processing for predictable filtering, joining, ranking, deduplication, aggregation, or validation when the input fields and output schema are known.

Use direct model/tool calls or human review when an intermediate result changes the next judgment, approval is required, source citations or native artifacts must be preserved, or the final result needs semantic validation.

Define one handoff between the two routes. Do not repeat completed calls or switch routes without a new reason.

### 4. Define Roles And State Transitions

Use these role boundaries:

- **operator/owner**: decides scope, approves sensitive actions, and accepts exceptions;
- **AI/skill**: interprets evidence, applies judgment, drafts, and validates semantic results;
- **automation/scheduler**: triggers predictable reads, checks, calculations, and handoffs;
- **platform adapter**: a bot, API, or integration that reads or writes only within its configured permissions;
- **durable record**: stores the latest verified state and minimum necessary evidence;
- **report**: summarizes the record for a decision and does not replace it.

Track the action through:

```text
observed -> scoped -> prepared -> pending approval -> approved
-> executed -> verified -> recorded -> reviewed
```

Use `blocked`, `data gap`, `ambiguous`, or `cancelled` when the normal path stops. An automation run, draft, approval, or unverified execution is not a completed public action.

### 5. Decide What Can Run Automatically

Safe default automation:

- read-only collection;
- draft generation;
- report assembly;
- reminder preparation only;
- version comparison;
- non-destructive local archiving of approved, non-sensitive materials;
- checklist creation;
- data-gap detection.

Do not archive credentials, webhook URLs, raw private messages, personal profiles, payment details, or unnecessary user-level data. Store only the minimum evidence needed for the stated workflow.

Require explicit approval before:

- public posts or announcements;
- DMs or user mentions;
- rewards, winner lists, discounts, or benefit promises;
- role, channel, permission, webhook, or bot changes;
- official metrics, revenue claims, or public commitments;
- handling disputes or payment/access issues.

### 6. Add Dry-Run, Verification, And Review

For workflows with any external effect, include:

- dry-run mode;
- exact target list;
- preview output;
- owner confirmation point;
- execution log;
- read-back verification from the target system;
- state writeback to the durable record;
- rollback or correction note where applicable.

If exact targets are missing, stop at a draft or checklist.

Do not retry an action when the first attempt may already have caused an external effect and its status is ambiguous. Stop, preserve the evidence, and ask the owner to verify the target system.

### 7. Produce The Automation Map

Use this format:

```text
Workflow:
Input and source of truth:
Roles and handoffs:
Automated steps:
Human approval gate:
State transitions:
Output:
Execution receipt:
Read-back verification:
Evidence/writeback:
Success criteria:
Stop/question condition:
Retry limit:
Direct judgment or final validation:
Failure checks:
Review rhythm:
```

## Output Rules

Keep the answer operational. Name what the tool does, what the human decides, and what artifact is produced. If a requested automation crosses a sensitive boundary, propose a safer workflow that stops at draft, dry-run, checklist, or owner review.
