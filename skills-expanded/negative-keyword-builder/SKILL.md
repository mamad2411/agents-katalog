---
name: negative-keyword-builder
description: 'Turn confirmed bad-fit searches into a safe, approval-ready negative keyword draft with match types, scope, and collision checks. Use after search-term review, before excluding traffic.'
---

# Negative Keyword Builder

## Doctrine

A negative keyword can save spend or quietly remove good demand. Draft from confirmed bad-fit queries, choose the narrowest useful scope, and test the proposed negative against protected searches and positive keywords. Exact, phrase, and broad negatives behave differently from positive keywords and do not cover every close variant.

## When to use

- After the Search Term Miner has produced confirmed exclude candidates.
- Use a connected Google Ads MCP for read-only context, or paste the candidates, current negatives, positive keywords, campaign purposes, and protected queries.
- Bring separate Brand, Careers, Support, or content campaign purposes so a useful query is not blocked account-wide.

## Run it

```
Build a READ-ONLY negative keyword draft. Use live account data for context if connected; otherwise use what I paste. Do not add anything to Google Ads.

1. Confirm the exclude candidates, source queries, campaign and ad group, current negative lists, positive keywords, campaign purpose, and protected brand or high-intent queries.
2. For every proposed negative show: negative text, negative match type, scope, source queries, reason, collision test, protected queries, risk, and "approval required".
3. Use the narrowest scope that solves the problem. Keep Brand, Careers, Support, and intentional free or educational campaigns protected from acquisition-campaign negatives.
4. Apply Google negative-match mechanics correctly:
   - negative broad blocks when all negative terms appear, in any order;
   - negative phrase blocks when the full phrase appears in the same order;
   - negative exact blocks only that exact query;
   - negatives do not automatically cover every close variant, so show necessary singular, plural, or synonym checks.
5. Test each draft against current positive keywords and at least 5 plausible good queries. If a useful query would be blocked, narrow the text, match type, or scope.
6. Put ambiguous candidates in a hold list instead of forcing a negative.

Return an upload-ready table, but make no changes. End with "Approval required for every row. No changes were made."
```

## Guardrails

- Never invent a negative that is not supported by the supplied business exclusions or source queries.
- Do not use a one-word account-wide negative when a phrase, exact query, campaign scope, or ad-group scope is safer.
- Exact negative `payroll template` does not block `free payroll spreadsheet template`. Check the actual mechanics before calling a row covered.
- Words such as "free", "cheap", "login", "jobs", and "how to" can be useful in the right campaign. Protect intentional demand.
- Draft only. Adding a negative is a reach-reducing account change and still requires explicit row-level approval.

## Good output looks like

A small, upload-ready negative list whose scope and match type can be explained, with the good queries it protects and every row waiting for approval.
