---
description: Consent behavior rules across frontend and API
globs:
  - "frontend/src/features/consents/**/*"
  - "ai-service/app/domains/consents/**/*"
  - "ai-service/app/api/v1/consents.py"
alwaysApply: false
---

# Consent Rules

- Consent is never implied by registration, navigation, or another consent.
- Keep each consent separate, explicit, auditable, and reversible.
- Do not merge cloud storage, research participation, AI improvement, or community sharing into one choice.
- Keep frontend consent identifiers aligned with API/domain consent types.
- Add or update tests when consent types, labels, API responses, or service behavior change.
