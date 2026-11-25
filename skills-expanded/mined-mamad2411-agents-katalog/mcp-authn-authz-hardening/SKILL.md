---
name: mcp-authn-authz-hardening
description: Use when MCP servers require explicit authentication and authorization hardening for protected tools, resources, and transport boundaries.
---

# MCP Authn/Authz Hardening

## Specialization

Harden MCP authentication and authorization controls with explicit security boundaries and verification evidence.

## Trigger Conditions

- Server tools or resources expose sensitive operations.
- Token and authorization boundaries are unclear.
- Security review identifies access-control risk.

## Hard Constraints

- Security controls must align with official MCP documentation and specification.
- Secrets and sensitive data must be protected and redacted in artifacts.

## Inputs

- Protected operation inventory.
- Current authn/authz architecture.
- Threat model and trust boundaries.

## Required Outputs

- Access-control policy matrix.
- Token and session handling controls.
- Security test checklist and findings summary.

## Deterministic Workflow

1. Enumerate protected tools/resources.
2. Map authn and authz requirements per operation.
3. Validate token, session, and header handling.
4. Verify deny-by-default behavior.
5. Publish hardening findings and remediation actions.

## Access Matrix Template

| Surface | Auth Required | Role or Scope | Deny-by-Default Verified | Notes |
|---|---|---|---|---|
| Tool A | Yes | <scope> | Yes or No | <notes> |
| Resource B | Yes | <scope> | Yes or No | <notes> |

## Done Criteria

- Access-control matrix is complete.
- Critical authn/authz gaps have remediation actions.
- Security evidence is explicit and reviewable.
