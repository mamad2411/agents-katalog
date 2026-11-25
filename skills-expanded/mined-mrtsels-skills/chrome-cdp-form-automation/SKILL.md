---
name: chrome-cdp-form-automation
description: 用CDP自动化用户真实Chrome填表/上传文件时使用，含Chrome 151+调试启动与uploadifive上传。
metadata:
  imported_from: hermes
---

# Real-Chrome CDP Form Automation

Drive the user's actual Chrome (not Hermes cloud browser) through
chrome-devtools-mcp (mcporter) or raw WebSocket CDP. Covers launching Chrome
with remote debugging on modern versions, connecting, filling forms, and
uploading files through JS upload plugins that plain `DOM.setFileInputFiles`
on the visible input won't satisfy.

## Chrome 151+ launch: non-default user-data-dir is MANDATORY

Chrome 151 refuses remote debugging on the default profile:
`DevTools remote debugging requires a non-default data directory.`
Symptom: process runs with `--remote-debugging-port=9222` but nothing listens
on the port and no `DevToolsActivePort` is created.

**Fix — copy the profile once, reuse it:**

```bash
# 1. quit Chrome (AppleScript preserves tabs)
osascript -e 'tell application "Google Chrome" to quit'
# 2. copy profile (keeps extensions incl. Auto 2FA + login state)
ditto "$HOME/Library/Application Support/Google/Chrome" \
      "$HOME/Library/Application Support/Google/Chrome-Debug"
rm -f "$HOME/Library/Application Support/Google/Chrome-Debug"/{Singleton*,DevToolsActivePort}
# 3. launch (background; zsh: quote the * arg)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  '--remote-allow-origins=*' \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome-Debug"
```

**mcporter only reads the DEFAULT path's DevToolsActivePort.** The Chrome-Debug
instance may never write one — reconstruct it manually (uuid from
`curl http://127.0.0.1:9222/json/version` → webSocketDebuggerUrl):

```bash
printf '9222\n/devtools/browser/<UUID>\n' > \
  "$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"
```

Note: second line is the **path**, not the full `ws://` URL.

## Connecting

- `mcporter list` → chrome-devtools must be registered (29 tools).
- `mcporter call chrome-devtools.list_pages`, `select_page pageId=N`,
  `take_snapshot`, `click uid=...`, `fill uid=... value="..."`,
  `evaluate_script --args '{"function": "function(){...}"}'`.
- Raw WebSocket (python `websocket-client`) to a page target: requires
  `--remote-allow-origins=*` at launch, else handshake 403
  ("Rejected an incoming WebSocket connection from the http://127.0.0.1:9222
  origin"). In zsh, quote the arg: `'--remote-allow-origins=*'`.

## Filling forms

- PeopleSoft/NUI pages: text in `input`/`textarea`, courses in `a.ps-link`,
  grid content in `div.ps_box-scrollarea`. Use `evaluate_script` +
  `document.body.innerText` for bulk extraction (parse in Python, don't grep
  snapshots).
- Verify before submit: snapshot and re-read field values (some forms validate
  on submit and highlight errors — check for "There was a problem with your
  submission" and re-read the flagged fields).

## File upload through JS plugins (uploadifive etc.)

Two inputs exist: the **hidden submit field** (`#element_12`) and the
**transparent overlay input** (`#uploadifive_upload_element_12`) that captures
clicks/changes. Setting files on the hidden field does NOT register with the
plugin → submit fails with "This field is required. Please upload a file."

Correct sequence — set the file on the **overlay** input, then dispatch change:

```python
# via WebSocket CDP (needs --remote-allow-origins=*)
r = send("Runtime.evaluate", {"expression": "document.getElementById('uploadifive_upload_element_12')", "returnByValue": False})
obj_id = r["result"]["result"]["objectId"]
send("DOM.setFileInputFiles", {"files": [file_path], "objectId": obj_id})
send("Runtime.evaluate", {"expression": "document.getElementById('uploadifive_upload_element_12').dispatchEvent(new Event('change', {bubbles: true}))"})
```

Then the plugin POSTs to `upload.php` (async). Wait several seconds; the queue
UI must show the filename before Continue/Submit passes validation.

**If the upload POST aborts (`net::ERR_ABORTED` in the network log):** click the
queue item's X (delete), re-set the file, re-dispatch change, wait again. The
failed item must be removed first or validation stays red.

See `references/uploadifive-file-upload.md` for the full worked example and
`scripts/set_file_input.py` for a reusable helper.

## Pitfalls

- **Never use Hermes browser tools for this** — cloud browser, no user login
  state. Real session only, single instance (PeopleSoft/CUSIS lock on second
  login of same account).
- zsh expands `*` in unquoted args — always quote `--remote-allow-origins=*`.
- `evaluate_script` results come back as JSON strings — strip the ```json fence
  before `json.loads`, or parse with Python.
- After killing/restarting Chrome, page ids change → `list_pages` again.
- Don't kill user Chrome with `killall` — AppleScript quit preserves tabs.

## References

- `references/uploadifive-file-upload.md` — full ELITE webform worked example,
  error transcripts, verification steps.
- `scripts/set_file_input.py` — reusable CDP file-input setter (takes page WS
  URL, input id, file path).
