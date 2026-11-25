---
name: check-shell-history
description: "OBSERVE: detect whether the forensic trail has been WIPED — shell history (all users + root) redirected to /dev/null, history-disabled in a shell rc, world-readable, or login records (wtmp) truncated. Metadata only — never reads what users typed."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# check-shell-history (Grammar / Observe)

Answers one question across **every login user and root**: *has someone wiped the
evidence?* Clearing `~/.bash_history`, pointing it at `/dev/null`, disabling history
in a shell rc, or truncating `/var/log/wtmp` are textbook post-compromise moves. This
is the detective complement to `check-log-retention` (which asks whether logs are kept
at all). Read-only; `integrity`-category findings.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## What it does and does NOT read

- **Metadata only.** It judges tampering from size / symlink target / mode / owner /
  immutable bit / shell-rc settings / "logged in but no history" — it **never reads the
  CONTENTS** of anyone's shell history. That is both more reliable than grepping for "bad
  commands" and privacy-respecting (it does not expose what users typed).
- **Most effective as root** (the deployment): it can stat every home. A home it cannot
  traverse is **skipped, never false-flagged**.
- **Honest limit:** a root-level attacker can also tamper with the journal. The durable
  value is the loop's regression **email**, which leaves the host before suppression — plus
  steering the operator toward append-only logging (auditd / remote syslog) as the real fix.

## When to use

Every `/watchman audit` / `/watchman loop`. Relevant on both server and workstation
profiles (any box with users or root).

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never
   `source lib/…` directly (dontAsk refuses a dot-source). Initialize with
   `bash lib/wm journal_init`. Determine the machine's family and profile by running
   `bash lib/wm watchman_family` and `bash lib/wm watchman_profile` and reading the printed
   values — use them to decide which checks apply. You do NOT pass them to journal_upsert (it
   auto-resolves them; pass `"" ""`). Gate:
   `bash lib/wm profile_runs_check shell_history_integrity` (runs in both profiles). If running
   non-root, note in the summary that unreadable homes were skipped.
2. **Scan.** Run `bash lib/wm shellhist_scan`. It enumerates login users + root
   (`bash lib/wm shellhist_login_users`) and emits one TSV finding-candidate per tamper indicator:
   `category \t severity \t risk_tier \t check_id \t target \t title \t detail \t remediation`.
   No output = the trail looks intact (journal nothing — absence is not a finding).
3. **Journal each record** through the dispatcher exactly as emitted — for each line
   (pass `"" ""` for family/profile — journal_upsert auto-resolves them):
   `bash lib/wm journal_upsert "" "" <category> <severity> <risk_tier> <check_id> <target> <title> <detail> <remediation>`.
   `target` is the user (or the file/path) so the fingerprint is stable and a re-wiped trail
   **regresses loudly** on the next run.
4. **Tiers are mostly `manual`.** A wiped history is **detect-and-explain**, not auto-fixed:
   `shell_history_devnull`, `shell_history_disabled`, `login_record_wiped`,
   `shell_history_login_gap` are `manual` (investigate). Only a permission fix
   (`shell_history_perms` → `chmod 600`) is `review`. Never re-enable history, remove an
   immutable bit, or restore a file yourself — hand it to the operator.
5. **Summarize.** If there are findings, lead with the highest-severity tamper signal and
   what it implies (possible compromise); if clean, say the forensic trail looks intact and
   note any homes skipped for lack of access.
6. **Read-only.** Never modify a history file, a permission, an rc file, or a log. Acting is
   the operator's call.
<!-- /origin -->

## Grounding

These functions are reached via the dispatcher (`bash lib/wm <function> [args…]`), never by
dot-sourcing the libs directly.

- `lib/shellhist.sh` — `shellhist_scan`, `shellhist_login_users` (the metadata engine; the
  privacy model and the tamper heuristics live there).
- `lib/profile.sh` — `profile_runs_check` / `profile_severity` (`shell_history_integrity`).
- `lib/journal.sh` — `journal_upsert` (per-user/per-path findings; stable fingerprints).
- `check-log-retention` — the proactive "are logs kept" counterpart to this detective check.
- `manifest.json` — declared permissions (`reads: /home, /root`; `last`/`stat`/`lsattr`/`getent`).
