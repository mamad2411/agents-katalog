---
name: regl-matter-workspace
version: 1.0.0
description: Set up and maintain a single regulatory-matter workspace that keeps rules, diffs, comments, deadlines, and decisions organized and audit-ready.
author: matrixx0070
tags: [regulatory, legal, matter-management, organization, audit-trail, workspace]
capabilities: []
---

## When to use

Use this to create the home for a regulatory matter and keep it coherent as work accumulates — the place where the feed hits, diffs, comment drafts, deadlines, and decision records all live in one traceable structure. Reach for it at the start of a matter and whenever the workspace needs re-organizing.

**Not for:** the analytical work itself (regl-policy-diff, regl-gap-surfacer), drafting comments or policy (regl-comments, regl-policy-redraft), or the weekly rollup (regl-gaps). Privilege and legal-hold decisions about what the workspace contains are attorney calls — flag them, don't decide them.

## Method

1. Define the matter scope in one line: the regulation(s), jurisdiction, business line, and the question the matter exists to answer. Everything filed must serve that scope.
2. Establish a consistent structure: source rules, analysis (diffs/gaps), comment drafts, deadlines, decision log, and correspondence. Key everything to docket/RIN so cross-references hold.
3. Maintain a decision log: each material choice with date, rationale, and who decided. This is the audit spine.
4. Track deadlines centrally so regl-gaps and regl-comments read from one clock, not scattered notes.
5. **Decision point:** mark any document that is or may be privileged, or subject to legal hold, and route the privilege determination to an attorney — do not label or waive privilege yourself.
6. Keep provenance: for every source rule, store the official citation and retrieval date so later readers can verify.
7. Prune duplicates and dead references periodically so the workspace stays trustworthy.

## Example

> Matter: "US consumer-lending — CFPB retention rule." Scope: does RIN 3170-AB00 change our retention obligations? Structure created: /sources (rule + prior version), /analysis (diff v1), /comments (draft), /deadlines (comment close 08-29, effective 2027-01-01), /decisions (log). Decision logged: "File comment on §4 — GC approved 08-20." One doc flagged possibly-privileged → attorney to confirm before sharing with vendor.

## Pitfalls

- No single scope line, so unrelated material accretes and the matter loses focus.
- Deadlines living in scattered notes instead of one tracked place.
- No decision log — six months later no one can reconstruct why a choice was made.
- Self-labeling privilege or waiving it, instead of leaving that determination to counsel.

## Output format

```
MATTER WORKSPACE — <matter name>
Scope: <rule/jurisdiction/business line — the question>
Key: docket/RIN <id>
Structure:
  sources/     <rule versions + citations + retrieval dates>
  analysis/    <diffs, gap findings>
  comments/    <drafts + submission IDs>
  deadlines/   <comment close, effective, internal>
  decisions/   <log: date | decision | rationale | who>
Privilege / legal-hold flags: <docs → attorney review>
```

## Reference

**Rulemaking lifecycle:** organize sources so the matter shows the full arc — prior rule, ANPRM/NPRM, comments filed, final rule, effective date — which is exactly the trail an examiner or auditor reconstructs.

**Comment-period mechanics:** the deadlines section must carry comment-close dates (~30–60 day windows) alongside effective dates so nothing time-boxed slips; regl-comments and regl-gaps read from this single clock.

**Policy-diff method:** the analysis folder holds obligation-level diffs keyed to the same docket/RIN, so every conclusion traces back to a stored source. Attorney-escalation gate: privilege, legal-hold, and disclosure decisions about workspace contents are legal determinations for counsel, not the operator.
