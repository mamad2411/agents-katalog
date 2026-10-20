---
description: Run Web3 Security and Smart Contract Standards Check
globs: ['**/contracts/**/*.sol', '**/web3/**/*.ts', '**/blockchain/**/*.ts', 'hardhat.config.js']
---

# Security: Web3 & Smart Contract Security Standards

<audit_rules>

- You MUST implement proper smart contract security patterns including reentrancy protection and overflow checks.
- You MUST use established libraries like OpenZeppelin for common functionality (ERC20, ERC721, access control).
- You MUST implement proper access control with role-based permissions for contract functions.
- You MUST ensure all external calls are handled safely with checks-effects-interactions pattern.
- You MUST implement proper input validation and sanitization for all contract functions.
- You MUST configure proper gas optimization to prevent DoS attacks and high transaction costs.
- You MUST implement proper event logging for transparency and off-chain integration.
- You MUST ensure contracts are upgradeable safely using proxy patterns when needed.
- You MUST implement proper oracle security for external data feeds.
- You MUST conduct thorough smart contract testing including edge cases and attack vectors.
  </audit_rules>

<example_good>

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract SecureToken is ERC20, AccessControl, ReentrancyGuard, Pausable {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    // Gas optimization: pack structs
    struct Transaction {
        uint128 amount;     // 16 bytes
        uint64 timestamp;   // 8 bytes
        uint32 nonce;       // 4 bytes
        address recipient;  // 20 bytes
    }

    mapping(address => uint256) private _nonces;
    mapping(address => Transaction[]) private _transactions;

    uint256 private constant MAX_TRANSACTIONS_PER_USER = 100;
    uint256 private constant MAX_AMOUNT = 1000000 * 10**18;

    event TokensMinted(address indexed to, uint256 amount);
    event TokensBurned(address indexed from, uint256 amount);
    event TransactionAdded(address indexed user, uint256 amount, uint256 timestamp);

    constructor() ERC20("SecureToken", "SEC") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
    }

    function mint(address to, uint256 amount)
        public
        onlyRole(MINTER_ROLE)
        whenNotPaused
        nonReentrant
    {
        require(to != address(0), "Invalid address");
        require(amount > 0 && amount <= MAX_AMOUNT, "Invalid amount");

        _mint(to, amount);
        emit TokensMinted(to, amount);
    }

    function burn(uint256 amount)
        public
        whenNotPaused
        nonReentrant
    {
        require(amount > 0 && amount <= balanceOf(msg.sender), "Invalid amount");

        _burn(msg.sender, amount);
        emit TokensBurned(msg.sender, amount);
    }

    function addTransaction(address recipient, uint128 amount)
        external
        whenNotPaused
        nonReentrant
    {
        require(recipient != address(0), "Invalid recipient");
        require(amount > 0, "Invalid amount");
        require(_transactions[msg.sender].length < MAX_TRANSACTIONS_PER_USER, "Too many transactions");

        uint64 timestamp = uint64(block.timestamp);
        uint32 nonce = uint32(_nonces[msg.sender]++);

        Transaction memory transaction = Transaction({
            amount: amount,
            timestamp: timestamp,
            nonce: nonce,
            recipient: recipient
        });

        _transactions[msg.sender].push(transaction);
        emit TransactionAdded(msg.sender, amount, timestamp);
    }

    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }

    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }

    function getTransactions(address user)
        external
        view
        returns (Transaction[] memory)
    {
        return _transactions[user];
    }
}
```

</example_good>

<example_bad>

```solidity
// BAD: Multiple security vulnerabilities
contract InsecureToken {
    mapping(address => uint256) public balances;

    // BAD: No access control
    function mint(address to, uint256 amount) public {
        // BAD: No input validation
        balances[to] += amount; // BAD: Potential overflow
    }

    // BAD: Reentrancy vulnerability
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount);

        // BAD: External call before state update
        (bool success,) = to.call{value: amount}("");
        require(success);

        balances[msg.sender] -= amount;
        balances[to] += amount;
    }

    // BAD: No reentrancy protection
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;

        // BAD: External call can re-enter contract
        (bool success,) = msg.sender.call{value: amount}("");
        require(success);
    }

    // BAD: No event logging
    // BAD: No access control
    // BAD: No pause mechanism
    // BAD: No gas optimization
}
```

</example_bad>
