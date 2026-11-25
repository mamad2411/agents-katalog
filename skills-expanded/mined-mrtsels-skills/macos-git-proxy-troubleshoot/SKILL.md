---
name: macos-git-proxy-troubleshoot
description: >
  Diagnose and fix Git/GitHub connectivity issues on macOS when using VPN/proxy
  clients (Shadowrocket, Surge, ClashX, etc.). Covers the full diagnosis chain:
  TUN vs Proxy-mode detection, proxy node health check, Git global config,
  VS Code proxy settings, credential helper setup, and settings.json JSON repair.
---

# macOS Git/VPN Proxy Connectivity Troubleshooting

## When to Use

Trigger when a user on macOS reports that Git can't connect to GitHub (push/pull/clone fails), especially when:
- They're using a VPN/proxy client (Shadowrocket, Surge, ClashX, etc.)
- Terminal `git` works but VS Code Git integration doesn't
- Or both fail with timeout/SSL/proxy errors
- The proxy client shows it's "connected" but traffic isn't routing properly

## Diagnosis Flow

### Step 0 — Determine VPN mode: TUN vs Proxy-only

Some VPN clients (Shadowrocket, Surge) can run in two modes. In TUN (VPN) mode, a virtual interface intercepts ALL system traffic at network level. In Proxy-only mode, only apps that respect the system proxy are affected.

**Check if TUN is active:**
```bash
ifconfig | grep -E "^[a-z]|inet " | grep -v "127.0.0.1"
```
Look for `utun*` interfaces with IPs (e.g. `100.117.x.x` or `198.18.x.x`).

**Identify which app owns each TUN interface:**
```bash
for i in $(seq 0 15); do
  ip=$(ifconfig utun$i 2>/dev/null | grep "inet " | awk '{print $2}')
  [ -n "$ip" ] && echo "utun$i: $ip"
done
```
- `100.x.x.x` → Shadowrocket
- `198.18.x.x` → Tailscale or Surge
- `172.x.x.x` → typically another VPN

This helps isolate which client's TUN settings are interfering.

**Check effective proxy state:**
```bash
scutil --proxy
```
But the short form can be misleading. **Read the full proxy dict** to see scoped per-interface settings — this is critical for diagnosing TUN override issues:
```bash
scutil << 'EOF'
show State:/Network/Global/Proxies
quit
EOF
```
Look for the `__SCOPED__` dictionary — this shows per-interface proxy settings:
- `en0` (Wi-Fi) may have `HTTPEnable: 1` (proxy configured correctly on en0)
- `utun*` (TUN/VPN) may have `HTTPEnable: 0` (no proxy on the VPN TUN)
- Global `HTTPEnable: 0` despite en0 having 1

This means: **the TUN interface overrides the system proxy globally.** Terminal tools using explicit `--proxy` flag may work, but Safari and other system apps using the global proxy setting won't.

**Check network service priority:**
```bash
networksetup -listnetworkserviceorder
```
If VPN/TUN service (Shadowrocket, Surge, etc.) is ranked above Wi-Fi, its proxy settings take precedence.

#### Shadowrocket-specific: Reading its config plist

Shadowrocket stores its configuration in the group container plist:
```bash
python3 -c "
import plistlib
p = '/Users/minimx/Library/Group Containers/group.com.liguangming.Shadowrocket/Library/Preferences/group.com.liguangming.Shadowrocket.plist'
with open(p, 'rb') as f:
    d = plistlib.load(f)
for k, v in sorted(d.items()):
    print(f'{k} = {v}')
"
```

Key settings to look for:
- `group.com.liguangming.GlobalRoutingMethod` — `Config` (rule-based), `Proxy` (all proxy), or `Auto` (auto-speed)
- `group.com.liguangming.ProxyServerType` — `HTTP` or `SOCKS5`
- `group.com.liguangming.ProxyShareEnabled` — whether local proxy (1082) is running
- `group.com.liguangming.CompatibilityMode` — compatibility mode on/off

**If Safari opens GitHub but not Google**, the most likely cause is Shadowrocket's **rule-based routing** (`GlobalRoutingMethod = Config`). The rule file has Google domains set to DIRECT (直连) while GitHub is on PROXY. Fix by changing the routing mode in Shadowrocket's main screen from "Routing/Config" to "Proxy/Agent" or "Auto".

**If TUN's node is bad (SSL timeout) but local proxy (1082) works but system apps still can't connect:**
- Most likely cause: the TUN interface has its own routing rules that override the system proxy
- Check if Shadowrocket is using **rule-based routing** — certain domains may be set to DIRECT instead of PROXY, causing them to bypass the proxy entirely
- Solution: Switch Shadowrocket to Proxy-only mode (turn off VPN toggle, connect Proxy only), or enable "设置为系统代理" (Set as System Proxy) in Shadowrocket's settings

**If TUN's node is bad (SSL timeout) but local proxy (1082) works:** The user needs to either:
- Switch Shadowrocket to Proxy-only mode (turn off VPN toggle, connect Proxy only)
- Or enable "设置为系统代理" (Set as System Proxy) in Shadowrocket's settings
- The terminal command `sudo scutil` can set `State:/Network/Global/Proxies` but requires admin password

### Step 0.5 — Detect DNS poisoning (blocked-domain pattern)

When the user says the VPN is "connected" but some international sites are unreachable, check if DNS is returning fake IPs.

**Quick suspicion check:**
```bash
nslookup www.google.com 2>&1 | grep Address
```

If this returns a non-Google IP (e.g. `157.240.7.20` = Facebook, `69.171.235.22` = Facebook), DNS is poisoned.

**Confirm by comparing DNS sources:**
```bash
# Shadowrocket fake DNS (should return 198.18.0.x if TUN is active)
nslookup www.google.com 198.18.0.2 2>&1

# Clean upstream DNS (1.1.1.1 should return real Google IP)
nslookup www.google.com 1.1.1.1 2>&1

# Corporate DNS (usually 114.114.114.114 — will show poisoned IP)
nslookup www.google.com 114.114.114.114 2>&1
```

Expected patterns:
- **198.18.0.2 → `198.18.0.5`**: Shadowrocket fake DNS working (TUN mode redirects traffic internally)
- **1.1.1.1 → `142.250.x.x`**: Clean DNS, correct answer
- **114.114.114.114 → `157.240.7.20` or `69.171.235.22`**: Corporate firewall transparently hijacking DNS — **returning Facebook IPs for Google queries**

**Why this matters:** Corporate firewalls often do transparent DNS interception at the network level, overriding whatever DNS server you set. This means queries to 114.114.114.114, 8.8.8.8, or even custom DNS can all return poisoned results.

**How DNS poisoning breaks VPN:**
1. App resolves google.com locally → gets Facebook's IP (157.240.7.20)
2. VPN routes to Facebook's IP through the proxy
3. Proxy connects to Facebook, sends TLS ClientHello for "www.google.com"
4. Facebook returns its own certificate → TLS mismatch → `SSL_ERROR_SYSCALL`

**When to suspect Tailscale interference:**
If `scutil --dns` shows Tailscale's `100.100.100.100` as a supplemental resolver with priority over Shadowrocket's `198.18.0.2`, DNS queries may resolve through Tailscale's network instead of the VPN tunnel.

```bash
scutil --dns | grep -E "nameserver|order|if_index" | head -20
# Shadowrocket should have order 200000 (primary)
# Tailscale may have order 101400 (supplemental — can interfere)
```

**Fix DNS poisoning:**
```bash
# 1. Change Wi-Fi DNS to a clean resolver
sudo networksetup -setdnsservers Wi-Fi 1.1.1.1 1.0.0.1

# 2. Enable system HTTP/HTTPS proxy on Wi-Fi (so apps send hostnames through proxy)
sudo networksetup -setwebproxy Wi-Fi 127.0.0.1 1082
sudo networksetup -setsecurewebproxy Wi-Fi 127.0.0.1 1082

# 3. Flush DNS cache
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# 4. Verify
nslookup www.google.com 1.1.1.1  # Should return real Google IP
```

For terminal tools, set environment variables:
```bash
export https_proxy=http://127.0.0.1:1082
export http_proxy=http://127.0.0.1:1082
```
Add to `~/.zshrc` for permanence.

**Verify the fix:**
```bash
curl -v --connect-timeout 15 https://www.google.com 2>&1 | head -5
# Should show HTTP 200/302, not SSL_ERROR_SYSCALL
```

### Step 1 — Check Git global proxy config

```bash
git config --global --list | grep -i proxy
```

Expected output if configured:
```
http.proxy=127.0.0.1:1082
https.proxy=127.0.0.1:1082
```

If missing, set it:
```bash
git config --global http.proxy http://127.0.0.1:1082
git config --global https.proxy http://127.0.0.1:1082
```

The port (1082 here) may vary — check what your VPN client uses.

### Step 2 — Check if proxy port is actually listening

```bash
lsof -iTCP -sTCP:LISTEN -P | grep -E "108[0-9]|SOCKS"
```

If nothing shows, the VPN/proxy client's HTTP proxy isn't running. Check the client's settings.

### Step 3 — Test connectivity chain

**A. Test proxy node via curl:**
```bash
curl -v --connect-timeout 10 --proxy http://127.0.0.1:1082 https://github.com 2>&1 | tail -10
```

- `200` = node works
- `503 Service Unavailable` = node is dead, switch in VPN client
- `Connection refused` = proxy port not listening
- Timeout + no response = node unreachable

**B. Test direct connection (no proxy):**
```bash
curl -v --connect-timeout 10 https://github.com 2>&1 | tail -5
```

**C. Test domestic vs international:**
```bash
curl -s --connect-timeout 10 -o /dev/null -w "baidu: %{http_code}\n" https://www.baidu.com
curl -s --connect-timeout 10 -o /dev/null -w "google: %{http_code}\n" https://www.google.com
```

Pattern to look for:
- Baidu 200 + Google/GitHub 000/503 = **proxy node is the problem**
- Everything fails = internet or DNS issue
- Baidu 200 + Google/GitHub 200 = everything fine, check Git auth

### Step 4 — Check VS Code settings

VS Code uses its own `settings.json` for proxy, separate from git config.

```bash
# Read settings.json
cat ~/Library/Application\ Support/Code/User/settings.json
```

Look for these keys:
```json
"http.proxy": "http://127.0.0.1:1082",
"http.proxyStrictSSL": true,
```

If missing, add them. VS Code reads these at startup — may need restart.

### Step 5 — Fix VS Code settings.json JSON syntax

Common issue: trailing commas in JSON objects/arrays cause parse failure, making VS Code ignore the file. This happens easily when VS Code plugins hand-edit the file.

**Check syntax:**
```bash
python3 -c "import json; json.load(open('~/Library/Application Support/Code/User/settings.json')); print('OK')"
```

**Fix all trailing commas at once:**
```bash
python3 -c "
import re
with open('~/Library/Application Support/Code/User/settings.json') as f:
    c = f.read()
c = re.sub(r',\s*}', '\n}', c)
c = re.sub(r',\s*]', '\n]', c)
open('~/Library/Application Support/Code/User/settings.json', 'w').write(c)
"
```

Then re-verify JSON is valid.

### Step 6 — Check Git credentials

Even if proxy is working, push/publish may fail if Git has no credential helper.

```bash
git config --global credential.helper
```

If empty, set to macOS keychain:
```bash
git config --global credential.helper osxkeychain
```

Also check if `gh` (GitHub CLI) is authenticated — it can be used to set up git auth:
```bash
gh auth setup-git  # Configures git to use gh as credential helper
```

**Check keychain directly for GitHub credentials:**
```bash
security find-internet-password -s github.com -w  # returns the token/password
```

**Verify the token actually works with GitHub API:**
```bash
curl -H "Authorization: token $(security find-internet-password -s github.com -w)" \
  https://api.github.com/user | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('login'))"
```

### Step 7 — Final verification

```bash
git ls-remote https://github.com/curl/curl.git HEAD
```

## Digging Deeper: VS Code Git Extension Log

When VS Code's Git extension fails but terminal `git` works, check the extension log.

**First find the newest session** (VS Code keeps multiple days of logs):

```bash
ls -lt ~/Library/Application\ Support/Code/logs/ | head -5
```

Then read the Git extension log from the newest session:

```bash
NEWEST=$(ls -t ~/Library/Application\ Support/Code/logs/ | head -1)
cat "$HOME/Library/Application Support/Code/logs/$NEWEST/window1/exthost/vscode.git/Git.log"
```

Or scan all windows in the newest session for errors:

```bash
NEWEST=$(ls -t ~/Library/Application\ Support/Code/logs/ | head -1)
find "$HOME/Library/Application Support/Code/logs/$NEWEST" -path "*vscode.git*Git.log" -exec grep -iE "error|fatal|reject|fail|timeout|503|CONNECT" {} \;
```

This shows every git command VS Code ran in the current session, including timing and errors. Key things to look for:
- `git push` or `git pull` followed by `fatal: unable to access ... CONNECT tunnel failed, response 503` — proxy node is intermittently failing
- Large file warnings — `remote: warning: File ... is XX MB; this is larger than GitHub's recommended maximum file size of 50.00 MB` — large files cause slow pushes that may timeout the proxy
- `Failed to execute git` for `git config --get --local` — minor, usually harmless

## Common Failure Patterns

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Intermittent 503 on git operations | VPN proxy node unstable — overloaded or rate-limited | Switch to a more stable node; retry the operation |
| Proxy returns 503 consistently | VPN node expired/dead | Switch node in VPN client |
| SSL_ERROR_SYSCALL or SSL timeout | TUN mode node issue | Try proxy-only mode or switch node |
| Terminal git works, VS Code doesn't | VS Code missing http.proxy | Add to settings.json |
| **VS Code git fails with 503 / SSL — terminal git works through TUN** | Shadowrocket Config mode + unstable node: VS Code has `http.proxy` set, but git has no proxy — terminal bypasses proxy via TUN, VS Code's explicit proxy hits the dead node | Diagnose via VS Code Git extension log (`find ~/Library/Application\\ Support/Code/logs -path "*vscode.git*" -name "*.log"`). Fix: `git config --global http.proxy http://127.0.0.1:1082` so git and VS Code share the same proxy path, OR remove VS Code `http.proxy` and rely solely on TUN |
| Safari: GitHub works, Google doesn't | Shadowrocket rule-based routing (`GlobalRoutingMethod=Config`) has Google set to DIRECT | Switch routing mode to Proxy or Auto; or fix the rule file |
| "Illegal trailing comma" in settings.json | Plugin or hand edit corruption | Strip trailing commas (Step 5) |
| Could not resolve host | DNS not routing through proxy | Check VPN client DNS settings |
| Google resolves to Facebook IP (157.240.x.x, 69.171.x.x) | Corporate DNS poisoning — firewall transparently hijacks DNS queries for blocked domains | Change system DNS to 1.1.1.1/1.0.0.1 AND enable system HTTP proxy on Wi-Fi |
| GitHub API auth OK but git push fails (no prompt) | credential.helper not set | Set to osxkeychain or run `gh auth setup-git` |
