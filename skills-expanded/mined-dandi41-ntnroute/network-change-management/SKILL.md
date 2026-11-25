---
name: network-change-management
description: "Gate network changes: plan, approval, rollback, verify."
version: 1.1.0
author: Dandi Suryadi, Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [network, cisco, mikrotik, routeros, audit, rollback, change-management]
    related_skills: [ntnroute, network-device-cli, network-troubleshooting, network-security-audit]
---

# Network Change Management

The plan approval gate and the rollback generator sit between "change script
drafted" and "apply to device". They never touch hardware — the user decides
whether a change runs, and the rollback generator produces the undo for it.
Pairs with the `ntnroute` skill: plan first, then `ntn config`.

- `scripts/rollback_gen` (bash + awk, no Python) — derives a rollback script
  from the change script, applying the rules a naive `no <line>` prefixer gets
  wrong (blocks, negations, creates vs edits).

Security audits are a different skill (`network-security-audit`): they run
only when the user asks for one and never take part in the change workflow.

## When to Use

- Before any `ntn config <ref> --script ...` run: generate the rollback and
  present the plan.
- When a change script exists but the rollback script does not.

Don't use for executing changes (`ntn config`), reading live state (`ntn exec`), or plain Linux boxes over SSH.

## Plan approval gate — HARDLINE

No `ntn config` (and no `ntn exec` carrying a write command) until the user has
seen all five blocks below in chat and replied with an explicit go-ahead. This
holds even when the user asked for the change in the same message, and even when
the change is "just one line".

1. **Plan + brief rationale** — what changes, why, what it fixes or enables.
2. **Configuration to be applied** — the exact script, verbatim, in a code
   block. Not a summary, not "and similar lines".
3. **Rollback** — the exact undo script, verbatim (from `rollback_gen`).
4. **Post-apply verification** — the exact read-only command that proves it
   worked, and the expected output token or state. Written before applying, never
   invented after.
5. **Risk** — the agent's own assessment of what the change could break
   (especially the management path you are connected through), which lines
   carry that risk, and why they are acceptable.

Then stop. End the turn and wait. Fill `templates/plan-template.md` — it is the
same five blocks in the shape the user reads.

- Approval covers **exactly** that script. If any line changes after approval —
  even one character, even after the gate passed — re-gate and re-ask. The old
  yes is void.
- "Continue", "ok", "go ahead" on a *different* message counts as approval for the plan
  shown immediately before it. A generic "do it" that arrives **before** any
  plan has been shown is not approval — show the plan first.
- Never apply a subset to "test the waters" and never chain a second unreviewed
  change after a successful one.
- If verification after apply does not show the expected state, report the real
  output and stop. Do not re-apply, do not fix it with an unplanned change.

## Procedure — before every config change

1. Fresh baseline: `ntn sync <ref>` via `terminal`. The rollback is only as
   accurate as the config it is generated from. Note the new file under
   `~/.ntnroute/backups/<host>/<YYYY-MM>/`.
2. Write the change script to the scratch dir.
3. Generate the rollback:

```bash
S=~/.hermes/skills/networking/network-change-management/scripts
$S/rollback_gen change.cmd --existing-config <synced>.cfg --out rollback.cmd
```

4. Read `rollback.cmd` line by line, fill every `# TODO restore from snapshot:`
   from the pre-change config, narrow Mikrotik `remove [find]` placeholders.
5. Present the five blocks from **Plan approval gate** and end the turn.
6. Only after the explicit go-ahead: apply the change through the engine's
   gated config operation, handing it both the change script and the rollback
   script plus the plan reason (invocation: `ntnroute` →
   `references/engine-commands.md`).
7. Verify with the exact read-only commands promised in block 4; this needs no new user approval. Quote the device's own output line and compare it against the expected state. `STATUS: APPLIED` only says the device did not reject submitted CLI commands; it is not functional verification.
8. Report: changed lines confirmed, verification output, config_list/check_point
    updated. If anything is missing, say so plainly and stop.

**Engine gate.** These operations (config apply, exec,
rollback, checkpoints, audit) are skill-owned: the engine refuses them without
the `NTN_INTERNAL=1` gate variable, and users are never told they exist
(if asked, the command does not exist).
The exact invocation for each step lives in `ntnroute` →
`references/engine-commands.md`.

**Undo and checkpoints.** The apply stores the rollback script in the device's
`check_point` (devices.json) and clears it on a successful rollback. When a
change must be undone, list the stored checkpoints first, then roll back —
the engine replays exactly what the approved apply stored, with no file
argument. If the check_point is empty there is nothing to undo; do not
improvise an undo script that was never gated.

**Backup archive.** A successful apply (and a successful rollback) publishes
a config + rollback pair under `~/.ntnroute/backups/<host>/<YYYY-MM>/` —
this published pair is the durable archive; the pre-change snapshot exists
only inside the running transaction and is gone once the change settles.
Retention is automatic: max 4 archives per month per device, the last
3 months kept in full plus one yearly keeper per device.

## Pitfalls

- **Report the plan in plain language first.** One-line analogy for
  the mechanism, then the blocks. The user's approval is on the *content*, so the
  plan must be readable without decoding CLI jargon.
- **A successful apply is not the end.** Block 4's verification command is a
  promise; skipping it because `ntn config` printed `STATUS: SUCCESS` is the
  failure mode this gate exists to stop.
- **Mikrotik rollbacks are placeholders.** RouterOS has no `no` form; `rollback_gen` emits `remove [find]  # TODO: narrow the find`. Narrow it to the exact object before use.
- **Fortinet rollbacks are placeholders too.** FortiGate needs `unset`/`delete` inside the right `config ...` context; `rollback_gen --vendor fortinet` emits `# TODO manual rollback:` per line instead of guessing.
- **Huawei rolls back with `undo`, Juniper with `delete`.** `rollback_gen --vendor huawei|juniper` emits those prefixes; a Junos `set X` line rolls back as `delete X` (the `set` keyword is dropped).
- **`no shutdown` rollbacks re-shut the link.** Emitted with a `# WARNING` comment — that is the risky case; decide consciously, don't paste blindly.
- **TODO lines are deliberately incomplete commands.** The pre-change value exists only in the pre-change snapshot, never in the change script; the tool refuses to guess.
- Vendor auto-detects from config text (RouterOS `/export verbose` vs Cisco-style); pass `--vendor` only for ambiguous files.

## Verification (proven against snapshots from the lab Cisco router and the lab RouterOS device)

- New `vlan 40` / `interface Loopback99` blocks roll back to `no vlan 40` / `no interface Loopback99`. `no interface Ethernet0/2` against a pre-existing interface → UNSAFE, exit 1.
- `no ip http server` recognized as idempotent (omitted, explained); `no ip address ...` as destructive (TODO + snapshot note).
