---
id: bap578-scanner
name: BAP-578 On-Chain Scanner
description: Use this skill when reading, verifying, scanning, querying, indexing, or monitoring BAP-578 agent data directly from BNB Chain, including metadata, event history, vault integrity, and bulk RPC workflows.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 On-Chain Scanner

Use this skill to read, verify, and index BAP-578 agent data directly from the blockchain. This covers single-agent lookups, bulk scanning, event indexing, vault integrity checks, and building automated monitoring pipelines.

---

## When to use this skill

- Looking up a specific agent's identity, state, or metadata by token ID.
- Listing all agents owned by a particular address.
- Verifying that off-chain vault content matches the on-chain hash.
- Building an event indexer or monitoring pipeline for BAP-578.
- Auditing agent histories through event reconstruction.
- Answering questions like "how many agents exist?" or "what's the TVL?"

---

## The Four Identity Questions (Scanner View)

### 1) Who are you?

The scanner reveals the full on-chain identity of any agent. By calling `getAgentState` and `getAgentMetadata`, you retrieve the complete profile:

- Token ID (the unique agent identifier)
- Owner address (who controls this agent)
- Persona (JSON-encoded character definition)
- Experience (plain-text domain expertise)
- Logic address (optional behavior contract)
- Active status (operational or dormant)
- Creation timestamp (when the agent was minted)
- Balance (BNB held by the agent)

This is the authoritative identity. Any off-chain representation should match these fields.

### 2) What do you remember?

The scanner can reconstruct the complete history of an agent by querying on-chain events:

- **AgentCreated** — when and how the agent was born (minter, initial metadata)
- **AgentFunded** — every BNB deposit with amount and sender
- **AgentWithdraw** — every withdrawal with amount
- **AgentStatusChanged** — every active/inactive toggle
- **MetadataUpdated** — every identity change (new persona, vault, etc.)

Additionally, the scanner can verify extended memory by fetching `vaultURI` content and comparing its keccak256 hash against the on-chain `vaultHash`. This proves whether the off-chain data is authentic.

### 3) What can you do?

The scanner performs read-only operations. It does not modify state. Capabilities include:

- Single agent lookup (state + metadata)
- Owner portfolio listing (all tokens owned by an address)
- Total supply query
- Free mint status check
- Event history reconstruction
- Vault content verification
- Bulk scanning across token ID ranges
- Aggregate metrics computation (TVL, active count, mint velocity)

### 4) How can I trust it?

Scanner results come directly from the blockchain via RPC calls. Trust is established by:

- Reading from the canonical contract address (verified on block explorer)
- Using authenticated RPC endpoints
- Cross-referencing event data with state reads
- Verifying vault hashes independently
- All data is publicly verifiable by anyone with an RPC connection

---

## Contract Interface for Scanning

### View Functions Used

```
getAgentState(tokenId)     → (balance, active, logicAddress, createdAt, owner)
getAgentMetadata(tokenId)  → (persona, experience, voiceHash, animationURI, vaultURI, vaultHash)
tokensOfOwner(address)     → uint256[]
getTotalSupply()           → uint256
getFreeMints(user)         → uint256
isFreeMint(tokenId)        → bool
tokenURI(tokenId)          → string
ownerOf(tokenId)           → address
```

### Events Indexed

```
AgentCreated(tokenId, owner, logicAddress, metadataURI)
AgentFunded(tokenId, funder, amount)
AgentWithdraw(tokenId, owner, amount)
AgentStatusChanged(tokenId, active)
MetadataUpdated(tokenId, newURI)
Transfer(from, to, tokenId)  // ERC-721 standard
```

---

## Scanning with ethers.js

### Setup

```js
const { ethers } = require("ethers");

const provider = new ethers.JsonRpcProvider(process.env.BSC_RPC_URL);
const BAP578_ADDRESS = process.env.BAP578_ADDRESS;
const BAP578_ABI = require("./abi/BAP578.json");

const contract = new ethers.Contract(BAP578_ADDRESS, BAP578_ABI, provider);
```

### Single agent lookup

```js
async function scanAgent(tokenId) {
  const state = await contract.getAgentState(tokenId);
  const metadata = await contract.getAgentMetadata(tokenId);
  const uri = await contract.tokenURI(tokenId);
  const freeMint = await contract.isFreeMint(tokenId);

  return {
    tokenId,
    owner: state.owner,
    balance: ethers.formatEther(state.balance),
    active: state.active,
    logicAddress: state.logicAddress,
    createdAt: new Date(Number(state.createdAt) * 1000).toISOString(),
    persona: metadata.persona,
    experience: metadata.experience,
    voiceHash: metadata.voiceHash,
    animationURI: metadata.animationURI,
    vaultURI: metadata.vaultURI,
    vaultHash: metadata.vaultHash,
    tokenURI: uri,
    isFreeMint: freeMint,
  };
}
```

