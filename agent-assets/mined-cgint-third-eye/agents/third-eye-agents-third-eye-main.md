# AGENTS.md (repo-local)

## Screenshot evidence (UI changes)

When producing screenshots as evidence for UI changes:

- Prefer **absolute output paths** for screenshots (e.g. `/Users/cgint/dev/third-eye/.../screenshots/foo.png`).
  - Reason: tools like `agent-browser` can run via a daemon/session where relative paths may resolve unexpectedly, causing screenshots to be saved somewhere else.
- Alternatively use `browsershot.sh <url> <output.png>` which is reliable for path handling.
- **Always load and visually inspect** the saved screenshot(s) after creation (using the `read` tool).
  - First check: the file actually exists at the expected location.
  - Second check: the screenshot contains the **specific UI detail** you intended to verify.

If you cannot clearly see the relevant detail in the screenshot, do **not** accept it as “good enough”.
Instead, iterate until the evidence is readable:
- Increase viewport size (e.g. 1440x900 or larger).
- Use full-page capture where applicable (`browsershot.sh --full ...` or `agent-browser screenshot --full`).
- Take a second screenshot after scrolling to the relevant area.
- Re-open the resulting image and confirm the target detail is visible.

Recommended:
- Store screenshots under the relevant OpenSpec change directory, e.g.
  `openspec/changes/<change>/screenshots/`
