---
name: LayerZero Integration Patterns
description: >
  Auto-loaded by cross-chain-auditor agent during Phase 2 when LayerZero is detected.
  Provides patterns for: OApp security (peer validation), OFT tokens (slippage),
  compose message validation, gas options. Critical: missing peer check, wrong
  peer encoding, no compose validation, insufficient executor gas.
user-invocable: false
---

# LayerZero Integration Patterns

This skill provides comprehensive knowledge for auditing LayerZero integrations.

## LayerZero V2 Architecture

| Component | Purpose |
|-----------|---------|
| Endpoint | Entry point for sending/receiving |
| OApp | Omnichain Application base |
| OFT | Omnichain Fungible Token |
| DVN | Decentralized Verifier Network |
| Executor | Message delivery |

---

## OApp Security Patterns

### Standard Receiver Implementation

```solidity
import { OApp, Origin } from "@layerzerolabs/lz-evm-oapp-v2/contracts/oapp/OApp.sol";

contract MyOApp is OApp {
    constructor(
        address _endpoint,
        address _delegate
    ) OApp(_endpoint, _delegate) {}

    function _lzReceive(
        Origin calldata _origin,
        bytes32 _guid,
        bytes calldata _message,
        address _executor,
        bytes calldata _extraData
    ) internal override {
        // CRITICAL: Validate source chain
        require(
            peers[_origin.srcEid] != bytes32(0),
            "Peer not set"
        );

        // CRITICAL: Validate source address
        require(
            _origin.sender == peers[_origin.srcEid],
            "Invalid sender"
        );

        // Process message
        _processMessage(_message);
    }
}
```

### Required Security Checks

| Check | Location | Risk if Missing |
|-------|----------|-----------------|
| Peer validation | `_lzReceive` | Accept forged messages |
| Chain validation | `_lzReceive` | Cross-chain injection |
| GUID uniqueness | Optional | Replay attacks |
| Compose validation | `_lzCompose` | Malicious compose calls |

---

## OFT (Omnichain Fungible Token) Security

### Standard OFT Pattern

```solidity
import { OFT } from "@layerzerolabs/lz-evm-oapp-v2/contracts/oft/OFT.sol";

contract MyOFT is OFT {
    constructor(
        string memory _name,
        string memory _symbol,
        address _lzEndpoint,
        address _delegate
    ) OFT(_name, _symbol, _lzEndpoint, _delegate) {}

    // Verify amount received
    function _debit(
        address _from,
        uint256 _amountLD,
        uint256 _minAmountLD,
        uint32 _dstEid
    ) internal override returns (uint256 amountSentLD, uint256 amountReceivedLD) {
        // Standard debit with slippage protection
        (amountSentLD, amountReceivedLD) = super._debit(
            _from,
            _amountLD,
            _minAmountLD,
            _dstEid
        );

        // Custom validation if needed
        require(amountReceivedLD >= _minAmountLD, "Slippage exceeded");
    }
}
```

### OFT Vulnerabilities

**1. Missing Slippage Protection**
```solidity
// DANGEROUS: No minimum amount check
function send(
    uint32 _dstEid,
    bytes32 _to,
    uint256 _amountLD,
    bytes calldata _options
) external payable {
    // No minAmountLD protection!
    _send(_dstEid, _to, _amountLD, _options);
}

// SECURE: Include minimum
function send(
    uint32 _dstEid,
    bytes32 _to,
    uint256 _amountLD,
    uint256 _minAmountLD, // Add this!
    bytes calldata _options
) external payable {
    require(_minAmountLD > 0, "Set minimum");
    _send(_dstEid, _to, _amountLD, _minAmountLD, _options);
}
```

**2. Decimal Conversion Issues**
```solidity
// LayerZero uses shared decimals (usually 6)
// Local token might have 18 decimals

// DANGEROUS: Precision loss on small amounts
uint256 sharedDecimals = 6;
uint256 localDecimals = 18;
uint256 decimalConversionRate = 10 ** (localDecimals - sharedDecimals);

// Amount like 0.000001 tokens becomes 0 in shared format!
```

---

## Peer Configuration Security

### Trusted Peer Setup

