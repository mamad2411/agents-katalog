---
name: experimentation-rigor-paper-reproduction-protocol
description: "Staged reproduction from inference-first to full retrain with deviation journals."
---
# Reproduce papers without drowning

> Staged reproduction from inference-first to full retrain with deviation journals.

**Track:** 🧮 ML Research Engineering · **Domain:** Experimentation Rigor · **Level:** advanced · **~50 min**

**Who this is for:** Research Engineers, ML Scientists, PhD Researchers, Applied Scientists

## When to Use This Skill

Staged reproduction from inference-first to full retrain with deviation journals.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Stage 0: run authors' code if available; record environment verbatim
2. Stage 1: reimplement inference on their checkpoint; compare outputs numerically
3. Stage 2: retrain smallest configuration matching reported metrics ±noise band
4. Journal EVERY deviation from paper text with suspected impact
5. Contact authors once with specific questions — response rate rewards clarity
6. Publish reproduction report regardless of outcome; negatives are valuable

## Common Pitfalls

- Jumping straight to full-scale retraining
- Undocumented 'small' tweaks compounding into irreproducibility

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-rigor-paper-reproduction-protocol
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-rigor-paper-reproduction-protocol -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills