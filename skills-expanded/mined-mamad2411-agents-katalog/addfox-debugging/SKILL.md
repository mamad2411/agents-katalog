---
name: addfox-debugging
description: >-
  Debug Addfox CLI and runtime. Interpret terminal output and .addfox/error.md (entry, location, message, stack,
  front-end-framework), .addfox/meta.md, addfox build -r / dev -r Rsdoctor reports, extension load failures
  (chrome://extensions, about:debugging), blank popup, content script not injecting, defineShadowContentUI not visible,
  messaging sendMessage undefined, HMR/hot reload, duplicate React, MV3 service worker registration.
metadata:
  tags: addfox, debugging, build-error, error.md, meta.md, rsdoctor, hot-reload, hmr, browser-extension, troubleshooting
---

## When to use

Use this skill **as soon as** something fails in an Addfox workflow: `addfox build` / `addfox dev` errors, user pastes stack traces, **`.addfox/error.md`** exists, extension does not load, popup is white screen, content UI never mounts, messages return `undefined`, or hot reload stopped updating.

Trigger examples:

- "addfox 构建失败", "Cannot find module", "Manifest validation"
- "扩展加载不了", "popup 空白", "content script 没注入"
- "defineShadowContentUI 不显示", "z-index", "CSP"
- "热更新不生效", "Rsdoctor", "bundle 太大"
- "Chrome 可以 Firefox 不行"

For **correct patterns** (how config should look), use **addfox-best-practices** after unblocking. For **test flakiness**, use **addfox-testing**.

## How to use

Work through sections 1–7 below in order: terminal → `.addfox/error.md` → runtime reproduction → Rsdoctor if bundle-related. Extra context: [reference.md](reference.md).

---

# Addfox Debugging

Read terminal output, `.addfox/error.md`, `.addfox/meta.md`, and Rsdoctor reports.

---

## 1. Build errors (read terminal and .addfox/error.md)

Addfox produces detailed error information when build fails.

### 1.1 Build Failure Sources

| Source | Symptoms | Diagnostic Location |
|--------|----------|---------------------|
| Config syntax | `addfox.config.ts` load error | Terminal + `.addfox/error.md` |
| TypeScript errors | Red squiggles, type check failures | Terminal |
| Missing dependencies | `Cannot find module` | Terminal |
| Manifest validation | Invalid manifest structure | Terminal + `.addfox/error.md` |
| Plugin errors | Framework plugin failures | Terminal |
| Entry discovery | Missing entry files | Terminal |

### 1.2 Error Structure (error.md)

When present, `.addfox/error.md` contains structured information:

```markdown
## Error Summary
- **entry**: popup/index.tsx
- **location**: /path/to/project/app/popup/index.tsx:42
- **message**: Cannot find module '../components/Button'
- **stack**: Error: Cannot find module...
  at resolve (...)
  at load (...)
- **front-end-framework**: react
```

**Common error fields:**
- `entry` — Which entry point failed (e.g., `content/index.ts`, `popup/index.tsx`)
- `location` — File path and line number
- `message` — Human-readable error description
- `stack` — Stack trace
- `front-end-framework` — React/Vue/Svelte/etc. detection

### 1.3 Error Analysis Steps

1. **Check terminal** — First error message is most relevant
2. **Check `.addfox/error.md`** — If it exists, contains structured error info
3. **Check `.addfox/meta.md`** — Build metadata, useful for verification
4. **Validate config** — Ensure `addfox.config.ts` is syntactically valid
5. **Check entry files** — Verify file paths in `entry` config exist

### 1.4 Common Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module '@rsbuild/plugin-*'` | Missing framework plugin | `pnpm add -D @rsbuild/plugin-react` (or @addfox/rsbuild-plugin-vue, etc.) |
| `Manifest version mismatch` | MV2 vs MV3 conflict | Set `manifest_version: 3` explicitly |
| `Entry not found` | Wrong path in `entry` | Check relative path from project root |
| `Invalid host permission` | Malformed match pattern | Use valid pattern like `*://*.example.com/*` |
| `Service worker registration failed` | Background path error | Ensure `app/background/index.ts` exists |

---

## 2. Framework-specific errors

### 2.1 React

**Hook errors:**
```
Invalid hook call. Hooks can only be called inside...
```
- Causes: Multiple React copies, mismatched versions
- Fix: Ensure single React version; check `pnpm ls react`

**JSX transformation errors:**
```
Unexpected token `<`
```
- Fix: Ensure `@rsbuild/plugin-react` plugin is in config

### 2.2 Vue

**Reactivity warnings:**
```
[Vue warn]: Avoid app logic that relies on enumerating...
```
- Causes: Mutating reactive object in wrong lifecycle
- Fix: Use `ref()` and `computed()` properly

### 2.3 TypeScript

**Type errors during build:**
```
TS2345: Argument of type '...' is not assignable to parameter of type '...'
```
- Fix: Run `tsc --noEmit` separately to isolate type issues
- Check `tsconfig.json` paths and module resolution

---

## 3. Runtime debugging

### 3.1 Extension Not Loading

**Chrome:**
1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `.addfox/extension/` directory

**Firefox:**
1. Go to `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Select `manifest.json` from `.addfox/extension/`

### 3.2 Content Script Not Injecting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Script doesn't appear on page | Wrong `matches` pattern | Check manifest `content_scripts.matches` |
| Script runs but no UI | Target element not found | Wait for `DOMContentLoaded` |
| Styles not applied | CSS not bundled | Import CSS in content entry |
| CSP blocking | Inline script execution | Use external files only |

**Debug steps:**
1. Open DevTools on target page
2. Check Console for content script logs
3. Verify `chrome.scripting.executeScript` worked (if programmatic)
4. Check Network tab for script loading

### 3.3 Content UI Not Appearing

When using `defineShadowContentUI` or `defineIframeContentUI` from `@addfox/utils`:

| Issue | Diagnostic | Fix |
|-------|------------|-----|
| UI not visible | Check Elements tab for shadow root/iframe | Verify `target` selector matches existing element |
| Styles broken | Check shadow DOM CSS isolation | Import styles in content script entry |
| Z-index issues | Element exists but hidden | Set `z-index: 2147483647` on container |
| Mount timing | `target` not yet in DOM | Wait for `DOMContentLoaded` or mutation observer |

**Debug code:**
```ts
import { defineShadowContentUI } from '@addfox/utils';

const mountUI = defineShadowContentUI({
  name: 'debug-ui',
  target: 'body',
  attr: { style: 'border: 2px solid red !important;' }  // Visual debug
});

// Log mount result
const root = mountUI();
console.log('Content UI mounted:', root);
console.log('Shadow root:', root.shadowRoot);
console.log('Parent element:', root.parentElement);
```

### 3.4 Messaging Not Working

**Symptoms:** Messages not received, `sendMessage` throws, `undefined` response.

**Diagnostic steps:**
1. Verify sender includes `from` field:
   ```ts
   chrome.runtime.sendMessage({ from: 'popup', action: 'ping' });
   ```
2. Check receiver is listening:
   ```ts
   chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
     console.log('Received:', msg.from, msg.action);
     return true; // Keep channel open for async
   });
   ```
3. Verify `chrome.tabs.sendMessage` uses valid `tabId`
4. Check if content script is injected on target tab
5. **Ensure using polyfill consistently** (see cross-browser section below)

**Common mistakes:**
```ts
// ❌ Wrong - not returning true for async response
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  fetchData().then(data => sendResponse(data));
  // Missing return true;
});

