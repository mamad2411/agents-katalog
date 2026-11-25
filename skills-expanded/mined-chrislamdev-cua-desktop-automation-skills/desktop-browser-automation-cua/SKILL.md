---
name: desktop-browser-automation-cua
description: Use Cua Driver to automate desktop browsers (Chrome/Safari) — open pages, type text, click elements, execute JavaScript. Includes React/Draft.js workaround for X.com and similar SPA platforms.
tags:
  - cua browser
  - browser automation
  - desktop browser
  - x.com
  - twitter
  - react
  - controlled-component
triggers:
  - cua browser automation
  - desktop browser control
  - react form automation
  - x.com automation
  - twitter compose
---

# Desktop Browser Automation via Cua Driver

Use Cua Driver to control desktop browsers (Chrome, Safari, Edge) for web automation tasks like opening pages, filling forms, submitting queries, and extracting text.

## Prerequisites

- Cua Driver installed (`cua-driver --version`)
- Permissions granted: Accessibility + Screen Recording
- Daemon running: `cua-driver serve` or `open -n -g -a CuaDriver --args serve`

## Workflow

### 1. Launch browser to target URL
```bash
cua-driver call launch_app '{"bundle_id":"com.google.Chrome","urls":["https://example.com"]}'
```
Note the returned pid.

### 2. Find the window
```bash
cua-driver call list_windows '{"pid":<PID>}'
```
Find the target window_id (the one with matching title).

### 3. Handle any dialogs
Check for extra windows (restore dialogs, permission prompts). Close them via AXPress on the appropriate button element.

### 4. Enable JavaScript Apple Events (one-time setup for Chrome, requires restart)
```bash
echo '{"action":"enable_javascript_apple_events","bundle_id":"com.google.Chrome","user_has_confirmed_enabling":true}' | cua-driver call page
```
After this, Chrome restarts. Wait ~8s then find the new pid/window_id.

### 5. Use the `page` tool with execute_javascript

For SAFARI (no enable_javascript_apple_events needed — works out of box):
```bash
cua-driver call page '{"pid":<PID>,"window_id":<WID>,"action":"execute_javascript","javascript":"document.title + \" | \" + window.location.href"}'
```

⚠️ **For long JavaScript** (over ~100 chars), shell quoting breaks. Use file-based JSON payload:
```bash
# Write JS to file
cat > /tmp/script.js << 'JSEOF'
(function(){
  // your JS code here
  return "result";
})()
JSEOF

# Pipe via file-based approach
cat /tmp/script.js | python3 -c "
import sys, json
js = sys.stdin.read()
payload = json.dumps({'pid': <PID>, 'window_id': <WID>, 'action': 'execute_javascript', 'javascript': js})
with open('/tmp/payload.json', 'w') as f:
    f.write(payload)
" && cat /tmp/payload.json | cua-driver call page
```

### 6. Common JavaScript operations

**Type into standard <textarea> or <input>:**
```javascript
(function(){
 let el = document.querySelector("textarea, input");
 if(!el) return "not found";
 el.value = "YOUR TEXT";
 el.dispatchEvent(new Event("input",{bubbles:true}));
 el.dispatchEvent(new Event("change",{bubbles:true}));
 return "done";
})()
```

**Type into contenteditable (simple):**
```javascript
(function(){
 let el = document.querySelector("[contenteditable]");
 if(!el) return "not found";
 const sel = window.getSelection();
 const range = document.createRange();
 range.selectNodeContents(el);
 sel.removeAllRanges();
 sel.addRange(range);
 document.execCommand('insertText', false, 'YOUR TEXT');
 return "done";
})()
```

## ⚠️ CRITICAL: React / Primer / Draft.js / Controlled Components

**Three major controlled-component patterns exist:**

| Pattern | Where | Working approach |
|---------|-------|-----------------|
| **Draft.js** (X.com) | Custom contenteditable — React state managed via Draft.js editor | CGEvent `type_text` only |
| **React Primer** (GitHub new forms: repo create, settings, tokens) | Standard `<input>` but Primer's React wrappers reject `nativeSetter + dispatchEvent` | `execCommand('insertText')` after `focus()` + `click()` |
| **ProseMirror** (Medium editor) | Custom editor with its own state tree | `textContent` + `dispatchEvent(new Event('input'))` |

### ✅ Working approach for GitHub Primer React components (new finding):

GitHub's Primer component library uses `<input>` elements that:
- ❌ Reject `el.value = 'text'` (silent overwrite but React state doesn't sync)
- ❌ Reject `nativeSetter + dispatchEvent('input')` (React rejects programmatic dispatch)
- ✅ ACCEPT `el.focus(); el.click(); document.execCommand('insertText', false, 'text')`

```javascript
// Fill Primer React <input> in GitHub forms:
(function(){
  var el = document.querySelector('#repository-name-input'); // or other selector
  el.focus();
  el.click();
  document.execCommand('insertText', false, 'desired-value');
  return 'val: [' + el.value + ']';
})()
```

**Tips for Primer forms:**
- Always use `querySelector` with ID selectors (e.g. `#repository-name-input`, `#_r_d_`)
- For `<select>` or checkbox, use native DOM click
- GitHub 2FA sudo mode: navigating to settings pages from a **new Safari instance** triggers sudo mode requiring re-auth. Prefer reusing an existing Safari session that's already authenticated.

### ⚠️ Draft.js (X.com) — CGEvent approach:

**Do NOT use JavaScript to fill the field. Instead:**

1. **Use Cua Driver pixel click** to focus the textarea (find coordinates via screenshot):
```bash
screencapture -x /tmp/screen.png
# Use vision_analyze to find the textarea coordinates
cua-driver call click '{"pid":<PID>,"window_id":<WID>,"x":<X>,"y":<Y>}'
```

2. **Use Cua Driver `type_text`** (CGEvent key synthesis) to type character-by-character:
```bash
cua-driver call type_text '{"pid":<PID>,"text":"Your tweet content here","delay_ms":10}'
```
`type_text` sends real keyboard events that React/Draft.js properly captures.

3. **Click the Post/Submit button** via pixel coordinates:
```bash
cua-driver call click '{"pid":<PID>,"window_id":<WID>,"x":<X>,"y":<Y>}'
```

### Why this works:
- CGEvent keyboard events (via `type_text`) are indistinguishable from real keyboard input
- React/Draft.js listens for native keyboard events, not JavaScript property changes
- `delay_ms: 10` adds a small per-character delay for reliable event processing

### Pixel coordinate tips for X.com:
- **Tweet compose textarea (homepage):** ~(285, 225) in a 1600x796 Safari window
- **Post button (in compose box):** ~(610, 420)
- **Left sidebar Post button (new tweet):** ~(175, 730)
- Coordinates vary by window size — always verify via screenshot + vision_analyze

## X API Pay-Per-Use Note

X's new Developer Console (console.x.com) uses pay-per-use credits:
- **Free tier no longer exists** — must buy credits ($5 minimum)
- Post write cost: ~$0.05 per tweet
- API returns `402 credits depleted` if balance is $0.00
- OAuth 1.0a user context: Consumer Key + Secret + Access Token + Secret (generated in console.x.com app settings → Keys & Tokens tab)
- Alternative: use Cua Driver browser automation (above) to post without API cost

## Pitfalls

1. **Chrome may show "Restore pages?" dialog** — Close it via AXPress on element_index (use `get_window_state` to find the button).
2. **JSON quoting in shell** — Always pipe JSON via stdin for complex payloads. For long JS, use file-based payload (Step 5).
3. **Gemini/Web apps** — Use JavaScript execution via `page` tool rather than AX `type_text` for web apps that use custom input components.
4. **Browser restart after enable_javascript_apple_events** — Gets a new pid. Always re-discover pid/window_id after enabling.
5. **Large AX trees** — Use `query` parameter to filter `get_window_state` output.
6. **Safari `page` tool works without JavaScript Apple Events** — Safari's WebKit inspector is enabled by default.
7. **`click_element` not implemented for Safari** — Use `execute_javascript` with `el.click()` instead, or use pixel click for complex SPAs.
8. **Safari zoom/screenshot may fail** — `screencapture failed` for certain windows. Fall back to `page.execute_javascript` to read DOM state instead.
9. **Safari AX tree is massive (1000+ nodes)** — Queries like "Repository name" will not match Primer form fields because they're inside web content regions, not native AX elements. Always use `page.execute_javascript` for filling web forms, not AX.
10. **Cua Driver `type_text` (CGEvent) targets the frontmost focused element** — If the Safari tab isn't focused, keystrokes go to the wrong place. Use `page.execute_javascript` with `execCommand('insertText')` as the more reliable approach for text input.
11. **GitHub 2FA sudo mode blocks settings access** — Navigating to sensitive pages (`/settings/tokens`, `/settings/tokens/new`) from a freshly launched Safari instance triggers GitHub's sudo mode requiring 2FA. Fix: (a) reuse an existing long-running Safari session, (b) ask user to relay 2FA code, or (c) use a stored PAT from credential file instead.
12. **Repo creation via Safari + Primer forms works end-to-end** — Steps: navigate to `github.com/new` → fill name via `execCommand('insertText')` → fill description → find "Create repository" button via `querySelectorAll('button')` and match text → `el.click()` → verify redirect to `github.com/{owner}/{repo}`.
8. **Safari zoom/screenshot may fail** — `screencapture failed` for certain windows. Fall back to `page.execute_javascript` to read DOM state instead.
9. **Safari AX tree is massive (1000+ nodes)** — Queries like "Repository name" will not match Primer form fields because they're inside web content regions, not native AX elements. Always use `page.execute_javascript` for filling web forms, not AX.
10. **Cua Driver `type_text` (CGEvent) targets the frontmost focused element** — If the Safari tab isn't focused, keystrokes go to the wrong place. Use `page.execute_javascript` with `execCommand('insertText')` as the more reliable approach for text input.
