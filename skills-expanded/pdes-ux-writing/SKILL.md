---
name: pdes-ux-writing
description: Write every string for one flow in a single copy deck, with labels, buttons, helper text, errors that say what happened and what to do next, empty states, length limits, a glossary check and the approvals still needed. Use for "run pdes-ux-writing", "UX writing", "write the microcopy", "copy deck for this flow", "fix my error messages", "replace the lorem ipsum", "better button labels", "empty state copy", part of the Claude for Product Designers Pack by 90n.
---

# UX Writing Copy Deck

## When To Use
The screens are done and the copy is still "Lorem ipsum", "Oops, something went wrong" and "Submit". Nobody owns the words, so they will be written by whoever builds the screen, at the moment they build it. This skill answers one question: what does every string in this flow say, and who still has to approve it?

## When Not To Use
Not for deciding which states a screen has. If you are unsure whether an empty or offline state exists at all, run UI States and Edge Cases, then come back for the words. Not for marketing pages or long help articles, where a content designer's brief is the better start.

## Inputs
- The flow, as screens, a frame list or a user flow table
- Voice rules and the product glossary, or the product context file that holds them
- The errors that can happen, with their real causes from engineering if you have them
- Character limits per element, the languages you ship in, and who approves copy
If you have none of this, I start from a description of the screens and mark the output as a first draft with limits and approvers left as placeholders.

## Approach
Errors follow two public sources. Nielsen Norman Group's error message guidelines (2023) ask for a message shown near its cause, in plain words, specific about what went wrong, with a constructive next step and the user's input kept. The GOV.UK Design System guidance on error messages adds three tests: clear and concise, consistent wherever the message appears, and specific. The judgement is knowing what copy cannot do. If a flow causes the same error for most people, a kinder sentence hides a design problem, and I will say so instead of polishing it.

## Workflow
1. I ask up to three questions: which flow and which screens, the character limits and languages, and who approves copy.
2. I build the deck with one row per string: id, screen, element type, the copy, the limit you set, the longest realistic version, approval and status.
3. Buttons and labels. A button names its action ("Send invite"), never "Submit" or "OK". Labels match the glossary word for word.
4. Errors, by the two sources. Each one says what happened and how to fix it. An empty field gets an instruction ("Enter your first name"); a wrong entry gets a description ("Name must be 35 characters or less"). The same message appears beside the field and in any summary. No error blames the user.
5. Empty states say what goes here and how to start. Confirmations say what just happened and what follows, in the past tense.
6. Glossary check: each product term used one way across the deck, and every synonym flagged for you to settle.
7. Longest-version pass and approvals. I write the longest realistic version of each string, flag the rows that break the limit, and mark each row for the content owner, legal or none.

## Output Format
```markdown
# UX Writing Copy Deck
Flow: [flow] · Voice rules from: [source] · Languages: [list] · Content owner: [role]
## Strings
| Id | Screen | Element type | Copy | Limit | Longest realistic version | Approval needed | Status |
|---|---|---|---|---|---|---|---|
| [S01] | [screen] | [label, button, helper, empty state, confirmation] | [copy] | [limit] | [longest version] | [content owner, legal, none] | [draft] |
## Errors
| Id | Screen | Cause | Message | Next step offered | Shown where | Input kept |
|---|---|---|---|---|---|---|
| [E01] | [screen] | [real cause, or cause not confirmed] | [message] | [action] | [beside field, summary] | [yes, no] |
## Glossary check
- [Term] · Used as: [meaning] · Also found: [synonym, string ids] · Settle as: [your call]
## Over the limit
- [String id] · [in which language, by how much] · [shorter option]
## Decision
[The content owner] approves or returns the deck by [date]. [Legal] reviews the rows marked for legal by [date]. Until then every row stays at status "draft".
```

## Done When
- Every string in the flow has a row, including helper text and confirmations
- Every error names what happened and offers a next step
- No button reads "Submit", "OK" or "Click here"
- Every row has a limit, a longest realistic version and an approval mark, or a placeholder for each

## Quality Bar
- Plain words a user would say. Internal names, error codes and system terms stay out of the message.
- An error whose real cause is unknown reads "cause not confirmed" and goes to engineering as a question. I do not guess at what failed.
- The longest-version column is a prompt to check with a translator, not a measurement.
- Voice rules bend for errors and for anything about money, data or deletion: clarity first. Strings that make a legal promise: check with a qualified adviser.
- Nobody has read these strings in a session yet. The words that carry the task belong in your next round of testing with real users.
- Copy is a draft until the content owner approves it; legal wording is flagged for a qualified adviser, never written as final.

## Next
Run pdes-ui-states-and-edge-cases (UI States and Edge Cases) to check every state the copy assumed.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
