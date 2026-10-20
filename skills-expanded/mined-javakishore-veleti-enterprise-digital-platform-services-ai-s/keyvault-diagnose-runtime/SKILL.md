---
name: keyvault-diagnose-runtime
description: Diagnose Azure Key Vault runtime failures end-to-end across identity, RBAC/access policies, networking/private endpoints, secret/key/certificate state, throttling, AKS CSI, Spring Boot, CI/CD, and diagnostics. Use as the primary Key Vault incident workflow when the failure domain is unknown.
---

# Diagnose Runtime

1. Read `.digital-platform-ai/keyvault.yaml`, service metadata, environment context, and relevant instructions.
2. Resolve workload identity, vault/HSM, object reference, operation, and network path.
3. Gather independent evidence in parallel:
   - authentication/identity
   - RBAC/access policy
   - DNS/private endpoint/network
   - secret/key/certificate metadata
   - application logs/traces
   - Key Vault diagnostics/audit events
4. Build a timeline around the first confirmed failure.
5. Route to focused `keyvault-*` skills.
6. Separate authentication, authorization, network, object lifecycle, throttling, client integration, and platform issues.
7. Never expose secret values, keys, certificates, or tokens.
8. Do not mutate production resources unless explicitly authorized.

## Output
- Incident Scope
- First Confirmed Failure
- Supporting Evidence
- Failing Layer
- Recommended Action
- Remaining Unknowns
