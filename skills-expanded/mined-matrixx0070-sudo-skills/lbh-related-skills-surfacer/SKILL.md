---
name: lbh-related-skills-surfacer
version: 1.0.0
description: Surface legal skills related to what a user already installed or is viewing — complements, prerequisites, and safer alternatives — as a vetting-first shortlist.
author: matrixx0070
tags: [legal, recommendation, discovery, complements, alternatives]
capabilities: []
---

## When to use

Use this to suggest what else a user might need given their current context — after they install a skill, view a registry entry, or finish a workflow. It maps relationships (this drafts, that reviews; this needs that as a prerequisite) and offers safer alternatives when a chosen skill is borderline.

**Not for:** the primary search a user drives themselves (`lbh-registry-browser`), the safety decision (`lbh-skills-qa`), or installing (`lbh-skill-installer`). You surface candidates; the gate still decides.

## Method

1. Anchor on context: the installed or viewed skill's capability, jurisdiction, and doc type.
2. Find complements — skills that operate on the same document at a different lifecycle stage (draft → review → negotiate → file).
3. Find prerequisites — skills whose output the anchor consumes, or shared jurisdiction packs it assumes.
4. Find safer alternatives — same capability, cleaner security posture — especially when the anchor carries elevated conditions.
5. Filter every suggestion through the discovery hard gates (author, version, license, recency) before showing it.
6. Present a small, reasoned set (max 4) with the relationship type and a one-line risk note each, and route the chosen one to QA.

## Example

User just installed `nda-draft@1.2` (US-DE). You surface: complement `nda-review@2.0` (same doc, review stage), prerequisite `us-jurisdiction-pack@1.1` (clause definitions it references), and a safer alternative to a borderline redliner they were eyeing. Each carries a risk note; the user picks review, you hand `nda-review@2.0` to `lbh-skills-qa`.

## Pitfalls

- Recommending on similarity alone, so an unvetted or stale skill gets surfaced as a "related" pick. Apply hard gates first.
- Suggesting a cross-jurisdiction skill as a complement. Related must share or correctly extend jurisdiction.
- Flooding the user with options. Cap at four, each with a clear relationship reason.
- Presenting a suggestion as endorsed. Every surfaced skill still passes through the security gate before install.

## Output format

```
# Related Skills — anchored on <name>@<ver>
COMPLEMENTS: <name>@<ver> (stage:<...>) risk:<one line>
PREREQUISITES: <name>@<ver> (why:<...>) risk:<one line>
SAFER ALTERNATIVES: <name>@<ver> (vs anchor:<cleaner posture>) risk:<one line>
DROPPED: <name> (<hard-gate reason>)
NEXT: chosen -> lbh-skills-qa
```

## Reference

**Skill-vetting checklist (surfacer link):** each surfaced skill must already show author, version, license, and recency; anything failing the discovery gates is dropped before display, never recommended.

**Security-review gate criteria:** "safer alternative" is defined by security posture — fewer/no elevated conditions, no unsafe primitives — not by popularity or feature count; no surfaced skill bypasses `lbh-skills-qa`.

**Versioning / rollback:** surface pinned coordinates so the user installs and can roll back the exact version suggested, keeping complement/prerequisite sets version-consistent.
