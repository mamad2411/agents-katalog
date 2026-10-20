---
name: detection-operations-detcode-testing
description: "Atomic test fixtures, expected-fire assertions, and regression packs keeping detection debt visible."
---
# Test detections like code with unit + integration suites

> Atomic test fixtures, expected-fire assertions, and regression packs keeping detection debt visible.

**Track:** 🔐 Cybersecurity · **Domain:** Detection Operations · **Level:** advanced · **~45 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Atomic test fixtures, expected-fire assertions, and regression packs keeping detection debt visible.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Every rule ships with fixture events that MUST fire + MUST-NOT-fire neighbors
2. Run rule suites against synthetic telemetry in CI on every change
3. Track rule precision/recall over time like code coverage trends
4. Version rules semantically; logic changes bump minor, tuning patches
5. Quarantine flaky environment-dependent rules visibly, fix root cause
6. Report suite health to leadership: rules tested %, drift count

## Common Pitfalls

- Rules edited live in SIEM UIs diverging from repo truth
- Fixtures rotting until they validate nothing anymore

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill detection-operations-detcode-testing
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill detection-operations-detcode-testing -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills