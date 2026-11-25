---
name: automation-flaky-test-elimination
description: "Quarantine, root-cause classes, and stabilization patterns restoring CI trustworthiness."
---
# Eliminate flaky tests systematically

> Quarantine, root-cause classes, and stabilization patterns restoring CI trustworthiness.

**Track:** 🧪 QA & Testing · **Domain:** Test Automation · **Level:** advanced · **~40 min**

**Who this is for:** QA Engineers, SDETs, Test Automation Engineers, Developers

## When to Use This Skill

Quarantine, root-cause classes, and stabilization patterns restoring CI trustworthiness.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Auto-detect flakiness via retry-pass detection; report rate weekly
2. Quarantine flaky tests immediately — a red CI must mean something
3. Root-cause by class: timing/sleep → explicit waits; order-dependence → isolation
4. Fix test-data collisions with unique-per-run factories
5. Stabilize environment noise: ports, clocks, network mocks
6. Burn down quarantine weekly; two-strikes rule for chronic offenders

## Common Pitfalls

- Auto-retry hiding flake instead of surfacing it
- Deleting flaky tests silently losing coverage

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill automation-flaky-test-elimination
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill automation-flaky-test-elimination -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills