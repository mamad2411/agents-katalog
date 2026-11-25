---
name: browser-chrome-cookie
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Extract Chrome session cookies from the SQLite Cookies database, decrypt AES-256-GCM protected values using the DPAPI-derived key, and identify session tokens.
subdomain: browser-forensics
tags:
  - chrome
  - cookie
  - dpapi
  - session-token
  - aes-gcm
  - sqlite
  - credential-theft
nist_csf:
  - DE.AE-02
  - RS.AN-03
mitre:
  - T1539
  - T1552.001
cwe:
  - CWE-312
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
