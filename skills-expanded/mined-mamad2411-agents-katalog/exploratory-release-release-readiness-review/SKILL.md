---
name: exploratory-release-release-readiness-review
description: "Checklist verdicts across quality signals making go/no-go boring and defensible."
---
# Gate releases with a readiness review

> Checklist verdicts across quality signals making go/no-go boring and defensible.

**Track:** 🧪 QA & Testing · **Domain:** Exploratory & Release · **Level:** foundation · **~25 min**

**Who this is for:** QA Engineers, SDETs, Test Automation Engineers, Developers

## When to Use This Skill

Checklist verdicts across quality signals making go/no-go boring and defensible.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Collect: automated pass rates, open severity counts, perf deltas
2. Verify rollback plan exists and was rehearsed this cycle
3. Confirm monitoring dashboards updated for new surfaces
4. Legal/support/comms sign-offs for customer-visible changes
5. Decision recorded with dissent noted — no silent overrides
6. Post-release retro compares predicted vs actual issues

## Common Pitfalls

- Go/no-go theater after decision already made upstream
- Severity-3 backlog blocking honest signal reading

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill exploratory-release-release-readiness-review
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill exploratory-release-release-readiness-review -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills