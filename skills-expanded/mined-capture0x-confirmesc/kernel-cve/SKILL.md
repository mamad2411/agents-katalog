---
name: kernel-cve
description: Act on a LIKELY kernel, sudo, or polkit CVE match from confirmesc. Use when confirmesc flags a version-based CVE such as Dirty Pipe, PwnKit, or Baron Samedit.
---

# Kernel / sudo / polkit CVEs

confirmesc compares the running kernel, sudo, and polkit versions against
known-vulnerable ranges and flags matches as `LIKELY`. This is a version-based
signal, not a live exploitation check.

## When to use

confirmesc reports a finding like:

```
[LIKELY] Dirty Pipe (CVE-2022-0847) - kernel 5.15.0 looks vulnerable
```

## How to proceed

- `LIKELY` means the version is in range, but a distro backport may already have
  fixed it. Confirm the exact patch level before running anything.
- Cross-check the distro advisory; the version string alone can be misleading.
- Use a known-good public PoC for the specific CVE and test it in a sandbox
  first. Kernel exploits can crash the host.
- High-value matches this tool knows: Dirty Pipe (CVE-2022-0847), Dirty COW,
  PwnKit (CVE-2021-4034), Baron Samedit (CVE-2021-3156), nf_tables
  (CVE-2024-1086), OverlayFS, sudoedit escape.

## Verify

Run `id` after the exploit and confirm `uid=0`.

## Rules

- Authorized targets only. Kernel PoCs are risky; prefer a snapshot or sandbox,
  and do not run them against production without a maintenance window.
