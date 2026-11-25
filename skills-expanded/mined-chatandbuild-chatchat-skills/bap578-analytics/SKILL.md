---
id: bap578-analytics
name: BAP-578 Analytics & Indexing
description: Use this skill when defining metrics, building indexers, creating dashboards, or generating reports for BAP-578 Non-Fungible Agents from minting, vault funding, treasury, engagement, and event data.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Analytics & Indexing

Use this skill to define metrics, build indexers, create dashboards, and generate reports for BAP-578 Non-Fungible Agents. This covers metric definitions with data sources, event indexing pipelines, aggregation patterns, dashboard design, alerting strategies, and reporting templates.

---

## When to use this skill

- Defining KPIs and metrics for a BAP-578 deployment.
- Building an event indexer that processes on-chain events into a queryable database.
- Creating a real-time analytics dashboard.
- Generating periodic reports (daily, weekly, monthly).
- Setting up alerts for anomalous activity.
- Computing aggregate metrics like TVL, active agent ratio, or mint velocity.
- Comparing BAP-578 metrics across different time periods.

---

## The Four Identity Questions (Analytics View)

### 1) Who are you?

The analytics layer turns raw on-chain events and state reads into actionable insights. It answers questions about adoption, engagement, revenue, and ecosystem health. Analytics don't modify the contract — they observe and interpret.

### 2) What do you remember?

All on-chain events are immutable and permanently available. The analytics layer indexes and stores:

- Every `AgentCreated` event (minting activity)
- Every `AgentFunded` event (funding flows)
- Every `AgentWithdraw` event (withdrawal patterns)
- Every `AgentStatusChanged` event (lifecycle data)
- Every `MetadataUpdated` event (engagement signals)
- Every `Transfer` event (ownership changes)
- Point-in-time state snapshots (balances, active status)

### 3) What can you do?

- Compute real-time and historical metrics
- Build dashboards with charts and tables
- Generate automated reports
- Set up alerts for thresholds or anomalies
- Reconstruct any agent's complete history
- Compare metrics across time periods
- Export data for external analysis

### 4) How can I trust it?

Every metric maps directly to immutable on-chain data. Events cannot be modified after emission. State reads return the current authoritative values. The analytics pipeline can be independently verified by anyone with RPC access.

---

## Metric Definitions

### Primary Metrics

**Total Agents Minted**
- Source: `getTotalSupply()` or count of `AgentCreated` events
- Type: Cumulative counter
- Update: Real-time

**Unique Owners**
- Source: Distinct `owner` values from `AgentCreated` events or `tokensOfOwner`
- Type: Cumulative counter
- Update: Real-time

**Active Agent Ratio**
- Formula: `(Active agents / Total agents) × 100`
- Source: Scan all agents for `active == true`
- Type: Percentage
- Update: Daily

**Agent Funding TVL (Total Value Locked)**
- Formula: Sum of all agent balances
- Source: `getAgentState(tokenId).balance` for all tokens
- Type: BNB amount
- Update: Real-time or hourly

**Paid Mint Count**
- Formula: `Total supply - Free mints`
- Source: Count tokens where `isFreeMint(tokenId) == false`
- Type: Counter
- Update: Real-time

**Treasury Revenue**
- Formula: `Paid mints × Mint fee`
- Source: BNB transfers to treasury address in `AgentCreated` transactions
- Type: BNB amount
- Update: Real-time

**Monthly Active Agents (MAA)**
- Definition: Agents with at least one on-chain interaction in the last 30 days
- Source: Union of token IDs from all events in last 30 days
- Type: Counter
- Update: Daily

### Secondary Metrics

**Mint Velocity**
- Formula: `Mints per day/week/month`
- Source: `AgentCreated` events grouped by time period
- Type: Rate

**Average Agent Balance**
- Formula: `TVL / Active agent count`
- Source: Computed from TVL and active count
- Type: BNB amount

**Free-to-Paid Conversion Rate**
- Formula: `(Users with paid mints / Users with only free mints) × 100`
- Source: Per-user analysis of mint events
- Type: Percentage

**Metadata Update Frequency**
- Formula: `MetadataUpdated events per week`
- Source: Event count
- Type: Rate (engagement signal)

**Logic Contract Adoption**
- Formula: `(Agents with non-zero logicAddress / Total agents) × 100`
- Source: State scan for `logicAddress != address(0)`
- Type: Percentage

**Churn Rate**
- Formula: `(Agents deactivated in period / Active agents at period start) × 100`
- Source: `AgentStatusChanged` events where `active == false`
- Type: Percentage

**Average Agent Lifetime**
- Formula: `Average time between creation and last activity`
- Source: `AgentCreated` timestamp vs last event timestamp
- Type: Duration

---

## Event Sources

### Contract events used for analytics

```
AgentCreated(uint256 indexed tokenId, address indexed owner, address logicAddress, string metadataURI)
AgentFunded(uint256 indexed tokenId, address indexed funder, uint256 amount)
AgentWithdraw(uint256 indexed tokenId, address indexed owner, uint256 amount)
AgentStatusChanged(uint256 indexed tokenId, bool active)
MetadataUpdated(uint256 indexed tokenId, string newURI)
Transfer(address indexed from, address indexed to, uint256 indexed tokenId)
```

### Derived data from events

From `AgentCreated`:
- Mint count (total and per-user)
- New owner count
- Free vs paid classification (check `msg.value` in transaction)

From `AgentFunded`:
- Funding volume (per agent, per user, per period)
- Funding frequency
- Top funders

From `AgentWithdraw`:
- Withdrawal volume
- Net flow (funding minus withdrawals)

From `AgentStatusChanged`:
- Active/inactive transitions
- Churn events
- Reactivation events

From `MetadataUpdated`:
- Engagement frequency
- Agent evolution patterns

From `Transfer`:
- Secondary market activity
- Ownership concentration (Gini coefficient)

---

## Building an Event Indexer

### Architecture

```
BNB Chain (RPC)
      │
      │ poll events / websocket
      ▼
┌──────────────┐
│  Event Poller │  ← reads AgentCreated, AgentFunded, etc.
└──────┬───────┘
       │ parse & normalize
       ▼
┌──────────────┐
│  Processor   │  ← computes derived metrics
└──────┬───────┘
       │ store
       ▼
┌──────────────┐
│  Database    │  ← PostgreSQL, SQLite, or in-memory
└──────┬───────┘
       │ query
       ▼
┌──────────────┐
│  API / UI    │  ← REST API or dashboard
└──────────────┘
```

### Event poller implementation

```js
const { ethers } = require("ethers");

class BAP578Indexer {
  constructor(provider, contractAddress, abi) {
    this.contract = new ethers.Contract(contractAddress, abi, provider);
    this.lastBlock = 0;
    this.events = [];
  }

  async indexFromBlock(fromBlock) {
    const eventNames = [
      "AgentCreated",
      "AgentFunded",
      "AgentWithdraw",
      "AgentStatusChanged",
      "MetadataUpdated",
    ];

    for (const name of eventNames) {
      const events = await this.contract.queryFilter(
        this.contract.filters[name](),
        fromBlock,
        "latest"
      );

      for (const event of events) {
        const block = await event.getBlock();
        this.events.push({
          name,
          blockNumber: event.blockNumber,
          transactionHash: event.transactionHash,
          timestamp: new Date(block.timestamp * 1000),
          args: this.parseArgs(name, event.args),
        });
      }
    }

    this.events.sort((a, b) => a.blockNumber - b.blockNumber);
    this.lastBlock = await this.contract.runner.provider.getBlockNumber();
  }

  parseArgs(name, args) {
    switch (name) {
      case "AgentCreated":
        return {
          tokenId: args.tokenId.toString(),
          owner: args.owner,
          logicAddress: args.logicAddress,
          metadataURI: args.metadataURI,
        };
      case "AgentFunded":
        return {
          tokenId: args.tokenId.toString(),
          funder: args.funder,
          amount: ethers.formatEther(args.amount),
        };
      case "AgentWithdraw":
        return {
          tokenId: args.tokenId.toString(),
          owner: args.owner,
          amount: ethers.formatEther(args.amount),
        };
      case "AgentStatusChanged":
        return {
          tokenId: args.tokenId.toString(),
          active: args.active,
        };
      case "MetadataUpdated":
        return {
          tokenId: args.tokenId.toString(),
          newURI: args.newURI,
        };
      default:
        return args;
    }
  }

  computeMetrics() {
    const created = this.events.filter((e) => e.name === "AgentCreated");
    const funded = this.events.filter((e) => e.name === "AgentFunded");
    const withdrawn = this.events.filter((e) => e.name === "AgentWithdraw");
    const statusChanged = this.events.filter((e) => e.name === "AgentStatusChanged");
    const metaUpdated = this.events.filter((e) => e.name === "MetadataUpdated");

    const uniqueOwners = new Set(created.map((e) => e.args.owner)).size;

    const totalFunded = funded.reduce(
      (sum, e) => sum + parseFloat(e.args.amount), 0
    );
    const totalWithdrawn = withdrawn.reduce(
      (sum, e) => sum + parseFloat(e.args.amount), 0
    );

    const deactivations = statusChanged.filter((e) => !e.args.active).length;
    const reactivations = statusChanged.filter((e) => e.args.active).length;

    return {
      totalMinted: created.length,
      uniqueOwners,
      totalFunded: totalFunded.toFixed(4) + " BNB",
      totalWithdrawn: totalWithdrawn.toFixed(4) + " BNB",
      netFunding: (totalFunded - totalWithdrawn).toFixed(4) + " BNB",
      deactivations,
      reactivations,
      metadataUpdates: metaUpdated.length,
    };
  }

  mintsByPeriod(periodDays = 7) {
    const created = this.events.filter((e) => e.name === "AgentCreated");
    const periods = {};

    for (const event of created) {
      const periodStart = new Date(event.timestamp);
      periodStart.setDate(
        periodStart.getDate() - (periodStart.getDate() % periodDays)
      );
      const key = periodStart.toISOString().split("T")[0];
      periods[key] = (periods[key] || 0) + 1;
    }

    return periods;
  }
}
```

