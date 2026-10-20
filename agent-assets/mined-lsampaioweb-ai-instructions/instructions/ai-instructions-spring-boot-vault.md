---
description: "Spring Cloud Vault client integration contract for dependencies, Config Data, KV secrets, runtime reads, and tests."
applyTo: "**/pom.xml, **/src/main/resources/application*.yml, **/src/main/resources/application*.yaml, **/*Vault*.java, **/vault/**/*.java"
---

# Spring Cloud Vault Integration Contract

Apply this contract only when a Spring Boot application integrates with Vault.
It governs the client, not Vault server provisioning or secret-engine setup.

Pom owns the Boot ↔ Cloud BOM train. Configuration owns profiles and secrets.
TLS owns certificate validation. Architecture and testing own boundaries and
verification. Do not build a custom `RestClient` for Vault.

## Dependency

- Import `spring-cloud-dependencies` as a BOM; choose the train from the pom
  contract (Boot 4.1.x: `2025.1.2` or newer). Do not pin Vault starter versions
  outside the BOM.
- Add `spring-cloud-starter-vault-config`.

## Startup secrets

- Prefer Config Data (`spring.config.import` with `vault:///...`) for secrets
  required at startup.
- Use an explicit import context and property prefix when binding KV keys.
- Set `spring.cloud.vault.kv.backend` and `backend-version` to match the mount
  (version 2 only for KV v2).
- Keep import path, mount, and secret path consistent when the same data is also
  read at runtime.
- Set `spring.cloud.vault.fail-fast: true` when the app cannot start without Vault.
- Bind through `@ConfigurationProperties` and reject missing/blank required keys
  at startup; fail-fast alone does not validate individual keys.

## Authentication and transport

- Supply tokens or auth credentials from the environment or a secret store.
- Prefer a scoped production identity over a local root/dev token.
- Use HTTPS for production Vault and keep certificate validation enabled.
- Never log token or secret values.

## Explicit runtime reads

- Use `VaultOperations` only when Config Data is not enough.
- For KV v2, use `opsForVersionedKeyValue(mountPath).get(secretPath)` and validate
  the data; do not hand-parse Vault HTTP envelopes.
- Static KV values are not renewable leases. Add scheduled polling only when the
  feature explicitly needs runtime refresh, and replace the cache atomically after
  validating required keys.

## Testing

- Keep unit/context tests independent of a live Vault server (disable Vault,
  supply test properties for required keys).
- Mock `VaultOperations` for runtime-read unit tests.
- Report live-Vault integration as unverified unless an environment-dependent
  test actually runs against Vault.

## Forbidden

- Never build a custom HTTP client for Vault access.
- Never put Vault server deployment, policies, or engine provisioning in this
  client contract.
