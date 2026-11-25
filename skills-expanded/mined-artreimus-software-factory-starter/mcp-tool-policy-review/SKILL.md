---
name: mcp-tool-policy-review
description: Use when adding, changing, or reviewing MCP servers, agent tools, provider integrations, credentials, scopes, or tool approval behavior.
---

# MCP Tool Policy Review

## Workflow

1. Read `AGENTS.md`, `docs/MCP_TRUST_BOUNDARY.md`, and the affected tool policy.
2. Classify each tool as read-only, external write, destructive, credential-bearing, or expensive.
3. Verify the policy names allowed operations, denied operations, scopes, approval behavior, logging, and validation.
4. Check that secrets are not stored in prompts, docs, screenshots, or example configs.
5. Confirm permission enforcement lives in code or configuration, not only prompt text.
6. Recommend tests or manual validation for the trust boundary.

## Required Findings

Report a finding when:

- destructive or external-write tools lack approval gates
- tool scopes are vague or impossible to enforce
- credentials can leak into model context or logs
- examples contain real secrets or private endpoints
- logging omits necessary audit context or stores sensitive payloads

## Output

Lead with findings. Include the affected tool, risk, file reference, and concrete fix.
