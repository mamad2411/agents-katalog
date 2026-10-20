---
name: studio-cua-drive
description: >-
  Drive Mac Studio desktop/Chrome from Hermes on Pro via SSH + Studio
  cua-driver CLI (never Pro computer_use on the Screen Sharing window).
version: 1.2.1
---

# Studio cua-drive (SSH)

## When to use
- Cooper wants automation on **Coopers-Mac-Studio** Chrome/apps without touching Pro browser tabs.
- AA.com / rebook / travel-credit forms, Studio-only logins.

## Anti-pattern (user correction — LOUD)
**Do not** drive Studio by Pro `computer_use` against **Screen Sharing**. That AX tree is only Screen Sharing chrome. Pixel-driving remote video is last resort. Canonical path: **SSH → Studio `cua-driver`**. Cooper will interrupt (“ssh in then use cua”, “PLEASE STOP”) if you loop Screen Sharing / local Pro Chrome.

## Stop / thrash (user correction)
When Cooper says stop / is interrupted / switches goals: **halt** automation immediately. Do not keep “one more script” cycles on AA forms, redials, or scroll loops. Resume only on a new explicit ask. Treat **“PLEASE STOP WITH THE …”** and mid-turn interrupts as hard stops — summarize state once if useful, then wait.

## Canonical workflow

**Computer-use-only preference:** Cooper requires Studio UI automation through the computer-use agent / `cua-driver` only. Do not use AppleScript, shell-based UI automation, `open -a` URL launching, direct browser scripting, or Pro Screen Sharing as a substitute. If CUA capture is unavailable, stop and report the blocker; do not guess coordinates or silently downgrade.

**Do not mix browser protocols:** the Kernel browser skill's vision workflow (`vmap.py`/`vcoord.py` and its configured vision model) applies only to Kernel cloud browsers. This local-Studio skill uses `cua-driver` snapshots and actions; it does not imply Kernel vision.

**Verified drive loop:** start/revive a named session; list windows; snapshot the exact Chrome PID/window before every action; act on current element index/token; re-snapshot after each state change. Escalate background → foreground only after the driver reports an ineffective/unverifiable action. If the session expires, revive it. If the window becomes AX-unresolved or screenshot capture fails, stop and ask the user to bring Chrome front/unlock or run the driver doctor—never fall back to shell navigation.

```bash
HOST=coopermaruyama@coopers-mac-studio
export RPATH='export PATH=$HOME/.local/bin:/opt/homebrew/bin:$PATH'

ssh -o BatchMode=yes -o ConnectTimeout=15 "$HOST" "$RPATH; cua-driver status"
```

1. Daemon on Studio: `cua-driver serve` (add `--grant existing-profile` when attaching logged-in Chrome). Expect Accessibility + Screen Recording true for `com.trycua.driver`.
2. JSON-stdin calls (quote-safe):
   ```bash
   echo '{"session":"job1","capture_scope":"window"}' | cua-driver call start_session
   echo '{"session":"job1"}' | cua-driver call list_windows   # pick Chrome pid + window_id
   echo '{"session":"job1","pid":PID,"window_id":WID,"include_screenshot":false,"max_elements":200}' \
     | cua-driver call get_window_state
   ```
3. Snapshot before every element_index action — indices expire after navigation.
4. Web forms: use `delivery_mode: "foreground"` only when a prior background action was ineffective/unverifiable; then re-snapshot to verify.
5. Navigate only through visible CUA address-bar interaction or a CUA browser navigation action; never use shell URL launching or AppleScript.
6. At regulated, financial, account-security, identity, legal-consent, MFA, payment, approval, or submission checkpoints, stop unless the user explicitly authorizes that exact action. Standard terms acceptance is allowed only when it is clearly required to reach the requested form and the user has not prohibited it; if the user says it was okay to click, proceed with a fresh snapshot and CUA click.
7. If Chrome focus shifts to another existing tab/window, do not use shell navigation or assume a text `replace` flag worked. Fresh-snapshot the visible Chrome window, click the address bar, send `cmd+a` as a discrete CUA key action, type the URL, send `return`, then re-snapshot the resulting page. If the address bar is clean but Return/Reload remains ineffective after the documented background→foreground escalation, stop rather than appending duplicate URLs or repeatedly retrying. Report that CUA native-event delivery is the blocker; do not downgrade to AppleScript, shell URL launching, CDP, Playwright, or Kernel.
8. For a requested Chrome restart, prefer the proper CUA hotkey chord `hotkey` with `keys:["cmd","q"]`; a standalone `press_key` for `q` is not equivalent. Verify the Chrome windows disappear, then relaunch via the CUA `launch_app` action. Standard mode must refuse force-killing a foreign Chrome process; do not bypass that safety gate. If the daemon exits during quit/relaunch, restart the daemon and verify connectivity before continuing.
9. Long automation: use discrete CUA calls; avoid giant quoted remote shell commands and generated UI scripts.

