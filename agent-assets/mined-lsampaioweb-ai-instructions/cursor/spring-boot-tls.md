---
description: "Spring Boot HTTPS and TLS contract for embedded TLS, certificate material, keystores, and transport-security boundaries."
globs: "**/src/main/resources/application*.yml,**/src/main/resources/application*.yaml,**/*Ssl*.java,**/*Tls*.java,**/*Https*.java,**/Dockerfile,**/docker-compose*.yml"
alwaysApply: false
---

# Spring Boot HTTPS and TLS Contract

These rules apply when an application terminates HTTPS itself or defines TLS-related
runtime settings. They do not require embedded TLS when a trusted reverse proxy or
ingress terminates TLS before traffic reaches the application.

## Ownership

- Defer general YAML structure, profiles, environment variables, and secret handling
  to `spring-boot-config.mdc`.
- Defer certificate and keystore ignore patterns to `spring-boot-gitignore.mdc`.
- Defer endpoint authorization and anonymous-access rules to
  `spring-boot-security.mdc`.
- Defer human-facing setup and certificate instructions to
  `spring-boot-readme.mdc`.
- Keep proxy-specific TLS termination, routing, and middleware rules in the
  deployment or proxy contract that owns them.

## Embedded TLS

- Enable `server.ssl.enabled` only when the Spring Boot application terminates TLS.
- Use a PKCS12 keystore for embedded HTTPS unless an explicit compatibility
  requirement requires another supported store type.
- Supply the keystore password through an environment variable or external secret
  source.
- Keep the keystore path, store type, enabled protocols, and HTTPS port in
  environment-appropriate configuration.
- Enable TLS 1.3 as the minimum protocol baseline unless a documented client
  compatibility requirement requires a different supported protocol set.
- Enable HTTP/2 only when the deployment and clients support it; do not add it merely
  because HTTPS is enabled.
- Keep development and production TLS settings in their matching profile files when
  the settings differ by environment.
- Use a truststore only when the application must validate client certificates or
  outbound peer certificates. Do not add mutual TLS by default.
- Make the TLS termination boundary explicit when a reverse proxy, ingress, or
  service mesh terminates HTTPS before the application.

## Certificate material

- Keep private keys, keystores, truststores, and certificate passwords outside source
  control.
- Load certificate passwords and externally managed certificate paths from the
  environment or an approved secret source.
- Use local-only development certificates only when they are clearly isolated from
  production material.
- Document the required certificate, keystore, and truststore inputs without including
  private material or real passwords.
- Do not copy certificate material into Docker images or committed application
  resources.

## Validation and operations

- Verify that the configured keystore path exists in the intended runtime environment
  before declaring embedded TLS ready.
- Verify that the configured protocol set and HTTPS port match the deployment boundary.
- Treat TLS-dependent tests as environment-dependent when certificate material or a
  running HTTPS endpoint is required.
- Report missing certificates, invalid passwords, handshake failures, and unsupported
  protocols as environment or configuration failures rather than masking them.
- Reuse the existing project verification policy for compilation and tests.

## Forbidden

- Never commit private keys, keystores, truststores, or plaintext certificate
  passwords.
- Never enable embedded TLS and configure proxy termination for the same traffic path
  without documenting the intended boundary.
- Never use a development certificate or password in production configuration.
- Never disable certificate validation to make a local or integration test pass.
- Never add mutual TLS, custom truststores, or certificate pinning without an explicit
  product or deployment requirement.
- Never claim HTTPS is configured based only on an `application.yml` entry; verify the
  certificate material and runtime boundary.
