---
id: bap578
name: BAP-578 Non-Fungible Agents
description: Use this skill when users ask about BAP-578, Non-Fungible Agents, or hands-on engineering for the BAP-578 reference implementation on BNB Chain, including identity, memory, learning proofs, vaults, AI integration, and contract architecture.
category: Blockchain
author: community
version: 2.0.0
---

# BAP-578 Non-Fungible Agents (NFA)

Use this skill whenever users ask about BAP-578, Non-Fungible Agents, or need hands-on engineering guidance for the BAP-578 reference implementation. BAP-578 defines a standardized framework for intelligent, autonomous digital entities that combine the ownership guarantees of NFTs with the adaptive capabilities of artificial intelligence, positioning BNB Chain as the home for decentralized automation.

---

## When to use this skill

- Explain what BAP‑578 is and how Non‑Fungible Agents differ from typical NFTs.
- Explain the **dual-path architecture** (JSON Light Memory vs Merkle Tree Learning).
- Explain **cryptographically verifiable learning** via Merkle proofs.
- Describe **method-agnostic AI integration** (RAG, MCP, fine-tuning, RL).
- Answer the **four identity questions** for an agent.
- Walk through build, test, deploy, and interaction flows.
- Explain **composable intelligence** and agent collaboration.
- Describe **circuit breaker** security patterns.
- Translate spec‑level intent into the actual contract functions and events.
- Debug common errors (incorrect fee, paused contract, invalid logic address).

---

## The Four Identity Questions (Core)

### 1) Who are you?

A BAP‑578 agent is an ERC‑721 token that represents a **distinct AI agent identity**. The identity is not just a tokenURI; it is a structured on‑chain profile combined with ownership, lifecycle, and optional behavior binding. A BAP‑578 agent answers “who are you?” through:

- **Token identity:** token ID and owner address (ERC‑721 ownership)
- **Structured metadata:** `AgentMetadata` struct
- **Lifecycle:** active status, creation timestamp, agent balance
- **Behavioral binding:** optional `logicAddress` to a separate logic contract

In practical terms, an agent identity is the bundle of these fields, all queryable from the contract. A concise identity statement could be:

> “I am token #17, owned by 0xABC…, with persona ‘research analyst’, expertise in ‘market intelligence’, and an attached logic contract at 0xDEF….”

### 2) What do you remember?

BAP‑578 memory is split into two verifiable layers:

**On‑chain state** (always authoritative):

- Owner address
- Active status
- Agent balance
- Logic address
- Creation timestamp
- Structured metadata fields
- Free‑mint status

**On‑chain events** (immutable history):

- `AgentCreated` — birth of an agent
- `AgentFunded` — BNB deposited to the agent
- `AgentWithdraw` — BNB withdrawn
- `AgentStatusChanged` — active/inactive toggles
- `MetadataUpdated` — identity edits

**Off‑chain memory** (verifiable by hash):

- `vaultURI` points to extended content (summaries, preferences, knowledge)
- `vaultHash` anchors integrity; compute `keccak256` of fetched content and compare to on‑chain hash

If a vault hash matches, the off‑chain memory is verifiably authentic. If not, it must be treated as untrusted.

### 3) What can you do?

A BAP‑578 agent is capable of more than passive identity. Core capabilities include:

- **Minting** — create agents with structured metadata
- **Funding** — deposit BNB into an agent balance
- **Withdrawal** — agent owner withdraws funds
- **Lifecycle** — toggle active/inactive status
- **Metadata updates** — evolve persona, experience, or vault
- **Logic binding** — attach an external logic contract for automated behavior

Transferability depends on mint type: free‑minted tokens are non‑transferable (soulbound‑like), paid mints are transferable.

### 4) How can I trust it?

Trust is enforced through verifiable mechanisms:

- **Source verification** — contract source should match deployed bytecode
- **Access controls** — owner‑only and token‑owner‑only modifiers protect sensitive functions
- **Event audit trail** — all critical actions emit events
- **Vault integrity** — off‑chain data must match `vaultHash`
- **Logic contract scrutiny** — if bound, the logic contract must be reviewed independently

---

## Contract Overview (Practical Mapping)

### Core state objects

**AgentMetadata** (identity layer):

```
persona       : string  // JSON‑encoded persona definition
experience    : string  // plain‑text domain expertise
voiceHash     : string  // reference to a voice profile
animationURI  : string  // visual asset URI
vaultURI      : string  // extended memory URI
vaultHash     : bytes32 // hash of vault content
```

