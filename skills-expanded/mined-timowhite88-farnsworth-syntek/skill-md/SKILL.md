# SYNTEK Memory Service

> 7-layer recursive agent memory with context branching, holographic recall, and on-chain persistence via DropClaw.

## Endpoint

`https://ai.farnsworth.cloud/memory`

## Authentication

All routes except `/memory/health` and `/memory/skill` require an API key:
```
Authorization: Bearer <api-key>
```
Or:
```
X-API-Key: <api-key>
```

## MCP Integration

```bash
claude mcp add farnsworth-syntek -- npx farnsworth-syntek-mcp
```

### MCP Tools

| Tool | Description |
|------|-------------|
| `syntek_recall` | Search memory across all 7 layers |
| `syntek_store` | Store knowledge to a specific layer |
| `syntek_learn` | Process conversation into structured memory via 5-pass compiler |
| `syntek_identity` | Get/set core identity genome |
| `syntek_graph` | Query knowledge graph (entities, paths, neighborhoods) |
| `syntek_branch` | Manage context branches (create, switch, merge, delete) |
| `syntek_context` | Get current context snapshot with budget info |
| `syntek_status` | Check memory status across all layers |
| `syntek_session_end` | Trigger dream consolidation + upload memory to chain via DropClaw |
| `syntek_subscribe` | Initiate or check on-chain subscription |

## REST API

### Public

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/memory/health` | Health check |
| `GET` | `/memory/skill` | This file |

### Authenticated

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/memory/recall` | Search memory — `{ query, topK?, layers?, minRelevance? }` |
| `POST` | `/memory/store` | Store knowledge — `{ content, layer?, importance?, tags? }` |
| `GET` | `/memory/identity` | Get identity genome |
| `PUT` | `/memory/identity` | Update identity — `{ preferences }` |
| `GET` | `/memory/status` | Full memory status with layer stats |
| `POST` | `/memory/branch` | Create branch — `{ name }` |
| `GET` | `/memory/branch` | List branches |
| `DELETE` | `/memory/branch` | Delete branch — `{ name }` |
| `POST` | `/memory/branch/merge` | Merge branch — `{ name, strategy? }` |
| `POST` | `/memory/subscribe` | Start subscription — `{ wallet, tier }` |
| `GET` | `/memory/subscribe` | Check subscription status |
| `POST` | `/memory/sync` | Upload memory to chain via DropClaw (subscribers only) |

## Memory Layers

| # | Layer | Purpose | Token Budget |
|---|-------|---------|-------------|
| L1 | **Identity** | Core preferences, personality, style | 200 |
| L2 | **Active Context** | Working memory with branch support | 2,000 |
| L3 | **Episodic** | Session journal with temporal compression | 16,000 |
| L4 | **Semantic** | Factual knowledge with abstraction levels | 32,000 |
| L5 | **Procedural** | Learned workflows and patterns | 16,000 |
| L6 | **Graph** | Entity-relationship knowledge graph | 32,000 |
| L7 | **Synthesis** | Cross-domain insights and meta-knowledge | 24,000 |

## SYNTEK Compiler (5-Pass)

1. **Extract** — Pull structured knowledge from raw input
2. **Integrate** — Merge with existing knowledge, resolve conflicts
3. **Abstract** — Climb the abstraction ladder (instance > category > concept > principle > axiom)
4. **Synthesize** — Find cross-domain patterns, generate insights
5. **Compress** — Minimize token footprint, maximize information density

## On-Chain Persistence via DropClaw

Syntek uses [DropClaw](https://github.com/timowhite88/dropclaw) for permanent on-chain memory storage. When a session ends (`syntek_session_end`), consolidated memory is encrypted (AES-256-GCM) and uploaded directly to the Monad blockchain as calldata via DropClaw.

**How it works:**
1. `syntek_session_end` triggers dream consolidation (compress + merge memory layers)
2. Consolidated memory is encrypted client-side — Syntek never sees plaintext on-chain data
3. Encrypted memory blob is written directly on-chain as Monad calldata via DropClaw
4. Encryption keys stay with the user in `~/.farnsworth/` — if lost, on-chain data cannot be recovered
5. On next session start, memory is loaded from chain and decrypted locally

**DropClaw access for Syntek subscribers:**
- Syntek subscription ($100/90 days) includes DropClaw access **for Syntek memory uploads only**
- The $30 DropClaw service fee is waived for Syntek memory syncs
- **User still pays Monad gas fees** for on-chain storage (variable, depends on memory size)
- Regular DropClaw usage (non-Syntek file storage) still costs $30 + gas

## Pricing

- **Subscription:** $100 / 90 days via x402 protocol
- **Includes:** Full 7-layer memory engine + DropClaw access for Syntek uploads (gas only)
- **Gas fees:** User pays Monad gas for on-chain memory sync (per session end)
- **Regular DropClaw:** For non-Syntek file storage, standard DropClaw pricing applies ($30 + gas)
- **PlanetExpress:** Syntek subscribers get 50% off marketplace listings ($15 instead of $30)

## Payment Options

| Network | Chain ID | Asset | Pay-To Address |
|---------|----------|-------|---------------|
| Monad | eip155:143 | MON (native) | `0xC86E4a0b90874d8081276AE13e830e23C726229e` |
| Solana | solana:5eykt4... | SOL (native) | `9cQMUBgEPzunpzkjQxV2TMKUUHPFqAHWzNGw9dBzZeSc` |
| Base | eip155:8453 | USDC | `0xC86E4a0b90874d8081276AE13e830e23C726229e` |

## Example Usage

```bash
# Health check
curl https://ai.farnsworth.cloud/memory/health

# Store knowledge
curl -X POST https://ai.farnsworth.cloud/memory/store \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "React hooks enable stateful functional components", "layer": "semantic"}'

# Recall
curl -X POST https://ai.farnsworth.cloud/memory/recall \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "React state management", "topK": 5}'

# Get status
curl https://ai.farnsworth.cloud/memory/status \
  -H "Authorization: Bearer YOUR_KEY"
```
