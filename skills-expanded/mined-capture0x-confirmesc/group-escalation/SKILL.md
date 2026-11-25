---
name: group-escalation
description: Escalate via a CONFIRMED privileged group membership (docker, lxd, lxc, disk). Use when confirmesc confirms both the group membership and real access to its socket or device.
---

# Group-membership escalation

Membership in `docker`, `lxd`, `lxc`, or `disk` is effectively root: these
groups control resources that read or write the host as root.

## When to use

confirmesc reports a finding like:

```
[CONFIRMED] Member of the 'docker' group with an accessible docker socket
```

`CONFIRMED` means the group membership AND real socket/device access were both
verified, not just the group name in `id`.

## How to exploit

- `docker`: `docker run -v /:/mnt --rm -it alpine chroot /mnt sh` mounts the
  host filesystem and drops a root shell on the host.
- `lxd` / `lxc`: import a minimal image, launch a privileged container with the
  host disk mounted, and chroot into it.
- `disk`: the group can read and write raw block devices (`/dev/sda`). Use
  `debugfs` to read `/etc/shadow` or write files as root.

## Verify

Inside the container or chroot, read a host root-only file or run `id`.

## Rules

- Authorized targets only. Containers and images you create are state; remove
  them afterwards.
