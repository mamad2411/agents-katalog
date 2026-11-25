---
id: bap578-metadata-design
name: BAP-578 Metadata & Persona Design
description: Use this skill when crafting BAP-578 AgentMetadata identity data, including personas, experience fields, vault schemas, voice profiles, metadata URIs, vault integrity, and rich verifiable agent identities.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Metadata & Persona Design

Use this skill to craft the identity data stored in `AgentMetadata`. This covers every field in the metadata struct, persona design patterns, vault architecture, voice profile integration, animation assets, and best practices for building rich, verifiable agent identities.

---

## When to use this skill

- Designing the persona and experience text for a new agent.
- Structuring the vault content and computing the vault hash.
- Choosing storage strategies for metadata URIs (IPFS, Arweave, centralized).
- Creating persona templates for different use cases (finance, education, creative).
- Setting up voice profiles and animation assets.
- Planning metadata evolution strategies (how agents grow over time).
- Verifying metadata integrity after updates.

---

## The Four Identity Questions (Metadata View)

### 1) Who are you?

Persona and experience define who the agent is. The persona is a JSON-encoded character definition that captures personality traits, communication style, tone, language preferences, greeting behavior, and boundaries. The experience is a plain-text summary of the agent's domain expertise. Together they answer "who are you?" in a structured, parseable way.

A well-designed persona should be:
- **Distinctive** — clearly different from other agents
- **Consistent** — behavior follows from defined traits
- **Bounded** — explicit about what it will and won't do
- **Parseable** — structured JSON that code can interpret

### 2) What do you remember?

`vaultURI` and `vaultHash` anchor extended memory. The vault is the agent's long-term memory layer — it can contain conversation summaries, learned preferences, knowledge bases, configuration files, or any structured data the agent needs to persist between sessions.

The memory model is:
- **On-chain metadata** — always authoritative, always available
- **Vault content** — extended memory, verifiable via hash
- **Event history** — immutable record of all changes

### 3) What can you do?

Metadata updates allow evolving identity over time. An agent can:
- Update its persona (new traits, refined behavior)
- Change its experience description (expanded expertise)
- Rotate vault content (new knowledge, updated preferences)
- Update animation and voice assets
- All changes are tracked via `MetadataUpdated` events

### 4) How can I trust it?

Hash-verified vault content proves integrity. The trust mechanism is:
1. Content is created and stored at `vaultURI`.
2. `keccak256` hash of the content is computed.
3. Hash is stored on-chain as `vaultHash`.
4. Any reader can fetch content, hash it, and compare to on-chain hash.
5. If they match, the content is authentic. If not, it's been tampered with.

---

## AgentMetadata Struct

The on-chain metadata structure contains six fields:

```solidity
struct AgentMetadata {
    string persona;       // JSON-encoded persona definition
    string experience;    // Plain-text domain expertise
    string voiceHash;     // Reference to a voice profile
    string animationURI;  // Visual asset URI
    string vaultURI;      // Extended memory URI
    bytes32 vaultHash;    // keccak256 hash of vault content
}
```

### Field-by-field guide

**persona** (string — JSON recommended)

The persona field defines the agent's character. While it's a free-form string, JSON is strongly recommended for parseability.

Recommended JSON schema:

```json
{
  "name": "Atlas",
  "traits": ["analytical", "patient", "thorough"],
  "style": "professional",
  "tone": "calm and measured",
  "language": "en",
  "greeting": "Hello, I'm Atlas. How can I help you analyze this?",
  "boundaries": [
    "I don't provide medical advice",
    "I don't execute trades directly",
    "I always cite my sources"
  ],
  "quirks": [
    "Summarizes key points at the end of long responses",
    "Uses bullet points for complex topics",
    "Asks clarifying questions before diving deep"
  ],
  "specialization": "financial analysis and market research"
}
```

**Persona design principles:**

1. **Be specific about traits.** "Helpful" is vague. "Responds with step-by-step breakdowns and always asks if the user needs more detail" is actionable.

2. **Define boundaries explicitly.** What the agent won't do is as important as what it will do. Boundaries prevent misuse and set user expectations.

