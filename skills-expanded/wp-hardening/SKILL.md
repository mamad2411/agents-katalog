---
name: wp-hardening
description: >
  Safely harden a WordPress site — "lock the doors so it doesn't happen again." Runs over ANY connected
  WordPress MCP gateway (SproutOS recommended) or SSH+WP-CLI. Applies idempotent, reversible hardening:
  disable the file editor, turn off debug output, rotate salts, block PHP execution in uploads, disable
  directory listing, add non-breaking security headers, cap revisions, enable minor auto-updates — and,
  with confirmation, the riskier controls (fix file permissions, FORCE_SSL_ADMIN, HSTS, disable XML-RPC,
  hide REST user enumeration, limit-login, DISALLOW_FILE_MODS). Every change is classified
  SAFE / RISKY / MANUAL by blast radius, wrapped in sentinel markers so it is idempotent and cleanly
  reversible, and gated on a confirmed backup. Use when the user asks to harden or secure a WordPress
  site, apply a security checklist, or close the entry vector after a cleanup. For a read-only posture
  score first use wp-security-audit; to remove an active infection use wp-malware-removal.
license: AGPL-3.0-or-later
metadata:
  author: Aditya Sharma (adityaarsharma.com)
  version: 1.0.0
  homepage: https://github.com/adityaarsharma/wordpress-malware-removal
---

# WordPress Hardening

You apply and recommend WordPress hardening **safely and reversibly**. The engine is
`scripts/harden_actions.py` — a catalog of idempotent actions, each classified by blast radius:

- **SAFE** — near-zero chance of breaking a working site → auto-apply (still through the gate).
- **RISKY** — can break a plugin or lock users out → **ask the human first**, then apply with `--force`.
- **MANUAL** — needs human judgment or infra outside WP-CLI → **present, never auto-execute**.

One of three sibling skills: **wp-security-audit** (posture), **wp-malware-removal** (clean a hack), this
**wp-hardening** (close the door). Shared gateway contract in `references/gateway.md`; full control
reference in `references/hardening.md`.

**Never harden a site you haven't confirmed is clean.** Hardening a live infection just locks the
attacker's backdoor in. If there's any sign of compromise, run wp-malware-removal first.

---

## Step 0 — Establish the gateway & prerequisites
Read `references/gateway.md`. Detect access (SproutOS MCP ▸ other WP MCP ▸ SSH+WP-CLI), and critically
detect the **server type** (Apache vs Nginx — decides whether a control is a `.htaccess` edit or a
server-block change + reload) and dependencies (`wp plugin is-active jetpack` before touching XML-RPC;
a valid TLS cert before FORCE_SSL_ADMIN/HSTS).

**Backup gate (non-negotiable for anything but read-only listing):** the tool does **not** create the
backup. Before applying any RISKY action or any change you can't sentinel-rollback, hard-remind the user
to take a full off-site backup and register a snapshot via `scripts/safety_gate.py` so destructive steps
are mechanically blocked without one.

---

## The flow: list → plan → apply-safe → ask-risky → present-manual

1. **List / triage.** `python3 scripts/harden_actions.py list` shows all actions by class. If the user
   ran **wp-security-audit** first, work its ranked fix list — each fix is already tagged safe/risky/manual.
2. **Plan (gateway/MCP mode).** `python3 scripts/harden_actions.py plan --wp-path WPROOT --site https://SITE
   --json plan.json` emits the exact **apply / verify / rollback** commands for every action. Over an MCP
   gateway (no local shell), you run those emitted commands through the gateway's verbs. Over SSH you can
   let the script execute them directly.
3. **Apply SAFE (auto).** `python3 scripts/harden_actions.py apply --wp-path WPROOT --site https://SITE`
   dry-runs every SAFE action; add `--commit` to execute. Server-config edits are wrapped in
   `# BEGIN/# END wp-malware-hunter-harden:<id>` sentinels — **idempotent** (re-runs don't duplicate) and
   **cleanly reversible**. `wp config` actions are idempotent by nature (`set` updates-or-adds).
4. **Ask before RISKY.** For each RISKY action, **explain the tradeoff and get explicit confirmation**,
   then `apply --action <id> --force --commit`. Detect the dependency first (Jetpack for XML-RPC, TLS for
   HSTS/FORCE_SSL_ADMIN, web-server user for permissions). For file-permission changes capture
   `getfacl -R WPROOT > perms.bak` **before** so rollback is exact.
5. **Present MANUAL.** List them with the exact commands as recommendations — CSP (Report-Only first),
   least-privilege DB user, admin/App-Password review, rename-admin, 2FA enrollment, fail2ban/WAF, hiding
   wp-login. **Never auto-execute; never auto-delete users or revoke App Passwords** — those kill live
   integrations; list for the human and act only on confirmation.
6. **Verify each applied action** with its `verify` command (e.g. `curl -sI SITE | grep -i x-frame`,
   `wp config get DISALLOW_FILE_EDIT`). Record the result; if a change regressed the site, **roll back**
   (`harden_actions.py rollback --action <id> --commit`) and mark it MANUAL.

---

## Tie hardening to the entry vector (when following a cleanup)
If wp-malware-removal attributed the breach, apply the matching control **first**:
- **Stolen credentials / infostealer** → rotate salts (`shuffle_salts`), force password resets, **2FA**
  (MANUAL enrollment), limit-login, revoke unexpected App Passwords. A stolen password alone must not
  grant access again.
- **Plugin/theme CVE** → update or remove the flagged component; enable minor auto-updates.
- **Uploaded PHP payload** → `block_php_uploads` + fix permissions.
- **Infected operator machine** → tell the user to clean that machine and rotate creds from a *different*
  device, or it reinfects.

---

## Idempotency & rollback contract
- Every server-config edit lives inside a sentinel block, so applying twice is a no-op and rollback
  removes exactly what we added — nothing else in the file is touched.
- `wp config` constants roll back to `false` / delete.
- `shuffle_salts` and `remove_readme` are not "rolled back" (re-login / restore-from-backup) — the plan
  says so honestly.
- Actions that need two steps to be safe (disable wp-cron + add system cron) must **both land or neither**
  — classified so they are never half-applied automatically.

## The report
- **Applied (SAFE):** each action + its verify result.
- **Applied on confirmation (RISKY):** what, why it was safe to do here, rollback command.
- **Recommended (MANUAL):** the checklist with exact commands and the human judgment each needs.
- **Verify evidence:** the `curl`/`wp config get` output proving each change took effect.
- **Residual risk + still-to-do**, stated plainly. Hardening reduces attack surface; it is not a
  guarantee. Point back at wp-security-audit for a re-score.

## Bundled resources
- `references/gateway.md` — reach the site over SproutOS / any WP MCP / SSH+WP-CLI.
- `references/hardening.md` — the full SAFE/RISKY/MANUAL control reference (what/apply/verify/rollback/source).
- `scripts/harden_actions.py` — the idempotent, reversible action engine (`list`/`plan`/`apply`/`rollback`).
- `scripts/safety_gate.py` — code-enforced backup + rollback for destructive steps.
