---
name: rollstack-check-figures
description: Check that the numbers and claims on a Rollstack slide deck match its data, with the Rollstack MCP tools getReportContent, listReportDatasheets and queryReportData, and report what is wrong. Use when the user asks you to check, verify, audit or proofread the numbers of a deck before it goes out.
license: MIT
---

# Rollstack check figures

This is a read: change nothing unless the user asks you to fix what you find.

1. Find the report with `listReports`. It must be a slide deck (type `SlideDeck`).
2. Read every slide's text, charts and tables with `getReportContent`, and look at the slides with `getReportSlideImages`.
3. List its datasheets with `listReportDatasheets`. Skip the entries with a `copyOf`: they repeat another datasheet's data. A datasheet never read (`lastReadAt` is `null`), or read longer ago than the user expects, is a finding on its own.
4. Call `getReportDataGuide` once and read "Checking figures": how to name a datasheet's table and write the SQL.
5. For each figure and claim on a slide, such as a total, a change, a share or "the largest region", work it out with `queryReportData` from the datasheet it comes from. Queries run one at a time: send each once the last has answered, and check a slide's figures from one datasheet in one query. Never compute it by hand from the rows a query answered.
6. Report each slide that is wrong: what it says, what the data says, and the query you checked it with. Say too which figures were typed in rather than tied to a datasheet, since those do not update when the data does: in a slide's draft from `getReportSlideHtml`, a tied one sits in an element with a `data-datasheet-id`.

To fix what you found, follow the `rollstack-edit-deck` skill.
