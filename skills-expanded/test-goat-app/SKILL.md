---
name: test-goat-app
description: Test GOAT's web and desktop UI through its built-in Browser panel against isolated development state. Use for browser verification, browser pairing recovery, and test fixtures. Use test-goat-mobile for native mobile verification.
---

# Test GOAT web and desktop

Use GOAT's built-in Browser panel for verification. Its tools drive the GOAT
server's own headless browser, which runs without the desktop app, so a remote
or SSH host with only a GOAT server can use it too. Do not install or switch to
another automation system. For native mobile testing, use
[test-goat-mobile](../test-goat-mobile/SKILL.md).

`available:false` with no `tabId` only means no tab is open yet. Read its
`browser.state`: `installed` or `installs_on_open` means call `preview.open`
(the first open installs the browser and can take a minute), `installing`
means check `preview.status` again in a minute, and `install_failed` means
`preview.open` retries the install. The blockers are `blocked` or
`unsupported`, an install error from that retry, and a "browser preview tools
are off for this thread" error: report the reason and stop verification.
`goat_call {path:"host.status", args:{host}}` shows the same `browser` state for
another host.

## Start the app

Reuse this task's healthy dev server. Otherwise run `vp run dev` from the
repository root and retain its terminal session. Use the worktree's ignored
`.goat` state (`.t3` in a worktree created earlier) and read the actual ports and pairing URL from the dev-runner output.
Never run a server against `~/.goat/userdata` or `~/.t3/userdata`, and never set
`VITE_HTTP_URL` or `VITE_WS_URL`. `vp run migrate-dev-db` reads
`~/.goat/userdata/statev2.sqlite` (or `~/.t3/userdata/statev2.sqlite` when the
GOAT database is absent) and writes the worktree home.

Test with meaningful project and thread data. Read
[references/sqlite-fixtures.md](references/sqlite-fixtures.md) only when
inspecting or seeding SQLite. Stop the test server before direct fixture writes.

## Drive agent turns for free

Do not spend a paid model to see a turn render. `vp run dev` in a worktree registers
the `Replay (dev)` provider, which replays recorded turns with simulated streaming
through the real adapter and orchestration. Its models are scenarios: `showcase`
covers thinking, a plan, tool calls, an approval, and markdown. Press
`Ctrl+Alt+Shift+R` for a picker, or call `window.goatdev.replay("showcase")` from
the page. When the test needs real provider behavior, use that provider's cheapest
model, such as Haiku for Claude or Luna for Codex.

For the desktop client, start `GOAT_DEV_INSECURE_SECRET_STORAGE=1 vp run dev:desktop`
in the worktree, which keeps its isolated home. Without the flag, the unsigned dev
build makes macOS ask for the login keychain password on start, and that prompt
takes focus until someone answers it. With the flag, secrets saved through the
keychain earlier do not open, so enter them again. If saving connections fails on
an old saved-environment registry, start once without the flag first. Browser
cookie import still reads the OS key store. See
[State and ports](../../../docs/operations/development.md#state-and-ports).

## Use the Browser panel

GOAT's browser tools run through `goat_call`. Call `goat_call {path:"preview.status"}`, then
`goat_call {path:"preview.open"}` if the Browser panel is closed. Navigate to the complete
startup pairing URL once with `goat_call {path:"preview.navigate", args:{url}}`, then use
`goat_call {path:"preview.snapshot"}` and the other `preview.*` paths that
`goat_describe {path:"preview"}` lists.
If the token was consumed or expired, run `node apps/server/src/bin.ts pair`
for a fresh one. Keep using the same tab.

## Verify and retain

Exercise the affected flow and capture the state that proves it works. Keep
the server, state, and panel available while the user inspects or iterates.
An assistant turn ending is not teardown. Stop only processes you started,
using retained terminal sessions or captured PIDs.

When sharing is requested, start with `vp run dev --share` and give the user
a fresh complete pairing URL that you have not consumed. Keep other credentials
out of screenshots, commits, and replies.

## Computer use on another host

For a desktop flow that needs computer use on another host, read
`metrics.computerUse.reason` from `host.status` for that host. A Mac that
runs only a GOAT server cannot use it; the reason names the installed GOAT apps
and versions. A person at that Mac or over Screen Sharing updates and opens the
desktop app. Start the lane in the app's environment: SSH dispatch moves to the
app's server only once the background server has no running work, and threads
already there keep running without computer use. From a GOAT app connected
directly to the app's environment with permission to change its settings, the
person turns computer use on in **Settings → Computer** and approves the
thread's `computer_use.request` there. Agents cannot turn it on or approve it
themselves.
