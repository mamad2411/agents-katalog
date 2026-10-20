---
name: db-elasticsearch-exposure
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect publicly exposed Elasticsearch clusters with no authentication, identifying accessible indices, sensitive data fields, and cluster metadata via REST API enumeration.
subdomain: database-security
tags:
  - elasticsearch
  - exposure
  - rest-api
  - index-enum
  - shodan
  - unauthenticated
nist_csf:
  - ID.RA-01
  - DE.CM-04
mitre:
  - T1190
  - T1078
cwe:
  - CWE-306
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
