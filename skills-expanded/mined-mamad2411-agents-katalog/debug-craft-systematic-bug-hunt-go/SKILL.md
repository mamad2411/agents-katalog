---
name: debug-craft-systematic-bug-hunt-go
description: "Reproduce, bisect, hypothesize, verify — the method that beats random poking under deadline pressure."
---
# Hunt bugs systematically (Go)

> Reproduce, bisect, hypothesize, verify — the method that beats random poking under deadline pressure.

**Track:** 🧰 Engineering Essentials · **Domain:** Debugging Craft · **Level:** foundation · **~30 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Reproduce, bisect, hypothesize, verify — the method that beats random poking under deadline pressure.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Reproduce deterministically first; flaky repro = flaky fix
2. Write failing test capturing the bug before touching source
3. Bisect history or code path until minimal failing case remains
4. Form ONE hypothesis, predict its observable, then check
5. Fix root cause, not nearest symptom; add regression test
6. Document the hunt briefly for future searchers
7. Run pprof profiles; check goroutine leaks with goleak
8. Enforce vet/lint gates; keep error wrapping with %w intact

## Common Pitfalls

- Shotgun changes stacking unknown unknowns
- Fixing symptoms while root cause ships elsewhere

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill debug-craft-systematic-bug-hunt-go
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill debug-craft-systematic-bug-hunt-go -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills