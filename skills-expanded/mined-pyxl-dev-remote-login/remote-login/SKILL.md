---
name: remote-login
description: Get the user signed in to a site from their phone when the built-in browser (or any browser task) hits a sign-in page, 2FA or captcha and they may not be at the Mac. Sends them a link (chat + optional push); they sign in themselves on a live view, then Claude continues. Use instead of asking them to sign in at the Mac whenever they are away, on mobile, in Remote Control, or did not answer a sign-in request.
---

# remote-login

`remote-login` (this repository, linked into `~/.local/bin`) serves a one-time page on the Mac's Tailscale address; the phone must be on the same tailnet. The page shows a live view of a browser; the user's taps and keyboard become real input there. Claude never sees or types the credentials: they go phone -> server -> browser. Never ask the user to send a password in chat, and never type one yourself.

## Targets

- `pane`: Claude's built-in browser pane in the desktop app (real clicks/keystrokes on the Mac). The sign-in lands in the pane's persistent profile, so Claude keeps working there with the `mcp__Claude_Browser__*` tools. Needs the Mac screen unlocked and this session, with its Browser pane, on screen.
- `headless`: a dedicated headless Brave (profile `~/.cache/remote-login/profile`, CDP 127.0.0.1:9334), viewport set to the phone's own screen size, streamed with CDP screencast. Works with the Mac locked. The sign-in stays in that profile: continue the task there with
  `BU_CDP_URL=http://127.0.0.1:9334 BU_NAME=remote-login browser-harness` (call `ensure_real_tab()` first; helpers: `goto_url`, `page_info`, `click_at_xy`, `type_text`, `press_key`, `capture_screenshot`, `js`, `list_tabs`).
- `auto` (default): pane if possible, else headless (prints `FALLBACK headless: <why>`).

## Steps

1. Pane case: open the sign-in page in the built-in browser. Then put this session on screen and show the pane:
   - session id: `mcp__ccd_window__get_window_layout` -> `this_session.session_id` (`local_...`)
   - `open "claude://code/continue?session=<local_id>"`
   - `mcp__ccd_view__show_pane` with `pane: "preview"`
2. Start the server in the background (Bash `run_in_background: true`):
   `remote-login serve --host <site host> --url <sign-in URL> --notify`
   `--notify` also runs `~/.config/remote-login/notify LINK MESSAGE` (your own script: push service, chat bot...). Read the `TARGET` and `LINK` lines from the output file.
3. Tell the user in chat: the site, the target, and the link (also pushed, if `--notify`). One line on how it works: it behaves like a browser, tap a field and the phone keyboard opens and types live, swipe to scroll, "Terminé" when signed in. Pane target only: tap the keyboard icon at the top to type.
4. Wait for the background task to finish (do not poll). Output and exit code:
   `DONE` (0) signed in, continue. `CANCELLED` (3) they gave up: ask what to do. `TIMEOUT` (2, 15 min default, `--minutes`): say so.
5. Check the sign-in worked (pane: `get_page_text`; headless: browser-harness `page_info()`), then continue the task.
6. Headless: when the task is over, `remote-login headless-stop` (the profile and its sign-ins stay on disk).

## Limits

- A headless sign-in does not reach the built-in pane: Claude's cookie import needs a click in the desktop app and a keychain prompt. If the task must run in the pane, wait for the Mac to be unlocked and use the pane target.
- Pane target: the Mac must stay unlocked and the session on screen during the sign-in; the page warns them if the Mac locks.
- Port 8791 on the Tailscale address only; the token in the link is single-use: the first browser that opens the page claims it with a session cookie, any other device gets 403 (server stops on Terminé/Annuler/timeout).
- Build the helper after a fresh clone: `./build.sh` (Swift, uses the desktop app's Accessibility and Screen Recording grants, so run it from a desktop-app session).
