---
name: ducter-deploy
description: Install, deploy, connect, upgrade or cleanly reinstall Ducter (a self-hosted personal AI) for a user, on a Mac or a Linux server/VPS (Hetzner, DigitalOcean, AWS…). Use when the user asks to set up, deploy, host, move, pair or reinstall Ducter, put it on a server, a domain or their Tailscale network (tailnet), connect their Mac or phone to it, or add a computer as a worker.
---

# Deploy Ducter

Ducter is a personal AI the user runs on their own computers. You install it, give it an address,
and connect the user's devices. Prefer `--json` outputs and exit codes over reading prose. Every
command below says how to check it worked; when one fails, its output names the next command:
run that instead of improvising.

## What runs where (read before any command)

```
   Mac app · phone (browser / iPhone / Android app) · ducter CLI        <- clients
          |  https://<machine>.<tailnet>.ts.net  (Tailscale: only devices in the tailnet)
          |  or https://<your domain>            (reachable from anywhere)
   tailscale serve :443  or  Caddy :443  (the edge: HTTPS, proxies to 127.0.0.1:7777)
                    |
   THE HOME: core = partner, the Log, tasks, ~/.ducter (data + keys)   <- exactly one per person
                    |  workers dial OUT to the home
   Workers: other computers that only do tasks (ducter worker <address> --code …)
```

