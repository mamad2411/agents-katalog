---
name: db-mssql-xp-cmdshell
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect and audit MSSQL xp_cmdshell usage enabling OS command execution from SQL context, including attempts to enable it through sp_configure.
subdomain: database-security
tags:
  - mssql
  - xp-cmdshell
  - rce
  - sql-server
  - command-execution
  - sp-configure
nist_csf:
  - DE.CM-04
mitre:
  - T1505.001
  - T1059
cwe:
  - CWE-78
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
