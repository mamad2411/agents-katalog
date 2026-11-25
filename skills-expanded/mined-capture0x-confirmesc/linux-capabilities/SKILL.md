---
name: linux-capabilities
description: Turn a CONFIRMED Linux capability finding from confirmesc into a root shell or a protected-file read. Use when confirmesc reports a dangerous file capability such as cap_setuid or cap_setgid on an abusable binary.
---

# Linux capabilities

File capabilities grant a binary a subset of root powers without the SUID bit.
`cap_setuid` / `cap_setgid` on an interpreter let it set its uid to 0 and keep
it, which is a direct root path.

## When to use

confirmesc reports a finding like:

```
[CONFIRMED] Dangerous capability on /opt/vulnapp2/python3: cap_setgid, cap_setuid
  root shell: /opt/vulnapp2/python3 -c 'import os,pty;os.setuid(0);pty.spawn("/bin/bash")'
```

`CONFIRMED` means `getcap -r /` observed the capability and the binary is a
known GTFOBins capability vector.

## How to exploit

- Use the `exploit_command` from the report. For `cap_setuid` it calls
  `setuid(0)` before spawning a shell, so the shell is really root.
- Capabilities worth knowing:
  - `cap_setuid` / `cap_setgid`: become uid/gid 0 directly.
  - `cap_dac_read_search`: read any file (dump `/etc/shadow` and crack).
  - `cap_dac_override`: write any file.
  - `cap_sys_ptrace`, `cap_sys_admin`: broader abuse paths.
- Not every capability yields a direct shell; read-oriented ones are used to
  exfiltrate protected files instead.

## Verify

Run `id` and confirm `uid=0(root)`, or read a root-only file.

## Rules

- Authorized targets only.
- The operator runs the command; do not auto-execute it.
