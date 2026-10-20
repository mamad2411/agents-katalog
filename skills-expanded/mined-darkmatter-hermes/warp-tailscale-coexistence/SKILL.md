---
name: warp-tailscale-coexistence
description: >-
  Run Cloudflare WARP (Zero Trust / Access identity) and Tailscale together on
  Cooper's Mac without breaking .ts.net, .lan/.internal split DNS, subnet
  routes, or hanging configd. Use when WARP + Tailscale conflict, Access login
  should be skipped via WARP, .lan/.internal/<REDACTED> die after WARP on,
  accept-dns questions, or dual-tunnel bring-up.
version: 1.0.0
metadata:
  hermes:
    tags: [warp, tailscale, cloudflare, zero-trust, dns, split-dns, macos, access]
    category: devops
    related_skills: [cooper-feed-dashboard]
---

# WARP + Tailscale coexistence (macOS)

Class skill for dual-tunnel networking on Cooper's machines (esp. Mac Pro).

## Hard rules (agent)

1. **Never thrash tunnels.** No loops of `warp-cli connect/disconnect`, `tailscale up/down`, or rapid `accept-dns` flips. That starved `configd` and caused a **userspace watchdog panic** (`configd` missed checkins 180s → reboot). One careful bring-up or stop and explain.
2. **If Cooper says wait / evaluate — stop.** Do not “finish the DNS fix” after an explicit hold.
3. Prefer **API/dashboard config** (Zero Trust device profiles) over repeated client churn.
4. Prefer **explaining tradeoffs** when Cooper is deciding; only flip live networking with clear consent.

## Goals Cooper actually wants

| Goal | Mechanism |
|---|---|
| Skip Access email OTP on internal apps | WARP enrolled + app `allow_authenticate_via_warp: true` + fresh WARP identity |
| Keep Tailscale mesh + subnet routes | TS up with **`--accept-routes`** |
| Avoid DNS fight with WARP | TS **`--accept-dns=false`** while WARP owns system DNS |
| Keep `*.ts.net` / `*.lan` / `*.internal` | Must **forward those suffixes** to the right resolver — they are **not** automatic when `accept-dns=false` |

## Critical DNS model

**Tailscale split DNS + search domains only apply when Tailscale is handling DNS** (`accept-dns=true` / Use Tailscale DNS).

With WARP connected and `accept-dns=false`:

| Feature | Status |
|---|---|
| System default resolver | WARP (`127.0.2.2` / Gateway) |
| TS split DNS (`lan`→`ca`, `internal`→`ca`, …) | **Not installed into OS** |
| TS search domains (`internal`, `tail….ts.net`) | **Not applied** |
| MagicDNS server on-box | Still at **`100.100.100.100`** (and IPv6 `fd7a:115c:a1e0::53`) if MagicDNS enabled on tailnet |
| Peer IPs `100.x` | Work if TS interface/routes are up (independent of DNS) |
| Subnet routes | Still installed if **`--accept-routes`** |

So: **`accept-dns=false` does not delete MagicDNS** — it only stops Tailscale from owning *all* DNS. Names work only if something sends queries to `100.100.100.100` (or to `ca` for `.lan`/`.internal`).

### Cooper tailnet split DNS (when TS DNS is ON)

From `tailscale dns status` (authoritative when accept-dns=true):

| Suffix | Resolver |
|---|---|
| `lan` | `100.105.82.38` (`ca`) |
| `internal` | `100.105.82.38` (`ca`) |
| `dm` | `100.105.82.38` (`ca`) |
| various DoH | `http://100.75.11.55:51191/dns-query` |
| search domains | includes `internal`, `<REDACTED>` |

`<REDACTED>` and `*.lan` **depend on this path**. WARP Local Domain Fallback that lists `lan`/`internal` **without** `dns_server: ["100.105.82.38"]` still fails (falls through to Gateway → NXDOMAIN/root SOA).

## Recommended dual-stack recipe (manual, slow)

```text
1. Quit Tailscale completely
2. Connect WARP → wait Connected/healthy (no retries storm)
3. Browser once if needed: Access refresh-identity / WARP auth
4. Start Tailscale:
     tailscale up --accept-dns=false --accept-routes
5. Verify lightly (few probes, not loops):
     curl -s https://www.cloudflare.com/cdn-cgi/trace | rg warp
     curl -sI https://feed.cm.xyz/ | head -5
     tailscale ping <100.x peer>
```

**Keep:** `--accept-routes` (subnets).
**Off while WARP on:** `--accept-dns`.
**Do not** enable a Tailscale **exit node** while WARP is full-tunnel.

### Flag cheat sheet

| Flag | With WARP | Alone (TS only) |
|---|---|---|
| `--accept-routes` | **on** | on |
| `--accept-dns` | **off** | on (nicest for names) |
| exit node | **off** | optional |

## WARP Zero Trust device profile requirements

Account: darkmatter CF `acb126dc2c4cf93764fa69d9bd55a3cf`, org **drkmttr**.

