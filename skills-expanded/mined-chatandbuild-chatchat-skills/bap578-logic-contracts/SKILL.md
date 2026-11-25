---
id: bap578-logic-contracts
name: BAP-578 Logic Contracts
description: Use this skill when designing, building, deploying, binding, or reviewing logic contracts that define autonomous on-chain behavior for BAP-578 Non-Fungible Agents.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Logic Contracts

Use this skill to design, build, deploy, and bind logic contracts that define on-chain agent behavior for BAP-578 Non-Fungible Agents. Logic contracts are the behavioral extension layer — they give agents the ability to perform autonomous actions, execute strategies, respond to events, and interact with other contracts.

---

## When to use this skill

- Designing autonomous behavior for a BAP-578 agent.
- Building a logic contract from scratch.
- Binding or unbinding a logic contract to an existing agent.
- Reviewing the security of a logic contract before binding.
- Understanding the relationship between the NFA contract and logic contracts.
- Creating logic contract templates for common use cases.
- Planning a logic contract marketplace.

---

## The Four Identity Questions (Logic View)

### 1) Who are you?

The logic contract is the behavioral layer of a BAP-578 agent. While the main NFA contract defines identity (who the agent is) and state (what it remembers), the logic contract defines action (what it does). A logic contract is a separate smart contract deployed independently, then bound to an agent via the `logicAddress` field.

The binding creates a relationship:
- **NFA contract** = identity + state + ownership
- **Logic contract** = behavior + strategy + automation

Think of it as: the NFA contract is the agent's brain (memory and identity), and the logic contract is the agent's hands (actions and capabilities).

### 2) What do you remember?

Logic contracts can maintain their own state variables, giving agents additional memory beyond what the NFA contract stores. This could include:

- Strategy parameters (thresholds, targets, limits)
- Execution history (last action timestamp, cumulative results)
- Configuration (enabled features, permissions)
- Relationships (other agents or contracts it interacts with)

The logic contract can also read the agent's on-chain state from the NFA contract by calling view functions like `getAgentState` and `getAgentMetadata`.

### 3) What can you do?

Logic contracts enable agents to perform actions autonomously. Capabilities depend entirely on what the logic contract implements:

- **Execute strategies** — DeFi yield farming, rebalancing, arbitrage
- **Respond to events** — react to price changes, governance proposals, or external triggers
- **Route requests** — forward incoming calls to specialized handler contracts
- **Manage resources** — allocate agent balance to different protocols
- **Interact with other agents** — agent-to-agent communication and coordination
- **Provide services** — answer queries, generate outputs, process requests

### 4) How can I trust it?

Logic contract trust must be established independently of the NFA contract:

- **Source verification** — the logic contract source code should be verified on a block explorer
- **Audit** — critical logic contracts should undergo security review
- **Permissions analysis** — understand exactly what the logic contract can and cannot do
- **Immutability assessment** — determine if the logic contract is upgradeable
- **Separation of concerns** — the logic contract should not be able to drain agent funds unless explicitly designed to do so

---

## Architecture

### How logic binding works

```
┌──────────────────────────┐
│      NFA Contract         │
│                           │
│  Agent #17                │
│  ├── owner: 0xABC         │
│  ├── balance: 1.5 BNB     │
│  ├── active: true         │
│  ├── metadata: {...}      │
│  └── logicAddress: 0xDEF  │◄──── binding
│                           │
└──────────────────────────┘
              │
              │ calls / reads
              ▼
┌──────────────────────────┐
│    Logic Contract (0xDEF) │
│                           │
│  - execute()              │
│  - getStatus()            │
│  - configure()            │
│                           │
│  Can read NFA state via:  │
│  - nfa.getAgentState(17)  │
│  - nfa.getAgentMetadata() │
│                           │
└──────────────────────────┘
```

### Binding rules

1. **Only the token owner** can set the logic address for their agent.
2. **The logic address must be a contract**, not an externally owned account (EOA). The contract checks `address.code.length > 0`.
3. **Setting to `address(0)`** unbinds the logic contract (removes behavior).
4. **Binding is reversible** — the owner can change or remove the logic contract at any time.
5. **The logic contract has no special permissions** on the NFA contract. It cannot withdraw agent funds, transfer the token, or modify metadata unless explicitly delegated.

