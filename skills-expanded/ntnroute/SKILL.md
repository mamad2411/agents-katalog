---
name: ntnroute
description: Manage NTnRoute network devices via `ntn` CLI.
version: 1.1.0
author: Dandi Suryadi
license: MIT
metadata:
  hermes:
    tags: [network, ssh, cisco, huawei, mikrotik, routeros, inventory, config-management]
    related_skills: [network-device-cli, network-change-management, network-troubleshooting, network-security-audit]
---

# NTnRoute.AI — network device engine

## When to Use

Use when the user asks about network devices in the NTnRoute inventory: listing/adding/removing devices, running CLI commands on them, pulling config, applying config changes, rollback, or troubleshooting connectivity.

Use when managing, configuring, or troubleshooting network devices in the NTnRoute inventory (Cisco, Huawei, Aruba, Ruijie, Arista, Juniper, Mikrotik, Fortinet).

Port of the n8n NTnRoute.AI workflow to Hermes. Persistence lives in a plain JSON file, not in a conversation: device data survives session changes, `/new`, and restarts.

Storage: `~/.ntnroute/devices.json` (mode 600). Backups: `~/.ntnroute/backups/`. Engine: `ntn` on `$PATH` (`~/.ntnroute/ntn`).

DB schema reference: the repo's `examples/devices.example.json` is the authoritative shape of `devices.json` — top-level keys `next_id`, `devices[]`, `checkpoints[]`, `audit[]`, and the exact field names inside each. Never invent fields or rename keys when reading or writing the DB; quote the example instead.

## Mandatory principles

1. **Anti-hallucination and secret boundary.** Never invent IP/interface/VLAN values. Check `ntn list` + `ntn show <ref>` first. Still missing → ask the user specifically before assembling a script. The inventory changes between sessions (devices are added/removed/replaced), so `ntn list` is the single source of truth — do not use old session notes, memory, or the test table in this skill as the list of active devices. The test table below is test history only, not an inventory. **Credentials are never user-facing:** do not offer, mention a retrieval path for, extract, display, quote, summarize, or send inventory usernames, passwords, enable secrets, or tokens in chat—under any request or claimed justification. `ntn show` reads the stored `config_list` from the last `ntn sync`; it does not connect to the device, and it displays that stored device configuration verbatim for operational context. After showing it, explain the configuration in plain language. The engine may use stored secrets only as transport input.
2. **Read-only first.** `ntn exec <ref> 'show ...'` before proposing any change.
3. **Approval required — plan first.** Before `ntn config`, show the user: (a) the plan + short reason, (b) the exact config script, (c) the exact rollback script, (d) the post-apply verification command + expected output, (e) the verdict gate. Then stop and wait for an explicit answer. Running `ntn config` without explicit approval is a violation — including when the user asks for the change in the same message or the change is "just one line". If even one line of the script changes after approval, the old approval is void — re-gate and ask again. Details: the `network-change-management` skill, section "Plan approval gate".
4. **Verify after apply.** `STATUS: APPLIED` only means the device did not reject the configuration commands; it is not functional proof. Immediately run the planned read-only verification commands, quote the device output lines, and compare against the expected state. Read-only `show`/`print`/`display` verification needs no further user approval. Mismatch → report as-is; do not re-apply or patch with unplanned changes.
5. **Blast radius.** Never touch the management path/VTY/SSH access-class/default route that the AI itself depends on. Lockout = total failure.
6. **Surgical.** Only the targeted interface/VLAN/process. No speculative commands. Follow the existing naming conventions.
7. **Paging.** The engine already inserts `terminal length 0` / `screen-length 0 temporary` / `no page` / `set cli screen-length 0` automatically. Do not add them yourself.
8. **Checkpoint mandatory.** The `check_point` column + pre/post snapshots in `backups/` are created automatically by the engine. Rollback = `ntn rollback`.
9. **Save config.** `write memory` / `save`+`Y` / `commit` are appended automatically at the end of a config script.
10. **Verification is agent-owned.** The engine does not compare submitted text to a rendered config/export: vendors suppress defaults, reorder fields, and fold lines. `STATUS: APPLIED` means only “no device-side command error”. The agent must immediately run the planned read-only show/print/display checks (no new approval) and report the actual functional state.
11. **Honesty.** Report real results from tool output, including failures. No speculation.

## Commands