## Consent gates & regulated-filing predicate (user corrections — LOUD)

- **Consent gates are PRE-AUTHORIZED.** "Get through the portal without issues" (or any get-it-done instruction) includes clicking agree/accept/terms gates as many times as needed. NEVER ask permission to click an agree/accept button — Cooper interrupted: "dont ask me permission to click the agree button for the 5th time." The ONLY hard stops are actual legal/financial SUBMISSION (e.g. Form 40 certify/file), credential/MFA entry, and payment. Section 6 below's "explicit authorization for legal-consent" applies to attestations, not routine portal agree gates.
- **Determine the predicate from ACTUAL positions BEFORE driving a regulated portal.** For CFTC Form 40 / LTR: log the user into Coinbase (user enters credentials manually), open advanced-trade **futures → Positions** tab, read contract/side/quantity/notional. An FCM-issued Form 40 notice is itself evidence the reporting level was already crossed — the notice answers the qualification question; the position read answers which contract. Choose the portal org type (LTR vs other) from that finding, never by guessing.
- **Coinbase positions table:** on the advanced-trade futures page the positions are under a **Positions (n)** tab; the table (AXTable) rows expose Market/Quantity/Notional/Avg Entry/Mark/Est Liq/Funding/P&L as AXStaticText. Scroll the page region down to bring the table into the AX tree if only headers appear.

## Transport architecture (user-corrected)
- Prefer a durable named Studio service over Tailscale/MagicDNS when available; do not manually run a fresh `ssh ... cua-driver call ...` for every action.
- The Studio’s macOS-managed `cua-driver serve` daemon is the durable GUI service. Hermes should connect once to its stdio MCP stream through a persistent SSH-backed MCP entry using the Studio’s Tailscale MagicDNS service name (for example `coopers-mac-studio`), with `BatchMode=yes` and pinned host-key checking. Verify with `hermes mcp test` and reload MCP/new-session before driving.
- Do not invent or switch to a public Cloudflare subdomain merely because the remote host is inaccessible: CuaDriver’s native interface is stdio, so a Cloudflare HTTP endpoint requires an explicit authenticated wrapper/proxy. Tailscale is preferred for private CUA transport.
- Do not report the setup as durable if the live session is still using manually scripted SSH calls; distinguish the configured MCP transport from the currently loaded tool registry. A valid `hermes mcp test` proves discovery/configuration, not that the current TUI has reloaded it; verify the live `mcp_stdio_watchdog` + SSH child, then `/reload-mcp` or start a fresh session.
- Smoke-test the whole path before regulated browser work: (1) `hermes mcp test cua-driver`, (2) confirm the persistent watchdog/SSH child on the Mac Pro, (3) confirm Studio `cua-driver status`, (4) perform one real read-only CUA call such as `list_windows` or `get_window_state`. Keep host roles explicit: Hermes/MCP client on the Mac Pro, CuaDriver/Chrome on the Studio, Linux not involved unless explicitly requested.
- **Multiple Studio services:** one macOS-managed CuaDriver daemon is not a one-MCP-server limit. Multiple MCP client streams/sessions can share it; coordinate concurrent access to the same Chrome window. HTTP dashboards/tools should run as separate localhost services on separate ports. Use Tailscale Serve for tailnet-only HTTPS and path routing (for example `/dashboard` → `127.0.0.1:8787`, `/api` → `127.0.0.1:3001`); use structured Serve config for multiple handlers rather than repeated commands that may replace the route table. Cloudflare is only needed for non-Tailnet/public access. CuaDriver remains stdio over Tailscale SSH unless an explicit authenticated HTTP MCP wrapper exists.

