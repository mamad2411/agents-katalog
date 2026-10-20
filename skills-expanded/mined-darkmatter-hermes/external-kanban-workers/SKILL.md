---
name: external-kanban-workers
description: "Use when routing Kanban to external agents over SSH."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, kanban, external-workers, ssh, desktop-agents, routines]
    related_skills: [kanban-worker-operations, hermes-agent, computer-use]
---

# External Hermes Kanban Workers

## Overview

Route Kanban work to an agent that is **not** a Hermes profile: a desktop app, persistent local agent, remote control-plane process, or another tool that can execute commands. The central discipline is **capability-first integration**:

> If the target already has a browser and can run `ssh <host> 'hermes kanban …'`, give it a precise operating contract. Do not build a bridge, API, tunnel, plugin, service, account, or restricted-shell layer unless a real missing capability requires one.

Hermes Kanban remains the lifecycle source of truth. The external agent pulls one card, performs the work with its native tools, and terminates the Kanban run through the stock CLI.

## When to Use

- A desktop agent should replace ordinary Hermes profile workers for a board or task class.
- An external agent can already reach the Hermes host over SSH or another shell transport.
- The user asks for instructions, a saved skill, or a routine to give another agent.
- A non-Hermes worker needs an atomic claim and durable complete/block audit trail.
- You must decide whether direct CLI access is enough or a custom integration is justified.

Don't use for:

- Normal Hermes profile workers; use the standard dispatcher and `kanban-worker-operations`.
- A user who explicitly asked for an HTTP API, plugin, or service and lacks direct command access.
- Cross-system event ingestion that is not task execution; use webhooks or the relevant connector.

## 1. Identify the Worker Correctly

Before proposing architecture, classify the target:

| Target | Correct interpretation |
|---|---|
| Model/provider such as Grok | Configure a Hermes profile or model override |
| Desktop agent application | External worker using its own browser, shell, and routines |
| CLI coding agent | External CLI lane or wrapper, if it cannot use the stock lifecycle directly |
| Human operator | Manual Kanban workflow; no autonomous claim loop |

Treat the user's correction as authoritative. If they say “this is a desktop app” or “it already runs `ssh devbox`,” stop reasoning about provider profiles or network bridges.

**Completion criterion:** the integration plan names the actual executing process and its existing capabilities, not merely the model brand behind it.

## 2. Use the Smallest Existing Transport

Apply this order:

1. **Existing SSH/shell works** → use the stock `hermes kanban` CLI directly.
2. **Host is reachable but authentication is missing** → configure only the missing access, and only if the user asked you to do so.
3. **No command transport, but an authenticated service surface exists** → use that existing surface.
4. **No usable transport exists** → then consider a narrow API, plugin lane, or bridge.

Do not add infrastructure “for cleanliness” when it does not unlock a missing capability. A JSON-producing CLI over SSH is already a machine interface; it does not require an HTTP JSON API around it.

### Instruction-first mode

When the user asks for instructions to give the external agent:

- Deliver a paste-ready worker prompt and, when recurring, a routine prompt.
- Do not mutate Nix, SSH, Cloudflare, services, or credentials.
- State any **separate** Hermes-side routing change still required, but do not perform it unless requested.
- Keep the explanation shorter than the artifact.

**Completion criterion:** the user can paste the instructions into the target agent without translating an architecture proposal into operating steps.

## 3. Preserve Kanban Ownership and Routing

Use a stable assignee string such as `grokbot` for the external lane. In Hermes versions that support manually pulled/nonspawnable assignees, the dispatcher leaves those cards ready for the external worker instead of launching a profile. Verify the installed version rather than assuming this behavior forever.

The external worker must:

1. Resume an existing `running` card assigned to itself before claiming more work.
2. Poll only its intended boards and assignee.
3. Atomically claim exactly one `ready` card.
4. Retrieve the full card after claiming.
5. End every claim with `complete`, `block`, `request-review`, or another supported terminal lifecycle command.
6. Never rely on final prose as task completion.

New intake cards must be assigned to the external lane. Merely teaching the external agent to poll does not stop ordinary workers from claiming cards still assigned to Hermes profiles.

**Completion criterion:** no race exists between the external agent and a spawnable Hermes profile for the same ready card.

## 4. Build the Pull Loop from Stock CLI Commands

The exact boards and prioritization are domain-specific, but a worker contract should contain these phases.

### Resume before claim

```bash
ssh HOST 'hermes kanban --board BOARD list --assignee EXTERNAL --status running --json'
```

If one exists, resume it. If several exist unexpectedly, do not claim more; reconcile the anomaly.

### Poll ready work

```bash
ssh HOST 'hermes kanban --board BOARD list --assignee EXTERNAL --status ready --json --sort priority-desc'
```

When several boards have precedence, encode that order explicitly rather than relying on a global scheduler.

### Claim atomically

```bash
ssh HOST 'hermes kanban --board BOARD claim TASK_ID --ttl SECONDS'
```

