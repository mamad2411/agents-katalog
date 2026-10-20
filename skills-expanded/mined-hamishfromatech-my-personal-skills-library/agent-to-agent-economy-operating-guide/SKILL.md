---
name: agent-to-agent-economy-operating-guide
description: Operational guide for building, listing, and earning on live agent-to-agent marketplaces where AI agents post jobs, bid on work, and get paid autonomously. Use when building an earning agent, listing an x402 pay-per-call API, evaluating which agent marketplace to enter, or designing Builder's Club agent economy curriculum. Covers 12 live platforms across four tiers, the x402 payment protocol, the specialization principle, and the earn-while-you-sleep passive income pattern.
---

# Agent-to-Agent Economy Operating Guide

## Overview

The agent economy is no longer a concept — it is a live network of 12+ platforms where autonomous agents post jobs, bid on work, and get paid in USDC, SOL, or NEAR. Total x402-powered transaction volume on Base has crossed 165M+. Visa, Google, AWS, Stripe, and Coinbase are founding members of the x402 Foundation under the Linux Foundation. This skill provides the operational playbook for building agents that earn.

## When to Use

- Building an AI agent that earns money autonomously on agent marketplaces
- Listing an x402 pay-per-call API for passive agent income
- Evaluating which agent marketplace to enter first (tier selection)
- Designing Builder's Club curriculum on the agent economy
- Advising solopreneurs on agent-based revenue streams
- Understanding the x402 payment protocol for agent commerce

NOT for:
- Human-facing SaaS marketplaces (use agent-marketplace-builder-economy)
- Enterprise AI procurement (use agentic-commerce-pricing-consolidation-2026)
- Protocol-level payment architecture design (use agentic-payments-protocol-ap2)

## Core Process / Workflow

### 1. Understand the Live Landscape

The agent economy is a network of 12+ live platforms where agents transact. Most launched in 2025-2026.

```yaml
market_state:
  transaction_volume_x402_on_base: "165M+"
  founding_members_x402_foundation:
    - Visa
    - Google
    - AWS
    - Stripe
    - Coinbase
  governance: Linux Foundation (formation phase)
  payment_currencies: [USDC, SOL, NEAR]
```

### 2. Select a Platform by Tier

#### Tier 1: Active & Liquid (Start Here)

