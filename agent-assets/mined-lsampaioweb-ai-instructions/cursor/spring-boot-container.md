---
description: "Container and Compose contract for build strategy, runtime hardening, profiles, networks, resources, and container operations."
globs: "**/Dockerfile,**/Dockerfile-*,**/docker-compose.yml,**/docker-compose*.yml,**/compose.yml,**/compose*.yml,**/.dockerignore,**/.env.example"
alwaysApply: false
---

# Spring Boot Container Contract

These rules govern container images and Compose-based orchestration for Spring Boot
projects. They are generic container rules. Service-specific contracts own the
configuration and behavior of databases, brokers, caches, secret stores, and proxies.

## Ownership

- Defer application YAML, profiles, and secrets to `spring-boot-config.mdc`.
- Defer HTTPS and certificate handling to `spring-boot-tls.mdc`.
- Defer certificate and secret-file ignore patterns to `spring-boot-gitignore.mdc`.
- Defer health endpoint exposure and authorization to `spring-boot-actuator.mdc`
  and `spring-boot-security.mdc`.
- Defer human-facing container commands and prerequisites to
  `spring-boot-readme.mdc`.
- Keep service-specific infrastructure settings in the contract for that service.

## Image builds

- Use a multi-stage build for deployable application images.
- Keep compilation and dependency resolution in the builder stage; keep the runtime
  stage limited to the application artifact and runtime requirements.
- Copy a locally built JAR into a runtime image only as an explicitly development-only
  workflow.
- Use a base image whose Java runtime matches the project's configured Java version.
- Prefer maintained minimal runtime images. Custom base images are optional, but their
  Java version, user, filesystem layout, and update process must be documented.
- Pin image references to explicit versions. Use immutable digests for production
  deployments when the deployment platform supports them.
- Keep build context small with a focused `.dockerignore`.
- Do not copy source-controlled secrets, local environment files, build caches, or
  unrelated workspace files into an image.

## Runtime identity and hardening

- Run application containers as a non-root user.
- Declare or verify the runtime user explicitly; do not rely on undocumented base-image
  behavior.
- Drop Linux capabilities with `cap_drop: ALL` unless a documented runtime requirement
  needs a specific capability.
- Set `no-new-privileges:true` for application and infrastructure services by default.
- Use a read-only root filesystem with a narrowly scoped `tmpfs` for writable temporary
  paths when the process supports it.
- Mount certificates, configuration, and persistent data read-only unless the process
  must write them.
- Do not grant privileged mode or host namespaces without an explicit operational need.

## Compose profiles and resources

- Default Compose configurations to the `production` application profile.
- Select `development` explicitly for local development; do not hardcode it as the
  shared or production-like default.
- Keep CPU and memory limits in production-like Compose deployments.
- Local-only Compose files may omit resource limits when their purpose is interactive
  development, but the omission must be intentional.
- Load credentials, ports, profile overrides, and environment-specific values from
  environment variables or an ignored `.env` file. Keep `.env.example` free of secrets.
- Use required variable substitution for values that must exist before startup.

## Health, networks, and persistence

- Add a healthcheck for every long-running service when a reliable health command or
  health endpoint exists.
- Use the application's Actuator liveness or readiness endpoint for orchestration
  healthchecks when Actuator is enabled; keep the scheme and port aligned with the TLS
  termination boundary.
- Create project-local Compose networks by default. Use an external network only when
  deployment infrastructure owns that network and the dependency is documented.
- Give persistent data explicit named volumes or host paths with documented ownership.
- Do not treat container replacement as a data backup strategy.
- Expose host ports only when local access or an explicit deployment boundary requires it.

## Logging and TLS boundaries

- Write container logs to stdout/stderr so the container runtime can collect them.
- Keep rolling file logging only when the deployment explicitly requires local files;
  use a documented writable mount for those files.
- Do not assume that a file-only application logger is visible through container logs.
- Default application containers to HTTP when a trusted reverse proxy terminates TLS.
  Use embedded HTTPS only when the TLS contract and deployment boundary require it.
- Document whether TLS terminates in the application, a proxy, or another ingress layer.

## Local-only services

- Mark unauthenticated services, insecure dashboards, public infrastructure ports,
  disabled transport encryption, and development certificates as local-development
  choices.
- Do not carry local-only insecure defaults into production-like Compose files.
- Keep service credentials in environment variables or an approved secret source.
- Use explicit healthchecks and persistence settings for local infrastructure services,
  but defer their service-specific authentication and topology rules to their own
  contracts.

## Forbidden

- Never build a production image from a runtime that uses a different Java major
  version than the application requires.
- Never run a deployable application container as root without a documented exception.
- Never use privileged containers or host-network mode as a convenience workaround.
- Never commit `.env` files, private keys, keystores, or real credentials.
- Never use `development` as the default profile in a production-like Compose file.
- Never publish databases, brokers, caches, secret stores, or administration dashboards
  publicly without an explicit local-only or deployment requirement.
- Never claim a service is ready based only on a running container; use a meaningful
  healthcheck.
- Never assume stdout and rolling-file logging are equivalent without documenting the
  chosen collection path.
