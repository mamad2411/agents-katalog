---
name: postgres-analyze-cmk
description: Analyze customer-managed key encryption for Azure Database for PostgreSQL Flexible Server, including Azure Key Vault keys, managed identities, permissions, key state, rotation, networking, and service availability impact. Use for CMK/BYOK architecture or incidents.
---

# Analyze Customer-Managed Keys

1. Identify PostgreSQL server, managed identity, Key Vault/key reference, region, and encryption configuration.
2. Inspect identity access to the key and Key Vault network accessibility.
3. Check key state, version/rotation behavior, expiration, and recent changes.
4. Correlate PostgreSQL encryption errors with Key Vault evidence.
5. Route deep key investigation to `keyvault-*` skills.
6. Do not disable or rotate production CMKs without explicit authorization.

## Output
- Server/Key Mapping
- Identity/Permission Findings
- Key/Network State
- Availability Impact
- Recommended Action
