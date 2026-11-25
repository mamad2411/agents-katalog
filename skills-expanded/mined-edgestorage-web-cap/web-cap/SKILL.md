---
name: web-cap
description: Use when you need to operate or inspect a real browser tab through local-first browser automation, including clicking, typing, reading page state, extracting data, navigating pages, or running reusable scripts against live browser sessions.
---

# Web Cap CLI

## Overview

Web Cap is a command-line browser automation toolkit for agents. The npm package is `web-capability`, and the installed CLI command is `web-cap`.

Use `web-cap --help` to view all available commands, and `web-cap <command> --help` to inspect options for a specific command.

## Check And Install

If the `web-cap` command is not available, install the CLI:

```bash
npm install -g web-capability
```

The browser side requires the `web_cap` extension/runtime to be loaded and connected. Users can download the browser extension from the latest GitHub Release at `https://github.com/edgestorage/web-cap/releases/latest`.

## Connection Checks

Before the first page automation step in a task, run:

```bash
web-cap session-status
```

Use the result to decide the next step:

- If the `web-cap` command is missing, install the CLI with `npm install -g web-capability`, then run `web-cap session-status` again.
- If no browser runtime is connected, tell the user to install or enable the `web_cap` extension. The extension can be downloaded from the latest GitHub Release: `https://github.com/edgestorage/web-cap/releases/latest`.
- If the extension is installed but still disconnected, ask the user to confirm that the `web_cap` extension is enabled and that a normal `http` or `https` tab is open.
- If `session-status` lists multiple tabs, choose the tab that matches the user's requested title or URL. Do not guess a tab id when the target is ambiguous.
- If the intended tab is not listed, ask the user to open or focus the target page, then run `web-cap session-status` again.
- If `session-status` returns `availableScripts.sites` for the target page, inspect the listed site directory before writing a new script or doing non-trivial page-specific work.
- Do not run `script-execute` until you have a specific `--tab-id` from `session-status`.

## Run Scripts

Prefer running scripts directly with `script-execute`:

```bash
web-cap session-status
web-cap script-execute --tab-id <tab-id> --script "export default async function () { return { ok: true, title: document.title, url: location.href }; }"
```

Choose the lightest script form that fits the task:

- Use one-off inline `--script` only for very small reads such as `document.title`, `location.href`, or a short visible text fragment.
- Use `--script-file` for non-trivial scripts, generated scripts, or anything with quoting-sensitive selectors or template strings.
- Save repeated or site-specific workflows under `${WEB_CAP_PATH}` as reusable capability scripts.
- Pass variable data through `--input` or `--input-file`.
- Return structured JSON objects, including `ok`, `url`, and `title` when useful.

## Script Files

When using saved reusable Web Cap scripts:

- Resolve `WEB_CAP_PATH`; if it is not defined, use `.web-cap` in the current working directory.
- When `session-status` shows `availableScripts.sites[]` entries for the target page, run `ls <directory>` on the listed directory to see whether an existing script can be reused.
- Look under `${WEB_CAP_PATH}/<domain>/` for scripts that match the target site or workflow.
- Read `${WEB_CAP_PATH}/<domain>/README.md` when it exists before running a saved script.
- Execute saved scripts with `script-execute --tab-id <tab-id> --script-file <path>`.
- Use `--script-file -` to read script source from stdin, and `--input-file -` to read JSON input from stdin. Prefer stdin for long generated scripts or JSON input that would be awkward to shell-escape.
- Do not use `--script-file -` and `--input-file -` in the same command, because stdin can only be consumed once.
- Before writing any file under `${WEB_CAP_PATH}` or a reusable script domain directory, read `references/how-to-write-reusable-scripts.md`.
- When saving a new reusable script, write it to `${WEB_CAP_PATH}/<domain>/<capability-name>.js`.
- Follow `references/how-to-write-reusable-scripts.md` for reusable script metadata, naming, examples, and README format.

```bash
web-cap script-execute --tab-id <tab-id> --script-file .web-cap/example.com/read-page-summary.js --input '{"limit":10}'
web-cap script-execute --tab-id <tab-id> --script-file - < script.js
web-cap script-execute --tab-id <tab-id> --script-file .web-cap/example.com/read-page-summary.js --input-file - < input.json
```

## Script-Execute Guidelines

These guidelines apply to scripts run explicitly with `script-execute`, including
reusable capability scripts. They do not apply to page userscripts.

Write `script-execute` scripts as small browser functions with clear boundaries:

- Accept variable behavior through input JSON.
- Return structured JSON objects, not raw arrays or loose strings.
- Include `ok` in structured results.
- Normalize whitespace before returning page text.
- Filter hidden elements with computed style and bounding boxes.
- Use waits sparingly and expose timing through result fields when it affects reliability.
- For destructive actions, return a preview plan first unless the user explicitly asked to perform the action.
- For controlled multi-page workflows, return `cap.goto(url, nextInput)`. Web Cap navigates to `url`, then reruns the same script with exactly `nextInput` as `input`; `cap.goto` is a continuation, not final output.
- Because page/script state is lost after navigation, carry all needed state in `nextInput` and handle it at the top of the same script. Every goto workflow must eventually return a normal JSON result, not another `cap.goto(...)`.

Example one-off read:

```bash
web-cap script-execute --tab-id <tab-id> --script "export default async function () { return { ok: true, title: document.title, url: location.href, text: document.body.innerText.slice(0, 4000) }; }"
```

## Script-Execute Page Operations

When a `script-execute` script operates on page content, prefer the Playwright-compatible runtime APIs exposed as global `page` and `cap.page`. Use `page.locator(...)`, role/text helpers, and locator actions instead of hand-rolled DOM clicks or form mutations.