// ✅ Correct - async response
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  fetchData().then(data => sendResponse(data));
  return true; // Keep message channel open
});
```

### 3.5 Hot Reload Issues

**Symptoms:** Changes not reflected, extension reloads but old code runs.

**Diagnostic steps:**
1. Check `.addfox/` directory has recent timestamps
2. Reload extension manually in `chrome://extensions/`
3. Clear browser cache (DevTools → Network → Disable cache)
4. Restart dev server: `Ctrl+C`, then `addfox dev`

**Firefox-specific:**
- Hot reload may be less reliable; use manual reload
- Check `about:debugging` for extension errors

---

## 4. Cross-browser debugging

### 4.1 Using webextension-polyfill

**Strongly recommended** for consistent debugging across Chrome and Firefox:

```ts
import browser from 'webextension-polyfill';

// Debugging wrapper
async function sendMessageWithDebug(message: any) {
  try {
    const response = await browser.runtime.sendMessage(message);
    console.log('Message sent:', message, 'Response:', response);
    return response;
  } catch (error) {
    console.error('Message failed:', message, error);
    throw error;
  }
}
```

### 4.2 Chrome vs Firefox Differences

| Feature | Chrome | Firefox | Debug Tip |
|---------|--------|---------|-----------|
| Service Worker | `background.service_worker` | `background.scripts` + persistent | Check manifest output in `.addfox/` |
| Action API | `chrome.action` | `browser.browserAction` | Polyfill handles this |
| Scripting | `chrome.scripting.executeScript` | `browser.tabs.executeScript` | Polyfill unifies |
| Downloads | `chrome.downloads` | `browser.downloads` | Check permissions |
| Storage | `chrome.storage` | `browser.storage` | Same API |

