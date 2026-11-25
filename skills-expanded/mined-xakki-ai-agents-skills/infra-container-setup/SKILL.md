---
name: infra-container-setup
description: 'Scaffold a project with containers when containerization is requested or required. Use for a new or existing project that needs a Docker/Compose setup. RU: новый Docker-проект, контейнеризация.'
disable-model-invocation: true
---

# Containerized project setup

Use when a new or existing project explicitly needs a container-based development or deployment setup. Inspect its stack, existing repository, tooling, runtime contracts and requested scope before proposing files. Do not assume every project needs Docker, Compose, a Makefile, a particular logging provider or a running service.

Select a minimal container image and, when appropriate, a Compose configuration for the actual components. Define ports, health checks, state, resource constraints, secrets and configuration according to the project's needs and security policy. Provide documented commands and an example configuration only when useful and authorized; never commit real secrets. Preserve existing files and staged work.

The [historical templates](templates.md) contain examples for a particular stack. Use them only after checking that each dependency and convention matches the project; do not blindly add vendor libraries, submodules or observability endpoints. A request to write container files does not automatically authorize starting services, publishing images or deploying. Validate the files with suitable project-supported checks and report which runtime behavior remains unverified.