If the target element cannot be determined confidently from roles, text, selectors, or DOM state, capture a screenshot before taking action. Use visual confirmation to disambiguate the target and avoid guessing, especially when controls have similar labels, icons, or repeated layouts.

Use `browser-screenshot` with the tab id from `session-status`:

```bash
web-cap browser-screenshot --tab-id <tab-id> --pretty
```

Example form interaction:

```javascript
export default async function (input) {
  await page.locator('input[name="email"]').fill(input.email);
  await page.locator('input[name="password"]').fill(input.password);
  await page.getByRole("button", { name: "Login" }).click();

  return {
    ok: true,
    url: location.href,
    title: document.title
  };
}
```

Example controlled navigation:

`cap.goto(url, nextInput)` is a continuation: every goto path must feed a later branch in the same script, and that branch must eventually return a normal JSON result. Carry every cross-page field you need through `nextInput`.

Minimal pattern:

```javascript
export default async function (input = {}) {
  if (input.step === "read") {
    return {
      ok: true,
      url: location.href,
      title: document.title,
      text: document.body.innerText.slice(0, 4000)
    };
  }

  const url = input.url;
  if (!url) return { ok: false, error: "No URL provided" };

  return cap.goto(url, { url, step: "read" });
}
```

Example repeated item extraction:

```javascript
export default async function (input) {
  const cards = page.locator(input.cardSelector);
  const count = Math.min(await cards.count(), input.limit ?? 20);
  const items = [];

  for (let index = 0; index < count; index += 1) {
    const card = cards.nth(index);
    items.push({
      title: await card.locator(input.titleSelector).first().textContent().catch(() => ""),
      href: await card.locator("a").first().getAttribute("href").catch(() => "")
    });
  }

  return { ok: true, url: location.href, title: document.title, items };
}
```

## Stateful Site Actions

For actions that change a user's account or site state, prefer browser-visible UI operations such as clicking the page's own buttons and verifying the resulting page state.

Avoid calling a site's private or semi-private HTTP APIs directly, even from the same-origin page context, unless the user explicitly asks for API-based execution or the UI path is unavailable and the tradeoff is explained first.

When opening pages or tabs only to perform an operation, treat them as temporary and close them before finishing the task, after the operation and verification are complete. Do not leave temporary pages open unless the user asked to keep them open or the page is useful context for the next step.

## Tab Selection And Cleanup

Use `web-cap session-status` as the source of truth for available tabs and tab ids:

- Reuse the user's existing target tab when the task is about a page they already opened.
- Do not close tabs that were already open before the task unless the user explicitly asks.
- Temporary tabs opened only for lookup, navigation, or verification should be closed after the result is captured.
- Keep a tab open when it is the deliverable, when the user asked to keep it open, or when the next step depends on the page staying live.
- Keep a tab open for handoff when it is waiting for user login, approval, payment, CAPTCHA, or another user-only action.
- If multiple tabs match, prefer a tab whose title or URL clearly matches the user's request. Ask for the target tab when the match is ambiguous.

## Page Userscripts

Use page userscripts only when the user needs persistent automatic behavior on
matching page loads. For normal extraction, clicking, navigation, or one-off
workflows, use `script-execute`.

Reusable capability scripts and page userscripts are different script types:

| Script type | Purpose | How it runs | Where it belongs |
| --- | --- | --- | --- |
| Reusable capability script | Agent-triggered browser workflow that can accept JSON input and return structured JSON output. | Run explicitly with `web-cap script-execute --script-file <path>`. | `${WEB_CAP_PATH}/<domain>/<capability-name>.js`. |
| Page userscript | Page lifecycle script that should run automatically when matching pages load. | Installed with `web-cap userscript install --file <path>` and then injected by the extension. | Source file can live anywhere before install; after install, Web Cap copies it into the managed userscripts state directory. Do not store userscripts in `${WEB_CAP_PATH}` reusable script folders. |

Only reusable capability scripts in `${WEB_CAP_PATH}` are meant to be run with
`script-execute`. Do not put page userscripts under `${WEB_CAP_PATH}/<domain>/`,
because the reusable script registry treats that folder as `script-execute`
capabilities.

Page userscripts do not use `export default`, do not accept `script-execute`
input JSON, do not return structured command output, and cannot use
`script-execute` helpers such as `cap.goto`.

Use `web-cap userscript` files for scripts that should run automatically when
matching pages load:

```javascript
/**
 * web-cap userscript
 *
 * @id com.example.foo
 * @name Foo
 * @version 1.0.0
 * @match https://example.com/*
 * @runAt document-idle
 */
console.log("foo");
```

Userscript metadata fields:

- `@id`: Required stable identity for the userscript. Use a lowercase dotted id
  that names the site and purpose, such as `com.example.hide-ads`. Keep it
  unchanged when updating the same script. Changing `@id` creates a separate
  userscript instead of overwriting the old one; remove the old id first when
  replacing it.
- `@name`: Human-readable display name.
- `@version`: Script version for tracking installed revisions. Increase it when
  behavior changes.
- `@match`: Page scope using WebExtensions/Chrome match pattern syntax, for
  example `https://example.com/*` or `*://*.example.com/docs/*`.
- `@runAt`: Injection timing using WebExtensions userscript timing values:
  `document-start`, `document-end`, or `document-idle`.

Install and manage page userscripts with:

```bash
web-cap userscript install --file ./foo.js
web-cap userscript install --file - < foo.js
web-cap userscript list
web-cap userscript list --id com.example
web-cap userscript list --match-url https://example.com/page
web-cap userscript list --status active
web-cap userscript show com.example.foo
web-cap userscript enable com.example.foo --apply-now
web-cap userscript disable com.example.foo
web-cap userscript remove com.example.foo
```
