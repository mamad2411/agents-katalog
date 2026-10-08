---
name: lan-direct
description: "Use when testing or running an app while a VPN/proxy tunnel is up and the app's own outbound calls must leave via the real ISP connection instead of the tunnel - geo-locked or domestic APIs, payment/SMS gateways, bank endpoints, or any service that rejects the VPN's exit IP. Gives the app under test a LAN-direct egress path via per-socket binding and a local LAN-bound proxy, while the agent's own connection stays on the VPN. Triggers: test my app without VPN, bypass VPN for this request, split tunnel, API blocked from VPN IP, works without VPN but not with it, my payment gateway rejects the request, domestic API fails while VPN is on."
---

# lan-direct

Route **the app's** traffic out through the ISP while **you, the agent** stay on the VPN.

Works in Claude Code and Codex alike - the mechanism is per-socket binding, which has nothing
to do with the harness.

## The invariant

Never modify the routing table, the WinINET/system proxy settings, or the VPN client's
configuration. Only ever:

- set environment variables scoped to a **child process**, or
- pass **per-tool source-binding flags**.

Both are per-socket and opt-in, so they cannot touch your own connection. This is the
whole point of the skill - if you reach for `route add`, you have broken it (see the
**Escape hatch** section at the end).

Do not suggest disconnecting the VPN. That is the problem this skill exists to avoid.

## Workflow

### 1. Detect and verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\lan-detect.ps1
```

On Linux or macOS use the counterpart instead - same JSON, same exit-code contract:

```bash
bash scripts/lan-detect.sh
```

Emits JSON: `lanIp`, `gateway`, `lanDns`, `subnet`, `tunnelActive`, `vpnAdapter`,
`directEgress`, `lanEgress`, `fakeIpDns`, `bypassWorks`. Exits 0 only when `bypassWorks`
is true - it proves the bypass with two live probes rather than inferring it.

- `tunnelActive: false` -> no VPN is up. Say so and stop; there is nothing to bypass.
- `bypassWorks: false` with a tunnel up -> go to **Troubleshooting** below. Do not proceed.
  Traffic would silently stay on the VPN and you would report a false pass.

### 2. Pick the mechanism

**Node backend (incl. Next.js)? Skip the proxy** - jump to the **Node** recipe under
Per-stack recipes. One env var, no proxy process, and it is the only thing that reaches
native `fetch`.

Everything else: start the LAN-bound proxy. A server process has no `--interface` flag, so
this is how it gets an ISP egress.

```bash
node scripts/lan-proxy.mjs --bind <lanIp> --port 8899          # run in background
node scripts/lan-proxy.mjs --bind <lanIp> --port 8899 --dns <lanDns>   # if fakeIpDns: true
```

It listens on `127.0.0.1` only and logs every host it tunnels, so you can see what the app
actually called.

### 3. Restart the backend pointed at it

```
HTTP_PROXY=http://127.0.0.1:8899
HTTPS_PROXY=http://127.0.0.1:8899
NO_PROXY=localhost,127.0.0.1,<subnet>
```

`NO_PROXY` matters: without it the backend's calls to its own local services get pushed
through the proxy for no reason. (Local DBs on TCP - MySQL, Postgres, Mongo - are not HTTP
and are unaffected either way.)

Set these on the backend's launch command, not globally. See **Per-stack recipes** below -
`HTTP_PROXY` is not enough for several stacks.

### 4. Exercise and confirm

Hit the endpoint whose outbound call was failing. Confirm **both**:

- the call now succeeds, and
- the proxy log shows the host it dialled.

A pass without a matching log line means the request never went through the proxy.

### 5. Tear down

Stop the proxy, restart the backend without the env vars. Nothing else to undo - no global
state was changed.

`pkill -f lan-proxy` from Git Bash does **not** kill a Windows `node.exe`. Use:

```powershell
Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
  Where-Object { $_.CommandLine -like '*lan-proxy*' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

A leftover instance is harmless but will make the next launch fail with a port clash.

## Per-stack recipes

| Stack | How to feed it the proxy |
|---|---|
| Python `requests` / `httpx` | env vars, as-is |
| Go, .NET `HttpClient` | env vars, as-is |
| PHP CLI | libcurl reads `http_proxy` / `https_proxy` from the process env |
| Node (incl. Next.js) | **not the proxy** - use the `lan-bind.mjs` preload, see below |
| PHP under Apache/XAMPP | see below - the service does not inherit your shell |
| curl, wget, npm, ssh, git | skip the proxy, bind directly (see **Direct binding** below) |

### Node - use the preload, not the proxy

Native `fetch` runs on Node's built-in undici, which **ignores `HTTP_PROXY`** on Node <= 23
and accepts no `https.Agent`. Verified on Node 22.20: plain env vars, `NODE_USE_ENV_PROXY=1`
and `--use-env-proxy` all do nothing - the proxy log stays empty and traffic silently goes
out over the VPN. This hits Next.js, the `openai` SDK, and anything else on native `fetch`.

Skip the proxy entirely and use the preload, which binds every outbound socket in the
process:

```bash
LAN_BIND=<lanIp> node --import "file:///<skill-dir>/scripts/lan-bind.mjs" script.js
LAN_BIND=<lanIp> NODE_OPTIONS="--import file:///<skill-dir>/scripts/lan-bind.mjs" npm run dev
```

`<skill-dir>` is this skill's own base directory **with forward slashes** - normally
`C:/Users/<you>/.claude/skills/lan-direct` under Claude Code, or
`C:/Users/<you>/.agents/skills/lan-direct` under Codex. `--import` needs an absolute `file://`
URL on Windows; a bare Windows path with backslashes fails.

`NODE_OPTIONS` propagates to forked workers, so it covers Next.js and Vite dev servers.

This reaches native `fetch`, the `openai` SDK, axios, node-fetch, got and plain
`http`/`https` at once - no dependency, no proxy process, no `HTTP_PROXY` needed. It skips
loopback destinations, so a local DB or dev server keeps working.

Only if the preload is unavailable: **Node >= 24** honors `NODE_USE_ENV_PROXY=1` with the
env vars, and **axios** honors them on any version.

### PHP under Apache / XAMPP

`SetEnv`/`PassEnv` in `httpd.conf` only populates `$_SERVER`; libcurl reads the *process*
environment, so it will not pick them up. Use one of:

- start Apache from a shell that already has `http_proxy`/`https_proxy` exported (e.g.
  `xampp\apache_start.bat`), or
- `putenv('https_proxy=http://127.0.0.1:8899');` before `curl_init()`, or
- `curl_setopt($ch, CURLOPT_PROXY, '127.0.0.1:8899');` directly.

`file_get_contents()` honors none of these - it needs a stream context with `'proxy' =>
'tcp://127.0.0.1:8899'`.

### Direct binding

No proxy needed when the tool can bind its own socket:

| Tool | Flag |
|---|---|
| curl | `--interface <lanIp>` |
| wget | `--bind-address=<lanIp>` |
| npm | `--local-address=<lanIp>` |
| ssh | `-b <lanIp>` |
| Chromium / Playwright | no bind flag exists - use the browser MCP on port 8900, see below |

### Browser / Playwright MCP

Chromium has no source-binding flag, so a browser reaches the ISP only through the proxy.
Use `lan-browser.mjs`: it is a Playwright MCP server that starts and owns its proxy, so the
browser can never come up without one.

It ships with this skill - `scripts/install.ps1` registers it:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <skill-dir>\scripts\install.ps1
```

**Which hosts use the ISP** comes from three merged sources, so this is almost never a
reinstall: `lan-hosts.txt` in the skill directory (shipped defaults, replaced on `git pull`),
`~/.lan-direct-hosts` (the user's own, never overwritten), and `--lan-hosts a,b` at launch.
One rule per line, `#` comments allowed, suffix matching.

When a user wants another host routed via the ISP, append a line to `~/.lan-direct-hosts` and
tell them to restart the browser - do not edit `lan-hosts.txt`, which the next update will
overwrite.

If the user asks to register it by hand, **quote the `--` separator**. On Windows `claude`
resolves to `claude.ps1`, and PowerShell's parameter binder strips a bare `--` before the
script sees it; the CLI then reads the next flag as its own and fails with
`error: unknown option '-y'`. Quoting survives PowerShell and is a no-op in bash, so one
form works everywhere:

```bash
# from a clone
claude mcp add playwright-split --scope user "--" \
  node <skill-dir>/scripts/lan-browser.mjs --lan-hosts ".ir"

# from npm - survives the checkout moving, so prefer it when the user has it installed
claude mcp add playwright-split --scope user "--" npx -y lan-direct browser
```

From a PowerShell *script* rather than the prompt, splat an array instead - see
`scripts/install.ps1`, which builds `$mcpArgs` and passes `@mcpArgs` for the same reason.

Other CLI subcommands, when the package is installed: `lan-direct detect` picks the right
detect script for the platform, and `lan-direct route <host>` answers "would this host go via
the ISP or the tunnel?" without starting a browser. Reach for that one when a user reports a
site not loading - a wrong rule and a down site look identical from the outside.

The server detects the LAN IP, refuses to start if `lan-detect` says the bypass is broken,
reuses an existing proxy if one is already listening, and shuts down what it started when the
MCP exits. Its own logs go to stderr; stdout is left clean for JSON-RPC.

It uses **port 8900**, deliberately not the 8899 used for backend testing above. Reuse is by
port alone, so sharing the number would let a bind-everything backend proxy silently capture
the browser and route all of its traffic via the ISP.

**Mixed browsing works in one browser.** `--lan-hosts` makes the proxy decide per host:
matching hosts egress via the ISP, everything else is left unbound and takes the tunnel. So
"check hoosha and youtube" needs no tool switching - hoosha goes out via the ISP, youtube via
the VPN, same session. The proxy log shows the decision on every line:

```
CONNECT  lan  hoosha.com:443
CONNECT  vpn  youtube.com:443
```

Keep the list accurate: a domestic host missing from it gets the tunnel and fails with an
empty reply, and a foreign host wrongly added to it gets the ISP and may be filtered. When a
site fails in a way that looks like a dead connection, check which route the log picked
before assuming the site is down.

Why an explicit list rather than auto-detection: connecting to a blocked host *through* the
tunnel succeeds at the TCP level (measured: `connect@14ms`) and only dies ~860ms later, after
the proxy has already answered `200 Connection Established`. Falling back would mean
buffering and replaying the TLS handshake and paying that delay on every domestic request.

**Playwright routes loopback through the proxy.** Chrome normally bypasses localhost, but
Playwright overrides that when a proxy is set, so `http://127.0.0.1:3000` arrives at
`lan-proxy.mjs` rather than going direct. Verified in the proxy log. The proxy's loopback
guard is what keeps local dev servers reachable - without it every one of those requests
fails with `EADDRNOTAVAIL`. Don't add `--proxy-bypass=<-loopback>`; it changes nothing here
and only confuses the picture.

## Troubleshooting

**`directEgress` equals `lanEgress` with a tunnel up.** The VPN is enforcing a kill-switch
or strict-route (a WFP filter that blocks bound sockets). Fix it in the VPN client, not
around it: disable strict route, or add a direct/bypass routing rule for the hosts you
need. nekoray/sing-box: turn off `strict_route`, or add a `direct` outbound rule.

On Linux this can also happen with no kill-switch at all: a source address alone does not
override the routing table there the way it does on Windows, so policy routing keeps the
traffic in the tunnel. The fix is a rule sending traffic from the LAN IP out the physical
gateway - `ip rule add from <lanIp> table <n>` plus a default route in that table. That
needs root and is a system-wide change, so explain it and let the user decide. Everything
else in this skill stays unprivileged and process-scoped.

**`fakeIpDns: true`.** The OS resolver is returning `198.18.x.x` placeholders that only
mean something inside the tunnel. Pass `--dns <lanDns>` to the proxy so it resolves through
the LAN's own DNS.

**Egress probe returns nothing.** No connectivity to the probe host. Check the link, re-run.

### Escape hatch

If a backend genuinely cannot be proxied (a compiled binary with no proxy support), the
only remaining option is a host-specific static route:

```powershell
route add <targetIp> mask 255.255.255.255 <gateway> metric 1   # needs admin
route delete <targetIp>                                        # undo, always
```

**This is global.** It pulls *every* process off the tunnel for that destination -
including you, if you ever contact the same host. Requires elevation, survives until
deleted, and is easy to forget about. Ask before using it, and delete it in the same
session.
