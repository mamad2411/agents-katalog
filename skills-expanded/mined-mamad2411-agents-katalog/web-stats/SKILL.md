---
name: web-stats
description: "EXPRESS: privacy-respecting web-traffic analytics from the server's own access logs — page views, unique visitors, top pages, referrers, status mix, bots-vs-humans, daily trend. On-demand only; never part of the loop. A GDPR-friendly alternative to third-party analytics."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# web-stats (Rhetoric / Express)

Turns the access logs your web server already keeps (for security) into a decent
traffic report — **without** Google Analytics, cookies, JavaScript beacons, or any
third party. This is the standalone analytics feature: it is run **on demand** by the
operator (`/watchman stats`) and is deliberately **NOT** invoked by the audit/loop
cycle. Read-only.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## Privacy model (the whole point — keep the claim honest)

- The client IP is used **only transiently, in memory**, to correlate visits (so one
  visitor reloading a page does not inflate page views or visitor counts). It is **never
  written, hashed-and-stored, or printed** — the report is pure anonymous aggregates.
- **No cookies, no third parties, no beacon.** The data is the logs the server already
  keeps under its security/legitimate-interest basis; this adds **zero new exposure** and
  nothing leaves the host.
- Do not "improve" accuracy by exposing or persisting IPs. If the operator ever wants the
  **real** offending IP (a DDoS/abuse block), that is a SEPARATE security path on a
  different legal basis (defending the system) handled by `inspect-logs` + `fix-redflag` —
  it is not this report.

## When to use

On demand, via `/watchman stats`. Never wire this into the audit or loop orchestration —
it is an operator-run analytics feature, not an observe/analyze step.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher — `bash lib/wm
   <function> [args…]` — which sources the libs (`lib/distro.sh`, `lib/webstats.sh`) under
   bash internally; never `source lib/…` directly (dontAsk refuses a dot-source). (No
   journal write — this skill reports analytics, it does not record findings.)
2. **Confirm there is a web surface.** `bash lib/wm webserver_detect` — if no web server /
   no access logs, say so plainly and stop. The logs are found via `bash lib/wm
   webserver_log_paths` (current + rotated + `.gz`).
3. **Run the engine.** `bash lib/wm webstats_report` computes the aggregates with awk (fast
   over large and rotated logs; the IP never leaves the awk pass) and prints the report:
   page views, unique visitors, total requests, bots-vs-humans %, bandwidth, top pages **by
   unique visitors** (dedup'd so reloads don't skew), top external referrers, status-code
   mix, and the daily trend.
4. **Per-site (optional).** When the host serves multiple vhosts, run `bash lib/wm
   webstats_report <site-access-log>` per site using the log paths from `inspect-web-config`'s
   site index, so each site gets its own numbers.
5. **Present and interpret.** Show the report, then add brief plain-language insight a raw
   tool can't — e.g. "bots are 40% of raw hits, so the human page-view number is the one
   to trust", a spike in the daily trend, a 404-heavy path worth fixing, an unexpected
   referrer. Never invent numbers; interpret only what the engine produced.
6. **Stay read-only and anonymous.** Never print or persist an IP, never write a file,
   never touch config or the firewall. Acting on what you see (blocking, tightening) is
   `fix-redflag`'s job under the risk tiers.
<!-- /origin -->

## Grounding

- `lib/webstats.sh` — the parsing engine (`webstats_report`, `webstats_access_logs`,
  reached via `bash lib/wm`); the privacy model lives here in code.
- `lib/distro.sh` — `webserver_detect`, `webserver_log_paths` (find the access logs),
  reached via `bash lib/wm`.
- `skills/grammar/inspect-web-config` — the per-site index, for per-vhost breakdowns.
- `skills/grammar/inspect-logs` / `skills/rhetoric/fix-redflag` — the SECURITY path
  (real-IP abuse/DDoS finding → operator-confirmed firewall rule), distinct from this
  anonymized analytics report.
- `manifest.json` — declared permissions (`reads: webserver_log_paths`).
