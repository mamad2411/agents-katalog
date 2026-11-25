---
name: vamp-ui-validation
description: Validate VAMP VS Code webviews and packaged VSIX installations with isolated profiles and deterministic UI evidence. Use for release UI checks, native file pickers and installed-extension regressions.
---

# VAMP UI validation

## Choose the test boundary

For copy, layout and message handling, render generated HTML with a mocked acquireVsCodeApi. Record outgoing messages without dispatching them to a real extension. Exercise loading, ready, busy, error and unsupported backend states at wide and narrow sizes.

For installed-extension bugs, build the VSIX and install it into an isolated user-data directory and extensions directory. Record extension ID, version and resolved installation path. A development host or source override is not evidence that the packaged extension works. Updating an isolated profile does not update the user's normal profile.

## Target the correct window

- Identify the isolated VS Code process and its exact webview frame before using locators. Prefer IDs, roles and labels over coordinates.
- Native file pickers are outside the webview. On Windows, locate the dialog by process and window handle, then locate its filename Edit and Open button through UI Automation. Validate the owning process before targeted window messages. Control IDs vary across dialogs; inspect them instead of assuming them.
- Bringing a browser page forward does not prove native focus. Avoid global SendKeys. Never type into an unverified foreground window.
- Use the matching backend skill for authorized guest input. Do not resume paused VM automation merely to validate UI changes.

## Check outcomes

Wait for settled UI state rather than fixed delays. For server buttons, check busy/disabled states and final Running/Stopped status; check HTTP health only when server lifecycle changes are authorized. Use an isolated fixture otherwise.

For creation flows, distinguish accepted request, VM creation, OS installation and completed guest setup. Verify recorder installation and session policy inside the guest only when that test is authorized. A manually invoked installer cannot prove automatic setup.

Return a compact record: artifact version/path, host/backend, action, expected state, observed state and evidence path. Mark unrun or incomplete stages explicitly. Keep credentials and development VM names out of release artifacts.
