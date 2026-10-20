---
name: flag
description: Feature-flag lifecycle — create, roll out (gated), audit, retire. Use to manage a feature flag, or /flag. Not for deploys (deploy) or infra config (ops domain).
---

# Flag

You manage a feature flag across its whole life: **DRAFT → ACTIVE → ROLLING → RETIRED**, with rollout
**gated on declared conditions**, and you keep the flag manifest honest. The discipline that matters: a
flag created without a **retirement plan** is technical debt that never gets paid — so every flag you
create declares how and when it dies. You manage the flag's state and manifest; you do not ship the
artifact behind it (`deploy`) or provision infrastructure (the `ops` domain).

## What this does / does not do

Does: create a flag (with an owner + a retirement condition), advance it through the lifecycle FSM with
each transition gated on its declared condition, audit the manifest (stale flags, flags past their
retirement condition), and retire flags. Does **not**: deploy the artifact the flag gates (`deploy`),
configure environments/infra (`ops` domain), or advance a flag whose gate condition is unmet.

## When NOT to use

- The task is shipping/rolling back an artifact — that is `deploy` (flags gate *what* is live; deploy
  ships it).
- The task is environment/infra config — that is the `ops` domain.

## Reference Routing

| Situation | Reference |
|---|---|
| The flag manifest (source of truth) | `<workspace>/flags/manifest.json` |
| Rollout monitoring during a ROLLING flag | the `ops` domain (`monitor`) / `status` |
| Receipt write delegation | `engine/shared/references/script-delegation-contract.md` |

## Inputs

| Field | Required | Description |
|---|---|---|
| `action` | yes | `create` \| `rollout` \| `audit` \| `retire` |
| `flag` | for create/rollout/retire | the flag id |
| `condition` | for create/rollout | the gate the transition depends on (and, for create, the retirement condition) |

## How to do it

### The lifecycle FSM
| State | Meaning | Advances when |
|---|---|---|
| **DRAFT** | declared, not active | the gate condition + owner + **retirement condition** are set |
| **ACTIVE** | on for the declared cohort (e.g. internal) | the rollout condition for the next cohort is met |
| **ROLLING** | gradually widening (10% → 100%) | each percentage step's condition is met (monitored) |
| **RETIRED** | removed; the flag and its dead branch are cleaned up | the retirement condition fired |

### Step 1 — Resolve the action against the manifest
Read `<workspace>/flags/manifest.json`. For `create`: require an **owner** and a **retirement condition**
(a flag with no death plan is rejected). For `rollout`/`retire`: the flag must exist and be in a state
the transition is valid from.

### Step 2 — Gate the transition
A transition only happens if its **declared condition** is met (e.g. "error rate < X at 10% before going
to 50%"). An ungated rollout (advance with no condition checked) is refused — that is how a bad flag
reaches 100%.

### Step 3 — Update the manifest + receipt
Apply the transition to the manifest; for `audit`, list stale flags and flags past their retirement
condition (debt). Write the receipt.

## Output Contract

**flag receipt** (`<workspace>/receipts/flag-receipt-<timestamp>.json`): base + `action`, `flag`,
`from_state`, `to_state`, `gate_condition`, `gate_met` (bool), `retirement_condition`, `audit_findings`
(array — stale / past-retirement flags), `confidence`. persistence: Spec-Anchored.

## Proactive Triggers

- **A flag is created with no retirement condition**: reject it — an immortal flag is permanent debt.
- **A rollout is requested but the gate condition is unmet/unchecked**: refuse the advance — never widen a
  flag past an unverified gate.
- **An audit finds a flag past its retirement condition**: surface it as debt to retire — a shipped flag
  that never dies rots the config.
- **The flag's state and the running config disagree**: flag the drift; the manifest is the declared
  intent, the running state is truth — reconcile, don't silently overwrite.

## Completion Criteria

**Done when:** the action is applied to the manifest with each transition gated on its declared condition;
create carries an owner + retirement condition; audit lists debt; a receipt records the transition.

**Not done if:** a flag was created without a retirement condition; a rollout advanced past an unmet/
unchecked gate; the flag deployed the artifact itself (that is `deploy`).

**Next step:** `deploy` ships the artifact the flag gates; `monitor`/`status` watch a ROLLING flag; a
past-retirement flag is retired (and its dead branch cleaned by `clean`).

## Related Skills

- **deploy** (ops domain): Ships the artifact. flag gates *what* is live; deploy makes it live.
- **monitor** / **status**: Watch a ROLLING flag's health. flag manages state; they observe it.
- **clean**: Removes the dead code branch a RETIRED flag leaves behind.
