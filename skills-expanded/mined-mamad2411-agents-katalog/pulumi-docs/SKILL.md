---
name: pulumi-docs
description: 'Access and fetch Pulumi documentation, registry schemas, and READMEs in markdown format. You MUST load this skill when retrieving Pulumi documentation.'
license: MIT
---

# Pulumi Documentation

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- Fetching documentation or schemas programmatically (e.g., parsing `https://www.pulumi.com/llms.txt`).
- Retrieving provider READMEs or documentation via the Pulumi Registry API.
- Accessing markdown versions of Pulumi documentation pages.
- Retrieving provider schemas for analysis or code generation.

## WHEN NOT TO USE

- Executing Pulumi CLI commands for stack management (use `pulumi-cli` instead).
- Writing infrastructure code.

## Core Principles

- **Markdown First**: Prefer fetching documentation in markdown format for easier processing by AI agents.
- **URL Consistency**: Use standard patterns for fetching markdown (e.g., appending `.md` or using `Accept: text/markdown`).
- **Schema Stability**: Use provider schemas to understand resource structures and requirements.

## Step-by-Step Workflows

### Accessing Markdown Documentation

1. **Fetch Documentation as Markdown**:
   Use `webfetch` with `Accept: text/markdown` or append `.md` to the URL.
   `curl -H "Accept: text/markdown" https://www.pulumi.com/docs/iac/concepts/resources/`
   `curl https://www.pulumi.com/docs/iac/concepts/resources.md`

### Retrieving Registry Documentation

1. **Query Registry API for README**:
   Use `pulumi api` to fetch package READMEs.
   `pulumi api /api/registry/packages/<source>/<publisher>/<name>/versions/latest/readme`

### Retrieving Provider Schemas

1. **Get Schema for Package**:
   `pulumi package get-schema <name>[@version]` (e.g., `pulumi package get-schema aws@6.0.0`)

## Common Pitfalls

- **Missing Auth Token**: The Cloud registry API for private packages requires `Authorization: token $PULUMI_ACCESS_TOKEN`. Ensure environment variables are populated when making direct HTTP calls instead of using `pulumi api`.
- **Incomplete Endpoints**: When using `pulumi api`, remember that type tokens for `docs/{typeToken}` must be URL-encoded (e.g. `random:index/RandomPassword` becomes `random%3Aindex%2FRandomPassword`).

## References

- [Datadog Provider](references/datadog.md)
  MUST be fetched when creating or debugging Datadog infrastructure or monitors in Pulumi.
- <https://www.pulumi.com/llms.txt> - The official Pulumi documentation curated for LLMs.
  MUST be fetched when retrieving comprehensive Pulumi documentation, guides, or overarching provider concepts.