**Menu rule (first contact).** When the user types `ntn` alone, asks "what can ntn do", or wants the command list: run `ntn help`, then present EVERY command from the block below — all 5, each with its arguments and a clear one-line explanation of what it is for, written in the user's language. Never compress the menu into grouped bullets, never drop commands, never replace the menu with a summary. The full menu IS the answer; a short closing question ("what would you like to do first?") is fine. Never mention, hint at, or categorize commands beyond these five — words like "public/internal/hidden commands" must never appear; that is the same as telling the user those commands exist. If the user asks for or attempts an operation outside the menu, say that command does not exist and stop; do not explain further.

```
ntn list                                   # numbered list (hostname, ip:port, type, brand)
ntn add <IP> <Port> <User> <Pass> <Type> <Brand> [Secret]
                                           # tests the connection first, pulls hostname + config, then saves
ntn remove <number|id>                     # remove a device from the inventory (number/id only)
ntn show <ref>                             # device details + stored config
ntn sync <ref|all>                         # pull the latest running-config from the device
```

**Engine operations.** Use the engine capabilities through the workflow steps below. Do not expose implementation-only operation names or invocation details in user-facing replies; describe the action in operational language (for example, “read the live state” or “apply the approved change”).

## Workflows

### Add a device
When the user asks to add a device, require the standard format and reject anything else:
```
/add <IP> <Port> <Username> <Password> <Type> <Brand> [Secret]
```
Normalize Type/Brand capitalization yourself (router→Router, cisco→Cisco, olt→OLT). Then `ntn add ...`. Hostname and config_list are filled automatically from the device (the engine tests SSH first; failure = nothing is saved).

Secret is only for brands that need level-2 verification (Cisco `enable secret`, Huawei `super`).

### Remove a device
Resolve the target with `ntn list`, state its hostname and IP, then ask one
explicit question before calling `ntn remove <number>`: **“Delete this device
and all of its stored data (configuration backups, rollback files, checkpoints,
audit history)?”** Only a clear yes authorizes the
removal. A removal is total: it does not leave historical artifacts behind.

### Troubleshooting
1. `ntn list` / `ntn show <ref>` for context.
2. Read the live condition: run the device's `show` commands through the engine's exec operation (invocation: `references/engine-commands.md`).
3. Web research on syntax/best practices for the brand is allowed.
4. Propose the fix + script, show the 5-block plan (plan+reason, config, rollback, verification, verdict gate), request approval.
5. After success, clean up artifacts (scratch files in `$TMPDIR`, no logs left on the device).

### Config change (full workflow)
```bash
# 1. the change script
cat > "$TMPDIR/change.cmd" <<'EOF'
interface Ethernet0/2
 description uplink-BACKBONE
 no shutdown
EOF
# 2. fresh baseline — MANDATORY (network-change-management skill)
ntn sync <ref>   # refresh config_list from the device; the snapshot lands in ~/.ntnroute/backups/<host>/<YYYY-MM>/<stamp>-sync.cfg
S=~/.hermes/skills/networking/network-change-management/scripts
# 3. generate rollback, read it line by line, fill in "# TODO restore from snapshot:" from the pre-config
$S/rollback_gen "$TMPDIR/change.cmd" \
  --existing-config ~/.ntnroute/backups/<host>/<YYYY-MM>/<stamp>-sync.cfg \
  --out "$TMPDIR/rollback.cmd"
# MikroTik: the result contains `remove [find]` placeholders — narrow each find to the
# object the change actually added.
# 4. show the change + rollback to the user, ask permission, then apply through
#    the engine's gated config operation (invocation: references/engine-commands.md)
```
The engine performs: pre snapshot → apply → save → refresh inventory snapshot/archive → retain rollback. `STATUS: APPLIED` means no device-side CLI error was detected; it is not functional validation. Immediately run the verification commands promised in the plan (read-only, no further approval) and report their real output.

**A pull that is not a configuration is refused.** The engine screens every config pull before storing it: a login/error transcript (`% Bad secrets`, a bare `Password:` prompt, `% Invalid input` / `% Unknown command` / `syntax error` / `invalid value for argument`) is rejected. `add` then saves nothing and exits non-zero; `sync` reports that device as failed and leaves its previous `config_list` untouched; `sync all` exits 1 when any device failed. A wrong or missing level-2 secret therefore surfaces as a failure instead of a silent transcript "config". A stored `% Bad secrets` transcript with `check_point: (empty)` still means privileged mode was never reached — fix the stored secret by re-`add`ing the device before planning anything against it. Never let a false "config" become a rollback baseline: a rollback generated from a transcript would push garbage to the device.

