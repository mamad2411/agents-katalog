---
name: studio-cua-driver
description: |
  Drive Mac Studio GUI from Pro over SSH using Studio's local cua-driver
  (not Pro Screen Sharing). Use when user wants Studio desktop/browser
  automation, booking pages on Studio Chrome, or rejects Screen Sharing.
version: 1.1.0
metadata:
  hermes:
    tags: [cua-driver, mac-studio, remote, ssh, desktop]
    category: desktop
    related_skills: [computer-use, vapi-phone-ops]
---

# Studio computer-use via SSH + cua-driver

## Preference (hard)

When the target is **Mac Studio**, do **not** drive **Screen Sharing** with Pro Hermes `computer_use`. That only automates a remote-video frame with no real Chrome AX.

**Correct path:** SSH to Studio → Studio’s own `cua-driver` CLI against the local interactive session.

```bash
ssh -o BatchMode=yes coopermaruyama@<REDACTED>
```

User correction: *“why are you using screen sharing? ssh in then use cua”*.

## Prerequisites on Studio

| Check | Command / note |
|---|---|
| Binary | `~/.local/bin/cua-driver` → CuaDriver.app |
| Perms | Accessibility + Screen Recording for **com.trycua.driver** |
| Daemon | `cua-driver status` → socket under `~/Library/Caches/cua-driver/` |

**Binary/TCC identity:** `~/.local/bin/cua-driver` is a symlink to `/Applications/CuaDriver.app/Contents/MacOS/cua-driver`; macOS permissions belong to bundle ID `com.trycua.driver` / **CuaDriver.app**, not the symlink path. Verify with:

```bash
cua-driver permissions status --json
# Require: accessibility=true and screen_recording=true
```

If Screen Recording is unexpectedly false despite System Settings appearing correct, run the driver-owned permission flow (it attributes the request to the correct app and may show a macOS consent dialog):

```bash
cua-driver permissions grant
```

A daemon log repeatedly saying `still waiting on: Screen Recording` and `rechecking permissions — restarting daemon` means every live browser binding will be invalidated by those restarts. Fix TCC first, then re-prepare Chrome.

Start daemon with Chrome profile attach when automating logged-in Chrome:

```bash
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
pkill -f "cua-driver serve" 2>/dev/null || true
sleep 1
# Non-interactive SSH: TCC permissions gate can block and open System Settings.
# Prefer no-gate + grant when already previously authorized for com.trycua.driver.
nohup env CUA_DRIVER_RS_PERMISSIONS_GATE=0 \
  cua-driver serve --grant existing-profile --no-permissions-gate \
  > /tmp/cua-driver-serve.log 2>&1 &
sleep 2
cua-driver status
printf '%s' '{"session":"aa1","capture_scope":"window"}' | cua-driver call start_session
```

Without `--grant existing-profile`, `browser_prepare` refuses existing Chrome (`browser_consent_required`).
`cua-driver permissions status` may report daemon_running false even when `status` is healthy — trust a successful `start_session` over the TCC helper.

## Call shape

JSON on **stdin** (avoid shell-quote breakage):

```bash
printf '%s' '{"session":"aa1","capture_scope":"window"}' | cua-driver call start_session
```

Or a Python wrapper scp’d to Studio:

```python
subprocess.run(["cua-driver","call",tool], input=json.dumps(args), text=True, capture_output=True)
```

## Standard loop

1. `start_session` with stable `session` id
2. `list_windows` → Google Chrome by height + empty title OK; pick largest `bounds.height`
3. `get_window_state` every turn (indices expire); re-pick Chrome after every navigate/submit
4. Chrome web fields: `element_index` + `delivery_mode: "foreground"`
5. Re-read AX `value` before submit; DOB month often stuck on Jan after type — fix with open → `down` → `return`
6. Prefer a **local Python script scp’d to Studio** over giant SSH one-liners (quote breakage is constant)
7. Payment / final purchase / “Select … fare”: **stop and ask** — shop and expand fare ladders only

### Chrome AX quirks

