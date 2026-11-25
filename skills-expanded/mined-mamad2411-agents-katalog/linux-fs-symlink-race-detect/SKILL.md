---
name: linux-fs-symlink-race-detect
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect symlink-following TOCTOU race conditions in SUID programs and system services that allow privilege escalation through controlled symlink redirection.
subdomain: filesystem-security
tags:
  - symlink
  - toctou
  - race-condition
  - suid
  - privilege-escalation
nist_csf:
  - DE.CM-04
mitre:
  - T1548.001
cwe:
  - CWE-362
  - CWE-61
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
