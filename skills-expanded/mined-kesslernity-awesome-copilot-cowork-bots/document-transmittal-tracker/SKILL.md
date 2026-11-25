---
name: document-transmittal-tracker
description: Tracks documents issued to clients, contractors and authorities: what was sent, to whom, on what date, what response was due and what is now overdue for return. Use when the user asks what has been transmitted, what is outstanding for comment or approval, to build a transmittal register, or which documents are overdue for return.
---

# Document Transmittal Tracker

Answers "what did we send, and who still owes us a response", from the mail itself.

## Inputs
- **Email** for transmittal messages and their responses
- **Enterprise Search** for the transmittal register, if one exists as a file
- `references/config.md` for document-number patterns, response windows and the party list

## Procedure
1. **Find transmittals** by the document-number pattern in config, plus the usual vocabulary:
   "for approval", "for comment", "for construction", "IFC", "IFR", "transmittal".
2. **One row per document revision**, not per message. Revision B of a drawing is a different row
   from revision A, and conflating them hides the resubmission.
3. **Extract**: document number, revision, title, party, date issued, purpose, response due by
   the config window, response received, and the source link.
4. **Determine status**: `Awaiting response`, `Responded`, `Overdue`, `Superseded by later
   revision`. Superseded is not overdue and must not be chased.
5. **Age** overdue items from the due date, not the issue date.
6. **Write** the register and list overdue items first.

## Output
| Doc no | Rev | Title | Party | Issued | Purpose | Due | Status | Age | Source |

Then: overdue by party, items due in the next week, and revisions that superseded an open item.

## Definition of done
Every transmittal has a status, superseded revisions are excluded from overdue, and overdue items
lead the output.

**Nothing overdue is the goal, not a failure of the skill.** Say it in one line.

## When there is no data
- No transmittals matching the pattern: say which pattern you used, since the pattern is the most
  common cause of an empty result.
- A response that does not state which revision it answers: mark the status ambiguous and link
  both candidate rows rather than picking one.
- Register file exists but disagrees with the mail: show both and say they disagree. The register
  is the record; the mail is the evidence.

## Boundaries
- **Never issue, reissue or transmit a document.**
- **Never chase a party directly.** Drafts go to the user.
- Never mark anything as approved. Approval is a recorded act in the project's own system.
- 🔴 Never treat a transmittal as a safety or regulatory clearance. This tracks correspondence,
  not permits, sign-offs or certifications.

## Self-check
- Is every row a document revision rather than a message?
- Are superseded revisions kept out of the overdue list?
- Did I state the document-number pattern I searched for?
