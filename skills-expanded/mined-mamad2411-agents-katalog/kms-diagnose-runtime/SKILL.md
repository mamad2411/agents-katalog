---
name: kms-diagnose-runtime
description: Diagnose AWS KMS runtime failures end-to-end across key policy, IAM, grants, key state, region, encryption context, custom key stores, service integrations, application code, and CloudTrail evidence. Use as the primary AWS KMS incident workflow when the failure domain is unknown.
---

# Diagnose Runtime

1. Read `.digital-platform-ai/keyvault-aws.yaml`, service metadata, environment context, and relevant instructions.
2. Resolve key ARN/alias, region, operation, caller identity, and consuming service/application.
3. Gather independent evidence in parallel:
   - key metadata/state
   - key policy
   - IAM/SCP/boundary/session policies
   - grants
   - encryption context
   - service integration
   - application logs/traces
   - CloudTrail
4. Build a timeline around the first confirmed failure.
5. Route to focused `kms-*` skills.
6. Separate authorization, key-state, region, cryptographic-usage, custom-store, service-integration, and application failures.
7. Never expose plaintext data keys or sensitive key material.
8. Do not mutate production resources unless explicitly authorized.

## Output
- Incident Scope
- First Confirmed Failure
- Supporting Evidence
- Failing Layer
- Recommended Action
- Remaining Unknowns
