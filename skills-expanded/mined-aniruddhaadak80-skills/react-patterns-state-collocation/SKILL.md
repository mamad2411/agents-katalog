---
name: react-patterns-state-collocation
description: "Choose between local state, lifted state, URL state, and stores by asking who needs the data and when."
---
# Colocate state where it is consumed

> Choose between local state, lifted state, URL state, and stores by asking who needs the data and when.

**Track:** 🎨 Frontend Engineering · **Domain:** React Patterns · **Level:** foundation · **~25 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Choose between local state, lifted state, URL state, and stores by asking who needs the data and when.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Start local with useState; lift only when a sibling truly needs it
2. Move shareable UI state (tab, sort, filters) into URL search params
3. Use a store only for cross-tree client state that changes often
4. Derive values during render instead of syncing via effects
5. Keep server data in a query cache, never copied into local state
6. Delete any effect whose dependency list keeps growing to mirror other state

## Common Pitfalls

- Duplicating server data into useState then fighting staleness
- Global store as default dumping ground

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill react-patterns-state-collocation
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill react-patterns-state-collocation -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills