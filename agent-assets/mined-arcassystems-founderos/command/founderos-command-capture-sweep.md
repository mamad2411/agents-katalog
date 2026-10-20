---
description: Notice what was recorded and propose where it goes. Say "sweep my meetings", "anything new to capture", or run /founder-os:capture-sweep. Sorts each item (client conversation, training media, internal, personal) and proposes queue items plus provisional-fact rows. Propose only - it never files a record or does the capture.
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write"]
---

# Founder OS capture sweep

Run the capture-sweep skill at `skills/capture-sweep/SKILL.md` end to end.

## Procedure

1. Read `skills/capture-sweep/SKILL.md`.
2. Preflight the recorder bound in `stack.json`. If one is named but unreachable, say so in one line, note it in `system/quarantine.md`, and stop. If none is bound, sweep `capture/inbox/` and say plainly that no recorder is connected.
3. Read the marker at `brain/.capture-sweep.json`. Missing means first run.
4. Sort every item into exactly one of the four types and print the decision per item.
5. Show the proposed queue items and ledger rows, then run them on one go.
6. Write the marker and close with the honest counts, including what was skipped.

## Rules

- Propose only. Never edit a person's record, never run the capture, never route a transcript.
- Personal items are skipped and counted, never filed.
- An unconfirmed name goes to `python scripts/unconfirmed_facts.py add`, never into an item as a fact.
- No personal data and no amounts in any item.
- No em dashes or en dashes. No banned words.