1. **The home.** Exactly one per person: the core (conversation, the Log, tasks, settings, keys in
   `~/.ducter`) runs on ONE machine, the user's Mac or a server. Never run two homes on the same
   data, and never install a second home to "move" it: moving is a deliberate migration (history
   doesn't move yet; a new home starts fresh).
2. **Clients.** The Mac app (runs the home itself, or connects to a home elsewhere with a pair
   code), the phone (browser, the iPhone app in TestFlight beta, or the Android app, at the
   home's https address), and the `ducter` CLI (talks to the home on this machine; `--port` /
   `--data-dir` pick another).
3. **Workers.** Other computers that only DO tasks for the home: `ducter worker <address> --code
   <code>`. They keep no data of their own beyond task worktrees.
4. **AI agents (harnesses).** Claude Code / Codex (also pi, DeepSeek Harness) must be installed
   AND signed in on every machine that runs the partner or tasks: the home and each worker. On a
   headless server: `claude auth login` / `codex login --device-auth` (a link to open on any
   device), or a token in `~/.ducter/keys.env`.
5. **The edge.** Ducter never listens publicly; never open port 7777. One of:
   - **Tailscale** (`ducter tailscale`): `tailscale serve` puts HTTPS on 443 at the machine's
     tailnet name and forwards to `127.0.0.1:7777`. No domain, no DNS record, no open port; only
     devices in the user's tailnet can open it.
   - **A domain** (`ducter domain <name>`): Caddy terminates HTTPS on 443 (ports 80 and 443 open,
     an A record to the public IP), or a proxy the user already runs.
   - **From outside** (`ducter anywhere on`): the user's own Cloudflare tunnel at their domain on
     Cloudflare; no open port, but Cloudflare can read the traffic.
   A home may have several; every device keeps the list and uses the best one that answers
   (`ducter reach` lists them).
6. **Outside services.** OpenConnector/oo (accounts), Nowledge Mem (memory), push (APNs, Web Push)
   are outbound only. No inbound ports for them; notifications work on a tailnet-only server too.

### Ask first: how should the user's devices reach it?

Before any command on a server, ask this one question (with the default in brackets):

> Should your phone and Mac reach Ducter **privately through Tailscale** (only your own devices,
> no domain, no open ports; your phone needs the Tailscale app on), or **at your own domain**
> (reachable from anywhere, no app on the phone; needs a public IP with ports 80/443 open)?
> [Tailscale if this server is already in your tailnet, else a domain]

Find the default yourself first: `tailscale status --json 2>/dev/null | grep -m1 BackendState`
says `"Running"` when the server is already in a tailnet. A server with no public IP (home lab,
behind NAT, a private VPC) can only use Tailscale or From outside: don't ask for a domain there.

### Pick the topology

| Situation | Home | Commands |
|---|---|---|
| Mac only | the Mac | `curl -fsSL https://ducter.ai/install.sh \| sh` (app + CLI) |
| Server as home, Tailscale; Mac and phone as clients | server | server: one-liner `--service`, `ducter tailscale`; Mac and phone in the same tailnet; Mac app: Settings › Connect to a Ducter on another computer (or first run: My Ducter is on another computer), address + code |
| Server as home, a domain; Mac and phone as clients | server | server: one-liner `--service`, `ducter domain <name>`; Mac app as above |
| Mac as home; reached from the phone | Mac | Tailscale on the Mac and the phone: `ducter tailscale` on the Mac (see "Mac as the home over Tailscale"); or From outside (`ducter anywhere on`) with a domain on Cloudflare |
| Mac as home; server as a worker (a cloud computer) | Mac | Mac needs an address first (`ducter tailscale` on the Mac with the server in the same tailnet, or `ducter anywhere on`); server: `ducter worker <address> --code <code>` then `ducter service install --worker` |
| Server is the home AND does the tasks (one box) | server | same as "server as home"; tasks run on the home itself. No worker install on it |
| Server home + the Mac does tasks in local repos | server | server as home, then on the Mac: `ducter worker <address> --code <code>` (over Tailscale the Mac must be in the tailnet) |

**Ask the user which topology when it isn't clear.** Then look before you change anything:

```sh
ducter version; ducter doctor --json      # what's installed, signed in, running (exit 0 = ready)
systemctl --user is-active ducter          # Linux: an existing service?
ls /Applications/Ducter.app ~/.ducter 2>/dev/null   # Mac: an existing app or home?
cat ~/.ducter/public-url 2>/dev/null       # an address already set up?
ducter reach --json 2>/dev/null            # every address this home has
tailscale status --json 2>/dev/null | grep -m2 -E '"BackendState"|"DNSName"'   # in a tailnet? its name
```

An existing home with data: don't reinstall over it or start a second one; ask.

## Mac

```sh
curl -fsSL https://ducter.ai/install.sh | sh     # Apple silicon; signed + notarized app, CLI at ~/.local/bin/ducter
```

Verify: the app opens; `ducter doctor --json` → `"ok": true`. If `ducter` isn't found in this
shell: `export PATH="$HOME/.local/bin:$PATH"` (the installer added it to the profile for new shells).

## Linux server (home)

The order: **install `--service` → local health → sign in an AI agent → the address (Tailscale
or a domain) → `ducter pair` for each device.** For a domain, ask for the name first so the A
record propagates while you install.

1. **Install as a service** (x64 or arm64; as root is fine, data goes to `/root/.ducter`):
   ```sh
   curl -fsSL https://ducter.ai/install.sh | sh -s -- --service
   ```
   Verify: `curl -fsS http://127.0.0.1:7777/health` → `{"ok":true,…}`; `systemctl --user is-active ducter` → `active`;
   `loginctl show-user $USER -p Linger` → `Linger=yes` (the service survives logout and reboot; if
   not: `loginctl enable-linger $USER`). Not answering: `journalctl --user -u ducter -n 50 --no-pager`.
   As root it links `/usr/local/bin/ducter`; otherwise run the `export PATH=…` line it prints, or
   use `~/.local/bin/ducter`. Not root and `systemctl --user` fails: log in over SSH as that user
   (not `sudo su`). The end of the output is the next step: on a server already in a tailnet it
   leads with "This server is in your tailnet (<name>) … ducter tailscale"; otherwise it lists
   From outside, a domain, Tailscale and an SSH tunnel. `ducter pair --json` says the same as
   data: `reachable`, `tailnet` (the name, or null) and `steps` (Tailscale first when in a tailnet).
2. **Sign in an AI agent on the server** (no browser): `claude auth login` or
   `codex login --device-auth`; send the user the link it prints, wait for the code. Or put
   `CLAUDE_CODE_OAUTH_TOKEN=…` (from `claude setup-token` on any machine) in `~/.ducter/keys.env`,
   then `chmod 600 ~/.ducter/keys.env`. Never print or log tokens. Verify: `ducter doctor --json`.
   One agent is enough. **Codex only is fine:** with Claude Code not signed in and Codex signed
   in, the partner thinks with Codex and Codex does the tasks, with no setting to change.
3. **The address:** path A (Tailscale) or path B (a domain), as the user chose.

### Path A: Tailscale (private to the user's devices)

Nothing is opened to the internet: no firewall change, no DNS record, no domain.

1. **The server in the tailnet.** Skip when `tailscale status --json` already says
   `"BackendState": "Running"`. Else:
   ```sh
   curl -fsSL https://tailscale.com/install.sh | sh     # Tailscale's own installer
   sudo tailscale up                                     # prints a login link: send it to the user
   ```
   The user opens the link on any device and signs in to their tailnet. If their tailnet needs
   new machines approved, they approve it at https://login.tailscale.com/admin/machines.
   Verify: `tailscale status --json | grep -m2 -E '"BackendState"|"DNSName"'` → `Running` and a
   name like `hel.tail1234.ts.net.`.
2. **HTTPS for the tailnet (once per tailnet, the user does it).** On
   https://login.tailscale.com/admin/dns the user turns on **MagicDNS** and **HTTPS
   Certificates**. Tell them Tailscale notes there that machine names appear in a public
   certificate log. You can't check this switch except through step 3 (`ducter tailscale` reads
   `CertDomains` and stops before `serve` would hang).
3. **Serve and pair:**
   ```sh
   ducter tailscale --json
   ```
   `ok: true` → `address` (`https://<machine>.<tailnet>.ts.net`), `pair.code`, `pair.link`.
   It runs `tailscale serve --bg --https=443 http://127.0.0.1:7777` (kept across reboots), saves
   the address and makes a code. `warning` set (this server couldn't open its own name, often
   `--accept-dns=false`) is fine: devices in the tailnet still can. `ok: false` → `error` and
   `next`; the step that failed is the one with `ok: false` in `steps`:

   | `steps[].id` / words | Cause | Do |
   |---|---|---|
   | `tailscale` "isn't installed here" | no `tailscale` CLI | step 1 |
   | `tailscale` "doesn't answer" | `tailscaled` not running | `sudo systemctl enable --now tailscaled`, rerun |
   | `tailscale` "installed here but not signed in" | NeedsLogin | `sudo tailscale up`, send the link, rerun |
   | `tailscale` "hasn't approved this computer yet" | NeedsMachineAuth | the user approves it at admin/machines, rerun |
   | `tailscale` "turned off on this computer" | Stopped | `sudo tailscale up`, rerun |
   | `https` "can't give this computer an HTTPS certificate yet" | MagicDNS or HTTPS Certificates off | step 2 (the user), rerun |
   | `serve` "didn't let this user change what it serves" | not root, not Tailscale's operator | `sudo tailscale set --operator=$USER` once, rerun |
   | `serve` "asks you to turn on HTTPS (Serve)" | the tailnet wants the feature on first; `next` is its link | the user opens `next`, turns it on, rerun |
   | `serve` "already serves something else" | 443 on that name is another app's | ask the user; never remove their serve yourself |
   | `reach` 502/503/504 | Ducter isn't answering behind serve | `systemctl --user restart ducter`, `ducter doctor`, rerun |

   Rerunning is safe. `ducter tailscale --remove` turns Ducter's serve off (only Ducter's) and
   takes the tailnet address out; Tailscale stays.