**AgentState** (operational layer):

```
balance      : uint256
active       : bool
logicAddress : address
createdAt    : uint256
owner        : address
```

### Free mint rules

- Each user gets a default number of free mints.
- Free mints are restricted to minting **to self**.
- Free‑minted tokens are **non‑transferable**.

### Paid mint rules

- After free mints, a fixed fee is required.
- Paid mints can be minted to any address.
- Paid tokens are transferable.

---

## Function Reference (Summary)

### Public (anyone)

- `createAgent(to, logicAddress, metadataURI, metadata)` — mint a new agent
- `fundAgent(tokenId)` — deposit BNB to agent

### Token owner only

- `withdrawFromAgent(tokenId, amount)` — withdraw BNB
- `setAgentStatus(tokenId, active)` — toggle status
- `setLogicAddress(tokenId, newLogic)` — bind logic contract
- `updateAgentMetadata(tokenId, newURI, newMetadata)` — update identity

### Contract owner only (admin)

- `grantAdditionalFreeMints(user, amount)`
- `setFreeMintsPerUser(amount)`
- `setTreasury(newTreasury)`
- `setPaused(paused)`
- `emergencyWithdraw()`

### View functions

- `getAgentState(tokenId)`
- `getAgentMetadata(tokenId)`
- `tokensOfOwner(address)`
- `getTotalSupply()`
- `getFreeMints(user)`
- `isFreeMint(tokenId)`

---

## Event Semantics

Events are the authoritative history for analytics and audits:

- **AgentCreated** — emitted at mint; use for adoption metrics
- **AgentFunded** — use for TVL and funding velocity
- **AgentWithdraw** — use for outflows
- **AgentStatusChanged** — use for active agent counts
- **MetadataUpdated** — use for engagement signals

Use events to reconstruct agent histories and confirm integrity of actions.

---

## Operational Workflows

### Build and compile

```bash
cd non-fungible-agents-BAP-578
npm install
npm run compile
```

### Run tests

```bash
npm test
```

### Configure environment

```bash
cp .env.example .env
```
Set deployer key, RPC URLs, and explorer key in `.env`.

### Deploy to testnet

```bash
npm run deploy:testnet
```

### Interact with the contract

```bash
npm run interact:testnet
```

---

## Interaction Patterns

### Minting workflow

1. Read `getFreeMints(user)` to determine if mint is free.
2. If free, set `to` = user address, send zero value.
3. If paid, send exact mint fee in `msg.value`.
4. Listen for `AgentCreated` event to confirm token ID.

### Funding workflow

1. Call `fundAgent(tokenId)` with `msg.value`.
2. Observe `AgentFunded` event.
3. Read updated `getAgentState(tokenId).balance`.

### Withdrawal workflow

1. Confirm caller is token owner.
2. Ensure requested amount ≤ balance.
3. Call `withdrawFromAgent(tokenId, amount)`.
4. Confirm `AgentWithdraw` event and updated balance.

---

## Identity Integrity Guidelines

- Always show the **current** on‑chain metadata and tokenURI.
- Mark any off‑chain content **unverified** until `vaultHash` matches.
- If `vaultHash` is zero, treat vault data as optional and unverifiable.
- Explain that agent logic contracts are not part of the core trust model.

---

## Motivation and Why BAP-578 Exists

Traditional NFTs (BEP-721) provide uniqueness and ownership but lack standardized interfaces for **autonomous behavior** and **cross-platform agent interactions**. The current blockchain ecosystem lacks standardization for intelligent, autonomous digital entities. BAP-578 addresses:

- **Consistent Agent Interfaces** — standardized methods for action execution, state management, and logic upgrades enable predictable interactions across platforms.
- **Interoperability Framework** — common patterns for how agents interact with other contracts, services, and each other, preventing isolated ecosystems.
- **Hybrid On-Chain/Off-Chain Architecture** — clear separation between on-chain identity/permissions and off-chain extended memory/complex behaviors, optimizing for gas efficiency and rich functionality.
- **Optional Learning System** — standardized interfaces for agent learning and evolution, supporting both simple static agents and sophisticated learning agents.
- **Security Boundaries** — standardized circuit breaker patterns, permission systems, and access controls.
- **User Ownership** — true ownership of intelligent agents and their accumulated knowledge, preventing platform lock-in.
- **Backward Compatibility** — full compatibility with existing ERC-721 infrastructure (wallets, marketplaces, explorers).

