---
name: cws-extension-check
description: Check a Chrome extension against the Chrome Web Store's rules before upload and build a correct upload zip. Catches what gets uploads refused or reviews rejected - not Manifest V3, name over 75 / description over 132 characters, bad version strings, missing or wrong-size 128x128 icon, _locales and __MSG_ keys that don't line up, manifest files that are missing or differ only in case, remotely hosted code (remote <script src>, importScripts/import of URLs, eval of fetched strings), declared-but-unused permissions and host permissions, chrome.* APIs used without their permission, broad host access, obfuscation, placeholder URLs, .git/node_modules/.env/.pem in the package. Drafts the single-purpose and permission-justification text for the dashboard. Use when the user says "publish my extension to the Chrome Web Store", "package/zip my extension for the store", "is my extension ready to submit", "why was my extension rejected", or quotes a violation like Blue Argon, Purple Potassium, Yellow Magnesium or Red Titanium.
---

# cws-extension-check

`scripts/cws-check.mjs` is zero-dependency Node 22+. It only reads the extension; nothing is written unless you pass `--zip`.

```
node cws-check.mjs ./my-extension                  check only
node cws-check.mjs ./my-extension --zip out.zip    check, then write the upload zip
node cws-check.mjs ./upload.zip                    check a zip you already made
node cws-check.mjs ./repo --no-dist                check the folder itself, not its dist/
node cws-check.mjs ./my-extension --json           findings as JSON
```

Point it at the extension folder, or at the repo: if `dist/`, `build/`, `.output/` (WXT) or `build/chrome-mv3-prod` (Plasmo) holds a manifest.json, that build is what gets checked, and it warns when the build looks older than the source. The report has three levels:

- **✘ Blocking**: the store refuses the upload, or Chrome won't load it, or a declared part (popup, worker, content script) won't run. Exit code 1, and `--zip` writes nothing.
- **▲ Likely rejection**: matches a documented review violation, tagged with Google's code name (Blue Argon, Purple Potassium, …) so it lines up with rejection emails.
- **! Warnings**: slower review, or worth a look.

Fix the ✘ and ▲ items, run it again, then build the zip. Show the user the findings with their file:line, not a summary.

## What it checks
- **Manifest**: valid JSON, `manifest_version` 3, name ≤ 75 and description ≤ 132 characters (after `__MSG_` lookup, in every locale), version format (1-4 integers, 0-65535, no leading zeros), `default_locale` vs `_locales/`, every `__MSG_key__` defined, MV2 leftovers (`browser_action`, `background.scripts`, string `web_accessible_resources`/CSP), CSP that adds script sources or `'unsafe-eval'`, invalid match patterns, a `key` field.
- **Icons**: a 128 entry exists, every declared icon exists, is PNG (not SVG/WebP), and its real size (read from the PNG header) matches the declared size.
- **Files**: everything the manifest points at (service worker, content scripts, popup, options, side panel, devtools, overrides, sandbox pages, DNR rule files, web-accessible resources), plus `<script src>`/stylesheets in pages, `import`/`importScripts`, and `scripting.executeScript({files})`. A reference that only matches with different capitalization is an error: Windows and macOS hide it.
- **Remote code** (MV3 bans it): remote `<script src>`, `importScripts`/`import()` of URLs, remote `.js` assigned to a script `src`, inline scripts and `onclick=` on extension pages, `eval`/`new Function`/string `setTimeout` (rejection when the string looks fetched or stored, warning otherwise), obfuscated code, and module/classic worker mismatches.
- **Permissions**: declared but unused (no `chrome.<api>` calls found), APIs called without their permission, unused host permissions, `<all_urls>`-style access, sensitive permissions, localhost hosts, `webRequestBlocking`.
- **Package**: leaves `.git`, `node_modules`, `.env`, `*.pem`, source maps, OS junk, docs, lockfiles and TypeScript sources out of the zip (unless something loads them), flags secrets in shipped code (first 4 characters only), folders and scripts nothing loads, and the 2 GB limit. The zip has `manifest.json` at the root and is read back and CRC-checked before it's written.

It also prints **dashboard drafts**: the single-purpose line, a justification per permission naming the files that use it, the host-permission sentence and the remote-code answer. Fill in the `[brackets]` with the user-facing reason; reviewers reject vague text.

## What it can't check
- Human review policy: whether the extension really has a single purpose, the listing's description and screenshots, keyword stuffing, deceptive behavior, user-data handling and consent, and whether the privacy policy matches what the code sends. It lists the external hosts the code references, as a starting point for the Data usage form.
- Code it can't see statically: URLs and file names built at runtime, webpack chunks, `chrome` passed around under another name (unused-permission findings drop to warnings when it detects that).
- Dashboard-only items: store icon padding (96x96 artwork in a 128x128 PNG), screenshots (1280x800 or 640x400), a version higher than the published one, the privacy policy URL.

## Uploading
Chrome Web Store Developer Dashboard → **Add new item** (or the item's **Package** tab → Upload new package) → choose the zip. Then fill in **Store listing** and **Privacy practices** (paste the drafts) and submit. Review usually takes a few days; broad host permissions and sensitive permissions make it longer.
