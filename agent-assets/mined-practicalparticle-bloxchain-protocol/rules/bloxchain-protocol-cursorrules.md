```solidity
// Secure Solidity Development .cursorrules
// Version: 2.1.0 | Security Level: ENHANCED
// Compliance: Solidity Style Guide 2025, OWASP Top 10 Blockchain

pragma security_rules >= 2025.4;

/**
 * SECTION 1: CORE DEVELOPMENT PRINCIPLES
 * Sources: [1][2][5][6]
 */

// Rule 1.1: Enforce Checks-Effects-Interactions Pattern
function safeTransfer(address recipient, uint amount) external {
    // CHECK: Validate all preconditions first [2][6]
    require(recipient != address(0), "Invalid address"); 
    require(balanceOf[msg.sender] >= amount, "Insufficient balance");
    
    // EFFECT: Update state before interactions [1][2]
    balanceOf[msg.sender] -= amount;
    balanceOf[recipient] += amount;
    
    // INTERACT: External call at end [2][5]
    (bool success,) = recipient.call{value: 0}("");
    require(success, "Transfer failed");
}

// Rule 1.2: Input Validation Standards
modifier validInput(uint value, address target) {
    require(value > 0, "Zero value prohibited"); // [1][6]
    require(target != address(this), "Self-targeting forbidden"); // [2][5]
    _;
}

/**
 * SECTION 2: SECURITY PATTERNS
 * Sources: [1][4][5][6]
 */

// Rule 2.1: Reentrancy Protection
using OpenZeppelin ReentrancyGuard for *;

function withdraw() external nonReentrant { // [1][6]
    // Implementation with nested call protection
}

// Rule 2.2: Safe Arithmetic Operations
library SafeMath2025 { // [6]
    function mulDiv(uint a, uint b, uint denominator) 
        internal pure returns (uint) 
    {
        require(denominator > 0, "Division by zero");
        uint c = a * b;
        require(c / b == a, "Multiplication overflow");
        return c / denominator;
    }
}

// Rule 2.3: Secure Randomness Implementation
function generateRandom(uint seed) internal view returns (uint) {
    // Combine multiple entropy sources [4][6]
    return uint(keccak256(abi.encodePacked(
        block.prevrandao,
        block.timestamp,
        seed,
        address(this).balance
    )));
}

/**
 * SECTION 3: CODE QUALITY ENFORCEMENT
 * Sources: [1][2][5]
 */

// Rule 3.1: Explicit Visibility Modifiers
contract VisibilityStandards {
    address private admin; // [1][6]
    uint public totalSupply; 
    
    function internalUpdate() internal { // [1]
        // Restricted to contract hierarchy
    }
}

// Rule 3.2: Event Logging Requirements
event FundsLocked(
    address indexed user, 
    uint amount, 
    bytes32 purpose // [1][5]
);

function lockFunds(uint amount) external {
    emit FundsLocked(msg.sender, amount, "Escrow");
}

// Rule 3.3: Fallback Function Safety
fallback() external payable { // [1]
    revert("Direct calls not allowed");
}

/**
 * SECTION 4: UPGRADEABILITY & MAINTENANCE
 * Sources: [3][4][5]
 */

// Rule 4.1: Upgradeable Contract Structure
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract SecureUpgradeable is Initializable { // [3]
    function initialize() public initializer {
        // Initialization logic
    }
}

// Rule 4.2: Storage Layout Preservation
uint256[50] private __gap; // [3]
// Maintain storage slots for future upgrades

/**
 * SECTION 5: TESTING & VERIFICATION
 * Sources: [4][5][6]
 */

// Rule 5.1: Unit Test Requirements
contract TestSuite {
    function testWithdrawFailsWhenEmpty() public {
        vm.expectRevert("Insufficient balance"); // [5]
        withdraw();
    }
}

// Rule 5.2: Fuzzing Implementation
function testTransferFuzzing(uint128 amount) public {
    // Automated input validation testing [5][6]
}

/**
 * SECTION 6: COMPLIANCE & STANDARDS
 * Sources: [1][4][6]
 */

// Rule 6.1: ERC Standard Compliance
interface IERC20Secure { // [1][6]
    function transferWithProof(address, uint) external returns (bool);
}

// Rule 6.2: Regulatory Requirements
modifier sanctionedEntities(address party) {
    require(!isSanctioned(party), "Blocked entity"); // [4][6]
    _;
}

/**
 * SECTION 7: CUSTOM ERROR HANDLING & GAS OPTIMIZATION
 * Sources: [1][2][5][6]
 */

// Rule 7.1: Custom Error Implementation
error InvalidAddress(address provided);
error InvalidTimeLockPeriod(uint256 provided);
error NoPermission(address caller);

function validateInput(address addr, uint256 value) internal pure {
    if (addr == address(0)) revert InvalidAddress(addr);
    if (value == 0) revert InvalidTimeLockPeriod(value);
}

// Rule 7.2: Gas-Efficient Error Patterns
library ValidationLibrary {
    error InvalidSignature(bytes signature);
    error TransactionNotFound(uint256 txId);
    
    function validateSignature(bytes memory sig) internal pure {
        if (sig.length != 65) revert InvalidSignature(sig);
    }
}

/**
 * SECTION 8: MULTI-PHASE SECURITY OPERATIONS
 * Sources: [1][4][5][6]
 */

// Rule 8.1: Time-Lock Security Implementation
struct SecureOperation {
    uint256 txId;
    uint256 releaseTime;
    uint8 status; // 0=PENDING, 1=APPROVED, 2=CANCELLED
    address requester;
}

function requestOperation(bytes32 operationType) external {
    // CHECK: Validate operation type and permissions
    require(supportedOperations[operationType], "Unsupported operation");
    
    // EFFECT: Create pending operation with timelock
    uint256 releaseTime = block.timestamp + timeLockPeriod;
    operations[nextTxId] = SecureOperation({
        txId: nextTxId,
        releaseTime: releaseTime,
        status: 0, // PENDING
        requester: msg.sender
    });
    
    // INTERACT: Emit event for monitoring
    emit OperationRequested(nextTxId, operationType, releaseTime);
}

// Rule 8.2: Meta-Transaction Support
function executeMetaTransaction(
    MetaTransaction memory metaTx,
    bytes memory signature
) external {
    // Validate EIP-712 signature
    bytes32 hash = _hashTypedDataV4(_hashMetaTransaction(metaTx));
    address signer = ECDSA.recover(hash, signature);
    require(authorizedSigners[signer], "Unauthorized signer");
    
    // Execute with proper validation
    _executeTransaction(metaTx.txRecord);
}

/**
 * SECTION 9: DYNAMIC ROLE-BASED ACCESS CONTROL
 * Sources: [1][4][5][6]
 */

// Rule 9.1: RBAC Implementation Patterns
struct Role {
    string roleName;
    bytes32 roleHash;
    mapping(address => bool) authorizedWallets;
    mapping(bytes4 => bool) functionPermissions;
    uint256 maxWallets;
    bool isProtected;
}

function createRole(string memory roleName, uint256 maxWallets) external {
    require(!isProtectedRole(roleName), "Cannot modify protected roles");
    require(maxWallets > 0, "Max wallets must be greater than zero");
    
    bytes32 roleHash = keccak256(abi.encodePacked(roleName));
    roles[roleHash] = Role({
        roleName: roleName,
        roleHash: roleHash,
        maxWallets: maxWallets,
        isProtected: false
    });
    
    emit RoleCreated(roleHash, roleName, maxWallets);
}

// Rule 9.2: Permission Validation
modifier onlyRole(bytes32 roleHash) {
    require(roles[roleHash].authorizedWallets[msg.sender], "No permission");
    _;
}

modifier onlyFunction(bytes4 functionSelector) {
    require(hasFunctionPermission(msg.sender, functionSelector), "No function permission");
    _;
}

/**
 * SECTION 10: TYPESCRIPT SDK DEVELOPMENT
 * Sources: [1][2][5]
 */

// Rule 10.1: SDK Interface Patterns
interface ISecureOwnable {
    transferOwnershipRequest(options: TransactionOptions): Promise<TransactionResult>;
    transferOwnershipDelayedApproval(txId: bigint, options: TransactionOptions): Promise<TransactionResult>;
}

// Rule 10.2: Type-Safe Contract Interaction
export class SecureOwnable implements ISecureOwnable {
    constructor(
        protected client: PublicClient,
        protected walletClient: WalletClient | undefined,
        protected contractAddress: Address,
        protected chain: Chain
    ) {}

    async transferOwnershipRequest(options: TransactionOptions): Promise<TransactionResult> {
        if (!this.walletClient) throw new Error('Wallet client is required');
        
        const hash = await this.walletClient.writeContract({
            chain: this.chain,
            address: this.contractAddress,
            abi: SecureOwnableABIJson,
            functionName: 'transferOwnershipRequest',
            args: [],
            account: options.from
        });
        
        return {
            hash,
            wait: () => this.client.waitForTransactionReceipt({ hash })
        };
    }
}

/**
 * SECTION 11: TESTING & VERIFICATION ENHANCEMENTS
 * Sources: [4][5][6]
 */

// Rule 11.1: Comprehensive Test Coverage
contract TestSuite {
    function testMultiPhaseOperation() public {
        // Test request phase
        vm.expectEmit(true, true, true, true);
        emit OperationRequested(1, OPERATION_TYPE, expectedReleaseTime);
        requestOperation(OPERATION_TYPE);
        
        // Test approval phase
        vm.warp(expectedReleaseTime);
        vm.expectEmit(true, true, true, true);
        emit OperationApproved(1);
        approveOperation(1);
    }
    
    function testFuzzing(uint128 amount, address target) public {
        vm.assume(amount > 0);
        vm.assume(target != address(0));
        vm.assume(target != address(this));
        
        // Fuzz test with valid inputs
        transferWithValidation(target, amount);
    }
}

// Rule 11.2: Invariant Testing
contract InvariantTest {
    function invariant_TotalSupplyConservation() public {
        assertEq(totalSupply, sumOfBalances());
    }
    
    function invariant_NoZeroAddressRoles() public {
        for (uint i = 0; i < roleCount; i++) {
            assertTrue(roles[i].authorizedWallets[address(0)] == false);
        }
    }
}

/**
 * SECTION 12: DOCUMENTATION & CODE GENERATION
 * Sources: [1][2][5]
 */

// Rule 12.1: NatSpec Documentation Standards
/**
 * @title SecureOwnable
 * @dev Enhanced ownership contract with multi-phase security operations
 * @notice This contract implements time-locked operations for critical administrative functions
 * @author Particle Crypto Security
 * @custom:security-contact security@particlecrypto.com
 */

/**
 * @dev Creates a new secure operation request
 * @param operationType The type of operation to request
 * @return txId The transaction ID of the created request
 * @custom:security This function implements time-lock security and requires proper authorization
 */
function requestOperation(bytes32 operationType) external returns (uint256 txId);

// Rule 12.2: Event Documentation
/**
 * @dev Emitted when a new operation is requested
 * @param txId The transaction ID of the request
 * @param operationType The type of operation requested
 * @param releaseTime The timestamp when the operation can be executed
 */
event OperationRequested(uint256 indexed txId, bytes32 indexed operationType, uint256 releaseTime);

/**
 * SECURITY FOOTER
 * Implements best practices from:
 * - OWASP Blockchain Top 10 [4][6]
 * - Ethereum Smart Contract Security Guidelines [1][2]
 * - Military-Grade Development Standards [Previous Implementation]
 * - OpenZeppelin Upgrade Patterns [3]
 * - Custom Error Optimization Patterns [Gas Efficiency]
 * - Multi-Phase Security Operations [Time-Lock Security]
 * - Dynamic RBAC Implementation [Role-Based Access Control]
 * - TypeScript SDK Development [Client-Side Integration]
 * - Truffle Development Platform Standards [Contract Size Optimization]
 * - Contract Size Monitoring with npm run compile:truffle:size [Gas Efficiency]
 */
```

## Key Security Features Implemented

1. **Reentrancy Protection**  
   Uses OpenZeppelin's `nonReentrant` modifier and strict CEI pattern to prevent callback attacks[1][6]. Includes fallback function hardening against unintended interactions.

2. **Arithmetic Safety**  
   Implements SafeMath2025 library with overflow/underflow protection and explicit division handling[6]. All mathematical operations require bounds checking.

3. **Input Validation**  
   Comprehensive validation modifiers check for zero-address, self-targeting, and invalid value parameters[2][6]. Includes fuzzing tests for edge case discovery[5].

4. **Visibility Enforcement**  
   Strict visibility modifiers (private/internal) for sensitive functions and state variables[1][6]. Public functions require explicit access control.

5. **Upgrade Safety**  
   Follows OpenZeppelin upgrade patterns with storage gaps and initializer functions[3]. Prohibits constructor usage in upgradeable contracts.

6. **Compliance Integration**  
   Built-in sanctions checking and regulatory compliance modifiers[4][6]. Supports ERC standard interfaces with enhanced security proofs.

7. **Custom Error Optimization**  
   Gas-efficient custom errors with contextual parameters reduce contract size by ~50%[6]. Enhanced error reporting with specific failure reasons and context.

8. **Multi-Phase Security Operations**  
   Time-locked operations with request/approval workflow[1][6]. Meta-transaction support with EIP-712 signature validation for delegated operations.

9. **Dynamic Role-Based Access Control**  
   Flexible RBAC system with protected/unprotected roles[4][6]. Function-level permissions with role hierarchy and wallet limits.

10. **TypeScript SDK Integration**  
    Type-safe contract interfaces with Viem integration[1][2]. Comprehensive SDK with meta-transaction utilities and event monitoring.

11. **Advanced Testing Patterns**  
    Comprehensive test coverage with fuzzing and invariant testing[5][6]. Multi-phase operation testing with proper state transitions.

12. **Documentation Standards**  
    NatSpec documentation with security annotations[1][5]. Automated code generation with proper type definitions.

## Development Workflow Requirements

```solidity
// CI/CD Pipeline Rules
pragma pipeline_rules >= 2025.1;

// Pre-Commit Checks
rule StaticAnalysis {
    use Slither with "security-medium";
    use Semgrep with "solidity-best-practices";
    max_warnings = 0; // [4][5]
}

// Test Coverage Requirements
rule TestValidation {
    min_coverage = 95%;
    fuzz_tests required; // [5]
    invariant_checking enabled;
}

// Audit Requirements
rule SecurityAudits {
    external_audit before_deployment; // [4]
    automatic_scanning continuous;
}

// Truffle Development Platform Rules
rule TruffleCompilation {
    platform = "Truffle"; // [Primary Development Platform]
    compilation_check = "npm run compile:truffle:size";
    contract_size_limit = "24KB"; // [Ethereum Mainnet Limit]
    optimization_enabled = true;
    bytecode_verification = required;
}
```

This ruleset enforces:  
- Mandatory static analysis with zero warnings[4][5]  
- 95%+ test coverage with fuzzing requirements[5]  
- Third-party audits before mainnet deployment[4]  
- Continuous security monitoring post-deployment[6]
- Truffle as primary development platform with size optimization[Contract Efficiency]
- Contract size monitoring with `npm run compile:truffle:size` validation[Gas Optimization]

## Truffle Development Platform Standards

```solidity
// SECTION 13: TRUFFLE DEVELOPMENT WORKFLOW
// Sources: [Truffle Best Practices][Contract Size Optimization]

// Rule 13.1: Truffle Compilation Standards
contract TruffleOptimized {
    // Always run: npm run compile:truffle:size
    // Verify: Contract size < 24KB (Ethereum mainnet limit)
    // Check: No compilation errors or warnings
    
    // Use Truffle's built-in optimization
    // pragma solidity ^0.8.0;
    // optimizer: { enabled: true, runs: 200 }
}

// Rule 13.2: Contract Size Optimization Patterns
library SizeOptimization {
    // Use libraries for reusable code
    // Minimize storage variables
    // Use packed structs where possible
    // Implement custom errors instead of strings
    
    struct PackedData {
        uint128 value1; // Packed into single slot
        uint128 value2; // Packed into single slot
    }
    
    // Use events instead of storage for historical data
    event OptimizedEvent(uint256 indexed id, bytes32 data);
}

// Rule 13.3: Truffle Testing Integration
contract TruffleTestSuite {
    // Use Truffle's testing framework
    // Implement size-aware testing
    // Verify deployment gas costs
    
    function testContractSize() public {
        // Verify contract compiles under size limit
        // Check gas optimization effectiveness
    }
}
```

## Implementation Guidance

1. Use `require()` for all pre-condition checks[1][2]  
2. Apply `nonReentrant` modifier to state-changing functions[6]  
3. Validate all external inputs with modifier chains[2][6]  
4. Maintain upgrade compatibility through storage gaps[3]  
5. Implement comprehensive event logging for all critical operations[1][5]  
6. Use custom errors instead of string messages for gas optimization[6]  
7. Implement multi-phase operations with proper time-lock validation[1][6]  
8. Apply RBAC patterns with role-based function permissions[4][6]  
9. Use EIP-712 for meta-transaction signature validation[1][2]  
10. Create type-safe SDK interfaces with proper error handling[1][2]  
11. Write comprehensive tests with fuzzing and invariant checking[5][6]  
12. Document all functions with NatSpec and security annotations[1][5]
13. **Always run `npm run compile:truffle:size` before deployment**[Contract Size Optimization]
14. **Maintain contract size under 24KB limit**[Gas Efficiency]
15. **Use Truffle as primary development and testing platform**[Development Workflow]

## Assistant Workflow Modes

```json
{
  "version": "0.1",
  "rules": [
    {
      "selector": "code",
      "actions": [
        {
          "type": "if_text_contains_any",
          "keywords": [
            "explore",
            "hypothesis",
            "broad",
            "divergent",
            "open-ended",
            "uncertain",
            "investigate",
            "research"
          ],
          "actions": [
            { "type": "set_workflow_mode", "mode": "exploration" }
          ]
        },
        {
          "type": "if_text_contains_any",
          "keywords": [
            "efficient",
            "direct",
            "specific",
            "answer",
            "solve",
            "fix",
            "reuse",
            "exact"
          ],
          "actions": [
            { "type": "set_workflow_mode", "mode": "exploitation" }
          ]
        },
        {
          "type": "if_no_workflow_mode",
          "actions": [
            {
              "type": "set_workflow_mode",
              "mode": "exploitation"
            }
          ]
        },
        {
          "type": "if_mode",
          "mode": "exploration",
          "actions": [
            { "type": "prioritize", "targets": ["hypothesis_generation", "broad_patterns", "divergent_examples", "investigative_approach"] },
            { "type": "allow", "targets": ["exploitation_elements", "direct_solutions", "efficiency_focus"] },
            { "type": "restrict", "targets": ["premature_optimization", "over-narrowing_scope"] }
          ]
        },
        {
          "type": "if_mode",
          "mode": "exploitation",
          "actions": [
            { "type": "prioritize", "targets": ["efficiency", "direct_solution_paths", "reuse_existing_knowledge", "immediate_implementation"] },
            { "type": "allow", "targets": ["exploration_elements", "investigative_aspects", "broad_context"] },
            { "type": "eliminate", "targets": ["redundant_exploration", "tangential_investigation"] }
          ]
        },
        {
          "type": "if_context_contains_any",
          "keywords": [
            "absolute mode",
            "blunt",
            "directive",
            "no sentiment",
            "suppress emotion",
            "no engagement",
            "no softening",
            "terminate immediately",
            "cognitive rebuilding"
          ],
          "actions": [
            { "type": "set_mode", "mode": "absolute" }
          ]
        },
        {
          "type": "if_mode",
          "mode": "absolute",
          "actions": [
            { "type": "disable", "targets": ["emojis", "excessive_agreement", "emotional_softening", "sentiment_boosting"] },
            { "type": "allow", "targets": ["structured_responses", "markdown_formatting", "conversational_flow", "suggestions", "call_to_action"] },
            { "type": "prioritize", "targets": ["direct_communication", "factual_presentation", "constructive_feedback"] },
            { "type": "suppress", "targets": ["excessive_politeness", "unnecessary_apologies", "overly_agreeable_tone"] }
          ]
        },
        { "type": "prioritize", "focus": ["mode_fidelity"] },
        { "type": "disable", "targets": ["workflow_blurring", "ambiguous_instruction"] },
        { "type": "terminate", "rule": "deliver_mode-specific_info_only" }
      ]
    }
  ]
}
```