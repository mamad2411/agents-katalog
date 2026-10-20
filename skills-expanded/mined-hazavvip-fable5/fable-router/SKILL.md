---
name: fable-router
description: Fable phase router with target_class fork
version: 8.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# Fable Router

1. Read `docs/WORKFLOW_CANON.md`, `docs/TARGET_CLASS_CANON.md`, `fable/OBJECTIVES.md`
2. After recon: CLASSIFY_TARGET in fingerprint.json
3. Route by target_class:

| target_class | Next phase(s) |
|--------------|---------------|
| cms_shared_hosting | initial-access |
| spa_saas_api | application-logic |
| api_only | application-logic |
| hybrid | initial-access + application-logic |

4. Load `Workflow/{current_phase}/PLAYBOOK.md`

Skills: `fable-app-mapping` (recon), `fable-application-logic`, `fable-logic-verification` (execution).
