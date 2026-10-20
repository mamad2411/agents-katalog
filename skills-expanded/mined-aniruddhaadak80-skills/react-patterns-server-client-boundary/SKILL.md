---
name: react-patterns-server-client-boundary
description: "Decide what renders on the server versus client in React Server Components to minimize JavaScript shipped."
---
# Draw the server/client component boundary

> Decide what renders on the server versus client in React Server Components to minimize JavaScript shipped.

**Track:** 🎨 Frontend Engineering · **Domain:** React Patterns · **Level:** intermediate · **~30 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Decide what renders on the server versus client in React Server Components to minimize JavaScript shipped.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Default every component to server-rendered; add interactivity at the leaves
2. Push 'use client' down to the smallest interactive subtree (buttons, inputs)
3. Fetch data in server components; pass plain serializable props downward
4. Never import server-only secrets from a client module, even indirectly
5. Keep providers minimal: theme/auth wrappers are client, pages stay server
6. Audit bundle after each feature: any client component over 15KB needs justification

## Common Pitfalls

- One 'use client' at page level dragging the whole tree into the bundle
- Passing functions or class instances across the boundary

## Success Signals

- Client JS per route under 120KB gzipped
- Zero hydration mismatch warnings

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill react-patterns-server-client-boundary
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill react-patterns-server-client-boundary -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills