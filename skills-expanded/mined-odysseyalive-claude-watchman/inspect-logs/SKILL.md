---
name: inspect-logs
description: "OBSERVE: on a server, hunt inbound attack patterns; on a workstation, watch outbound connections. Queries CrowdSec where present, degrades gracefully when not."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# inspect-logs (Grammar / Observe)

The same skill points two directions, chosen by the profile resolver:
- **server** → inbound attack patterns in the web-server/auth logs;
- **workstation** → outbound connections (what the machine is talking *to*).

Prefers **CrowdSec** (`cscli`) over fragile log regex, and uses its **alert-only**
mode for visibility without enforcement. Degrades gracefully when CrowdSec is
absent. Read-only.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

Every `/watchman audit` / `/watchman loop`. On a workstation it pairs with
`baseline-network`: it flags outbound connections to destinations not in the baseline.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never
   `source lib/…` directly (dontAsk refuses a dot-source). Initialize with
   `bash lib/wm journal_init`. Run `bash lib/wm profile_log_direction` (prints `inbound` or
   `outbound`) and branch on that value, and `bash lib/wm watchman_family` (the family
   selects the Linux vs macOS auth-log and connection commands in step 3). **I/O courtesy:** scanning large/rotated logs is heavy — IF
   `bash lib/wm io_should_defer_heavy`, journal one `capacity`/`info`/`safe`
   `diagnostic_deferred` (`target=inspect-logs`, detail = `"deferred: "` followed by the printed
   output of `bash lib/wm io_pressure_reason`, run first; no `$(…)` substitution) and skip the log-scan/rate steps this pass;
   otherwise run the scans through `bash lib/wm io_run` (the webstats engine idle-prices its reads).
2. **CrowdSec path (preferred).** If `cscli` is available:
   `sudo cscli alerts list -o json` and `sudo cscli decisions list -o json`
   (alert-only — never auto-ban from here, especially on a workstation). Respect the
   family collections (`crowdsecurity/{nginx,apache2,sshd,linux}`).
3. **Degrade gracefully.** If `cscli` is missing, journal one `config`/`low`
   finding "CrowdSec not configured — log analysis degraded" with a remediation to
   install it, then fall back:
   - inbound: scan EVERY directory listed by running `bash lib/wm webserver_log_paths` — this is
     config-derived (parsed from each present server's config), so it covers custom
     `access_log`/`CustomLog` targets, per-vhost logs, and niche servers, NOT just
     `/var/log/{nginx,apache2,httpd}`. For auth-failure bursts (repeated 4xx/401), run
     `bash lib/wm log_path_auth` and branch on the literal it prints:
     - a file path ⇒ scan that file;
     - a `journald:*` sentinel ⇒ `journalctl -u sshd`;
     - a `darwin:log:process==sshd` sentinel (macOS) ⇒
       `bash lib/wm io_run log show --predicate 'process == "sshd"' --last 24h 2>/dev/null`
       (requires Full Disk Access in System Settings > Privacy & Security).
     - a `windows:*` sentinel (family == `windows`) ⇒ there is no `journalctl`; read the
       Windows Security Event Log via the ported dispatcher function (`Get-WinEvent` under the
       hood — the same `bash lib/wm` auth-log function `log_path_auth` resolves to on Windows),
       hunting failed-logon events (Security **4625**) for auth-failure bursts. Do NOT shell
       out to `journalctl`/`ss` on Windows.
   - outbound — current connections compared against `journal/network-baseline.txt` from
     `baseline-network`, branched on `bash lib/wm watchman_family`:
     - Linux ⇒ `ss -tunp`;
     - macOS (`darwin`) ⇒ `lsof -i -n -P 2>/dev/null | awk '/ESTABLISHED/{print $9}'`;
     - Windows (`windows`) ⇒ there is no `ss`/`lsof`; enumerate established connections via the
       ported dispatcher (`Get-NetTCPConnection`, the function `bash lib/wm` resolves to on
       Windows) and compare against the baseline the same way.
4. **Request-rate spikes (DDoS / abuse) — server profile.** If
   `bash lib/wm profile_runs_check request_rate_spike`: run
   `bash lib/wm webstats_rate_offenders` (threshold `$WATCHMAN_RATE_PER_MIN`, default 300 — the
   peak requests-in-one-minute from a single source). It reads **incrementally** by
   default (`WATCHMAN_LOG_INCREMENTAL`) — only the new log lines since the last pass,
   so each loop's read is proportional to recent traffic, not total log size. This
   reuses the web-stats log parser but — unlike the anonymized `/watchman stats`
   analytics — **keeps the real
   offending IP**, because you cannot firewall-block a hash and this is the security
   path (defending the system, a different legal basis). For each offender, journal:
   `category=security`, `severity=<level>` (run `bash lib/wm profile_severity request_rate_spike`;
   use the printed level as the literal severity),
   `risk_tier=review`, `check_id=request_rate_spike`, `target=<ip>` (per-IP, so the
   fingerprint is stable and a returning flooder regresses loudly); detail = the
   peak/min, total, and UA sample; remediation = `firewall_deny <ip>/32` — shown and
   confirmed per the risk tiers. Note: on macOS `firewall_deny` uses pf and will
   explain the anchor-file approach rather than applying directly. Bots/crawlers may
   appear here; the operator decides (it is `review`, never auto-applied).
5. **Journal findings.** Inbound probe clusters → `category=security`; new outbound
   destinations → `category=security`, severity per `bash lib/wm profile_severity outbound_new_connections`.
   `check_id` stable per pattern/destination so re-runs update in place.
6. **Never block or ban.** Enforcement (firewall/ban) is the operator-run fixer's
   job under the risk tiers — this skill only observes and records.
<!-- /origin -->

## Grounding

All claude-watchman functions below are reached via `bash lib/wm <function>` (never a
direct `source`); the lib files are where they live.

- `lib/distro.sh` — `webserver_log_paths` / `webserver_config_roots` / `webserver_detect`
  (config-derived web-log discovery — scans `/etc` config roots and parses log directives),
  `log_path_auth`.
- `lib/webstats.sh` — `webstats_rate_offenders` (the security-path rate detector; keeps the
  real IP for the firewall proposal — distinct from the anonymized `/watchman stats` report).
- `lib/profile.sh` — `profile_log_direction`, `profile_severity` (`request_rate_spike`).
- `lib/journal.sh` — `journal_upsert`.
- `skills/rhetoric/fix-redflag` — applies the proposed `firewall_deny` (review-tier, confirmed).
- `baseline-network` — produces `journal/network-baseline.txt`.
