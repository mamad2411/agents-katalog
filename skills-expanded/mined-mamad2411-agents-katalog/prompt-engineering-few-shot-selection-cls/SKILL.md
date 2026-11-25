---
name: prompt-engineering-few-shot-selection-cls
description: "Choose and order examples covering edge cases so the model generalizes instead of copying surface patterns."
---
# Select few-shot examples that move accuracy (Classification tasks)

> Choose and order examples covering edge cases so the model generalizes instead of copying surface patterns.

**Track:** 🤖 AI Engineering · **Domain:** Prompt Engineering · **Level:** intermediate · **~30 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Choose and order examples covering edge cases so the model generalizes instead of copying surface patterns.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Cover each output field's edge cases once: empty, unicode, long input, ambiguity
2. Order examples easy-to-hard so difficulty ramps within context
3. Match example format byte-for-byte to the required output format
4. Prefer real production samples over invented ones
5. Rotate in failure cases you fixed, turning regressions into teachers
6. Measure: remove one example at a time, drop any whose removal costs nothing
7. Include one deliberately ambiguous item with the correct tie-break label
8. Balance classes in examples; imbalance biases predictions

## Common Pitfalls

- Six near-identical easy examples teaching style but not judgment
- Whitespace mismatches between examples and instructions

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill prompt-engineering-few-shot-selection-cls
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill prompt-engineering-few-shot-selection-cls -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills