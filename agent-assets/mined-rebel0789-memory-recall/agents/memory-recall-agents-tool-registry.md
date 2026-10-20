# AGENTS.md — Tool Registry

## Scope

Applies to `packages/tool-registry`.

## Rules

- Treat OAF-009 policy as the only authority source for tool invocation.
- Do not accept caller-supplied role, owner, policy, filesystem, network,
  secret, sandbox, or approval authority fields.
- Load executable tool manifests only through reviewed checksum-pinned catalog
  entries.
- Never persist or emit raw grant tokens or secret values.
- Keep filesystem, loopback egress, and secret-reference brokers independent.
- Reuse durable idempotent effect boundaries for writes.
- Do not add arbitrary shell execution, downloaded tools, browser automation,
  public internet access, publishing, or external adapters in this package.
