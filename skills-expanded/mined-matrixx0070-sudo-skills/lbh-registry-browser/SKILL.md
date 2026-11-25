---
name: lbh-registry-browser
version: 1.0.0
description: Browse the community legal-skills registry — search, filter, and shortlist candidate skills before any evaluation or install.
author: matrixx0070
tags: [legal, registry, discovery, search, catalog]
capabilities: []
---

## When to use

Use this when a user needs a legal capability (contract review, clause drafting, jurisdiction lookup) and you want to discover what community skills already exist before building anything. This is the front door of the Legal Builder Hub: it turns a vague need into a ranked shortlist of named registry entries.

**Not for:** deciding whether a shortlisted skill is safe (use `lbh-skills-qa`), installing it (use `lbh-skill-installer`), or first-time users who don't yet know what they need (use `lbh-cold-start-interview`).

## Method

1. Restate the legal need as a capability phrase plus jurisdiction and document type — e.g. "NDA mutual, US-Delaware, review".
2. Query the registry index by tag, then by full-text description. Prefer tag matches; treat description matches as secondary.
3. Filter out entries that fail hard gates: no author, no version, no license, or last-updated older than your staleness threshold (default 18 months).
4. Rank survivors by fit: capability match, jurisdiction match, install count, and recency. Break ties toward higher review scores.
5. Emit a shortlist of 3-5 entries with the one fact that would disqualify each, so the next step (QA) has a head start.
6. Never present a match as "recommended" — you surface candidates; the security gate decides.

## Example

Need: "review a SaaS subscription agreement, EU/GDPR". You query tags `[contract-review, saas, gdpr]`, get 11 hits, drop 4 with no license and 2 stale, and rank the rest. Top candidate: `saas-agreement-eu-review v2.1`, 900 installs, updated 3 months ago, flag "author unverified — needs QA".

## Pitfalls

- Treating install count as a safety signal. Popularity is not vetting; a popular skill can still fetch remote code.
- Matching on description keywords only, so a US-only skill surfaces for an EU query. Jurisdiction is a hard filter, not a ranking nudge.
- Presenting one "best" result and skipping the gate. Always hand off a shortlist to QA.

## Output format

```
# Registry Shortlist — <need>
NEED: capability=<...> jurisdiction=<...> doc=<...>
CANDIDATES (ranked):
1. <name> v<ver> — installs=<n> updated=<date> — DISQUALIFIER RISK: <one line>
2. ...
DROPPED: <name> (<hard-gate reason>) ...
NEXT: run lbh-skills-qa on top candidate(s)
```

## Reference

**Skill-vetting checklist (discovery layer):** present author, version, license, description, source URL, last-updated date; jurisdiction and doc-type declared; capabilities list not empty of meaning.

**Security-review gate criteria (pre-filter):** entries requesting network fetch, filesystem write, or dynamic code load are flagged HIGH before they reach the shortlist, never silently ranked.

**Versioning / rollback:** always record the exact `name@version` you shortlisted so a later install and any rollback target the same immutable coordinate. Prefer pinned versions over "latest".
