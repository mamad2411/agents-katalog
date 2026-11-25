---
name: sudo-abuse
description: Turn a CONFIRMED sudo-rule finding from confirmesc into a root shell. Use when confirmesc reports that the current user is authorized to run a GTFOBins-abusable binary through sudo.
---

# sudo rule abuse

A permissive `sudo` rule lets a user run a specific binary as root. If that
binary can execute other commands (a GTFOBins "sudo" entry), the rule becomes a
full root escalation.

## When to use

confirmesc reports a finding like:

```
[CONFIRMED] Exploitable sudo rule: /usr/bin/find
  root shell: sudo /usr/bin/find . -maxdepth 0 -exec /bin/bash -p \; -quit
```

The `CONFIRMED` label means `sudo -n -l` was actually run and the authorization
for this binary as root was directly verified, not guessed.

## How to exploit

- Use the `exploit_command` from the report. For shell-spawning binaries it
  uses `bash -p` or a direct exec so the resulting shell keeps root, instead of
  a plain shell that would drop privileges.
- `NOPASSWD` rules escalate without any password. Rules that need a password
  require you to already know it.
- For a binary not in the verified-reliable set, check its GTFOBins "sudo"
  function and adapt the technique.

## Verify

Run `id` in the resulting shell and confirm `uid=0(root)`.

## Rules

- Authorized targets only.
- The operator runs the command; do not auto-execute it.