A failed claim means another worker owns it or the card is no longer ready. Poll again; do not continue using stale list output.

Choose a claim TTL long enough for the native task. Do not assume a heartbeat renews a manual claim; verify the installed version's semantics.

### Read full context

```bash
ssh HOST 'hermes kanban --board BOARD show TASK_ID --json'
```

Require the worker to read the task body, comments, prior runs, parents, children, attached skills, risks, and acceptance criteria before acting.

### Record progress

```bash
ssh HOST 'hermes kanban --board BOARD heartbeat TASK_ID --note "concise progress"'
```

### Terminate durably

```bash
ssh HOST 'hermes kanban --board BOARD complete TASK_ID --summary "verified outcome" --metadata "{...}"'
ssh HOST 'hermes kanban --board BOARD block --kind needs_input TASK_ID "exact ask and consequence"'
ssh HOST 'hermes kanban --board BOARD block --kind capability TASK_ID "missing capability and evidence"'
ssh HOST 'hermes kanban --board BOARD block --kind transient TASK_ID "failure and safe retry condition"'
```

Dynamic values must be shell-quoted. Never interpolate untrusted email, issue, webpage, or task content directly into a remote command.

**Completion criterion:** the worker instructions cover selection, claim, context, progress, terminal state, and post-transition read-back.

## 5. Encode Domain Policy, Not Just Queue Mechanics

An external worker does not automatically inherit Hermes skills pinned to a card. Its instructions must tell it either:

- how to load/read the governing domain policy; or
- the domain invariants it must obey.

For email, this includes full-thread reading, provider-label verification, send/payment/security approval boundaries, and Inbox/Kanban parity. For code, include repository instructions, tests, commit/review boundaries, and artifact reporting.

Pinned skill names on a card are useful evidence but are not proof that the external agent consumed them.

**Completion criterion:** the external agent knows both how to operate the queue and how to execute the task safely.

## 6. Design Recurring Routines for Single Ownership

A reliable routine should state:

- schedule and time zone;
- resume-running-before-claim behavior;
- one active card per worker unless parallelism is explicitly intended;
- board precedence;
- silence when no work exists;
- where approval questions and technical failures are reported;
- no-data and SSH-failure behavior;
- approval boundaries for consequential actions.

Prefer one-card-per-run or one-card-at-a-time. A routine wake-up is not permission to duplicate an already-running task.

**Completion criterion:** repeated wakes are idempotent and cannot create parallel work on the same card.

## 7. Verify with a Disposable Lifecycle Test

Before changing production routing, prove the actual installed CLI contract on a disposable board:

1. Create a disposable board and one harmless card assigned to the external assignee.
2. Claim it from one external shell/SSH process.
3. Heartbeat it from a second process.
4. Complete or block it from a third process.
5. Read back the card and latest run.
6. Archive the disposable board.

Verify:

- claim is atomic;
- separate invocations can operate on the current run;
- final card status matches the terminal command;
- latest run has the expected outcome and `error=null`;
- no production board was touched.

Only after this passes should intake routing change to the external assignee.

## Common Pitfalls

1. **Confusing a desktop app with a model/provider.** Confirm the executing product before discussing profiles.
2. **Building an API around working SSH.** Direct stock CLI access is already sufficient for polling and lifecycle mutations.
3. **Continuing infrastructure work after the user asks for instructions.** Switch immediately to a paste-ready skill/routine artifact.
4. **Adding a restricted SSH account when access already works.** Do not solve a nonexistent authentication problem.
5. **Changing only the worker prompt.** Intake must also assign cards to the external assignee or ordinary workers can race it.
6. **Claiming multiple cards on each wake.** Resume running work first and preserve single ownership.
7. **Treating `--json` as a new API requirement.** It is only structured stdout from the existing CLI.
8. **Assuming pinned Hermes skills load in another product.** Restate or explicitly load the domain policy.
9. **Finishing with prose.** Every claimed task needs a durable Kanban terminal transition.
10. **Passing untrusted task text through shell interpolation.** Quote generated values and keep raw external content out of command strings.

## Verification Checklist

- [ ] Target is classified as app, model/profile, CLI, or human
- [ ] Existing browser/SSH/shell capabilities were checked first
- [ ] No unnecessary API, tunnel, plugin, service, or account was proposed
- [ ] Deliverable matches the user's request: instructions vs implementation
- [ ] External assignee and ordinary-dispatcher race are addressed
- [ ] Pull loop resumes running work before claiming ready work
- [ ] Claim, context, heartbeat, and terminal commands are explicit
- [ ] Governing domain policy and approval boundaries are included
- [ ] Dynamic shell values are quoted; untrusted content is not interpolated
- [ ] Disposable cross-process lifecycle test passed before production routing
- [ ] Production routing remains unchanged unless the user requested the switch

## Support Files

- `references/grok-bot-email-ssh.md` — validated Grok Bot + email Kanban recipe and paste-ready instruction template from the 2026-08-25 session.
