---
name: cis-gcp-cos-5.1.18
description: "Ensure SSH warning banner is configured"
category: cis-gcp-cos
version: "1.2.0"
author: siaga-official
tags: [cis, gcp, container-optimized-os, ssh, sshd, sshd-config]
cis_id: "5.1.18"
cis_benchmark: "CIS Google Container-Optimized OS Benchmark v1.2.0"
tech_stack: [gcp, linux]
cwe_ids: []
chains_with: []
prerequisites: []
severity_boost: {}
sha256: e047a15dfbfa4a7c5beb89fbc7777c30d1075968a09d1f680390183bcdf980d6
signature: AjvZtHxqQCDptgVL4xeCDXFcDxNKqHb5PeyhDFYvvB9fdoBwDWYtDj2FM0vWZjZ4Zjr3LUWklax7NUOK2oG1Cw==
signed_by: siaga-official
---

# 5.1.18 Ensure SSH warning banner is configured (Automated)

## Description

The `Banner` parameter specifies a file whose contents must be sent to the remote user before authentication is permitted. By default, no banner is displayed.

## Rationale

Banners are used to warn connecting users of the particular site's policy regarding connection. Presenting a warning message prior to the normal user login may assist the prosecution of trespassers on the computer system.

## Audit Procedure

Run the following command and verify that output matches:

```bash
# sshd -T | grep banner

Banner /etc/issue.net
```

## Expected Result

Output should show `Banner /etc/issue.net`.

## Remediation

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```
Banner /etc/issue.net
```

## CIS Controls

| Controls Version | Control                             | IG 1 | IG 2 | IG 3 |
| ---------------- | ----------------------------------- | ---- | ---- | ---- |
| v7               | 5.1 Establish Secure Configurations | x    | x    | x    |

## Profile

- Level 2 - Server
