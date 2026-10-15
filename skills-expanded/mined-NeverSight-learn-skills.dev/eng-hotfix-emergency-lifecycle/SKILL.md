---
name: eng-hotfix-emergency-lifecycle
description: Execute the fast-track emergency hotfix pipeline for P0 and P1 production incidents with time-boxed root cause isolation, surgical repair, targeted smoke regression, tagged emergency delivery, and mandatory postmortem. Use during live incident response.
---

# Emergency Hotfix Lifecycle

Provides the fast lane for production incidents: minimum ceremony with maximum safety rails. Skips full SDD freezing by design and compensates with a mandatory postmortem.

## 5-Stage Pipeline State Machine

```
Stage 1: Minimal Repro & Root Cause Lock (time-boxed)
           │
           ▼
[Gate: Human Hotfix Approval - production action]
           │
           ▼
Stage 2: Surgical Fix Implementation (smallest safe diff)
           │
           ▼
Stage 3: Targeted Smoke Regression (affected paths only)
           │
           ▼
Stage 4: Emergency Commit on hotfix/<incident-id> branch + PR
           │
           ▼
Stage 5: Postmortem Report (root cause, timeline, prevention)
```

---

## Autonomous Execution Protocol

1. **Execute Stage 1 (Root Cause Lock)**: Reproduce the failure with the narrowest possible case and time-box this stage. If the cause cannot be locked quickly, escalate to the user with collected evidence instead of guessing.
2. **Gate (Human Approval)**: Present the symptom, root cause, blast radius, proposed minimal diff, and rollback plan. Proceed only on explicit approval because this touches production behavior.
3. **Execute Stage 2 (Surgical Fix)**: Apply the smallest diff that removes the failure mode. No opportunistic refactoring.
4. **Execute Stage 3 (Smoke Regression)**: Run only the tests covering affected paths plus the previously passing suite subset relevant to the change surface.
5. **Execute Stage 4 (Emergency Delivery)**: Commit on a `hotfix/<incident-id>` branch with a conventional commit message, open the PR, and label it with the incident priority.
6. **Execute Stage 5 (Postmortem)**: After stabilization, write `.agents/prod-execution-reports/postmortem-<incident-id>.md` covering the timeline, root cause, detection gap, and prevention actions.

## State Persistence & Resumption

Record pipeline progress in `.agents/lifecycle-state.json`:

```
{
  "feature": "<incident-id>",
  "pipelineType": "emergency-hotfix",
  "currentStage": 3,
  "stageName": "smoke-regression",
  "completedStages": [
    "root-cause-lock",
    "surgical-fix"
  ],
  "lastUpdated": "YYYY-MM-DDTHH:mm:ssZ"
}
```

## Checkable Completion Criteria

- [ ] Root cause locked with reproducible evidence before any fix.
- [ ] Explicit human approval captured before touching shared branches.
- [ ] Minimal diff merged with smoke tests green.
- [ ] Hotfix branch labeled and PR opened.
- [ ] Postmortem document completed after stabilization.