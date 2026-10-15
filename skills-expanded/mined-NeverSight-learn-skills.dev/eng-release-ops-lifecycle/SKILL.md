---
name: eng-release-ops-lifecycle
description: Orchestrate production release operations automatically covering pre-flight inventory, zero-downtime container updates, optional server hardening, health verification, rollback planning, and an operations report. Use when executing release windows or routine production maintenance.
---

# Release & Production Operations Lifecycle

Automates the recurring release and maintenance workflow while keeping humans in command of the production window decision.

## 5-Stage Pipeline State Machine

```
Stage 1: Pre-flight Inventory (targets, images, configs)
           │
           ▼
[Gate: Human Release Window Approval]
           │
           ▼
Stage 2: eng-docker-update (digest diff, zero-downtime recreation)
           │
           ▼
Stage 3: eng-linux-security Hardening (optional flag)
           │
           ▼
Stage 4: Health Verification + Rollback Plan Generation
           │
           ▼
Stage 5: Operations Report at .agents/release-reports/<release-id>.md
```

---

## Autonomous Execution Protocol

1. **Execute Stage 1 (Pre-flight Inventory)**: Enumerate compose stacks, current image digests, target hosts, exposed ports, and volume mounts. Verify all configuration paths resolve on the target environment.
2. **Gate (Human Approval)**: Present the change set (old digest vs new digest per service), maintenance window, and rollback triggers. Proceed only on explicit approval.
3. **Execute `eng-docker-update`**: Perform image digest comparison and zero-downtime container recreation with health probes between batches.
4. **Execute `eng-linux-security`** (optional): Include this stage when the user requests server hardening during the same window.
5. **Execute Stage 4 (Health & Rollback)**: Probe every service endpoint, verify logs are free of fatal errors, and generate an executable rollback plan mapping each service to its previous digest.
6. **Execute Stage 5 (Report)**: Save the operations report to `.agents/release-reports/<release-id>.md` covering applied changes, probe results, and rollback instructions.

## State Persistence & Resumption

Record pipeline progress in `.agents/lifecycle-state.json`:

```
{
  "feature": "<release-id>",
  "pipelineType": "release-ops",
  "currentStage": 2,
  "stageName": "eng-docker-update",
  "completedStages": [
    "pre-flight-inventory"
  ],
  "lastUpdated": "YYYY-MM-DDTHH:mm:ssZ"
}
```

## Checkable Completion Criteria

- [ ] Pre-flight inventory verified against the real target environment.
- [ ] Explicit human approval captured for the release window.
- [ ] All container recreations passed health probes.
- [ ] Executable rollback plan produced covering every changed service.
- [ ] Operations report saved to `.agents/release-reports/`.