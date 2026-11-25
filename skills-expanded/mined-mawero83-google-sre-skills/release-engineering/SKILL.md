---
name: release-engineering
description: >-
  Apply Google release engineering: repeatable builds, hermeticity, policy as code, and separation of release roles. Use when improving CI/CD reliability and release process design.
---

# Release Engineering

**Domain:** `delivery`  
**Sources:** SRE Book 1e Ch8, SRE Book 2e Ch14

## When to use

- CI/CD reliability problems
- Release process redesign
- Emergency release path design

## Principles

- Releases should be automated, repeatable, and policy-enforced.
- Build once; promote artifacts; avoid snowflake prod builds.
- Fast, safe rollback is a feature of the release system.
- Release engineering partners with SRE on change risk.

## Workflow

1. Map current path: commit → artifact → environments → prod.
2. Find non-hermetic steps and manual gates without evidence.
3. Add artifact provenance, tests gates, and progressive delivery hooks.
4. Define emergency release path that is still audited.
5. Measure change failure rate and time-to-rollback.

## Decision guide

- If rollback > 15–30 min for critical services → treat as reliability bug.

## Output template

```markdown
# Release engineering review
- Path:
- Risks:
- Hermeticity gaps:
- Rollback story:
- Actions:
```

## Anti-patterns

- Hand-built prod binaries.
- Untested hotfixes as culture.

## Related skills

`canarying-releases`, `testing-for-reliability`, `configuration-design`

## Canonical references

- [Release Engineering](https://sre.google/sre-book/release-engineering/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