**Split Tunnels = Exclude mode** must include at least:

- `100.64.0.0/10` — Tailscale CGNAT
- `fd7a:115c:a1e0::/48` — Tailscale IPv6

(Default private ranges 10/8, 172.16/12, 192.168/16 usually already excluded.)

**Local Domain Fallback** (suffix → DNS servers) — *pending Cooper decision for `.lan`/`.internal`*:

| Suffix | Intended `dns_server` | Purpose |
|---|---|---|
| `ts.net` | `100.100.100.100` | MagicDNS apex |
| `<REDACTED>` | `100.100.100.100` | tailnet MagicDNS |
| `lan` | `100.105.82.38` | was TS split DNS → `ca` |
| `internal` | `100.105.82.38` | `<REDACTED>` etc. |
| `dm` | `100.105.82.38` | same |

API shape (when Cooper approves applying):

```http
PUT /accounts/{id}/devices/policy/fallback_domains
PUT /accounts/{id}/devices/policy/{policy_id}/fallback_domains
PUT /accounts/{id}/devices/policy/exclude
```

Auth: himitsu `cloudflare-global-api-token` + `cloudflare-email` (`X-Auth-Email` / `X-Auth-Key`).
Custom profile path is **`devices/policy/{id}/…`** (singular), not `devices/policies/{id}/…`.

Already applied previously (confirm before re-applying): default + onboarding profile excludes for TS ranges; fallback entries for `ts.net` / `<REDACTED>` → `100.100.100.100`. **`.lan`/`.internal` → `ca` may still need Cooper-approved apply.**

## Access via WARP

- Org: `allow_authenticate_via_warp: true`, session often `warp_auth_session_duration: 8h`.
- Per-app flag: `allow_authenticate_via_warp` on the Access self_hosted app (feed + many internals were enabled).
- Agents/crons still use **service tokens** + `non_identity` policies — WARP identity is for browser UX.
- First hit may return `Please authenticate via the warp client` until browser completes identity refresh.

## Cooper's verdict (Aug 2026)

**Dual-stack was evaluated and rejected.** The dealbreaker: `.lan` / `<REDACTED>` / `.dm` split DNS (→ `ca` at `100.105.82.38`) and search domains stop working under WARP, and the WARP Local Domain Fallback fix (pointing those suffixes at `100.105.82.38`) was never worth applying vs. the complexity cost. Cooper said "not worth it."

**Rolled back:** `allow_authenticate_via_warp` on 21 Access apps (feed.cm.xyz + internals) → all set back to `false`. Device-profile fallback/exclude additions for TS ranges → reverted (except pre-existing `100.64.0.0/10` exclude).

**Recommended path for now:** TS-only daily with `accept-dns=true`. Access via email OTP or service tokens. WARP only if Cooper explicitly asks again.

## Modes Cooper can pick

1. **TS-only daily (CURRENT PREFERENCE)** — WARP off, `accept-dns=true` → split DNS + search domains “just work”. Access via email/service token.
2. **WARP + TS mesh** — recipe above; names need Local Domain Fallback (or use `100.x` IPs). **Rejected Aug 2026 — too much complexity for lost split DNS.**
3. **WARP only when needed** — flip WARP on for Access sessions; don't leave both fighting DNS all day.

## Failure signatures

| Symptom | Likely cause |
|---|---|
| WARP stuck “DNS Lookup Failed” | TS `accept-dns=true` owns resolver; turn TS DNS off or quit TS first |
| `*.ts.net` NXDOMAIN with TS up | Nothing forwards to `100.100.100.100` |
| `*.lan` / `<REDACTED>` dead under WARP | Fallback missing **dns_server=`100.105.82.38`** (or TS DNS off without fallback) |
| Feed 302 Access login with WARP on | App flag off or identity not refreshed |
| Peers timeout / TS offline after WARP thrash | Restart TS once; don’t loop |
| `configd` watchdog panic / reboot | Tunnel connect storms — stop immediately |
| `warp-cli` IPC timeout | Daemon wedged after thrash — leave it; user recovers |

## Diagnostics (light — few commands)

```bash
warp-cli status
tailscale status | head
scutil --dns | head -40
tailscale dns status | head -40
warp-cli settings | rg -i 'fallback|exclude|100\.64|Mode'
dig +time=2 +tries=1 <REDACTED>
dig +time=2 +tries=1 <REDACTED> @100.100.100.100
curl -s https://www.cloudflare.com/cdn-cgi/trace | rg 'warp|gateway'
```

## References

- `references/dual-stack-runbook.md` — bring-up order, IDs, API notes, panic postmortem anchors
- Cloudflare: Split Tunnels + Local Domain Fallback docs (Exclude mode; fallback does **not** move IP traffic — only DNS)
- Tailscale: MagicDNS still on `100.100.100.100` with `accept-dns=false`; point `*.ts.net` there manually if needed
- Sibling: `cooper-feed-dashboard` (Access app WARP flag + feed routes)