## Resource-safety guard
Before long or repeated Studio CUA work, take a lightweight host snapshot (`uptime`, `memory_pressure`, and top CPU processes). Avoid high-frequency screenshots/polling or concurrent CUA sessions when the host is already heavily loaded by a VM, local LLM server, multiple coding-agent processes, or WindowServer. A recent Studio panic showed the failure mode: this was not RAM exhaustion (compressor/swap were healthy), but `configd` missed watchdog check-ins for 180 seconds while aggregate CPU pressure was high; `cua-driver` was also a significant CPU consumer. Prefer one CUA session, discrete actions, bounded waits, and a cooldown/stop when load is extreme. Never restart VPN/network daemons repeatedly during this state because configd starvation can turn recovery attempts into another watchdog panic.

## Chrome pitfalls
- MCP bridge `:12306` is sticky single-client (`Already connected`). Prefer cua-driver or free the other client.
- When Hermes runs on Pro but cua-driver is installed on Studio, configure an SSH-backed MCP stdio server rather than copying the Studio absolute path into local config:
  ```bash
  hermes mcp add cua-driver --command ssh --args -o BatchMode=yes -o StrictHostKeyChecking=yes coopermaruyama@coopers-mac-studio ~/.local/bin/cua-driver mcp
  ```
  Accept tool discovery, then run `/reload-mcp` in the live Hermes TUI. Verify with `hermes mcp test cua-driver`.
- **Chrome URL navigation (verified):** Return keypresses on an existing tab's address bar repeatedly no-op (AdBlock-tab failure, several attempts). Reliable path: `cmd+t` (foreground) fresh tab → click address bar → `cmd+a` → `type_text` URL → Return (foreground). Foreground delivery is required for these Chrome field keystrokes; background CGEvent presses drop.
- Apple Events JS off until Chrome menu enables it; legacy `page` mutations may need unrestricted/approved mode.
- `browser_prepare` existing-profile often needs interactive `browser-approve` or serve `--grant existing-profile`.
- Browser target/tab refs are short-lived and can be invalidated by navigation or daemon restart. After `browser_prepare`, bind with `get_browser_state` immediately; after navigation, re-prepare and re-bind before querying or acting on page refs. Do not reuse a pre-navigation target ID.
- **CuaDriver TCC identity pitfall:** macOS Screen Recording / Accessibility grants key on the app bundle `/Applications/CuaDriver.app` (com.trycua.driver), NOT the `~/.local/bin/cua-driver` symlink — granting the symlink does nothing. The correct fix flow is `cua-driver permissions grant` (a LaunchServices launch attributes the TCC prompt to the bundle), then verify `cua-driver permissions status --json` reports `screen_recording: true`. Do not keep clicking through System Settings against the wrong binary.
- **Permission-induced daemon restart (verified Studio pitfall):** if bindings disappear repeatedly, inspect the Studio daemon log/status before retrying. Missing Screen Recording causes `cua-driver` to log `still waiting on: Screen Recording` and periodically `rechecking permissions — restarting daemon`; every restart invalidates MCP sessions, target/tab refs, and the owned DevTools endpoint. This is the "remote debug keeps disappearing" failure mode — it is NOT Chrome losing DevTools. Fix the bundle grant (above), restart the daemon once with `--grant existing-profile`, verify status stable, then `browser_prepare` + `get_browser_state` again. Do not thrash with stale refs.
- When Hermes runs on Pro via an SSH-backed MCP server, the remote daemon’s permission state is authoritative; `hermes mcp test` can succeed even while the daemon is restarting between browser calls, so also verify `cua-driver status` and the daemon log.
- For ordinary page inspection, prefer the CUA `page`/AX snapshot (`query_dom` or visible AX elements) and use current element indices; do not invent selectors or rely on stale refs. Native dropdown options may be exposed only as the placeholder in AX; do not guess an organization/category choice—report the exact list if available or ask the user.
- **AX-truncated dynamic panels (verified technique):** dense SPA chrome (Coinbase notifications panel, profile dropdowns, TradingView widgets) often truncates the AX tree before panel contents appear — the tree shows toolbar/nav but not the opened panel. Do not keep raising `max_elements` (it returns earlier-different noise) or conclude the panel is empty. Use `get_window_state(include_screenshot=true)` then `vision_analyze` on the saved image to read the panel, then act on what vision reports (pixel click at panel coordinates). Verified on Coinbase notifications bell and profile menu.
- Screenshot writes: use `$HOME/…` paths (e.g. `~/aa-shot/`).

