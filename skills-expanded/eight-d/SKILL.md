---
name: eight-d
description: Draft an 8D problem-solving report (D0–D8) from complaint emails, test logs and meeting notes, with a source for every fact and containment kept apart from root cause.
version: 2
tools: [document_reader, explorer]
min_context: 16000
pins: local
---

# Draft an 8D report

An 8D is read by the customer who complained and by the auditor who comes after
them. Both check the same thing: that every statement can be traced to a record,
and that "what we did to stop the bleeding" was never presented as "why it bled".

## Finding the material

List **every** file under the folder you were given, recursively, with no
filter on type — do not pass a list of extensions to the explorer. Records
arrive as PDF, Word, spreadsheet, email export, plain text and Markdown, and a
filter chosen before looking is how a folder full of documents reads as empty.
Then read each file the reader can open; report the ones it cannot, by name.

Do not stop to ask whether to continue. If nothing readable is there, say
which files you found and why none could be read — that *is* the answer.

## Method

1. **Read everything first**: the complaint, the test and yield logs, the
   inspection records, the meeting notes. An 8D written in reading order
   inherits the order the files were listed in.
2. **Collect facts**, one per line, each with its source: what failed, where,
   when, how many, how it was detected. A figure from a meeting note is a
   figure someone said, and is marked as such.
3. **Fill the disciplines** from those facts only:
   - **D0** — symptom and any emergency response already taken;
   - **D1** — the team, as named in the documents;
   - **D2** — the problem description: what, where, when, how many, and what
     is *not* affected;
   - **D3** — containment: what was done to protect the customer now, with
     dates and quantities;
   - **D4** — root cause, for occurrence and for escape (why it happened, why
     it was not caught), each with the evidence that supports it;
   - **D5** — permanent corrective actions proposed, each tied to a D4 cause;
   - **D6** — implementation and verification, only where records show it;
   - **D7** — prevention: what changes in process, FMEA or control plan;
   - **D8** — closure and recognition, left for the team to complete.
4. **List the open questions**: every discipline that the documents do not
   support is left open with what would close it — a measurement, a record, a
   person to ask.

## Output

```
8D DRAFT · <complaint reference> · <date of the latest source>

D0  <line> · <source>
D1  <name, role> · <source>
D2  <line> · <source>
    NOT AFFECTED: <line> · <source>
D3  CONTAINMENT
    <action, date, quantity> · <source>
D4  ROOT CAUSE — OCCURRENCE
    <cause> · evidence: <source> · status: confirmed | suspected
    ROOT CAUSE — ESCAPE
    <cause> · evidence: <source> · status: confirmed | suspected
D5  <action> · addresses: <D4 cause>
D6  <action, verification> · <source>   (or OPEN)
D7  <change> · <source>                 (or OPEN)
D8  OPEN — for the team

OPEN QUESTIONS
  - <discipline> · <what is missing> · <what would close it>
CONFLICTS
  - <two sources that disagree, and on what>
```

## Rules

- Nothing is asserted without a source. A sentence you cannot trace to a
  document goes to OPEN QUESTIONS, not into a discipline.
- Containment is not root cause. Sorting parts, adding an inspection or
  replacing a probe card stops the symptom; it goes in D3 and never in D4.
- A root cause is "suspected" until a record shows it was verified — by
  reproduction, by measurement, or by the defect disappearing after the fix.
- Keep the documents' own wording for defect names and part numbers; do not
  translate a customer's failure description into your own diagnosis.
- This is a draft for the quality engineer who signs it. Do not assign blame to
  people, and do not commit the organisation to dates the documents do not give.
