---
name: gpt-pro
description: Operate ChatGPT Pro through Browser Use/Playwright or Computer Use. Use when the user asks Codex to ask GPT Pro, prompt GPT Pro, use ChatGPT Pro, send a prompt to ChatGPT Pro/GPT Pro, or wait for a GPT Pro result. Checks whether Browser Use/Playwright and/or Computer Use are available, asks for a first-run default route when both are available, selects Pro, submits prompts, waits through long reasoning or streaming, and returns the completed answer while pausing for login, MFA, CAPTCHA, account-security prompts, and never exporting or saving cookies, session tokens, or auth credentials.
---

# GPT Pro

Use the in-app browser, or the user's already-authenticated default browser via Computer Use when needed, to send the user's prompt to ChatGPT Pro and wait for the final answer.

## Route Selection

1. Check which browser-control routes are available in the current Codex session before navigating:
   - Browser Use / Playwright route: available when `mcp__playwright__` browser tools or equivalent in-app browser tools are present.
   - Computer Use route: available when `mcp__computer_use__` tools are present.
   - If tool availability is unclear and `tool_search` exists, search for Playwright/browser navigation tools and Computer Use desktop-control tools.
2. If neither route is available, report that this skill requires Browser Use/Playwright or Computer Use and stop.
3. If exactly one route is available, use that route.
4. If both routes are available, check for a saved default route in `preferences.json` next to this `SKILL.md`.
5. If the current user prompt explicitly requests `playwright`, `Browser Use`, `in-app browser`, `Computer Use`, or the default browser, use that as the current-run route even when a saved default exists.
6. If both routes are available and no saved default exists, ask the user which route to use by default going forward. Treat this as a separate preference question, not as a request to reroute the current run. Ask it even when the current prompt explicitly requested a one-off route, and keep the one-off route for the current run unless the user says otherwise:
   - `playwright`: use Browser Use / in-app browser by default.
   - `computer-use`: use Computer Use with the user's already-authenticated default browser by default.
7. After the user chooses, save the preference as JSON in `preferences.json` next to this `SKILL.md`, for example:

```json
{
  "default_route": "playwright"
}
```

8. If the saved preference is missing, malformed, or names an unavailable route, ignore it for the current run and ask again when both routes are available.
9. If the preference file cannot be written, continue with the selected route for the current request and tell the user that the default was not saved.

## Workflow

1. Use the selected route from Route Selection. For `playwright`, navigate the Browser Use / in-app browser to `https://chatgpt.com/` if ChatGPT is not already open. For `computer-use`, open `https://chatgpt.com/` in the user's default browser and operate the visible UI.
2. If the selected route fails before prompt submission, try the other available route when it exists and explain the switch.
3. Use only the browser's existing authenticated session. If login, MFA, CAPTCHA, account verification, billing, rate-limit, or security prompts appear, pause and ask the user to complete them in the browser.
4. Never request, read, export, save, persist, or recreate passwords, one-time codes, recovery codes, cookies, localStorage, sessionStorage, authorization headers, browser profile files, or other ChatGPT/OpenAI auth material.
5. Start a new chat unless the user explicitly asks to continue the current conversation.
6. Open the model selector and choose `Pro` / `Research-grade intelligence`.
7. Verify that Pro is selected, such as by checking for the Pro composer pill or the Pro model-picker state. If Pro is unavailable, report that directly and do not silently fall back to another model.
8. Enter the user's prompt exactly, preserving constraints and requested wording. Attach files only when the user supplied or requested them.
9. Submit the prompt.
10. Wait until the response is complete. Poll while the UI shows `Stop streaming`, `Reasoning...`, a progress indicator, or changing assistant text. GPT Pro can take several minutes; keep waiting unless the user interrupts or the browser reaches a clear error state.
11. Return the latest assistant answer and the conversation URL. Include any visible error, timeout, or uncertainty about model selection instead of overclaiming.

## Computer Use Fallback

- Treat Computer Use as a fallback for the user's real browser session, not as a way to harvest or persist auth.
- Prefer a new tab/window for a new prompt unless the user asks to continue a visible conversation.
- Use the accessibility tree to identify the composer, Pro pill/model selector, send button, stop-streaming control, and final assistant text.
- Expect this route to be more fragile than Browser Use because it depends on window focus, layout, zoom, accessibility permissions, and visible UI state.

## Completion Checks

- Treat the answer as complete only after streaming controls disappear and the latest assistant text has stabilized.
- Extract the final assistant message, not hidden reasoning or details panels.
- If the browser loses authentication or asks for a private verification step, stop at that boundary and ask the user to take over in the browser.
