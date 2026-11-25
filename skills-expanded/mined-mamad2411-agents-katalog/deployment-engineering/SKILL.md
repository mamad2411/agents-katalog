---
name: deployment-engineering
description: Gets a verified artefact running in a target environment on any platform: target selection, migration ordering, health gated rollout, rollback that states what it cannot restore, and deployment documentation. Platform agnostic; inspects the project before choosing.
license: MIT
metadata:
  category: devops-skills
  version: 1.0.0
  depends_on: [engineering-core, devops-core, environment-management, ci-cd-pipelines]
  outputs: [deployment-procedure, rollback-plan, deployment-record, platform-decision]
---

# Deployment Engineering

Moves a tested artefact into an environment and proves it runs there.

Platform agnostic by construction. The project and its requirements decide the
target, not habit.

## 1. Target selection

Read the constraints before choosing. The client's operations capability is
usually the deciding factor, not the technical merits.

| Target | Fits when | Costs |
|---|---|---|
| a single server | one artefact, predictable load, an operations team that runs servers | patching, monitoring, backups are yours |
| a managed application platform | a web application, standard runtime, small team | less control, per instance pricing |
| a container platform | several services, existing container practice | operational complexity |
| serverless functions | spiky or event driven load, stateless work | cold starts, execution limits, vendor coupling |
| static hosting plus an API | a mostly static front end | two deployment paths |
| the client's existing infrastructure | they have one and a team who runs it | you inherit its constraints |

Record the decision with the same format as `technology-selection`: choice,
alternatives, rejection reasons, trade-off, reversal cost.

## 2. Deployment properties

Whatever the target, aim for these. Where one is unattainable, say so.

```
Repeatable    the same procedure produces the same result
Reversible    a previous version can be restored, and how long it takes is
              known
Observable    the outcome is visible without asking a user
Gradual       traffic moves only after health is confirmed
Zero downtime where the platform allows it; where it does not, the window is
              stated and announced
```

## 3. Migration ordering

The most common cause of a broken deployment is code and schema disagreeing
during the window when both versions run.

```
Expand      add the new column, table or index; both versions work
Migrate     backfill in bounded batches, resumable
Switch      deploy code that writes and reads the new shape
Contract    remove the old shape, in a later deployment
```

Rules:

- Never rename in one step. Add, backfill, switch, drop.
- Never drop in the same deployment that stops using it.
- Additive migrations run before the code deploy.
- Destructive migrations run after the code deploy that stopped using the old
  shape, and only once that version is confirmed stable.
- Every migration is tested against a copy of realistic data, or the absence
  of that rehearsal is stated.

## 4. Health gating

A deployment is not complete when the process starts.

```
1  the new instance starts
2  its health check passes
3  traffic moves to it, partially where the platform allows
4  error rate and latency are watched for a stated window
5  the remaining traffic moves
6  the old version is retired
```

Where the platform cannot do this, the equivalent is: deploy, verify with a
real request, watch the errors for the window, and keep the previous artefact
ready.

## 5. Rollback

Written before the deployment, always, including for small changes.

```
Command      how to revert, exactly
Duration     how long it takes, measured not guessed
Restores     what returns to the previous state
Does not     sent mail, delivered webhooks, captured payments, written files,
             dropped columns, rows created since the deploy
Cache        what must be invalidated after reverting
Verify       how to confirm the rollback worked
```

The `Does not` line is what makes a rollback plan honest. A release that sends
email is not reversible, whatever the code does.

## 6. Deployment record

Every deployment above `development` leaves one.

```
Version      the artefact, by commit
Environment  named, and how the target was verified
Migrations   which ran, additive or destructive
Started      timestamp
Health       when it passed
Traffic      when it shifted
Watched      the window, and what was observed
Result       success, rolled back, or partial with detail
```

## 7. Failure

A failed deployment is diagnosed, not retried blindly.

```
1  Read the logs from the failing instance, not only the deploy tool output
2  Distinguish: build failure, start failure, health failure, runtime failure
3  Start failure is usually configuration; check the required variables first
4  Health failure is usually a dependency; check the database and the network
5  Fix the cause, not the symptom
6  Redeploy, and verify
```

Never: redeploy hoping for a different result, disable the health check to let
a deployment through, or deploy directly to production to test a fix.

## 8. Documentation

The deployment procedure exists in written form, executable by someone who did
not write it.

```
Prerequisites        access, tools, versions
Environment          which variables must exist, verified how
Build                the command, or where the artefact comes from
Migration            the command, and when it runs relative to the code
Deploy               the command or the trigger
Health verification  the exact check, and the expected result
Smoke check          one real user path
Rollback             from section 5
Troubleshooting      the failures seen before, and their fixes
```

## 9. Protocol

1. Choose the target, section 1, and record the decision.
2. Establish the deployment properties achievable, section 2.
3. Plan the migration ordering, section 3.
4. Confirm required variables exist in the target before starting.
5. Write the rollback plan, section 5, before deploying.
6. Deploy with health gating, section 4.
7. Verify with `production-verification`.
8. Record, section 6.
9. Document, section 8.

## 10. Auto-critique

Score from 0 to 5: target chosen from constraints rather than habit,
properties stated honestly, migration ordering safe across the window,
variables verified before starting, rollback written beforehand with its
limits, health gating applied, record complete, documentation executable by
someone else.

Threshold: no axis below 3, average at least 4. A deployment with no rollback
plan, or a destructive migration in the same deployment as the code that stops
using the old shape, is an automatic failure.

## 11. Interfaces

- Upstream: `ci-cd-pipelines`, `containerization`,
  `environment-management`, `database-operations`.
- Downstream: `production-verification`, `observability`,
  `release-engineering`, `client-handover`.
