---
name: gameplay-systems-save-system-design
description: "Versioned, forward-compatible saves with migration paths protecting player progress."
---
# Design save systems that survive updates

> Versioned, forward-compatible saves with migration paths protecting player progress.

**Track:** 🎮 Game & Interactive Dev · **Domain:** Gameplay Systems · **Level:** intermediate · **~30 min**

**Who this is for:** Game Developers, Technical Designers, Live-Ops Engineers, Indie Devs

## When to Use This Skill

Versioned, forward-compatible saves with migration paths protecting player progress.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Serialize data by key-value schema with explicit version field
2. Write migrations as ordered transforms; never assume latest on load
3. Keep save atomic: write temp + rename to avoid corruption on crash
4. Cloud-sync conflict policy defined (newest-wins vs merge) and tested
5. Back up previous save slot automatically before migrating
6. Test loading every historical version in CI nightly

## Common Pitfalls

- Binary blobs unreadable after class renames
- Corrupted-save reports traced to mid-write power loss

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill gameplay-systems-save-system-design
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill gameplay-systems-save-system-design -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills