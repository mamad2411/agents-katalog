---
id: bap578-agent-economy
name: BAP-578 Agent Economy
description: Use this skill when designing, modeling, or operating BAP-578 agent economies where NFAs transact, collaborate, compete, provide services, handle funding, build reputation, or align incentives.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Agent Economy

Use this skill to design, model, and operate economic systems where BAP-578 agents transact, collaborate, compete, and provide services. This covers agent funding flows, inter-agent payment patterns, reputation mechanisms, service marketplaces, and economic incentive alignment.

---

## When to use this skill

- Designing how agents fund each other or pay for services.
- Building reputation systems that track agent quality.
- Creating a service marketplace where agents offer and consume capabilities.
- Modeling economic incentives to encourage healthy ecosystem behavior.
- Designing staking or collateral mechanisms for agent accountability.
- Planning token economics that complement the NFA system.
- Analyzing agent economy health metrics.

---

## The Four Identity Questions (Economy View)

### 1) Who are you?

The agent economy is the layer where agents become economic actors. Each agent has an on-chain balance (BNB held in the NFA contract), a persona (defining what services it offers), and a status (active/inactive). In an agent economy, identity is directly tied to economic capability: agents with funding can pay for services, agents with expertise can earn revenue, and agents with reputation attract more business.

### 2) What do you remember?

Economic memory is captured through on-chain events and state:

- **Funding history:** `AgentFunded` and `AgentWithdraw` events track every BNB flow
- **Transaction patterns:** which agents fund each other, how often, how much
- **Reputation scores:** derived from successful service completions (stored in vault or logic contract)
- **Service records:** metadata updates and vault content track what services were delivered
- **Economic relationships:** persistent patterns of agent-to-agent interaction

### 3) What can you do?

The agent economy enables:

- **Service provision:** agents offer capabilities (analysis, generation, monitoring)
- **Service consumption:** agents pay other agents for capabilities they lack
- **Reputation building:** successful service delivery increases reputation
- **Fund management:** agents accumulate and spend BNB for services
- **Marketplace participation:** agents list services, bid on tasks, and fulfill orders
- **Collaborative networks:** agents form alliances and share resources

### 4) How can I trust it?

Economic trust in the agent economy comes from:

- **On-chain balances:** agent funding is verifiable and transparent
- **Event audit trail:** every payment and interaction is recorded
- **Reputation scores:** derived from verifiable service history
- **Logic contract enforcement:** automated service agreements via smart contracts
- **Vault integrity:** service records anchored by hash verification

---

## Agent Funding Model

### How agents hold and use funds

Each BAP-578 agent has an on-chain BNB balance managed by the NFA contract:

```
Agent #17
├── balance: 2.5 BNB    ← held in NFA contract
├── active: true
└── owner: 0xABC         ← controls withdrawals
```

Funding flows:
- **Inbound:** Anyone can call `fundAgent(tokenId)` with BNB
- **Outbound:** Only the token owner can call `withdrawFromAgent(tokenId, amount)`
- **Agent-to-agent:** Owner withdraws from Agent A, funds Agent B

### Direct agent-to-agent payment pattern

Since agents cannot directly transfer BNB to each other (only owners can withdraw), agent-to-agent payments follow this pattern:

```
1. Agent A's owner withdraws from Agent A
2. Agent A's owner funds Agent B
3. Both transactions are atomic (can be batched in one tx via helper contract)
```

### Payment helper contract

A helper contract can batch withdraw-and-fund into a single transaction:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface INFA {
    function withdrawFromAgent(uint256 tokenId, uint256 amount) external;
    function fundAgent(uint256 tokenId) external payable;
    function getAgentState(uint256 tokenId) external view returns (
        uint256 balance, bool active, address logicAddress,
        uint256 createdAt, address owner
    );
}

contract AgentPaymentRouter {
    INFA public immutable nfa;

    event AgentPayment(
        uint256 indexed fromAgent,
        uint256 indexed toAgent,
        uint256 amount,
        string reason
    );

    constructor(address _nfa) {
        nfa = INFA(_nfa);
    }

    function payAgent(
        uint256 fromTokenId,
        uint256 toTokenId,
        uint256 amount,
        string calldata reason
    ) external {
        // Verify caller owns the source agent
        (, , , , address owner) = nfa.getAgentState(fromTokenId);
        require(msg.sender == owner, "Not source agent owner");

        // Withdraw from source agent
        nfa.withdrawFromAgent(fromTokenId, amount);

        // Fund destination agent
        nfa.fundAgent{value: amount}(toTokenId);

        emit AgentPayment(fromTokenId, toTokenId, amount, reason);
    }

    receive() external payable {}
}
```

---

## Service Marketplace

### Concept

A service marketplace where agents advertise capabilities and other agents (or users) can purchase those services. Services are defined in agent metadata (persona + experience) and priced via the marketplace contract.

### Service listing structure

```json
{
  "serviceId": "analysis-001",
  "agentTokenId": 17,
  "name": "DeFi Yield Analysis",
  "description": "Comprehensive yield comparison across top 20 DeFi protocols",
  "priceBnb": "0.005",
  "deliveryTime": "1 hour",
  "category": "finance",
  "rating": 4.8,
  "completedJobs": 142
}
```

### Marketplace contract pattern

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AgentMarketplace {
    struct ServiceListing {
        uint256 agentTokenId;
        uint256 price;
        bool active;
        string serviceURI;
    }

    struct Order {
        uint256 listingId;
        uint256 buyerAgentId;
        uint256 amount;
        OrderStatus status;
        uint256 createdAt;
    }

    enum OrderStatus { Pending, Delivered, Completed, Disputed }

    mapping(uint256 => ServiceListing) public listings;
    mapping(uint256 => Order) public orders;
    uint256 public nextListingId;
    uint256 public nextOrderId;

    uint256 public constant PLATFORM_FEE_BPS = 250; // 2.5%

    event ServiceListed(uint256 indexed listingId, uint256 indexed agentId, uint256 price);
    event OrderCreated(uint256 indexed orderId, uint256 indexed listingId, uint256 buyerAgentId);
    event OrderCompleted(uint256 indexed orderId);

    function listService(
        uint256 agentTokenId,
        uint256 price,
        string calldata serviceURI
    ) external returns (uint256) {
        uint256 id = nextListingId++;
        listings[id] = ServiceListing({
            agentTokenId: agentTokenId,
            price: price,
            active: true,
            serviceURI: serviceURI
        });
        emit ServiceListed(id, agentTokenId, price);
        return id;
    }

    function createOrder(uint256 listingId, uint256 buyerAgentId) external payable returns (uint256) {
        ServiceListing memory listing = listings[listingId];
        require(listing.active, "Listing not active");
        require(msg.value >= listing.price, "Insufficient payment");

        uint256 id = nextOrderId++;
        orders[id] = Order({
            listingId: listingId,
            buyerAgentId: buyerAgentId,
            amount: msg.value,
            status: OrderStatus.Pending,
            createdAt: block.timestamp
        });
        emit OrderCreated(id, listingId, buyerAgentId);
        return id;
    }

    function completeOrder(uint256 orderId) external {
        Order storage order = orders[orderId];
        require(order.status == OrderStatus.Delivered, "Not delivered");

        ServiceListing memory listing = listings[order.listingId];
        uint256 fee = (order.amount * PLATFORM_FEE_BPS) / 10000;
        uint256 payment = order.amount - fee;

        // Payment would go to the service agent's funding
        // Implementation depends on NFA integration
        order.status = OrderStatus.Completed;
        emit OrderCompleted(orderId);
    }
}
```

---

## Reputation System

### On-chain reputation model

Reputation is built from verifiable service history:

```
Reputation Score = f(completed_orders, ratings, disputes, agent_age, balance)
```

### Reputation components

**Service completion rate:**
```
completion_rate = completed_orders / (completed_orders + cancelled_orders + disputed_orders)
```

**Average rating:**
- After each completed order, the buyer rates the service (1-5 stars)
- Stored on-chain or in vault with hash verification

**Economic stake:**
- Higher agent balance signals commitment (skin in the game)
- Agents with more BNB locked are less likely to misbehave

**Agent age:**
- Older agents (higher `createdAt` delta) have longer track records
- New agents start with neutral reputation

**Dispute rate:**
```
dispute_rate = disputed_orders / total_orders
```

### Reputation tiers

```
Tier 1: New Agent      — < 10 completed orders
Tier 2: Established    — 10-50 completed orders, > 4.0 rating
Tier 3: Trusted        — 50-200 completed orders, > 4.5 rating
Tier 4: Expert         — 200+ completed orders, > 4.7 rating
Tier 5: Elite          — 500+ completed orders, > 4.8 rating, < 1% disputes
```

### Storing reputation

**Option 1: Logic contract state**

A reputation logic contract maintains scores per agent:

```solidity
contract ReputationLogic {
    struct Reputation {
        uint256 completedOrders;
        uint256 totalRating;
        uint256 disputes;
        uint256 lastUpdated;
    }

    mapping(uint256 => Reputation) public reputations;

    function getScore(uint256 tokenId) external view returns (uint256) {
        Reputation memory rep = reputations[tokenId];
        if (rep.completedOrders == 0) return 0;
        uint256 avgRating = (rep.totalRating * 100) / rep.completedOrders;
        uint256 completionBonus = rep.completedOrders > 100 ? 20 : rep.completedOrders / 5;
        uint256 disputePenalty = (rep.disputes * 100) / rep.completedOrders;
        return avgRating + completionBonus - disputePenalty;
    }
}
```

**Option 2: Vault-based reputation**

Store detailed reputation data in the agent's vault:

```json
{
  "reputation": {
    "score": 487,
    "tier": "Expert",
    "completedOrders": 234,
    "averageRating": 4.72,
    "disputeRate": 0.008,
    "specializations": {
      "defi-analysis": { "orders": 145, "rating": 4.8 },
      "market-research": { "orders": 89, "rating": 4.6 }
    },
    "lastUpdated": "2026-03-06T10:00:00Z"
  }
}
```

Verify integrity via `vaultHash` comparison.

---

## Economic Incentive Design

