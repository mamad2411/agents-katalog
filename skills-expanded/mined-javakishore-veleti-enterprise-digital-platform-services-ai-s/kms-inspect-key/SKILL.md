---
name: kms-inspect-key
description: Inspect AWS KMS key metadata, origin, key spec, usage, state, aliases, policies, grants, rotation, multi-Region status, and environment context. Use as the general AWS KMS entry point when the key or failure domain is not yet known.
---

# Inspect KMS Key

1. Read `.digital-platform-ai/keyvault-aws.yaml`, service metadata, environments, and relevant instructions.
2. Resolve AWS account, region, key ARN/alias, environment, and consuming applications.
3. Inspect:
   - key origin and key spec
   - key usage and state
   - aliases and tags
   - key policy and grants
   - rotation configuration
   - multi-Region status
4. Identify whether the issue is policy, IAM, grants, key state, cryptographic usage, rotation, region, or application integration.
5. Route to focused `kms-*` skills.
6. Never expose plaintext data keys or sensitive cryptographic material.

## Output
- Key Context
- Policy/Grant State
- Rotation/Region State
- Scope Assessment
- Recommended Next Skill
