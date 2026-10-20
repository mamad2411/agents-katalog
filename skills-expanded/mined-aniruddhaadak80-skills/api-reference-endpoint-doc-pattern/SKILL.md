---
name: api-reference-endpoint-doc-pattern
description: "Every endpoint documented with working request, realistic response, and error table."
---
# Document endpoints developers can copy-paste

> Every endpoint documented with working request, realistic response, and error table.

**Track:** ✍️ Technical Writing · **Domain:** API Reference & Guides · **Level:** intermediate · **~30 min**

**Who this is for:** Technical Writers, Developer Advocates, Engineers Who Document, Content Leads

## When to Use This Skill

Every endpoint documented with working request, realistic response, and error table.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Lead with minimal working request using realistic sandbox data
2. Show full response body, not truncated ellipses
3. Error section lists codes with causes AND fixes
4. Note rate limits, auth scopes, and idempotency behavior inline
5. Provide copyable snippets in three top languages minimum
6. Test every example in CI against staging nightly

## Common Pitfalls

- Examples with fake keys that fail when tried
- Parameter tables without units or formats

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill api-reference-endpoint-doc-pattern
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill api-reference-endpoint-doc-pattern -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills