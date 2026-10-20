---
description: "Spring Cloud Config contract for Config Server Git backends, clients, credentials, and Config Data import."
applyTo: "**/pom.xml, **/src/main/resources/application*.yml, **/src/main/resources/application*.yaml, **/*ConfigServer*.java, **/cloud/config/**/*.java"
---

# Spring Cloud Config Contract

Apply this contract when a module is a Spring Cloud Config Server or a Config
client. Pom owns the Boot ↔ Cloud BOM train. Configuration owns profiles and
secrets. TLS owns HTTPS keystores and trust. Security owns filter-chain style.
Vault remains a separate secrets integration (Vault contract).

## Shared dependency management

- Import `spring-cloud-dependencies` as a BOM; choose the train from the pom
  contract (Boot 4.1.x: `2025.1.2` or newer). Do not pin Config Server/client
  artifact versions outside the BOM.

## Config Server

- Add `spring-cloud-config-server` and annotate the application with
  `@EnableConfigServer`.
- Point `spring.cloud.config.server.git.uri` at the configuration Git repo
  (local file URI or remote URL). Prefer an environment override for the path or
  URL, and set `cloneOnStart: true` when the server should clone before serving.
- Use `search-paths: "{application}/{profile}"` so `spring.application.name` +
  active profile select the right folder under the Git backend.
- Protect client-facing config HTTP paths with authentication; supply server and
  client passwords from the environment (for example HTTP Basic with
  `CONFIG_SERVER_*` / `CLOUD_CONFIG_CLIENT_*`).
- Development may serve plain HTTP. When the server serves HTTPS, follow the TLS
  contract for keystore settings.
- Initialize the configuration Git backend before first run when using a fresh
  local repository (commit at least one application/profile tree).

## Config client

- Add `spring-cloud-starter-config`.
- Set `spring.application.name` to the Git application folder name the server
  should serve.
- Import Config Data with `spring.config.import` pointing at the Config Server
  URL (for example `optional:configserver:http://localhost:8888` in development
  and an HTTPS URL in production).
- Supply `spring.cloud.config.username` / `password` from the environment when
  the server requires auth; values must match the server.
- Bind remote properties through `@ConfigurationProperties` in the feature
  package.
- Keep context tests independent of a live Config Server (for example
  `optional:configserver:` import and `spring.cloud.config.fail-fast=false` in
  tests).

## Forbidden

- Never commit Config Server or client passwords in YAML.
- Never pin `spring-cloud-config-*` versions outside the Cloud BOM.
- Never hardcode a machine-specific Git path when an environment override
  (for example `CONFIG_REPO_PATH`) can keep the URI portable.
- Never use Cloud Config as a substitute for Vault when the value is a secret
  that belongs in a secret store (Vault contract).
