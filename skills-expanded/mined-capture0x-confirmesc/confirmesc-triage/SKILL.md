---
name: confirmesc-triage
description: Run confirmesc on an authorized Linux target, read the report, and prioritize the CONFIRMED privilege-escalation vectors to act on. Use at the start of any Linux post-exploitation or privesc assessment, before trying techniques by hand.
---

# confirmesc triage

Use this when you have a shell on an authorized Linux target and need to know,
quickly, whether it can be escalated to root and how.

Load `privesc-authorization-check` first; only proceed once that gate passes.

## Workflow

1. Run a passive scan and read structured output:
   - CLI: `confirmesc --format json`
   - or the `scan` MCP tool (`confirmesc-mcp`)
2. Look at `findings`. Act on `CONFIRMED` first, then `LIKELY`. Ignore `INFO`
   unless nothing actionable is found.
3. For each `CONFIRMED` finding, open the matching skill for the technique:
   - SUID / SGID binary -> `suid-sgid-exploitation`
   - sudo rule -> `sudo-abuse`
   - Linux capability -> `linux-capabilities`
   - writable cron / systemd / `$PATH` -> `cron-path-hijack`
   - cron wildcard injection -> `cron-wildcard-injection`
   - kernel / sudo / polkit CVE -> `kernel-cve`
   - docker / lxd / disk group -> `group-escalation`
   - sudo `env_keep` / `LD_PRELOAD` -> `sudo-env-keep`
   - NFS `no_root_squash` -> `nfs-no-root-squash`
   - readable keys / credentials -> `credential-recon`
   - writable `/etc/passwd` / `/etc/shadow` / `/etc/sudoers` -> `critical-file-write`
4. Every `CONFIRMED` SUID / sudo / capability finding already carries an
   `exploit_command` field. That command is built to actually return a root
   shell on a modern box (it accounts for the `dash`/`bash` privilege drop).
   Present it to the operator.
5. After a technique succeeds, follow `post-exploitation-notes` to record the
   path, keep changes reversible, and clean up.

## Reading confidence

- `CONFIRMED`: the exploitable condition was directly observed. Trust it.
- `LIKELY`: a strong indicator matched (often a version string). Verify before
  relying on it; a distro backport can block it.
- `INFO`: context only, not an escalation path.

## Rules

- Operate only on systems you are explicitly authorized to test: your own
  systems, a CTF, or an engagement with signed authorization.
- confirmesc confirms conditions and prints a suggested command. Turning that
  into a shell is an operator decision. Do not auto-execute exploit commands.