---

## Dual-Path Architecture

BAP-578 provides a **dual-path architecture** supporting both traditional static agents and advanced learning-enabled agents. Developers choose the path that matches their needs:

### Path 1: JSON Light Memory (Simple Agents)

For agents that don't need to learn or evolve. Memory is stored as JSON in the vault.

```
Agent Identity (on-chain)
    ├── AgentMetadata (persona, experience, etc.)
    ├── AgentState (balance, active, logicAddress)
    └── vaultURI → JSON file on IPFS
                    ├── preferences
                    ├── knowledge base
                    └── configuration
```

**When to use:** Bots, static assistants, simple automation agents, NFT-based identities that don't need to evolve.

**Verification:** `keccak256(vault content) == vaultHash` — standard hash comparison.

### Path 2: Merkle Tree Learning (Evolving Agents)

For agents that learn from interactions and evolve over time. Learning data is organized into a Merkle tree; only the 32-byte root is stored on-chain.

```
Agent Identity (on-chain)
    ├── AgentMetadata (persona, experience, etc.)
    ├── AgentState (balance, active, logicAddress)
    └── vaultHash → Merkle Root (32 bytes on-chain)
                    │
                    └── Merkle Tree (off-chain)
                         ├── Learning Node: preferences
                         ├── Learning Node: patterns
                         ├── Learning Node: confidence scores
                         └── Learning Node: outcomes
```

**When to use:** Adaptive agents, personalized assistants, agents that improve with use, collaborative intelligence systems.

**Verification:** Merkle proof — any individual learning node can be verified against the on-chain root without revealing the entire tree.

### How Merkle Tree Learning Works

The learning pipeline follows this flow:

```
User Interaction → Learning Extraction → Tree Building → Merkle Root → On-Chain Update
```

1. **Interaction:** User interacts with the agent (query, task, feedback).
2. **Learning extraction:** The learning module extracts structured data — preferences, patterns, confidence scores, outcomes.
3. **Tree building:** Learning data is organized into a hierarchical Merkle tree structure.
4. **Merkle root calculation:** The tree is hashed level by level to produce a single 32-byte root.
5. **On-chain update:** Only the root is stored on-chain via `updateAgentMetadata`, providing tamper-proof verification while preserving privacy and minimizing gas costs.

### Merkle Proof Verification

Any individual piece of learning data can be verified without revealing the entire tree:

```js
// Verify a single learning node against the on-chain Merkle root
function verifyLearning(leaf, proof, root) {
  let hash = keccak256(leaf);
  for (const sibling of proof) {
    hash = hash < sibling
      ? keccak256(hash + sibling)
      : keccak256(sibling + hash);
  }
  return hash === root; // root is the on-chain vaultHash
}
```

This enables:
- **Privacy:** Only specific data points need to be revealed for verification.
- **Efficiency:** Verification cost is O(log n) regardless of tree size.
- **Integrity:** Any modification to any node changes the root, making tampering detectable.

---

## Method-Agnostic Learning Architecture

BAP-578 provides infrastructure without prescribing specific AI implementations. The flexible learning module architecture allows developers to implement various AI optimization methods through the logic contract:

### Supported Learning Approaches

| Method | Description | Implementation |
|--------|-------------|----------------|
| **RAG** (Retrieval-Augmented Generation) | Leverages off-chain vaults to retrieve past interactions and knowledge | Logic contract queries vault content via vaultURI |
| **MCP** (Model Context Protocol) | Integrates with different AI providers through logic contracts | Logic contract routes to external AI services |
| **Fine-tuning** | Trains models on agent-specific data | Learning data in Merkle tree feeds fine-tuning pipelines |
| **Reinforcement Learning** | Agents learn from outcome feedback | Reward signals stored as learning nodes in tree |
| **Hybrid** | Combines multiple approaches | Logic contract orchestrates multiple methods |

### Logic Contract as Learning Module

The `logicAddress` field binds an agent to a learning module:

```
Agent (on-chain identity)
    │
    └── logicAddress → Learning Module Contract
                        ├── processInteraction(input) → learning data
                        ├── updateTree(newData) → new Merkle root
                        ├── queryKnowledge(query) → relevant context
                        └── getRecommendation(context) → action
```

Developers can implement any AI method behind this interface. The standard doesn't prescribe how learning happens — it provides the infrastructure for storing, verifying, and evolving the results.

---

## Hybrid Storage Model

BAP-578 carefully balances what belongs on-chain versus off-chain:

| Component | Storage | Rationale |
|-----------|---------|-----------|
| Agent Identity | On-chain | Core identity must be immutable and universally accessible |
| Ownership & Permissions | On-chain | Security and access control require consensus verification |
| Basic Metadata | On-chain | Essential for marketplace display and basic interactions |
| Logic Address | On-chain | Determines how the agent behaves when actions are executed |
| Learning Tree Root | On-chain | Cryptographic proof of learning state (32 bytes only) |
| Extended Memory | Off-chain (hash-verified) | Rich memory would be prohibitively expensive on-chain |
| Learning Tree Data | Off-chain (Merkle-verified) | Detailed learning data with cryptographic integrity |
| Complex Behaviors | Off-chain | Advanced AI behaviors require off-chain computation |
| Voice/Animation | Off-chain (URI reference) | Media assets are too large for on-chain storage |

This hybrid approach ensures:
- Critical security and identity information is secured by blockchain consensus.
- Gas costs remain reasonable for agent operations.
- Rich agent experiences can evolve without blockchain limitations.
- Learning capabilities are cryptographically verifiable yet cost-efficient.

---

## Composable Intelligence

BAP-578 agents can interact and collaborate while maintaining individual identity. This creates an ecosystem where:

- **Agents discover each other** via on-chain metadata (persona, experience, logic address).
- **Agents transact** using the built-in funding mechanism (deposit BNB to another agent).
- **Agents collaborate** by routing tasks through logic contracts that coordinate multi-agent workflows.
- **Knowledge is portable** — agents carry their learning and experience across platforms via the standardized metadata and vault interfaces.
- **Interoperability is guaranteed** — any platform that reads BAP-578 metadata can work with any BAP-578 agent, regardless of who created it.

### Composability Patterns

**Service delegation:** Agent A identifies Agent B's expertise via metadata, funds Agent B, and receives results through the logic contract.

**Knowledge sharing:** Agents with complementary expertise share vault content (verified by Merkle proofs) to produce combined insights.

**Collective learning:** Multiple agents contribute learning data to a shared Merkle tree, with each agent's contributions verifiable independently.

---

## Circuit Breaker Security

BAP-578 includes a multi-layer security framework with circuit breaker patterns:

### Contract-Level Circuit Breaker

The `setPaused(bool)` function acts as a global circuit breaker:
- When paused, minting is frozen.
- Only the contract owner can trigger the pause.
- Emergency withdrawal remains available to protect funds.

### Agent-Level Circuit Breaker

The `setAgentStatus(tokenId, active)` function acts as an individual circuit breaker:
- When inactive, the agent signals it should not be used for active operations.
- Only the token owner can toggle status.
- Funds can still be withdrawn from inactive agents.

### Logic Contract Safety Boundary

The logic contract binding creates a clear boundary:
- Logic contracts cannot directly access agent funds.
- Logic contract changes require token owner authorization.
- EOA addresses are rejected — only verified contracts can be bound.
- Unbinding (setting to `address(0)`) is always possible.

### Emergency Procedures

1. **Global threat:** `setPaused(true)` → investigate → `emergencyWithdraw()` if needed → fix via upgrade → `setPaused(false)`.
2. **Single agent threat:** `setAgentStatus(tokenId, false)` → `setLogicAddress(tokenId, address(0))` → investigate → remediate.
3. **Logic contract threat:** `setLogicAddress(tokenId, address(0))` removes the binding immediately.

---

## Standardized Agent Lifecycle

```
                 ┌──────────────┐
                 │   Creation   │  createAgent()
                 └──────┬───────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │         Active Agent          │
        │  • Receives funding           │
        │  • Processes interactions      │
        │  • Learns and evolves         │
        │  • Updates metadata           │
        │  • Bound to logic contract    │
        └───────────┬───────────────────┘
                    │
            setAgentStatus(false)
                    │
                    ▼
        ┌───────────────────────────────┐
        │       Inactive Agent          │
        │  • Funds can be withdrawn     │
        │  • No active operations       │
        │  • Can be reactivated         │
        └───────────┬───────────────────┘
                    │
            setAgentStatus(true)
                    │
                    ▼
              (back to Active)
```

