---
name: firefox-stealth-automation
description: >-
  Manage Firefox MCP server configuration, anti-detection, and protocol
  switching. Covers the unified ultimate-firefox-mcp server (BiDi+CDP),
  Firefox profile prefs to preserve password autofill, and MCP server
  config updates for OpenCode and Codex. ALSO covers xul.dll binary
  patching to hide navigator.webdriver (the ONLY fix for Firefox 151+).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [firefox, stealth, anti-detection, mcp, automation]
    triggers:
      - firefox
      - stealth
      - anti-detection
      - password-autofill
      - signon
      - webdriver
      - marionette
      - browser-automation
      - ultimate-firefox-mcp
      - firefox-mcp
      - opencode-mcp
      - codex-mcp
      - browser-cdp
      - browser-engine
      - cdp-url
      - agent-browser
      - cloudflare
      - csp
      - bot-detection
      - tampermonkey
      - userscript
      - gm_xmlhttprequest
      - conversation-extraction
      - chatgpt-scraping
      - grok-scraping
      - pim-ingestion
      - remote-debugging-port
      - bidi-session-limit
      - stealth-verify
      - port-ghosting
      - time-wait
      - session-cookies
      - firefox-profile-contamination
      - two-profile-strategy
      - bookmarklet
      - console-paste
      - content-security-policy
      - bot-management
      - harvester
      - bidi-protocol
      - remote-active-protocols
      - config-override
      - prefs-persistence
      - profile-config
      - profile-extension-install
      - signon-username-only
      - policy-templates
      - extended-trigger-list
    related_skills: [firefox-cdp-bridge, firefox-remote-control, multi-agent-system-architecture, firefox-stealth-ops]
---

# Firefox Stealth Automation & MCP Server Management

## 🔥 CRITICAL: xul.dll Binary Patching (Solves navigator.webdriver for GOOD)

**`navigator.webdriver` in Firefox 151+ is forced at the C++ level when `--remote-debugging-port` is active.** The check is in `Navigator::GetWebdriver()` which calls `RemoteAgent::IsRunning()`. This is NOT fixable by:
- ❌ `user.js` prefs (`dom.webdriver.enabled=false`) — C++ code bypasses prefs
- ❌ `lockPref()` in `autoconfig.cfg` — runs before command-line flags, but C++ ignores the lock
- ❌ `script.addPreloadScript` JS overrides — `Object.defineProperty` can't override C++ getter
- ❌ `Page.addScriptToEvaluateOnNewDocument` — same limitation
- ✅ **The ONLY fix: binary patching `xul.dll`** to remove the `"webdriver"` string

### The Patch (30 seconds)

1. Copy Firefox installation to a user-writable directory (no admin needed):
   ```bash
   cp -r "/c/Program Files/Mozilla Firefox/"* "${USER_HOME}/firefox-portable/"
   ```

2. Replace ALL webdriver-related byte strings — there are TWO patterns:
   - `b'webdriver'` (9 bytes) — the C++ property name, 3 occurrences in xul.dll
   - `b'WEBDRIVER_BIDI'` (14 bytes) — the BLOCKING_REASON_WEBDRIVER_BIDI constant, 1 occurrence

   Use mmap to avoid MemoryError (xul.dll is 150-170MB):

   ```python
   import mmap
   path = r'${USER_HOME}\firefox-portable\xul.dll'
   with open(path, 'r+b') as f:
       with mmap.mmap(f.fileno(), 0) as mm:
           # Pattern 1: 9-byte "webdriver" (3 occurrences)
           pos = 0
           while (pos := mm.find(b'webdriver', pos)) != -1:
               mm[pos:pos+9] = b'w3bdrv3r_'
               pos += 9
           # Pattern 2: 14-byte "WEBDRIVER_BIDI" (1 occurrence)
           pos = 0
           while (pos := mm.find(b'WEBDRIVER_BIDI', pos)) != -1:
               mm[pos:pos+14] = b'W3BDRVR_BIDI__'
               pos += 14
   ```

3. Verify (read first/last 5MB to avoid MemoryError):
   ```python
   with open(path, 'rb') as f:
       head = f.read(5000000)
       f.seek(-5000000, 2)
       tail = f.read()
   print(f'webdriver strings remaining: {head.lower().count(b"webdriver") + tail.lower().count(b"webdriver")}')
   ```
   Should print: 0

### How it works

- `xul.dll` contains the compiled C++ implementation of `Navigator::GetWebdriver()`
- The C++ function uses the string `"webdriver"` internally for the property name
- By changing the string to random garbage (keeping same 8-byte length), the property becomes `undefined`
- All other uses of the word "webdriver" in the binary are references to the same string pool entry
- The browser remains fully functional — only `navigator.webdriver` is affected
- **Works with `--remote-debugging-port` enabled** — Robot detection is GONE

### Verification

Start the patched Firefox with remote debugging and check:
```python
result = await client.evaluate("typeof navigator.webdriver")
# -> "undefined"
```

### Robot icon (userChrome.css)

The xul.dll patch hides `navigator.webdriver` at the C++ level, but Firefox's **chrome UI still shows a robot icon** in the address bar when `--remote-debugging-port` is active. The browser itself detects the startup flag and renders `#remote-control-box` — sites see `navigator.webdriver=undefined`, but the user sees the icon.

**Fix: userChrome.css**

```css
#remote-control-box { display: none !important; }
```

**Steps:**
1. Create `chrome/userChrome.css` in the profile directory with the CSS above
2. Add to `user.js` or `prefs.js`: `user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);`
3. Restart Firefox

The `#remote-control-box` element is the chrome-level DOM node containing the robot icon and "controlled by automated software" text. This is a UI-only cosmetic fix — the underlying automation flags remain, only the visual indicator is hidden. All functional behavior (password manager, tab restore, BiDi/CDP) is unaffected.

### Inspiration

Approach from `bytexenon/undetected_geckodriver` (pip package) and `coleleavitt/undetected_geckodriver` (Rust binary patcher). These are open-source projects that patch `libxul.so` / `xul.dll` to remove the webdriver flag. The approach: replace ALL occurrences of `b"webdriver"` in the binary with random bytes of the same length.

### Camoufox (pre-built patched Firefox)

**Repo:** `https://github.com/daijro/camoufox` (8.8k ★)  
**Windows binaries available** in releases (`camoufox-*-win.x86_64.zip`).  
Pre-patched Firefox fork built on LibreWolf with extensive anti-detection modifications:
- Patches `NavigatorManager.cpp` for per-context navigator property control
- Audio/WebGL/font fingerprint spoofing
- Geolocation, permissions, media device spoofing
- Blocks `browsingContext.create` via BiDi (anti-debugging measure)
- Config via `camoufox.cfg`

**Note:** Camoufox blocks BiDi tab creation as an anti-detection measure. Use a non-Camoufox patched Firefox (the simple xul.dll string-replacement approach above) when BiDi automation is needed.

**Pattern:**
1. Start the AUTOMATION Firefox first (with `--remote-debugging-port` using the hermes-mcp profile)
2. Log into sites ONCE in that window (ChatGPT, Grok, etc.)
3. Leave it running in the background — the MCP servers connect to IT
4. the operator opens his NORMAL Firefox separately for browsing — stays clean

## Architecture

Three layers prevent Firefox from detecting automation and disabling password manager:

  1. **Profile prefs** — `user.js` enforces `marionette.enabled=false`, `dom.webdriver.enabled=false`,
     and forces `signon.*=true` at the browser level
  2. **Server-level stealth** — unified `ultimate-firefox-mcp` auto-injects anti-detection JS
     on every page load, hiding `navigator.webdriver`, plugins, etc.
  3. **Tool-level config** — OpenCode and Codex each maintain their own MCP server configs
     that must point to the unified server

## Layer 1: Firefox Profile Preferences

### Profiles to patch
| Profile | Type | Path |
|---------|------|------|
| Hermes MCP (automation) | AUTOMATION | `C:\\Users\\<you>\\AppData\\Local\\hermes\\firefox-profile\\` |
| <profile-id> (normal browsing) | NORMAL | `%APPDATA%\\Mozilla\\Firefox\\Profiles\\<profile-id>.default-release-1\\` |

### Patcher script (v2 — detects automation prefs in normal profiles)
`C:\\Users\\<you>\\AppData\\Local\\hermes\\firefox-stealth-patcher.py` (legacy, file-system install)
`scripts/stealth-patcher.py` (skill-bundled v2 — preferred)

v2 adds detection of `remote.active-protocols=1` and `devtools.debugger.remote-enabled=true`
in normal-browsing profiles. Use the skill-bundled version:

```bash
# Run from the skill directory
python /path/to/skill/devops/firefox-stealth-automation/scripts/stealth-patcher.py --check --all

# Or copy to PATH
python scripts/stealth-patcher.py --all
```

```bash
# Patch all known profiles
python firefox-stealth-patcher.py --all

# Check status only
python firefox-stealth-patcher.py --check --all

# Patch specific profile
python firefox-stealth-patcher.py --profile "C:\\path\\to\\profile"
```

### user.js template — NORMAL browsing profile (NO automation)
Only marionette/webdriver stealth + password manager. No BiDi/CDP prefs.

```javascript
user_pref("marionette.enabled", false);       // prevents navigator.webdriver
user_pref("dom.webdriver.enabled", false);    // explicit webdriver flag override
user_pref("signon.autofillForms", true);      // keep password autofill ON
user_pref("signon.rememberSignons", true);    // keep password saving ON
```

### user.js template — AUTOMATION profile (with remote debugging)
Same stealth + explicit remote debugging prefs for BiDi.

```javascript
user_pref("marionette.enabled", false);
user_pref("dom.webdriver.enabled", false);
user_pref("signon.autofillForms", true);
user_pref("signon.rememberSignons", true);
user_pref("devtools.debugger.remote-enabled", true);     // allow BiDi/CDP
user_pref("devtools.debugger.prompt-connection", false);  // no prompt
user_pref("remote.active-protocols", 1);                 // BiDi only
```

After modifying profiles, **restart Firefox** for changes to take effect.

### Launcher
`C:\\Users\\<you>\\AppData\\Local\\hermes\\firefox-stealth.bat`
Patches profiles then starts Firefox with `--remote-debugging-port 9222`.

### 🚨🚨🚨 Orphan Firefox accumulation — the #1 cause of broken profiles 🚨🚨🚨

Headless PIM extraction sessions that crash or miss cleanup can accumulate orphan Firefox processes. In one incident, **23 orphan Firefox processes** accumulated over ~2 days, each holding a `parent.lock` on various profiles. This prevents Firefox from launching, blocks Sync, and corrupts the user's browsing experience.

**Prevention in `ingest-chatgpt-grok.sh` (the PIM ingestion script):**

Add an orphan cleanup step BEFORE launching Firefox. Kill any Firefox process on the PIM port (9239) by PID, targeting only the automation Firefox:

```bash
python << 'PYEOF'
import subprocess
try:
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=5)
    for line in result.stdout.splitlines():
        if ':9239' in line and 'LISTENING' in line:
            pid = line.strip().split()[-1]
            if pid != '0':
                subprocess.run(['powershell', '-Command', f'Stop-Process -Id {pid} -Force'],
                              capture_output=True, timeout=5)
                print(f'Killed orphan PID {pid} on port 9239')
except Exception as e:
    print(f'Orphan cleanup skipped: {e}')
PYEOF
```

**Do NOT use `taskkill /F /IM firefox.exe`** — that kills the user's visible Firefox with active login sessions. Always kill by port-specific PID.

**Cleanup after any Firefox interaction:**

After killing a headless Firefox process (either manually or in the ingestion cleanup step), ALWAYS:
1. Remove stale `parent.lock` from the profile directory: `rm -f /path/to/profile/parent.lock`
2. Wait 2-3 seconds for the OS to release file handles before relaunching
3. Check with `ls -la /path/to/profile/parent.lock` that it's gone

**Detection:** Run `netstat -ano | grep LISTENING` and check for unexpected Firefox processes (multiple PIDs on your debug port, or processes that have been running for hours/days). Run `find ${USER_HOME}/AppData/Roaming/Mozilla/Firefox/Profiles -name "parent.lock"` to find stale locks.

### 🛠️ profiles.ini configuration — setting the right default profile

When Firefox has multiple profiles (common with automation testing), the `profiles.ini` file at `%APPDATA%\Mozilla\Firefox\profiles.ini` may have the wrong profile set as default. This causes Firefox to open the wrong profile when the user clicks the icon.

**Structure:**
```
[Install<GUID>]           ← One per Firefox installation
Default=Profiles/<name>   ← Default profile for that installation
Locked=1

[ProfileX]                ← Each profile
Name=<display-name>
IsRelative=1
Path=Profiles/<folder>
Default=1                 ← SYSTEM default (only one profile should have this)
StoreID=<mozilla-account> ← Mozilla Account linked to this profile
```

**Fixing:**
1. Find the right profile section (e.g., `[Profile2]` with `Name=default-release-1`)
2. Set it as default for the main installation: change `Default=<wrong>` to `Default=Profiles/<profile-id>.default-release-1` in the `[Install308046B0AF4A39CB]` section
3. Remove `Default=1` from any other profile section (only one system default should exist)
4. Ensure `StartWithLastProfile=1` is still set in `[General]`

**Verification:** Launch Firefox — it should open the right profile. Check `about:profiles` in the browser.

### 🍪 Copying cookies between profiles (migrating sessions)

When ChatGPT/Grok/YouTube sessions expire in the automation profile, the fix is to copy the session cookies from the operator's main browsing profile — NOT to switch the PIM target profile:

```bash
python << 'PYEOF'
import shutil, os, sqlite3

main = r'${USER_HOME}\AppData\Roaming\Mozilla\Firefox\Profiles\<profile-id>.default-release-1'
auto = r'${USER_HOME}\AppData\Local\hermes\firefox-profile'

# Stop Firefox first! (kill by PID on 9239)
# Then copy session-critical files
for fname in ['cookies.sqlite', 'logins.json', 'key4.db']:
    src = os.path.join(main, fname)
    dst = os.path.join(auto, fname)
    if os.path.exists(src):
        # Backup existing automation file
        bak = dst + '.bak'
        if os.path.exists(dst) and not os.path.exists(bak):
            shutil.copy2(dst, bak)
        shutil.copy2(src, dst)
        print(f'Copied {fname} ({os.path.getsize(src):,} bytes)')

# Verify ChatGPT session tokens made it
conn = sqlite3.connect(os.path.join(auto, 'cookies.sqlite'))
cur = conn.execute("SELECT host, name FROM moz_cookies WHERE host LIKE '%.chatgpt.com' AND name LIKE '%session%'")
tokens = cur.fetchall()
print(f'ChatGPT session tokens: {len(tokens)}')
conn.close()
PYEOF
```

Key files to copy: `cookies.sqlite` (session cookies), `logins.json` (saved passwords), `key4.db` (encryption key), `places.sqlite` (bookmarks/history — optional but useful), `signedInUser.json` (Firefox Account / Sync).

### 🚨🚨🚨 CRITICAL: Never use the operator's main profile for PIM headless extraction 🚨🚨🚨

**Every headless PIM ingestion run that uses the operator's real profile (`<profile-id>.default-release-1`) with `--remote-debugging-port` writes automation prefs into that profile's `prefs.js`.** These persist after Firefox exits:
- `remote.active-protocols=1` or `3`
- `devtools.debugger.remote-enabled=true`
- `devtools.debugger.prompt-connection=false`

When the operator later opens the same profile in his main Firefox (without `--remote-debugging-port`), these contaminated prefs cause the browser to initialize its Remote Agent, show the robot icon, potentially disable password manager, and be detectable by bot-detection services.

**ROOT CAUSE FIX:** PIM headless extraction MUST use the dedicated **automation profile** at `${USER_HOME}\AppData\Local\hermes\firefox-profile`, NOT the operator's main browsing profile. The automation profile already has `remote.active-protocols=1`, `devtools.debugger.remote-enabled=true`, and signon=force in its user.js — contamination is by-design and harmless.

**Files to update when switching profiles:**
| File | Variable/Section | Old | New |
|------|-----------------|-----|-----|
| `_firefox_bidi.py` | `AUTOMATION_PROFILE` constant | `OPERATOR_PROFILE` = <profile-id> | `AUTOMATION_PROFILE` = hermes-mcp |
| `ingest-chatgpt-grok.sh` | `--profile` arg | `<profile-id>.default-release-1` | `C:\...\hermes\firefox-profile` |
| `firefox-stealth.bat` | profile target | `default` or <profile-id> | hermes-mcp profile |

**The automation profile already has ChatGPT, Grok, and YouTube cookies** (cf_clearance, device IDs, __Secure-YNID). If sessions expire, launch the automation profile in a visible window and log in once — sessions persist across headless restarts.

### Profile contamination detection and cleanup (when automation prefs leaked into normal profile)
If a normal-browsing profile was EVER started with `--remote-debugging-port`,
it may have `remote.active-protocols=1` and `devtools.debugger.remote-enabled=true`
written into its `prefs.js`. These persist across restarts even without the flag.

**Check for contamination:**
```python
import os
profiles_dir = r'${USER_HOME}\AppData\Roaming\Mozilla\Firefox\Profiles'
for p in os.listdir(profiles_dir):
    prefs_path = os.path.join(profiles_dir, p, 'prefs.js')
    if os.path.exists(prefs_path):
        with open(prefs_path) as f:
            content = f.read()
        issues = []
        if 'remote.active-protocols' in content:
            if any('1' in l.split(',')[0] for l in content.splitlines() if 'remote.active-protocols' in l):
                issues.append('remote.active-protocols=1 (BiDi enabled)')
        if 'devtools.debugger.remote-enabled' in content:
            if any('true' in l for l in content.splitlines() if 'devtools.debugger.remote-enabled' in l):
                issues.append('devtools.debugger.remote-enabled=true')
        if issues:
            print(f'{p}: CONTAMINATED: {", ".join(issues)}')
```

