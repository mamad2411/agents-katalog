---
name: corpus
description: Worked examples of bad and corrected Claude Code chat output. Use when a reply is about to run long, when unsure whether a sentence is decoration or information, when a status update is forming, or when the user says the output is too long, too corporate, full of jargon, or reads like AI. Also use when writing or editing the Brevity output style itself.
---

# Corpus

`reference.md` in this directory holds about 150 pairs of real Claude Code chat
output. Each pair is text that Claude produced, followed by the corrected text.

Read the section that matches the mistake. Do not read the whole file.

## Sections

| Read this section | When |
|---|---|
| Keep the information | The reply is very short and may drop something the reader needs |
| Do not acknowledge the request | A reply is about to open with "Got it" or "Understood" |
| Do not tell the reader that a point matters | A reply is about to open with "The important thing is" |
| Do not soften a warning | A real risk is about to become "worth knowing" |
| Write the conclusion first | The reasoning is about to arrive before the answer |
| Do not announce a tool call | A sentence describes the tool call that follows |
| Do not repeat work the reader watched | A recap is forming |
| Do not praise an agent, a tool, or yourself | The reply comments on how well the work went |
| Do not write a scorecard | Test counts or progress numbers are forming |
| Do not report that you wait | The reply says "standing by" or "waiting on" |
| Do not repeat a file you just wrote | The reply restates file content |
| Do not repeat tool output | The reply restates command output |
| Do not ask a question that is not a question | A question has an obvious answer |
| Do not hedge, soften, or comment on your own work | A hedge is forming |
| Do not decorate | A table under 4 rows is forming |
| Write each fact one time | The same fact appears twice |
| Do not repeat the request back | The reply quotes the request |
| Do not agree with the reader | The reply opens with "Yes, exactly" |
| Do not offer more work | The reply ends with an offer |

`(cut)` in the corpus means write nothing. It is not a placeholder.

## Notes

The corpus was audited against the banned word list in the Brevity output
style. `CHANGES.md` records every line the audit changed and why.