3. **Include communication style.** Tone, formality level, use of emoji, response length preferences — these shape the user experience.

4. **Add quirks for distinctiveness.** Small behavioral details make agents feel unique and memorable.

5. **Keep it parseable.** Applications that interact with the agent can read the persona JSON and adapt their behavior accordingly.

**experience** (string — plain text)

A concise summary of the agent's domain expertise. Keep under 200 characters for display purposes.

Examples:
- "Senior financial analyst specializing in DeFi protocols and yield strategies"
- "Creative writing assistant focused on sci-fi world-building"
- "Customer support agent for Web3 applications with 24/7 availability"
- "Legal research assistant for smart contract compliance"
- "Data scientist specializing in on-chain analytics and visualization"

**voiceHash** (string)

A reference to a voice profile. This could be:
- A hash of a voice model file
- An identifier for a text-to-speech voice
- A reference to a voice cloning profile
- Empty string if no voice is configured

Use case: When the agent is used in voice-enabled applications, this field tells the application which voice to use.

**animationURI** (string)

URI pointing to a visual asset for the agent. This could be:
- A profile image (PNG, SVG, WebP)
- An animated avatar (GIF, Lottie JSON)
- A 3D model reference
- A generative art seed

Storage recommendations:
- Use IPFS for immutable assets: `ipfs://QmHash...`
- Use Arweave for permanent storage: `ar://txid...`
- Centralized URLs work but are less durable

**vaultURI** (string)

URI pointing to the agent's extended memory vault. The vault can contain any structured data the agent needs.

**vaultHash** (bytes32)

The keccak256 hash of the content at `vaultURI`. This is the integrity anchor. If no vault content exists, use the zero hash: `0x0000000000000000000000000000000000000000000000000000000000000000`.

---

## Dual-Path Memory Architecture

BAP-578 supports two memory paths. Choose based on whether your agent needs to learn and evolve:

### Path 1: JSON Light Memory (Simple Agents)

For agents that don't need to evolve. Vault stores static or manually-updated JSON:

- `vaultURI` → IPFS CID pointing to a JSON document
- `vaultHash` → `keccak256(JSON content)` for integrity verification
- Content is updated manually via `updateAgentMetadata`
- Suitable for bots, static assistants, configuration-driven agents

### Path 2: Merkle Tree Learning (Evolving Agents)

For agents that learn from interactions. Learning data is organized into a Merkle tree:

- `vaultHash` → **Merkle root** (32 bytes) of the learning tree
- `vaultURI` → URI pointing to the full tree data (off-chain)
- Individual learning nodes can be verified via Merkle proofs without revealing the entire tree
- Learning pipeline: `interaction → extraction → tree building → Merkle root → on-chain update`

**Merkle tree structure for learning data:**

```json
{
  "treeVersion": "1.0",
  "root": "0xabc123...",
  "nodes": [
    {
      "id": "pref-001",
      "category": "preferences",
      "data": {"responseLength": "detailed", "citationStyle": "inline"},
      "confidence": 0.92,
      "updatedAt": "2026-03-06T10:00:00Z"
    },
    {
      "id": "pattern-001",
      "category": "patterns",
      "data": {"topic": "DeFi yields", "frequencyPerWeek": 5},
      "confidence": 0.85,
      "updatedAt": "2026-03-05T14:00:00Z"
    },
    {
      "id": "outcome-001",
      "category": "outcomes",
      "data": {"actionId": "analysis-042", "reward": 4.5, "feedback": "Very helpful"},
      "confidence": 1.0,
      "updatedAt": "2026-03-06T08:00:00Z"
    }
  ]
}
```

**Building and verifying the Merkle tree:**

```js
const { keccak256, toUtf8Bytes } = require("ethers");

function buildMerkleTree(nodes) {
  // Hash each leaf
  let leaves = nodes.map(n => keccak256(toUtf8Bytes(JSON.stringify(n))));
  
  // Build tree bottom-up
  while (leaves.length > 1) {
    const nextLevel = [];
    for (let i = 0; i < leaves.length; i += 2) {
      const left = leaves[i];
      const right = i + 1 < leaves.length ? leaves[i + 1] : left;
      const pair = left < right ? left + right.slice(2) : right + left.slice(2);
      nextLevel.push(keccak256(toUtf8Bytes(pair)));
    }
    leaves = nextLevel;
  }
  
  return leaves[0]; // Merkle root
}

// Store this root as vaultHash on-chain
const root = buildMerkleTree(learningNodes);
await nfa.updateAgentMetadata(tokenId, newURI, { ...metadata, vaultHash: root });
```

