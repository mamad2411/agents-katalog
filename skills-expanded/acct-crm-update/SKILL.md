---
name: acct-crm-update
description: Prepares the CRM update from your call notes, with a before and after table per field, the source of each value, fields with no source left empty and a copy block or writes you approve one by one. Use for "run acct-crm-update", "CRM update", "update the CRM from my notes", "update this opportunity", "log this call in the CRM", "CRM hygiene", "fill in the CRM after my meeting", "stop typing things twice", part of the Claude for Account Executives Pack by 90n.
---

# CRM Update

## When To Use
You type the same thing twice, once in your notes and once in the CRM. Run this after your call notes are written. It answers: which fields change, to what value, and which line of the notes does each value rest on?

## When Not To Use
To write the notes themselves, run Sales Call Notes. To review every open deal and its gaps, run Pipeline Review.

## Inputs
- The call notes from the meeting.
- Your CRM's fields in their order, and the current values on the record (copy and paste, or an export).
- Your exit criteria per stage, if they are written down.
If you have none of this beyond the notes, I use the common fields (stage, amount, close date, next step, contacts) and mark the output as a first draft.

## Approach
CRM hygiene as common practice, described generically: one fact, one field, one source, and a next step that always has a date and an owner. A CRM is worth only the trust people place in its fields: an amount guessed today distorts the pipeline review and the forecast later. Salesforce in Claude (beta) asks the seller to approve each proposed change before it is written, by default (claude.com), and this skill keeps that rule for every CRM. It prevents double entry and fields filled in to look tidy.

## Workflow
1. I ask at most three questions: which fields does your CRM have and in what order, what are the current values, and which criteria move a deal from one stage to the next.
2. I read the notes line by line and tie each fact to the field it belongs in: one fact, one field. Narrative stays in the notes.
3. I fill the table: field, current value, proposed value, source line. A field with no source stays empty, above all the amount and the close date, which I never estimate.
4. Stage: I propose a change only if the notes hold the proof your exit criteria ask for. Otherwise the stage stays and I write what is missing.
5. Next step: always dated, with an owner. With no date in the notes it reads "to date" and I flag it.
6. Contacts: name, job role, role in the decision, work contact details. No note on personality or mood goes into a record that other people read.
7. I deliver a copy block in your CRM's field order. With Salesforce in Claude (beta) I propose each write and you approve it field by field; nothing is written without that.

## Output Format
```markdown
# CRM Update
[Account] · [opportunity] · from the call notes of [date]
## Before and after
| Field | Current value | Proposed value | Source (line in the notes) |
|---|---|---|---|
| Stage | [value] | [value or unchanged] | [line] |
| Amount | [value] | [empty if no source] | [line] |
| Close date | [value] | [empty if no source] | [line] |
| Next step | [value] | [who, what, date] | [line] |
| Contacts | [value] | [name, job role, role in the decision] | [line] |
## Fields left empty
- [field]: [what is missing to fill it]
## Stage check
[Exit criterion] · proof in the notes: [yes, line / no, missing: ...]
## Copy block
[Fields in your CRM's order, approved values only]
## Decision
[You] approve each field before any write, today; the stage change is your call.
```

## Done When
- Every proposed value has its source in the notes.
- The amount and the close date are never estimated.
- The next step has a date and an owner, or is flagged.
- The copy block follows your CRM's field order.

## Quality Bar
- One fact, one field: no storytelling in structured fields.
- No opinion about a person in the CRM; personal data limited to what the work needs (if in doubt, check with a qualified adviser).
- The same method works for any CRM by copy and paste.
- A stage moves on evidence, not on effort.
- No amount or date is invented: a field with no source stays empty, and you approve every write.

## Next
Run acct-meeting-recap-email (Meeting Recap Email) to confirm to the customer what was agreed.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
