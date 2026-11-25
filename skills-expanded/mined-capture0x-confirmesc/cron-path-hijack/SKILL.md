---
name: cron-path-hijack
description: Exploit a CONFIRMED writable cron, systemd, or $PATH entry that a root scheduler executes. Use when confirmesc reports a root-run file or directory you can write to.
---

# Cron / systemd / $PATH hijack

A root scheduler (cron, systemd timer) that runs a file you can modify, or looks
up a command through a directory you can write to, will run your code as root.

## When to use

confirmesc reports a finding like:

```
[CONFIRMED] Writable file executed by root scheduler: /etc/cron.d/maint
[CONFIRMED] Writable directory in $PATH: /usr/local/writablebin
```

`CONFIRMED` means `os.access` confirmed you can write to the file or its
containing directory.

## How to exploit

- Writable script: append a payload line, for example `chmod +s /bin/bash` or a
  reverse shell, then wait for the next scheduled run.
- Writable directory containing the script: delete and replace the file.
- Writable `$PATH` directory that comes before the real binary: drop a malicious
  file with the command's name so it is found first.
- Keep changes reversible and restore the original afterwards.

## Timing

confirmesc confirms write access, not the scheduler firing. You still need to
wait for the schedule or trigger it.

## Verify

After the scheduled run, check for your artifact (a SUID `/bin/bash`, a new root
file, a callback).

## Rules

- Authorized targets only. Prefer reversible edits; restore the original file.
