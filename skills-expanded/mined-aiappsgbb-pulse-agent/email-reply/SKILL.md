---
name: email-reply
description: Reply to an email in Outlook Web. Use when the user wants to send an email reply. Navigates to the specific email thread and sends a reply. Requires browser automation via Playwright.
---

# Email Reply

Reply to an email using Outlook Web (outlook.office.com) via Playwright browser automation.

## Workflow

1. Navigate to `https://outlook.office.com/mail/` and wait 3 seconds
2. Take a `browser_snapshot` — confirm the inbox is visible. If you see a login page, STOP and report that the session has expired.
3. Find the target email:
   a. Use the search box at the top — click it, type the sender name or subject, wait 2 seconds
   b. Take a `browser_snapshot` to read search results
   c. Click on the matching email to open it
   d. Wait 2 seconds, take a `browser_snapshot` to confirm the email thread is open
4. Read the email content from the snapshot to confirm this is the correct thread (verify sender, subject, and recent message content)
5. **MANDATORY CONFIRMATION** — call `ask_user`:
   "Reply to email:
    Thread: [subject line]
    From: [sender name]
    Last message: [brief summary of the most recent message]

    Draft reply:
    ---
    [the draft reply text]
    ---

    Reply YES to send, or NO to cancel."
6. WAIT for user response. If anything other than YES → abort immediately.
7. Click the "Reply" button (not Reply All, unless specifically requested)
8. Wait 2 seconds, take a `browser_snapshot` to find the reply compose area
9. Type the reply message using `browser_type` into the compose box
10. Take a `browser_snapshot` to verify the message appears correctly in the compose area
11. Click the "Send" button, or press Ctrl+Enter
12. Wait 2 seconds, take a `browser_snapshot` to confirm the reply was sent (compose area should close)
13. Report success: "Reply sent to [sender] re: [subject]"

## Finding the Right Email

If search doesn't find the email:
- Try searching by subject line keywords instead of sender name
- Try scrolling through recent emails in the inbox list
- If the email is in a specific folder, navigate there first

If multiple emails match:
- Take a snapshot showing all matches
- Include them in the `ask_user` confirmation and ask the user to pick

## Rules

- NEVER send a reply without calling `ask_user` first and receiving YES.
- NEVER use Reply All unless the user explicitly requests it. Default is Reply (to sender only).
- ALWAYS show the draft reply text in the confirmation prompt so the user can review it.
- ALWAYS verify you're replying to the correct thread by checking sender and subject.
- If Outlook shows a login page or error, STOP and report the issue.
- Keep replies professional and concise.
- Do NOT modify, delete, or forward any emails unless explicitly asked.
- Do NOT open or download attachments.
- If the compose area isn't found after clicking Reply, take a snapshot and report what you see.