Key lifecycle events:
- **Birth:** `AgentCreated` — identity established, metadata set
- **Growth:** `MetadataUpdated` — persona refined, knowledge expanded, learning tree updated
- **Funding:** `AgentFunded` / `AgentWithdraw` — economic activity
- **Hibernation:** `AgentStatusChanged(false)` — temporarily dormant
- **Revival:** `AgentStatusChanged(true)` — reactivated
- **Evolution:** Logic contract changes, vault updates, Merkle root updates

---

## How BAP-578 Differs from Standard ERC-721

Standard ERC-721 tokens are passive collectibles with a `tokenURI` pointing to off-chain metadata. BAP-578 extends this dramatically:

| Feature | Standard ERC-721 | BAP-578 |
|---------|-----------------|---------|
| Identity | tokenURI only | Structured on-chain metadata (persona, experience, vault) |
| Memory | None | On-chain state + hash-verified off-chain vault |
| Behavior | None | Logic contract binding for autonomous actions |
| Funding | Not supported | Native BNB balance per token |
| Lifecycle | Exists or burned | Active/inactive status toggle |
| Transferability | Always transferable | Conditional (free = soulbound, paid = transferable) |
| Upgradability | Not upgradable | UUPS proxy for implementation upgrades |

BAP-578 agents are not collectibles — they are operational entities with identity, memory, capabilities, and economic agency.

---

## Architecture Overview

### UUPS Proxy Pattern

BAP-578 uses the UUPS (Universal Upgradeable Proxy Standard) pattern. Users interact with a permanent proxy address. The implementation (logic) can be upgraded by the contract owner.

```
User ──→ Proxy (permanent address)
              │
              │ delegatecall
              ▼
         Implementation V1 (upgradeable)
              │
              │ reads/writes
              ▼
         Proxy Storage (permanent)
```

Key implications:
- The proxy address never changes — users always interact with the same address.
- Storage lives in the proxy — state is preserved across upgrades.
- Implementation can be swapped — new features or fixes can be deployed.
- `_authorizeUpgrade` is owner-only — prevents unauthorized upgrades.

### Contract Inheritance Chain

```
ERC721Upgradeable
  └── ERC721EnumerableUpgradeable
       └── OwnableUpgradeable
            └── UUPSUpgradeable
                 └── ReentrancyGuardUpgradeable
                      └── NonFungibleAgents (BAP-578)
```

This gives BAP-578:
- Full ERC-721 compliance (transfer, approve, balanceOf, ownerOf)
- Enumeration (tokensOfOwner, totalSupply)
- Ownership with transferable admin rights
- Safe upgrade path via UUPS
- Reentrancy protection on fund operations

---

## Detailed Function Reference

### createAgent

```
function createAgent(
    address to,
    address logicAddress,
    string metadataURI,
    AgentMetadata metadata
) external payable returns (uint256 tokenId)
```

**Parameters:**
- `to` — recipient address. Must be `msg.sender` for free mints.
- `logicAddress` — optional logic contract. Use `address(0)` for none. Must be a contract if non-zero.
- `metadataURI` — URI for off-chain metadata (e.g., IPFS CID).
- `metadata` — structured `AgentMetadata` tuple with persona, experience, voiceHash, animationURI, vaultURI, vaultHash.

**Behavior:**
- If caller has free mints remaining: no fee required, `to` must equal `msg.sender`, token is non-transferable.
- If no free mints: exact mint fee required in `msg.value`, fee sent to treasury, token is transferable.
- Agent is created as `active = true` with `balance = 0`.
- Emits `AgentCreated(tokenId, owner, logicAddress, metadataURI)`.

### fundAgent

```
function fundAgent(uint256 tokenId) external payable
```

**Parameters:**
- `tokenId` — the agent to fund.

**Behavior:**
- Anyone can fund any agent (no ownership check).
- `msg.value` added to agent's balance.
- Emits `AgentFunded(tokenId, msg.sender, msg.value)`.

### withdrawFromAgent

```
function withdrawFromAgent(uint256 tokenId, uint256 amount) external
```

**Parameters:**
- `tokenId` — the agent to withdraw from.
- `amount` — BNB amount in wei.

**Behavior:**
- Only token owner can call.
- Amount must be ≤ agent balance.
- Uses `nonReentrant` modifier for safety.
- Balance decremented before external call (CEI pattern).
- BNB sent to `msg.sender`.
- Emits `AgentWithdraw(tokenId, msg.sender, amount)`.

