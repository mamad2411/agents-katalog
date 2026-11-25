---
name: teams-sender
description: Send a message to someone on Microsoft Teams. Use when the user wants to message a person or channel on Teams. Requires browser automation via Playwright.
---

# Teams Sender

Send a message to a person on Microsoft Teams using Playwright browser automation.

## Workflow

1. Navigate to https://teams.microsoft.com and wait 3 seconds
2. Use the search box at the top to find the recipient by name — type then wait 2 seconds
3. Take a browser_snapshot — read the search results (name, email, title)
4. **MANDATORY CONFIRMATION** — call ask_user:
   "Confirm Teams message:
    To: [Full Name] ([email@domain.com]) — [Job Title]
    Message: [exact message text]

    Reply YES to send, or NO to cancel."
   If MULTIPLE people match, list ALL and ask user to pick.
5. WAIT for user response. If anything other than YES → abort immediately.
6. Click on the correct person from search results, wait 2 seconds
7. Take a browser_snapshot to find the compose box
8. Type the message using browser_type
9. Press Ctrl+Enter to send (do NOT search for the Send button — Ctrl+Enter is faster)

## Rules

- NEVER send a message without calling ask_user first and receiving YES.
- NEVER guess which person to message if multiple results appear — list all and ask.
- ALWAYS include the recipient's email address in the confirmation prompt. The email is visible in Teams search results.
- If Teams shows a login page, STOP and report that the session has expired.
- Keep messages professional and concise.
- Do NOT modify or delete any existing messages.
