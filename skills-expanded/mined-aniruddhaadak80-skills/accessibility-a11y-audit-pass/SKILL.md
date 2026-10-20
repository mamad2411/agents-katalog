---
name: accessibility-a11y-audit-pass
description: "Combine automated scans with keyboard and screen-reader passes to find issues tools miss."
---
# Run a practical accessibility audit pass

> Combine automated scans with keyboard and screen-reader passes to find issues tools miss.

**Track:** 🎨 Frontend Engineering · **Domain:** Accessibility · **Level:** intermediate · **~40 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Combine automated scans with keyboard and screen-reader passes to find issues tools miss.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Automate first: axe scan on key routes, triage all criticals
2. Unplug the mouse: complete every core flow keyboard-only
3. Listen once with a screen reader through signup and checkout
4. Check focus visibility, order, and trap-free modals manually
5. Verify contrast against actual rendered colors including disabled states
6. File findings with WCAG criterion references and own fixes within sprint

## Common Pitfalls

- Trusting automated score as proof of compliance
- outline:none without a visible replacement

## Success Signals

- Zero critical axe issues
- All flows completable keyboard-only

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill accessibility-a11y-audit-pass
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill accessibility-a11y-audit-pass -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills