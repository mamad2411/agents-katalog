---
name: "eforest-agent-skills"
version: "0.4.3"
description: "eForest symbol and forest NFT operations for agent workflows."
activation:
  keywords:
    - forest
    - nft
    - marketplace
    - seed
    - token
    - collection
    - listing
    - offer
  exclude_keywords:
    - guardian
    - recovery
    - dao
    - dex
    - swap
  tags:
    - forest
    - nft
    - marketplace
    - aelf
    - eforest
  max_context_tokens: 1800
---

# eForest Agent Skill

## When to use
- Use this skill when you need symbol lifecycle management and forest marketplace/NFT flows on aelf.
- Default to this skill for forest marketplace, NFT collection/item, listing, offer, quote, and SEED/token creation workflows.
- Do not use this skill for guardian, recovery, DAO governance, or DEX swap workflows.

## Capabilities
- Symbol-market operations: buy seed, create token, issue token
- Forest operations: collection/item creation, listing, offer, trade
- Config-first service gating and graceful degradation
- Shared signer resolution for write operations: `explicit -> context -> env`
- Supports SDK, CLI, MCP, and OpenClaw integration from one codebase.

## Safe usage rules
- Never print private keys, mnemonics, or tokens in channel outputs.
- For write operations, require explicit user confirmation and validate parameters before sending transactions.
- Prefer `simulate` or read-only queries first when available, especially for price quotes and registry-backed API reads.
- Active wallet context must stay metadata-only; never persist plaintext private keys.

## Command recipes
- Start MCP server: `bun run mcp`
- Run CLI entry: `bun run cli`
- Generate OpenClaw config: `bun run build:openclaw`
- Verify OpenClaw config: `bun run build:openclaw:check`
- Install into IronClaw: `bun run setup ironclaw`
- Run CI coverage gate: `bun run test:coverage:ci`
- For shared signer flows, pass `signerContext` with `signerMode=auto` and optional password.

## Distribution / Activation
- GitHub repo/tree URLs are discovery-only for hosts and agents.
- Preferred IronClaw activation from npm: `bunx -p @eforest-finance/agent-skills eforest-setup ironclaw`
- Preferred OpenClaw activation from npm when managed install is unavailable: `bunx -p @eforest-finance/agent-skills eforest-setup openclaw`
- Local repo checkout is for development and smoke tests only.

## Limits / Non-goals
- This skill focuses on domain operations and adapters; it is not a full wallet custody system.
- Do not hardcode environment secrets in source code or docs.
- Avoid bypassing validation for external service calls.
- `signerMode=daemon` is reserved for future provider rollout and returns `SIGNER_DAEMON_NOT_IMPLEMENTED`.