### Real-time event listener

```js
function startRealTimeMonitoring(contract) {
  contract.on("AgentCreated", (tokenId, owner, logicAddress, metadataURI, event) => {
    console.log(`[MINT] Agent #${tokenId} by ${owner} at block ${event.log.blockNumber}`);
    // Update metrics, send to dashboard, trigger alerts
  });

  contract.on("AgentFunded", (tokenId, funder, amount, event) => {
    console.log(`[FUND] Agent #${tokenId} +${ethers.formatEther(amount)} BNB`);
  });

  contract.on("AgentWithdraw", (tokenId, owner, amount, event) => {
    console.log(`[WITHDRAW] Agent #${tokenId} -${ethers.formatEther(amount)} BNB`);
  });

  contract.on("AgentStatusChanged", (tokenId, active) => {
    console.log(`[STATUS] Agent #${tokenId} → ${active ? "active" : "inactive"}`);
  });

  console.log("Real-time monitoring started...");
}
```

---

## Dashboard Design

### Recommended layout

```
┌─────────────────────────────────────────────┐
│  BAP-578 Analytics Dashboard                │
├──────────┬──────────┬──────────┬────────────┤
│ Total    │ Active   │ TVL      │ Treasury   │
│ Minted   │ Agents   │          │ Balance    │
│ 1,247    │ 892      │ 45.3 BNB │ 12.1 BNB   │
├──────────┴──────────┴──────────┴────────────┤
│  Minting Activity (line chart — last 30d)   │
│  ▁▂▃▅▇▆▄▃▂▅▇▆▅▄▃▂▁▂▃▅▇▆▅▄▃▂▁            │
├─────────────────────┬───────────────────────┤
│  Top Owners (table) │  Funding Flow (chart) │
│  0xABC: 15 agents   │  In:  +12.5 BNB       │
│  0xDEF: 12 agents   │  Out: -3.2 BNB        │
│  0x123: 8 agents    │  Net: +9.3 BNB        │
├─────────────────────┴───────────────────────┤
│  Recent Events (live feed)                   │
│  10:05 — Agent #1247 minted by 0xABC        │
│  10:03 — Agent #892 funded +0.5 BNB         │
│  09:58 — Agent #445 status → inactive        │
└─────────────────────────────────────────────┘
```

### Dashboard components

1. **Summary cards** — total minted, active agents, TVL, treasury
2. **Mint chart** — line chart of daily/weekly mints
3. **Funding flow** — bar chart of inflows vs outflows
4. **Top owners** — table sorted by agent count
5. **Recent events** — live feed of contract events
6. **Conversion funnel** — free mint → paid mint flow
7. **Agent status** — pie chart of active vs inactive
8. **Logic adoption** — percentage with bound logic contracts

---

## Alerting

### Recommended alerts

**Critical:**
- Emergency withdraw executed
- Contract paused/unpaused
- Ownership transferred
- Upgrade executed

**High:**
- Large withdrawal (> threshold BNB)
- Rapid minting (> N mints in M minutes)
- Treasury balance below minimum

**Medium:**
- New record for daily mints
- TVL milestone reached
- Active agent ratio drops below threshold

### Alert implementation

```js
function checkAlerts(event) {
  if (event.name === "AgentWithdraw") {
    const amount = parseFloat(event.args.amount);
    if (amount > 10) {
      sendAlert("HIGH", `Large withdrawal: ${amount} BNB from Agent #${event.args.tokenId}`);
    }
  }

  if (event.name === "AgentCreated") {
    const recentMints = getMintsInLastMinutes(5);
    if (recentMints > 50) {
      sendAlert("HIGH", `Rapid minting detected: ${recentMints} mints in 5 minutes`);
    }
  }
}
```

---

## Reporting Templates

### Daily summary

```
BAP-578 Daily Report — 2026-03-06
──────────────────────────────────
New mints:        +14 (total: 1,247)
New owners:       +6  (total: 423)
Funding inflows:  +2.3 BNB
Withdrawals:      -0.5 BNB
Net funding:      +1.8 BNB
TVL:              45.3 BNB
Active agents:    892 (71.5%)
Metadata updates: 23
Notable: Agent #1200 funded with 5 BNB (largest single deposit this week)
```

### Weekly trends

```
BAP-578 Weekly Trends — W10 2026
─────────────────────────────────
Metric              This Week    Last Week    Change
Mints               98           72           +36.1%
New owners           34           28           +21.4%
Funding volume      15.2 BNB     11.8 BNB     +28.8%
Active ratio        71.5%        69.2%        +2.3pp
Paid mint conv.     18.2%        15.7%        +2.5pp
```

---

## Subgraph Integration (The Graph)

For production-grade indexing, use The Graph protocol to create a subgraph:

### Subgraph schema

```graphql
type Agent @entity {
  id: ID!
  tokenId: BigInt!
  owner: Bytes!
  balance: BigDecimal!
  active: Boolean!
  logicAddress: Bytes!
  createdAt: BigInt!
  persona: String
  experience: String
  vaultURI: String
  vaultHash: Bytes!
  isFreeMint: Boolean!
  fundingEvents: [FundingEvent!]! @derivedFrom(field: "agent")
  withdrawEvents: [WithdrawEvent!]! @derivedFrom(field: "agent")
}