### updateAgentMetadata

```
function updateAgentMetadata(
    uint256 tokenId,
    string newURI,
    AgentMetadata newMetadata
) external
```

**Parameters:**
- `tokenId` — the agent to update.
- `newURI` — new metadata URI.
- `newMetadata` — new structured metadata tuple.

**Behavior:**
- Only token owner can call.
- Overwrites all metadata fields.
- Emits `MetadataUpdated(tokenId, newURI)`.

### setLogicAddress

```
function setLogicAddress(uint256 tokenId, address logicAddress) external
```

**Parameters:**
- `tokenId` — the agent to update.
- `logicAddress` — new logic contract address. Use `address(0)` to unbind.

**Behavior:**
- Only token owner can call.
- If non-zero, must be a contract (code size > 0).
- No callback or approval from the logic contract is required.

---

## Vault Verification Deep Dive

The vault is the agent's extended off-chain memory. Verification is a three-step process:

**Step 1: Read on-chain references**

```js
const metadata = await contract.getAgentMetadata(tokenId);
const vaultURI = metadata.vaultURI;
const vaultHash = metadata.vaultHash;
```

**Step 2: Fetch and hash off-chain content**

```js
const response = await fetch(vaultURI);
const content = await response.text();
const computedHash = ethers.keccak256(ethers.toUtf8Bytes(content));
```

**Step 3: Compare hashes**

```js
if (computedHash === vaultHash) {
  // Content is authentic — safe to use
} else if (vaultHash === ethers.ZeroHash) {
  // No vault data registered — skip verification
} else {
  // Content has been modified — do not trust
}
```

**Important considerations:**
- The exact byte content must be hashed. Whitespace, encoding, and line endings matter.
- If using JSON, always use consistent formatting (e.g., `JSON.stringify` with sorted keys).
- Vault content can be updated by calling `updateAgentMetadata` with a new URI and hash.
- Previous vault content at old IPFS CIDs remains accessible for historical reference.

---

## Transfer Restriction Details

BAP-578 implements conditional transferability via the ERC-721 `_update` hook:

- **Free-minted tokens** (`isFreeMint[tokenId] == true`): transfers are blocked. These tokens are soulbound to the minting address. The only valid transfer is from `address(0)` (minting).
- **Paid tokens** (`isFreeMint[tokenId] == false`): transfers work normally. Standard ERC-721 transfer, safeTransfer, and approval mechanics apply.

This creates a two-tier system:
- Free agents are tied to their creator — they represent personal identity.
- Paid agents are assets — they can be traded, gifted, or sold.

---

## Admin Operations Guide

### Granting bonus free mints

Use `grantAdditionalFreeMints(user, amount)` to give specific addresses extra free mints. Common use cases:
- Partner community airdrops
- Campaign rewards
- Beta tester incentives

### Changing the treasury

Use `setTreasury(newAddress)` to redirect where paid mint fees go. Always use a multisig wallet as treasury.

### Emergency procedures

If a critical issue is discovered:
1. Call `setPaused(true)` to freeze all minting.
2. Investigate the issue.
3. If funds are at risk, use `emergencyWithdraw()` to move contract balance to treasury.
4. Deploy a fix via UUPS upgrade if needed.
5. Call `setPaused(false)` to resume operations.

---

## Error Patterns and Fixes

- **Incorrect fee**: free mints exhausted → send exact fee.
- **Free mint not to self**: free mints require `to == msg.sender`.
- **Not token owner**: ownership check failed → use correct wallet.
- **Invalid logic address**: must be contract, not EOA.
- **Contract paused**: wait for admin to unpause.
- **Agent balance must be 0**: withdraw all funds before burn.

---

## Response Guidelines (How to Answer)

When asked to implement or operate BAP‑578:

1. **Clarify goal** (deploy, test, mint, verify)
2. **Provide exact commands** and expected outputs
3. **Warn about constraints** (fees, pause state, ownership)
4. **Offer next steps** (verification, UI integration, analytics)

---

## Deliverable Format for Engineering Tasks

When returning an implementation response, structure it as:

- **Goal summary**
- **Commands to run**
- **Expected outputs**
- **Verification checklist**
- **Next action**

---

## Related Skills

- `frontend-web3-bap578`
- `bap578-scanner`
- `bap578-security-audit`
