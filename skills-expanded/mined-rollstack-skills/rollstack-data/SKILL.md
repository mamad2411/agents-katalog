---
name: rollstack-data
description: Bring a CSV or Excel file into a Rollstack report and shape its data for charts, with the Rollstack MCP tools createDatasetUpload, getDataset, addReportDatasheets, queryReportData and previewReportDatasheetChanges. Use when the user gives you a spreadsheet or file to build Rollstack slides from, or asks for a chart, total or breakdown the report's data does not have yet.
license: MIT
---

# Rollstack data

Rollstack's MCP server hands out the guide to getting data in and shaping it, so the guide always matches the tools. This skill only tells you where to start.

1. Call `getReportDataGuide` once, before anything else. Read it and follow it.
2. In short: send the file with `createDatasetUpload` when you have a shell, read a workbook's sheets with `getDataset` and add the range that starts at its header row, then add the file to the report with `addReportDatasheets` and use the datasheet ids it answers.
3. Check every figure you will claim with `queryReportData`, and shape data a chart needs with `previewReportDatasheetChanges` until it answers `valid: true`. Save it with `saveReportDatasheetChanges` before you save the slides that show it.
4. To write the slides themselves, follow the `rollstack-slides` skill. To have Rollstack's slides agent build them, pass the datasheet ids to `sendReportMessage` as the `rollstack-build-deck` skill says.
