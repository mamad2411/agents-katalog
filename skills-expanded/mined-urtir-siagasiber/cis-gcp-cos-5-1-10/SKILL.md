---
name: cis-gcp-cos-5.1.10
description: "Ensure SSH root login is disabled"
category: cis-gcp-cos
version: "1.2.0"
author: siaga-official
tags: [cis, gcp, container-optimized-os, ssh, sshd, sshd-config, authentication]
cis_id: "5.1.10"
cis_benchmark: "CIS Google Container-Optimized OS Benchmark v1.2.0"
tech_stack: [gcp, linux]
cwe_ids: []
chains_with: []
prerequisites: []
severity_boost: {}
sha256: 2e7c1a071d611df2f26c6d18713ca7c4c8f9c20e70992e2f7b7ab6c351b0159b
signature: FqC6M3JZDAKEkbOtuazBJt+0NwA37tQhax9GHc9PGLKs9DMChB2A9nWtBnuPrUBA9xbNBlL94l/9ltnM+RMYAA==
signed_by: siaga-official
---

# 5.1.10 Ensure SSH root login is disabled (Automated)

## Description

The `PermitRootLogin` parameter specifies if the root user can log in using ssh. The default is no.

## Rationale

Disallowing root logins over SSH requires system admins to authenticate using their own individual account, then escalating to root via `sudo` or `su`. This in turn limits opportunity for non-repudiation and provides a clear audit trail in the event of a security incident.

## Audit Procedure

Run the following command and verify that output matches:

```bash
# sshd -T | grep permitrootlogin

PermitRootLogin no
```

## Expected Result

Output should show `PermitRootLogin no`.

## Remediation

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```
PermitRootLogin no
```

## Default Value

PermitRootLogin without-password

## CIS Controls

| Controls Version | Control                                                                   | IG 1 | IG 2 | IG 3 |
| ---------------- | ------------------------------------------------------------------------- | ---- | ---- | ---- |
| v8               | 5.4 Restrict Administrator Privileges to Dedicated Administrator Accounts | x    | x    | x    |
| v7               | 4.3 Ensure the Use of Dedicated Administrative Accounts                   | x    | x    | x    |

## Profile

- Level 1 - Server
