---
name: chrome-extension-developer
description: "Ultimate Codex workflow for Google Chrome extension work: Manifest V3, WXT, Plasmo, CRXJS, content scripts, service workers, popup UI, side panel, permissions, testing, security review, payments, assets, and Chrome Web Store publishing."
---

# Chrome Extension Developer

Use this skill when the task involves a Google Chrome extension, Manifest V3,
WXT, Plasmo, CRXJS, a browser extension popup, content script, service worker,
side panel, options page, extension permissions, Chrome Web Store submission, or
extension monetization.

This is the router and operating kernel for the specialist skills installed in
this plugin. Load the smallest relevant specialist skill before task actions:

| User intent | Load this specialist |
| --- | --- |
| New extension, scaffold, architecture | `../extension-create/SKILL.md` |
| Add a feature or debug runtime behavior | `../extension-dev/SKILL.md` |
| Manifest, permissions, host permissions | `../extension-manifest/SKILL.md` |
| Security, performance, best practices | `../extension-analyze/SKILL.md` |
| Chrome Web Store rejection risk | `../extension-review/SKILL.md` |
| Unit, integration, E2E testing | `../extension-test/SKILL.md` |
| Popup, side panel, options, content UI | `../extension-ui/SKILL.md` |
| Icons, screenshots, listing assets | `../extension-assets/SKILL.md` |
| Publishing, packaging, CI/CD | `../extension-publish/SKILL.md` |
| MV2 to MV3 migration | `../extension-migration/SKILL.md` |
| Payments, licensing, subscriptions | `../extension-payment/SKILL.md` |
| Backend, auth, proxy, webhooks | `../extension-backend/SKILL.md` |

## Workflow

1. Detect the current stack before editing.
   - Prefer the included script: `scripts/detect-extension-stack.ps1`.
   - Look for `wxt.config.ts`, `plasmo.config.ts`, `vite.config.*`,
     `manifest.json`, `package.json`, `src/`, `entrypoints/`, `public/`, and
     browser-specific output folders.
2. Identify extension contexts and data flow.
   - Popup, side panel, options, content script, background service worker,
     offscreen document, devtools page, injected page script, backend API.
3. Map permissions from actual Chrome API usage.
   - Prefer `activeTab`, optional permissions, and narrow host patterns.
   - Use `scripts/audit-extension-manifest.ps1` for a first-pass read-only scan.
4. Implement in the existing framework.
   - WXT: use `entrypoints/` and `wxt.config.ts`.
   - Plasmo: use `src/popup.tsx`, `src/background.ts`, `src/contents/*`, and
     Plasmo manifest overrides.
   - CRXJS: keep Vite and manifest conventions.
   - Vanilla: keep direct `manifest.json` and plain JS/TS files.
5. Verify with checks that can fail.
   - Run the project package manager's lint/test/build/package scripts when
     present.
   - For UI changes, load or screenshot popup/side panel/options/content UI.
   - For messaging bugs, test each sender/receiver context explicitly.
6. Handoff with what changed, checks run, and any unverified browser/manual
   steps.

## Chrome Extension Rules

- Manifest V3 is the default. Preserve MV2 only during explicit migration work.
- Background logic must be event-driven. MV3 service workers can be suspended.
- Do not use remote code, `eval`, CDN scripts, or dynamic script strings.
- Do not store API keys or provider secrets in extension source code.
- Validate every `runtime.onMessage` request and sender before trusting it.
- Treat page DOM content as untrusted input. Avoid `innerHTML` for untrusted
  strings.
- Keep permissions minimal and explain any user-visible warning.
- Use `host_permissions` for URL patterns, not `permissions`.
- Use `chrome.scripting.executeScript()` instead of deprecated tab injection.
- Keep content scripts small; lazy-load heavy UI or logic where possible.
- Use `chrome.storage.session` for temporary state, `local` for device data, and
  `sync` only for small cross-device settings.
- Publishing, external payment setup, store submission, and production backend
  changes require explicit user approval.

## Current Docs

Extension APIs, WXT, Plasmo, Vite, React, Vue, Svelte, payment providers, and
Chrome Web Store rules are moving targets. For implementation details, fetch
current official documentation when available. Prefer official Chrome docs,
framework docs, and provider docs over blog posts.

## Source References

- `references/source-material.md` records the attached files used to build this
  plugin and their role.
- `references/browser-extension-builder-source.md` preserves the broad
  extension-builder skill supplied by the user.
- `references/wxt-repomix-source-yamadashy.md` and
  `references/wxt-repomix-source-repomix.md` preserve the WXT/Repomix-specific
  attached skills.
- The 12 `extension-*` specialist skills and their reference directories come
  from the attached `browser-extension-skills-main.zip` pack.

## Default Handoff

For implementation work, end with:

- Changed files.
- Verification commands and results.
- Browser/manual checks run or not run.
- Remaining risk, especially store-policy, permissions, auth, payment, or
  production backend risk.
