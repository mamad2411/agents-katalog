---
name: hermes-dashboard-ops
description: >-
  Diagnose and operate Hermes Agent web dashboard + messaging gateway on
  NixOS/devbox — hermes-serve, hermes-gateway, basic/OAuth auth plugins,
  Cloudflare Tunnel (hermes.cm.xyz), stripped plugin.yaml packages, and
  argv0 liveness traps. Use for CF 502s, bind refusals, missing telegram
  adapters, or dashboard gateway_running:false while the unit is active.
version: 1.1.0
metadata:
  hermes:
    tags: [hermes, dashboard, gateway, cloudflared, nix, auth, 502, telegram]
    category: devops
    related_skills: [nix-darwin-hermes-deployment, sops-nix-ops]
---

# Hermes dashboard hosting ops

Class: **Hermes web dashboard behind a tunnel** (not the chat CLI, not Studio CUA).

## Topology (Cooper / darkmatter)

```text
Browser → Cloudflare (hermes.cm.xyz)
       → cloudflared (devbox systemd)
       → hermes-serve user unit 0.0.0.0:9119
       → HERMES_HOME + auth providers
```

Config sources of truth:

| Piece | Where |
|---|---|
| Managed public_url | `/etc/hermes/config.yaml` → `dashboard.public_url` (NixOS) |
| User unit | Home Manager `systemd.user.services.hermes-serve` on devbox |
| Basic auth password | sops → `/run/secrets/rendered/hermes-dashboard.env` (`HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`) |
| Username | unit env `HERMES_DASHBOARD_BASIC_AUTH_USERNAME=cm` |
| Tunnel token | sops → cloudflared `TUNNEL_TOKEN` |
| Studio local MCP | different host — use `nix-darwin-hermes-deployment` / `studio-cua-drive` |

Host: `ssh devbox` (Tailscale / `devbox` in SSH config).

## Fast 502 triage (order matters)

1. **Edge:** `curl -sI https://hermes.cm.xyz/` — bare CF `error code: 502` = origin/tunnel, not DNS/TLS.
2. **Tunnel:** `ssh devbox 'systemctl is-active cloudflared; journalctl -u cloudflared -n 30 --no-pager'`
   - `dial tcp [::1]:9119: connection refused` → origin down (or IPv6-only miss).
3. **Origin:** `ssh devbox 'systemctl --user status hermes-serve; ss -lntp | grep 9119; journalctl --user -u hermes-serve -n 40 --no-pager'`
4. **Local probe:** `curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:9119/api/status`

Healthy public surface:

- `/` → **302** `/login?next=…` (auth gate)
- `/api/status` → **200** JSON with `version`

## Failure class A — no auth providers (2026.7.x)

### Symptom

```text
Refusing to bind dashboard to 0.0.0.0 — the auth gate engages on
non-loopback binds, but no auth providers are registered.
```

Crash-loop → cloudflared origin refused → CF 502.

### Root cause (Nix package trap)

Hermes discovers **bundled** plugins only via **`plugin.yaml`** manifests under the bundled plugins dir (`HERMES_BUNDLED_PLUGINS` or package `site-packages/plugins`).

Some llm-agents Nix builds ship `plugins/**/*.py` but **strip every `plugin.yaml`** (`find $pkg -name plugin.yaml` → 0). Then:

- `discover_plugins()` returns empty
- `dashboard_auth/basic` never runs `register()`
- Env `HERMES_DASHBOARD_BASIC_AUTH_*` is present but unused
- Non-loopback bind is hard-refused

Env vars **do** work when the plugin loads:

- `HERMES_DASHBOARD_BASIC_AUTH_USERNAME`
- `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` or `_PASSWORD_HASH`
- optional `_SECRET`, `_TTL_SECONDS`

Config surface: `dashboard.basic_auth.{username,password|password_hash,secret}`.

Upstream-related: [hermes-agent#54489](https://github.com/NousResearch/hermes-agent/issues/54489) (provider disabled / missing → public bind fails).

### Fix

1. **Confirm package is yaml-less:**
   `find "$(python -c 'import hermes_cli,pathlib; print(pathlib.Path(hermes_cli.__file__).resolve().parents[1]/\"plugins\")')" -name plugin.yaml | wc -l`
2. **Overlay manifests** (keep store `.py`, add yaml):

```bash
# Minimal basic auth overlay
FIX=~/.hermes/bundled-plugins-fix
STORE=…/site-packages/plugins   # from hermes package
mkdir -p "$FIX/dashboard_auth/basic"
ln -sfn "$STORE/dashboard_auth/basic/__init__.py" "$FIX/dashboard_auth/basic/__init__.py"
cat > "$FIX/dashboard_auth/basic/plugin.yaml" <<'YAML'
name: basic
version: 1.0.0
description: "Dashboard auth provider — username/password."
author: NousResearch
kind: backend
requires_env:
  - HERMES_DASHBOARD_BASIC_AUTH_USERNAME
YAML
```

3. Point the unit at it:
   `Environment=HERMES_BUNDLED_PLUGINS=~/.hermes/bundled-plugins-fix`
   (or Nix `hermesBundledPluginsFix` derivation in `~/darwin/homes/…/cm@devbox/default.nix`)
4. `systemctl --user daemon-reload && systemctl --user restart hermes-serve`
5. Expect log line `HERMES_DASHBOARD_READY port=9119` and public 302/200.

Durable Darwin/Home Manager path: `hermesBundledPluginsFix` + `HERMES_BUNDLED_PLUGINS=${hermesBundledPluginsFix}` on the user unit. Remove when upstream package ships yamls again.

### Also check

- Plugin not in `plugins.disabled` (setup wizard can disable `basic` — #54489).
- Password env file readable by the user unit (`EnvironmentFile=…hermes-dashboard.env`).
- Username set in unit env (password-only file is not enough).

## Failure class B — IPv6 localhost vs IPv4 bind

cloudflared often dials **`[::1]:9119`**. If hermes only listens on **`0.0.0.0:9119`**, journal shows connection refused even when IPv4 works.

Mitigations:

- Tunnel origin `http://127.0.0.1:9119` (not `localhost`), or
- Bind dual-stack / also `::`, or
- Confirm `curl http://127.0.0.1:9119` vs `curl http://[::1]:9119`.

Public can still succeed if some edges hit IPv4; fix origin URL for stability.

## Failure class C — tunnel only

- `cloudflared` inactive / bad `TUNNEL_TOKEN` / sops template not rendered.
- Origin healthy but wrong ingress hostname in Cloudflare Zero Trust.

## Failure class D — gateway "running" but useless / dashboard lies

Two independent traps (often stacked after the same Nix upgrade).

### D1 — No platform adapters (`No adapter available for telegram`)

Same stripped-`plugin.yaml` root cause as Failure class A, under `plugins/platforms/*`.

- Unit may be **active**, webhook may listen on `:8644`, but messaging is dead.
- Log: `WARNING gateway.run: No adapter available for telegram`
- Config `platforms.telegram.enabled` + `TELEGRAM_BOT_TOKEN` is not enough without discovery.

**Fix:** extend the same `HERMES_BUNDLED_PLUGINS` overlay with `platforms/<name>/plugin.yaml` (+ symlink store `.py`). Telegram upstream name is `telegram-platform` (`kind: platform`). Restart `hermes-gateway`. Expect `✓ telegram connected` / `Gateway running with N platform(s)`.

Durable: `hermesBundledPluginsFix` in `~/darwin/modules~ (auth + platforms) and `HERMES_BUNDLED_PLUGINS` on **both** `hermes-serve` and `hermes-gateway`.

### D2 — Dashboard `gateway_running: false` while process is healthy

`gateway_state.json` can show telegram+webhook `connected` while `/api/status` still says `gateway_running: false`.

**Root cause:** Nix hermes re-execs as `python3.14 …/.hermes-wrapped gateway run --replace`. Liveness only accepts basename `hermes` (or `hermes_cli.main`). `.hermes-wrapped` → false-negative.

**Fix:**

```sh
#!/bin/sh
# unit PATH may lack bash — avoid env bash → 127
exec -a hermes "$PYTHON" "$WRAPPED" gateway run --replace
```

Live cmdline must start with `hermes `. Durable: `hermesGatewayRunner` in `~/darwin/modules~

### D3 — Require four signals

| Signal | Means |
|---|---|
| unit active | supervised |
| `gateway_state.json` platforms connected | adapters up |
| local `/api/status` `gateway_running: true` | argv0 + pid OK |
| public `/api/status` same | tunnel + edge OK |

Harmless noise: `google_chat-platform is not a valid Platform`; HM-owned unit "outdated" warnings.

## Non-negotiables

- Never print dashboard passwords, tunnel tokens, or age keys.
- Hit **public** `/` and `/api/status` (curl + browser UA; bare urllib can CF 403).
- Parse status JSON with Python/`jq` — do not grep booleans.
- Same missing-`plugin.yaml` package bug often causes both CF 502 and dead telegram.

## Verification checklist

```bash
bash ~/.hermes/skills/devops/hermes-dashboard-ops/scripts/verify-public.sh

curl -sS -A 'Mozilla/5.0' -o /dev/null -w '%{http_code}\n' https://hermes.cm.xyz/   # 302
curl -sS -A 'Mozilla/5.0' https://hermes.cm.xyz/api/status | python3 -c \
  'import sys,json;d=json.load(sys.stdin);assert d["gateway_running"] is True;assert d["overall"]=="ok"'
ssh devbox 'pid=$(systemctl --user show -p MainPID --value hermes-gateway); tr "\0" " " </proc/$pid/cmdline; echo'
```

## References

- `references/cf-502-plugin-yaml.md` — dashboard 502 + basic-auth overlay (2026-08-04)
- `references/gateway-nix-liveness.md` — telegram adapters + argv0 hermes launcher
- `references/hermes-cm-xyz-dashboard.md` — Access/httpHostHeader, kanban plugin strip notes
- `scripts/verify-public.sh` — ad-hoc public/origin/gateway checks
- Studio local Hermes+CuaDriver: `nix-darwin-hermes-deployment`
- Secrets / sops-nix / agenix: **`sops-nix-ops`**
- Operator feed (feed.cm.xyz, not hermes.cm.xyz): **`operator-status`** Mode C
