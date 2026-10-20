---
name: gameplay-systems-game-feel-tuning
description: "Juice systems — input buffering, coyote time, screen feedback — tuned via live-adjustable parameters."
---
# Tune game feel with parameter discipline

> Juice systems — input buffering, coyote time, screen feedback — tuned via live-adjustable parameters.

**Track:** 🎮 Game & Interactive Dev · **Domain:** Gameplay Systems · **Level:** intermediate · **~35 min**

**Who this is for:** Game Developers, Technical Designers, Live-Ops Engineers, Indie Devs

## When to Use This Skill

Juice systems — input buffering, coyote time, screen feedback — tuned via live-adjustable parameters.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Expose movement/combat parameters to a runtime debug panel
2. Add input buffering (100-150ms) before touching anything else
3. Add coyote time (~100ms) and jump buffering for platformers immediately
4. Layer feedback per action: animation, sound, particle, camera nudge, hitstop
5. Tune one parameter set at a time; record clips comparing before/after
6. Playtest with controller AND touch/keyboard; feel differs per input

## Common Pitfalls

- Hardcoded magic numbers nobody dares retune
- Juice added after systems freeze, breaking balance

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill gameplay-systems-game-feel-tuning
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill gameplay-systems-game-feel-tuning -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills