---
name: canvas-editing
description: Change the claims of a Lean Canvas on the hub as a member asks, by the rev protocol of the plugin canvas (base_rev, 409, undo by command) and its rules of status and evidence.
---

# Editing a canvas by the rev protocol

Every change of a claim is a rev. The hub takes a change only from the rev it was read at, so two people never
overwrite each other without seeing it.

## A change

1. Read the canvas, or the claim, with `canvas__read`. Note each claim's code and rev: `CL-3 [assumption, medium,
   rev 4]`.
2. Call `canvas__edit` once with every change of the member's request:
   - a change of a claim: `claim` (CL-3), `base_rev` (4), and only the fields that change;
   - a new claim: `cell`, `text`, and a `test_card`, without `claim`, `base_rev` or `status`;
   - `reason`: what the member asked, in their words.
3. The edit is all or nothing. When one claim changed since you read it, the hub refuses the whole edit, writes
   nothing, and lists the claim with the rev it is at, who changed it and what differs.
   - The new text does not touch what the member asked: make the change again on the new rev.
   - It does: show the member both and ask which to keep. Do not choose for them.
4. Tell the member what was written: each claim's code and its new rev. Say that they can ask you to undo it.

## Fields

| Field | Values |
|---|---|
| `text` | at most 2,000 characters, one claim each |
| `status` | assumption, testing, invalidated, retired; testing needs a test card with a hypothesis, a test and a deadline |
| `confidence` | low, medium, high |
| `cell`, `position` | where it sits; position 0 is first in its cell |
| `test_card` | the whole card; null takes it away |
| `archived` | true archives the claim, false brings it back |

## Undo

- "Undo", "take that back": `canvas__undo` without claims. The hub takes back every claim the member's last command
  changed, back to the rev before it; a claim the command made is archived. Saying undo again takes back the command
  before.
- "Undo CL-3": `canvas__undo` with `claims` [{"claim": "CL-3", "rev": <its current rev>}].
- When a claim changed after the command, the undo is refused with what changed: tell the member.

## Status and evidence

- validated is never yours to set, nor to undo back to. A writer validates a claim when it has real evidence that
  supports it: not synthetic, not a document or a simulation, not withdrawn, added by a person or confirmed by a
  writer.
- invalidated and retired need nothing; they are cheap and can be undone.
- Evidence is not part of a rev: adding some does not change the claim's rev.