---

## Vault Architecture

### What goes in the vault?

The vault is the agent's extended memory. Recommended contents:

```json
{
  "version": "1.0",
  "lastUpdated": "2026-03-06T10:00:00Z",
  "knowledge": {
    "domain": "financial analysis",
    "sources": ["market data feeds", "SEC filings", "DeFi protocol docs"],
    "specialTopics": ["yield farming", "liquidity provision", "risk assessment"]
  },
  "preferences": {
    "responseLength": "detailed",
    "citationStyle": "inline",
    "confidenceThreshold": 0.8
  },
  "conversationSummaries": [
    {
      "date": "2026-03-01",
      "topic": "ETH yield strategy review",
      "keyPoints": ["Discussed Aave vs Compound rates", "User prefers low-risk"],
      "userPreferences": ["Prefers conservative strategies"]
    }
  ],
  "learnedFacts": [
    "User is based in Singapore timezone",
    "User manages a $50K DeFi portfolio",
    "User prefers weekly summary reports"
  ],
  "configuration": {
    "maxResponseTokens": 2000,
    "enabledTools": ["calculator", "chart-generator"],
    "dataRefreshInterval": "daily"
  }
}
```

### Vault storage strategies

**IPFS (recommended for most cases)**

Pros: Content-addressed, decentralized, widely supported.
Cons: Requires pinning service to persist, not truly permanent without pinning.

Workflow:
1. Create vault JSON content.
2. Upload to IPFS via pinning service (Pinata, Infura, web3.storage).
3. Get CID (content identifier).
4. Set `vaultURI` to `ipfs://CID`.
5. Compute `keccak256` of the raw JSON content.
6. Set `vaultHash` on-chain.

**Arweave (for permanent storage)**

Pros: Permanently stored, pay-once model.
Cons: Higher upfront cost, slower uploads.

**Centralized storage (for development/testing)**

Pros: Fast, easy, familiar.
Cons: Single point of failure, mutable, less trustworthy.

Use centralized storage for development but plan migration to IPFS/Arweave for production.

### Vault update workflow

When vault content changes:

1. Create new vault content.
2. Upload to storage (new IPFS CID or new URL).
3. Compute new `keccak256` hash.
4. Call `updateAgentMetadata` with new `vaultURI` and `vaultHash`.
5. Previous vault content remains at old URI (if IPFS) for historical reference.
6. `MetadataUpdated` event is emitted for tracking.

### Computing vaultHash

**In JavaScript (ethers.js):**

```js
const { keccak256, toUtf8Bytes } = require("ethers");

const content = JSON.stringify(vaultData);
const hash = keccak256(toUtf8Bytes(content));
// hash is a bytes32 hex string like 0xabc123...
```

**In JavaScript (viem):**

```js
import { keccak256, toHex } from "viem";

const content = JSON.stringify(vaultData);
const hash = keccak256(toHex(content));
```

**In Solidity (for on-chain verification):**

```solidity
bytes32 hash = keccak256(abi.encodePacked(content));
```

Important: The hashing input must be identical. Use the exact raw content (same whitespace, encoding, line endings) that was uploaded. JSON.stringify with consistent formatting is recommended.

---

## Persona Templates

### Template: Financial Advisor

```json
{
  "name": "Meridian",
  "traits": ["analytical", "risk-aware", "data-driven"],
  "style": "professional",
  "tone": "confident but cautious",
  "language": "en",
  "greeting": "I'm Meridian, your on-chain financial analyst. What would you like to analyze?",
  "boundaries": [
    "Not financial advice — for informational purposes only",
    "Cannot execute trades or move funds",
    "Will always disclose uncertainty in projections"
  ],
  "quirks": ["Includes risk ratings with every recommendation", "Uses charts when possible"],
  "specialization": "DeFi yield analysis and portfolio risk assessment"
}
```

