---
id: bap578-business
name: BAP-578 Business & Monetization
description: Use this skill when planning monetization, pricing, treasury flows, growth strategy, unit economics, go-to-market, or commercial sustainability for BAP-578 Non-Fungible Agents.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Business & Monetization

Use this skill when planning monetization, pricing, treasury flows, growth strategy, and unit economics for BAP-578 Non-Fungible Agents. This skill bridges contract mechanics to business outcomes and provides actionable frameworks for launching, growing, and sustaining an NFA ecosystem.

---

## When to use this skill

- Designing pricing and fee structures for agent minting.
- Planning the freemium-to-paid conversion funnel.
- Modeling treasury inflows, outflows, and sustainability.
- Building a go-to-market strategy for an NFA launch.
- Evaluating partnership and marketplace opportunities.
- Forecasting unit economics and break-even scenarios.
- Reporting on key business metrics to stakeholders.

---

## The Four Identity Questions (Business View)

### 1) Who are you?

The business layer translates on-chain contract mechanics into revenue, growth, and sustainability. It answers: how does this project make money, how does it grow, and how does it stay solvent? The business identity is the commercial wrapper around the technical standard — it defines pricing, positioning, target audiences, and value capture mechanisms.

### 2) What do you remember?

Business memory is derived from on-chain metrics and off-chain analytics:

**On-chain metrics (authoritative):**
- Total agents minted (from `getTotalSupply()`)
- Free mints consumed per user (from `getFreeMints()`)
- Paid mint count (total supply minus free mints)
- Treasury balance (contract balance or treasury address balance)
- Agent funding TVL (sum of all agent balances)
- Active agent ratio (active count / total supply)

**Off-chain metrics (supplementary):**
- User acquisition cost (CAC)
- Free-to-paid conversion rate
- Retention (agents still active after 30/60/90 days)
- Average revenue per user (ARPU)
- Community growth rate (Discord, Twitter, GitHub)

### 3) What can you do?

Build and execute complete business strategies:

- Design pricing models aligned with contract fee mechanics
- Model freemium funnels with conversion projections
- Create treasury management policies
- Plan multi-phase go-to-market launches
- Structure partnership and integration deals
- Build marketplace economics for secondary agent trading
- Project unit economics and break-even timelines
- Design growth loops that leverage the free mint mechanic

### 4) How can I trust it?

All revenue and core business metrics are enforceable or verifiable via on-chain state and events:

- Mint fees flow to the treasury address — verifiable on block explorer
- Free mint allocations are tracked per user on-chain
- Agent funding TVL is computed from on-chain balances
- Treasury withdrawals are tracked via events
- No hidden revenue flows — everything is transparent

---

## Revenue Architecture

### Primary revenue streams

**1. Mint fees (core revenue)**

After each user exhausts their free mint allocation, every subsequent mint requires a fixed fee. This fee is sent to the treasury address as part of the `createAgent` transaction.

Revenue formula:
```
Mint revenue = (Total mints - Free mints) × Mint fee
```

Example: If 10,000 agents are minted, 3,000 are free, and the fee is 0.01 BNB:
```
Revenue = 7,000 × 0.01 = 70 BNB
```

**2. Agent funding fees (optional)**

Agents can hold BNB. A wrapper contract or protocol fee could take a percentage of funding deposits. This is not built into the base contract but can be added via a logic contract or wrapper.

**3. Premium services (off-chain)**

- Hosted vault storage (IPFS pinning, encrypted vaults)
- Premium persona templates and voice profiles
- Custom logic contract development
- Analytics dashboards and reporting
- Priority support and onboarding

**4. Marketplace fees (secondary market)**

If agents are traded on a marketplace (built by you or third-party), a royalty or listing fee captures value from secondary sales. ERC-721 royalty standards (ERC-2981) can be implemented in an upgrade.

**5. Partnership and integration fees**

- B2B licensing of the NFA framework to enterprises
- White-label deployments for other chains or verticals
- API access fees for third-party integrations

---

## Pricing Strategy

### Freemium model (recommended)

The contract's built-in free mint allocation creates a natural freemium funnel:

**Phase 1: Free tier**
- Default free mints per user (e.g., 3)
- Purpose: reduce friction, drive adoption, let users experience the product
- Free-minted tokens are non-transferable (soulbound-like)
- Users learn the value before paying

**Phase 2: Paid tier**
- After free mints, a fixed fee per mint
- Paid tokens are transferable
- Higher perceived value due to transferability

**Phase 3: Premium tier (optional)**
- Discounted bulk minting for enterprises
- Custom metadata templates
- Dedicated logic contract hosting
- SLA-backed vault storage

### Setting the mint fee

Consider these factors:

- **Gas costs on BNB Chain:** typically 0.001-0.005 BNB per transaction
- **Competitive landscape:** what do similar NFT projects charge?
- **Target audience:** developers (price-sensitive) vs. enterprises (value-driven)
- **Revenue goals:** work backward from target monthly revenue

Recommended starting ranges:
- Consumer/developer: 0.005–0.02 BNB per mint
- Enterprise: 0.05–0.5 BNB per mint
- Promotional: temporarily reduced or zero fees for campaigns

### Dynamic pricing (advanced)

Implement pricing tiers based on supply:
```
if (totalSupply < 1000) fee = 0.005 BNB    // early adopter
if (totalSupply < 5000) fee = 0.01 BNB     // growth phase
if (totalSupply >= 5000) fee = 0.02 BNB    // mature phase
```

This requires a contract upgrade to modify fee logic.

---

## Freemium Conversion Funnel

### Funnel stages

```
Awareness → Visit → Connect Wallet → Free Mint → Use Agent → Paid Mint → Retention
```

### Conversion levers

**Awareness → Visit:**
- Content marketing (blog posts, Twitter threads, YouTube)
- Developer documentation and tutorials
- Partnership announcements
- Community events

**Visit → Connect Wallet:**
- Clear value proposition on landing page
- Low-friction wallet connection (RainbowKit)
- Social proof (agent count, community size)

**Connect Wallet → Free Mint:**
- One-click mint with pre-filled defaults
- Clear explanation of what they get
- No payment required (removes biggest friction)

**Free Mint → Use Agent:**
- Guided onboarding after mint
- Dashboard showing agent identity
- Prompt to customize persona and experience
- Integration with chat or automation tools

**Use Agent → Paid Mint:**
- Show value of additional agents (different personas)
- Highlight transferability of paid agents
- Time-limited promotions (bonus free mints via admin)
- Social features (agent collections, leaderboards)

**Paid Mint → Retention:**
- Regular metadata updates and new features
- Community events and competitions
- Logic contract marketplace
- Agent-to-agent interaction features

### Target conversion rates

- Visit → Connect wallet: 15-25%
- Connect wallet → Free mint: 40-60%
- Free mint → Active use: 30-50%
- Active use → Paid mint: 10-20%
- Paid mint → Second paid mint: 15-30%

---

## Treasury Management

### Treasury address setup

Use a multisig wallet (e.g., Safe/Gnosis Safe) as the treasury address. Configure:

- 2-of-3 or 3-of-5 signer threshold
- Named signers with known identities
- Transaction execution requires quorum

### Inflow tracking

Treasury inflows come from:
- Paid mint fees (automatic, on every paid mint)
- Emergency withdraw (admin function, should be rare)

Track by monitoring `Transfer` events to the treasury address and the `AgentCreated` events that indicate paid mints.

### Outflow categories

- **Operations:** hosting, RPC infrastructure, domain names
- **Development:** smart contract audits, frontend development
- **Marketing:** campaigns, partnerships, bounties
- **Reserves:** minimum 3-month operating runway

### Treasury reporting

Publish periodic reports (monthly or quarterly):

```
Treasury Report — Q1 2026
─────────────────────────
Opening balance:     50.00 BNB
Mint revenue:       +35.00 BNB
Funding fees:        +2.50 BNB
Total inflows:      +37.50 BNB

Operations:         -10.00 BNB
Development:        -15.00 BNB
Marketing:           -5.00 BNB
Total outflows:     -30.00 BNB

Closing balance:     57.50 BNB
Runway:              5.75 months (at current burn rate)
```

### Treasury policies

- Maintain minimum 3-month runway at all times.
- No single-signer withdrawals.
- Emergency withdrawals require documented justification.
- Publish reports within 15 days of period end.
- Allocate 10-20% of revenue to a reserve fund.

---

## Go-to-Market Playbook

### Phase 1: Pre-launch (2-4 weeks)

**Goals:** Build awareness, establish community, prepare infrastructure.

