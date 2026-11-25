---
name: check-security-currency
description: "OBSERVE: are the defenses being kept CURRENT? Pending security updates / known-CVE packages, threat-intel freshness (CrowdSec hub, ClamAV signatures, AIDE db), and whether the auto-update automation is even on — across Debian/RHEL/Arch. Detect + propose; never auto-applies."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# check-security-currency (Grammar / Observe)

Config checks ask "is it set up right." This asks the **time-based** question: *is it
up to date, and is something keeping it up to date* — so a once-hardened box doesn't
quietly drift open as attackers gain new tricks. The journal tracks staleness as a
trend, so the loop **emails you when a fresh defense goes stale** (a regression). Works
across Debian/RHEL/Arch through the resolvers. Read-only `security`/`config`/`integrity`
findings.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## The pattern it enforces: automate the freshness, then guard the automation

Manual update-nagging doesn't scale. The durable way to "keep defenses current" is
**automation** — auto security-updates, auto threat-intel refresh — and this skill's job
is to **verify that automation is on and catch it when it drifts off, stale, or failing**.
It NEVER syncs the network (no `apt update`/`pacman -Sy`) and NEVER applies an update:
an update can break a production server, so every finding is **detect-and-propose** at
`review`/`manual` tier — the operator applies it via `watchman fix`, or (better) turns on
the automation and lets the loop verify it stays on.

## When to use

Every `/watchman audit` / `/watchman loop`. Relevant on both profiles — a workstation needs
current defenses too.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs (`lib/journal.sh`,
   `lib/distro.sh`, `lib/profile.sh`, `lib/security_currency.sh`, `lib/io-courtesy.sh`)
   under bash internally; never `source lib/…` directly (dontAsk refuses a dot-source).
   Initialize with `bash lib/wm journal_init`. Determine the machine's family and profile by
   running `bash lib/wm watchman_family` and `bash lib/wm watchman_profile` and reading the
   printed values — use them to decide which checks apply. You do NOT pass them to
   journal_upsert (it auto-resolves them; pass `"" ""`). Gate:
   `bash lib/wm profile_runs_check security_currency` (runs in both profiles).
   **I/O courtesy:** the package-DB queries touch disk — IF
   `bash lib/wm io_should_defer_heavy`, journal a `capacity`/`info`/`safe` `diagnostic_deferred`
   (`target=check-security-currency`) and skip this pass.
2. **Scan.** Run `bash lib/wm seccur_scan`. Read-only — it reads CACHED package state (no network sync)
   and stats local threat-intel files; it emits one TSV finding-candidate per staleness
   signal: `category \t severity \t risk_tier \t check_id \t target \t title \t detail \t remediation`.
   No output = the defenses look current.
3. **Journal each record** through the dispatcher exactly as emitted
   (pass `"" ""` for family/profile — journal_upsert auto-resolves them):
   `bash lib/wm journal_upsert "" "" <category> <severity> <risk_tier> <check_id> <target> <title> <detail> <remediation>`.
   On Darwin the resolvers behind `seccur_scan` behave platform-specifically: `pkg_db_age_days`
   measures days since the last `brew update` (Homebrew git FETCH_HEAD mtime); `autoupdate_enabled`
   reads macOS Software Update prefs (`com.apple.SoftwareUpdate AutomaticCheckEnabled`);
   `pkg_list_upgradable` uses `brew outdated --formula`; `security_update_cmd` is
   `brew upgrade && softwareupdate --install --all`; and `vuln_scanner` returns `none` (no CVE
   scanner exists for Homebrew packages — surface that gap in the finding `detail`).
   `target` is the subject (packages / cve / clamav / a mechanism) so the fingerprint is
   stable and a re-stale defense **regresses loudly** on the next run.
4. **Tiers — never apply.** `security_updates_pending`, `vuln_packages`, `auto_security_updates_off`,
   `*_stale` are `review` (the fixer shows the exact update command and confirms);
   `pkg_db_stale` and `aide_db_missing` are `manual` (investigate / initialize). NEVER run an
   update, install, or any package sync here — propose the command, the operator decides.
5. **Summarize.** Lead with the highest-severity currency gap and the one-line action. On
   Darwin, if `vuln_scanner=none`, note that CVE scanning for Homebrew packages is not
   available and recommend periodically reviewing `brew audit --cask` manually. If clean,
   say the defenses look current.
<!-- /origin -->

## Grounding

All claude-watchman functions below are reached via `bash lib/wm <function>` — the
dispatcher sources these libs internally; never `source lib/…` directly.

- `lib/security_currency.sh` — `seccur_scan` (the freshness engine; thresholds
  `WATCHMAN_SIG_STALE_DAYS` / `WATCHMAN_UPDATE_STALE_DAYS`).
- `lib/distro.sh` — `security_update_cmd`, `pkg_db_age_days`, `vuln_scanner` / `vuln_scan`,
  `pkg_list_upgradable`, `autoupdate_mechanism` / `autoupdate_enabled` (the cross-platform layer).
- `lib/profile.sh` — `profile_runs_check security_currency`.
- `lib/io-courtesy.sh` — `io_should_defer_heavy` (defer under load).
- `lib/journal.sh` — `journal_upsert` (per-subject findings; staleness regresses over time).
- `skills/rhetoric/fix-redflag` — applies the proposed update commands (review-tier, confirmed).
- `manifest.json` — declared permissions.