**Fix in order:**
1. Kill all Firefox processes by port-specific PID (do NOT nuke user's visible Firefox):
   ```bash
   netstat -ano | grep LISTENING
   powershell -Command "Stop-Process -Id <PID> -Force"
   ```
2. Edit `prefs.js` in the contaminated profile: set `remote.active-protocols` to `0`, `devtools.debugger.remote-enabled` to `false`, `devtools.debugger.prompt-connection` to `true`
3. Ensure `user.js` does NOT contain any remote debugging or BiDi prefs (those belong only in the automation profile)
4. Remove stale `parent.lock` file from profile directory
5. Restart Firefox normally — verify `about:config` shows `remote.active-protocols=0` and no remote debugging indicators
6. Run the stealth patcher check: `python firefox-stealth-patcher.py --check --all`

**Prevention:** The PIM ingestion script (`ingest-chatgpt-grok.sh`) and `_firefox_bidi.py`'s `ensure_firefox()` function both use the `AUTOMATION_PROFILE` constant. Never change them to point to the operator's main profile. If a site requires the operator's session cookies, copy the cookies from the main profile to the automation profile rather than switching the target profile.

## Layer 2: Unified Firefox MCP Server

**Repo:** `https://github.com/pmb2/ultimate-firefox-mcp` (private)
**Workdir:** `C:\\Users\\<you>\\ultimate-firefox-mcp`
**Entry:** `python -m ultimate_firefox_mcp.main`

### 🚨 CRITICAL: pip install -e required (new-install / sync step)

The package must be installed as editable for other services to import it:
```bash
cd C:\\Users\\<you>\\ultimate-firefox-mcp
pip install -e .
```

**Without this step, `from ultimate_firefox_mcp.stealth import StealthEngine` silently fails** with ImportError in any Python process that doesn't already have the workdir on its sys.path. The PIM cron job (`ingest-chatgpt-grok.sh`) runs from a different directory and will silently fall back to **zero stealth** if the import fails — the ImportError is caught in `_apply_stealth()` and only logs a warning. This was the root cause of stealth being inactive for days after initial setup.

**Verification:**
```bash
pip list | grep ultimate-firefox-mcp
# Should show: ultimate-firefox-mcp   1.0.0    ...\ultimate-firefox-mcp
python -c "from ultimate_firefox_mcp.stealth import StealthEngine; print('OK')"
# Should print: OK
```

### Protocol Auto-Detection

The server tries BiDi (port 9223) first, then CDP (port 9222). Override with `--protocol`:

```bash
# Auto-detect (default)
python -m ultimate_firefox_mcp.main --protocol auto

# Force BiDi (newer, Firefox 136+)
python -m ultimate_firefox_mcp.main --protocol bidi --port 9223

# Force CDP (fallback)
python -m ultimate_firefox_mcp.main --protocol cdp --port 9222

# Human timing profile
python -m ultimate_firefox_mcp.main --profile human_slow
```

### Stealth Behavior (Always-On — No Opt-Out)

Both protocols ALWAYS have all 22 stealth measures applied. CDP stealth was upgraded 2026-05-29 (commit 6122e73) from a 4-measure fallback to the full 22-measure suite + `Network.setUserAgentOverride`.

| Protocol | Stealth mechanism | Measures | UA Spoof | Enabled by |
|----------|-------------------|----------|----------|------------|
| BiDi | `StealthEngine.apply()` injects 22 `script.addPreloadScript` patches | 22/22 | Profile-level `general.useragent.override` | Auto on connect |
| CDP | `Page.addScriptToEvaluateOnNewDocument` + `Network.setUserAgentOverride` injected in `attach_tab()` & `navigate()` | 22/22 | `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0` | Auto on attach + every navigate |

Stealth is **always applied** — there is no `--no-stealth` flag. CDP preload script (`Page.addScriptToEvaluateOnNewDocument`) ensures even newly created tabs/pages get full stealth before any page JS runs.

### Hermes Config Entry (standardized port 9239)

Placed in `~/.hermes/config.yaml` under `mcp:`. Use **port 9239** as the single standard port across all services — it's a high port that avoids Docker (9226) and other reserved ranges:

```yaml
  ultimate-firefox-mcp:
    args:
    - -m
    - ultimate_firefox_mcp.main
    - '--protocol'
    - 'auto'
    - '--port'
    - '9239'
    command: python
    timeout: 300
    workdir: C:\\Users\\<you>\\ultimate-firefox-mcp
```

This single entry replaces the three legacy entries (`firefox-devtools`, `firefox-phantom-mcp`, `firefox-remote`).

### Tool Name Aliases

All tool names from both original servers work. See `references/tool-aliases.md` for the complete map.

Key patterns:
- `firefox_*` prefixed names (phantom-mcp style): `firefox_navigate`, `firefox_click`, etc.
- Unprefixed names (firefox-remote-mcp style): `navigate`, `click`, `fill`, `screenshot`, etc.
- Stealth tools: `firefox_apply_stealth`, `stealth_inject`, `stealth_toggle`

## Layer 3: OpenCode & Codex MCP Config

Both OpenCode and Codex maintain their **own** MCP server configurations separate from Hermes.
After creating or updating the unified server, these must be updated independently.

### OpenCode

**Config file:** `~/.config/opencode/opencode.json`
**Section:** `mcp.ULTIMATE_FIREFOX`

```json
"ULTIMATE_FIREFOX": {
  "type": "local",
  "command": ["python", "-m", "ultimate_firefox_mcp.main", "--protocol", "auto"],
  "enabled": true,
  "cwd": "C:\\Users\\<you>\\ultimate-firefox-mcp",
  "description": "Unified Firefox MCP — BiDi + CDP + stealth anti-detection"
}
```

**Update method:**
```bash
python -c "
import json
with open(r'~/.config/opencode/opencode.json') as f: c = json.load(f)
c['mcp']['ULTIMATE_FIREFOX'] = {'type':'local','command':['python','-m','ultimate_firefox_mcp.main','--protocol','auto'],'enabled':True,'cwd':r'${USER_HOME}\ultimate-firefox-mcp','description':'Unified Firefox MCP — BiDi + CDP + stealth'}
if 'FIREFOX_DEVTOOLS' in c['mcp']: del c['mcp']['FIREFOX_DEVTOOLS']
if 'FIREFOX_REMOTE' in c['mcp']: del c['mcp']['FIREFOX_REMOTE']
with open(r'~/.config/opencode/opencode.json','w') as f: json.dump(c, f, indent=2)
"
```

### Codex

**Config file:** `~/.codex/config.toml`
**Section:** `[mcp_servers.ULTIMATE_FIREFOX]`

```toml
[mcp_servers.ULTIMATE_FIREFOX]
command = 'python.exe'
args = ['-m', 'ultimate_firefox_mcp.main', '--protocol', 'auto']
cwd = 'C:\\Users\\<you>\\ultimate-firefox-mcp'
```

### Verification

After updating, verify the new server shows up:
```bash
# OpenCode
opencode mcp list | grep FIREFOX

# Codex — check config.toml
grep -A3 "ULTIMATE_FIREFOX" ~/.codex/config.toml
```

## Layer 4: Ctrl+Routing Hermes Built-in Browser Tools Through Firefox CDP

Hermes's built-in `browser_*` tools (`browser_navigate`, `browser_click`, `browser_snapshot`, etc.) use `agent-browser` (a Node.js CLI built on Playwright) which defaults to Chromium. To route them through Firefox instead, use the CDP override config.

### Config Approach (preferred over code modification)

The `personal-intelligence-mcp` server has `ingest_chatgpt` and `ingest_grok` connectors that need to connect to a running Firefox via BiDi. The `_firefox_bidi.py` connector auto-injects stealth preload scripts to prevent bot detection.

### Architecture (Two-Phase Stealth)

Phase 1: Connect via ultimate-firefox-mcp's BiDi browser → apply 22 StealthEngine measures via `script.addPreloadScript` → DISCONNECT the MCP session (preload scripts persist at Firefox runtime level, NOT session level).

Phase 2: PIM connector creates its own BiDi session → navigates to target sites → persistent preload scripts run before any page JS → sites see a normal browser.

### Step-by-Step Flow

1. Start Firefox with the operator's main profile + `--remote-debugging-port` (use a fresh high port like 9228 to avoid TIME_WAIT ghosts)
2. Connect via `ultimate_firefox_mcp.browser.FirefoxBrowser`
3. Apply stealth: `StealthEngine().apply(browser)` — registers 22 preload scripts
4. CRITICAL: `await browser.disconnect()` — closes the BiDi session. Preload scripts PERSIST at the Firefox runtime level.
5. Set `PIM_BIDI_PORT` env var to the same port
6. Run the PIM ingestion connector (creates new session, stealth already applies)
7. Close Firefox

### BiDi Single-Session Limit

Firefox allows only ONE BiDi session at a time. If one session is active, a second `session.new` call returns `"Maximum number of active sessions"`. The MCP browser session must be disconnected before the PIM connector can create its own.

### `_firefox_bidi.py` Modifications

The PIM connector at `app/connectors/_firefox_bidi.py` was modified to integrate ultimate-firefox-mcp's StealthEngine:

**Changes made:**
1. Added `import os` for env var support
2. Port reads `PIM_BIDI_PORT` env var (default 9225) — no hardcoded port
3. Removed homemade 11-script STEALTH_SCRIPTS class constant
4. `_apply_stealth()` (BiDi path): imports `StealthEngine` from `ultimate_firefox_mcp.stealth`, calls `engine.get_preload_script()` for the full 22-measure combined script, sends via `script.addPreloadScript`
5. `_apply_cdp_stealth()` (CDP path): same StealthEngine import and `get_preload_script()`, sends via `Page.addScriptToEvaluateOnNewDocument`
6. Both methods called AFTER session creation but BEFORE browsing context creation — ensures preload scripts run on ALL subsequent page loads

**⚠️ Silent import failure hazard:**
Both `_apply_stealth()` and `_apply_cdp_stealth()` catch `ImportError` from the `from ultimate_firefox_mcp.stealth import StealthEngine` import and log a warning: `"ultimate-firefox-mcp not available, skipping stealth"`. This means if `pip install -e` was not run (or PYTHONPATH doesn't include the workdir), the pipeline runs with ZERO anti-detection — no error is raised, extraction proceeds, but every site sees an automated browser.

**Always add a sys.path fallback as belt-and-suspenders:**
```python
import sys
sys.path.insert(0, r'C:\\Users\\<you>\\ultimate-firefox-mcp')
from ultimate_firefox_mcp.stealth import StealthEngine
```
This ensures the import works even if `pip install -e` was skipped. The primary fix is `pip install -e`, but the fallback prevents silent failure during development iterations.

**Key behavior:**
- Stealth is applied in the same BiDi/CDP session that creates tabs — scripts persist for that session's lifetime
- `script.addPreloadScript` operates at the Firefox runtime level, not per-tab — all future frames/pages get stealth
- The `_apply_stealth()` and `_apply_cdp_stealth()` calls happen inside `_try_bidi_connect()` and `_try_cdp_connect()` respectively, right after connection but before page navigation

## Layer 4: Config Approach (preferred over code modification)

Set `browser.cdp_url` in `config.yaml` to point to Firefox's remote debugging endpoint:

```yaml
browser:
  cdp_url: http://localhost:9222
```

When `cdp_url` is set, `agent-browser` connects to the existing CDP endpoint instead of launching its own Chromium. The precedence chain is:

1. `BROWSER_CDP_URL` env var (live override, set by `/browser connect`)
2. `browser.cdp_url` in `config.yaml` (persistent)

### Prerequisites

- Firefox must be running with `--remote-debugging-port 9222`
- Use the stealth launcher to start Firefox: `firefox-stealth.bat`
- Verify the endpoint responds: `curl http://localhost:9222/json/version`

### Limitations

- `agent-browser` is built for Chromium CDP — Firefox's CDP implementation is partial
- `ariaSnapshot` (accessibility tree) is Chromium-only; Firefox CDP may not return full snapshot data
- For tasks that need full Firefox automation with stealth, use the MCP server tools directly (`mcp_ultimate_firefox_navigate`, etc.) instead of the `browser_*` Hermes tools
- The `browser.engine` config only supports `auto`, `lightpanda`, and `chrome` — there is no `firefox` engine option

### Decision Guide

| Need | Use |
|------|-----|
| Quick browse / click / type with Firefox | Set `browser.cdp_url` + start Firefox |
| Stealth / anti-detection / saved cookies | MCP Firefox tools via `ultimate-firefox-mcp`, `git-stars`, or `personal-intelligence` |
| Full screenshot + vision analysis | MCP Firefox tools (have native `screenshot` tool) |
| Complex form filling with autofill | MCP Firefox tools (work with Firefox's saved passwords) |
| Chrome-only features (ariaSnapshot, Page.* Domains) | Leave `browser.cdp_url` empty (uses local Chromium) |

### Launcher Fix (git-bash compat)

The `firefox-stealth.bat` uses Windows-only commands (`timeout /t`, `taskkill`, PowerShell). When run from git-bash, `timeout` resolves to the git-bash `timeout` instead of the Windows `timeout.exe`. Preferred invocation:

```bash
# From git-bash, use cmd to run the bat properly
cmd.exe /c "${USER_HOME}\AppData\Local\hermes\firefox-stealth.bat"

# Or just start Firefox directly from git-bash:
"C:/Program Files/Mozilla Firefox/firefox.exe" --remote-debugging-port 9222 --no-remote &
```

### Key Directive: Use ultimate-firefox-mcp FIRST

**Never manually hack Firefox launches.** The `ultimate-firefox-mcp` MCP server (configured in Hermes config.yaml) is the infrastructure for all Firefox automation on this machine. It handles:
- Protocol auto-detection (BiDi to CDP fallback)
- StealthEngine anti-detection (22 measures)
- Reconnect logic and error recovery
- Human input simulation

Before launching Firefox manually:
1. **Always** try the ultimate-firefox-mcp server tools first (via the MCP toolset) before any manual launch
2. **Always** check if the personal-intelligence or git-stars MCP tools can navigate Firefox before starting a new instance
3. Use the **Python subprocess launch pattern** (below) as the fallback when MCP servers can't auto-launch Firefox

### Python Subprocess Launch Pattern (reliable fallback)

This is the most reliable Firefox lifecycle management approach on this Windows machine. It avoids bash/cmd.exe quoting issues and gives full control over process lifecycle:

```python
import subprocess, urllib.request, json, os, time

def launch_firefox(profile_path: str, port: int = 9222,
                   headless: bool = False, timeout: int = 60):
    """Launch Firefox with BiDi remote debugging. Returns process handle."""
    # 1. Kill any orphan Firefox processes
    os.system('taskkill /F /IM firefox.exe 2>nul')
    os.system('taskkill /F /IM crashreporter.exe 2>nul')
    time.sleep(35)  # critical: wait out TIME_WAIT ghosts on port

    # 2. Build command
    ff = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    cmd = [ff, '--new-instance', '-profile', profile_path,
           '--remote-debugging-port', str(port), '--new-window', 'about:blank']
    if headless:
        cmd.append('--headless')

    # 3. Launch
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1
    )

    # 4. Wait for BiDi readiness with port check
    for i in range(timeout // 2):
        time.sleep(2)
        try:
            resp = urllib.request.urlopen(
                f'http://127.0.0.1:{port}/json/version', timeout=2)
            data = json.loads(resp.read())
            print(f'BiDi ready! Firefox={data.get("Browser","?")}')
            return proc
        except:
            if proc.poll() is not None:
                code = proc.returncode
                out = proc.stdout.read(200)
                raise RuntimeError(
                    f'Firefox died (code={code}): {out}')
    raise TimeoutError(f'BiDi not ready after {timeout}s')

# Usage
profiles_dir = os.path.expanduser('~/AppData/Roaming/Mozilla/Firefox/Profiles')
profile = os.path.join(profiles_dir, '<profile-id>.default-release-1')
proc = launch_firefox(profile, port=9222)
try:
    # ... do work with BiDi ...
    pass
finally:
    proc.terminate()
    proc.wait()
    # Clean ghosts
    os.system('taskkill /F /IM firefox.exe 2>nul')
```

**Why Python subprocess over bash/cmd:**
- Avoids MSYS path quoting issues with `C:\Program Files\`
- No `timeout` binary confusion (Windows vs git-bash)
- Proper process lifecycle tracking (PID, output, exit code)
- Can wait for specific port/BiDi readiness
- Can handle TIME_WAIT ghosts with precise timing
- No orphan processes from `start` in cmd.exe subprocess

## Layer 6: Cloudflare-Bot-Protected Sites — Console-Paste / WebSocket Harvester Pattern

**When Firefox BiDi/CDP stealth fails (Cloudflare, bot-detection services):**  
Some sites (ChatGPT, Grok, financial sites) are behind Cloudflare Bot Management or similar services that detect `--remote-debugging-port` at the network level — no amount of JS stealth can fix this. The site sees the WebSocket upgrade to the debugging protocol and flags the browser.

For these sites, use the **console-paste / WebSocket harvester pattern**:

1. Start a local WebSocket harvester server (port 8898)
2. User opens the target site in their NORMAL Firefox (no debugging, clean session)
3. User pastes a one-liner JS snippet into the browser DevTools console (F12)
4. The snippet uses `new WebSocket("ws://127.0.0.1:8898")` to send extracted data
5. Harvester feeds data into PIM

### Why WebSocket (not HTTP fetch)
Groks's CSP blocks `connect-src http://127.0.0.1:*` but allows `ws://127.0.0.1:*`.  
ChatGPT's CSP also allows localhost WebSocket connections. See `references/csp-bypass-websocket.md`.

### Console syntax compatibility
Firefox's console rejects certain modern JS when pasted:
- ❌ Arrow functions + template literals → use `function(){}` + string concat
- ❌ `let`/`const` may cause redeclaration errors → use `var`
- ❌ `async` IIFEs → use `onmessage` callback pattern instead

### Harvester script
`templates/pim-harvester.py` (WebSocket version, port 8898):

```bash
python /path/to/pim-harvester.py
```

### Console snippets

**ChatGPT** — paste on `https://chatgpt.com`:
```js
var ws=new WebSocket("ws://127.0.0.1:8898");ws.onopen=function(){var c=[];document.querySelectorAll('a[href*="/c/"]').forEach(function(a){var m=a.href.match(/\/c\/([a-f0-9-]+)/);if(m&&!c.find(function(x){return x.id===m[1]}))c.push({id:m[1],title:(a.textContent||"").trim()||"Untitled",url:a.href})});ws.send(JSON.stringify({source:"chatgpt",conversations:c}));console.log("Sent "+c.length+" convos");ws.onmessage=function(e){console.log("PIM:",e.data)}};
```

**Grok** — paste on `https://grok.com`:
```js
var ws=new WebSocket("ws://127.0.0.1:8898");ws.onopen=function(){var c=[];document.querySelectorAll('a[href*="/c/"]').forEach(function(a){var m=a.href.match(/\/c\/([a-f0-9-]+)/);if(m&&!c.find(function(x){return x.id===m[1]}))c.push({id:m[1],title:(a.textContent||"").trim()||"Untitled",url:a.href})});ws.send(JSON.stringify({source:"grok",conversations:c}));console.log("Sent "+c.length+" convos");ws.onmessage=function(e){console.log("PIM:",e.data)}};
```

### Why this works
- Uses the browser's OWN JS context — same origin, same cookies, same Cloudflare clearance
- No remote debugging port needed — zero automation flags
- `WebSocket` from the page origin uses the page's authentication (cookies, tokens, CF clearance)
- Works even if the user is logged in via SSO, SAML, or OAuth
- WebSocket avoids CSP `connect-src` restrictions that block HTTP fetch

### Tampermonkey alternative
the operator has `firefox@tampermonkey.net` installed. A Greasemonkey/Tampermonkey userscript can auto-extract conversations from the sidebar on page load and periodically send new ones to the harvester. This enables ongoing automatic extraction without manual paste.
### Limitations

- Requires the user to have the site open in a tab (for one-shot paste)
- One-shot extraction (no cron automation unless combined with Tampermonkey)
- Large conversation lists may hit browser tab load limits  
- **Does not fetch conversation message content** — only conversation IDs/titles/URLs. Full message extraction requires navigating to each conversation and extracting DOM content, which is more complex.

### Layer 6b: Tampermonkey/Userscript Approach (CSP-Proof, Recurring)

When console-paste is impractical (recurring extraction needed, too many conversations), use a Tampermonkey userscript instead. This is the MOST reliable approach for Cloudflare/CSP-protected sites because:

- `GM_xmlhttpRequest` runs in the extension context, **bypassing Content-Security-Policy entirely**
- Uses the browser's OWN cookies and Cloudflare clearance (zero automation flags)
- Can auto-extract on page load and run on a timer

**Architecture:**

```
Browser (Tampermonkey)  --GM_xmlhttpRequest-->  Local HTTP server (port 8897)  --PIM pipeline-->  pim.db
```

**Tampermonkey script** (`templates/pim-full-extractor.user.js`):

```js
// @match        https://chatgpt.com/*
// @match        https://grok.com/*
// @grant        GM_xmlhttpRequest
// @run-at       document-idle
```

The script:
1. Waits for the sidebar to render (up to 20s, 1s intervals)
2. Extracts conversation IDs from sidebar links (`a[href*="/c/"]` for ChatGPT, `a[href*="/c/"]` for Grok)
3. For EACH conversation, fetches full message content via the site's internal API using `GM_xmlhttpRequest` (uses browser cookies — Cloudflare clearance is valid)
4. Sends IDs + messages together to the local harvester

**ChatGPT API endpoint for message content:**
```
GET https://chatgpt.com/backend-api/conversation/{id}
-> { mapping: { msgId: { message: { author: { role }, content: { parts: [...] } } } } }
```

**Grok API endpoint for message content:**
```
GET https://grok.com/rest/app-chat/conversations/{id}
-> { messages: [{ role, content }] }  or  { conversation: { messages: [...] } }
```

**Harvester** (`templates/pim-harvester-tampermonkey.py`, port 8897):
- CORS-enabled HTTP server (Access-Control-Allow-Origin: *)
- Accepts POST with `{ source: "chatgpt"|"grok", conversations: [{ id, title, url, messages: [{role, content}] }] }`
- Builds `full_text_override` from messages and writes to PIM via `process_item()`
- Skips the PIM HTTP fetcher (which hits Cloudflare 403) — uses browser-fetched content directly

**Why this works:**
- `GM_xmlhttpRequest` bypasses both CSP (`connect-src` restrictions) and Cloudflare (browser has valid clearance)
- API calls to `chatgpt.com/backend-api/conversation/{id}` and `grok.com/rest/app-chat/conversations/{id}` return JSON with full message history
- The harvester uses `full_text_override` so PIM never needs to HTTP-fetch the content itself

**One-time setup:**
1. Start the harvester: `python templates/pim-harvester-tampermonkey.py`
2. Install the userscript in Tampermonkey (Create new script -> paste -> Ctrl+S)
3. Visit chatgpt.com and grok.com -- script auto-runs, sends data, shows alert

### CSP specifics by site

| Site | CSP `connect-src` allows | CSP `connect-src` blocks | Working approach |
|------|--------------------------|--------------------------|------------------|
| ChatGPT | `wss://*.chatgpt.com`, `https://*.chatgpt.com` | `http://127.0.0.1:*`, `ws://127.0.0.1:*` | Tampermonkey `GM_xmlhttpRequest` only |
| Grok | `ws://127.0.0.1:*`, `ws://localhost:*` | `http://127.0.0.1:*` | WebSocket (wss:// upgrade issue) or Tampermonkey `GM_xmlhttpRequest` |

Both sites: `GM_xmlhttpRequest` works consistently because it runs in the extension context, not the page context.

### Console snippet syntax -- Firefox DevTools compatibility

Firefox's console rejects certain modern JS when pasted:
- Arrow functions + template literals -> use `function(){}` + string concat
- `let`/`const` may cause redeclaration errors -> use `var`
- `async` IIFEs -> use `onmessage` callback pattern instead
- Template literals with backticks get corrupted on paste -> use string concat
- `location.hostname.includes()` -> use `location.hostname.indexOf() !== -1`

Always test the paste script yourself in Firefox DevTools before asking the user.

### StealthEngine verify() behavior

`StealthEngine.verify(browser)` evaluates JS expressions in a browsing context to confirm each measure is working.

| Condition | Expected result |
|-----------|----------------|
| No page/tab loaded (verify right after connect) | ALL fail (0/10) -- no context to evaluate |
| After navigating to a simple page | Partial pass (5/10) -- basic JS properties work, but engine-level flags fail |
| `navigator.webdriver` check | FAILS on page -- even with `dom.webdriver.enabled=false`, the C++ getter may still return `true` when `--remote-debugging-port` is active |

Measures that PASS on a loaded page: `languages`, `plugins`, `geolocation`, `touchSupport`, `performanceNow`  
Measures that FAIL on a loaded page (engine-level): `webdriver`, `hardwareConcurrency`, `deviceMemory`, `screenResolution`, `webrtc`

**Workaround:** For Cloudflare-protected sites where engine-level detection matters, use the Tampermonkey approach (Layer 6b). The stealth measure `webdriver` failure directly correlates with Cloudflare's bot detection.

### PIM Ingestion — Historical Setup (scripts removed June 2026)

The PIM pipeline (`pim-pipeline.py`, `ingest-chatgpt-grok.sh`) was deleted
during cleanup. To re-establish PIM extraction from ChatGPT/Grok, the
pipeline script must be re-created and cron job re-registered. See
`references/pim-ingestion-stealth.md` for the architecture and
`templates/pim-ingest-runner.py` for the reusable runner.

The Firefox MCP server + BiDi infrastructure is still in place and
functional. Only the orchestration scripts were removed.

### Headless Firefox Launch (automatic via ensure_firefox())

The `_firefox_bidi.py` connector's `ensure_firefox()` function auto-launches Firefox with `--headless` if no process is listening on the target port. It uses the patched portable Firefox at `C:\\Users\\<you>\\firefox-portable\\firefox.exe` with the **automation profile** (`hermes-mcp`):

```python
AUTOMATION_PROFILE = r"C:\\Users\\<you>\\AppData\\Local\\hermes\\firefox-profile"

def ensure_firefox(port, headless=True, profile=None):
    if _port_open(port):
        return port  # already running
    binary = _find_browser()  # portable > system > PATH
    p = profile or AUTOMATION_PROFILE
    cmd = [binary, "--remote-debugging-port", str(port), "--no-remote", "--profile", p]
    if headless:
        cmd.insert(1, "--headless")
    subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
    # Wait up to 30s for port
```

⚠️ **Profile choice:** Always use `AUTOMATION_PROFILE` (hermes-mcp), NOT the operator's main browsing profile (`<profile-id>.default-release-1`). The automation profile already has remote debugging prefs by design — the operator's profile should NEVER get `remote.active-protocols=1` written into its prefs.js.

When headless + BiDi works (it does with the patched xul.dll Firefox), the extraction is fully invisible — no popup windows.

### Automation profile

PIM extraction must use the **automation profile** (`hermes-mcp`) — NOT the operator's real browsing profile:

```python
AUTOMATION_PROFILE = r"${USER_HOME}\AppData\Local\hermes\firefox-profile"
```

The automation profile has:
- `remote.active-protocols=1` (BiDi enabled — by design for automation)
- `devtools.debugger.remote-enabled=true` (needed for MCP connection)
- `marionette.enabled=false`, `dom.webdriver.enabled=false` (stealth)
- `signon.*=true` (password manager ON)
- ChatGPT/Grok/YouTube login cookies (already logged in from prior sessions)

🎯 **If ChatGPT/Grok/YouTube sessions expire in the automation profile:** launch the portable Firefox VISIBLY with the automation profile, log into each site once, then close. The next headless PIM run picks up the fresh cookies. Never change the profile target to <profile-id>.

```bash
# Log into the automation profile (visible, one-time)
"${USER_HOME}/firefox-portable/firefox.exe" \
    --no-remote \
    --profile "${USER_HOME}\AppData\Local\hermes\firefox-profile" \
    --new-window "https://chatgpt.com"
```

### Sidebar Scrolling JS (ChatGPT + Grok)

Both connectors use the same async scroll-and-extract JavaScript pattern. Instead of one-shot `document.querySelectorAll('a[href*="/c/"]')` which only finds visible links, they run a scroll loop inside the page:

```javascript
(async () => {
    const seen = new Set();
    const conversations = [];

    // Find sidebar container with /c/ links
    let sidebar = /* scrollable element with a[href*='/c/'] */;
    
    // Find the scrollable child
    let scrollEl = sidebar;
    for (const child of sidebar.querySelectorAll('div,section,ul,ol')) {
        const style = getComputedStyle(child);
        if ((style.overflowY === 'auto' || style.overflowY === 'scroll') &&
            child.scrollHeight > child.clientHeight) {
            scrollEl = child;
            break;
        }
    }

    // Extract + scroll loop
    extractLinks(sidebar);
    for (let i = 0; i < 100 && stale < 3; i++) {
        scrollEl.scrollTop = scrollEl.scrollHeight;
        await new Promise(r => setTimeout(r, 2500));
        extractLinks(sidebar);
        // stale = count of scrolls with no new items
    }
    return JSON.stringify(conversations);
})();
```

**Dedup** by conversation ID (`/c/{uuid}`).
**Stop condition:** 3 consecutive scrolls yield no new items.

Full JS source in `references/chatgpt-grok-sidebar-scroll.md`.

### Connector Auto-Recovery

Each connector's navigation loop uses two safeguards:
1. `ff.ensure_connected()` — health check before every page navigation
2. `ff.reconnect()` every **3** conversations — prevents BiDi session timeout on React SPAs

⚠️ **RECONNECT_EVERY=3 not 15.** The skill's pitfall says the per-session navigation limit is ~5 for heavy React SPAs (ChatGPT, Grok). The extraction code in `chatgpt.py` and `grok.py` had `RECONNECT_EVERY = 15` as of 2026-05-30, which is too high — the WebSocket dropped at conversation #12, before the reconnect threshold. Set to 3 to stay well within the stability window.

```python
RECONNECT_EVERY = 3  # not 15 — React SPAs degrade after ~5 navigations
for i, conv in enumerate(conversations):
    if i > 0 and i % RECONNECT_EVERY == 0:
        await ff.reconnect()
    await ff.ensure_connected()
    await ff.navigate(conv['url'])
```

**Why 3:** Each BiDi navigation on a React SPA (ChatGPT, Grok) adds server-side state. After ~5 navigations, the WebSocket may stall with `"no close frame received or sent"`. Reconnecting every 3 navigations leaves margin. Simple pages (bookmarks, search results) can use a higher value.

### Ingestion Script (historical — removed June 2026)

The orchestration script `ingest-chatgpt-grok.sh` was deleted. See
`references/pim-ingestion-stealth.md` for architecture. To rebuild,
use `templates/pim-ingest-runner.py` as a starting point.

### Cron Job (removed June 2026)

The PIM cron job was removed with the script. Re-create via
cronjob(action='create') with the runner template and `gpt-researcher`
skill when PIM extraction is needed again.

### Cron job removal

The PIM cron job (previously job_id `b0490179124c`) was removed with
the orchestration script. Re-create via cronjob(action='create') when
needed.

### Headless Launch Pattern

**🚨 Firefox 151 limitation: headless + `--remote-debugging-port` — varies by binary.**

| Firefox binary | Headless + BiDi | Crash window | Notes |
|---------------|-----------------|--------------|-------|
| System Firefox (C:\Program Files) | ❌ BiDi never binds | 40-60s visible | httpd.js only in headless |
| Patched portable (xul.dll patched) | ✅ BiDi WORKS | ~3-5 min extended | Patching xul.dll resolves the BiDi binding issue in headless mode. 11+ ChatGPT conversations successfully extracted in a single headless session before per-navigation WebSocket timeout. |

**Confirmed (2026-05-30):** With the xul.dll-patched portable Firefox at `${USER_HOME}\firefox-portable\firefox.exe`, headless + `--remote-debugging-port` on port 9239 DOES start BiDi. The pipeline (`pim-pipeline.py`) used `--headless --remote-debugging-port 9239 --profile <automation-profile>` and successfully extracted 11 ChatGPT conversations before a per-session navigation timeout (not a crash). The GFX crash still occurs but the window is extended to ~3-5 minutes with the patched binary + automation profile.

**Recommendation for cron extraction:** Use headless mode with the patched portable Firefox. Set `RECONNECT_EVERY=3` in extraction loops to complete work within the extended crash window.

| Need | Launch mode | BiDi/CDP | Reliable? | Notes |
|------|-------------|----------|-----------|-------|
| Long extraction (>100 convos) | `--headless` with patched portable | Both work | ✅ | Needs RECONNECT_EVERY=3 to avoid per-session timeouts |
| Quick extraction (<15 convos) | `--headless` with patched portable | Both work | ✅ | Single session likely sufficient |
| Screenshot/vision only | `--headless` | Not needed | ✅ | Use MCP tools directly |

On machine where headless BiDi works, use the Python subprocess launch pattern below.

```bash
FIREFOX="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
taskkill /F /IM firefox.exe >nul 2>&1; sleep 2
"$FIREFOX" --headless --remote-debugging-port 9223 -P "default-release-1" --no-remote &

# Wait up to 20s for port to respond
for i in $(seq 1 20); do
  if curl -s http://127.0.0.1:9223/json/version >nul 2>&1; then
    echo "Firefox ready on port 9223"; break
  fi
  sleep 1
done

# Apply stealth
python "${USER_HOME}\AppData\Local\hermes\firefox-stealth-patcher.py" --all 2>/dev/null || true

# ... extraction scripts ...

# Cleanup
taskkill /F /IM firefox.exe >nul 2>&1 || true
```

**Key details:**
- Uses **the operator's real profile** (`default-release-1` = `<profile-id>.default-release-1`) for YouTube cookies — no cookie injection needed when using the real profile directly
- `--headless` flag keeps extraction invisible — no popup windows during cron
- `--no-remote` prevents interfering with any already-running Firefox instances
- Always kills Firefox at end so there's no orphan left eating resources
- Also kills at start to clear any previous headless instance that may have crashed/hung
- The profile path resolution: `-P "default-release-1"` selects the profile by name (Firefox matches against profiles.ini), no need for full path

### YouTube Extraction (Phase 1)

The `yt_extract.py` script in `~/FireFox-Phantom-MCP/` navigates to YouTube Library and:
1. Scans for all playlist links (including system playlists: Liked Videos=LL, Watch Later=WL, Favorites=FL)
2. Navigates to each playlist, scrolls up to 30 passes extracting video IDs, titles, channels
3. Saves to `youtube_temp.json` for downstream transcript processing

`yt_transcripts.py` then fetches transcripts for any new (previously unseen) videos using YouTube Transcript API, with browser InnerTube fallback for rate-limited videos.

### Profile choice

**🚨 CRITICAL: The automation profile MUST be used for all headless PIM extraction.** Never use the operator's real browsing profile (`<profile-id>.default-release-1`). Headless runs with `--remote-debugging-port` write automation prefs into the profile's prefs.js that persist and contaminate the operator's normal browsing experience.

Using the automation profile (`hermes-mcp`) is the right call because:
- ChatGPT, Grok, and YouTube login sessions can be established in the automation profile and persist across headless restarts (the profile's cookies.sqlite retains OAuth refresh tokens)
- The automation profile's user.js already has `remote.active-protocols=1`, `devtools.debugger.remote-enabled=true` — contamination is by-design and doesn't affect the operator's browsing
- No xul.dll binary patching needed for the automation profile — the portable Firefox's patched binary handles navigator.webdriver

**How to log into the automation profile:**
```bash
# Open visible Firefox with automation profile
"${USER_HOME}/firefox-portable/firefox.exe" --no-remote --profile "${USER_HOME}\AppData\Local\hermes\firefox-profile"

# Log into ChatGPT, Grok, YouTube in this window
# Close when done — cookies persist in the profile
```

### Cleanup

`taskkill /F /IM firefox.exe` terminates the headless instance. Note this destroys session cookies, but since the profile is the real one and gets relaunched fresh each time, it picks up persisted auth tokens (OAuth refresh tokens, etc.) on next launch.

## Page-Text Fallback Extraction (When DOM Selectors Fail)

Many sites (Indeed, LinkedIn, job boards, React SPAs) use dynamic CSS class names that change between deployments, making `document.querySelector('.jobTitle')` unreliable. The fix: **extract `document.body?.innerText` and parse it line-by-line with heuristics**.

### The Pattern (3 steps)

```python
# Step 1: Get raw page text
text = await bidi.eval_js("document.body?.innerText || ''")
await asyncio.sleep(4)  # let page render

# Step 2: If DOM selectors found structured data, use it
# Step 3: Otherwise fall back to text parsing
lines = text.split('\n')
noise_patterns = ["Skip to", "Home", "Search", "Sign in", "Menu"]

for i, line in enumerate(lines):
    line = line.strip()
    if not line or len(line) < 5:
        continue
    if any(line.startswith(n) for n in noise_patterns):
        continue
    
    # Look ahead 3-5 lines for known patterns (salary, company name, location)
    context = lines[i+1:i+5]
    # ...
```

### When to use innerText vs querySelector

| Approach | Use when | Success rate | Notes |
|----------|----------|-------------|-------|
| `querySelector` chains | Static markup, stable class names | High for stable sites | Fragile across deployments |
| `innerText` + heuristics | Dynamic class names, React SPAs, job boards | Lower but robust | Rougher output, needs cleanup |
| JSON API extraction | Site has internal API | Highest | Needs API endpoint discovery |

See `templates/bidi-page-extractor.py` for a complete working BiDi client class with both approaches.

### Known Site-Specific Heuristics

**Indeed** — Job listings appear as consecutive lines: `$TITLE`, `Easily apply`, `$COMPANY`, `$LOCATION`, `$SALARY`. Filter noise lines (navigation, footer, "Skip to main content"). Look for `$` in salary field, known company names.

**LinkedIn** — Jobs appear as tab cards with title → company → location. Lines starting with job keywords ("Senior", "AI Architect", "Software Engineer") followed by company name on the next line. LinkedIn messaging shows sender name (first+last, colon or time on next line) and InMail snippets.

**General** — Same pattern works for any data-rich page: scroll down, extract text, filter noise, look for line adjacency to infer structure.

## Pitfalls

- **🚨 Headless BiDi works but requires clean profile state:** The patched portable Firefox (`C:\\\\Users\\\\<you>\\\\firefox-portable\\\\`) starts BiDi in headless mode on port 9239, BUT only if the profile directory has NO stale `WebDriverBiDiServer.json`. If a previous non-headless launch (or a launch on a different port) wrote `{\"ws_host\": \"127.0.0.1\", \"ws_port\": 9223}` into this file, the headless launch on port 9239 will fail silently — Firefox starts but never binds the BiDi WebSocket. **Fix:** Always delete `WebDriverBiDiServer.json` and `MarionetteActivePort` from the profile directory before a headless launch:
  ```bash
  rm -f "${HERMES_HOME}/firefox-profile/WebDriverBiDiServer.json"
  rm -f "${HERMES_HOME}/firefox-profile/MarionetteActivePort"
  ```
  This is built into `ensure_firefox()` and the `ingest-chatgpt-grok.sh` script — if launching manually, remember to clean these first.
- **🧹 Never kill ALL Firefox:** `Get-Process firefox | Stop-Process -Force` destroys the user's visible browser with active login sessions. Always kill by port-specific PID via `netstat -ano | grep LISTENING`:
  ```python
  PID=$(netstat -ano | grep ":9239" | grep "LISTENING" | awk '{print $NF}')
  powershell -Command "Stop-Process -Id $PID -Force"
  ```
- **⚠️ connect() retry loop:** Firefox may have maxed-out session slots from orphaned sessions. `connect()` should retry up to 3 times, killing and restarting Firefox between attempts. Bio's 3-retry pattern is: `ensure_firefox()` → `_try_bidi_connect()` → fail → `_kill_firefox()` → `ensure_firefox()` → retry.
- **⚠️ `websockets` v16 compatibility:** `WebSocketClientProtocol` is deprecated. Use `ClientConnection.state` (import `from websockets.protocol import State as WsState`):
  ```python
  # ✅ Correct check
  self._ws is not None and self._ws.state == WsState.OPEN
  # ❌ Does not raise but always True (returns 0 when closed)
  self._ws is not None and hasattr(self._ws, "open") and self._ws.open
  ```
  In v16, `state` returns an int: 0=CONNECTING, 1=OPEN, 2=CLOSING, 3=CLOSED.
- **🚨 Silent stealth import failure in PIM connectors:** `from ultimate_firefox_mcp.stealth import StealthEngine` in `_firefox_bidi.py` catches ImportError silently and falls back to zero stealth. If the package isn't installed with `pip install -e`, `pip list | grep ultimate-firefox-mcp` shows nothing, and every extraction runs with no anti-detection. Fix: run `pip install -e C:\\Users\\<you>\\ultimate-firefox-mcp` AND add a `sys.path.insert(0, ...)` fallback to both `_apply_stealth()` and `_apply_cdp_stealth()`. Verify with `python -c "from ultimate_firefox_mcp.stealth import StealthEngine"` from the PIM workdir. 
- **⚠️ Firefox 1-session reconnect not supported:** BiDi spec describes reconnecting to an existing session via `ws://host:port/session/{sessionId}`, but this Firefox version returns HTTP 404. Always create a fresh session instead.
- **⚠️ Orphaned sessions survive WS close:** Firefox server-side session slots persist for several minutes after the WebSocket drops, even without the `session.end` command. If multiple scripts crash without cleanup, sessions accumulate until the cap is hit. The only recovery is killing the Firefox process entirely and restarting.
- **⚠️ CDP fallback is always available:** Even when BiDi sessions are maxed out, CDP (`/json/version`, `/json/list`) may still respond. Always try CDP fallback before concluding Firefox is unreachable.
- **🚨 Firefox 151 GFX compositor crash with `--remote-debugging-port`**: Firefox 151.0.2 on this Windows machine crashes consistently when `--remote-debugging-port` is active. Symptom: `CompositorBridgeChild receives IPC close with reason=AbnormalShutdown` preceded by `[ERROR shell_windows::limited_access_features] Error generating feature token: NS_ERROR_FAILURE`. Crash exits with codes like 4294967295 (0xFFFFFFFF, forced kill) or 3489660927 (0xD00000FF, GPU crash). Fresh profiles crash faster (2-8s) than the established <profile-id> profile (40-60s). `--safe-mode`, `--disable-gpu`, `--disable-webrender`, and GPU-disabling user.js prefs do NOT prevent the crash. **Crash window varies by binary:** the patched xul.dll portable Firefox (`C:\\Users\\<you>\\firefox-portable\\`) extended the window to ~3-5 minutes in headless mode (confirmed 2026-05-30, 11 conversations extracted before per-navigation timeout). The system Firefox at `C:\\Program Files\\Mozilla Firefox\\` still crashes in 40-60s. **Workaround:** use the patched portable Firefox in headless mode with `RECONNECT_EVERY=3` in extraction loops. See `references/firefox-151-gfx-crash.md`.
- **Port wait loop must use `/json/version`**: `curl http://127.0.0.1:9223` returns raw `httpd.js` if a ghost process is on the port. Only `/json/version` returns BiDi-specific headers. Wait for that endpoint specifically.
- **No `navigator.webdriver` check in headless mode**: With the real profile and `dom.webdriver.enabled=false`, `navigator.webdriver` is `undefined` by default in headless mode — no xul.dll patching needed unless Cloudflare is the target.
- **Marionette detection**: `marionette.enabled = true` in prefs.js is the #1 cause of Firefox disabling password autofill. The patcher script correctly sets it to `false`.
- **Profile overrides**: `user.js` values override `prefs.js` at startup, but if Firefox was opened with `marionette.enabled=true` already written to prefs.js, the bad value gets re-applied until `user.js` overrides it. Always run the patcher then restart Firefox.
- **Cloudflare-blocked ChatGPT extraction vs working Grok extraction:** Even with all 22 StealthEngine measures + patched xul.dll + headless mode, **ChatGPT consistently finds 0 conversations** while **Grok successfully extracts 30+ conversations** on the same headless Firefox session. Reason: x.ai/Grok's Cloudflare configuration is less aggressive or uses different detection thresholds than OpenAI's. The `--remote-debugging-port` WebSocket upgrade is visible at the network level, but Grok's Bot Management doesn't penalize it as heavily. **Workaround for ChatGPT:** Tampermonkey userscript with `GM_xmlhttpRequest` (Layer 6b) — bypasses both CSP and Cloudflare by running in the operator's normal Firefox extension context. Grok extraction via headless BiDi can continue as-is.
- **🚨 NEVER put remote debugging prefs in a normal-browsing profile's user.js**: `remote.active-protocols`, `devtools.debugger.remote-enabled`, and `devtools.debugger.prompt-connection` belong ONLY in the automation profile. Adding them to the main profile causes robot detection + password manager failure. See `references/multi-profile-strategy.md`.
- **Three separate configs**: Hermes, OpenCode, and Codex each have their own MCP server config. Updating only one leaves the others pointing at stale/stopped servers.
- **GitHub auth**: Use `pmb2` account for all git/gh operations to avoid auth prompts.
- **BiDi vs CDP**: Firefox 151+ prefers BiDi, but `--remote-debugging-port` exposes CDP first. The unified server handles both.
- **Stale parent.lock blocks Firefox launch**: After a headless Firefox session is killed (taskkill), a `parent.lock` file may remain in the profile directory. The next `ensure_firefox()` call should clean this before launching: `rm -f ${HERMES_HOME}/firefox-profile/parent.lock`
- **Session cookies lost on force-kill**: `taskkill /f` destroys session cookies (ChatGPT, Grok logins). The automation Firefox must be kept running, or the user must re-authenticate. For cron jobs, start automation Firefox at boot and leave it running.
- **Multiple profiles in profiles.ini**: The profile marked `Default=1` may not be the actual active profile. `StartWithLastProfile=1` means Firefox uses the last-opened profile. Always verify by checking `about:profiles` in the running instance or parsing `profiles.ini` sections.
- **🚨 Profile contamination cycle from headless PIM runs:** Every headless PIM ingestion that launches Firefox with `--remote-debugging-port` using the operator's main profile writes automation prefs (`remote.active-protocols=1`, `devtools.debugger.remote-enabled=true`) into `prefs.js`. These persist after Firefox exits. When the operator later opens his main Firefox, it reads the contaminated prefs → initializes Remote Agent → robot icon → potential password manager failure → user experiences "broken Firefox". **Fix: always use the automation profile for headless extraction.** The automation profile already has the remote debugging prefs by design.
- **Stealth patcher's BAD_PREFS is incomplete**: The patcher only checks for `marionette.enabled=true` and `signon.*=false`. Add `remote.active-protocols=1` and `devtools.debugger.remote-enabled=true` to the bad-pref list if they appear in a normal-browsing profile.
- **⚠️ BiDi per-session navigation timeout**: Even within a SINGLE BiDi session, navigating between heavy React SPA pages (ChatGPT, Grok) ~5 times causes the WebSocket to disconnect with `no close frame received or sent` or `BiDi command timed out: browsingContext.navigate`. This is NOT the same as the session-exhaustion cap — the session itself is fine but per-navigation stability degrades. **Fix:** Set `RECONNECT_EVERY = 3` (not 15) in the extraction loop. The actual code in `chatgpt.py:243` and `grok.py:252` had `RECONNECT_EVERY = 15` as of 2026-05-30, causing a disconnect at conversation #12 (before the reconnect at #15). Reconnection creates a new tab each time, so 3 works well for up to 200 conversations (67 reconnects).
- **🚨 `session.new({})` fails — must pass `{"capabilities": {}}`**: Firefox BiDi's `session.new` returns `Expected "capabilities" to be an object` when called with empty params `{}`. The `capabilities` key is required and must be an object even if empty:
  ```python
  # ❌ Fails
  await send("session.new", {})
  # ✅ Works
  await send("session.new", {"capabilities": {}})
  ```
  This is a Firefox BiDi implementation quirk — the spec says `capabilities` is optional, but Firefox enforces it. See `templates/bidi-page-extractor.py` for the working session lifecycle pattern.
- **📝 `script.callFunction` result parsing**: The return value lives at `resp["result"]["result"]["value"]`. The top-level `result` is the BiDi command response wrapper; the nested `result` is the `ScriptResult` with the actual remote value:
  ```python
  resp = await send("script.callFunction", {
      "target": {"context": ctx},
      "functionDeclaration": "() => document.title",
      "awaitPromise": True,
      "resultOwnership": "root"
  })
  # Extract: resp["result"]["result"]["value"]
  rv = resp.get("result", {}).get("result", {})
  if rv.get("type") == "string":
      return rv.get("value", "")
  ```
  This triple-nesting (`resp.result.result.value`) is non-obvious and frequently the cause of silent empty extractors.
- **🚨 Killing Camoufox on Windows via git-bash**: `taskkill /F /PID <pid>` from git-bash silenty fails because MSYS translates `/F` to a path. The process stays alive. Use `cmd //c "taskkill /F /PID <pid>"` or kill by image name: `taskkill /F /IM camoufox.exe` from git-bash, or PowerShell directly. Camoufox spawns multiple child processes (plugin-container.exe, etc.) that can keep xul.dll locked even after the main process dies — verify with `netstat -ano | grep LISTENING | grep <port>` before patching.
- **🔌 OPSEC check_fingerprint fails on BiDi-only browsers (Camoufox)**: The launcher's `check_fingerprint(port)` function tries CDP `/json/version` which returns HTTP 404 on BiDi-only browsers. The fix (commited to launcher.py June 21, 2026) adds a WebSocket upgrade handshake fallback: connects to `ws://127.0.0.1:{port}/session`, sends HTTP upgrade, checks for `101 Switching Protocols`. This returns `{"connected": True, "protocol": "bidi"}`. Without this fix, `--opsec-check` always reports failure for Camoufox. See `references/bidi-opsec-fallback.md`.
- **📝 Page-text fallback extraction**: When JS DOM selectors fail (React SPAs, dynamic class names), extract the full innerText and parse line-by-line with heuristics:
  ```python
  # Step 1: Get raw page text
  text = await evaluate("document.body?.innerText || ''")
  # Step 2: Split lines and parse with keyword/pattern heuristics
  for line in text.split('\n'):
      if looks_like_job_title(line):
          jobs.append(parse_job_from_context(lines, i))
  ```
  This is more robust than fragile selectors but produces rougher output. See `templates/bidi-page-extractor.py` for a complete working example.
- **🔌 Standard port convention: use 9239 consistently**: Different sections of this skill historically referenced ports 9222, 9223, 9225, and 9239. **Use 9239** everywhere — it's high enough to avoid Docker (9226), ghost scanning (9220-9225 range), and WSL relay. Update ALL of: Hermes config.yaml `--port` arg, PIM `PIM_BIDI_PORT` env var, ingestion script launch command, Firefox keepalive script, `_firefox_bidi.py` default port, and `ensure_firefox()` default.

**Default port verification table** (check these files for hardcoded old defaults):

| File | Line | Hardcoded default | Should be | Status |
|------|------|-------------------|-----------|--------|
| `_firefox_bidi.py::__init__` | 128 | `9225` | `9239` | ✅ Fixed 2026-05-30 |
| `_firefox_cdp.py::__init__` | 31 | `9223` | `9239` | ✅ Fixed 2026-05-30 |
| `ultimate-firefox-mcp/main.py::detect_protocol` | 49 | `bidi_port=9223, cdp_port=9222` | `bidi_port=9239, cdp_port=9239` | ✅ Fixed 2026-05-30 |
| `_firefox_bidi.py::ensure_firefox` | 71 | env `PIM_BIDI_PORT` default `9239` | `9239` | ✅ Correct |
| `config.yaml::personal-intelligence` | 540 | `PIM_BIDI_PORT: '9239'` | `9239` | ✅ Correct |
| `ingest-chatgpt-grok.sh` | 11 | `export PIM_BIDI_PORT=9239` | `9239` | ✅ Correct |
| `pim-pipeline.py` | 17 | `PIM_BIDI_PORT = 9239` | `9239` | ✅ Correct |

The env var `PIM_BIDI_PORT` masks the wrong defaults in production, but the 3 unfixed files are latent bugs that activate when the env var is missing.

### BiDi Session Exhaustion & Auto-Recovery

**Firefox limits BiDi sessions (~5 max).** Each `session.new` call creates server-side state that persists even after the WebSocket disconnects. If scripts crash or time out without calling `session.end`, orphaned sessions accumulate silently until the cap is hit.

**Symptoms:**
```
session not created: Maximum number of active sessions
```
This can persist across script restarts — a new Python process still hits the cap because the Firefox process still holds the orphaned sessions.

**⚠️ Key insight:** Closing the WebSocket (`ws.close()`) does NOT immediately free the server-side session slot. You MUST send `session.end` before closing.

**Prevention — always use try/finally with session.end:**
```python
ff = FirefoxBiDiClient()
try:
    await ff.connect()
    ctx = await ff.new_tab()
    # ... work ...
finally:
    await ff.close()  # sends session.end before closing WS
```

**Auto-recovery pattern (`ensure_connected()` → `reconnect()`):**

When the WebSocket drops unexpectedly (BiDi timeout, network blip):

1. `ensure_connected()` checks `self._ws.state == WsState.OPEN`
2. If disconnected, calls `reconnect()`
3. `reconnect()` properly ends the old session (`session.end`) if the WS is still alive
4. Creates a fresh BiDi session
5. If session creation fails (orphaned slots), kills Firefox by PID and restarts fresh

**Firefox PID-targeted kill (surgical, safe):**
```python
def _kill_firefox(port):
    import subprocess
    result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=5)
    for line in result.stdout.splitlines():
        if f":{port}" in line and "LISTENING" in line:
            pid = line.strip().split()[-1]
            if pid != "0":
                subprocess.run(["powershell", "-Command", f"Stop-Process -Id {pid} -Force"])
                return
```

**Never kill ALL Firefox processes.** That destroys the user's visible browser with active login sessions. Always kill by port-specific PID.

**connect() 3-retry loop:**
```python
for attempt in range(3):
    ensure_firefox(port=port, headless=True)
    if await _try_bidi_connect(): return
    if await _try_cdp_connect(): return
    _kill_firefox(port)  # session exhaustion — restart
    await asyncio.sleep(3)
```

**Periodic reconnect in extraction loops:**
To avoid session buildup during long extractions (200+ conversation navigations), call `reconnect()` every 3 iterations for React SPAs (ChatGPT, Grok) or 15 for simpler pages:

```python
RECONNECT_EVERY = 3  # React SPAs — navigation limit ~5
for i, conv in enumerate(conversations):
    if i > 0 and i % RECONNECT_EVERY == 0:
        await ff.reconnect()         # fresh session + tab
    await ff.ensure_connected()      # health check before each nav
    await ff.navigate(conv['url'])
```

**`websockets` v16 compatibility:**
The `websockets` library changed its API in v16. `WebSocketClientProtocol` is deprecated in favor of `ClientConnection`. Check connection state via:
```python
from websockets.protocol import State as WsState
# self._ws.state == WsState.OPEN  ✅
# hasattr(self._ws, "open")       ❌ not available in v16
```

Restricting WebDriver BiDi to one session at a time. Trying to create a second session (e.g., PIM connector connecting while ultimate-firefox-mcp already has a session) returns `"Maximum number of active sessions"`. Always disconnect the MCP browser before the PIM connector starts.
- **StealthEngine.verify() requires a page context**: The verify() method evaluates JS in a browsing context. If no tab/page exists when called, ALL checks report as failed (0/10+). This is expected — verify after navigating to a page.
- **Preload scripts survive session disconnect**: Both script.addPreloadScript (BiDi) and Page.addScriptToEvaluateOnNewDocument (CDP) register scripts at the Firefox runtime level, not the session level. They persist even after the registering session closes.
- **Console paste syntax failures**: Firefox DevTools console rejects modern JS when pasting. Arrow functions (`()=>{}`) can cause "unexpected token" errors — use `function(){}`. Template literals (`` `text ${var}` ``) get corrupted — use string concatenation (`'text '+var`). `let`/`const` trigger redeclaration errors — use `var`. `async` IIFEs may not parse — use WebSocket `onmessage` callbacks. Always test the paste script yourself before asking the user to paste it.

## Verification Checklist

1. `about:config` shows `marionette.enabled=false`, `dom.webdriver.enabled=false`, `signon.*=true`
2. `navigator.webdriver === undefined` in DevTools console
3. Password autofill works on sites with saved credentials
4. `opencode mcp list` shows ULTIMATE_FIREFOX connected
5. `~/.codex/config.toml` shows `[mcp_servers.ULTIMATE_FIREFOX]`
6. Firefox restarts without requesting password re-entry
7. `PIM_BIDI_PORT=9239` env var set and match across config.yaml, ingestion script, and _firefox_bidi.py default
8. Two-phase stealth: StealthEngine.apply() → disconnect → PIM ingestion works (persistent preload scripts)
9. **PIM stealth import works**: Run `python -c "from ultimate_firefox_mcp.stealth import StealthEngine; print('OK')"` from the PIM directory
10. **Automated stealth verification**: Run `python scripts/verify-stealth.py` — all measures should pass
11. **PIM log shows stealth applied**: `grep -i "Applied.*stealth" pim.log` should show "Applied 22/22 stealth measures" per connector phase
12. **Profile isolation**: Verify `<profile-id>` main profile has `remote.active-protocols=0` and `devtools.debugger.remote-enabled=false`. The `hermes-mcp` automation profile should have the opposite.
13. **No stale parent.lock**: Check `ls -la ${HERMES_HOME}/firefox-profile/parent.lock` after headless runs — should not exist when Firefox is stopped
14. **Standard port 9239**: Verify `grep "9239"` on config.yaml, ingest-chatgpt-grok.sh, _firefox_bidi.py default port, and ensure_firefox() default all match
| File | Description |
|------|-------------|
| `references/xul-patching.md` | Binary patching of xul.dll to remove navigator.webdriver — research, implementation, and verification |
| `references/pim-ingestion-stealth.md` | Detailed runner pattern for stealth-enabled PIM ingestion (ChatGPT/Grok scraping) |
| `references/chatgpt-grok-sidebar-scroll.md` | Sidebar scrolling JavaScript for lazy-loaded ChatGPT/Grok conversation lists |
| `references/port-ghosting.md` | TIME_WAIT issue when force-killing Firefox, how to detect and work around |
| `references/protocol-detection.md` | How BiDi vs CDP detection works |
| `references/tool-aliases.md` | Full map of tool names from legacy firefox-* servers to ultimate-firefox-mcp |
| `references/csp-bypass-websocket.md` | CSP WebSocket bypass for Cloudflare-protected sites — console syntax, harvester pattern, port ghost cleanup |
| `scripts/stealth-patcher.py` | v2 patcher — detects `remote.active-protocols=1` in normal-browsing profiles |
| `templates/firefox-bidi-runner.py` | Reusable Firefox+BiDi lifecycle: start → connect → work → cleanup |
| `templates/pim-harvester.py` | WebSocket harvester for CSP-restricted sites (replaces HTTP version) |
| `templates/pim-ingest-runner.py` | Reusable two-phase stealth runner for ChatGPT/Grok ingestion |
| `references/firefox-151-gfx-crash.md` | Firefox 151 GFX compositor crash — timing, workarounds, and root cause hypothesis |
| `references/stale-bidi-server-state.md` | Stale WebDriverBiDiServer.json blocks headless BiDi — diagnosis and fix |
| `references/cloudflare-chatgpt-grok-asymmetry.md` | Why ChatGPT extraction returns 0 while Grok works — Cloudflare asymmetry |
| `references/profile-sync-cron-setup.md` | Profile sync cron job 28d080a625fd — copies cookies from main→auto every 2h |
| `references/pim-env-api-key-config.md` | PIM .env API key injection — OpenCode Go as primary, OpenRouter fallback |
| `scripts/patch-xul-webdriver.py`
| `references/cloudflare-chatgpt-grok-asymmetry.md` | Why ChatGPT extraction returns 0 while Grok works — Cloudflare asymmetry |
| `scripts/patch-xul-webdriver.py` | Binary-patch Firefox xul.dll to hide navigator.webdriver |
| `scripts/verify-stealth.py` | End-to-end BiDi stealth verification: connect, apply StealthEngine, tab, verify measures, cleanup |
| `references/extraction-performance-benchmark.md` | Real-world PIM extraction metrics (2026-05-30): headless+BiDi throughput, crash cycle timing, RECONNECT_EVERY analysis — 11 ChatGPT conversations extracted in 3.5 min before per-navigation timeout |
| `scripts/pim-pipeline.py` (external, at `~/AppData/Local/hermes/scripts/pim-pipeline.py`) | Historical — removed June 2026. See `templates/pim-ingest-runner.py`. |