| Control | What works |
|---|---|
| `AXTextField` | click → `cmd+a` → `type_text`; re-snapshot to confirm |
| `AXComboBox` (airport From/To) | fill hostel codes (`LAX`/`LHR`) then `return` to commit suggestion |
| `AXPopUpButton` (DOB siblings) | open → `down` / type short label → `return`; **re-check month every time** |
| Modifier chords | Use the driver's `hotkey` action for held combinations such as `cmd+q`/`cmd+l`; `press_key` with a modifier is a discrete event and may be ignored by Chrome |
| Unverifiable type | Values often stick anyway — trust re-snapshot, not `effect: confirmed` |
| type_text incomplete on day/year popups | open popup, type digits, `return`; if value ok already, leave it |
| Scroll | `AXWebArea` click + `pagedown` often **suspected_noop** on SPA pages; don’t rely on scroll for content |
| Screenshots | may fail under TCC even when AX works (`shot False`); text dump is enough |
| Deep sticky URL params | AA booking deeplinks may ignore query and land on empty form — fill Book flights UI manually |

### AA / airline booking notes (class)

- **Find reservation** works: last name + conf + DOB → cancel/active status is trustworthy.
- Canceled PNR pages often show **no residual $** in AX tree — don’t invent credit dollars; next is AAdvantage login / refund-status / phone.
- Legacy travel-credit paths (`/refunds/travelCreditLookUp.do`, `/manageTravelCredit/…`, `/travelInformation/manageCredits`) often **404 / taken flight** — use live Book or Receipts & refunds hub instead.
- After Search, results page is rich AX: date carousel `$…`, flight labels `AA 6935`, cabin buttons expand ladder (Basic / Main / Premium…).
- Expandfare button labels include “Click here for more fare options” → after click: “Fare options … displayed” + per-product Select buttons.
- **Never press Select / continue to pay** without Cooper.

### Hermes MCP integration (Pro Hermes → Studio CUA)

When Hermes runs on the Pro, do **not** configure the Studio-only absolute binary path directly; `~/.local/bin/cua-driver` exists on the Studio, not on Pro. Add an SSH-backed stdio MCP server instead:

```bash
hermes mcp add cua-driver --command ssh --args -o BatchMode=yes coopermaruyama@<REDACTED> ~/.local/bin/cua-driver mcp
```

Accept the tool-enable prompt, verify `hermes mcp list` shows `cua-driver` enabled, then run `/reload-mcp` inside the live Hermes TUI. The add command should connect and discover the CUA tool count before saving. The direct YAML shape supplied for a Studio-local Hermes is not portable to Pro.

### browser_* path (preferred for web navigation)

1. Start the daemon with existing-profile grant (`serve --grant existing-profile`; include the no-permissions-gate flags when the Studio is already TCC-authorized).
2. `browser_prepare` with `strategy: {kind: existing_profile}`, exact Chrome `pid`, and exact native `window_id`.
3. Immediately call `get_browser_state` with the same session/pid/window to obtain the live `target_id` and `tab_id`.
4. Call `browser_navigate` / `browser_click` / `browser_type` using those opaque ids.
5. After navigation, refs and bindings may be invalidated. Re-run `browser_prepare` and `get_browser_state` before the next browser query/action; never reuse a prior target/tab ref after a navigation or daemon restart.

**AX form/dropdown pattern:** For native Chrome forms, call `get_window_state` immediately before acting because element indices/tokens expire. Opening an `AXPopUpButton` and re-reading the tree exposes its `AXMenuItem` choices; use those exact labels rather than guessing. For legally meaningful acknowledgements (government terms, attestations, consent), stop and obtain explicit user authorization before clicking. Never submit an account request merely because the form is complete; review the fields and obtain explicit submission approval.

If `browser_prepare` returns `browser_consent_required`, restart the daemon with the existing-profile grant and retry. If a direct `get_browser_state` says `browser_requires_setup`, prepare again. AX remains a valid fallback for inspection, but browser-owned navigation is preferable once the existing profile is approved.

A compact MCP/SSH lifecycle transcript and reproduction recipe is captured in `references/mcp-ssh-browser-lifecycle.md` when available.

## Anti-patterns

- Pro `computer_use` app=`Screen Sharing` for Studio work
- Assuming Pro sees Studio AX trees
- Bare `open -a Chrome --args --remote-debugging-port=…` (flags often ignored)
- Unquoted zsh `*` in `--remote-allow-origins=*`
- Submitting airline/payment purchase without explicit user go-ahead

## Host

- SSH: `coopermaruyama@<REDACTED>`
- Pro Hermes `computer_use` = **local Pro only**

## References

- `references/studio-cua-runbook.md` — grants, form-fill pattern, SSH serve flags
- `references/aa-booking-lookup.md` — AA Find-your-trip / cancel / shop Aug patterns for Telavaya Reynolds PNR work
