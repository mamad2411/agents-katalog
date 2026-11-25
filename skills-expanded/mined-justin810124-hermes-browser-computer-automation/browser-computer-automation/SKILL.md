---
name: browser-computer-automation
description: "Use when the user asks Hermes to operate Chrome or the Mac UI for logged-in websites, form filling, seller portals, uploads, web dashboards, browser tasks, or desktop workflows. Teaches Hermes to combine browser tools, computer_use, CuaDriver, file helpers, and vision without attempting to bypass CAPTCHA or anti-bot checks."
version: 1.3.0
author: Justin + Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [chrome, browser, browser-use, computer-use, cuadriver, macos, form-filling, uploads, automation, gui]
    category: productivity
    related_skills: [macos-computer-use, dogfood, hermes-agent]
---

# Browser + Computer Automation

## Mission

When the user asks you to operate Chrome, fill forms, upload files, edit seller portals, or continue from an already-open logged-in page, act like a careful desktop co-pilot.

You do not magically bypass anti-bot systems. You use the safest available control surface:

1. Use APIs/connectors if they exist.
2. Use Browser Use when a mature web-agent loop is available and the task is an ordinary web workflow.
3. Use Hermes browser tools for small ordinary pages or when Browser Use is unavailable.
4. Use `computer_use` or CuaDriver for the user's current real Chrome session, native file pickers, visual UI, live desktop state, and handoffs.
5. Stop at CAPTCHA, PerimeterX, 2FA, identity verification, tax forms, payment, publish, or legal attestation gates and ask the user to complete or confirm them.

## Execution Contract

Before touching a browser, run the operator when this repo is available:

```bash
scripts/hermes_operator.py --task "<user task>"
```

Use its `Control surface`, `Next command`, `Handoff`, and `Warnings` as the execution plan.

If this repo is not available, output a short control-surface decision manually:

```text
Control surface: <API | Browser Use | Browser Use real Chrome | Hermes browser | computer_use/CuaDriver | stop>
Reason: <one sentence>
Stop gates: CAPTCHA, PerimeterX, 2FA, identity, tax, payment, publish, legal attestation
```

Then execute with that surface. If the first surface fails for a structural reason, re-state the new surface before switching.

This contract exists because Hermes may otherwise keep using simple browser automation when real Chrome, Browser Use, or a human handoff would be better.

## Tool Reality

Codex-only tools cannot be copied into Hermes. The equivalent Hermes capabilities are:

| Codex behavior | Hermes equivalent |
|---|---|
| Operate current real Chrome tab | `computer_use` targeting `app="Google Chrome"` |
| Click/type/scroll native Mac UI | `computer_use` or CuaDriver MCP/CLI |
| Mature autonomous web task loop | Browser Use runner in this repo |
| Use a clean automation browser | `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_vision` |
| Inspect/upload local files | `terminal` + `file` tools |
| Judge screenshots/images | `vision` or `browser_vision` |
| Create temporary upload copies | `terminal` or `file` |

The skill's job is to make you choose and sequence those tools correctly.

## Required Toolsets

Before attempting real Chrome automation, verify:

```bash
hermes tools list | rg 'browser|computer_use|vision|terminal|file|skills'
```

Required:

- `browser` enabled
- `computer_use` enabled
- `vision` enabled
- `terminal` enabled
- `file` enabled
- `skills` enabled

Optional but recommended:

- Browser Use integration installed with `bash scripts/install_browser_use.sh`

If `computer_use` is missing from the current session, tell the user to enable it and reset/restart the Hermes session:

```bash
hermes tools enable computer_use
```

Then start a fresh Hermes chat/session or use the UI reset command so the new tool list is loaded.

## Required macOS Permissions

If `computer_use` is present but cannot see/click/type reliably, diagnose CuaDriver:

```bash
/Applications/CuaDriver.app/Contents/MacOS/cua-driver doctor
```

If Accessibility or Screen Recording is denied, stop. Tell the user:

1. Open System Settings -> Privacy & Security.
2. Grant Accessibility to `CuaDriver.app`.
3. Grant Screen Recording to `CuaDriver.app`.
4. Restart CuaDriver:

```bash
open -n -g -a CuaDriver --args serve
```

Do not keep trying to click blind when permissions are denied.

## Optional: Add CuaDriver MCP

Hermes has an internal `computer_use` toolset. For lower-level GUI control, CuaDriver can also be registered as an MCP server:

```bash
hermes mcp add cua-driver --command /Applications/CuaDriver.app/Contents/MacOS/cua-driver --args mcp
hermes mcp list
```

After adding an MCP server, start a new Hermes session so tools are rediscovered. Use this only as an extra control surface; the built-in `computer_use` tool remains the default when available.

## Decision Tree

Use this exact decision tree:

```text
Does the task involve CAPTCHA, PerimeterX, reCAPTCHA, Cloudflare Turnstile, 2FA, identity, tax, payment, or publish?
├── Yes -> stop at the gate. Ask the user to complete/confirm. Continue only after user says done.
└── No
    Is there a purpose-built API/connector?
    ├── Yes -> use that API/connector.
    └── No
        Is it an ordinary web workflow that Browser Use can handle?
        ├── Yes -> use scripts/run_browser_use_task.py.
        └── No
            Does it need existing Chrome login/session/extensions?
            ├── Yes -> use Browser Use real Chrome if no native UI handoff is needed; otherwise computer_use/CuaDriver.
            └── No
                Is it a small normal page that Hermes browser tools can open?
                ├── Yes -> use browser_* tools.
                └── No -> use computer_use/CuaDriver.
```

For Fiverr and similar seller portals, prefer real Chrome through `computer_use` when the current user session, PerimeterX, native upload UI, or handoff matters.

## Browser Use Workflow

Use Browser Use for ordinary web tasks when installed. First check:

```bash
bash scripts/doctor.sh
```

Ask the operator for the route:

```bash
scripts/hermes_operator.py --task "<task>"
```

Dry-run the final task prompt when unsure:

```bash
.venv-browser-use/bin/python scripts/run_browser_use_task.py --dry-run --task "<task>"
```

Run an ordinary web task:

```bash
.venv-browser-use/bin/python scripts/run_browser_use_task.py --task "<task>"
```

Run with existing Chrome profile when the task needs login state but not native UI handoff:

```bash
.venv-browser-use/bin/python scripts/run_browser_use_task.py --real-chrome --profile "Default" --task "<task>"
```

Rules:

- Do not use Browser Use to bypass verification gates.
- Do not inspect cookies, local storage, passwords, payment data, identity documents, or tokens.
- If Browser Use reaches CAPTCHA/PerimeterX/2FA/identity/tax/payment/publish, stop and switch to user handoff.
- If Browser Use needs a native macOS file picker or the user's current visible Chrome tab, switch to `computer_use`/CuaDriver.

## Anti-Bot And Human Verification

Never claim you can bypass PerimeterX, CAPTCHA, reCAPTCHA, Cloudflare, 2FA, or device verification.

Correct behavior:

- If a challenge appears, stop.
- Tell the user exactly what is blocking progress.
- Ask the user to solve the challenge manually in Chrome.
- After the user says it is done, re-capture and continue.

Do not:

- Try repeated automated challenge attempts.
- Use "press and hold" CAPTCHA automation.
- Search for bypass tricks.
- Use stealth claims.
- Move cookies or tokens around to evade detection.

For Fiverr specifically:

- Browser automation may show PerimeterX errors.
- Real Chrome with existing login is the right surface.
- If PerimeterX still appears in real Chrome, the user must solve it manually.
- Prepare all text/content while waiting so the user is not blocked on writing.

## Real Chrome Workflow

Use this pattern when controlling the user's Chrome:

```text
computer_use(action="capture", mode="som", app="Google Chrome")
```

Read:

- window title
- active URL
- visible step
- required fields
- validation messages
- upload progress
- buttons that look irreversible

Then act one step at a time:

```text
computer_use(action="click", element=<index>, capture_after=True)
computer_use(action="type", text="...")
computer_use(action="key", keys="tab", capture_after=True)
computer_use(action="scroll", direction="down", amount=3, element=<scrollable_index>, capture_after=True)
```

Rules:

- Capture before every action group.
- Element indices are valid only for the most recent capture.
- Re-capture after navigation, save, upload, modal open/close, or user intervention.
- Prefer element indices. Use coordinates only for custom web controls that do not expose accessible elements.
- If the user changes Chrome while you are working, re-capture before doing anything else.
- Do not switch tabs blindly. If several tabs have similar titles, identify the correct one by URL/title.

## Browser Tool Workflow

Use this when not relying on the user's real Chrome session:

```text
browser_navigate(url="https://example.com")
browser_snapshot()
browser_vision(question="Describe visible page state and annotate controls.", annotate=true)
browser_click(ref="@e12")
browser_type(ref="@e7", text="...")
browser_press(key="Enter")
browser_console()
```

Rules:

