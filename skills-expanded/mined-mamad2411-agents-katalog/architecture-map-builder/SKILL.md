---
name: architecture-map-builder
description: Use to build a service / component map from a GitHub or GitLab monorepo or set of repos. Detects services, languages, internal dependencies (HTTP/SDK/import), and emits a Mermaid diagram + a service catalog YAML.
---

# Architecture Map Builder

## When to invoke
- "Map our microservices architecture from the GitHub org."
- "Generate a service catalog from these repos."
- "Show internal dependencies between services."

## Inputs needed
1. **Path** — local path to a monorepo or directory of cloned repos.
2. **Org / repo list** (optional) — for GitHub mode.
3. **Heuristics** — patterns that identify a service (Dockerfile, package.json, pyproject.toml, etc).

## Workflow
1. **Discover** services — walk for service markers (Dockerfile / k8s manifest / package manifest).
2. **Classify** language and framework.
3. **Detect dependencies** — scan source for known service hostnames, package imports, OpenAPI clients.
4. **Emit**:
   - `services.yml` — catalog with name, path, language, owners, deps.
   - `architecture.mmd` — Mermaid graph of services + dependencies.
   - Markdown summary with risks (orphan services, cyclic deps, missing owners).

## Output format
- `architecture.mmd` (Mermaid)
- `services.yml` (catalog)
- `report.md` (summary + risks)

## Guardrails
- Never claim a dep without a literal source reference.
- Flag services without owners (CODEOWNERS or `OWNERS` file) as risk.
- Detect cycles and report; do not silently render them.

## Reference code
`map.py` walks a path, detects services, infers deps, and writes outputs.
