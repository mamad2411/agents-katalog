---
name: azure-blob-storage-12-implementation
description: Implements and migrates Azure Blob Storage client-library v12 features. Use when adding blob upload, download, listing, metadata, tags, copy, lease, delete, or migration logic in .NET, JavaScript, Python, or Java projects.
license: MIT
compatibility: Requires a project using Azure Blob Storage SDK v12 or an explicit migration target to SDK v12.
---

# Azure Blob Storage 12 Implementation Skill

Use this skill for Azure Blob Storage client-library v12 feature work and migration.

## When To Use

Use this skill when the task involves:

- Adding or changing SDK v12 blob/container operations.
- Introducing passwordless `DefaultAzureCredential`-style clients.
- Replacing legacy v11 Azure Storage Blob SDK APIs.
- Designing upload/download/list/copy/delete flows.
- Handling metadata, tags, ETags, access tiers, leases, or conditions.
- Reviewing language-specific SDK package usage.

## Required First Steps

1. Identify the project language and package manager.
2. Inspect dependency files and lockfiles before writing code.
3. Confirm the codebase uses SDK v12 packages.
4. If the task is migration, read `workflows/migrate-v11-to-v12-workflow.md`.
5. If the task is new feature work, read `workflows/implement-blob-feature-workflow.md`.
6. Use `resources/sdk-v12-language-map.md` to map package names and client concepts.
7. Use `resources/operation-patterns.md` to choose safe operation patterns.
8. Use examples only as patterns, not as copy-paste API authority.

## Workflows

- `workflows/implement-blob-feature-workflow.md`: Use for normal feature implementation.
- `workflows/migrate-v11-to-v12-workflow.md`: Use for v11 or older SDK migration to v12.

## Resources

- `resources/sdk-v12-language-map.md`: Language and package map for common v12 SDK concepts.
- `resources/operation-patterns.md`: Operation-level design guidance.

## Examples

- `examples/passwordless-client-patterns.md`: Passwordless client-construction patterns and boundaries.

## Implementation Rules

- Prefer service/container/blob client separation over global utility wrappers that hide auth, retry, or operation semantics.
- Prefer constructor or dependency-injection patterns that allow test doubles and emulator/local integration tests.
- Keep storage account URL, container names, and blob prefixes configurable.
- Validate container and blob naming rules close to the boundary where names are created.
- Treat container creation as deployment/setup behavior unless the product explicitly creates per-tenant or per-user containers.
- Avoid using connection strings in production paths.
- Do not include broad SAS creation in implementation code unless it is a stated product requirement.
- Avoid manual HTTP calls when the SDK v12 provides a suitable client operation.
- Preserve metadata, tags, content headers, and access tier during copy/replace operations if they are semantically important.
