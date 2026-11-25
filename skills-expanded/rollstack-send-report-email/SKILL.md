---
name: rollstack-send-report-email
description: Set who a Rollstack report is emailed to, check the email with a test send, and send it to its recipients only after the user confirms them. Use when the user wants to email a deck or report from Rollstack, change its recipients, sender or attachment, or have its scheduled updates email it.
license: MIT
---

# Send a Rollstack report by email safely

An email goes to real people and can't be unsent. Show the user who gets it before anything is sent, and send a test first. Set up the connection with the `rollstack-getting-started` skill.

Only `SlideDeck` reports have email settings here. Check the report's `type` with `getReport` first.

## 1. Read the current setup

Call `getReportEmailConfig`. A 404 means the email isn't set up yet. Otherwise it answers:

- `to`, `cc`, `bcc` and `replyTo`: who gets it and where replies go.
- `smtpServerId`: the sender. `null` sends it from Rollstack's own address.
- `sharingFormat`: `pdf` or `ppt` sends the slides as a file, and `cloudLink` sends a link to the copy exported to Google Drive or OneDrive.
- `trigger`: which runs email it on their own (see step 5).

## 2. Change the recipients or how it's sent

`updateReportEmailConfig` **replaces** the whole setup. A field you leave out goes back to its default, so:

1. Start from what `getReportEmailConfig` answered.
2. Change only what the user asked for.
3. Show the user the recipients you're about to set, then send every field.

Each field:

- `to` is required. `to`, `cc` and `bcc` hold at most 100 addresses together.
- `groupRecipients: false` sends each address in `to` its own email.
- `smtpServerId` comes from `listSmtpConnections`: the user's own SMTP connections and those shared with the organization.
- `sendAttachmentAsLink` (`true` by default) puts the PDF or PowerPoint file behind a download button instead of attaching it.
- `cloudLink` needs the report's export set up in the app first. Until then, its emails fail to send.

## 3. Send a test

Call `sendReportTestEmail`. It sends the email to the user only, and waits until it's sent. Ask them to check it: the subject, the body and the attached slides.

## 4. Send it

1. List the recipients, `to`, `cc` and `bcc`, and get the user's go for this exact list.
2. Call `sendReportEmail`. It sends the report as it is now, so refresh it first with the `rollstack-refresh-and-schedule` skill if the user wants fresh numbers.

It answers 400 when the report has no recipients. The send runs in the background: while one is going, another call starts nothing.

## 5. Email it on every scheduled update

`trigger` decides which runs send the email:

- `all` (the default) or `scheduled`: each run started by one of the report's schedules sends it, once every datasheet updated. Set the schedules with the `rollstack-refresh-and-schedule` skill.
- `none`: only `sendReportEmail` or the app sends it.

Runs started with `startReportRun` or from the app never send it. A scheduled run in which a datasheet failed sends nothing, unless the failure is listed in `ignoredFailureStatusMessages`.

## When the slides agent proposes it

The user can ask the slides agent to change the email or send it. Its reply is a `settings_proposal` or an `email_send_proposal`, which does nothing until approved.

1. Show the user the proposal: the recipients, and what would change.
2. Call `approveReportMessageProposal` only if they say so, otherwise `rejectReportMessageProposal`.
3. After approving a send, follow it with `getReportMessage` until its status is `sent`, `partially_sent`, `failed` or `unconfirmed`.

Approving a send answers 409 while the report is still updating, such as after a filter change in the same message. Wait for the update, then approve again.

## Limits

- 5 email sends a minute per user, test sends and approved proposals included. Past it, calls answer 429: wait the seconds in `Retry-After`.
- Only the report's editors can change or send its email, with the `slide_decks:email` scope. A 403 means the user needs edit access or the token lacks the scope.
