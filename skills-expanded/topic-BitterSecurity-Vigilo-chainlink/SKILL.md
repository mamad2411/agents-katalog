---
name: Chainlink Integration Patterns
description: >
  Auto-loaded by oracle-auditor agent during Phase 2 when Chainlink is detected.
  Provides patterns for: Price Feeds (stale check, decimals), VRF (front-running),
  CCIP (message validation), Automation/Keepers. Critical: missing staleness check,
  wrong decimals, sequencer down handling.
user-invocable: false
---

# Chainlink Integration Patterns

This skill provides comprehensive knowledge for auditing Chainlink service integrations.

## Chainlink Services Overview

| Service | Purpose | Key Risks |
|---------|---------|-----------|
| Price Feeds | Oracle data | Stale prices, manipulation |
| VRF | Random numbers | Front-running, reorg attacks |
| CCIP | Cross-chain | Message validation |
| Automation | Keepers | Timing assumptions |
| Functions | Off-chain compute | Trust assumptions |

---

## Price Feed Integration

### Standard Integration Pattern

```solidity
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract PriceFeedConsumer {
    AggregatorV3Interface internal priceFeed;
    uint256 public constant HEARTBEAT = 3600; // 1 hour

    constructor(address feedAddress) {
        priceFeed = AggregatorV3Interface(feedAddress);
    }

    function getLatestPrice() public view returns (int256) {
        (
            uint80 roundId,
            int256 price,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        // Validation checks
        require(price > 0, "Invalid price");
        require(updatedAt > 0, "Round not complete");
        require(updatedAt >= block.timestamp - HEARTBEAT, "Stale price");
        require(answeredInRound >= roundId, "Stale round");

        return price;
    }
}
```

### Required Validations

| Check | Code | Risk if Missing |
|-------|------|-----------------|
| Zero price | `require(price > 0)` | Division by zero, wrong valuations |
| Freshness | `require(updatedAt >= block.timestamp - HEARTBEAT)` | Stale price exploitation |
| Round complete | `require(answeredInRound >= roundId)` | Incomplete data |
| Negative price | `require(price > 0)` | Wrap-around issues |

### L2 Sequencer Uptime Feed

```solidity
// REQUIRED for Arbitrum, Optimism, Base deployments
AggregatorV3Interface internal sequencerUptimeFeed;
uint256 public constant GRACE_PERIOD = 3600; // 1 hour

function getLatestPrice() public view returns (int256) {
    // Check sequencer first
    (, int256 answer,, uint256 startedAt,) =
        sequencerUptimeFeed.latestRoundData();

    // answer == 0: Sequencer is up
    // answer == 1: Sequencer is down
    bool isSequencerUp = answer == 0;
    require(isSequencerUp, "Sequencer down");

    // Grace period after sequencer comes back up
    uint256 timeSinceUp = block.timestamp - startedAt;
    require(timeSinceUp > GRACE_PERIOD, "Grace period active");

    // Now get price
    return _getPrice();
}
```

### Heartbeat Reference

| Feed | Heartbeat | Deviation |
|------|-----------|-----------|
| ETH/USD | 3600s | 0.5% |
| BTC/USD | 3600s | 0.5% |
| USDC/USD | 86400s | 0.1% |
| DAI/USD | 3600s | 0.25% |

---

## VRF V2 Integration

### Standard Pattern

```solidity
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";

contract VRFConsumer is VRFConsumerBaseV2 {
    VRFCoordinatorV2Interface COORDINATOR;

    uint64 s_subscriptionId;
    bytes32 keyHash;
    uint32 callbackGasLimit = 100000;
    uint16 requestConfirmations = 3; // Minimum for mainnet
    uint32 numWords = 1;

    mapping(uint256 => address) public requestIdToSender;
    mapping(uint256 => uint256) public requestIdToRandomWord;

    function requestRandomWords() external returns (uint256 requestId) {
        requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        requestIdToSender[requestId] = msg.sender;
        return requestId;
    }

    function fulfillRandomWords(
        uint256 requestId,
        uint256[] memory randomWords
    ) internal override {
        // Use randomWords[0] for result
        requestIdToRandomWord[requestId] = randomWords[0];
        // Process result...
    }
}
```

### VRF Security Checklist

