---
name: emplaw-investigation-query
version: 1.0.0
description: Query an existing investigation record for who was interviewed, outstanding items, and timeline gaps.
author: matrixx0070
tags: [employment, investigation, query, status, hr]
capabilities: []
---

## When to use
Use this when an investigation RECORD exists and you need to read its state — surface interviews done, evidence collected, open tasks, and holes in the timeline — without changing anything. **Not for:** creating the record (use emplaw-investigation-open); appending items (emplaw-investigation-add); running the full process (emplaw-internal-investigation); drafting the formal memo (emplaw-investigation-memo); leadership roll-ups (emplaw-investigation-summary); termination decisions (emplaw-termination-review); or the shared matter folder (emplaw-matter-workspace).

## Method
1. Load the record manifest read-only; note matter id and status.
2. List interviews (who, when, representation status) and flag who is still un-interviewed. Decision point: if the respondent has not yet been interviewed, mark the record not-ready-for-findings.
3. List exhibits/evidence with custody status; flag any with broken chain.
4. Map every logged event to a date and sort chronologically.
5. Detect gaps. Decision point: if a key date in an allegation has no corroborating item, flag it as an outstanding evidence gap.
6. Compile outstanding items: pending interviews, awaited documents, unresolved custody, follow-up questions.
7. Return a read-only status snapshot; do not mutate the record.

## Example
You query matter EMP-2026-014. The snapshot shows reporter and two peers interviewed, respondent still pending, four exhibits (one with an unverified custody note), and a timeline gap: the alleged retaliation date has no document or witness support. Outstanding: interview respondent, verify EXH-002 custody, obtain the deployment log for the gap date.

## Pitfalls
- **Reading as complete.** Absence of an entry is not proof of absence — flag gaps, don't assume clearance.
- **Mutating on query.** This step is read-only; corrections go through emplaw-investigation-add.
- **Ignoring representation flags.** An interview taken without honored Weingarten rights may not stand — surface it.
- **Timeline by memory.** Sort logged dates; do not reconstruct the sequence from recall.

## Output format
```
INVESTIGATION RECORD — QUERY (read-only)
Matter id / Status:
Interviews done: <name — date — rep status>
Not yet interviewed:
Evidence: <id — item — custody ok?>
Timeline (sorted):
Gaps / unsupported dates:
Outstanding items:
Ready for findings? (respondent interviewed, gaps closed):
```

## Reference
General reference, not tailored legal advice. A defensible investigation is thorough: the respondent is interviewed and each allegation has an evidentiary basis before findings. Findings apply the preponderance-of-evidence standard, so gaps in corroboration matter. EEOC credibility factors (plausibility, demeanor, motive, corroboration, past record) depend on complete interviews. Weingarten rights: verify representation was honored where requested. Anti-retaliation monitoring stays open until closure. Attorney-escalation gate: if a query reveals a broken chain of custody, a denied representation request, or a legal-exposure gap, involve counsel before acting to preserve privilege — not legal advice.
