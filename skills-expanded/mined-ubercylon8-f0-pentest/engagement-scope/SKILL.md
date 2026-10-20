---
name: engagement-scope
description: "Authorization and scope gate for offensive testing. Load FIRST in any offensive session. Defines rules of engagement, in-scope targets, window, and evidence trail; verifies every target before a tool touches it."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# Engagement Scope

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


The non-negotiable first step of any offensive session. Nothing — not even passive
recon — runs until an authorized scope is loaded and the target is confirmed in it.
Every other offensive skill depends on this one.

## When to Use

- At the very start of any web or network offensive session.
- Before invoking any other `offensive-*`, `web-*`, or `ad-*` skill (the bundles load this first).
- Whenever the target, engagement, or authorization changes mid-session.

## Quick Reference

Scope file schema (`<active-engagement>/scope.yaml`):

```yaml
engagement:
  name: "Acme Q3 external webapp"
  authorization_ref: "SOW-2026-014 / signed RoE 2026-06-01"   # REQUIRED — no auth ref, no run
  operator: "your-handle"
  window: { start: "2026-06-20T00:00:00Z", end: "2026-07-04T23:59:59Z" }
  contacts: ["client-soc@acme.example"]
in_scope:
  domains: ["*.acme-staging.io", "app.acme.io"]
  cidrs:   ["203.0.113.0/24"]
out_of_scope:                       # explicit deny always wins over in_scope
  domains: ["blog.acme.io", "*.prod.acme.io"]
  cidrs:   ["203.0.113.200/29"]
allowed_actions:
  passive_recon: true
  active_scan:   true
  exploitation:  gated              # true | false | gated  (gated = human approval required)
  destructive:   false
autonomy:
  mode:           gated             # gated (default) | supervised-auto
  spray_override: false             # supervised-auto STILL gates lockout-risk spraying unless true
```

### Autonomy & irreversible actions

`autonomy.mode` controls how **irreversible** commands — spraying, secret replication
(DCSync/secretsdump), remote exec (psexec/wmiexec/atexec/evil-winrm), AD writes (bloodyAD/dacl/RBCD),
coercion+relay (ntlmrelayx/krbrelayx/responder/coercer), cert issuance (certipy), and stateful web
exploitation — behave when the chain runs under an autonomous driver:

| `autonomy.mode`   | Reversible actions | Irreversible actions |
| ----------------- | ------------------ | -------------------- |
| `gated` (default) | run autonomously   | gated — the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) stops the chain to require approval |
| `supervised-auto` | run autonomously   | allowed — but a stage briefing (blast radius + revert) is posted first |

Independent of mode:
- **Lockout-risk password spraying always requires approval** unless `autonomy.spray_override: true`.
- `allowed_actions.exploitation: false` → all irreversible actions are denied outright.
- No active engagement / no `authorization_ref` → denied.

Gate a target before any tool call:

```bash
python3 <skill-dir>/scripts/scope_check.py \
    --scope "<active-engagement>/scope.yaml" --target <domain|ip|url> --action <action_class>
```

Exit codes: `0` in scope + permitted · `1` out of scope / not permitted · `2` error/no scope · `3` outside window.

## Procedure

1. **Load scope.** Read `<active-engagement>/scope.yaml`. If it is missing or has no `engagement.authorization_ref`, **STOP** and ask the operator to provide an authorized scope. Do not proceed, do not improvise a scope.
2. **Sanity-check the engagement.** Confirm the window covers the current date, that `in_scope` is specific (flag bare wildcards like `*` or `*.com`), and that `out_of_scope` exclusions are present where expected.
3. **Open the audit trail.** Ensure `<active-engagement>` exists; start a session log there (timestamp, engagement name, authorization_ref, operator). Every subsequent skill appends evidence and actions here.
4. **Gate every target.** Before any other skill runs a tool against a host, call `scope_check.py` for that host with the appropriate `--action`. Treat any non-zero exit as a hard stop for that target.
5. **Honor the action tiers.** `passive_recon`/`active_scan` may proceed when allowed. `exploitation` and `destructive` are **reversibility-gated**: anything irreversible or that changes target/third-party state is governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` (see *Autonomy & irreversible actions* above). In `gated` mode it stops for approval before execution; in `supervised-auto` it runs after you post the stage briefing. Lockout-risk spraying always stops for approval unless explicitly overridden. Never hand-wave an irreversible action past the gate.
6. **Re-check on change.** If the target or engagement changes, repeat from step 1.

## Pitfalls

- **Wildcard over-reach.** `*.acme.io` can include third-party-hosted subdomains or shared CDN tenants you are not authorized to touch. Prefer explicit hosts; keep an `out_of_scope` list.
- **Shared/CDN IPs.** A resolved IP may belong to Cloudflare/Akamai, not the client. Confirm ownership before treating an IP as in-scope.
- **Expired or not-yet-started window.** `scope_check` returns `3`; stop until the window is active.
- **Scope drift mid-chain.** A chain that pivots to a new host must re-gate that host — do not assume the chain inherits scope.
- **Silent default-deny.** A typo in a target reads as out-of-scope (good) — but verify you tested the host you meant.

## Verification

- `scope_check.py` returns `0` for a known in-scope host and `1` for a known out-of-scope host.
- The scope file parses and contains a non-empty `authorization_ref`.
- The evidence directory is writable and a session log entry was created.
