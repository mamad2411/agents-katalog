---
applyTo: "**/*.{json,jsonc}"
---

# JSON Conventions

## Parameter Files

- Bicep parameter files: `infra/bicep/{customer}/parameters/{env}.bicepparam`
- Terraform var files: `infra/terraform/{customer}/environments/{env}.tfvars`
- Never hardcode subscription IDs, tenant IDs, or secrets in parameter files

## MCP Config

- MCP server config: `mcp/mcp-config.json`
- 3 servers: azure-pricing, azure-platform, drawio

## Subscriptions

- Subscription mapping: `environments/subscriptions.json`
- Maps environment names to subscription IDs
