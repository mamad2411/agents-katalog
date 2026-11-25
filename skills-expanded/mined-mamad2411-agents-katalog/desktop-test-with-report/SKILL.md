---
name: desktop-test-with-report
description: Drive computer-use desktop automation (screenshot + click + type) to exercise the features a pull request changes in a native desktop app, then post an evidence-only findings report back to the PR. Sibling of agent-test-with-report — use THAT one for browser and Electron apps (they expose CDP, so agent-browser drives them); use THIS one for native, non-Chromium apps — Cocoa/SwiftUI/AppKit, Qt, Win32, and native-webview frameworks like Wails or Tauri on macOS (WKWebView), where agent-browser can't attach. Use when the user wants an agent to manually test a desktop-app PR on the real desktop and leave a report, with phrases like "agent-test this desktop app PR", "computer-use test the native app and comment on the PR", "run exploratory testing on the desktop build and post a report". macOS-local and interactive — not a CI gate. Collects evidence (operations, screenshots, findings, unverified scope); never a pass/fail verdict.
---

# Desktop Test with Report

This skill is the **native-desktop sibling** of `agent-test-with-report`. It turns a pull request into a structured, evidence-based manual test run, but drives the app through **computer-use** (desktop screenshot + mouse + keyboard) instead of a browser. Everything else — reading the PR to decide *what* to test, the fixed report format, and posting back to the PR — is shared with the browser sibling.

The report is **evidence, not a verdict**. It records what was done, what was seen, and what was *not* covered. Merge decisions stay with humans and CI; this skill never outputs "✅ Approved" or any pass/fail judgement.

## Which skill to use

- **Browser web app, or Electron app** (VS Code, Slack, Discord, Figma, Notion…) → use **`agent-test-with-report`**. These speak Chrome DevTools Protocol, so agent-browser drives them with reliable DOM/accessibility refs.
- **Native app with no CDP** — Cocoa/SwiftUI/AppKit, Qt, Win32, or a **native-webview** app (Wails/Tauri on **macOS** = WKWebView; Linux = WebKitGTK) → use **this skill**. agent-browser can't attach, so computer-use drives the real window by pixels.
- **Wails/Tauri whose change is frontend-only** → cheaper to point `agent-test-with-report` at the frontend **dev server** (a localhost URL) and skip this skill. Reach for computer-use only when the flow crosses into the native/Go side that the dev-server browser can't reach. On **Windows**, Wails/Tauri use WebView2 (Chromium/CDP), so `agent-test-with-report` via `agent-browser connect` may drive the real app there.

## Precondition: computer-use must be available

This skill drives the app through the **computer-use** tools (`mcp__computer-use__screenshot`, `left_click`, `type`, `key`, `open_application`, `request_access`, …). If they aren't available, **stop** and tell the user this skill needs the computer-use capability enabled.

computer-use runs on the **user's real desktop** — it is **local and interactive, not headless and not a CI gate**. Before driving any app, call `request_access` for that specific application and wait for approval. Mind the access tiers: native apps are granted **full** control; **terminals/IDEs are "click" tier** (clickable but not typable — use the Bash tool for shell input); **browsers are "read" tier** (you cannot click or type in them via computer-use — which is the other reason browser apps belong to the sibling skill).

For the mechanics of driving an app, dealing with focus/occlusion, and — crucially — turning a screenshot into an uploadable **file**, read **[references/computer-use.md](references/computer-use.md)** (provider-neutral). The points that bite are summarised inline at step 5, but the reference is the source of truth.

## Precondition (for inline screenshots): Screen Recording permission

Evidence screenshots must become **files** so they can be attached to the PR, and the computer-use `screenshot` tool does **not** give you a file path your shell/agent-browser can read — it only renders the image in chat. The file has to come from a native OS capture (`screencapture` on macOS), which **requires Screen Recording permission for the host app running your shell**. Without it, `screencapture` fails with *"could not create image from display"* and there is no way to attach native-window screenshots — the run then falls back to a **text-only** report.

This is a one-time human grant (System Settings → Privacy & Security → Screen Recording → enable the host app; it may need an app relaunch). If two similarly-named entries exist, grant the exact one that owns the shell process. Check this **before** driving the test, not at posting time.

## Precondition (optional): a GitHub-authenticated browser profile

Inline screenshots (step 8) are attached by an **agent-browser** session signed in to GitHub — the same mechanism as the sibling skill. computer-use can't drive a browser (read tier), so posting always goes through agent-browser (CDP Chrome, independent of computer-use) or the text-only `gh` fallback. Set up the persistent profile once:

```bash
agent-browser open https://github.com/login --headed --profile ~/.agent-browser/profiles/github
```

Log in by hand (credentials/2FA are the user's, never the skill's). Without it, the run still completes and falls back to the text-only post.

## Principles (do not bend these)

- **Evidence, not verdicts.** Report findings; never emit an approval or pass/fail call.
- **Capture and attach generously.** Screenshot every meaningful state, not just the end — and attach many of them to the comment, not one summary shot. **Anything that diverges from the expected behaviour gets its own screenshot, called out inline next to the finding** — surprises are the highest-value evidence, so never drop them. (Native captures cost a `screencapture` + crop each; that's fine — take them.)
- **Always declare the unverified scope.** "Not verified" is a required section.
- **Suggest missing test coverage; never commit test code.** Native apps are hard to test automatically — call out what no test guards, but don't add tests in this run.
- **Leave room for exploration.** After the scripted checks, spend a bounded exploration pass and report any "this feels off" observations.

## Workflow

### 1. Identify the PR and load its context

```bash
gh pr view --json number,title,body,labels,files
gh pr diff
```

From the description, extract the author's intent and "what to verify" notes — that's your charter. From the diff, identify which screens/flows the change touches.

### 2. Decide whether to run, and at what depth

- **Mechanical skip by diff path:** docs-only, CI/config-only, or test-code-only → skip with a one-line report.
- **Wrong-skill skip:** if the change is browser/Electron, or a Wails/Tauri frontend-only change reachable via a dev-server URL → stop and point the user at `agent-test-with-report`.
- **Otherwise choose depth:** *smoke* (the main path the diff touches) vs *full* (main path + edge cases + exploration). Bias toward smoke for small diffs.

### 3. Build, launch, and focus the target

Build/launch the desktop app **from this PR's branch** per the project's conventions (`CLAUDE.md` / `README.md` / the build script), or ask the user how to launch it. Bring it to the foreground with `open_application` and confirm with a `screenshot`. For reproducible shots, set a known window size/position if you can. Record the app name and build/commit in the report.

If you can't build or launch the app yourself, **stop and ask** — guessing wastes the run.

### 4. Derive the test points

Combine the PR's "what to verify" notes with the flows the diff touches into a short, explicit checklist. State it before acting.

### 5. Drive the app via computer-use

For each checklist item: `screenshot` to see the current state, act (`left_click` at the target, `type`/`key` for input), then **`screenshot` again** — never assume the result. **Save a file for every meaningful state**, captioned (e.g. `discover-default.png`, `filter-go.png`), not just one shot at the end — and whenever a result differs from what the test point expected, capture *that* state as its own labelled file to attach inline. Err toward too many.

**Capturing evidence as files is the part that bites — read [references/computer-use.md](references/computer-use.md).** The short version:

- The computer-use `screenshot` renders an image in chat but does **not** give you a file path you can upload. For an attachable file use a native capture: on macOS `screencapture -x out.png` (and `screencapture -x d1.png d2.png d3.png` writes one file **per display** — the app may be on a non-main display; pick the file by resolution).
- `screencapture` needs **Screen Recording permission** (see precondition) and does **no** app-filtering: it captures the *real* screen, so other windows — including the agent's own UI — show up. The computer-use `screenshot` looks clean only because it hides non-granted apps at the compositor level; the file capture won't.
- So make the target window **unobstructed** before capturing: maximize it, or ask the human to move the overlapping window, or capture the display and **crop** to the app region (`magick in.png -crop WxH+X+Y +repage out.png`). Save the clean PNGs and keep their paths for step 8.

Brittleness rules (pixel automation is far less stable than DOM refs):

- **Re-screenshot after every action.** Coordinates from an old screenshot go stale the moment anything moves or re-renders.
- **Focus bounces — re-focus before acting.** Notifications, terminals, and the agent's own window steal the foreground; computer-use actions **error when a non-granted app is frontmost**. Call `open_application <target>` immediately before a click, and prefer the batch form (it re-checks frontmost per action).
- **Window control may be blocked.** Reliably raising/resizing a native window via the OS automation bridge needs **Accessibility permission**, which is often not granted; don't assume `osascript`/System Events will work. Fall back to maximizing via the UI, or human help.
- **Redact** anything sensitive captured in a shot before it goes in the report (the real-screen capture may include other windows).

### 6. Exploration phase

A bounded pass touching the changed area freely — odd inputs, rapid clicks, empty/long values, window resize, app relaunch. Record anything that feels wrong, even if you can't tell whether it's a real bug, for human triage.

### 7. Note automated-test gaps

For each behaviour you verified by hand, ask whether an automated/UI test could guard it. List the gaps as suggestions. Do **not** write or commit tests now.

### 8. Compose and post the report

Fill the shared template below. If step 5 produced clean PNG **files**, posting works exactly like the sibling skill (upload them inline). If Screen Recording wasn't available and you have no files, skip straight to the text-only fallback and say so in the report's Evidence/Not-verified sections.

**Check GitHub auth first** (don't wait until posting): `agent-browser open https://github.com` then `agent-browser eval "document.querySelector('meta[name=user-login]')?.content || 'LOGGED_OUT'"`.

- **Signed in → post through agent-browser so screenshots render inline.** Follow the **posting recipe in `agent-test-with-report` SKILL.md (step 8)** — same selectors (`#new_comment_field`, `#fc-new_comment_field`), same upload-then-wait-for-`user-attachments`, and the **same submit guard**: pick the form-scoped `button[type=submit]` whose text is exactly `Comment`; never the first one (`Close with comment`), which closes the PR. Recover a stray close with `gh pr reopen <n>`.
- **Not signed in → don't drive a login** (2FA blocks you). Tell the user to run the `--headed --profile` login above, then fall back to the text-only post.

**Fallback — text-only via the bundled helper:**

```bash
scripts/post-report.sh <report.md> [pr]
```

Images can't be embedded this way — reference the saved screenshot paths and state in the report that they were **not** attached inline and why.

## Report template (posted to the PR)

Write the report — and any message you surface to the user — in the **agent's configured output language**; don't hard-code one. The English labels below are examples. The structure, the required "Not verified" section, and the no-verdict rule stay the same regardless of language.

```md
## 🖥️ Desktop agent test report

**App:** <app name + build/commit> · **Platform:** <e.g. macOS 15 / WKWebView> · **Depth:** smoke | full

### Summary of change
<1–3 lines: what this PR does, from the description + diff>

### Test points
<the checklist from step 4 — what you set out to verify>

### Operations performed
<ordered list of the desktop actions you took>

### Evidence (screenshots)
<A gallery — attach a shot for each meaningful state, not one summary. Caption each.>
**<caption 1>**
<image 1>
**<caption 2>**
<image 2>
<…as many as you took…>

### Findings
<observations from the scripted checks. Neutral, specific. No verdict. Where a
result diverged from the test point, say so AND attach its screenshot right here
(not only in the gallery) — surprises are the highest-value evidence.>

### Out-of-scope observations
<exploration-phase "this feels off" notes for human triage, each with its own screenshot where you can. "None" if nothing.>

### Missing automated-test coverage (suggestions)
<behaviours exercised by hand that no automated/UI test seems to guard. Suggestions only.>

### Not verified
<REQUIRED. What you could not or did not check, and why: flows you couldn't
launch, OS/window states untested, data you couldn't set up, areas left for
the human. Note pixel-automation blind spots here too.>

---
*Evidence for review — not a pass/fail verdict. Merge decision stays with the reviewer and CI.*
```

## Guardrails

- **Never emit a verdict.** Findings only.
- **Never leave "Not verified" empty.** Pixel automation has blind spots — name them.
- **Never commit test code or other changes** as part of this run.
- **Never run destructive or irreversible native actions** — deleting files, sending messages/emails, payments, account changes — unless the user explicitly confirms it's safe. Desktop apps touch the real machine; default to caution.
- **Never expose secrets** — redact tokens, credentials, and private data in screenshots and logs.
- **Don't fabricate evidence.** Only reference screenshots that exist; only claim actions you actually performed.
- **Don't drive a browser with computer-use** (read tier) — if the target turns out to be browser-based, switch to `agent-test-with-report`.

## When to stop and check in

Pause and ask the user when:

- You can't build, launch, or bring the app to the foreground.
- The change needs data, auth, or a flow you can't set up yourself.
- An action would be destructive or irreversible.
- Coordinates keep going stale (the window won't stay put), so the run can't proceed reliably.
- The diff's intent is unclear and the PR gives no review points.
