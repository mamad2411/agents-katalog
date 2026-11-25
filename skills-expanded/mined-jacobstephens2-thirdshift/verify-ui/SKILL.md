---
name: verify-ui
description: "Verify rendered HTML, CSS, templates, frontend routes or interactive UI state, and capture pull-request Visual evidence. Use before UI edits and again when verifying them."
---

# Verify UI

Use shell/CLI browser tools; no MCP configuration is needed. Invoke this before editing UI code and again before opening or updating a pull request; local verification alone never authorizes a push or upload.

## Discover and boot

Find the target repository's `.agents/skills/verify-*/SKILL.md` and `.claude/skills/verify-*/SKILL.md` (especially `verify-ui`). Follow the relevant project skill's boot, seed and flow instructions; otherwise read the `UI verification` section in `AGENTS.md`, then repository test/dev-server documentation. Use committed fixtures and idempotent seed scripts. Record newly discovered setup traps in the project-local `verify-*` skill's `Gotchas` as part of the PR when useful.

Optional host-only faux/sandbox test credentials live at `~/.config/thirdshift/verify-env/<owner>/<repo>.env`, with owner/repo determined from this repository's origin. Load that file only when the documented setup needs it, inside the verification subshell (`set -a; . "$verify_env"; set +a`, without shell tracing). Keep it outside git, redact credentials from output and captures, and use faux data on screen. Never copy untracked `.env` files from the Launch directory.

Each browser command owns its entire lifetime inside one `( ... )` subshell with a `trap ... EXIT`: create isolated app/database/profile state with `mktemp -d`, bind the target application to loopback on an OS-assigned ephemeral port (`0`), and read the actual port from its readiness output. Wait for readiness with a bounded poll. Avoid a probe-then-rebind free-port race. If the app cannot bind `0`, use the repository's documented equivalent that keeps the port reserved until startup.

Register cleanup before starting the application or browser daemon. Track their exact child PIDs/job handles; stop and wait for both on success, assertion failure and interruption. For a server wrapper that forks, own and terminate its process group or use the repository's supervisor to reap every descendant. Close Playwright contexts and browser in `finally`; stop any CLI browser daemon explicitly too. Remove temporary scripts/state on exit, but keep proof captures outside that state at their original `mktemp` paths. No server or browser child process may outlive the command.

## Phase 1 — Interactive exploration

Before editing UI code, boot the unpatched checkout and drive the affected flows using an installed browser CLI or short Playwright scripts. Inspect accessibility snapshots (`locator.ariaSnapshot()` or the CLI's snapshot), rendered state, browser console errors, `pageerror`, failed requests and failed network responses. Exercise the relevant edge cases, navigation and keyboard behavior. Fix broken UI behavior in-session, rerunning the affected flow until it works. Keep the exact reproduction command and failing/passing output for Execution evidence. Exploratory scratch captures are local, never upload candidates.

Choose proof by the change:

| Change | Visual evidence |
| --- | --- |
| Static layout, typography or copy | Matching Before/After `.png` screenshots; no video required. |
| Interactive UI | Always an After walkthrough `.mp4`; add static `.png` pairs where layout changed. |
| Bug fix or change to an existing interactive flow | Also a matching Before walkthrough `.mp4`. |
| Net-new control or route | After walkthrough; omit Before video of a flow that did not exist. |

Create each capture with `mktemp`, e.g. `"${TMPDIR:-/tmp}/before-desktop.XXXXXX.png"` or `"${TMPDIR:-/tmp}/after-desktop.XXXXXX.mp4"`. Write Before captures on the unpatched baseline before edits. Use `1440×900` desktop, plus `390×844` mobile when responsive behavior is affected; pair Before/After at the same viewport, state and flow. Retain those exact paths for the PR. Recover a missing Before from a temporary detached Base branch worktree (or the diagnosis Session's specified reproduction commit), boot it with independent temporary state, capture, stop its children and remove the worktree inside the same EXIT cleanup.

## Phase 2 — Clean walkthrough pass

Once exploration passes, record the chosen flow in one uninterrupted disposable Playwright script created with `mktemp` and removed by the owning subshell's EXIT trap. Use the repository's installed Playwright (resolve it from its package directory when the script lives outside the repository, such as in `${TMPDIR:-/tmp}`) and headless Chromium. Keep the script temporary; a separate durable regression test may be warranted at the repository's test seam.

Set `viewport` explicitly and match `recordVideo.size` to it: Playwright otherwise scales recordings down. For Playwright `>= 1.59`, enable native `recordVideo.showActions` cursor/click/highlight annotations:

```js
const viewport = { width: 1440, height: 900 }; // mobile: 390 × 844
const context = await browser.newContext({
  viewport,
  recordVideo: {
    dir: recordingDir, size: viewport,
    showActions: { cursor: 'pointer', duration: 500, style: {
      point: 'width:24px;height:24px;border:2px solid #e11d48;border-radius:50%',
      highlight: 'background:#facc1533;outline:2px solid #e11d48',
    } },
  },
});
```

Only when the target repository pins Playwright `< 1.59`, omit `showActions` and inject a lightweight cursor and click-ripple overlay with `context.addInitScript` before navigation: a fixed, high-z-index, `pointer-events:none` cursor updated on `mousemove`, and a transient expanding ring on `pointerdown`. Use CSS transitions and remove expired rings. Record the compatibility fallback in Evidence; keep the repository's dependency pin.

Attach listeners before navigation to collect unexpected `pageerror`, console errors, failed requests and `5xx` responses (including popups if the flow opens them). Drive the already explored steps with stable accessibility/DOM locators and assert the expected state after each action. Use brief `~300–500 ms` beats to make clicks and changes legible, with no model-thinking pauses in the recording. Name any expected failures explicitly; assert zero unexpected page errors or `5xx` responses before accepting the pass. Do not hide failures to produce a clean video.

Await `context.close()` to flush the recording, then `browser.close()` in `finally`. Transcode the resulting `.webm` with `ffmpeg` into a separate `mktemp "${TMPDIR:-/tmp}/after-desktop.XXXXXX.mp4"` capture (use Before/mobile names as appropriate):

```sh
ffmpeg -y -i "$raw_video" -an -c:v libx264 -pix_fmt yuv420p \
  -movflags +faststart -crf 28 "$capture"
test -s "$capture" && test "$(wc -c < "$capture")" -le 8388608
```

Target `5–25 s` of deliberate actions. If the output exceeds `8 MB` (`8,388,608` bytes), shorten the flow or lower bitrate and encode again; upload only a checked file. Review the finished screenshots/video for the claimed state, legibility and faux/redacted data. Keep the paired capture paths and flow/viewport labels for the `pr` skill, which validates and publishes GitHub attachments.

## Completion

Return the explored flows, commands/results, exact capture paths and any remaining limits. When the app, browser, `ffmpeg` or `gh >= 2.103.2 --attach` cannot run, keep the PR Ready for review with an explicit limitation under `## Evidence` naming what could not run and why. Continue available execution checks; absence of a recording adds no mechanical merge gate. A reproduced UI defect still needs a fix and regression test.
