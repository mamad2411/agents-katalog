---
name: docs-systems-docs-as-code-workflow
description: "Versioned markdown, PR reviews, link checks, and preview deploys keeping docs trustworthy."
---
# Run docs through the same pipeline as code

> Versioned markdown, PR reviews, link checks, and preview deploys keeping docs trustworthy.

**Track:** ✍️ Technical Writing · **Domain:** Documentation Systems · **Level:** intermediate · **~30 min**

**Who this is for:** Technical Writers, Developer Advocates, Engineers Who Document, Content Leads

## When to Use This Skill

Versioned markdown, PR reviews, link checks, and preview deploys keeping docs trustworthy.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Store docs beside code or in sibling repo with same review gates
2. CI checks links, style rules, and builds previews per PR
3. Enforce frontmatter metadata: owner, last-verified date, audience
4. Broken-build rule applies: failing docs checks block merges
5. Auto-generate changelog-driven updates for API surfaces
6. Quarterly stale-sweep: unverified pages get flagged visibly

## Common Pitfalls

- Wiki graveyards outside any workflow
- Screenshots rotting after every UI release

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill docs-systems-docs-as-code-workflow
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill docs-systems-docs-as-code-workflow -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills