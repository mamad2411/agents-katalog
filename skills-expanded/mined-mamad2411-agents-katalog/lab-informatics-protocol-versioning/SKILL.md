---
name: lab-informatics-protocol-versioning
description: "Controlled protocol documents, change logs, and effective-date discipline for reproducibility and audits."
---
# Version protocols like software

> Controlled protocol documents, change logs, and effective-date discipline for reproducibility and audits.

**Track:** 🧬 Biotech & Pharma · **Domain:** Lab Informatics · **Level:** foundation · **~25 min**

**Who this is for:** Bioinformaticians, Lab Scientists, Regulatory Affairs, Genetic Engineers, Clinical Data Managers

## When to Use This Skill

Controlled protocol documents, change logs, and effective-date discipline for reproducibility and audits.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Store protocols in controlled repo with semver-style versions
2. Change log entry per revision: what changed, why, approved by
3. Effective dates govern which version applies to which experiment dates
4. Link executed runs to exact protocol version used
5. Retire superseded versions visibly, never silently edit history
6. Review critical protocols annually or upon equipment change

## Common Pitfalls

- Protocol PDFs floating in email attachments
- Edits without version bumps breaking audit trails

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill lab-informatics-protocol-versioning
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill lab-informatics-protocol-versioning -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills