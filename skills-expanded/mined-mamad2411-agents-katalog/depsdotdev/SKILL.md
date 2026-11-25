---
name: depsdotdev
description: Use the deps.dev API, also called Open Source Insights, to fetch package metadata, versions, dependency graphs, advisories, project mappings, and hash lookups. Use this skill when the user mentions deps.dev, Open Source Insights, package or version lookups, dependency intelligence, resolved dependency graphs, purl lookups, advisory queries, or integrating the deps.dev API into code.
version: 1.0.0
source: https://docs.deps.dev/api/
license: MIT
---

# deps.dev API

Use this skill to map package coordinates (`system/name/version`) to high-signal dependency intelligence from Open Source Insights.

## Start Here

- Prefer stable API base: `https://api.deps.dev/v3`
- Use `v3alpha` only when you need purl and batch endpoints
- Percent-encode all path/query values before sending requests
- Use canonical values returned in responses (`packageKey`, `versionKey`, `projectKey`) for follow-up calls

## Fast Routing

| If you need to... | Use | Read |
|---|---|---|
| List versions for a package | `GetPackage` | `references/endpoint-map.md` |
| Inspect one version (licenses, advisories, links) | `GetVersion` | `references/endpoint-map.md` |
| Get declared constraints | `GetRequirements` | `references/endpoint-map.md` |
| Get resolved dependency graph | `GetDependencies` | `references/endpoint-map.md` |
| Map project repo to package versions | `GetProjectPackageVersions` | `references/endpoint-map.md` |
| Query by file hash or exact version key | `Query` | `references/endpoint-map.md` |
| Avoid encoding mistakes | URL/purl rules | `references/request-shapes-and-encoding.md` |
| Handle limits and error cases | batch/query limits | `references/limits-errors-and-reliability.md` |
| Use purl/batch/dependents | `v3alpha` features | `references/v3alpha-extras.md` |

## Minimal Workflow

1. Normalize user input into `{system, name, version?}`.
2. Call `GetPackage` if version is missing; prefer `isDefault` or newest published version.
3. Call `GetVersion` for license/advisory/provenance metadata.
4. Add `GetRequirements` and `GetDependencies` when user asks "declared" vs "resolved" dependency questions.
5. If input is a hash or purl, use `Query` or `v3alpha` purl endpoints.

## Examples

- Curl patterns and jq snippets: `examples/curl-cheatsheet.md`

## External Docs

- API overview and versions: https://docs.deps.dev/api/
- Stable REST schema: https://docs.deps.dev/api/v3/
- Experimental REST schema: https://docs.deps.dev/api/v3alpha/