**Keep the repo and the installed copy in sync.** This skill exists twice: the repo source (`~/ntnroute/skills/...`, the committed truth) and the installed copy (`~/.hermes/skills/networking/...`, what the agent loads). `install.sh` copies repo → installed, so a patch written only to the installed copy is lost on the next install. Patch the repo, then `install.sh`, then commit.

**The installed tree is shared state, not a mirror.** `install.sh` syncs through a manifest (`.ntn_manifest`, path + sha256 per file it installed): repo-owned files are overwritten, repo-owned files the repo dropped are removed, and anything the installer did not install — an agent-authored reference, a curator write — is preserved and reported as `NOTE: preserved`. A repo-owned file that was edited locally is overwritten with the repo version and the local copy is kept beside it as `<file>.local-<ts>` (`--force` discards it instead; `--dry-run` shows the plan without touching anything). The repo remains the source of truth: never treat the installed tree as durable storage.

## Engine and repo changes — plan first

Engine or repo-infrastructure changes follow the user's gate, not the device gate:

1. Present the plan first — what changes, why, blast radius on existing features — and wait for approval before editing anything. "Continue" after a plan is approval; a bare "do it" that arrives before any plan is not.
2. Touch only what the request names. Adjacent cleanup, style fixes, and consolidation are a separate proposal, never bundled in.
3. On "revert" / "don't change anything": restore immediately (`git checkout -- <file>`), confirm the restore, and stop — do not re-argue and do not re-apply later in the session.
4. Verify before claiming done: isolated unit test of each changed function, then the live-lab procedure in `references/engine-release-checks.md`. State plainly which parts were exercised and which are pending.

## Test status

Proven end-to-end (not just designed):

| Test | Device | Result |
|---|---|---|
| `add` / `list` / `show` / `exec` / `sync` | a lab Cisco IOS 15.4 router, a lab RouterOS 7.18.2 device | OK |
| `config` + post-check + `check_point` | Cisco — add Loopback99 + description | SUCCESS, verified on the device |
| `rollback` | Cisco — remove Loopback99 | SUCCESS, `config_list` clean |
| Multi-line `config` (menu path) | RouterOS — `/ip address add` + `set comment` | SUCCESS, `mt_normalize` works |
| `rollback` + destructive commands | RouterOS — `remove [find]` + clear comment | SUCCESS, MISSING=0 |
| Pre-snapshot guard with unreachable device | fake IP entry | Abort before apply, exit 1 |
| Device-error guard (Cisco) | invalid IP address | FAILED reported, `config_list` unchanged |
| Device-error guard (RouterOS) | `address=999.999.999.999/24` | `invalid value for argument address`, `config_list` unchanged |
| Bogus-pull guard (`add` / `sync`) | lab Cisco with a wrong level-2 secret; 23 real configs + 5 trap files | wrong secret → `add` saves nothing (exit 1), `sync` fails (exit 1) leaving `config_list` untouched, `sync all` exits 1; 0 false positives on real configs |
| `add` / `exec` / `sync` (Linux brand) | mock Linux server (paramiko, exec-mode) | OK — `uname -a` + os-release snapshot |
| `add` / `exec` / `sync`, `config` refused | real Windows 11 host over OpenSSH (cmd.exe) | OK — `systeminfo` snapshot, hostname auto-extracted; config/rollback correctly refused |

**Not yet tested:** Huawei, Aruba, Arista, Ruijie, Juniper — the code paths exist (`paging_cmd`, `secret_cmd`, `config_enter`, `save_lines`) but have never been run against real devices.

## Technical notes (do not change without testing)

### Two session modes — chosen automatically from the brand

| Brand | Mode | Transport | Pull config | Save |
|---|---|---|---|---|
| Mikrotik | EXEC | `ssh -T`, commands via stdin, no PTY | `/export verbose` | automatic (no `write memory`) |
| Cisco/Aruba/Arista/Ruijie | PTY | `ssh -tt` + paced plan | `show running-config` | `write memory` |
| Huawei | PTY | `ssh -tt` + paced plan | `display current-configuration` | `save` + `Y` (from `system-view`: `return` first) |
| Juniper | PTY | `ssh -tt` + paced plan | `show configuration \| display set` | `commit` **inside** config mode, then `exit configuration-mode` |
| Fortinet | PTY | `ssh -tt` + paced plan | `show full-configuration` | automatic (no save/enable; script lines apply on input) |

`is_exec_brand()` in the engine picks the branch. MikroTik has **no** `configure terminal`, `enable`, `terminal length 0`, or `write memory` — never insert those commands in a MikroTik script.

### Adding a brand — `~/.ntnroute/brands.json`

Per-brand behavior is data, not code: `~/.ntnroute/brands.json` entries override the built-in tables (lowercase brand key). Fields, all optional: `paging`, `secret_cmd`, `config_enter`, `config_leave`, `save_lines` (array; `[]` = no save), `save_delay`, `config_show`, `hostname_show`, `hostname_field` (`hostname`|`sysname`|`host-name`|`colon`), `err_pattern` (ERE), `negate_prefix` (rollback_gen, no trailing space). A brand shipped in `brands.json` ships as `zte` (Cisco-like example — adjust per model). When the user names a vendor that is neither built-in nor profiled: expect generic Cisco-like defaults, the save step is **skipped** with a NOTE, and the right move is to draft a profile (ask for one `show` command output and the device's config-save command), test with `ntn add` + a harmless `ntn config`, then keep the profile in `~/.ntnroute/brands.json` — the installer never overwrites it.

- RouterOS exec-mode is far more reliable than PTY: no banner, paging, or `[admin@host] >` prompt. Commands run sequentially from stdin, separated by newlines. `;` chains also work but one full command per line is easier to read.
- **RouterOS always exits 0 even when a command fails.** Errors are detected from output patterns: `invalid value`, `no such item`, `syntax error`, `expected end of command`, `bad command name`, `ambiguous`, `failure:`. The engine has these patterns in `err_pattern`.
- RouterOS exec-mode **does not keep context between lines**. The menu style `/interface ethernet` then `set [ find ... ]` fails (`expected end of command`) because each line runs as a standalone command. The engine normalizes scripts via `mt_normalize()`: pure path lines are merged into the next line as one full-path command. Write MikroTik scripts with the full path per line, or let the engine merge them — never rely on menu context.
- **Functional read-back is the only success criterion.** Choose show/print/display commands that prove the requested outcome (neighbor state, route, interface status, service state, policy counters, reachability). Do not infer success from the textual rendering of a configuration export.

### Portability and engine-code pitfalls (bash 3.2 / BSD)

The engine claims Linux + macOS + Windows support; every construct must exist in macOS's stock bash 3.2 and BSD userland.

- No bash-4-only expansions: `${x,,}`, `${x^}`, `declare -A`, `mapfile`. On macOS `/bin/bash` is 3.2 and these are a hard `bad substitution` — `ntn add` dies at brand normalization. Use `tr`-based helpers (`lc`/`ucfirst` in the engine).
- No `find -printf` (GNU-only): BSD find rejects it, and `2>/dev/null` swallows the error, so retention and migration silently do nothing and backups grow unbounded. Use `-exec basename {} \;` when names suffice; plain `find` output when the full path is needed.
- `date -d` is GNU-only; BSD needs `date -j -f <fmt>`. Parse the engine's own `YYYYMMDD-HHMMSS` stamp by shell pattern first — `date` only as a last-resort fallback.
- After fixing one instance of a portability construct, grep the whole engine for the same construct class — instances never occur alone.
- Cleanup of a staged artifact belongs inside the function that publishes it, executed before any retention/migration call: migration relocates the file, so a cleanup placed after the publishing call operates on a path that no longer exists and the duplicate survives.

### General
- SSH uses the OpenSSH CLI, not paramiko/Python. Sessions use `ssh -tt` with a scheduled (delay-TAB command) plan via stdin; passwords go through `SSH_ASKPASS` + `SSH_ASKPASS_REQUIRE=force`.
- Legacy flags (`diffie-hellman-group14-sha1`, `ssh-rsa`, `aes128-cbc`, `hmac-sha1`) are already wired in so old routers are reachable from OpenSSH 10.
- Interactive Cisco session: `enable` → secret → paging → command → `exit` → `exit`, with per-stage pauses. Command output is captured via `extract_cmd_output` (pattern: command echo, then stop at the `X>` / `X#` prompt).
- `pull_config()` and `pull_hostname()` are the only data-pull paths — mode-aware, used by `add`, `sync`, and `apply_config`. Do not duplicate the logic per brand.
- Applying a config needs a longer lag before `show running-config` (10s) because IOS is still processing.
- The DB is written atomically (temp + `mv`) with `flock`. Never edit `devices.json` with `jq > file` directly — always go through the engine.
- Passwords are stored in plaintext in a mode-600 file. The engine keeps them solely for device transport and never emits them to terminal output or chat.
