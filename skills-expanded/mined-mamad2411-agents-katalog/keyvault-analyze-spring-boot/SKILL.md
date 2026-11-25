---
name: keyvault-analyze-spring-boot
description: Analyze Spring Boot and Java integration with Azure Key Vault, including Azure SDK clients, DefaultAzureCredential/managed identity, configuration providers, secret retrieval, caching, retries, lifecycle, and runtime failures. Use for Java microservice Key Vault integration.
---

# Analyze Spring Boot Integration

1. Trace application configuration and runtime code paths that access Key Vault.
2. Identify SDK/configuration library, credential chain, vault URI, and object references.
3. Inspect client lifecycle, retry policy, secret/key/certificate access pattern, and caching.
4. Verify managed identity or Workload Identity selection in the deployment environment.
5. Correlate application errors with Key Vault RBAC, network, throttling, and object state.
6. Route generic framework issues to relevant `spring-boot-*` skills.
7. Never log secret values or access tokens.

## Output
- Integration Flow
- Credential Resolution
- Retrieval/Caching Findings
- Runtime Correlation
- Recommended Action
