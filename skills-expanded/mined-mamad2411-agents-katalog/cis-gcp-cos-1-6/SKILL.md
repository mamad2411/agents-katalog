---
name: cis-gcp-cos-1.6
description: "Ensure AppArmor is installed"
category: cis-gcp-cos
version: "1.2.0"
author: siaga-official
tags: [cis, gcp, container-optimized-os, apparmor, mandatory-access-control]
cis_id: "1.6"
cis_benchmark: "CIS Google Container-Optimized OS Benchmark v1.2.0"
tech_stack: [gcp, linux]
cwe_ids: []
chains_with: []
prerequisites: []
severity_boost: {}
sha256: 8a502c0bc1c7d2758ee6863ec6b448f8c2fdecae76a0a7b27eadd33637f90a0a
signature: 7I1f5ELl04CO30KK1x5niod3uTw5bApGrv6tRZnnssN5s9kxcNpnzQNBSMDx71y2yhaulIxArsBZCpJS1+ivDA==
signed_by: siaga-official
---

# 1.6 Ensure AppArmor is installed (Automated)

## Description

SELinux and AppArmor provide Mandatory Access Controls.

## Rationale

Without a Mandatory Access Control system installed only the default Discretionary Access Control system will be available.

## Audit Procedure

Verify that AppArmor is installed with the following command:

```bash
# grep '\"name\": \"apparmor\"' /etc/cos-package-info.json
"name": "apparmor",
```

## Expected Result

The output should show `"name": "apparmor",` confirming AppArmor is installed.

## Remediation

Update to an OS image that includes the apparmor package.

## Additional Information

SELinux and AppArmor both have several package names in use on different distributions. Research the appropriate packages for your environment.

## CIS Controls

| Controls Version | Control                                               | IG 1 | IG 2 | IG 3 |
| ---------------- | ----------------------------------------------------- | ---- | ---- | ---- |
| v8               | 3.3 Configure Data Access Control Lists               | x    | x    | x    |
| v7               | 14.6 Protect Information through Access Control Lists | x    | x    | x    |

## Profile

Level 1 - Server | Automated
