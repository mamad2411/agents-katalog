---
name: playbook-frontend-engineering-a11y-pass
description: "Reach keyboard-complete, screen-reader-navigable flows on core journeys."
---
# Playbook: Make an existing app accessible

> Reach keyboard-complete, screen-reader-navigable flows on core journeys.

**Track:** 🗺️ Frontend Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~65 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Reach keyboard-complete, screen-reader-navigable flows on core journeys.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Run a practical accessibility audit pass: start with "Automate first: axe scan on key routes, triage all criticals"
2. Step 2 — Write semantic markup before reaching for ARIA: start with "Choose native elements: button not clickable-div, real headings in order"
3. How it fits together: Audit → triage criticals → fix patterns not pages. Patterns prevent the next audit finding everything again.

### Referenced Skills

- `accessibility-a11y-audit-pass`
- `accessibility-semantic-first-markup`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill accessibility-a11y-audit-pass && npx skills add aniruddhaadak80/skills --skill accessibility-semantic-first-markup
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills