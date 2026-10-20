---
name: keyvault-analyze-rotation
description: Analyze Azure Key Vault rotation for secrets, keys, and certificates, including rotation policies, version rollover, application refresh, event-driven automation, and failure handling. Use for expired credentials, stale consumers, or rotation design review.
---

# Analyze Rotation

1. Identify the object type, rotation owner, expected cadence, and dependent applications.
2. Inspect rotation policy/configuration, current and previous versions, and expiration windows.
3. Determine how consumers discover and adopt new versions.
4. Check for pinned versions, stale caches, failed automation, or deployment dependencies.
5. Verify rollback/recovery behavior for bad rotations.
6. Do not rotate production material unless explicitly authorized.

## Output
- Rotation Model
- Current/Next Version State
- Consumer Refresh Findings
- Failure/Rollback Risks
- Recommended Action
