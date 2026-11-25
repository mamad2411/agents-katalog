---
name: cloak-bridge
description: Use when a user-driven CloakBrowser profile needs MV3 Chrome writes/events through the native messaging bridge.
---

# CloakBrowser bridge

Opt-in, zero-TCP extension channel. Load `bridge/extension` as an MV3 unpacked
extension; install the native host with the exact 32-character extension ID. The
host manifest needs an absolute executable path and exactly one
`chrome-extension://<id>/` allowed origin. **STDOUT IS PROTOCOL-ONLY; DIAGNOSTICS
GO TO STDERR.**

```js
import { createBridgeClient, createChromeApi } from "omowright";
const bridge = createBridgeClient({ extensionId, stdin, stdout });
const chrome = createChromeApi(connection, { profilePath, bridge });
```

Launch the pinned binary
`~/.cloakbrowser/chromium-145.0.7632.109.2/Chromium.app/Contents/MacOS/Chromium`
with `--load-extension=/absolute/path/to/bridge/extension` and optionally exactly
one `--silent-debugger-extension-api` — it only suppresses the warning; it is not
authorization.

## Support matrix

| API                                            | Bridge behavior                                      |
| ---------------------------------------------- | ---------------------------------------------------- |
| bookmarks.create/move/remove                   | Supported only when negotiated                       |
| history.deleteUrl/deleteRange                  | Supported only when negotiated                       |
| tabGroups.update                               | Supported only when negotiated                       |
| debugger.attach/detach                         | Supported only when negotiated, numeric tab IDs only |
| notifications, tabGroups, tabs, windows events | Forwarded without replay                             |
| bookmarks.update/removeTree                    | Unsupported                                          |
| history.addUrl                                 | Unsupported                                          |
| downloads.pause/resume/cancel/erase            | Unsupported                                          |
| standalone reads and downloads.download        | Existing CDP/profile behavior                        |

**NEVER RETRY A MUTATION AFTER DISCONNECT — COMPLETION IS INDETERMINATE.**
Subscribe to events before triggering actions. CloakBrowser native-host
registration requires a verified `nativeMessagingHostDir`; the product directory
**CANNOT** be guessed from `--user-data-dir` or the application filename.
