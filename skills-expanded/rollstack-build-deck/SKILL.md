---
name: rollstack-build-deck
description: Build or change a slide deck in Rollstack from company data, such as a BI dashboard, a spreadsheet or a CSV, with Rollstack's slides agent, then review and export it. Use when the user asks for a deck, QBR, business review, board pack or slides from their data in Rollstack.
license: MIT
---

# Build a deck with Rollstack

Rollstack's slides agent builds and edits decks the way its chat does in the app. You send it a message, follow its replies, and check the slides it changed. Set up the connection first with the `rollstack-getting-started` skill.

## 1. Pick or create the report

- **An existing deck**: find it with `listReports` (filter by `name`). Its `type` must be `SlideDeck`.
- **A new deck**: call `createReport` with a `name`, and a `folderId` from `listFolders` if the user wants it in a folder. To start from the company's design, pass `templateDeckId`, the id of a deck that has it. The new report gets that deck's theme and layouts, but none of its slides.

## 2. Add the data

The agent builds slides from datasheets on the report. Add the sources it needs:

- **A BI dashboard** (Tableau, Power BI, Looker, Metabase, Sigma, Omni, Lightdash): search with `searchDashboards` using the name the user gives, confirm the right one with the user, optionally check its tabs with `getDashboard`, then add it with `addReportDatasheets`.
- **A Google Sheets or Excel file** the user has added in Rollstack: find it with `searchSpreadsheets`, then add a range with `addReportDatasheets`.
- **A CSV**: upload it with `createDataset` (a header row, at most 10 MB), then add it with `addReportDatasheets`. For a large file, the REST endpoint is better than writing the CSV into a tool call.

`addReportDatasheets` answers the new datasheets' ids, in the order you sent the sources.

## 3. Message the slides agent

Call `sendReportMessage` with:

- `content`: the brief, as the user would write it in the chat. For example: "Build a Q3 business review: revenue by region, top accounts, churn. One chart per slide."
- `datasheetIds`: the datasheets from step 2.

It answers a `messageId` and a `chatId` right away. On a deck with no slides yet, the agent takes the message as a request to build it.

## 4. Follow the reply

Call `getReportMessage` with the `messageId`. It waits up to 30 seconds (`waitSeconds`), so call it again while the `status` is `queued` or `running`. Then act on each reply:

- **A `clarification` reply** asks questions. Ask the user, then send their picks as `answers` in a new `sendReportMessage` with the same `chatId`.
- **A proposal reply** (`settings_proposal` or `email_send_proposal`) changes nothing yet. Show the user exactly what it would change, then call `approveReportMessageProposal` or `rejectReportMessageProposal` as they decide. Never approve on your own.
- **Other replies** describe what the agent did, and list the slides it changed in `changedSlideIds`.

## 5. Check the slides

- `showReport` with the reply's `changedSlideIds` shows the user the deck in a viewer, opened on the first changed slide, with every changed slide marked. Clients that can't show the viewer, such as most coding agents, only get the slides' ids and titles back: use `getReportSlideImages` there.
- `getReportSlideImages` with the reply's `changedSlideIds` renders them as images, at most 10 per call. Look for text that overflows, overlapping shapes and charts too small to read.
- `getReportContent` with the same ids returns the titles, text and every chart's and table's values. Use it to check the numbers.

To fix something, send another message with the same `chatId`, and pass `slideIds` for the slides it's about.

## 6. Share or export

- `exportReport` with `format` set to `pdf` or `pptx` answers a download link that works for 15 minutes. In a PowerPoint export, charts are images.
- `shareReport` gives other members access, and `getReport` answers `appUrl`, the link that opens the deck in Rollstack.

## Limits

- 6 messages to the slides agent a minute per user.
- 10 exports and slide-image calls a minute per user.
- Past a limit, calls answer 429: wait the seconds in `Retry-After`.