### Binding flow

```solidity
// Token owner binds a logic contract
nfa.setLogicAddress(tokenId, logicContractAddress);

// Emits event for tracking
// event LogicAddressChanged(uint256 indexed tokenId, address logicAddress);

// Token owner unbinds
nfa.setLogicAddress(tokenId, address(0));
```

---

## Building a Logic Contract

### Minimal interface

Logic contracts don't need to implement a specific interface, but a recommended pattern is:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface INonFungibleAgents {
    struct AgentState {
        uint256 balance;
        bool active;
        address logicAddress;
        uint256 createdAt;
        address owner;
    }

    struct AgentMetadata {
        string persona;
        string experience;
        string voiceHash;
        string animationURI;
        string vaultURI;
        bytes32 vaultHash;
    }

    function getAgentState(uint256 tokenId) external view returns (AgentState memory);
    function getAgentMetadata(uint256 tokenId) external view returns (AgentMetadata memory);
}
```

### Pattern: Simple Greeter

A minimal logic contract that reads agent metadata and returns a greeting:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./INonFungibleAgents.sol";

contract GreeterLogic {
    INonFungibleAgents public immutable nfa;

    event GreetingGenerated(uint256 indexed tokenId, string greeting);

    constructor(address _nfa) {
        nfa = INonFungibleAgents(_nfa);
    }

    function greet(uint256 tokenId) external view returns (string memory) {
        INonFungibleAgents.AgentMetadata memory meta = nfa.getAgentMetadata(tokenId);
        return string(abi.encodePacked(
            "Hello! I am an agent with experience in: ",
            meta.experience
        ));
    }

    function getAgentInfo(uint256 tokenId) external view returns (
        bool active,
        uint256 balance,
        string memory experience
    ) {
        INonFungibleAgents.AgentState memory state = nfa.getAgentState(tokenId);
        INonFungibleAgents.AgentMetadata memory meta = nfa.getAgentMetadata(tokenId);
        return (state.active, state.balance, meta.experience);
    }
}
```

### Pattern: Strategy Executor

A logic contract that executes a defined action when triggered by a keeper or automation service:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./INonFungibleAgents.sol";

contract StrategyLogic {
    INonFungibleAgents public immutable nfa;

    struct StrategyConfig {
        uint256 threshold;
        uint256 lastExecuted;
        uint256 executionCount;
        bool enabled;
    }

    mapping(uint256 => StrategyConfig) public strategies;

    event StrategyExecuted(uint256 indexed tokenId, uint256 timestamp);
    event StrategyConfigured(uint256 indexed tokenId, uint256 threshold);

    constructor(address _nfa) {
        nfa = INonFungibleAgents(_nfa);
    }

    modifier onlyAgentOwner(uint256 tokenId) {
        INonFungibleAgents.AgentState memory state = nfa.getAgentState(tokenId);
        require(msg.sender == state.owner, "Not agent owner");
        _;
    }

    function configure(uint256 tokenId, uint256 threshold) external onlyAgentOwner(tokenId) {
        strategies[tokenId] = StrategyConfig({
            threshold: threshold,
            lastExecuted: 0,
            executionCount: 0,
            enabled: true
        });
        emit StrategyConfigured(tokenId, threshold);
    }

    function execute(uint256 tokenId) external {
        INonFungibleAgents.AgentState memory state = nfa.getAgentState(tokenId);
        require(state.active, "Agent not active");

        StrategyConfig storage config = strategies[tokenId];
        require(config.enabled, "Strategy not enabled");
        require(
            block.timestamp >= config.lastExecuted + config.threshold,
            "Too soon"
        );

        // Execute strategy logic here
        // This is where you'd interact with DeFi protocols, oracles, etc.

        config.lastExecuted = block.timestamp;
        config.executionCount++;

        emit StrategyExecuted(tokenId, block.timestamp);
    }

    function disable(uint256 tokenId) external onlyAgentOwner(tokenId) {
        strategies[tokenId].enabled = false;
    }
}
```

### Pattern: Request Router

A logic contract that forwards incoming requests to specialized handlers:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./INonFungibleAgents.sol";

contract RouterLogic {
    INonFungibleAgents public immutable nfa;

    mapping(bytes4 => address) public handlers;
    address public admin;

    event RequestRouted(uint256 indexed tokenId, bytes4 selector, address handler);

    constructor(address _nfa) {
        nfa = INonFungibleAgents(_nfa);
        admin = msg.sender;
    }

    function registerHandler(bytes4 selector, address handler) external {
        require(msg.sender == admin, "Not admin");
        require(handler.code.length > 0, "Handler must be contract");
        handlers[selector] = handler;
    }

    function route(uint256 tokenId, bytes4 selector, bytes calldata data) external returns (bytes memory) {
        INonFungibleAgents.AgentState memory state = nfa.getAgentState(tokenId);
        require(state.active, "Agent not active");

        address handler = handlers[selector];
        require(handler != address(0), "No handler registered");

        (bool success, bytes memory result) = handler.call(data);
        require(success, "Handler execution failed");

        emit RequestRouted(tokenId, selector, handler);
        return result;
    }
}
```

