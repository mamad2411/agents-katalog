---
name: meeting-notes-actions
description: Turn rough meeting or client-call notes into decisions, an action table with owner, due and status, open questions, risks and a follow-up email. Use when the user asks for MoM, minutes, meeting summary, action items, or a follow-up mail after a call.
---

# Meeting Notes to Actions

## Inputs
- Rough notes, typed live (half-sentences, shorthand, Hinglish)
- Transcript or chat export with speaker names
- Several people's notes of the same meeting (merge them)
- Optional: previous MoM (to carry over open actions)

## Defaults (state them in the output if used)
| Setting | Default | Options |
|---|---|---|
| Audience of email | Attendees, incl. client | Internal only · Client · Mixed |
| Meeting date | Date in notes, else "TBD" | Never assume today |
| Due date format | As written ("Fri", "EOW") + ISO date only if meeting date is known | |
| Email length | ≤ 150 words + action table | |

Ask **one** question only if it is unclear whether the email goes to a client (it changes what may be shown). Otherwise assume Mixed and hide internal-only remarks.

## Steps
1. Read all notes once; list attendees and map initials/nicknames to names (`references/extraction-rules.md`).
2. Normalise shorthand and Hinglish into plain English; keep the original meaning, never add intent.
3. Classify every line: **Decision · Action · Open question · Risk · Info · Noise**.
4. For each action capture owner, due, status, IDs (AWB, ULD, flight, ticket) exactly as written. Missing owner or due: "TBD".
5. Merge duplicates across sources; flag conflicts (different owner or date) under Needs input.
6. If a previous MoM is given, carry over its open actions with status Open / Done / Slipped.
7. Fill `templates/mom-template.md` (the example there shows the level of detail).
8. Draft the follow-up email from the same data: thanks, decisions, actions, next meeting.
9. Run the self-check and fix before returning.

## Format
Use `templates/mom-template.md`: header, Decisions, Action items table, Open questions, Risks, Follow-up email. Status values and icons are defined in `references/extraction-rules.md`.

## Rules
- **Branding only on request:** use plain, neutral formatting by default. Apply a company or brand design skill (colours, fonts, logo, templates) only when the user names that skill or brand in the request; never pick one automatically.
- Never invent owners, dates, decisions or numbers. Use "TBD" and list under Needs input.
- Keep IDs, names, flight numbers and figures exactly as given.
- A decision is only a decision if the notes show agreement ("agreed", "final", "go ahead", "done hai"). Otherwise it is an open question.
- One action per row; start with a verb ("Share", "Confirm", "Fix").
- "We" / "team" as owner is not an owner: write "TBD (team)".
- Relative dates ("kal", "next week") stay as written unless the meeting date is known; then add the ISO date in brackets.
- Client-facing email: no internal blame, no internal-only remarks, no internal tool names.
- Empty section: write "None". Never delete a section.

## Self-check
- [ ] Every non-noise line appears as decision, action, question, risk or info
- [ ] Every action has owner, due and status (TBD allowed, blank not allowed)
- [ ] No invented owners, dates or decisions
- [ ] IDs and numbers match the notes character for character
- [ ] Conflicts flagged, not silently resolved
- [ ] Email matches the MoM (same actions, owners, dates)
- [ ] Email ≤ 150 words plus the action table

## Output
Return the MoM, then the follow-up email draft, then an **"Assumptions & Needs input"** block (defaults used, TBDs, conflicts, unclear shorthand) outside both.

Benchmark after edits with `evals/test-cases.md`.