### Owner portfolio scan

```js
async function scanOwnerPortfolio(ownerAddress) {
  const tokenIds = await contract.tokensOfOwner(ownerAddress);
  const agents = [];
  for (const id of tokenIds) {
    agents.push(await scanAgent(id));
  }
  return { owner: ownerAddress, agentCount: agents.length, agents };
}
```

### Bulk scan (all agents)

```js
async function scanAllAgents() {
  const totalSupply = await contract.getTotalSupply();
  const agents = [];
  for (let i = 1; i <= Number(totalSupply); i++) {
    try {
      agents.push(await scanAgent(i));
    } catch (e) {
      console.warn(`Token ${i} not found or burned`);
    }
  }
  return agents;
}
```

### Aggregate metrics

```js
async function computeMetrics() {
  const agents = await scanAllAgents();
  const totalSupply = agents.length;
  const activeCount = agents.filter((a) => a.active).length;
  const uniqueOwners = new Set(agents.map((a) => a.owner)).size;
  const totalBalance = agents.reduce(
    (sum, a) => sum + parseFloat(a.balance),
    0
  );
  const freeMintCount = agents.filter((a) => a.isFreeMint).length;
  const paidMintCount = totalSupply - freeMintCount;
  const withLogic = agents.filter(
    (a) => a.logicAddress !== ethers.ZeroAddress
  ).length;

  return {
    totalSupply,
    activeCount,
    inactiveCount: totalSupply - activeCount,
    uniqueOwners,
    tvl: totalBalance.toFixed(4) + " BNB",
    freeMintCount,
    paidMintCount,
    agentsWithLogic: withLogic,
  };
}
```

---

## Scanning with viem

### Setup

```ts
import { createPublicClient, http } from "viem";
import { bsc } from "viem/chains";

const client = createPublicClient({
  chain: bsc,
  transport: http(process.env.BSC_RPC_URL),
});
```

### Read agent state

```ts
const state = await client.readContract({
  address: BAP578_ADDRESS,
  abi: BAP578_ABI,
  functionName: "getAgentState",
  args: [tokenId],
});
```

### Read events

```ts
const events = await client.getContractEvents({
  address: BAP578_ADDRESS,
  abi: BAP578_ABI,
  eventName: "AgentCreated",
  fromBlock: deploymentBlock,
  toBlock: "latest",
});
```

---

## Vault Integrity Verification

The vault is the off-chain memory layer. Verification ensures it has not been tampered with.

### Verification algorithm

```js
const { keccak256, toUtf8Bytes } = require("ethers");

async function verifyVault(vaultURI, onChainHash) {
  if (onChainHash === ethers.ZeroHash) {
    return { verified: false, reason: "No vault hash registered (zero hash)" };
  }

  try {
    const response = await fetch(vaultURI);
    if (!response.ok) {
      return { verified: false, reason: `Fetch failed: ${response.status}` };
    }

    const content = await response.text();
    const computedHash = keccak256(toUtf8Bytes(content));

    if (computedHash === onChainHash) {
      return { verified: true, contentLength: content.length };
    } else {
      return {
        verified: false,
        reason: "Hash mismatch — content may have been modified",
        expected: onChainHash,
        computed: computedHash,
      };
    }
  } catch (error) {
    return { verified: false, reason: `Error: ${error.message}` };
  }
}
```

### Verification states

- **Verified** — hash matches; off-chain data is authentic.
- **Hash mismatch** — content has been modified since registration.
- **Zero hash** — no vault data was registered; skip verification.
- **Fetch error** — URI unreachable; vault may be offline.

---

## Event Indexing

### Building a simple indexer

```js
async function indexAllEvents(fromBlock = 0n) {
  const eventNames = [
    "AgentCreated",
    "AgentFunded",
    "AgentWithdraw",
    "AgentStatusChanged",
    "MetadataUpdated",
  ];

  const allEvents = [];

  for (const eventName of eventNames) {
    const events = await contract.queryFilter(
      contract.filters[eventName](),
      fromBlock,
      "latest"
    );

    for (const event of events) {
      allEvents.push({
        eventName,
        blockNumber: event.blockNumber,
        transactionHash: event.transactionHash,
        args: event.args,
        timestamp: null, // fetch block timestamp if needed
      });
    }
  }

  // Sort by block number
  allEvents.sort((a, b) => a.blockNumber - b.blockNumber);
  return allEvents;
}
```

### Reconstructing agent history

```js
async function getAgentHistory(tokenId) {
  const allEvents = await indexAllEvents();
  return allEvents.filter((e) => {
    const args = e.args;
    return args.tokenId && args.tokenId.toString() === tokenId.toString();
  });
}
```

### Real-time monitoring

```js
function watchAgentEvents() {
  contract.on("AgentCreated", (tokenId, owner, logicAddress, metadataURI) => {
    console.log(`New agent #${tokenId} minted by ${owner}`);
  });

  contract.on("AgentFunded", (tokenId, funder, amount) => {
    console.log(
      `Agent #${tokenId} funded ${ethers.formatEther(amount)} BNB by ${funder}`
    );
  });

  contract.on("AgentWithdraw", (tokenId, owner, amount) => {
    console.log(
      `Agent #${tokenId} withdrew ${ethers.formatEther(amount)} BNB`
    );
  });

  contract.on("AgentStatusChanged", (tokenId, active) => {
    console.log(`Agent #${tokenId} status → ${active ? "active" : "inactive"}`);
  });

  contract.on("MetadataUpdated", (tokenId, newURI) => {
    console.log(`Agent #${tokenId} metadata updated → ${newURI}`);
  });
}
```

---

## Common Scan Patterns

### Check if a token exists

```js
try {
  await contract.ownerOf(tokenId);
  // Token exists
} catch {
  // Token does not exist or was burned
}
```

### Find agents with logic contracts

```js
const agents = await scanAllAgents();
const withLogic = agents.filter(
  (a) => a.logicAddress !== ethers.ZeroAddress
);
```

### Find inactive agents with balance

```js
const atRisk = agents.filter(
  (a) => !a.active && parseFloat(a.balance) > 0
);
```

### Find recently created agents

```js
const recentEvents = await contract.queryFilter(
  contract.filters.AgentCreated(),
  -1000 // last 1000 blocks
);
```

---

## Output Format

When asked for scanning help, respond with:

1. **What to scan** (single agent, portfolio, bulk, events)
2. **Complete code** (setup + query + processing)
3. **Expected output shape** (JSON structure)
4. **Verification steps** (how to cross-check results)
5. **Performance notes** (rate limits, batching for bulk scans)

---

## Data Export Formats

### JSON export (single agent)

```json
{
  "tokenId": 17,
  "owner": "0xABC...",
  "balance": "1.5",
  "balanceUnit": "BNB",
  "active": true,
  "logicAddress": "0xDEF...",
  "createdAt": "2026-03-01T10:00:00Z",
  "persona": {"name": "Atlas", "traits": ["analytical"]},
  "experience": "Financial analyst specializing in DeFi",
  "voiceHash": "",
  "animationURI": "ipfs://QmAnim...",
  "vaultURI": "ipfs://QmVault...",
  "vaultHash": "0xabc123...",
  "vaultVerified": true,
  "isFreeMint": false,
  "tokenURI": "ipfs://QmMeta...",
  "history": [
    {"event": "AgentCreated", "block": 12345, "tx": "0x...", "timestamp": "2026-03-01T10:00:00Z"},
    {"event": "AgentFunded", "block": 12400, "tx": "0x...", "amount": "1.0 BNB"},
    {"event": "MetadataUpdated", "block": 12500, "tx": "0x...", "newURI": "ipfs://QmNew..."}
  ]
}
```

### CSV export (bulk scan)

```
tokenId,owner,balance,active,logicAddress,createdAt,experience,isFreeMint
1,0xABC...,0.5,true,0x0000...,2026-03-01,DeFi analyst,true
2,0xDEF...,1.2,true,0xLOGIC...,2026-03-02,Research bot,false
3,0x123...,0.0,false,0x0000...,2026-03-03,Support agent,true
```

### Generating CSV from scan results

```js
function toCSV(agents) {
  const header = "tokenId,owner,balance,active,logicAddress,createdAt,experience,isFreeMint";
  const rows = agents.map(a =>
    `${a.tokenId},${a.owner},${a.balance},${a.active},${a.logicAddress},${a.createdAt},${a.experience.replace(/,/g, ";")},${a.isFreeMint}`
  );
  return [header, ...rows].join("\n");
}
```

---

## Advanced Scan Patterns

### Ownership concentration analysis

Detect whether a small number of addresses control most agents:

```js
function analyzeConcentration(agents) {
  const ownerCounts = {};
  for (const a of agents) {
    ownerCounts[a.owner] = (ownerCounts[a.owner] || 0) + 1;
  }
  
  const sorted = Object.entries(ownerCounts)
    .sort(([,a], [,b]) => b - a);
  
  const totalAgents = agents.length;
  const top10 = sorted.slice(0, 10);
  const top10Count = top10.reduce((sum, [, c]) => sum + c, 0);
  
  return {
    totalOwners: sorted.length,
    top10Owners: top10.map(([addr, count]) => ({
      address: addr,
      count,
      percentage: ((count / totalAgents) * 100).toFixed(1) + "%"
    })),
    top10Concentration: ((top10Count / totalAgents) * 100).toFixed(1) + "%"
  };
}
```

### Agent health scoring

Assign a health score to each agent based on multiple factors:

```js
function scoreAgentHealth(agent) {
  let score = 0;
  
  // Active status (30 points)
  if (agent.active) score += 30;
  
  // Has balance (20 points, scaled)
  const balance = parseFloat(agent.balance);
  if (balance > 0) score += Math.min(20, balance * 10);
  
  // Has persona (15 points)
  try {
    const persona = JSON.parse(agent.persona);
    if (persona.name) score += 10;
    if (persona.traits && persona.traits.length > 0) score += 5;
  } catch {}
  
  // Has experience (10 points)
  if (agent.experience && agent.experience.length > 10) score += 10;
  
  // Has logic contract (15 points)
  if (agent.logicAddress !== ethers.ZeroAddress) score += 15;
  
  // Has vault (10 points)
  if (agent.vaultURI && agent.vaultURI.length > 0) score += 5;
  if (agent.vaultHash !== ethers.ZeroHash) score += 5;
  
  return { tokenId: agent.tokenId, score, maxScore: 100 };
}
```

### Time-series analysis

Track how metrics change over time by bucketing events:

```js
function mintTimeSeries(events, interval = "day") {
  const buckets = {};
  const created = events.filter(e => e.name === "AgentCreated");
  
  for (const event of created) {
    const date = new Date(event.timestamp);
    let key;
    if (interval === "day") key = date.toISOString().split("T")[0];
    else if (interval === "week") {
      const weekStart = new Date(date);
      weekStart.setDate(date.getDate() - date.getDay());
      key = weekStart.toISOString().split("T")[0];
    } else if (interval === "month") {
      key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;
    }
    buckets[key] = (buckets[key] || 0) + 1;
  }
  
  return Object.entries(buckets)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([period, count]) => ({ period, count }));
}
```

### Funding flow analysis

Track net funding per agent over time:

```js
function fundingFlow(events) {
  const flows = {};
  
  for (const event of events) {
    if (event.name === "AgentFunded") {
      const id = event.args.tokenId;
      flows[id] = flows[id] || { inflow: 0, outflow: 0 };
      flows[id].inflow += parseFloat(event.args.amount);
    } else if (event.name === "AgentWithdraw") {
      const id = event.args.tokenId;
      flows[id] = flows[id] || { inflow: 0, outflow: 0 };
      flows[id].outflow += parseFloat(event.args.amount);
    }
  }
  
  return Object.entries(flows).map(([tokenId, flow]) => ({
    tokenId,
    inflow: flow.inflow.toFixed(4) + " BNB",
    outflow: flow.outflow.toFixed(4) + " BNB",
    netFlow: (flow.inflow - flow.outflow).toFixed(4) + " BNB"
  }));
}
```

---

## Performance Considerations

- **Rate limiting:** Public RPC endpoints have request limits. Use batched calls or a dedicated RPC provider for bulk scanning.
- **Block range limits:** Some providers limit `getLogs` block ranges. Paginate event queries in chunks of 5000-10000 blocks.
- **Caching:** Cache agent state reads for dashboard UIs. Invalidate on new events.
- **Parallel reads:** Use `Promise.all` for independent agent lookups, but respect rate limits.
- **Incremental indexing:** Store the last indexed block number and resume from there on restart.
- **Batch RPC calls:** Use `ethers.JsonRpcProvider.send("eth_call", [...])` with multicall for efficient bulk reads.

---

## Related Skills

- `bap578`
- `bap578-analytics`
- `frontend-web3-bap578`
