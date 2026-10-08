---
name: randomness
description: >
  Auto-loaded by logic-auditor agent during Phase 2.
  Provides detection patterns for: block.timestamp/blockhash misuse, predictable
  randomness, Chainlink VRF integration, commit-reveal schemes, RANDAO on L2.
  Core artifact: Randomness Source Analysis.
user-invocable: false
---

# Insecure Randomness Vulnerability Analysis

**OWASP SC09:2025** - Insecure Randomness allows attackers to predict or manipulate "random" outcomes for profit.

**2025-2026 Statistics**: Randomness exploits caused $85M+ in losses, with NFT mint exploits and lottery manipulations being the most common vectors.

---

## Why Randomness Fails (Root Causes)

### Root Cause 1: On-Chain Data is Public

Everything on-chain is visible to everyone, including miners/validators.

```solidity
// VULNERABLE: Uses public blockchain data
function roll() external returns (uint256) {
    return uint256(keccak256(abi.encodePacked(
        block.timestamp,      // @audit Miner controls this
        block.difficulty,     // @audit Known before execution
        msg.sender           // @audit Attacker controls this
    ))) % 100;
}
```

**Attacker's view**: "I can simulate this off-chain and only submit when I win."

### Root Cause 2: Miner/Validator Control

Block proposers control block.timestamp and can reorder transactions.

```solidity
// VULNERABLE: Miner can manipulate
function lottery() external {
    require(block.timestamp % 10 == 0);  // @audit Miner waits for favorable timestamp
    winner = msg.sender;
}
```

### Root Cause 3: Predictable Future State

Using future blockhash that can be predicted or influenced.

```solidity
// VULNERABLE: Blockhash only available for 256 blocks
function reveal(uint256 commitBlock) external {
    require(block.number > commitBlock + 10);
    uint256 random = uint256(blockhash(commitBlock + 10));  // @audit Returns 0 after 256 blocks!
}
```

### Root Cause 4: Single-Transaction Exploitation

Randomness generated and used in same transaction can be front-run or simulated.

```solidity
// VULNERABLE: Same-tx randomness
function mint() external {
    uint256 tokenId = uint256(keccak256(abi.encodePacked(block.timestamp, totalSupply)));
    _mint(msg.sender, tokenId);
    // @audit Attacker simulates result, only mints if rare
}
```

---

## The Randomness Source Analysis (Core Artifact)

For each randomness usage, document:

| Function | Source | Controller | Predictability | Attack Vector |
|----------|--------|------------|----------------|---------------|
| lottery() | block.timestamp | Miner | 100% | Miner manipulation |
| roll() | blockhash | Anyone | 100% | Off-chain simulation |
| mint() | tx + state | Attacker | 100% | Selective execution |
| draw() | VRF | None | 0% | Secure |

---

## Detection Patterns

### Pattern 1: block.timestamp as Randomness

**Root Cause**: Miner/Validator Control

```solidity
// VULNERABLE: Timestamp is miner-controllable
function randomize() public view returns (uint256) {
    return uint256(keccak256(abi.encodePacked(block.timestamp))) % 100;
}

function flipCoin() external {
    if (uint256(block.timestamp) % 2 == 0) {  // @audit Binary outcome, easily manipulated
        _winner(msg.sender);
    }
}
```

**Attack Flow**:
1. Attacker (or colluding validator) sees pending lottery
2. Adjusts block.timestamp within allowed range (~15 seconds)
3. Picks timestamp that gives winning result
4. Profits from "random" outcome

**Search Queries**:
```
Grep("block\\.timestamp.*%|block\\.timestamp.*random", glob="**/*.sol")
Grep("keccak256.*block\\.timestamp", glob="**/*.sol")
```

### Pattern 2: blockhash Exploitation

**Root Cause**: Predictable Future State

```solidity
// VULNERABLE: blockhash is predictable and limited
function getRandomNumber(uint256 blockNumber) public view returns (uint256) {
    return uint256(blockhash(blockNumber));
    // @audit blockhash(block.number) = 0
    // @audit blockhash(block.number - 257) = 0 (expired)
}

// VULNERABLE: Future blockhash commit scheme
mapping(address => uint256) public commitBlock;

function commit() external {
    commitBlock[msg.sender] = block.number;
}

function reveal() external {
    uint256 bn = commitBlock[msg.sender];
    require(block.number > bn + 10, "Too early");
    uint256 random = uint256(blockhash(bn + 10));  // @audit Returns 0 after 256 blocks!
    // ...
}
```

