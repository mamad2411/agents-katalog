---
name: apparmor-profile-basics
description: >
  AppArmor MAC profile basics for owned Linux hosts (Ubuntu/Debian and compatible):
  profiles in enforce/complain/disable, aa-status, aa-genprof/aa-logprof, aa-enforce,
  deny rules, abstractions, and debugging DENIED logs. Use when confining daemons or
  containers with path-based profiles on systems you administer — not for bypassing
  host policy on third-party infrastructure.
---

# AppArmor Profile Basics

## Scope And Authorization

- **In scope:** Linux hosts/VMs/containers you own or administer under authorization (labs, prod with change control).
- **Out of scope:** Disabling or weakening AppArmor on shared multi-tenant systems without approval; attacking others’ confinement.
- Prefer **complain** mode while learning a profile; move to **enforce** only after log review.
- Snapshot or document existing profiles before edits; keep a rollback (known-good profile copy).
- Pair profile packaging/automation with `code-quality-standards`.

## When To Use

- Writing or tightening profiles for nginx, postgres, custom agents, or CI runners.
- Diagnosing `DENIED` operations in `dmesg` / `journalctl` / audit logs.
- Moving a profile from complain → enforce after a soak period.
- Checking whether a binary is confined (`aa-status`, `/proc/<pid>/attr/current`).
- Packaging profiles under `/etc/apparmor.d/` with includes and abstractions.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SELinux policy (type enforcement) | SELinux-focused skill if present |
| Kubernetes PSP/PSA / seccomp | cluster security skills |
| Linux privilege escalation on owned host | `linux-privilege-escalation` (lab/authorized) |
| Container runtime hardening broadly | container security skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Profile modes | `enforce` (block + log), `complain` (allow + log), `disable` / unconfined |
| Attachment | Profile name usually equals absolute path of binary (e.g. `/usr/sbin/nginx`) |
| Rules | path access `r`/`w`/`ix`/`ux`/`Px`, network, capability, mount, signal, dbus |
| Abstractions | `#include <abstractions/base>` etc. for common libraries/paths |
| Tools | `aa-status`, `aa-enforce`, `aa-complain`, `aa-disable`, `aa-genprof`, `aa-logprof`, `apparmor_parser` |
| Logs | `audit: type=1400` / `APPARMOR=DENIED` in kernel audit or journal |

## Profile Mode Cheatsheet

| Mode | Behavior | Use |
| --- | --- | --- |
| enforce | Violations blocked | Production target |
| complain | Violations allowed, logged | Learning / soak |
| unconfined / disabled | No MAC from this profile | Temporary debug only |

## Workflow

### 1. Confirm scope and success criteria

1. Record host OS/version, kernel, AppArmor package version, service binary path, owner team.
2. Success: service starts under named profile; no unexpected DENIED for legit paths; malicious path probes denied in enforce.
3. Identify rollback: previous profile file + `systemctl restart` procedure.

### 2. Inventory current confinement

```bash
sudo aa-status
# Is AppArmor enabled?
cat /sys/module/apparmor/parameters/enabled
# What profile does a running PID use?
PID=$(pgrep -n nginx)
sudo cat /proc/$PID/attr/current
# List loaded profiles
sudo apparmor_status 2>/dev/null || sudo aa-status
ls /etc/apparmor.d/
```

1. Note which profiles are in enforce vs complain.
2. Confirm the binary path matches the profile attachment (symlinks can surprise you).
3. Check if the unit runs under a container runtime that uses a different LSM path.

### 3. Baseline before change

1. Copy existing profile: `sudo cp /etc/apparmor.d/usr.sbin.nginx /root/backup/usr.sbin.nginx.$(date +%F)`.
2. Capture 24h of DENIED lines (or reproduce workload once in complain).
3. Document required paths: config, logs, pid, sockets, TLS material, plugin dirs.

### 4. Generate and refine a profile

**Interactive learning (owned host):**

```bash
# Run genprof against the program while exercising it
sudo aa-genprof /usr/sbin/mydaemon
# Or iteratively:
sudo aa-complain /etc/apparmor.d/usr.bin.mydaemon
# exercise service...
sudo aa-logprof
sudo aa-enforce /etc/apparmor.d/usr.bin.mydaemon
```

**Minimal hand-written sketch:**

```text
#include <tunables/global>

/usr/bin/mydaemon {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  /usr/bin/mydaemon mr,

  /etc/mydaemon/** r,
  /var/log/mydaemon/** w,
  /run/mydaemon.pid wk,
  /var/lib/mydaemon/** rw,

  # Network if required
  network inet stream,
  network inet6 stream,

  # Deny secrets locations by default; open only what is needed
  deny /etc/shadow r,
}
```

**Load and set mode:**

```bash
sudo apparmor_parser -r /etc/apparmor.d/usr.bin.mydaemon
sudo aa-enforce /etc/apparmor.d/usr.bin.mydaemon
# or
sudo aa-complain /etc/apparmor.d/usr.bin.mydaemon
```

1. Prefer **least path access**: directory wildcards only where needed.
2. Prefer `ix` (inherit) / `Px` (discrete profile) over unconfined `ux` execute transitions.
3. Use abstractions before duplicating libc/DNS rules.

### 5. Debug DENIED events

```bash
sudo journalctl -k -b --grep=DENIED
sudo dmesg | grep -i apparmor | tail -n 50
# Ubuntu often:
sudo tail -n 100 /var/log/syslog | grep DENIED
```

1. Map DENIED operation + path + profile name → add rule or fix app path misuse.
2. Re-test after each small rule add; avoid “allow everything under /”.
3. If a capability is denied, justify `capability` lines explicitly (e.g. `capability net_bind_service`).

### 6. Verify with evidence

```bash
sudo aa-status | sed -n '/enforce/,/complain/p'
PID=$(pgrep -n mydaemon)
sudo cat /proc/$PID/attr/current   # expect: /usr/bin/mydaemon (enforce)
# Positive: service healthcheck OK
curl -fsS http://127.0.0.1:8080/healthz
# Negative: confined process cannot read forbidden file (lab probe as same user via app feature)
```

1. Soak in complain with production-like traffic, then enforce.
2. Keep before/after profile diffs and sample DENIED logs (redact hostnames if needed).
3. Confirm reboot persistence (profiles still loaded via `/etc/apparmor.d/`).

### 7. Hand off

1. Document profile owner, modes per environment, and how to `aa-logprof` safely.
2. Ship profiles via config management; avoid one-off production edits without PR.
3. Schedule review after major app upgrades (new paths/binaries).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Learning | complain + logprof + enforce | enforce with empty profile → broken prod |
| Rules | path-minimal + abstractions | `/** rwlkmix` “to make it work” |
| Exec | `Px`/`ix` with child profiles | blanket `ux` unconfined exec |
| Debug | map DENIED to single rule | disable AppArmor globally |
| Ops | CM-managed profiles + backup | hand-edit only on one host |
| Scope | owned hosts | turning off MAC on shared infra |

## Output Checklist

- [ ] Host, binary path, authorization, environment recorded
- [ ] Baseline `aa-status` and existing profile backups taken
- [ ] Profile authored/refined with complain soak evidence
- [ ] Loaded via `apparmor_parser`; mode set intentionally
- [ ] DENIED noise for legitimate traffic cleared
- [ ] Enforce mode verified via `/proc/<pid>/attr/current`
- [ ] Negative path/capability tests documented
- [ ] CM/packaging and owners updated
- [ ] `code-quality-standards` applied if automation shipped

## Rules

- Authorized hosts only; do not disable AppArmor to “fix” unauthorized issues.
- Prefer complain→enforce; never leave production unconfined without ticket + expiry.
- Avoid unconfined execute transitions unless there is no safer profile split.
- Keep secrets paths denied by default; open only what the daemon needs.
- Focus this skill on AppArmor profiles; route SELinux and full container policy elsewhere.
