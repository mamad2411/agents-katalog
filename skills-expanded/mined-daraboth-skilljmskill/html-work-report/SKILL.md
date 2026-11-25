---
name: html-work-report
description: After completing a task, creates a clean, plain-English HTML report of what Claude did and opens it in the user's browser. Use after coding, debugging, research, installations, or multi-step work.
---

# HTML Work Report

After completing any non-trivial task, create a human-friendly HTML report. The user does not want to read a long technical explanation in the terminal.

## When not to use

Skip the report (and do not open a browser) when:

- the session runs headless or on a schedule (`claude -p`, Task Scheduler or cron jobs);
- the turn is one iteration of a `/loop` or another unattended agent loop;
- you are a sub-agent; the main session writes the report;
- the answer is a short reply or a single lookup, not finished work.

## Required behavior

1. Create the report at:

   `~/work-reports/<project>/work-report-YYYY-MM-DD-HHMM.html`

   (on Windows: `%USERPROFILE%\work-reports\<project>\work-report-YYYY-MM-DD-HHMM.html`)

   `<project>` is the name of the working directory (for example `my-app` or `notes`). Use the current date and time. Create the folders if needed. Never write the report inside a repository or the vault, so it is never committed.

2. Write a complete, standalone HTML file. Do not rely on internet-hosted CSS, JavaScript, fonts, or images.

3. Make the report easy for a non-technical person to understand:
   - Start with a large result banner: "Completed", "Partly completed", or "Needs your attention".
   - Put the most important outcome in the first sentence.
   - Use short bullets and simple words.
   - Avoid jargon, command names, code identifiers, and implementation details in the main sections.
   - Keep the main report under 300 words.
   - No em dashes and no emoji.

4. Use these sections:

   - **What I did**
   - **What changed**
   - **What you should know**
   - **Next steps**: only if action is needed
   - **Technical details**: collapsed by default

5. The Technical details section may include commands, file paths, errors, logs, and implementation notes. It must be hidden by default using `<details>`.

6. After saving the file, open it in the default browser:

   - macOS: `open "<file>"`
   - Windows, from Git Bash: `cmd //c start "" "<file>"`
   - Windows, from PowerShell: `Start-Process "<file>"`
   - Linux: `xdg-open "<file>"`

7. In the terminal, reply with only:

   `Report ready: <absolute file path>`

   Do not paste the report content into the terminal unless the user asks for it.

8. If the task failed, make that obvious at the top and explain the next practical step in plain language.

## HTML style

Use a clean, readable design:

- White or very light background
- Dark readable text
- Large title
- Clear section headings
- Comfortable spacing
- Mobile-friendly layout
- Green banner for success, amber for partial completion, red for failure
- No tracking, analytics, external requests, or executable JavaScript