**Attack Flow**:
1. Attacker commits
2. Waits 257 blocks
3. blockhash returns 0
4. Outcome becomes deterministic

**Search Queries**:
```
Grep("blockhash\\(|block\\.prevrandao", glob="**/*.sol")
Grep("block\\.number.*\\-.*256|block\\.number.*>.*256", glob="**/*.sol")
```

### Pattern 3: prevrandao (RANDAO) Misuse

**Root Cause**: Validator can bias RANDAO

```solidity
// DANGEROUS on L1, CRITICAL on L2
function getRandomFromPrevrandao() public view returns (uint256) {
    return block.prevrandao;  // @audit On L2, sequencer fully controls this!
}
```

**L1 vs L2 Differences**:

| Chain | prevrandao Behavior | Manipulation Risk |
|-------|---------------------|-------------------|
| Ethereum L1 | RANDAO mixing | Low (but biasable) |
| Arbitrum | L1 block hash | Medium |
| Optimism | L1 block hash | Medium |
| Base | L1 block hash | Medium |
| zkSync | Sequencer controlled | **CRITICAL** |

**Search Queries**:
```
Grep("block\\.prevrandao|block\\.difficulty", glob="**/*.sol")
Grep("PREVRANDAO|RANDAO", glob="**/*.sol")
```

### Pattern 4: msg.sender/tx.origin in Randomness

**Root Cause**: Attacker Controls Input

```solidity
// VULNERABLE: Attacker controls msg.sender
function random() public view returns (uint256) {
    return uint256(keccak256(abi.encodePacked(
        msg.sender,  // @audit Attacker generates addresses until favorable
        block.number
    )));
}
```

**Attack Flow**:
1. Attacker generates many addresses
2. Simulates random() for each
3. Uses address that gives winning result
4. Deploys contract from that address or uses that EOA

**Search Queries**:
```
Grep("keccak256.*msg\\.sender|msg\\.sender.*random", glob="**/*.sol")
Grep("tx\\.origin.*random|random.*tx\\.origin", glob="**/*.sol")
```

### Pattern 5: Single-Transaction NFT Rarity Exploitation

**Root Cause**: Same-tx randomness is simulatable

```solidity
// VULNERABLE: Rarity determined at mint time
function mint() external payable {
    uint256 tokenId = totalSupply + 1;
    uint256 random = uint256(keccak256(abi.encodePacked(
        tokenId, block.timestamp, msg.sender
    )));
    
    if (random % 100 < 5) {
        _mintLegendary(msg.sender, tokenId);  // @audit 5% chance, attackers ONLY mint these
    } else {
        _mintCommon(msg.sender, tokenId);
    }
}
```

**Attack Flow**:
1. Attacker deploys contract
2. Contract simulates mint result
3. Only executes if legendary
4. Reverts otherwise (wasting only gas)
5. Attacker mints only rare NFTs

**Search Queries**:
```
Grep("mint.*random|random.*mint|rarity|legendary", glob="**/*.sol")
Grep("keccak256.*totalSupply|keccak256.*tokenId", glob="**/*.sol")
```

---

## Secure Randomness Patterns

### Pattern 1: Chainlink VRF v2.5

```solidity
import "@chainlink/contracts/src/v0.8/vrf/VRFConsumerBaseV2Plus.sol";

contract SecureLottery is VRFConsumerBaseV2Plus {
    uint256 private requestId;
    mapping(uint256 => address) public requestToPlayer;
    
    function enterLottery() external payable {
        // Request randomness
        requestId = s_vrfCoordinator.requestRandomWords(
            VRFV2PlusClient.RandomWordsRequest({
                keyHash: keyHash,
                subId: subscriptionId,
                requestConfirmations: 3,
                callbackGasLimit: 100000,
                numWords: 1,
                extraArgs: VRFV2PlusClient._argsToBytes(
                    VRFV2PlusClient.ExtraArgsV1({nativePayment: false})
                )
            })
        );
        requestToPlayer[requestId] = msg.sender;
    }
    
    function fulfillRandomWords(
        uint256 _requestId,
        uint256[] calldata randomWords
    ) internal override {
        // Use randomWords[0] for lottery
        address player = requestToPlayer[_requestId];
        uint256 result = randomWords[0] % 100;
        // ...
    }
}
```