- Use `browser_snapshot` for DOM/accessibility structure.
- Use `browser_vision(annotate=true)` when layout matters.
- Use refs like `@e12`; avoid coordinates.
- Check console after significant interactions for web app bugs.
- If blocked by PerimeterX or CAPTCHA, stop and switch to user-assisted real Chrome flow.

## Form Filling Playbook

1. Read the whole current section before typing.
2. Fill only fields requested by the user or supported by truthful facts.
3. Use exact user-provided text when supplied.
4. If asked to improve wording, make it concise, professional, SEO-aware, and truthful.
5. Respect character counters.
6. Fill and save one section at a time.
7. Verify saved state or next step.
8. Do not invent legal identity, certifications, tax status, work history, or company facts.

For long text fields:

- Prefer direct set-value style tools if available.
- Otherwise click the field, select existing text with `cmd+a`, then type/paste.
- Verify the field content after typing.

For custom fields:

- If AX tree exposes no input, use screenshot/vision to find the target.
- Click carefully by coordinate only after confirming the field visually.
- Re-capture and verify text landed in the right place.

## Upload Playbook

Before upload:

```bash
find "$HOME/Downloads" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.pdf' \)
sips -g pixelWidth -g pixelHeight /path/to/image.png
```

For image selection:

- Prefer clear subject, strong composition, commercial appeal.
- Reject fake tiny text, watermarks, obvious AI artifacts, broken anatomy, poor crops, or low resolution.
- For a gallery, choose variety: one hero image, one portrait/detail image, one scene/product/environment image.

For file picker reliability:

1. Copy chosen files into the current working directory with clear names.
2. Open the file picker.
3. Multi-select if possible; otherwise upload one file at a time.
4. Wait for progress circles/spinners to disappear.
5. Confirm previews rendered.

Example:

```bash
cp "/source/best-dragon.png" "$PWD/upload-01-hero.png"
cp "/source/best-portrait.png" "$PWD/upload-02-portrait.png"
cp "/source/best-city.png" "$PWD/upload-03-environment.png"
```

## Save, Preview, Publish Boundaries

Safe to do without asking again when it is clearly part of the task:

- Save draft
- Save and continue to next setup step
- Upload user-owned files
- Fill non-sensitive profile/gig fields

Ask before:

- Publish
- Submit final application
- Submit identity verification
- Submit W-9/W-8/tax declarations
- Verify phone/email
- Pay/buy/subscribe
- Delete/remove irreversible content
- Accept legal terms beyond routine content ownership checkbox

If the user has already said "confirm" for the exact action, proceed once, then report.

## PerimeterX/Fiverr Specific Pattern

For Fiverr tasks:

1. Use the user's real Chrome, not `browser_navigate`.
2. Capture the current Chrome page.
3. If the page is a PerimeterX challenge, stop and ask the user to solve it.
4. Once solved, continue section by section.
5. Save frequently.
6. Stop at W-9, identity verification, phone verification, or Publish.

Typical final report:

```text
Completed: overview, pricing, description/FAQ, requirements, gallery uploads.
Stopped at: Publish page.
Remaining: Form W-9, identity verification, phone verification, then user can publish.
```

## Recovery

- **No computer_use tool:** enable toolset and restart/reset Hermes session.
- **CuaDriver permission denied:** run doctor and ask user to grant Accessibility/Screen Recording.
- **Stale element index:** re-capture.
- **Click no effect:** re-capture; look for modal, overlay, validation, disabled button.
- **Typing went wrong field:** stop, undo if safe, re-capture, target field again.
- **File picker wrong folder:** use Finder/file picker sidebar or path navigation; if shortcuts steal focus, ask user to choose files or use copied files in visible folder.
- **Browser blocked by anti-bot:** stop; ask user to solve in real Chrome.
- **Save failed:** read visible validation messages and fix only those fields.

## Final Response Standard

At the end, report:

- what was completed
- what files were uploaded or changed
- what page/status is currently visible
- what still requires the user
- whether anything sensitive was not touched

Do not over-explain tool internals unless the user asks.

## Verification Checklist

- [ ] Correct tool surface selected: API, browser, or real Chrome.
- [ ] Chrome/page state captured before acting.
- [ ] Required fields filled with truthful/user-approved content.
- [ ] Uploaded files inspected and previews rendered.
- [ ] Save/continue succeeded.
- [ ] CAPTCHA/PerimeterX/2FA/identity/tax/payment/publish gates were not bypassed.
- [ ] Final response clearly states remaining user-owned steps.