- Deploy to testnet and run public testing
- Create documentation and tutorials
- Set up community channels (Discord, Twitter)
- Recruit beta testers and early advocates
- Prepare landing page with mint flow
- Complete security audit (see `bap578-security-audit`)

### Phase 2: Soft launch (1-2 weeks)

**Goals:** Validate with real users, identify issues, tune pricing.

- Deploy to mainnet with limited promotion
- Monitor first 100-500 mints closely
- Collect feedback on UX, pricing, and persona design
- Fix issues rapidly
- Begin community engagement

### Phase 3: Growth (ongoing)

**Goals:** Scale adoption, build partnerships, expand features.

- Launch marketing campaigns
- Partner with AI projects and platforms
- Grant bonus free mints for partner communities
- Build and ship logic contract marketplace
- Add analytics dashboard (see `bap578-analytics`)
- Launch secondary marketplace for agent trading

### Phase 4: Maturity (6+ months)

**Goals:** Sustainable revenue, ecosystem expansion, governance.

- Introduce premium service tiers
- Implement on-chain governance for treasury decisions
- Expand to additional chains (if demand warrants)
- Develop enterprise solutions and B2B offerings
- Consider token economics (if appropriate for the ecosystem)

---

## Key Metrics Dashboard

### North star metric

**Monthly Active Agents (MAA):** agents with at least one on-chain interaction (funding, withdrawal, metadata update, or status change) in the last 30 days.

### Primary metrics

| Metric | Source | Frequency |
|--------|--------|-----------|
| Total agents minted | `getTotalSupply()` | Real-time |
| Paid mint count | Total - free mints | Real-time |
| Treasury balance | Treasury address balance | Real-time |
| Free-to-paid conversion | (Paid users / Free users) × 100 | Weekly |
| Agent funding TVL | Sum of agent balances | Real-time |
| Active agent ratio | Active / Total | Daily |
| Monthly Active Agents | Event-based | Monthly |
| Unique owners | Distinct owner addresses | Real-time |

### Secondary metrics

| Metric | Source | Frequency |
|--------|--------|-----------|
| Mint velocity | Mints per day/week | Daily |
| Average agent balance | TVL / Active agents | Daily |
| Metadata update frequency | MetadataUpdated events | Weekly |
| Logic contract adoption | Agents with non-zero logic | Weekly |
| Churn rate | Agents deactivated / Total | Monthly |

---

## Unit Economics

### Cost structure

**Fixed costs (monthly):**
- RPC infrastructure: varies by provider
- Domain and hosting: minimal
- Team compensation: project-dependent

**Variable costs (per mint):**
- Gas subsidy (if sponsoring user gas): ~0.001-0.003 BNB
- Metadata storage (IPFS pinning): minimal per agent
- Support overhead: scales with user count

### Break-even analysis

```
Break-even mints = Fixed monthly costs / (Mint fee - Variable cost per mint)
```

Example:
```
Fixed costs:    5 BNB/month
Mint fee:       0.01 BNB
Variable cost:  0.001 BNB

Break-even = 5 / (0.01 - 0.001) = 556 paid mints per month
```

---

## Marketplace Strategy

### Building an agent marketplace

A marketplace where users can discover, trade, and evaluate agents adds a network effects layer to the ecosystem.

**Core features:**
- Agent discovery (search by persona, experience, active status)
- Agent profiles (four identity questions rendered as cards)
- Trading (list, buy, make offers for paid agents)
- Reviews and ratings (off-chain, linked to agent token ID)
- Collections (group agents by creator or theme)

**Revenue from marketplace:**
- Listing fees (flat fee to list an agent for sale)
- Transaction fees (percentage of sale price)
- Featured listings (premium placement)
- Verified creator badges (annual fee)

### Marketplace pricing

- Listing fee: 0 (free to list, to encourage volume)
- Transaction fee: 2-5% of sale price
- Featured listing: 0.05-0.1 BNB per week
- Verified badge: 0.5-1 BNB per year

---

## Output Format

When asked for business guidance, respond with:

1. **Objective** (what business goal is being addressed)
2. **Model** (funnel, pricing, fee strategy, or policy)
3. **KPIs** to track (with data sources)
4. **Financial projections** (if applicable)
5. **Risks** and mitigations
6. **Next actions** (concrete steps to execute)

---

## Related Skills

- `bap578`
- `bap578-analytics`
- `bap578-agent-economy`
