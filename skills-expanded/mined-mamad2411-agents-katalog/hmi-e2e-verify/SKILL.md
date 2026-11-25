---
name: hmi-e2e-verify
description: >-
  Verify industrial HMI operator flows (Init / Start / Stop / Abort / Recover)
  and settings forms with structured evidence. Use when validating frontend
  changes, operator gates, lifecycle presentation, or writing verification
  reports under docs/verification/.
---

# HMI E2E verify

## Purpose

Replace one-off JSON traces with a reusable operator verification gate. Pass criteria: connectivity healthy enough to run, lifecycle transitions correct, no orphan motion commands.

## Read first

1. `docs/LIFECYCLE_AND_JOB_QUEUE.md`
2. `.cursor/rules/industrial-hmi.mdc`, `.cursor/rules/frontend.mdc`
3. `frontend/src/types/machineLifecycle.types.ts`

## Stack notes

- HMI: `frontend/` (Vite + React)
- Existing scripts: `backend/scripts/hmi-settings-e2e.mjs`, `backend/scripts/e2e-centring-fixes.mjs`
- No Playwright pack in-repo yet — prefer browser MCP + scripts; add Playwright under `frontend/` only when intentionally introducing it
- Stub/SIM hardware in CI when `SIMULATE_HARDWARE` (or project equivalent) is available

## Operator flow checklist

```
Progress:
- [ ] 1. Start API + HMI (or attach to running cell)
- [ ] 2. Connectivity: Vision + Nanos + EtherCAT shown on init-status
- [ ] 3. Init → expected lifecycle IDLE (or documented ready state)
- [ ] 4. Start → RUN / phase labels match backend codes
- [ ] 5. Stop or Abort → safe idle; Abort ≠ ESTOP
- [ ] 6. Fault / Recover path if exercised
- [ ] 7. Settings form: units, ranges, ACL gates, save success/error
- [ ] 8. No orphan motion (no continuous busy without operator intent)
- [ ] 9. Write report under docs/verification/
```

## Browser MCP practice

1. Navigate to HMI URL
2. Snapshot → interact → screenshot for each gate
3. Lock during automation; unlock when finished
4. Capture console/network failures

## Report schema

Write `docs/verification/YYYYMMDD-HHMM-<topic>.md`:

```markdown
# HMI verification — <topic>
- Date / git SHA:
- Environment: SIM | cell LAN | kiosk
- Connectivity: pass/fail (details)
- Lifecycle Init/Start/Stop/Abort/Recover: pass/fail per step
- Settings touched:
- Screenshots / script output:
- Defects:
- Sign-off:
```

## Validation helpers

```bash
npm run build --prefix frontend
node backend/scripts/hmi-settings-e2e.mjs
npm test --prefix backend
```

## Pass criteria

- [ ] Connectivity section understood (not ignored)
- [ ] Lifecycle labels match backend
- [ ] Critical actions have confirmation where required
- [ ] Report filed under `docs/verification/`
