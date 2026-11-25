---
name: rollstack-burst-reports
description: Make one version of a Rollstack report per client, region, team or other value with a burst, set who each version is emailed to, then run or send them all, with the Rollstack MCP tools getReportParameters, createBurst, addBurstVariants, updateBurstVariantRecipients, startBurstRun and sendBurstVariantEmails. Use when the user wants the same report for every customer, region or team, or asks about a burst. For a single report, use rollstack-refresh-and-schedule or rollstack-send-report-email instead.
license: MIT
---

# Rollstack bursts

A burst makes one copy of a template report per value, such as one QBR per customer or one business review per region. Each copy, a variant, reads its own data, has its own recipients and runs on its own. Set up the connection first with the `rollstack-getting-started` skill.

## 1. Find or start the burst

- **An existing burst**: find it with `listBursts` (filter by `name`). `listReports` leaves out the reports of a burst.
- **A new burst of a Rollstack report** (type `SlideDeck`): call `getReportParameters` on the report. Its variants differ by the parameters marked `burstable` there. If none fits, create one with `createReportParameter`, linked to the dashboard filters and datasheet columns `getReportParameters` lists, after checking them with the user. Then call `createBurst` with the report as `templateReportId` and the parameters as `parameterIds`.
- **A new burst of an older report**, such as a Google Slides or PowerPoint file: find its syncs with `listReportSyncs` and their filters with `listReportSyncFilters`, then call `createBurst` with them in `filters`.

The report becomes the burst's template.

## 2. Add the variants

Call `addBurstVariants` with one entry per value the user names, such as each region or customer: `parameters` for a Rollstack report's burst, `filters` for an older report's. At most 500 per call. Each variant is copied from the template, then runs once to fetch its data, so the call answers a `batchId` at once: follow it with `getBurstVariantBatch` until it ends. A value the burst can't take adds nothing: tell the user which one.

Check the result with `listBurstVariants`.

## 3. Set each variant's recipients

`updateBurstVariantRecipients` replaces each variant's `to`, `cc` and `bcc`, and sends nothing. Show the user the recipients of every variant before you set them. How the variants' emails are sent, such as the sender, is set for all of them with `updateBurstVariantEmailSettings`.

## 4. Run and send

- `startBurstRun` refreshes every variant, or the `variantIds` passed. On an older report's burst, each variant whose email `trigger` is `all` is then emailed: tell the user who would get an email before you start it, and Rollstack asks them to confirm the run. Follow it with `getBurstRun` until nothing is running.
- `sendBurstVariantEmails` sends each variant's own email now, to its own recipients. List the recipients, get the user's go, then call it: Rollstack asks them to confirm it too. Only the burst's owner and admins may.
- To send one email that holds several variants, such as every region to one manager, use the burst's email configurations: `listBurstEmailConfigs`, `createBurstEmailConfig`, a test with `sendBurstEmailConfigTest`, then `sendBurstEmailConfig` once the user confirms.

## Removing

`removeBurstVariants` deletes the reports of the variants passed, and `deleteBurst` deletes every report in the burst, the template report included. Neither can be undone: confirm with the user exactly what goes, and Rollstack asks them to confirm again.
