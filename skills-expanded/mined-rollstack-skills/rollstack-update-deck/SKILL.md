---
name: rollstack-update-deck
description: Refresh a Rollstack slide deck with new data, such as this month's numbers or a newer version of a file, and fix the slides the new data made wrong yourself, with the Rollstack MCP tools replaceDataset, startReportRun, getReportSlideImages and saveReportSlides. Use when the user gives you a newer file for a deck, or wants you to roll a deck forward and fix its slides. If the user hasn't said whether Rollstack or you should fix the slides, ask them first, in the words the Rollstack MCP server's instructions give. To refresh a deck from its sources and let Rollstack repair its slides, or to schedule its updates, use rollstack-refresh-and-schedule instead.
license: MIT
---

# Rollstack update deck

Rollstack's MCP server hands out the guide to updating a deck, so the guide always matches the tools. This skill only tells you where to start.

1. Find the report with `listReports`. It must be a slide deck (type `SlideDeck`): for another type, `startReportRun` refreshes its syncs and there are no slides to fix.
2. Call `getReportDesign` for the report, without `layoutIds`, and follow "Updating a deck after its data changed" in its guide.
3. In short: when the user gives you a newer file, find the uploaded file each datasheet reads by its `datasetId` in `listReportDatasheets`, and replace it in the same columns. With a shell, send the new file, a CSV or a workbook, with `createDatasetUpload` and that `datasetId`; without one, write a CSV into `replaceDataset`. Only the user who uploaded a file may replace it. Data read from a dashboard or a spreadsheet needs no replacing: the run reads it again.
4. Run the report with `startReportRun` and `repairSlides: false`, wait for it with `getReportRun`, then look at every slide with `getReportSlideImages`.
5. Fix only what no longer fits or no longer reads true, such as a title whose claim the new numbers contradict. Check each figure you rewrite with `queryReportData`.
6. Tell the user which slides you changed, and show them with `showReport`.
