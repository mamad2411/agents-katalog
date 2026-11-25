---
name: chatgpt-images-browser-playbook
description: >-
  Use when generating stills on chatgpt.com with a signed-in browser session —
  Images UI only, one still per dispatch, no API keys, no cookie scraping,
  no sleep-poll loops. Session-only; hand the box to the owner for login/2FA.
---
# ChatGPT Images browser playbook

Automate ChatGPT Images through a signed-in box browser session. No API keys. No cookie scraping. No private endpoint scripts. No Shell-driven CDP, Playwright, Puppeteer, or cookie DB reads.

This is a **session-only** playbook: drive the live Images UI the owner already uses. It is product-agnostic — attach whatever identity or style reference images the current job requires.

## Session
1. Open `https://chatgpt.com` in the box browser on the account the owner already uses for Images.
2. Confirm Images / image gen is available (Plus or whatever plan they use). If login or 2FA blocks, hand the box to the owner. Do not lift cookies.
3. Prefer one long signed-in session. Reuse the tab. Do not open parallel browsers that fight the same login.

## How to drive the UI
1. Delegate clicks and typing to a browser or desktop subagent. Do not drive Chrome from Shell.
2. Scope each dispatch tightly: one prompt, attach named refs, wait for the still, download or save it, stop.
3. For a batch, loop many narrow dispatches (one still each). Do not ask one subagent to "generate the whole pack."
4. Always attach the locked identity / style reference images the job requires before Generate. Do not invent product cast locks or character sheets in this skill — those belong to the project brief.
5. Use the image-generation controls available in the current session. Do not assume a specific model name or picker exists. Reject GenerateImage and other local generators for this lane.
6. **No sleep-poll loops.** Do not chain `sleep 15` / `sleep 20` / `sleep 30` waiting on the UI. Wait on the page result in the browser subagent, or stop and report. Retry once on rate limit, then pause.

## Batch recipe
For each item in the current stage list (from the project PLAN or a companion consistency skill):
1. Build one clear English prompt (subject, look, camera, what must stay exact).
2. Dispatch: open Images, attach refs, paste prompt, generate, wait until the image is ready.
3. Save the file into the project folder with a stable name.
4. Quality-gate against the project brief. Redo once if it fails. Escalate to the owner after two fails.
5. Mark the item done and move to the next. Report progress; offer a question widget to continue or pause.

## Hard stops
- Login wall, captcha, phone verify, or payment wall → hand the box to the owner.
- Rate limit or "try again later" → wait and retry once, then pause the batch and tell the owner.
- UI changed so the Images controls cannot be found → stop and report. Do not invent a cookie or API workaround.
- Any urge to scrape session cookies or call undocumented ChatGPT APIs → refuse.

## Anti patterns
- GenerateImage "just this once."
- Parallel browser sessions on the same ChatGPT login.
- Sleep-poll shell loops instead of waiting on the page.
- One sprawling "do the whole pack" computerUse task.
- Baking product-specific cast boards or character locks into this playbook.
