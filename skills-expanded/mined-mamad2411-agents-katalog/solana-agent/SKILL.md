---
name: solana-agent
description: Scaffold a Solana AI agent using SendAI's Agent Kit v2 and the Solana Developer MCP. Triggers on "Solana agent", "AI agent on Solana", "agent kit", "on-chain agent", "agentic".
---

# Solana AI Agent Scaffolder

Build production-ready AI agents that interact with Solana on-chain. Uses [SendAI's Solana Agent Kit v2](https://github.com/sendaifun/solana-agent-kit) (60+ blockchain actions) and the official [Solana Developer MCP](https://mcp.solana.com/) for real-time docs, account queries, and transaction analysis.

## Why this matters now

The Solana Foundation positions the network as core infrastructure for the agentic internet. 15M+ on-chain agent payments have already been processed. Stablecoins are the default payment rail for agent-to-agent transactions.

## When to use this skill

- "Build an AI agent that trades on Solana"
- "Create an agent that monitors wallet activity"
- "Set up the Solana Agent Kit"
- "I want my agent to do on-chain actions"
- Any project combining AI/LLMs with Solana transactions

## Key ecosystem tools

| Tool | What it does | Link |
|------|-------------|------|
| **SendAI Solana Agent Kit v2** | 60+ blockchain actions, modular plugin system (Token, NFT, DeFi, Blinks), embedded wallet support | [github.com/sendaifun/solana-agent-kit](https://github.com/sendaifun/solana-agent-kit) |
| **Solana Developer MCP** | Official MCP server — real-time docs, account queries, transaction analysis, CPI generation | [mcp.solana.com](https://mcp.solana.com/) |
| **Helius MCP Server** | 60+ tools for querying Solana, sending transactions, webhooks, streaming | [helius.dev/docs/agents/mcp](https://www.helius.dev/docs/agents/mcp) |
| **ElizaOS** | TypeScript agent framework, 200+ plugins, strong Solana integrations | [github.com/elizaos](https://github.com/elizaos) |

## Build mode workflow

### Step 1 — Define the agent's purpose

Ask the founder:
1. **What does the agent do?** (trade, monitor, pay, mint, analyze, automate)
2. **Who triggers it?** (user command, cron schedule, on-chain event, webhook)
3. **What on-chain actions does it need?** (transfer SOL/tokens, swap, stake, mint NFT, read account data)
4. **What LLM integration?** (Claude API, OpenAI, LangChain, Vercel AI SDK)
5. **Wallet strategy?** (embedded via Turnkey/Privy, server-side keypair, user wallet via adapter)

### Step 2 — Scaffold the project

Based on answers, generate:

1. **Project structure**
   ```
   solana-agent/
   ├── src/
   │   ├── agent.ts          # Agent logic + LLM integration
   │   ├── actions/          # Custom on-chain actions
   │   ├── plugins/          # Agent Kit plugin configuration
   │   └── wallet.ts         # Wallet/key management
   ├── .env.example          # RPC, API keys, wallet config
   └── package.json
   ```

2. **Agent Kit plugin selection** — pick from:
   - `@solana-agent-kit/plugin-token` — transfer, swap, create tokens
   - `@solana-agent-kit/plugin-nft` — mint, transfer, burn NFTs
   - `@solana-agent-kit/plugin-defi` — stake, lend, provide liquidity
   - `@solana-agent-kit/plugin-blinks` — create and register Blinks

3. **MCP server configuration**
   ```bash
   # Add Solana Developer MCP to Claude Code
   claude mcp add --transport http solana-mcp-server https://mcp.solana.com/mcp

   # Add Helius MCP for enhanced querying
   claude mcp add helius-mcp-server
   ```

4. **Embedded wallet setup** (Turnkey or Privy) for secure key management without exposing private keys in code

### Step 3 — Implement core agent logic

```typescript
import { SolanaAgentKit } from "@solana-agent-kit/core";
import { TokenPlugin } from "@solana-agent-kit/plugin-token";

const agent = new SolanaAgentKit({
  rpcUrl: process.env.HELIUS_RPC_URL,
  wallet: embeddedWallet, // Turnkey/Privy managed
  plugins: [new TokenPlugin()],
});
```

### Step 4 — Deploy and test on devnet

- Configure devnet RPC
- Fund agent wallet with devnet SOL via faucet
- Run agent actions and verify on-chain state
- Set up monitoring/logging for production

## Hard rules

1. **Never store private keys in code or environment variables in production.** Use embedded wallet providers (Turnkey, Privy) or secure secret managers.
2. **Always start on devnet.** Never deploy untested agent logic to mainnet.
3. **Set transaction limits.** Agent actions should have configurable max amounts and rate limits.
4. **Log every on-chain action.** Agents must maintain an audit trail of all transactions.
5. **Handle RPC failures gracefully.** Use retry logic and RPC failover (Helius → QuickNode fallback).

## Reference links

- [Solana AI ecosystem overview](https://solana.com/ai)
- [SendAI Agent Kit docs](https://github.com/sendaifun/solana-agent-kit)
- [Solana Developer MCP](https://mcp.solana.com/)
- [Helius MCP Server](https://www.helius.dev/docs/agents/mcp)
- [Helius: How to use AI to build Solana apps](https://www.helius.dev/blog/how-to-use-ai-to-build-solana-apps)
