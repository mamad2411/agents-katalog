---
name: rollstack-slides
description: Write the slides of a Rollstack slide deck yourself, as HTML, check each one with the Rollstack MCP tool renderReportSlides and save them with saveReportSlides. Use when the user wants to shape the slides with you, or gives you material Rollstack can't read, such as files or notes in this chat. If the user hasn't said whether Rollstack's slides agent or you should build the slides, ask them first, in the words the Rollstack MCP server's instructions give. To have Rollstack's slides agent build a whole deck in one call on the company template, use rollstack-build-deck instead.
license: MIT
---

# Rollstack slides

Rollstack's MCP server hands out the guide to writing slides, fitted to the report you work on, so the guide always matches the tools. This skill only tells you where to start.

1. Find the report with `listReports`, or create it with `createReport`. It must be a slide deck (type `SlideDeck`). Before creating one, list the templates with `listTemplates` and pass one as `templateId`: when the organization has company templates, ask the user which one to use, even when there is only one; otherwise Rollstack's own.
2. Call `getReportDesign` for the report, without `layoutIds`. Its answer holds the guide: read it and follow it.
3. In short: you write each slide as one `<section>` of HTML, check it with `renderReportSlides` until it has no issues, and save it with `saveReportSlides`.
4. When the slides need the user's data, a CSV or an Excel workbook, call `getReportDataGuide` once before you add it: it covers sending the file, picking a range, checking figures and reshaping data.