## Regulated portal handoffs
- For official government portals, accept a required terms/warning gate only after explicit user authorization when the action attests to consent; then re-snapshot and report the new checkpoint.
- Account creation/request forms are a separate checkpoint from portal navigation: inspect the required fields, but stop before entering personal data or submitting until the user provides the missing values and explicitly authorizes submission.
- CFTC-specific field/checkpoint notes: see `references/cftc-portal-handoff.md`.

## AA / airline SPA booking (checklist)
Full recipes: `references/aa-booking-form-pitfalls.md`, `references/aa-online-credit-rebook.md`.

1. **Trip type:** force **One way** / Round trip. Multi city empties Flight 2 and can jam the date into Arrival.
2. **Fields:** `Departure airport` / `Arrival airport` / `Departure date` — re-read; Arrival must be airport code, **not** `mm/dd/yyyy`.
3. **Search:** form **Search**, not chrome **Submit search**.
4. **Fare ladder:** “Main from $836” opens Basic ~$836 vs **Main ~$946**. Click `Select … Main fare for $946`. Exclude Basic / Main Extra / Premium.
5. Band toggle “Fare options… being displayed” is **not** product Select — do not re-click it as the fare.
6. **Credit:** 13-digit `001…` required (PNR alone fails). Placeholder `ex. 001…` after “fill” = miss. Gate: **ticket digits must appear in cheap pre-submit readback**. Silent empty form after verified submit = **no AA match** (number wrong), not “field lost” — do not retry same 001… as automation fix.
7. **Spoken ticket from phone:** treat as **hypothesis** until cancel/e-ticket email or clean AA success. Session fact: Levi STT `0012342708964` was accepted cleaned on AA and returned empty form → **wrong digits** (Cooper confirmed). Never re-use that number.
8. **Summary:** Stay in Main if upsell; prefer **Continue as guest** (not accidental **Log in and continue**); **never** Purchase without Cooper go.

## Related
- Operator runbook: `references/studio-cua-runbook.md`
- AA canceled-PNR / travel-credit: `references/aa-online-credit-rebook.md`
- AA search/fare/passenger forms: `references/aa-booking-form-pitfalls.md`
- HITL / phone stop rules: `vapi-phone-ops` (communications)
- BlueBubbles send identity: Studio BB only `cooperton42391@gmail.com` — never Pro Messages self-loop

## Protected forms and locked Studio sessions
- For regulated, financial, account-security, or identity forms, navigate only to the relevant official portal and inspect the page; stop before account creation, personal-data entry, MFA, approvals, payments, or submission unless the user explicitly authorizes that exact step.
- If `list_windows` finds Chrome but `get_window_state` reports `desktop_unlocked: false`, an unresolved AX window, or unavailable screenshot, do not use Screen Sharing as a substitute and do not pixel-drive blindly. Open the requested URL if needed, then stop and tell the user to unlock/wake the Studio (or run the driver doctor) before continuing.
- Use a fresh Chrome tab for the requested portal so unrelated existing tabs are not disturbed. Re-capture after navigation and before every action; element indices expire after navigation.
- Report the exact handoff point: current URL/page, what is visible, and the next user-only step (for example, entering identity details or handling an MFA code).

## Verify
- Studio `get_window_state` shows web fields (Last name, Departure airport, etc.), not Screen Sharing toolbar.
- Re-read field values before claiming submit success.
- AA credit: real `001…` in the ticket field (not placeholder) before “credit looked up.”
- AA fare: trip-summary shows **Main** + agreed total (~$945.50 class), not only the band “from $836.”