```solidity
// Only owner can set peers
function setPeer(
    uint32 _eid,
    bytes32 _peer
) public override onlyOwner {
    peers[_eid] = _peer;
    emit PeerSet(_eid, _peer);
}

// Peer format: bytes32(uint256(uint160(address)))
// Ensure address is padded correctly!
```

### Peer Validation Vulnerabilities

**1. Missing Peer Check**
```solidity
// DANGEROUS: Accepts from anyone
function _lzReceive(
    Origin calldata _origin,
    bytes32 _guid,
    bytes calldata _message,
    address _executor,
    bytes calldata _extraData
) internal override {
    // Missing peer validation!
    _process(_message);
}
```

**2. Incorrect Peer Encoding**
```solidity
// DANGEROUS: Wrong encoding
bytes32 peer = bytes32(abi.encodePacked(remoteAddress)); // Wrong!

// CORRECT: Proper padding
bytes32 peer = bytes32(uint256(uint160(remoteAddress)));
```

---

## Compose Message Security

### Compose Pattern

```solidity
import { OAppComposer } from "@layerzerolabs/lz-evm-oapp-v2/contracts/oapp/OAppComposer.sol";

contract MyComposer is OAppComposer {
    function _lzCompose(
        address _oApp,
        bytes32 _guid,
        bytes calldata _message,
        address _executor,
        bytes calldata _extraData
    ) internal override {
        // CRITICAL: Validate compose source
        require(_oApp == trustedOApp, "Invalid OApp");

        // Process composed message
        _handleCompose(_message);
    }
}
```

### Compose Vulnerabilities

**1. Missing OApp Validation**
```solidity
// DANGEROUS: Accepts compose from any OApp
function _lzCompose(
    address _oApp,
    bytes32 _guid,
    bytes calldata _message,
    address _executor,
    bytes calldata _extraData
) internal override {
    // No _oApp validation!
    _processCompose(_message);
}
```

---

## Gas & Options Security

### Options Encoding

```solidity
import { OptionsBuilder } from "@layerzerolabs/lz-evm-oapp-v2/contracts/oapp/libs/OptionsBuilder.sol";

using OptionsBuilder for bytes;

// Build options with sufficient gas
bytes memory options = OptionsBuilder
    .newOptions()
    .addExecutorLzReceiveOption(200000, 0) // Gas limit
    .addExecutorNativeDropOption(1 ether, receiver); // Native drop

// Send with options
endpoint.send{value: fee}(
    dstEid,
    message,
    options,
    MessagingFee(fee, 0),
    payable(msg.sender)
);
```

### Gas Vulnerabilities

**1. Insufficient Executor Gas**
```solidity
// DANGEROUS: May fail on destination
bytes memory options = OptionsBuilder
    .newOptions()
    .addExecutorLzReceiveOption(50000, 0); // Too low!

// RECOMMENDED: Calculate based on callback complexity
uint128 gasForCallback = 200000; // Sufficient for your _lzReceive
```

---

## LayerZero Audit Checklist

### OApp Security
- [ ] Peer validation in `_lzReceive`
- [ ] Source chain (srcEid) validated
- [ ] Source sender validated against peer
- [ ] GUID tracked if replay protection needed
- [ ] Compose source validated in `_lzCompose`

### OFT Security
- [ ] Slippage protection implemented
- [ ] Decimal conversion correct
- [ ] Minimum amounts enforced
- [ ] Shared decimals configured correctly

### Configuration
- [ ] Peers set correctly (proper encoding)
- [ ] DVN/Executor configured appropriately
- [ ] Fee estimation correct
- [ ] Gas limits sufficient

### Edge Cases
- [ ] Message failure handling
- [ ] Stuck message recovery
- [ ] Admin key security for peer updates
- [ ] Rate limiting if needed

## Common Vulnerabilities Summary

| Vulnerability | Impact | Detection |
|--------------|--------|-----------|
| Missing peer validation | Message forgery | No `peers[srcEid]` check |
| Wrong peer encoding | Silent failures | `abi.encodePacked` instead of padding |
| No compose validation | Compose injection | No `_oApp` check in `_lzCompose` |
| Insufficient gas | Failed messages | Low gas in options |
| No slippage protection | Value loss | No `minAmountLD` |