type FundingEvent @entity {
  id: ID!
  agent: Agent!
  funder: Bytes!
  amount: BigDecimal!
  blockNumber: BigInt!
  timestamp: BigInt!
  transactionHash: Bytes!
}

type WithdrawEvent @entity {
  id: ID!
  agent: Agent!
  owner: Bytes!
  amount: BigDecimal!
  blockNumber: BigInt!
  timestamp: BigInt!
  transactionHash: Bytes!
}

type DailyStat @entity {
  id: ID!
  date: String!
  mintCount: Int!
  fundingVolume: BigDecimal!
  withdrawVolume: BigDecimal!
  activeAgents: Int!
  uniqueOwners: Int!
}
```

### Querying the subgraph

```graphql
# Top 10 funded agents
{
  agents(orderBy: balance, orderDirection: desc, first: 10) {
    tokenId
    owner
    balance
    active
    experience
  }
}

# Daily minting stats for last 30 days
{
  dailyStats(orderBy: date, orderDirection: desc, first: 30) {
    date
    mintCount
    fundingVolume
    activeAgents
  }
}

# Agent history
{
  agent(id: "17") {
    tokenId
    owner
    balance
    fundingEvents(orderBy: timestamp, orderDirection: desc) {
      amount
      funder
      timestamp
    }
  }
}
```

---

## API Endpoints for Dashboards

If building a REST API for the analytics dashboard:

```
GET /api/metrics/summary          → total minted, active, TVL, treasury
GET /api/metrics/mints?period=7d  → mint count by day for last 7 days
GET /api/metrics/funding?period=30d → funding volume by day
GET /api/agents/:tokenId          → single agent full profile
GET /api/agents/:tokenId/history  → event history for agent
GET /api/owners/:address          → portfolio for owner
GET /api/leaderboard/funded       → top agents by balance
GET /api/leaderboard/owners       → top owners by agent count
GET /api/alerts/recent            → recent triggered alerts
```

---

## Output Format

When asked for analytics help, respond with:

1. **Metric definitions** (what to measure and how)
2. **Event sources** (which events feed each metric)
3. **Implementation code** (indexer, aggregation, API)
4. **Dashboard layout** (what to display and where)
5. **Alert configuration** (thresholds and channels)

---

## Related Skills

- `bap578`
- `bap578-scanner`
- `bap578-business`
