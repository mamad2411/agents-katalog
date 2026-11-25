---
name: rendering-strategy-web-workers-architecture
description: "Worker pool sizing, transferable payloads, and Comlink-style RPC keeping UI at 60fps."
---
# Move heavy work off the main thread properly

> Worker pool sizing, transferable payloads, and Comlink-style RPC keeping UI at 60fps.

**Track:** 🎨 Frontend Engineering · **Domain:** Rendering Strategy · **Level:** advanced · **~45 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Worker pool sizing, transferable payloads, and Comlink-style RPC keeping UI at 60fps.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Profile first: identify tasks blocking main thread >50ms consistently
2. Pool workers = hardwareConcurrency minus reserve; reuse, don't spawn per task
3. Transfer ArrayBuffers instead of structured-cloning large payloads
4. Design message protocol versioned — workers update independently of pages
5. Fallback to main-thread execution behind feature detection for old browsers
6. Guard against worker startup latency for tiny tasks — often net-negative

## Common Pitfalls

- PostMessage cloning multi-MB datasets negating compute savings
- Workers importing entire app bundles via accidental transitive imports

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill rendering-strategy-web-workers-architecture
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill rendering-strategy-web-workers-architecture -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills