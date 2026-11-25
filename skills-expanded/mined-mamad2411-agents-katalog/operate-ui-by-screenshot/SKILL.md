---
name: operate-ui-by-screenshot
description: Operate desktop apps and websites through structured browser interfaces, DOM/HTML inspection, UI Automation, screenshots, visible UI state, clipboard paste, safe clicks, verification screenshots, and reusable app/site operation notes. Use when Codex needs to control or inspect a GUI/web app, click buttons, open software, fill forms, scrape/capture HTML, test frontend UI, use Edge/ChatGPT/GitHub/Kaggle/Luogu/Premiere, document UI process screenshots, or summarize reusable lessons from a newly explored app/site where no direct API is enough.
---

# Operate UI By Screenshot

Use this skill to drive visible desktop or web interfaces with a cautious loop. It is not only a screenshot-clicking helper: for multimodal GUI/web agents, it is a reusable operating layer that combines structured interfaces, screenshots, visible state checks, and small app/site operation notes. For web pages, prefer structured page access before visual clicking:

1. Inspect current state with a screenshot or window list.
2. Prefer an API, CLI, MCP, browser DOM snapshot, HTML fetch, Playwright, UI Automation, or app-specific automation when available.
3. If GUI operation is required, use coordinates only after a screenshot confirms the target.
4. Prefer clipboard paste for text, paths, prompts, and long form values.
5. Verify after each meaningful action with another screenshot.
6. Treat visible page health as part of correctness: do not click through corrupted layout, stale overlays, accidental full-page selection, wrong zoom, or ambiguous focus.

## Decision Order

- Use a structured API or script when it can complete the task without opening the UI.
- For account/profile inventory tasks, try official CLI/API/public endpoints before GUI browsing; use the visible browser only for authenticated state that cannot be reached otherwise.
- Use browser automation for web pages when a browser MCP, Playwright, DOM snapshot, HTML fetch, page asset, or CDP access is available.
- Use screenshot-based UI operation for visible, low-risk tasks: buttons, menus, simple text input, file dialogs, exports, and state capture.
- Continue through ordinary login only when the user explicitly authorizes it and the browser already has the needed autofill/session. Stop for passwords that must be entered manually, 2FA, CAPTCHA, payment, account/security changes, destructive confirmation, or ambiguous permission decisions.

## Web Page Strategy

For Edge, ChatGPT, or any website, use this priority order:

1. **In-app Browser / browser MCP**: use DOM snapshot, bounded read-only `evaluate`, locators, screenshots, console logs, and page assets.
2. **Terminal fetch**: use Node `fetch` or PowerShell `Invoke-WebRequest` for public pages where login and client-side rendering are not required.
3. **Debuggable Edge instance**: start a separate Edge profile with a remote debugging port only when structured DOM access is needed and using a separate browser profile is acceptable.
4. **Visible user Edge**: use screenshots, clipboard paste, and safe clicks when the existing logged-in browser state is needed.
5. **Manual checkpoint**: stop for login, CAPTCHA, payment, account changes, permission prompts, or destructive actions.

For known apps/sites, check `references/software-profiles.md` and load only the matching profile file under `references/software-profiles/`.

## Core Loop

1. **Bring target to foreground**: start the app or focus the existing window.
2. **Capture**: save a full-screen screenshot. Use `scripts/capture_screen.ps1` on Windows if no native screenshot tool is exposed.
3. **Interpret**: identify the active app, target control, expected next state, and risk level.
   - If the screenshot shows obvious layout corruption, stale overlays, unexpected full-page text selection, wrong zoom, or controls shifted away from expected positions, refresh the page/window or reset zoom before clicking again.
4. **Act**:
   - Use clipboard paste for text input.
   - Use keyboard shortcuts for standard operations such as `Ctrl+L`, `Ctrl+V`, `Enter`, `Ctrl+S`.
   - Use mouse coordinates only when the target is clearly visible and stable.
5. **Verify**: capture another screenshot, compare it to the expected state, and continue or recover.
6. **Record**: when process evidence matters, store screenshots with short ordered filenames. When a new app/site workflow becomes reusable, summarize durable operation lessons instead of saving one-off coordinates.

## Page Health Checks

Before clicking a coordinate, confirm:

- The intended app/tab is foregrounded and the URL/title matches the target.
- The page is not mid-load and no modal, toast, dropdown, or text selection obscures the target.
- Browser zoom is normal when coordinates or visual layout matter. Use `Ctrl+0` before sensitive web workflows.
- The target is visible with enough surrounding landmarks to recover if a click misses.
- For state-changing actions, the final button and the desired state label are visible in the same screenshot when possible.

## Safety Rules

- Never enter or expose passwords, 2FA codes, API keys, payment details, or private credentials.
- Do not click purchase, delete, publish, send-to-real-recipient, account-change, or irreversible controls without explicit user confirmation.
- For authorized account creation or repository/project creation, verify the owner, name, visibility, and final action button in screenshots before clicking.
- Treat dialogs, file overwrite prompts, permission prompts, and browser security warnings as checkpoints.
- If coordinates are uncertain, do not guess. Re-capture at full resolution or ask for user input.
- Keep user updates concise and state what is being clicked or pasted before sensitive-looking actions.

## Clipboard-First Input

Use paste instead of simulated typing for:

- Chinese text and mixed-language content.
- Long prompts, file paths, URLs, code, report sections, and filenames.
- Text that must preserve punctuation or line breaks.

Recommended pattern on Windows:

1. `Set-Clipboard -Value '<text>'`
2. Click the input field.
3. Send `Ctrl+V`.
4. Capture a screenshot to verify text appeared.
5. Press `Enter` or click submit only after the field is correct.

## Reusable App/Site Lessons

When a newly explored website or app becomes repeatable, add or propose a short profile file under `references/software-profiles/` and list it in `references/software-profiles.md`. Record only durable lessons:

- stable landmarks and visible state labels;
- best interface choice: API, CLI, HTML fetch, DOM, Playwright, CDP, UIA, or screenshot;
- common safe actions and verification screenshots;
- app/site-specific stop conditions;
- recovery rules for overlays, scroll traps, disabled buttons, wrong zoom, stale state, or ambiguous modals.

Do not record secrets, cookies, tokens, private user data, private screenshots, or one-off coordinates.

## References

Load only the reference needed for the current target:

- `references/windows-ui-recipes.md`: Windows screenshot, foreground, click, paste, key, and verification snippets.
- `references/web-page-interfaces.md`: structured browser, HTML, DOM, assets, scraping, and Edge/CDP strategy.
- `references/software-profiles.md`: index of maintained app/site profiles and the rule for adding more profile files.
- `references/software-profiles/*.md`: target-specific lessons for Edge/ChatGPT, GitHub, Kaggle, Luogu, Adobe Premiere Pro, and new app/site templates.
- `references/tooling-landscape.md`: when to use DOM, accessibility tree, UI Automation, image matching, or coordinates.
- `references/maintenance.md`: how to update this skill after a new UI workflow is learned.

Prefer bundled scripts over retyping Win32 snippets:

- `scripts/capture_screen.ps1`
- `scripts/list_windows.ps1`
- `scripts/focus_window.ps1`
- `scripts/open_edge_url.ps1`
- `scripts/click_at.ps1`
- `scripts/paste_text.ps1`
- `scripts/send_keys.ps1`
- `scripts/scroll_window.ps1`
- `scripts/dump_uia_tree.ps1`
- `scripts/fetch_page_summary.ps1`
- `scripts/fetch_page_summary.mjs`
- `scripts/github_public_summary.ps1`
- `scripts/github_public_summary.mjs`

Use `.ps1` helpers first on Windows. If a `.mjs` helper is useful but `node` is not on PATH, use the bundled Codex Node executable from `load_workspace_dependencies`.

## Output Expectations

When the user asks for an operation demo, report:

- The app or page reached.
- The action completed.
- Any visible result from the final screenshot.
- Any limitation, such as login, CAPTCHA, modal, or inaccessible control.

When the user asks for reusable UI automation lessons, summarize the observed loop, failure modes, and which actions are safe to generalize.
