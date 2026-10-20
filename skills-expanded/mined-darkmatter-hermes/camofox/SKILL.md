---
name: camofox
description: Deploy and operate Camofox (stealth headless browser for AI agents) on NixOS devboxes. Covers native setup, R2 persistence, systemd services, and Hermes integration. Use when setting up camofox-browser, configuring camoufox on NixOS, or wiring Hermes to a remote camofox instance.
version: 0.1.0
triggers:
  - camofox
  - camoufox
  - stealth browser
  - anti-detection browser
  - browser on devbox
---

# Camofox Browser — Deployment & Operations

Camofox-browser is a stealth headless browser server for AI agents, powered by Camoufox (a Firefox fork with C++ anti-detection). Repo: [jo-inc/camofox-browser](https://github.com/jo-inc/camofox-browser).

## Architecture

- **Server**: Node.js Express app on port 9377 (default)
- **Browser**: Camoufox (Firefox fork) with fingerprint spoofing at C++ level
- **Persistence**: Profiles stored on disk (cookies, localStorage survive restarts)
- **API**: REST API with tab lifecycle, snapshots, clicks, typing, scrolling, screenshots

## NixOS Deployment (Native, Not Docker)

**Prefer native over Docker.** The Docker image has an Xvfb display race bug (`cannot open display: [object Promise]`) where `VirtualDisplay.get()` returns before the display number is resolved. Native runs fine in headless mode without Xvfb.

### Step 1: Install shared libraries

NixOS doesn't put libs in standard paths. Install all required Firefox deps and set `LD_LIBRARY_PATH`:

```bash
nix profile install nixpkgs#gtk3 nixpkgs#dbus-glib nixpkgs#libXt nixpkgs#alsa-lib \
  nixpkgs#libpulseaudio nixpkgs#libXScrnSaver nixpkgs#atk nixpkgs#at-spi2-atk \
  nixpkgs#cups nixpkgs#pango nixpkgs#cairo nixpkgs#libX11 nixpkgs#libxcomposite \
  nixpkgs#libxdamage nixpkgs#libxext nixpkgs#libxfixes nixpkgs#libxrandr \
  nixpkgs#libxrender nixpkgs#libxcursor nixpkgs#libxi nixpkgs#freetype \
  nixpkgs#fontconfig nixpkgs#gdk-pixbuf nixpkgs#glib nixpkgs#dbus nixpkgs#xcbutil \
  nixpkgs#libxcb nixpkgs#libglvnd nixpkgs#gcc.cc.lib
```

Verify all libs resolve:
```bash
LD_LIBRARY_PATH=~/.nix-profile/lib ldd ~/.cache/camoufox/camoufox-bin | grep 'not found'
# Should return nothing
```

### Step 2: Clone and install

```bash
cd ~/projects
git clone https://github.com/jo-inc/camofox-browser
cd camofox-browser
npm install
```

The postinstall script fetches the Camoufox binary (~300MB) to `~/.cache/camoufox/`.

### Step 3: Configure environment

Create `.env` in the project root:

```
CAMOFOX_API_KEY=<REDACTED>
CAMOFOX_PROFILE_DIR=~/r2-mount/camofox-profiles
CAMOFOX_PORT=9377
LD_LIBRARY_PATH=~/.nix-profile/lib
```

Generate an API key: `openssl rand -hex 24`

### Step 4: Start the server

```bash
cd ~/projects/camofox-browser
LD_LIBRARY_PATH=~/.nix-profile/lib \
CAMOFOX_API_KEY=<REDACTED>
CAMOFOX_PROFILE_DIR=~/r2-mount/camofox-profiles \
node server.js
```

Health check: `curl -s http://localhost:9377/health` — look for `browserConnected: true`.

### Step 5: Systemd service

```ini
# ~/.config/systemd/user/camofox.service
[Unit]
Description=Camofox Browser Server (native)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=~/projects/camofox-browser
EnvironmentFile=~/projects/camofox-browser/.env
Environment=LD_LIBRARY_PATH=~/.nix-profile/lib
ExecStart=/etc/profiles/per-user/cm/bin/node server.js
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable camofox.service
systemctl --user start camofox.service
```

## R2 Persistence with rclone

Camofox profiles (cookies, localStorage) can be stored directly on an R2 FUSE mount so they're shared across instances and survive host reboots.

### rclone config for Cloudflare R2

```ini
# ~/.config/rclone/rclone.conf
[darkmatter-r2]
type = s3
provider = Cloudflare
access_key_id = <from himitsu: cloudflare/r2-team-drive/access-key-id>
secret_access_key = <REDACTED>
endpoint = https://<account-id>.r2.cloudflarestorage.com
region = auto
acl = private
```

Account ID from himitsu: `cloudflare-account-id`. R2 credentials from himitsu: `cloudflare/r2-team-drive/access-key-id`, `cloudflare/r2-team-drive/secret-access-key`. The remote name in rclone config is `darkmatter-r2`. Bucket name: `team-drive`. Run `himitsu read cloudflare/r2-team-drive/access-key-id` and `himitsu read cloudflare/r2-team-drive/secret-access-key` to retrieve current credentials.

### Mount and persist

```bash
# Mount R2 bucket (with vfs-cache-mode full for regular-directory feel)
mkdir -p ~/r2-mount
rclone mount darkmatter-r2:team-drive ~/r2-mount --vfs-cache-mode full --daemon

# Point camofox profiles at R2
CAMOFOX_PROFILE_DIR=~/r2-mount/camofox-profiles
```

**Recommended rclone mount flags for R2 as a shared drive:**
- `--vfs-cache-mode full` — enables full read/write caching (files feel local)
- `--vfs-cache-max-age 168h` — keep cached files for 7 days
- `--vfs-cache-max-size 10G` — up to 10G local cache
- `--vfs-read-chunk-size 128M` / `--vfs-read-chunk-size-limit 512M` — large chunk reads
- `--vfs-write-back 5s` — 5s delay before uploading writes (feels instant to user)
- `--dir-cache-time 72h` — cache directory listings for 3 days
- `--buffer-size 256M` — large read buffer
- `--no-checksum` / `--no-modtime` — skip checksum/modtime checks (faster, R2 doesn't need them)
- `--attr-timeout 72h` — cache file attributes for 3 days

**Important**: Docker containers CANNOT bind-mount from rclone FUSE mounts. Use native execution when you need R2-backed profiles.

### rclone systemd unit (NixOS)

```ini
# ~/.config/systemd/user/r2-mount.service
[Unit]
Description=R2 Team Drive (rclone mount)
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
NotifyAccess=all
ExecStartPre=/etc/profiles/per-user/cm/bin/mkdir -p ~/r2-mount
ExecStart=~/.nix-profile/bin/rclone mount darkmatter-r2:team-drive ~/r2-mount \
  --vfs-cache-mode full \
  --vfs-cache-max-age 168h \
  --vfs-cache-max-size 10G \
  --vfs-read-chunk-size 128M \
  --vfs-read-chunk-size-limit 512M \
  --vfs-write-back 5s \
  --dir-cache-time 72h \
  --buffer-size 256M \
  --no-checksum \
  --no-modtime \
  --attr-timeout 72h \
  --file-perms 0644 \
  --dir-perms 0755 \
  --umask 022 \
  --log-level INFO \
  --log-file ~/.local/state/rclone-mount.log
ExecStop=/run/wrappers/bin/fusermount -uz ~/r2-mount
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=60
StartLimitBurst=5

[Install]
WantedBy=default.target
```

**NixOS path quirks**: `/bin/mkdir` doesn't exist — use `/etc/profiles/per-user/cm/bin/mkdir`. `fusermount` is at `/run/wrappers/bin/fusermount`. `rclone` is at `~/.nix-profile/bin/rclone`. Always verify paths with `which <cmd>` before hardcoding in systemd units.

## Hermes Integration

Point Hermes at the remote camofox instance:

```bash
hermes config set browser.engine camofox
hermes config set camofox.url http://devbox:9377
hermes config set camofox.apiKey <key>
hermes config set camofox.managedPersistence true
hermes config set camofox.userId hermes
hermes config set camofox.sessionKey hermes
```

Use `devbox` hostname (resolves via Tailscale/SSH config) rather than raw IPs — the security scanner may block private network IPs.

## API Quick Reference

```bash
# Create tab (requires userId + sessionKey in body)
curl -X POST http://localhost:9377/tabs \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <REDACTED>' \
  -d '{"url":"https://example.com","userId":"hermes","sessionKey":"hermes"}'

# Get snapshot with screenshot (userId required on all GET endpoints)
curl "http://localhost:9377/tabs/<tabId>/snapshot?includeScreenshot=true&userId=hermes" \
  -H 'Authorization: Bearer <REDACTED>'

# Click element
curl -X POST http://localhost:9377/tabs/<tabId>/click \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <REDACTED>' \
  -d '{"ref":"e1","userId":"hermes"}'

# Health check (no auth required)
curl http://localhost:9377/health
```

### Screenshot via Python (recommended)

The `/screenshot` endpoint returns 410 Gone in practice. Use `/snapshot?includeScreenshot=true` instead. The response `screenshot` field is a **dict** `{data: "<base64>", mimeType: "image/png"}`, not a raw base64 string.

```python
import urllib.request, json, base64, os

API = "http://localhost:9377"
KEY = os.environ.get("CAMOFOX_API_KEY", "")
HEAD = {"Content-Type": "application/json", "Authorization": "<REDACTED>" + KEY}

# Create tab
data = json.dumps({"url": "https://example.com", "userId": "hermes", "sessionKey": "hermes"}).encode()
resp = json.loads(urllib.request.urlopen(urllib.request.Request(API + "/tabs", data=data, headers=HEAD, method="POST")).read())
tab_id = resp["tabId"]

# Get snapshot with screenshot
url = API + "/tabs/" + tab_id + "/snapshot?includeScreenshot=true&userId=hermes"
snap = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=HEAD)).read())

# Decode screenshot
ss = snap["screenshot"]  # dict: {"data": "<base64>", "mimeType": "image/png"}
with open("/tmp/screenshot.png", "wb") as f:
    f.write(base64.b64decode(ss["data"]))
```

For a ready-to-run script, see `scripts/screenshot.py` — takes URL and output path as args.

## VNC (Interactive Login via Browser)

VNC lets you log into websites interactively through a browser UI, then persist the session via R2 so Hermes can reuse authenticated cookies.

### Enable VNC in config

```json
// camofox.config.json — set vnc.enabled to true
{
  "plugins": {
    "vnc": { "enabled": true, "resolution": "1920x1080" }
  }
}
```

### Install VNC deps (NixOS)

```bash
nix profile install nixpkgs#xorg.xvfb nixpkgs#x11vnc nixpkgs#novnc nixpkgs#python3Packages.websockify
```

### Patch vnc-watcher.sh for NixOS

The watcher script has two hardcoded paths that don't work on NixOS:

1. **noVNC path** — hardcoded to `/usr/share/novnc`. Patch to the Nix store path:
   ```bash
   NOVNC_PATH=$(dirname $(find /nix/store -maxdepth 4 -name 'vnc.html' -path '*/novnc/*' 2>/dev/null | head -1))
   sed -i "s|NOVNC_DIR=\"/usr/share/novnc\"|NOVNC_DIR=\"$NOVNC_PATH\"|" ~/projects/camofox-browser/plugins/vnc/vnc-watcher.sh
   ```

2. **Log paths** — hardcoded to `/var/log/` which is immutable on NixOS:
   ```bash
   sed -i 's|/var/log/novnc.log|~/.local/state/novnc.log|' ~/projects/camofox-browser/plugins/vnc/vnc-watcher.sh
   sed -i 's|/var/log/x11vnc.log|~/.local/state/x11vnc.log|' ~/projects/camofox-browser/plugins/vnc/vnc-watcher.sh
   ```

### Access VNC

VNC listens on `0.0.0.0:5900` (raw VNC) and `127.0.0.1:6080` (noVNC web).

**Preferred: Tailscale direct connection (no SSH tunnel needed).** x11vnc binds to all interfaces by default, so you can connect directly via Tailscale IP:

```
# Find devbox Tailscale IP
ssh devbox "tailscale ip -4"
# e.g. 100.88.1.70

# Connect from Mac Screen Sharing
vnc://100.88.1.70:5900   (password from camofox.config.json)
```

Tailscale is more reliable than SSH tunnels — no tunnel process to die, auto-reconnect, encrypted mesh transport.

**Fallback: SSH tunnel** (if Tailscale is unavailable):
```bash
ssh -fNL 5900:127.0.0.1:5900 -L 6080:127.0.0.1:6080 devbox
# Screen Sharing: vnc://localhost:5900
# Browser: http://localhost:6080/vnc.html?autoconnect=true&password=camofox
```

**noVNC browser client** (requires SSH tunnel for port 6080 since it binds localhost only):
```
http://localhost:6080/vnc.html?autoconnect=true&password=<password>
```

### Login → R2 → Hermes workflow

1. Open `http://localhost:6080/vnc.html` in your local browser
2. Log into sites (Google, exchanges, etc.) via the VNC browser
3. Camofox persistence plugin auto-saves cookies to `CAMOFOX_PROFILE_DIR` (R2 mount)
4. When Hermes creates a tab with `userId=hermes`, it loads the saved session state
5. Authenticated browsing without sharing passwords

### VNC clipboard sync

For bidirectional clipboard (copy on your Mac, paste in VNC browser and vice versa), x11vnc needs `xclip` and `xsel` installed, and the `-seldir both` flag:

```bash
nix profile install nixpkgs#xclip nixpkgs#xsel
```

Then restart x11vnc with clipboard support:
```bash
# Kill existing x11vnc, then restart with -seldir both
kill $(pgrep x11vnc)
DISPLAY=:<current-display> x11vnc -display :<N> -forever -shared -rfbport 5900 \
  -noxdamage -quiet -bg -o ~/.local/state/x11vnc.log \
  -rfbauth /tmp/.vnc/passwd -seldir both
```

**noVNC clipboard**: The web client at `/vnc.html` has a clipboard panel on the left sidebar. Click it to manually paste text into the remote browser.

### VNC pitfalls

- **No password by default** — VNC is bound to `127.0.0.1` only, so SSH tunnel is the security boundary. Set `vnc.password` in `camofox.config.json` if you want an additional layer. **macOS Screen Sharing refuses blank passwords**, so you must set one if using a native VNC client. Example: `"vnc": {"enabled": true, "resolution": "1920x1080", "password": "<REDACTED>"}`.
- **Black screen on connect** — The browser shows a blank/black display when no tabs are open. Create a tab via the API first: `curl -X POST http://localhost:9377/tabs -H 'Content-Type: application/json' -H 'Authorization: Bearer <REDACTED>' -d '{"url":"https://google.com","userId":"hermes","sessionKey":"hermes"}'`.
- **x11vnc log path** — Must be writable. On NixOS, `/var/log/` is immutable; patch to `~/.local/state/`.
- **x11vnc dies silently** — If x11vnc crashes (e.g. can't write `/var/log/x11vnc.log`), the VNC connection drops with "connection refused" on port 5900. Check `~/.local/state/x11vnc.log` and the watcher log.
- **websockify must be in PATH** — Install `python3Packages.websockify` via nix profile; the watcher script calls it directly.
- **noVNC won't start without vnc.html** — If the Nix store path isn't set correctly, the watcher exits with `ERROR: /usr/share/novnc not found`.
- **Clipboard needs xclip/xsel** — Without these, x11vnc can't sync the X11 clipboard to VNC clients. Install both and restart x11vnc with `-seldir both`.

## Cookie Export

Camofox profiles are Firefox-based (Camoufox is a Firefox fork) and use Playwright's `storage_state.json` format — they are **not compatible** with Chrome profiles. However, the cookies themselves are portable.

### Reading stored cookies

Profile data is persisted at `CAMOFOX_PROFILE_DIR/<profile-hash>/storage-state.json`. This file contains:

```json
{
  "cookies": [
    {"name": "__cf_bm", "value": "...", "domain": ".uniswap.org", "path": "/", "expires": 1736683200, "httpOnly": true, "secure": true, "sameSite": "Lax"}
  ],
  "origins": [
    {"origin": "https://app.uniswap.org", "localStorage": [{"name": "key", "value": "val"}]}
  ]
}
```

### Chrome → Camofox session transfer

**Cookie-only transfer is insufficient.** Many sites (exchanges, banks, SaaS apps) store auth tokens in localStorage or IndexedDB, not just cookies. Transferring only cookies will appear to work briefly but sessions will invalidate immediately.

**Full session transfer requires cookies + localStorage + IndexedDB.** The Playwright `storage-state.json` format supports cookies and localStorage but not IndexedDB. For sites that rely on IndexedDB, you must interactively log in via VNC instead.

**Passkeys/U2F don't work through VNC.** The browser runs on the devbox with no access to your local authenticator hardware (Touch ID, YubiKey). If a site requires passkey-only login, you must log in on your local browser and transfer the session.

### Transfer workflow (Chrome → Camofox)

1. Log into the target site in Chrome on your Mac (using passkey if needed)
2. Open DevTools Console on the site and run:
   ```js
   copy(JSON.stringify({
     cookies: await cookieStore.getAll(),
     localStorage: Object.fromEntries(Object.entries(localStorage))
   }))
   ```
3. Paste the clipboard contents to the agent
4. Agent converts to Playwright `storage-state.json` and writes it to the R2 profile dir
5. Next camofox session with `userId=hermes` loads the saved state

For Netscape cookie jar export (Cookie Editor extension), convert with `references/cookie-export.md`.

**Best method: Cookie Editor JSON export.** The Cookie Editor extension can export in JSON format (not just Netscape), which includes HttpOnly cookies. Use `scripts/convert-cookies.py` to merge Cookie Editor cookies + Chrome DevTools localStorage into Playwright format:

```bash
python3 convert-cookies.py /tmp/cb-cookies-full.json /tmp/cb-chrome-export.json > /tmp/storage-state.json
```

Then write to the R2 profile dir:
```bash
cp /tmp/storage-state.json ~/r2-mount/camofox-profiles/<profile-hash>/storage-state.json
systemctl --user restart camofox.service
```

**Important**: `cookieStore.getAll()` from DevTools Console does NOT include HttpOnly cookies. Always also export via Cookie Editor extension in JSON format to get the full set. See `references/cookie-export.md` for format details.

### VNC login (when transfer isn't possible)

For sites where session transfer fails (IndexedDB-dependent, device-bound tokens), use VNC:
1. Connect via VNC (`vnc://localhost:5900`, password from `camofox.config.json`)
2. Log in interactively (email/password + TOTP only — passkeys won't work)
3. Persistence plugin auto-saves full state (cookies + localStorage) to R2
4. Hermes picks up the authenticated session on next tab creation

## 1Password Extension (Passkey/WebAuthn Support)

For sites that require passkey or U2F login (Coinbase, etc.), install the 1Password Firefox extension in camoufox. This lets the browser act as its own WebAuthn authenticator.

### Install 1Password extension

1. Download and extract the XPI:
   ```bash
   mkdir -p ~/.cache/camoufox/addons/1password
   # Get the latest XPI URL from AMO API
   XPI_URL=$(curl -sL 'https://addons.mozilla.org/api/v5/addons/addon/1password-x-password-manager/' | \
     python3 -c "import sys,json; print(json.load(sys.stdin)['current_version']['file']['url'])")
   curl -sL "$XPI_URL" -o /tmp/1password.xpi
   python3 -c "import zipfile; z=zipfile.ZipFile('/tmp/1password.xpi'); z.extractall('~/.cache/camoufox/addons/1password'); print(len(z.namelist()), 'files')"
   ```

2. Add to `launchOptions` in `server.js`:
   ```js
   const options = await launchOptions({
     // ... existing options ...
     addons: ["~/.cache/camoufox/addons/1password"],
   });
   ```

3. Restart camofox. The 1Password icon appears in the browser toolbar.

### First-time setup via VNC

1. Connect to VNC (`vnc://localhost:5900`, password from config)
2. Click the 1Password extension icon in the toolbar
3. Sign into your 1Password account (first time only — persists via R2)
4. When a site requests passkey auth, 1Password intercepts and fills it

### Install 1Password CLI (optional, for secret retrieval)

```bash
# NixOS requires allowUnfree for 1password-cli
NIXPKGS_ALLOW_UNFREE=1 nix profile install nixpkgs#_1password-cli --impure
op --version
```

**Note**: The CLI can retrieve passwords/secrets but cannot act as a WebAuthn authenticator. For passkey support, the browser extension is required.

## Pitfalls

- **Docker Xvfb bug**: The Docker image's Xvfb VirtualDisplay has a race condition — `DISPLAY` is set to `[object Promise]` instead of `:N`. Use native execution on NixOS instead.
- **NixOS shared libs**: Camoufox binary expects standard Linux lib paths. Must set `LD_LIBRARY_PATH=~/.nix-profile/lib` (or wherever nix profile libs live). Check with `ldd` on `camoufox-bin` and `libmozgtk.so`.
- **Docker + FUSE**: Docker `--mount bind` cannot access rclone FUSE mounts. Use native execution for R2-backed profiles.
- **Port conflicts**: Check for existing node/camofox processes on 9377 before starting: `ss -tlnp | grep 9377`
- **API auth**: Tab creation requires `userId` and `sessionKey` in the body. The `Authorization: Bearer <REDACTED> header is for the API key gate.
- **Headless mode**: Without Xvfb installed, camofox falls back to headless mode. This is fine for agent use — Camoufox's anti-detection works in headless via C++ patches.
- **`/screenshot` returns 410 Gone**: The dedicated screenshot endpoint is unreliable — returns `{"error":"Tab no longer exists (browser was restarted)","code":"browser_restarted"}` even when the tab is listed and healthy. Use `/snapshot?includeScreenshot=true&userId=*** instead.
- **Screenshot is a dict, not a string**: The `screenshot` field in the snapshot response is `{"data": "<base64>", "mimeType": "image/png"}`, not a raw base64 string. You must access `resp["screenshot"]["data"]` and then base64-decode it.
- **GET endpoints require userId**: The `/snapshot`, `/screenshot`, and tab listing endpoints all require `userId` as a query parameter (e.g. `?userId=hermes`). Without it, you get 400 Bad Request or 403 Forbidden.
- **Hermes MCP config key**: The Hermes `mcp_servers` config key (snake_case) is what `hermes mcp` commands read — NOT `mcpServers` (camelCase) in `config.yaml`. Use `hermes mcp add <name> --url <endpoint>` to add MCP servers, but note it requires interactive prompts for auth. For non-interactive setup, write the config directly.
- **rclone mount + Docker**: rclone FUSE mounts are not accessible from Docker containers. For R2-backed persistence, run natively or use periodic `rclone sync` instead of live FUSE mounts.
- **rclone `--allow-other` on NixOS**: Requires `user_allow_other` in `/etc/fuse.conf`. If not set, mount fails with `fusermount: option allow_other only allowed if 'user_allow_other' is set`. Omit `--allow-other` unless you need other users to access the mount.
- **rclone flag names**: `--dir-cache-ttl` was renamed to `--dir-cache-time` in recent rclone versions. Use `rclone mount --help` to verify flags. S3 remotes don't support `--poll-interval` — omit it to avoid log noise.
- **NixOS systemd ExecStartPre paths**: `/bin/mkdir` doesn't exist on NixOS. Use `which mkdir` to find the real path (typically `/etc/profiles/per-user/cm/bin/mkdir`). Same for `fusermount` (at `/run/wrappers/bin/fusermount` on NixOS).
- **rclone binary path in systemd**: The nix profile rclone path may be `~/.nix-profile/bin/rclone`, not `~/.local/state/nix/profile/bin/rclone`. Verify with `which rclone && readlink -f $(which rclone)`.
- **NixOS `allowUnfree` for `nix profile`**: Flake-based `nix profile install` ignores `~/.config/nixpkgs/config.nix`. Use `NIXPKGS_ALLOW_UNFREE=1 nix profile install nixpkgs#<pkg> --impure` instead. The config file works for `nix-env` but NOT for `nix profile`.
- **1Password extension addon path**: Must be the **extracted directory** (with `manifest.json`), not the `.xpi` file. Camoufox's `confirmPaths()` checks for `manifest.json` inside the addon directory.
- **1Password XPI download**: AMO uses the slug `1password-x-password-manager` (not `1password-xpi`). Get the download URL via the AMO API: `curl -sL 'https://addons.mozilla.org/api/v5/addons/addon/1password-x-password-manager/' | python3 -c "import sys,json; print(json.load(sys.stdin)['current_version']['file']['url'])"`.
- **SSH quoting for API keys**: Passing API keys through SSH commands is error-prone — shell quoting mangles long hex strings, and `write_file` may redact them. **Write scripts locally and `scp` them** to the devbox instead of inlining credentials in SSH commands. Read the API key from the `.env` file at runtime (`CAMOFOX_API_KEY` line in `~/projects/camofox-browser/.env`).
- **VNC vnc-watcher.sh hardcoded paths**: On NixOS, `/usr/share/novnc` and `/var/log/` don't exist. Patch `NOVNC_DIR` to the Nix store noVNC path and log paths to `~/.local/state/` before starting camofox with VNC enabled.
- **VNC requires all four nix packages**: `xorg.xvfb`, `x11vnc`, `novnc`, and `python3Packages.websockify` — missing any one causes silent failures in the watcher script.
- **VNC noVNC 404 on /vnc.html**: If websockify starts but noVNC files aren't found, the websocket connects but there's no web UI. Check the watcher log for `ERROR: .../novnc not found`.
- **Passkeys/U2F don't work through VNC**: The remote browser has no access to your local authenticator hardware. Sites requiring passkey-only login must be authenticated on your local browser first, then the session transferred. For VNC login, use email/password + TOTP only.
- **Cookie-only transfer is insufficient for many sites**: Coinbase and similar apps store auth tokens in localStorage or IndexedDB, not just cookies. Transferring cookies alone will fail — the session invalidates immediately. Use the Chrome DevTools `copy(JSON.stringify({...}))` method to capture localStorage too, or log in via VNC for full state.
- **Chrome profiles are not compatible with Firefox/camoufox**: Chrome uses LevelDB, Firefox uses SQLite/JSON. You cannot copy a Chrome profile directory into camofox. Must export storage data and convert to Playwright format instead.