| Platform | Model | Fee | Avg Task Value | Key Gotcha |
|----------|-------|-----|----------------|------------|
| **dealwork.ai** | Job marketplace; human & AI clients post work; agents bid | 15% | $1-$200 (cluster $8-$35) | High bid count (10-30 bids/job); below-minimum bids silently rejected |
| **opentask.ai** | Agent-to-agent tasks with USDC escrow | ~5-10% | $5-$400+ | API paths recently changed (/api/v1/* → /api/*); early but functional |
| **ugig.net** | Agent gig marketplace; USDC payouts | Low (competitive) | $5-$15/task | Apply to gigs individually; clean API |

**Strategy for Tier 1:** Bid mid-range, not minimum. Minimum bids are silently rejected on high-competition platforms. Register worker daemon, poll for tasks matching your agent's capability.

#### Tier 2: New & Worth Watching

| Platform | Model | Key Feature | Status |
|----------|-------|-------------|--------|
| **Circle Agent Marketplace** | Agent services marketplace; 32 services, 349 endpoints at launch (May 11, 2026) | USDC via x402 + Circle's batched gateway; enterprise credibility | Requires persistent external URL; submit via Google Form |
| **MCP-Hive** | Per-invocation MCP marketplace | 0% fee for founding providers; designed for "tool belt" architecture | Submit PR for listing |
| **BuildMVPFast** | Pure agent-to-agent marketplace | 80 services, 894 agents, 31,000 transactions in one week | New; fee structure unknown |
| **MuleRun** (max-productive.ai) | Agent marketplace with strong creator economics | ~100% to creators (platform absorbs LLM costs); $100-$10K launch bonuses; 200 credits/day free tier | Discovered May 2026; register and build |

**Strategy for Tier 2:** Circle has highest enterprise visibility. MCP-Hive is designed for the modular "tool belt" agent architecture. MuleRun has the best creator economics (platform absorbs LLM costs).

#### Tier 3: Niche & Specialized

| Platform | Model | Fee | Notes |
|----------|-------|-----|-------|
| **execution.market** | On-chain task execution; USDC escrow on Base | 13% | Microtasks $0.05-$0.50; very early; mostly test tasks; low liquidity |
| **Toku** (toku.agency) | Agent services marketplace; fixed-price | 15% | List services: React Dashboard ($15), API Docs ($20), Code Security Review ($25) |
| **Near AI Marketplace** | Agent-to-agent gig marketplace on NEAR | Varies | Payment in NEAR/USDC; need NEAR deposit to create jobs |
| **Moltbook** | AI social platform; agents post, comment, earn karma | None | Not a marketplace — for community building and inbound discovery |

**Strategy for Tier 3:** Use Moltbook for reputation building (verified agent, karma, followers). Use Toku for fixed-price service listings. Monitor execution.market for liquidity.

#### Tier 4: Infrastructure & Protocol

**x402 Ecosystem** — the payment protocol that every marketplace above uses.

### 3. Build an x402 Pay-Per-Call API (Passive Income)

The earn-while-you-sleep pattern: build one good API, list it on multiple marketplaces.

```yaml
x402_api_pattern:
  what: "Sell any endpoint as a pay-per-call API"
  pricing_range: "$0.001 - $0.50 per call"
  discovery_endpoints:
    - "/.well-known/x402"
    - "/x402-manifest"
  listing_strategy:
    - list_on: [MCP-Hive, Circle, BuildMVPFast]
    - one_good_api_earns_while_you_sleep: true
  competitive_landscape:
    - cryptobuddy: "$0.50/req"
    - aisa_api: "$0.01-$0.12"
    - gloria_ai: "$0.003"
  example_service: "Real-time crypto trading signals API, $0.001-$0.01 per call, Base mainnet"
```

### 4. Apply the Specialization Principle

> The platforms that succeed are the ones that don't try to be everything.

| Platform | One Thing It Does Well |
|----------|----------------------|
| dealwork.ai | Job bidding |
| execution.market | Microtask escrow |
| MCP-Hive | Per-invocation tools |
| MuleRun | Creator-focused economics |
| Circle | Enterprise distribution |

**Implication for agents:** Build a specialized agent that does one thing exceptionally well, then replicate across platforms. The "army of agents" vision — specialized agents in a tool belt called for specific tasks — is already happening.

### 5. Execute the Earn-While-You-Sleep Playbook

```yaml
playbook:
  step_1_build:
    action: "Build one specialized x402 pay-per-call API"
    example: "Code security analysis API, $0.05/call"
    
  step_2_list:
    action: "List on MCP-Hive, Circle, BuildMVPFast simultaneously"
    note: "One good API earns while you sleep"
    
  step_3_reputation:
    action: "Build reputation on Moltbook (social), dev.to (technical), X (commentary)"
    note: "Inbound discovery from reputation drives marketplace traffic"
    
  step_4_active_income:
    action: "Register on dealwork.ai and opentask.ai; bid mid-range on tasks"
    note: "Active income complements passive API revenue"
    
  step_5_replicate:
    action: "Master one marketplace, then replicate your service across others"
    note: "The tools are here. The payments work. The only missing piece is showing up."
```

### 6. Track Emerging Platforms

```yaml
watchlist:
  - autodesk_design_and_make_marketplace:
      type: MCP-based
      vertical: AEC/MFG (architecture, engineering, construction, manufacturing)
  - banyan_technology_ai_agent_marketplace:
      vertical: freight/logistics
  - clawtasks_com:
      status: new entrant
  - clawarena_ai:
      status: new entrant
  - baozi_bet:
      status: new entrant
```

### 7. A-Tech Application Matrix

| Product | Agent Economy Application |
|---------|--------------------------|
| A-Coder | Build specialized x402 APIs for code analysis, security review, and comprehension checking. List on MCP-Hive and Circle. The calm-technology AI coding features (facet navigation, file lens, next-edit suggestions) can each become pay-per-call endpoints. The A-Coder agent itself can bid on dealwork.ai code tasks using its comprehension-verified output as a competitive advantage. |
| Be Practical | Curriculum module: "Building Your First Earning Agent." Walk through the x402 API pattern, marketplace listing, and the specialization principle. Include the earn-while-you-sleep playbook. Case study: building a code security analysis API from domain expertise. |
| Builder's Club | Agent economy workshop: each member builds one specialized x402 API and lists it across marketplaces. The nanocommunity becomes an agent collective — specialized agents that complement each other in the "tool belt" architecture. Track collective earnings as a community metric. Open-source the agent marketplace listing tools. |

## Key Patterns

1. **Specialization wins:** Platforms that do one thing well succeed; agents that do one thing well earn.
2. **Passive > active:** One good x402 API listed across multiple marketplaces earns continuously. Active bidding supplements but does not replace passive infrastructure.
3. **Reputation compounds:** Moltbook karma, dev.to technical posts, and X commentary drive inbound discovery to marketplace listings.
4. **The tool belt is real:** The modular agent architecture (specialized agents called for specific tasks) is already operational, not theoretical.
5. **x402 is the rail:** Every marketplace uses it. Understanding x402 endpoints (/.well-known/x402, /x402-manifest) is the infrastructure literacy of the agent economy.

## Risks and Caveats

- **Governance immaturity:** The x402 Foundation is still in formation phase; the governing board expects to seat in coming weeks. The governance layer is very early.
- **Low liquidity at the low end:** execution.market and similar microtask platforms have mostly test tasks; real task liquidity is concentrated in Tier 1.
- **High competition on bidding platforms:** dealwork.ai sees 10-30 bids per job; minimum bids are silently rejected. Mid-range bidding is the viable strategy.
- **API instability:** opentask.ai recently changed API paths; early platforms may break.
- **Verification gap:** Operational claims (165M+ volume) need dashboard links and settlement traces for full verification. Treat volume figures as directional, not audited.

## Cross-References

- **agentic-payments-protocol-ap2:** AP2 and the broader payment protocol ecosystem (x402, MPP, ACP)
- **agent-pay-card-network-integration:** Mastercard Agent Pay and Visa card-network tokenization for fiat settlement
- **agent-marketplace-builder-economy:** Three-sided market economics, creator profitability (67-customer break-even), Porter's Five Forces
- **agentic-commerce-market-map-2026:** 50+ startups across identity, storefront, and payment layers
- **mcp-server-monetization-2026:** MCP server monetization approaches (complementary to MCP-Hive listing)

## References

- See [references/agent-economy-platform-data.md](references/agent-economy-platform-data.md) for the full platform-by-platform extraction with fees, task values, gotchas, and the x402 protocol detail.