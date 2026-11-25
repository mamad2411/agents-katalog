---
name: browser-automation-master
description: Master hub for Browser automation & visual QA. Use to automate the browser: visual QA, network auditing, and flow recording. Bundles 7 specialized skills (in skills/<name>/GUIDE.md). Use this for any browser automation task.
---

# Browser automation & visual QA — Master Hub

Use to automate the browser: visual QA, network auditing, and flow recording.

## How to use this hub

This single skill bundles **all 7 browser automation skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **blastum-puppeteer** — Headless web browser automation for document acquisition and page scraping. Use when fetching JavaScript-rendered pages, extracting clean document content, or bypassing basic bot detection for pers...  
  → `skills/blastum-puppeteer/GUIDE.md`
- **comparing-branches-visually** — Check out two branches in separate worktrees, start both dev servers on different ports, screenshot the same pages, and produce a visual diff.  
  → `skills/comparing-branches-visually/GUIDE.md`
- **network-request-auditing** — After navigating and interacting in Cursor's built-in browser, use browser_network_requests to audit every fetch/XHR for failures, slowness, duplicate calls, and suspicious payloads. Use for API-he...  
  → `skills/network-request-auditing/GUIDE.md`
- **recording-browser-flow-as-test** — Execute a user flow step-by-step in Cursor's built-in browser while documenting each action, then emit a Playwright test that replays the same flow using stable selectors derived from the accessibi...  
  → `skills/recording-browser-flow-as-test/GUIDE.md`
- **screenshotting-changelog** — Generate a visual changelog or PR description by taking before/after screenshots of UI changes using Cursor's built-in browser. Use when preparing a PR with visual changes.  
  → `skills/screenshotting-changelog/GUIDE.md`
- **verifying-in-browser** — After making code changes, start the dev server, open the app in Cursor's built-in browser, and verify everything works — check rendering, console errors, and network health. Use proactively after ...  
  → `skills/verifying-in-browser/GUIDE.md`
- **visual-qa-testing** — Visually QA a web application by launching it in Cursor's built-in browser, taking screenshots, checking console errors, and auditing network requests. Use after making UI changes to verify they lo...  
  → `skills/visual-qa-testing/GUIDE.md`

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