### 4.3 Build Target Debugging

Build for specific target to isolate platform issues:

```bash
# Chrome build
addfox build -t chromium

# Firefox build
addfox build -t firefox

# Compare outputs
ls -la .addfox/extension/
cat .addfox/extension/manifest.json
```

---

## 5. Bundle analysis (Rsdoctor)

Enable Rsdoctor to analyze build output:

```bash
addfox build -r
# or
addfox dev -r
```

Report opens in browser at `.addfox/report/`.

### 5.1 Analyzing Bundle Size

| Metric | Healthy | Warning |
|--------|---------|---------|
| Total size | < 2MB | > 4MB |
| JS bundle | < 500KB per entry | > 1MB |
| Dependencies | Deduplicated | Multiple copies |

### 5.2 Common Bundle Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Large vendor chunk | Heavy dependencies | Use dynamic imports, tree-shaking |
| Duplicate React/Vue | Multiple versions | `pnpm ls react`, dedupe in lockfile |
| Unused code | Poor tree-shaking | Use named imports, check sideEffects |

---

## 6. Error.md deep dive

When `.addfox/error.md` exists, extract structured fields:

```markdown
## Build Error
- **entry**: options/index.tsx
- **error**: Module not found
- **file**: ./components/Settings.tsx
- **line**: 23
- **column**: 8

## Stack Trace
Error: Cannot find module './components/Settings'
  at webpackMissingModule (...)
  at Object../options/index.tsx (...)
```

**Action based on fields:**
- `entry` + `file` → Check import paths relative to entry
- `line` + `column` → Check syntax at that location
- Module not found → Install missing dependency or fix path

---

## 7. Debugging Checklist

### Build Issues
- [ ] Terminal shows first error clearly
- [ ] `.addfox/error.md` contains structured info
- [ ] `addfox.config.ts` is syntactically valid
- [ ] All `entry` paths exist
- [ ] Dependencies installed (`pnpm install`)

### Runtime Issues
- [ ] Extension loaded in `chrome://extensions/` or `about:debugging`
- [ ] Correct manifest version (3)
- [ ] Content script matches URL pattern
- [ ] Permissions granted (check `chrome://extensions/` details)
- [ ] **Using `webextension-polyfill` for cross-browser compatibility**

### Content UI Issues
- [ ] `target` selector matches existing element
- [ ] Mount called after DOM ready
- [ ] Styles imported in content entry
- [ ] Z-index high enough
- [ ] No CSP blocking

### Messaging Issues
- [ ] `from` field included in messages
- [ ] Listener returns `true` for async responses
- [ ] `tabId` is valid for `tabs.sendMessage`
- [ ] Content script injected on target tab

### Performance Issues
- [ ] Run `addfox build -r` for Rsdoctor analysis
- [ ] Check bundle sizes
- [ ] Verify no duplicate dependencies
- [ ] Test with `-t firefox` for cross-browser compatibility

---

## Additional resources

- Build reference: [addfox-best-practices/reference.md](../addfox-best-practices/reference.md)
- Testing: [addfox-testing skill](../addfox-testing/SKILL.md)
- WebExtension API: [MDN Extension API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API)
- Chrome Extension Debugging: [Chrome DevTools](https://developer.chrome.com/docs/extensions/mv3/tut_debugging/)
