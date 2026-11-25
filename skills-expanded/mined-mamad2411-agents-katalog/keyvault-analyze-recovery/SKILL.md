---
name: keyvault-analyze-recovery
description: Analyze Azure Key Vault soft-delete, purge protection, recovery, backup/restore considerations, deleted objects, and accidental-deletion resilience. Use for deletion incidents, recovery planning, or data-loss protection review.
---

# Analyze Recovery

1. Inspect soft-delete and purge-protection settings.
2. Identify whether the vault/object is active, soft-deleted, recoverable, or permanently unavailable.
3. Review retention window and recovery requirements.
4. For Managed HSM, include security-domain and backup/recovery posture where relevant.
5. Distinguish vault recovery from individual secret/key/certificate recovery.
6. Never purge production vaults or objects unless explicitly authorized.

## Output
- Protection State
- Deleted Object/Vault State
- Recovery Options
- Data-Loss Risk
- Recommended Action
