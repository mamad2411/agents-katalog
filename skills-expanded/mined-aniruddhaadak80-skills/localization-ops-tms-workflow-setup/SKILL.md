---
name: localization-ops-tms-workflow-setup
description: "CAT/TMS pipelines, string freezes, and cost controls making localization routine not heroic."
---
# Set up translation management workflows

> CAT/TMS pipelines, string freezes, and cost controls making localization routine not heroic.

**Track:** 🌐 Localization & i18n · **Domain:** Localization Operations · **Level:** intermediate · **~35 min**

**Who this is for:** Localization Engineers, i18n Developers, Localization Managers, Transcreators

## When to Use This Skill

CAT/TMS pipelines, string freezes, and cost controls making localization routine not heroic.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Connect repo-to-TMS sync so keys flow automatically both directions
2. Enforce string freeze windows before release branches cut
3. Route content types appropriately: UI strings ≠ marketing ≠ legal
4. Configure translation memory + glossary enforcement in CAT tooling
5. Track wordage velocity and cost per locale monthly
6. Test localized builds before merge, not after release notes go out

## Common Pitfalls

- Late-string drops bypassing translation entirely
- TM reuse ignored, paying repeatedly for identical sentences

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill localization-ops-tms-workflow-setup
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill localization-ops-tms-workflow-setup -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills