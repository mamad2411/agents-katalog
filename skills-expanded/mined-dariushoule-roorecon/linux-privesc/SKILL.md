---
name: linux-privesc
description: Linux local privilege escalation methodology for authorized pentesting and CTF — turn a foothold shell (often a low-priv/service account like www-data) into root. Use after landing any non-root shell on a Linux host and you need to escalate: enumerate the local attack surface (sudo, SUID/SGID, capabilities, cron/timers, writable files, internal root services, credential reuse, kernel) and exploit the weakest link. Triggers on "privesc", "privilege escalation", "I have a shell now what", "escalate to root", "get root", "I'm www-data", "root this box", "linpeas", "sudo -l", "SUID", "GTFOBins".
---

# Linux local privilege escalation

You have a shell as a non-root user (commonly a service account — `www-data`,
`mysql`, an app user). Goal: become root. This skill is the **enumerate → find the
one thing you can influence that runs as root → exploit** loop, plus the footguns of
driving a half-broken foothold shell.

## Scope guardrail

Authorized targets only (CTF box, lab, signed scope). Enumeration maps the local
attack surface; the actual escalation is an *acting* step — surface the vector and
the one-liner, and let the operator approve before you fire it (same ethos as the
rest of the repo). Reading `root.txt` proves the privesc; don't go beyond the
assessment objective.

## First: stabilise the foothold

A webshell or raw reverse shell is not a TTY, and several escalation steps need one.

- **Get a PTY before anything interactive** (`su`, `sudo`, `ssh`, editors):
  `python3 -c 'import pty; pty.spawn("/bin/bash")'` (or `script -qc /bin/bash /dev/null`).
  Without it, `su` fails with *"must be run from a terminal"* and `sudo` can't prompt.
- For a durable, shareable shell use the **catch** skill (`./roo catch`) — drive it
  with `catch send`/`capture` (run `catch enter` once to drop from pwncat's local
  prompt into the remote shell).
- For clean, scriptable command output, driving the **webshell** (single commands via
  `curl --data-urlencode`) is often tidier than scraping a tmux pane.

## The enumeration ladder (run top-to-bottom; stop when one pays off)

1. **Who am I / quick wins.** `id; sudo -n true 2>&1; cat /etc/passwd | grep sh$`.
   Note your groups — `docker`, `lxd`, `disk`, `adm`, `sudo`/`wheel` are each a known
   root path on their own.
2. **sudo rights.** `sudo -l` (try with and without the foothold password). Any
   allowed binary → check **GTFOBins** for the sudo escape. `(ALL) NOPASSWD` on
   anything scriptable is usually instant root.
3. **SUID / SGID.** `find / -perm -4000 -type f 2>/dev/null` (and `-2000`). Diff
   against a stock list — anything **non-standard** (custom binary, an interpreter,
   a GTFOBins entry) is the lead. Stock set (mount, su, sudo, passwd, …) is noise.
4. **Capabilities.** `getcap -r / 2>/dev/null`. `cap_setuid`/`cap_dac_read_search`
   on a binary you can run = root or arbitrary file read.
5. **Cron & timers.** `cat /etc/crontab; ls -la /etc/cron.*; systemctl list-timers`.
   A root job that runs a script you can write (or a relative/`PATH`-resolved binary
   you can hijack, or a wildcard you can inject) → root.
6. **Writable things root trusts.** Writable `/etc/passwd`, `/etc/sudoers.d/*`,
   a systemd unit, a script invoked by a root service/cron, or a directory on root's
   `PATH`. `find / -writable -type f 2>/dev/null` (filter to /etc,/opt,/usr/local).
7. **Internal services running as root.** `ss -tlnp` — a daemon bound to
   `127.0.0.1` is often *more* privileged and *less* guarded than the public ones
   (admin panels, job/automation runners, DBs, message queues). If it runs as root
   and exposes any way to **run a command, render a template, or read/write a file**,
   that's your primitive — reach it locally (curl, or `./roo fwd` to pull it to the
   host) and look for a command/exec/file feature, an unauthenticated trigger, or an
   **argument/parameter injected into a shell string** (loosely-validated inputs in a
   config-driven action runner are a classic — break out of the surrounding quoting).
   A root-owned **web server** (e.g. `php -S 127.0.0.1:PORT -t <dir>` running as root)
   is the same primitive by another name: if any feature writes a file into its docroot
   — even a "save"/upload that `basename`-sanitizes the name — drop an **executable
   extension** (`.php`) and request it → RCE **as root**. A surviving `.php` is enough;
   you don't need path traversal or command injection in the filename.
8. **Credential reuse — try this *before* cracking.** The fastest "privesc" is a found
   *plaintext* password, and a reused cred beats a GPU every time — so the moment you
   have file read (a shell or RCE), scrape for creds *before* reaching for hashcat. App
   **config files** are the richest source (DB/app creds — e.g. `wp-config.php`
   `DB_PASSWORD`, `config*.php`, `.env`, `settings.py`) — a **service/DB password from a
   config is frequently reused as a login user's *system* password** — plus shell
   history, backups, `/var/mail`, world-readable home files, and any DB you can reach.
   Then **spray**: `su <user>` for every local user,
   and **reuse on SSH** (a service/DB password reused for a login account is a classic
   foothold→user hop). Only hand what *stays* a hash to the **hashcat** skill (`-m 1800`
   sha512crypt, `-m 3200` bcrypt) — even "slow" hashes fall fast if it's a common word,
   and spray any crack result too.
9. **Kernel / distro / installed software.** `uname -a; cat /etc/os-release; dpkg -l`
   → feed versions to the **vuln-research** skill (`./roo vulns`) for a local-exploit
   CVE. Lowest priority on a maintained box; don't lead with a kernel exploit.

## Tooling

- **Manual first** (the ladder above) — it's fast and quiet, and you learn the box.
- **Stage an automated enumerator** when manual stalls: drop `linpeas.sh` onto the
  target (host it from `./roo shell` / `./roo catch upload`, or fetch with the box's
  own curl/wget) and run it. Downloads egress the **public internet**, not the VPN.
- GTFOBins (gtfobins.github.io) is the lookup for sudo/SUID/capability escapes.

## Confirm & hand off

- Root proof: a SUID-root shell (`cp /bin/bash /tmp/rootbash; chmod 4755 /tmp/rootbash;
  /tmp/rootbash -p`) or a root reverse shell; then `id` (euid=0) and `cat /root/root.txt`.
- **Note any artifact you leave** (a SUID bash, an added user, a modified file) so the
  operator can clean up — on a lab box it's wiped at reset, but say so.
- Handoffs: **hashcat** (crack looted hashes), **vuln-research** (service/kernel CVEs),
  **catch** (stabilise/keep the shell), **memforensics** (if you loot a memory image),
  **ad** (if the box is domain-joined and you find domain creds).