| Check | Risk if Missing |
|-------|-----------------|
| Sufficient confirmations | Reorg attacks |
| requestId to user mapping | Wrong user gets result |
| Callback gas limit | DoS if too low |
| No state prediction | Front-running |
| Subscription funded | Failed requests |

### VRF Vulnerabilities

**1. Request Front-Running**
```solidity
// DANGEROUS: User can see result and decide
function play() external {
    uint256 requestId = requestRandomWords();
    // User can front-run fulfillment if they see result
}

// SECURE: Commit-reveal pattern
function commit(bytes32 commitment) external {
    commitments[msg.sender] = commitment;
}

function reveal(bytes32 secret) external {
    require(keccak256(abi.encode(secret)) == commitments[msg.sender]);
    // Request VRF
}
```

**2. Insufficient Confirmations**
```solidity
// DANGEROUS on chains with reorgs
uint16 requestConfirmations = 1; // Too low!

// RECOMMENDED
uint16 requestConfirmations = 3; // Mainnet minimum
// Higher for chains with frequent reorgs
```

---

## CCIP Integration

### Message Receiving

```solidity
import {CCIPReceiver} from "@chainlink/contracts-ccip/src/v0.8/ccip/applications/CCIPReceiver.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";

contract CCIPReceiverExample is CCIPReceiver {
    mapping(uint64 => bool) public allowlistedSourceChains;
    mapping(address => bool) public allowlistedSenders;

    function _ccipReceive(
        Client.Any2EVMMessage memory message
    ) internal override {
        // CRITICAL: Validate source chain
        require(
            allowlistedSourceChains[message.sourceChainSelector],
            "Source chain not allowlisted"
        );

        // CRITICAL: Validate sender
        address sender = abi.decode(message.sender, (address));
        require(
            allowlistedSenders[sender],
            "Sender not allowlisted"
        );

        // Process message
        _processMessage(message.data);
    }
}
```

### CCIP Security Checklist

- [ ] Source chain selector validated
- [ ] Sender address validated
- [ ] Message replay protection
- [ ] Proper error handling
- [ ] Fee payment configured

---

## Automation (Keepers)

### Standard Pattern

```solidity
import "@chainlink/contracts/src/v0.8/interfaces/AutomationCompatibleInterface.sol";

contract AutomationExample is AutomationCompatibleInterface {
    uint256 public lastTimeStamp;
    uint256 public interval = 3600; // 1 hour

    function checkUpkeep(bytes calldata)
        external
        view
        override
        returns (bool upkeepNeeded, bytes memory performData)
    {
        upkeepNeeded = (block.timestamp - lastTimeStamp) > interval;
        return (upkeepNeeded, "");
    }

    function performUpkeep(bytes calldata) external override {
        // Re-validate condition (important!)
        require(
            (block.timestamp - lastTimeStamp) > interval,
            "Upkeep not needed"
        );

        lastTimeStamp = block.timestamp;
        // Perform action...
    }
}
```

### Automation Vulnerabilities

**1. Missing Re-validation**
```solidity
// DANGEROUS: Anyone can call, no validation
function performUpkeep(bytes calldata) external override {
    // Missing re-validation!
    _doExpensiveOperation();
}

// SECURE: Re-validate in performUpkeep
function performUpkeep(bytes calldata) external override {
    require(needsUpkeep(), "Not needed");
    _doExpensiveOperation();
}
```

---

## Common Chainlink Vulnerabilities Summary

| Service | Vulnerability | Detection Pattern |
|---------|--------------|-------------------|
| Price Feed | Missing freshness check | No `updatedAt` validation |
| Price Feed | L2 sequencer not checked | No sequencer feed on L2 |
| VRF | Front-runnable | No commit-reveal |
| VRF | Low confirmations | `requestConfirmations < 3` |
| CCIP | Missing source validation | No chain/sender check |
| Automation | Missing re-validation | No check in `performUpkeep` |

## Audit Checklist

### Price Feeds
- [ ] Price > 0 checked
- [ ] Freshness validated with correct heartbeat
- [ ] Round completeness checked
- [ ] L2 sequencer checked (if applicable)
- [ ] Decimals handled correctly

### VRF
- [ ] Sufficient confirmations (>= 3)
- [ ] Request ID mapped correctly
- [ ] Callback gas limit adequate
- [ ] Subscription funded
- [ ] No result prediction possible

### CCIP
- [ ] Source chain validated
- [ ] Sender address validated
- [ ] Replay protection present
- [ ] Error handling implemented
