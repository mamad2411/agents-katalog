---
name: "secrets-management-azure-key-vault"
description: "Implement Azure Key Vault secrets management for all LeadPerfection Spring Boot 4.x microservices — Spring Cloud Azure Key Vault integration, zero-secret-in-code pattern, secret rotation, and CI/CD pipeline vault access."
version: 1
created: "2026-06-21"
updated: "2026-06-21"
---
## When to Use
Use when adding any credential or sensitive config to a microservice — DB creds, JWT signing keys, Service Bus strings, API keys. Never commit secrets to source. Per ADR anti-patterns table. Stack: spring-cloud-azure-starter-keyvault-secrets + BOM 7.3.0 + Managed Identity (DefaultAzureCredential).

## Procedure
1. STEP 1 — ADD dependency to pom.xml (version from BOM 7.3.0): spring-cloud-azure-starter-keyvault-secrets under com.azure.spring groupId.
2. STEP 2 — CONFIGURE application.yml: spring.cloud.azure.keyvault.secret.endpoint = https://${AZURE_KEYVAULT_NAME}.vault.azure.net/ and property-source-enabled: true. Key Vault secrets auto-inject as Spring @Value properties using their Key Vault name.
3. STEP 3 — MANAGED IDENTITY: Enable System-Assigned Managed Identity on each App Service. Grant Key Vault Secrets User RBAC role to the identity. No credentials in code or config files.
4. STEP 4 — STORE ALL SENSITIVE CONFIG in Key Vault. Naming convention: {service}-{env}-{config-item} e.g. sales-dev-db-cred. Required entries per service: DB credential, JWT signing key, NVD API key for SAST, Service Bus namespace config, ZAP scan service principal for DAST pipeline.
5. STEP 5 — ROTATION POLICY: Set 90-day expiry on all Key Vault entries (per Security.md). Enable expiry notifications 30 days before. Spring Cloud Azure auto-reloads rotated values without restart via Key Vault versioning.
6. STEP 6 — LOCAL DEV: Use Azure CLI auth (az login) pointing to DEV vault only. Add application-local.yml with dev vault endpoint, gitignored. Never allow local dev to access UAT or PROD vault.
7. STEP 7 — AZURE DEVOPS PIPELINE: Link Azure DevOps variable groups to Key Vault via the Key Vault integration in Library. Reference as $(variable-name) in pipeline YAML. Never echo or print secret variables in pipeline logs.

## Pitfalls
- Key Vault secret naming uses hyphens: sales-dev-db-cred maps to Spring property sales-dev-db-cred (hyphenated), NOT dot notation. Use hyphens consistently.
- Managed Identity must be assigned BEFORE app startup. If assigned after first deploy, restart the App Service instance to pick up the identity.
- Spring Cloud Azure Key Vault property source loads at startup. Rotated values are picked up on refresh, but @Value fields are NOT live-updated unless using @RefreshScope. Use Environment.getProperty() for values that must stay current.
- NEVER put Key Vault entries in azure-pipelines.yml in plaintext. Always use $(variable-group-name.variable-name) references from a linked variable group.
- Do not grant Key Vault Secrets Officer (write) role to app Managed Identity. Grant only Key Vault Secrets User (read-only). Write access is for ops/infra only.

## Verification
1. Application starts with no 401 errors from Key Vault in startup logs
2. curl /actuator/health returns UP with no Key Vault connection errors
3. Source scan: grep -r 'jdbc\|signing\|apikey' src/main/resources/ returns no matches
4. Azure portal Key Vault Secrets shows all required entries with expiry dates
5. Rotate a test entry in Key Vault and verify Spring app picks up new value within refresh interval without restart