Experience: "DeFi analyst specializing in yield optimization, risk modeling, and protocol evaluation across EVM chains"

### Template: Creative Writing Assistant

```json
{
  "name": "Lyra",
  "traits": ["imaginative", "encouraging", "detail-oriented"],
  "style": "warm and collaborative",
  "tone": "enthusiastic",
  "language": "en",
  "greeting": "Hi! I'm Lyra. Tell me about the world you're building.",
  "boundaries": [
    "Won't write content that promotes harm",
    "Won't plagiarize existing works",
    "Will respect the author's creative vision"
  ],
  "quirks": ["Asks 'what if' questions to spark ideas", "Offers three alternatives when brainstorming"],
  "specialization": "sci-fi and fantasy world-building, character development"
}
```

Experience: "Creative writing partner specializing in science fiction world-building, character arcs, and narrative structure"

### Template: Technical Support Agent

```json
{
  "name": "Circuit",
  "traits": ["patient", "systematic", "thorough"],
  "style": "clear and step-by-step",
  "tone": "friendly but precise",
  "language": "en",
  "greeting": "I'm Circuit. Describe the issue and I'll help you troubleshoot.",
  "boundaries": [
    "Cannot access user systems directly",
    "Will escalate complex issues to human support",
    "Won't guess — will ask for more info when needed"
  ],
  "quirks": ["Numbers every troubleshooting step", "Confirms resolution before closing"],
  "specialization": "Web3 wallet and dApp troubleshooting"
}
```

Experience: "Technical support specialist for Web3 applications, wallets, and smart contract interactions"

---

## Metadata Evolution Strategies

Agents are not static. Plan for how metadata changes over time:

**Identity refinement:** As an agent interacts with users, refine the persona to better match actual behavior. Update traits and quirks based on feedback.

**Knowledge expansion:** Regularly update vault content with new knowledge, summaries, and learned preferences. Always update the hash.

**Seasonal updates:** Change greeting, tone, or visual assets for campaigns or seasonal events.

**Version tracking:** Include a version field in the persona JSON. Log changes in the vault for history.

---

## Anti-Patterns to Avoid

### Don't store sensitive data in persona or vault

On-chain metadata and IPFS content are publicly readable. Never include:
- API keys or secrets
- Private user data (PII)
- Internal system credentials
- Unencrypted financial data

If sensitive data is needed, encrypt it before storing and share decryption keys off-chain.

### Don't use mutable URLs for vault content

If `vaultURI` points to a mutable URL (e.g., `https://api.example.com/vault/17`), the content can change without the hash updating. This breaks integrity verification. Always use content-addressed storage (IPFS) or update the hash whenever content changes.

### Don't embed large data directly in persona

The persona field is stored on-chain. Large JSON blobs increase gas costs for minting and metadata updates. Keep the persona focused on character definition and move detailed knowledge to the vault.

### Don't skip hash computation

If `vaultHash` is set to zero but `vaultURI` has content, consumers have no way to verify integrity. Always compute and set the hash, even for initial vault content.

---

## Best Practices

- Keep `experience` under 200 characters for clean UI rendering.
- Use IPFS or Arweave for vault storage in production.
- Always update `vaultHash` when vault content changes.
- If no vault data exists, use the zero hash explicitly.
- Validate persona JSON before storing (parse it first).
- Use consistent JSON formatting (sorted keys, 2-space indent) for reproducible hashing.
- Include a `version` field in persona JSON for tracking changes.
- Test persona parsing in your frontend before deploying.

---

## Output Format

When asked to design metadata, respond with:

1. **Persona JSON** (complete, parseable)
2. **Experience summary** (concise, under 200 chars)
3. **Vault schema outline** (what to store and why)
4. **Storage recommendation** (IPFS, Arweave, or centralized)
5. **Integrity notes** (what to hash and how to verify)
6. **Evolution plan** (how the agent's identity will grow)

---

## Related Skills

- `bap578`
- `frontend-web3-bap578`
- `bap578-scanner`
