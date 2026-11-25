---
name: install
description: Install or update the Chromaphore browser the plugin drives.
disable-model-invocation: true
---

# Install the Chromaphore browser

1. Call `browser_install` with `check_only: true`. It downloads nothing: it reports the installed release, if any, whether the plugin settings name a browser of their own, and the latest release on GitHub with its download size.

2. Then, by what it reported:
   - **The latest release is installed:** tell the user which release and where it is. Nothing needs downloading; stop here, apart from the permission tip below.
   - **The plugin settings name a browser:** tell the user `browser_open` uses that one, so an installed release is not needed, and ask whether they want one anyway.
   - **Nothing is installed:** before anything is downloaded, tell the user that the release comes from https://github.com/nodriver-project/Chromaphore-Browser/releases, the size the check reported (about 1.6 GB, most of it the font bundle that keeps the reported fonts consistent), that it is unpacked under `%LOCALAPPDATA%\Chromaphore\browser\`, checked against the SHA-256 GitHub publishes for it, and not registered with Windows (it does not become a default browser), and that profiles the browser tools create go under `%LOCALAPPDATA%\Chromaphore\profiles\`. Ask whether to go ahead.
   - **An older release is installed and GitHub has a newer one:** tell the user both releases and the download size, and that the old release's folder is removed afterwards (at a later start if a browser still runs from it) while profiles stay. Ask whether to upgrade.

3. If they agree, call `browser_install` without `check_only` and report its answer.

Finally, in one short paragraph (without looking at any settings file), tell them how to let the browser tools run without a prompt on every call: add this to `permissions.allow` in `~/.claude/settings.json` (all projects) or `.claude/settings.json` (this project). Running sessions pick it up without a restart.

```json
"mcp__plugin_chromaphore_browser__*"
```

If they have Chromaphore installed elsewhere already, they can skip the download: `/config`, then the Chromaphore plugin's "Browser" option, set to that `chrome.exe`.