---

## Deployment and Binding Workflow

### Step 1: Develop the logic contract

Write the logic contract in Solidity. Test thoroughly using Hardhat.

```bash
cd non-fungible-agents-BAP-578
# Create logic contract in contracts/logic/
# Write tests in test/logic/
npm test
```

### Step 2: Deploy the logic contract

Deploy separately from the NFA contract:

```js
const GreeterLogic = await ethers.getContractFactory("GreeterLogic");
const logic = await GreeterLogic.deploy(NFA_CONTRACT_ADDRESS);
await logic.waitForDeployment();
console.log("Logic deployed at:", await logic.getAddress());
```

### Step 3: Verify on block explorer

Verify the logic contract source code so anyone can review it:

```bash
npx hardhat verify --network bscTestnet LOGIC_ADDRESS NFA_CONTRACT_ADDRESS
```

### Step 4: Bind to agent

The token owner calls `setLogicAddress`:

```js
const nfa = await ethers.getContractAt("NonFungibleAgents", NFA_ADDRESS);
await nfa.setLogicAddress(tokenId, LOGIC_ADDRESS);
```

### Step 5: Interact with the logic

```js
const logic = await ethers.getContractAt("GreeterLogic", LOGIC_ADDRESS);
const greeting = await logic.greet(tokenId);
console.log(greeting);
```

---

## Security Considerations

### What logic contracts CAN do

- Read agent state and metadata from the NFA contract (public view functions)
- Maintain their own state
- Interact with other contracts (DeFi protocols, oracles, etc.)
- Emit events
- Receive and send ETH/BNB (if designed to)

### What logic contracts CANNOT do (by default)

- Withdraw from agent balance (only token owner via NFA contract)
- Transfer the agent token (only token owner or approved)
- Modify agent metadata (only token owner via NFA contract)
- Pause or unpause the NFA contract (only contract owner)

### Security checklist for logic contracts

- [ ] Source code is verified on block explorer
- [ ] No external calls to untrusted contracts without validation
- [ ] No self-destruct pattern (prevents permanent loss)
- [ ] Ownership checks reference the NFA contract's token ownership
- [ ] No hidden admin functions that could manipulate state
- [ ] Events emitted for all state-changing actions
- [ ] Reentrancy guards on functions that send BNB
- [ ] No upgradeable proxy unless explicitly required and documented
- [ ] Gas limits considered for all loops and external calls

### Risk assessment framework

Before binding a logic contract, evaluate:

1. **Source availability** — is the code open and verified?
2. **Audit status** — has it been reviewed by security professionals?
3. **Permissions** — what can this contract actually do?
4. **Upgadeability** — can the logic contract be changed after binding?
5. **Dependencies** — does it call other contracts that could be compromised?
6. **Fund exposure** — can it move BNB or tokens on behalf of the agent?

---

## Logic Contract Marketplace (Future)

A marketplace for logic contracts would allow:

- **Discovery** — browse available logic contracts by category
- **Verification** — verified source, audit status, usage statistics
- **One-click binding** — bind a marketplace logic contract to your agent
- **Reviews** — user ratings and reviews of logic contracts
- **Revenue sharing** — logic contract developers earn fees

