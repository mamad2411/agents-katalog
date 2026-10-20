---
name: evaluation-integrity-datasheet-documentation
description: "Provenance, composition, collection process, and limitations recorded before modeling begins."
---
# Document datasets with datasheets

> Provenance, composition, collection process, and limitations recorded before modeling begins.

**Track:** 🧮 ML Research Engineering · **Domain:** Evaluation Integrity · **Level:** foundation · **~30 min**

**Who this is for:** Research Engineers, ML Scientists, PhD Researchers, Applied Scientists

## When to Use This Skill

Provenance, composition, collection process, and limitations recorded before modeling begins.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Record provenance chain: sources, licenses, consent basis for personal data
2. Quantify composition: demographics/classes/languages with known skews stated
3. Document collection mechanics and any filtering applied
4. List known failure modes and unsuitable-use cases explicitly
5. Version datasheets with dataset versions — they evolve together
6. Review for PII leakage risks with fresh eyes before release

## Common Pitfalls

- Datasets inherited without provenance entering production models
- Limitations sections written only when reviewers ask

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill evaluation-integrity-datasheet-documentation
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill evaluation-integrity-datasheet-documentation -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills