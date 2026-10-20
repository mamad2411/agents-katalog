---
name: automation-e2e-maintainable-selectors-pw
description: "Selector strategy and structure choices keeping end-to-end suites maintainable through UI churn."
---
# Write E2E tests that survive redesigns (Playwright)

> Selector strategy and structure choices keeping end-to-end suites maintainable through UI churn.

**Track:** 🧪 QA & Testing · **Domain:** Test Automation · **Level:** intermediate · **~35 min**

**Who this is for:** QA Engineers, SDETs, Test Automation Engineers, Developers

## When to Use This Skill

Selector strategy and structure choices keeping end-to-end suites maintainable through UI churn.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Locate elements by accessible role/name — resilient AND forces a11y
2. Ban generated class names and nth-child position selectors
3. Model flows in helpers once; tests read as user intent scripts
4. Assert observable outcomes (row appears) over DOM internals
5. Seed state via APIs/fixtures, never UI-only setup chains
6. Keep each spec independent: any subset passes on fresh context
7. Prefer getByRole/getByLabel over CSS/XPath chains
8. Use web-first assertions auto-waiting instead of sleeps

## Common Pitfalls

- Page objects becoming second app full of logic
- Chained UI setups breaking one hop upstream

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill automation-e2e-maintainable-selectors-pw
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill automation-e2e-maintainable-selectors-pw -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills