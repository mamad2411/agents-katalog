---
name: emplaw-investigation-add
version: 1.0.0
description: Add a new piece of evidence, interview, or note to an existing open investigation record while preserving chain of custody.
author: matrixx0070
tags: [employment, investigation, evidence, chain-of-custody, hr]
capabilities: []
---

## When to use
Use this when an investigation RECORD already exists and you need to append one item — an interview summary, an exhibit, or an analyst note — and update the manifest without disturbing prior entries. **Not for:** creating the record (use emplaw-investigation-open); running the full process in one pass (emplaw-internal-investigation); reading the record back (emplaw-investigation-query); drafting the memo (emplaw-investigation-memo); leadership roll-ups (emplaw-investigation-summary); termination decisions (emplaw-termination-review); or the shared matter folder (emplaw-matter-workspace).

## Method
1. Load the record manifest and confirm status=OPEN. Decision point: if status is CLOSED, do not append — reopen via counsel first.
2. Classify the item: interview, document/exhibit, physical/digital evidence, or note.
3. Assign the next sequential exhibit/interview id.
4. For evidence, record chain of custody: source, who collected, when, how stored, hash/copy method. Decision point: if the item is a personal device or medical/health data, involve counsel on privacy/consent before ingesting.
5. For interviews, capture date, participants, representation status, and a factual (not conclusory) summary. Decision point: if a union employee requested representation and it was denied, stop and cure the Weingarten issue.
6. Cross-reference the item to the allegation(s) it bears on.
7. Append to the manifest with an immutable timestamp; never overwrite prior entries.

## Example
Mid-investigation you receive screenshots of the manager's messages. You confirm the record is OPEN, log EXH-004, record that the reporter exported them from her phone on 2026-07-09, note the SHA-256 of the file, store the original read-only, and link it to Allegation 1. You then add interview INT-003 with a peer, noting no representation was requested.

## Pitfalls
- **Editing prior entries.** Chain of custody dies the moment an exhibit is overwritten — append only.
- **Conclusory interview notes.** Record what the witness said, not your judgment of it; credibility belongs in the memo.
- **Untracked custody.** "Someone gave me a USB" is not custody; log source, collector, time, and storage.
- **Ingesting private data blindly.** Personal devices or health records can trigger privacy law — gate through counsel.

## Output format
```
INVESTIGATION RECORD — ADD ITEM
Matter id: (status must be OPEN)
Item type: interview | exhibit | evidence | note
Item id: (next sequential)
Date / Added by:
Source & chain of custody:
Storage / hash:
Summary (factual):
Representation status (if interview):
Linked allegation(s):
Timestamp (immutable):
```

## Reference
General reference, not tailored legal advice. Chain of custody: document who had the item, when, and how it was stored, unbroken from collection to record. Interview notes should be factual and contemporaneous; reserve credibility analysis for the memo. Weingarten rights: honor a union employee's request for representation in investigatory interviews. Privacy: personal devices, medical, and biometric data may be protected — obtain consent or counsel guidance. Preservation and anti-retaliation obligations remain live while the record is open. Attorney-escalation gate: involve counsel to preserve privilege before ingesting private-device or health data, or before reopening a closed record — not legal advice.
