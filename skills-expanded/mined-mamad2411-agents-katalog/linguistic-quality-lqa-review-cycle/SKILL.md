---
name: linguistic-quality-lqa-review-cycle
description: "In-context review, error typology scoring, and vendor feedback loops improving over releases."
---
# Run linguistic QA that catches real errors

> In-context review, error typology scoring, and vendor feedback loops improving over releases.

**Track:** 🌐 Localization & i18n · **Domain:** Linguistic Quality · **Level:** intermediate · **~35 min**

**Who this is for:** Localization Engineers, i18n Developers, Localization Managers, Transcreators

## When to Use This Skill

In-context review, error typology scoring, and vendor feedback loops improving over releases.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Review IN CONTEXT on real builds, not spreadsheet columns
2. Score errors by typology: accuracy, terminology, style, locale convention, typo
3. Critical (misleading/damaging) blocks release; minor batches into next sprint
4. Feedback to translators references error codes + suggested fix + why
5. Maintain per-product glossary and termbase; enforce in tooling
6. Track error density trend per locale/vendor as the quality metric

## Common Pitfalls

- Reviewing strings in isolation missing truncation and gender clashes
- Subjective style nitpicks weighted like factual errors

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill linguistic-quality-lqa-review-cycle
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill linguistic-quality-lqa-review-cycle -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills