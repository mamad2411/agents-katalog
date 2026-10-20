# Consent Domain Memory

Apply this inside `ai-service/app/domains/consents/`.

- Consent definitions must remain separate and explicit.
- Do not infer consent from account creation, app usage, or another consent type.
- Keep enum values stable once exposed to clients.
- Any new consent needs a clear title, patient-readable description, and focused purpose.
- Add or update tests when consent types, definitions, or service behavior changes.
