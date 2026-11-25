---
name: kms-analyze-rotation
description: Analyze AWS KMS automatic, on-demand, and manual rotation behavior, schedules, eligibility, key-material versions, and application impact. Use for rotation planning, stale key assumptions, or rotation incidents.
---

# Analyze Rotation

1. Identify key type, origin, multi-Region status, and current rotation configuration.
2. Determine which rotation mechanisms are supported for this key type.
3. Inspect automatic rotation schedule, on-demand rotation history, or manual replacement strategy.
4. For multi-Region keys, verify rotation is managed from the primary key.
5. For imported material, validate prerequisites before on-demand rotation.
6. Do not rotate production keys unless explicitly authorized.

## Output
- Rotation Eligibility
- Current Schedule/History
- Multi-Region/Imported Constraints
- Application Impact
- Recommended Rotation Plan
