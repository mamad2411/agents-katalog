---
name: inspect-web-config
description: "OBSERVE: index every web vhost/server block — config file+line, CORS policy, security headers, log paths — and journal per-site findings so the audit can reference each site and the fixer can maintain the exact directive."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# inspect-web-config (Grammar / Observe)

Builds a **per-site index** of the web configuration. For each virtual host /
server block it records where the site is defined and what it declares — CORS,
security headers, log paths — and journals one finding per site+concern. The
journal IS the index: the audit references each site, re-runs update in place
(stable fingerprint), and the fixer knows the exact file and directive to change.
Read-only — it observes and records; remediation is `fix-redflag`'s job.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

Every `/watchman audit` / `/watchman loop` on a **server** profile, after
`inventory-services` (so the web-server surface is known). It is the detector that
feeds the `web_cors_policy` / `web_security_headers` severities already declared in
`lib/profile.sh` and the remediation surface in `skills/rhetoric/fix-redflag`.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never
   `source lib/…` directly (dontAsk refuses a dot-source). Initialize with
   `bash lib/wm journal_init`. Determine the machine's family and profile by running
   `bash lib/wm watchman_family` and `bash lib/wm watchman_profile` and reading the printed
   values — you do NOT pass them to journal_upsert (it auto-resolves them; pass `"" ""`).
   These are **server-direction** checks: if
   `bash lib/wm profile_runs_check web_cors_policy` and
   `bash lib/wm profile_runs_check web_security_headers`
   are BOTH false (a workstation), do nothing — the workstation-actually-serving-public
   case is already surfaced by `inventory-services` (which tells the operator to switch
   to the server profile). Resolve the two base severities by running
   `bash lib/wm profile_severity web_cors_policy` and use the printed level as the literal
   severity for the CORS finding, and `bash lib/wm profile_severity web_security_headers` and use
   the printed level as the literal severity for the security-header findings.
2. **Discover the surface.** Use `bash lib/wm webserver_detect` (which web servers are present)
   and `bash lib/wm webserver_config_roots` (their `/etc` config roots). No web server → nothing
   to index; return.
3. **Enumerate per-site blocks (config-derived, block-aware).** Read the config files
   under each root with the Read tool and parse them STRUCTURALLY — this is where the
   in-session model beats brittle line-grep:
   - **nginx:** every `server { … }` block across `nginx.conf`, `sites-enabled/*`,
     `conf.d/*`. Capture: `server_name` (site identity), `listen` (port), the defining
     **file:line**, `add_header` directives (security headers), `Access-Control-Allow-Origin`
     (CORS), `access_log`/`error_log` (log paths). Honor `include` directives.
   - **apache:** every `<VirtualHost …>` block. Capture: `ServerName`, the `<VirtualHost :port>`,
     **file:line**, `Header set` / `Header always set` (headers), CORS (`Header set
     Access-Control-Allow-Origin`, or `SetEnvIf`-driven), `CustomLog`/`ErrorLog`.
   Use the resolver vocabulary — never assume a single config path or a distro layout.
4. **Journal one finding per site+concern** through `lib/journal.sh` (create-or-update;
   never duplicate — the fingerprint is `family+profile+category+check_id+target`, and
   `target=<site>` keeps each site stable across runs):
   - **Per-site index row** (context, not an alarm): `category=config`, `severity=info`,
     `risk_tier=safe`, `check_id=web_site_index`, `target=<server_name>`; detail names the
     config **file:line**, listen port, and resolved log dirs.
   - **CORS:** if `Access-Control-Allow-Origin` is `*` (most serious when the site is
     authenticated/credentialed) → `category=security`, `severity=<the CORS level printed by
     bash lib/wm profile_severity web_cors_policy>`,
     `risk_tier=review`, `check_id=web_cors_policy`, `target=<server_name>`; detail quotes
     the value and the **file:line**; remediation = restrict to the explicit allowed
     origins (operator decides which — that is why it is `review`, never auto-applied).
     A site with no CORS header is not itself a finding.
   - **Security headers** — for each of **HSTS** (`Strict-Transport-Security`),
     **X-Frame-Options**, **X-Content-Type-Options**, **Referrer-Policy**: if absent on
     the site → `category=security`, `severity=<the header level printed by
     bash lib/wm profile_severity web_security_headers>`, `risk_tier=review`,
     `check_id=web_security_headers_<hsts|xfo|xcto|referrer>`, `target=<server_name>`;
     remediation = the exact `add_header` / `Header always set` directive to add, naming
     the file. **Content-Security-Policy** absent → same shape but
     `check_id=web_security_headers_csp`, `risk_tier=manual` — a correct CSP is too
     context-specific to generate safely (the canonical manual-tier example); explain it
     and hand it back, never auto-apply.
5. **Respect the risk tiers and the Prime Directive.** This skill NEVER edits a config —
   it only reads and journals. Applying any of these is `fix-redflag`'s job, shown-and-
   confirmed per finding (`review`) or handed back (`manual`).
6. **Stay family-blind.** Reach the web surface only through the `webserver_*` resolvers;
   never hard-code `/etc/nginx` vs `/etc/httpd` or a single config path.
<!-- /origin -->

## Grounding

All claude-watchman functions below are reached via `bash lib/wm <function>` (never a
direct `source`); the lib files are where they live.

- `lib/distro.sh` — `webserver_detect`, `webserver_config_roots`, `webserver_log_paths`
  (config-derived web-server discovery; the entry point for finding each site's config).
- `lib/profile.sh` — `profile_severity` (`web_cors_policy`, `web_security_headers`),
  `profile_runs_check` (server-only direction).
- `lib/journal.sh` — `journal_upsert` (per-site findings; `target=<server_name>` is the
  stable key), `journal_set_status`.
- `skills/rhetoric/fix-redflag` — the remediation surface these findings feed (`review`
  for CORS/most headers, `manual` for CSP).
- `manifest.json` — declared permissions (`reads: webserver_config_roots`).