4. **Check from a device in the tailnet** (the user's Mac with Tailscale on):
   `curl -sS -o /dev/null -w '%{http_code}' https://<name>.ts.net/health` → `200`. `000` there:
   that device isn't in the tailnet or has Tailscale off; on the server `tailscale serve status`
   must show `https://<name>` → `http://127.0.0.1:7777`.
5. **Devices:** every phone and computer that connects must have **the Tailscale app on, signed
   in to the same tailnet** (iPhone/iPad and Android: the Tailscale app from their store; Mac: the
   Tailscale app). Tell the user this before giving them the code. Then step 4 below.

### Path B: your own domain

1. **Firewall** (cloud provider's firewall, and `ufw` if on): inbound TCP 22, 80, 443; UDP 443
   optional (HTTP/3). Never 7777.
2. **DNS.** Ask the user for a name, e.g. `ducter.example.com`. They add an A record → the server's
   IPv4 (AAAA for IPv6). Cloudflare: "DNS only", not proxied. Check: `getent ahosts <name>`.
3. **Domain + HTTPS + pair code:**
   ```sh
   ducter domain ducter.example.com --json
   ```
   `ok: true` → `address`, `pair.code`, `pair.link`. `ok: false` → `error` and `next` say what to do:
   - DNS missing/wrong: add exactly the record in `error`, wait a minute, rerun.
   - Port 80/443 held by nginx/another proxy: keep it; `ducter domain <name> --print` shows the
     site; forward `https://<name>` → `http://127.0.0.1:7777` with WebSocket upgrades and
     `X-Forwarded-For`, then `ducter reach add https://<name> --kind domain` and `ducter pair --json`.
   - `httpStatus` 502/503/504: HTTPS and the certificate are fine; Ducter behind Caddy isn't
     answering: `systemctl --user status ducter`, `ducter doctor`, `systemctl --user restart ducter`, rerun.
   - `httpStatus` 0: no HTTPS yet: ports 80/443 closed in the cloud firewall, or DNS; `journalctl -u caddy -n 50`.
   - Not Debian/Ubuntu: install Caddy yourself, add the `--print` block to the Caddyfile.
   Rerunning is safe; `ducter domain --remove` undoes it (Caddy stays).

**Both** is fine: run `ducter tailscale` and `ducter domain` (in either order); each adds its own
address and devices use the best one that answers.

### Then, on either path

4. **Connect the user's devices.** `ducter pair --json` → `code`, `link`, `address`. **One code
   per device:** it works once, for 10 minutes; run `ducter pair --json` again for each next
   device (or the user picks Devices › Add a device › To talk with Ducter / 设备 › 加一台设备 › 用它和 Ducter 说话
   in the Mac app, also when it is connected to a server home). The code `ducter tailscale` or
   `ducter domain` printed is spent once the first device uses it. Mac app: Settings › Connect
   to a Ducter on another computer (or "My Ducter is on another computer" on first run), paste
   the link. Phone: open the link in the browser, or the iPhone app
   (TestFlight: https://testflight.apple.com/join/Z4GvWt7t) or the Android app with address +
   code (or scan the QR code). Over Tailscale the phone needs the Tailscale app on at that moment.
   Verify: `ducter devices --json` lists it.
5. **Browsing the web (optional):** `ducter ability add browser` installs Ducter's own headless
   Chrome (Chrome for Testing, ~170 MB, into `~/.ducter/browser`) so tasks can browse. As root it
   installs Chrome's system libraries with apt-get itself; as a normal user it prints one
   `sudo apt-get install …` line: run it, then the same command again. Verify: it ends with
   "… can browse the web now (Chrome <version>)", and `ducter browser check` opens a page with
   it and says which Chrome answered. The user does the same with one tap in Devices
   › Browse the web. Sites that need a sign-in are signed into by the user, in the app's live
   view; never sign in for them. `ducter browser sites` lists them.

**Which layer is broken**, from any machine (with Tailscale: one in the tailnet):
`curl -sS -o /dev/null -w '%{http_code}' https://<address>/health`

| Code | Layer | Fix |
|---|---|---|
| 200 | all good | `ducter pair --json` |
| 502 / 503 / 504 | the edge (Caddy or tailscale serve) is fine; Ducter down | `systemctl --user status ducter`; `ducter doctor`; `systemctl --user restart ducter`; `journalctl --user -u ducter -n 50 --no-pager` |
| 308 / 301 on `http://` | Caddy redirecting to HTTPS (normal) | use `https://` |
| 000 / TLS error, a domain | DNS, firewall 80/443, or no certificate yet | `getent ahosts <name>` = server IP; open 80/443; `journalctl -u caddy -n 50`; rerun `ducter domain` |
| 000, a `.ts.net` address | this device isn't in the tailnet, Tailscale is off on it, or serve is off | Tailscale on here; on the server `tailscale serve status`, else rerun `ducter tailscale` |

**Neither Tailscale nor a domain:** the Mac alone can use an SSH tunnel; `ducter pair --json`
gives `tunnel` (`ssh -N -L 7777:127.0.0.1:7777 user@ip`, run on the Mac, kept open); the address
is then `http://127.0.0.1:7777`. A phone can't use that: it needs Tailscale, a domain or From
outside (`ducter anywhere on`). **Another private network** (ZeroTier, NetBird, a proxy of the
user's own): forward an `https://` address to `127.0.0.1:7777`, then `ducter reach add <address>`.
**IPv6-only server:** use an AAAA record; IPv4-only clients can't reach it.

## Mac as the home over Tailscale

For a user whose Mac is the home and who wants the phone to reach it privately:

1. The Tailscale app on the Mac, signed in (`ducter tailscale` finds its CLI inside
   `/Applications/Tailscale.app`; it isn't on PATH). MagicDNS and HTTPS Certificates on, as in
   path A step 2.
2. Ducter running (the app open, or `ducter up`), then on the Mac: `ducter tailscale --json`.
   Failures read as in path A; on a Mac "not signed in" and "turned off" are fixed in the
   Tailscale app (`open -a Tailscale`), and the operator line doesn't apply.
3. The phone: the Tailscale app on, then the link or QR code from `ducter pair`.

Tell the user plainly: the phone reaches Ducter only while the Mac is awake and online. For a
partner that works while the Mac sleeps, put the home on a server instead.

## Add a worker (Add a computer for tasks)

The user usually hands you a line from the app's **Your devices › Add a device › For Ducter to do tasks
on** ("Add this computer to my Ducter: … run `curl -fsSL https://ducter.ai/install.sh | sh -s -- worker <address>
--code <code>`"). On the computer you run on (the one being lent):

1. Check it reaches the home: `curl -sS -m 10 <address>/health` → `{"ok":true}`. A worker only
   dials OUT to the home: no public address, open port or Tailscale is needed on this machine,
   only outbound access to `<address>`. If it fails, say so in one sentence ("this computer
   can't reach <address>; its network or firewall blocks it") and stop. With a `.ts.net`
   address this machine must be in the same tailnet; with an `http://192.168…` address it must
   be on the home's own network.
2. Run the line exactly as given. It installs Ducter (kept if this version is already here),
   joins with the one-time code, and installs the worker service: a systemd user unit (system
   unit as root), a LaunchAgent on a Mac. It is safe to run again: a join that still works is
   kept and no code is spent.
3. Failures, each one sentence and one next step for the user: `That code has expired` → ask
   for a new code in **Add a computer for tasks** (codes last 10 minutes, once); `curl: not found` →
   install curl (`sudo apt install curl`) and rerun; `runs on x64 and arm64 Linux` or `needs
   Apple silicon` → this computer can't be lent.
4. The worker needs its own signed-in Claude Code or Codex for tasks to run there; if none is
   signed in (`ducter doctor`), offer to sign one in. The app shows the computer arriving by
   itself; you don't need to report it.

Without the app's line: on the home, `ducter pair --json` → `code`, then on the worker
`ducter worker <address> --code <code> --service` (the same three steps). A Mac with the Ducter
app connected to the home can instead turn on "Let this Mac help … with tasks" on its card. Verify on the
home: `ducter devices --json` → the worker with `"awake": true`. A server that is the home does
tasks itself: no worker needed there.

## Upgrade

In place, from the release (0.0.4 and later):

```sh
ducter update --check --json   # {latest, devices:[{id, name, home, current, latest, available, how, notes}]}
ducter update --yes            # this machine: download, check the SHA-256, self-check, swap, restart, health-check
ducter update --all --yes      # everything: the home, then the other computers, then their AI agents
ducter update --to 0.0.3 --yes # go back to a version (never done without --to)
ducter update --agents --check --json  # each AI agent: {device, harness, version, how, latest, available, standing}
ducter update --agents --yes          # update the AI agents that are behind, each at its safe point
```

It waits for merges and undos to finish and gives running tasks a moment; tasks resume after
the restart. If the new version doesn't answer `/health` within 60 s it puts `ducter.prev` back
and restarts again; the exit code is 1 and `--json` says `reason` and `rolledBack`. `how` tells
you what to do when it can't: `app` (a Mac: the app updates itself, Settings › Updates),
`source` (run from a checkout), `manual` (a Ducter before 0.0.4: run the one-liner once). Data
stays either way. Re-running the one-liner (with `--service` on a server) still works too.
Verify: `ducter version`.

## Clean reinstall (destroys this home's data; confirm with the user first)

```sh
ducter uninstall --all --dry-run --json   # show the user what goes and what stays
ducter uninstall --all --yes              # service/LaunchAgent, ~/.ducter, the ducter command, PATH lines, Ducter's Caddy site
curl -fsSL https://ducter.ai/install.sh | sh -s -- --service
ducter tailscale                          # if they used Tailscale
ducter domain ducter.example.com          # if they used a domain
```

Kept: repos and `ducter/*` branches, agent sign-ins, Caddy itself, Nowledge Mem. Every device
must pair again.

## Moving the home from a Mac to a server

A fresh start (history doesn't move yet): server install → `ducter tailscale` or `ducter domain`
→ Mac app Settings › Connect to a Ducter on another computer → optionally `ducter worker
<address> --code …` on the Mac so tasks can use its local repos. The Mac's own `~/.ducter` stays untouched.

## Never

- Answer **Go** on the user's behalf for anything irreversible, or paste pair codes, tokens or
  keys into chats, issues or logs.
- Open port 7777, run `ducter up --host 0.0.0.0` on a public machine, or edit other Caddy sites.
- Change the user's tailnet settings, take off a `tailscale serve` that isn't Ducter's, or turn on
  `tailscale funnel` (it makes the address public). The admin-console switches are the user's.
- Run a second home on the same data, or `uninstall --all` without the user's explicit yes.