### Pattern 2: Commit-Reveal Scheme

```solidity
contract CommitReveal {
    mapping(address => bytes32) public commits;
    mapping(address => uint256) public commitBlock;
    
    function commit(bytes32 hash) external {
        commits[msg.sender] = hash;
        commitBlock[msg.sender] = block.number;
    }
    
    function reveal(uint256 secret) external {
        require(block.number > commitBlock[msg.sender] + 10, "Too early");
        require(block.number < commitBlock[msg.sender] + 256, "Too late");
        require(keccak256(abi.encodePacked(secret)) == commits[msg.sender], "Bad reveal");
        
        // Combine secret with future blockhash
        uint256 random = uint256(keccak256(abi.encodePacked(
            secret,
            blockhash(commitBlock[msg.sender] + 10)
        )));
        
        delete commits[msg.sender];
        // Use random...
    }
}
```

### Pattern 3: Multiple Party Randomness (RANDAO-style)

```solidity
contract MultiPartyRandom {
    mapping(address => bytes32) public commits;
    mapping(address => uint256) public reveals;
    address[] public participants;
    
    function commit(bytes32 hash) external {
        commits[msg.sender] = hash;
        participants.push(msg.sender);
    }
    
    function reveal(uint256 secret) external {
        require(keccak256(abi.encodePacked(secret)) == commits[msg.sender]);
        reveals[msg.sender] = secret;
    }
    
    function finalize() external returns (uint256) {
        uint256 combined;
        for (uint i = 0; i < participants.length; i++) {
            combined ^= reveals[participants[i]];
        }
        return combined;
        // One honest participant = unbiased randomness
    }
}
```

---

## Randomness Audit Checklist

### Source Analysis
- [ ] No block.timestamp for randomness
- [ ] No blockhash for critical randomness
- [ ] No msg.sender in random seed
- [ ] No same-tx random generation + use

### VRF Integration (if applicable)
- [ ] Correct VRF version (v2.5 recommended)
- [ ] Adequate confirmations
- [ ] Request ID properly tracked
- [ ] Fulfillment properly validated

### Commit-Reveal (if applicable)
- [ ] Commit before reveal enforced
- [ ] Time bounds prevent blockhash expiry
- [ ] Secret properly validated
- [ ] Cannot reveal early

### L2 Considerations
- [ ] prevrandao not used on L2
- [ ] Sequencer manipulation considered
- [ ] Alternative randomness for L2

---

## Search Query Reference

```
# Find randomness sources
Grep("block\\.timestamp|block\\.number|blockhash", glob="**/*.sol")
Grep("block\\.prevrandao|block\\.difficulty", glob="**/*.sol")
Grep("keccak256.*abi\\.encodePacked", glob="**/*.sol")

# Find VRF usage
Grep("VRF|requestRandomWords|fulfillRandomWords", glob="**/*.sol")
Grep("Chainlink|randomness", glob="**/*.sol")

# Find commit-reveal
Grep("commit|reveal|hash.*secret", glob="**/*.sol")

# Find lottery/gaming
Grep("lottery|random|dice|flip|roll|mint.*rare", glob="**/*.sol")
```

---

## Severity Classification

### Critical
- Lottery/raffle outcome predictable
- NFT rarity manipulation possible
- High-value randomness exploitable

### High
- Partial randomness bias possible
- Commit-reveal timing exploitable
- VRF integration flawed

### Medium
- Low-value randomness biasable
- Minor outcome manipulation
- Missing commit-reveal validation

---

## Rationalization Table (Reject These Excuses)

| Excuse | Reality |
|--------|---------|
| "It's random enough" | If predictable, it's NOT random. Attackers will exploit. |
| "Nobody will notice" | MEV bots simulate every transaction. They WILL notice. |
| "Gas cost prevents exploitation" | $100 gas vs $10,000 lottery. Math is obvious. |
| "We use multiple inputs" | If all inputs are predictable, combination is predictable. |
| "It's just for fun" | Real money = real attacks. Even games get exploited. |
| "VRF is expensive" | $0.25 per request vs millions in losses. Worth it. |
| "L2 is the same as L1" | Sequencers have FULL control. Assume worst case. |