Categories:
- DeFi strategies (yield farming, rebalancing)
- Social (agent-to-agent messaging, reputation)
- Automation (scheduled tasks, event responses)
- Analytics (on-chain monitoring, alerts)
- Integration (bridge connectors, API proxies)

---

## Common Patterns and Anti-Patterns

### Do: Read-only logic for information agents

Logic contracts that only read state are inherently safe. They cannot modify anything and carry minimal risk.

### Do: Use ownership checks that reference the NFA contract

```solidity
modifier onlyAgentOwner(uint256 tokenId) {
    require(msg.sender == nfa.getAgentState(tokenId).owner, "Not owner");
    _;
}
```

### Don't: Allow arbitrary external calls

```solidity
// DANGEROUS — allows calling any contract with any data
function execute(address target, bytes calldata data) external {
    target.call(data);
}
```

### Don't: Store agent funds in the logic contract

Agent funds should stay in the NFA contract. If the logic contract holds funds, a bug or exploit in the logic contract could cause loss.

### Do: Emit events for every action

Events are the audit trail. Every meaningful action in the logic contract should emit an event with relevant parameters.

---

## Method-Agnostic AI Integration via Logic Contracts

BAP-578's specification defines logic contracts as the **learning module layer** — the interface through which agents connect to AI systems. The standard provides infrastructure without prescribing specific implementations:

### RAG (Retrieval-Augmented Generation) Pattern

The logic contract queries the agent's vault content to provide context for AI generation:

```solidity
interface IRAGLogic {
    function retrieveContext(uint256 tokenId, string calldata query) external view returns (string memory);
    function generateWithContext(uint256 tokenId, string calldata query) external returns (string memory);
}
```

Implementation: Logic contract reads `vaultURI` from agent metadata, fetches relevant documents, and passes them as context to an AI model via oracle or off-chain service.

### MCP (Model Context Protocol) Pattern

The logic contract routes agent interactions to different AI providers:

```solidity
interface IMCPLogic {
    function routeToProvider(uint256 tokenId, string calldata input, string calldata provider) external returns (bytes memory);
    function getAvailableProviders() external view returns (string[] memory);
}
```

Implementation: Logic contract acts as a router, forwarding requests to registered AI service endpoints and returning structured responses.

### Merkle Tree Learning Module

The logic contract manages the agent's learning tree and updates the on-chain Merkle root:

```solidity
interface ILearningLogic {
    function processInteraction(uint256 tokenId, bytes calldata interactionData) external returns (bytes32 newLearningNode);
    function updateMerkleRoot(uint256 tokenId, bytes32 newRoot, bytes32[] calldata proof) external;
    function verifyLearning(uint256 tokenId, bytes32 leaf, bytes32[] calldata proof) external view returns (bool);
    function queryKnowledge(uint256 tokenId, string calldata query) external view returns (bytes memory);
}
```

The learning pipeline: `interaction → learning extraction → tree building → Merkle root → on-chain update via updateAgentMetadata`.

### Reinforcement Learning Pattern

The logic contract stores reward signals and outcome data:

```solidity
interface IRLLogic {
    function recordOutcome(uint256 tokenId, bytes32 actionId, int256 reward) external;
    function getRecommendation(uint256 tokenId, bytes calldata context) external view returns (bytes memory);
}
```

### Hybrid Pattern

Combine multiple approaches in a single logic contract:

```solidity
contract HybridLearningLogic is IRAGLogic, ILearningLogic, IRLLogic {
    // RAG for knowledge retrieval
    // Merkle tree for verifiable learning state
    // RL for action optimization
    // All behind the single logicAddress binding
}
```

---

## Output Format

When asked for logic contract help, respond with:

1. **Behavior goal** (what should the agent do?)
2. **Contract architecture** (interfaces, state, functions)
3. **Complete Solidity code** (compilable, with comments)
4. **Security constraints** (what to check before binding)
5. **Deployment steps** (compile, deploy, verify, bind)
6. **Testing guidance** (what to test and expected outcomes)

---

## Related Skills

- `bap578`
- `bap578-security-audit`
- `bap578-upgrade`