### Incentive alignment goals

1. **Encourage quality:** high-quality service providers earn more
2. **Discourage fraud:** bad actors lose reputation and funding
3. **Promote participation:** new agents can bootstrap via free mints
4. **Sustain the ecosystem:** platform fees fund operations

### Incentive mechanisms

**Staking for service providers:**
- Agents must maintain a minimum balance to list services
- Balance acts as collateral — can be slashed for disputes
- Higher stakes unlock higher-value service tiers

**Escrow for payments:**
- Buyer payment held in escrow contract until service delivery confirmed
- Automatic release after confirmation or timeout
- Dispute resolution via arbitration (human or automated)

**Referral rewards:**
- Agents earn a bonus for referring new agents or buyers
- Tracked via logic contract or event logs

**Volume discounts:**
- Frequent buyers get reduced prices from marketplace agents
- Loyalty tracked on-chain or in vault

### Economic health metrics

| Metric | What it measures | Healthy range |
|--------|-----------------|---------------|
| Service completion rate | Quality of delivery | > 95% |
| Average order value | Economic activity | Growing |
| Agent funding velocity | Capital flow | Stable/Growing |
| Dispute rate | Trust issues | < 2% |
| Repeat buyer rate | Satisfaction | > 40% |
| New agent creation rate | Growth | Stable/Growing |
| Active service listings | Supply | > 50% of agents |

---

## Agent Collaboration Patterns

### Hub-and-spoke model

One coordinator agent distributes tasks to specialist agents:

```
        ┌── Agent A (research)
        │
Coordinator ── Agent B (analysis)
        │
        └── Agent C (reporting)
```

The coordinator receives funding, pays specialists, and delivers combined output to the buyer.

### Peer-to-peer model

Agents directly transact with each other without a coordinator:

```
Agent A ←→ Agent B ←→ Agent C
```

Each agent discovers and pays peers independently. Best for simple bilateral services.

### Pool model

Multiple agents contribute to a shared pool and share rewards:

```
Agent A ─┐
Agent B ──┼── Shared Pool ── Rewards distributed proportionally
Agent C ─┘
```

Implemented via a pool logic contract that tracks contributions and distributions.

---

## Economy Bootstrap Strategy

### Phase 1: Seeding (first 100 agents)

- Free mints create initial agent population
- Platform provides sample services and templates
- Manual curation of service listings
- Incentivize first transactions with bonus funding

### Phase 2: Growth (100-1000 agents)

- Organic service discovery via marketplace
- Reputation system begins differentiating quality
- Agent-to-agent payments become regular
- Community-driven service categories emerge

### Phase 3: Maturity (1000+ agents)

- Self-sustaining marketplace with diverse services
- Reputation tiers drive premium pricing
- Agent collaboration networks form organically
- Platform fees cover operations and development

---

## Risk Mitigation in Agent Economies

### Sybil resistance

Prevent one actor from creating many agents to game reputation:

- Free mint limit per address constrains initial sybil cost
- Paid mints add economic cost to creating fake identities
- Reputation requires actual completed orders (can't be faked cheaply)
- Logic contract binding adds development cost per agent type

### Marketplace fraud prevention

- **Escrow model:** Funds held until buyer confirms delivery
- **Dispute resolution:** Third-party arbitrator or DAO vote
- **Reputation slashing:** Bad actors lose reputation permanently
- **Minimum stake:** Service providers must lock BNB as collateral
- **Time-locks:** Large withdrawals have a cooling period

### Economic attack vectors and mitigations

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Wash trading | Agent pays itself to inflate metrics | Detect same-owner transactions |
| Reputation farming | Complete many low-value orders | Weight reputation by order value |
| Price manipulation | Undercut competitors to drive them out | Minimum listing price floors |
| Front-running | Observe pending orders and intercept | Commit-reveal order pattern |
| Balance drain | Exploit to empty agent funds | Reentrancy guards, CEI pattern |

---

## Tokenomics Integration

While BAP-578 uses native BNB, it can be extended with a governance or utility token:

### Potential token uses

- **Governance:** Token holders vote on marketplace rules, fee levels, and feature priorities
- **Staking rewards:** Stake tokens to earn a share of marketplace fees
- **Premium features:** Token holders unlock advanced agent capabilities
- **Fee discounts:** Pay marketplace fees in tokens at a discount
- **Agent badges:** Verified token holders get special reputation badges

### Revenue distribution model

```
Marketplace fee (2.5% per order)
    │
    ├── 40% → Treasury (operations, development)
    ├── 30% → Token stakers (reward distribution)
    ├── 20% → Service agent (bonus on top of payment)
    └── 10% → Referrer (if applicable)
```

---

## Output Format

When asked for agent economy help, respond with:

1. **Economic model** (payment flows, incentives, pricing)
2. **Smart contract code** (payment router, marketplace, reputation)
3. **Incentive analysis** (who benefits, potential abuse, mitigations)
4. **Metrics** (what to measure and healthy ranges)
5. **Bootstrap plan** (how to get from zero to self-sustaining)

---

## Related Skills

- `bap578`
- `bap578-business`
- `bap578-logic-contracts`
