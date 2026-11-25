---
id: bap578-testing
name: BAP-578 Testing
description: Use this skill when writing, running, debugging, or extending BAP-578 Non-Fungible Agent tests, including infrastructure setup, function coverage, edge cases, upgrades, gas profiling, and Hardhat workflows.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Testing

Use this skill to write, run, debug, and extend the test suite for BAP-578 Non-Fungible Agents. This covers test infrastructure setup, comprehensive test cases for every contract function, edge case coverage, upgrade testing, gas profiling, and debugging strategies.

---

## When to use this skill

- Writing new tests for BAP-578 contract functions.
- Running the existing test suite and interpreting results.
- Adding edge case coverage for minting, funding, and withdrawal.
- Testing access control boundaries.
- Writing upgrade tests (V1 → V2 state preservation).
- Debugging failing tests with specific error messages.
- Measuring gas usage for optimization.

---

## The Four Identity Questions (Testing View)

### 1) Who are you?

The testing layer is the quality gate for the entire contract. Tests prove that every function behaves correctly, every access control is enforced, every edge case is handled, and every upgrade preserves state. Without comprehensive tests, the contract cannot be trusted for deployment.

### 2) What do you remember?

The test suite remembers every expected behavior: valid minting flows, fee calculations, free mint restrictions, transfer rules, withdrawal safety, status toggles, metadata updates, and admin operations. Each test case is a documented expectation of how the contract should work.

### 3) What can you do?

- Run the full test suite with a single command
- Test individual functions in isolation (unit tests)
- Test multi-step workflows (integration tests)
- Test upgrade state preservation
- Measure gas consumption per function
- Verify error messages for invalid operations
- Simulate attacks and verify they fail

### 4) How can I trust it?

Tests map directly to contract functions and user stories. Every test has a clear description, setup, action, and assertion. Tests run against a local Hardhat network with deterministic results. Coverage tools can verify that all code paths are exercised.

---

## Test Infrastructure

### Setup

```bash
cd non-fungible-agents-BAP-578
npm install
```

### Running tests

```bash
# Run all tests
npm test

# Run with verbose output
npx hardhat test --verbose

# Run a specific test file
npx hardhat test test/NonFungibleAgents.test.js

# Run with gas reporting
REPORT_GAS=true npx hardhat test

# Run with coverage
npx hardhat coverage
```

### Test file structure

```
test/
├── NonFungibleAgents.test.js    # Main test suite
├── helpers/
│   ├── fixtures.js              # Reusable deployment fixtures
│   └── constants.js             # Test constants
└── upgrade/
    └── upgrade.test.js          # Upgrade-specific tests
```

---

## Test Fixtures

### Standard deployment fixture

```js
const { ethers, upgrades } = require("hardhat");

async function deployFixture() {
  const [owner, treasury, user1, user2, user3] = await ethers.getSigners();

  const NFA = await ethers.getContractFactory("NonFungibleAgents");
  const nfa = await upgrades.deployProxy(NFA, [
    "Non-Fungible Agents",
    "NFA",
    treasury.address,
  ], { kind: "uups" });

  const MINT_FEE = ethers.parseEther("0.01");
  const DEFAULT_FREE_MINTS = 3;

  const defaultMetadata = {
    persona: JSON.stringify({ name: "TestAgent", traits: ["helpful"] }),
    experience: "Test agent for unit testing",
    voiceHash: "",
    animationURI: "",
    vaultURI: "",
    vaultHash: ethers.ZeroHash,
  };

  return {
    nfa,
    owner,
    treasury,
    user1,
    user2,
    user3,
    MINT_FEE,
    DEFAULT_FREE_MINTS,
    defaultMetadata,
  };
}

module.exports = { deployFixture };
```

### Fixture with pre-minted agents

```js
async function deployWithAgentsFixture() {
  const base = await deployFixture();
  const { nfa, user1, user2, defaultMetadata } = base;

  // Mint 3 free agents for user1
  for (let i = 0; i < 3; i++) {
    await nfa.connect(user1).createAgent(
      user1.address,
      ethers.ZeroAddress,
      `ipfs://meta${i}`,
      { ...defaultMetadata, experience: `Agent ${i}` }
    );
  }

  // Mint 1 paid agent for user2
  await nfa.connect(user2).createAgent(
    user2.address,
    ethers.ZeroAddress,
    "ipfs://meta-paid",
    defaultMetadata,
    { value: base.MINT_FEE }
  );

  return { ...base, user1AgentIds: [1, 2, 3], user2AgentId: 4 };
}
```

---

## Comprehensive Test Cases

### Minting Tests

```js
describe("createAgent", function () {
  describe("Free mints", function () {
    it("allows free mint to self", async function () {
      const { nfa, user1, defaultMetadata } = await deployFixture();
      await expect(
        nfa.connect(user1).createAgent(
          user1.address,
          ethers.ZeroAddress,
          "ipfs://meta",
          defaultMetadata
        )
      ).to.emit(nfa, "AgentCreated");
    });

    it("reverts free mint to different address", async function () {
      const { nfa, user1, user2, defaultMetadata } = await deployFixture();
      await expect(
        nfa.connect(user1).createAgent(
          user2.address,
          ethers.ZeroAddress,
          "ipfs://meta",
          defaultMetadata
        )
      ).to.be.revertedWith("Free mints must be to self");
    });

    it("tracks free mint count per user", async function () {
      const { nfa, user1, defaultMetadata } = await deployFixture();

      const initialFree = await nfa.getFreeMints(user1.address);
      await nfa.connect(user1).createAgent(
        user1.address, ethers.ZeroAddress, "ipfs://meta", defaultMetadata
      );
      const afterFree = await nfa.getFreeMints(user1.address);

      expect(afterFree).to.equal(initialFree - 1n);
    });

    it("marks free-minted tokens as non-transferable", async function () {
      const { nfa, user1, user2, defaultMetadata } = await deployFixture();

      await nfa.connect(user1).createAgent(
        user1.address, ethers.ZeroAddress, "ipfs://meta", defaultMetadata
      );

      expect(await nfa.isFreeMint(1)).to.be.true;

      await expect(
        nfa.connect(user1).transferFrom(user1.address, user2.address, 1)
      ).to.be.reverted;
    });

    it("exhausts free mints after allocation", async function () {
      const { nfa, user1, defaultMetadata, DEFAULT_FREE_MINTS } = await deployFixture();

      for (let i = 0; i < DEFAULT_FREE_MINTS; i++) {
        await nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, `ipfs://meta${i}`, defaultMetadata
        );
      }

      expect(await nfa.getFreeMints(user1.address)).to.equal(0);
    });
  });

  describe("Paid mints", function () {
    it("requires exact fee after free mints exhausted", async function () {
      const { nfa, user1, defaultMetadata, MINT_FEE, DEFAULT_FREE_MINTS } = await deployFixture();

      // Exhaust free mints
      for (let i = 0; i < DEFAULT_FREE_MINTS; i++) {
        await nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, `ipfs://meta${i}`, defaultMetadata
        );
      }

      // Paid mint with correct fee
      await expect(
        nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, "ipfs://paid", defaultMetadata,
          { value: MINT_FEE }
        )
      ).to.emit(nfa, "AgentCreated");
    });

    it("reverts with incorrect fee", async function () {
      const { nfa, user1, defaultMetadata, DEFAULT_FREE_MINTS } = await deployFixture();

      for (let i = 0; i < DEFAULT_FREE_MINTS; i++) {
        await nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, `ipfs://meta${i}`, defaultMetadata
        );
      }

      await expect(
        nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, "ipfs://paid", defaultMetadata,
          { value: ethers.parseEther("0.005") }
        )
      ).to.be.revertedWith("Incorrect fee");
    });

    it("allows paid mint to different address", async function () {
      const { nfa, user1, user2, defaultMetadata, MINT_FEE, DEFAULT_FREE_MINTS } = await deployFixture();

      for (let i = 0; i < DEFAULT_FREE_MINTS; i++) {
        await nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, `ipfs://meta${i}`, defaultMetadata
        );
      }

      await nfa.connect(user1).createAgent(
        user2.address, ethers.ZeroAddress, "ipfs://gift", defaultMetadata,
        { value: MINT_FEE }
      );

      expect(await nfa.ownerOf(DEFAULT_FREE_MINTS + 1)).to.equal(user2.address);
    });

    it("sends fee to treasury", async function () {
      const { nfa, user1, treasury, defaultMetadata, MINT_FEE, DEFAULT_FREE_MINTS } = await deployFixture();

      for (let i = 0; i < DEFAULT_FREE_MINTS; i++) {
        await nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, `ipfs://meta${i}`, defaultMetadata
        );
      }

      await expect(
        nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, "ipfs://paid", defaultMetadata,
          { value: MINT_FEE }
        )
      ).to.changeEtherBalance(treasury, MINT_FEE);
    });

    it("paid tokens are transferable", async function () {
      const { nfa, user1, user2, defaultMetadata, MINT_FEE, DEFAULT_FREE_MINTS } = await deployFixture();

      for (let i = 0; i < DEFAULT_FREE_MINTS; i++) {
        await nfa.connect(user1).createAgent(
          user1.address, ethers.ZeroAddress, `ipfs://meta${i}`, defaultMetadata
        );
      }

      const tokenId = DEFAULT_FREE_MINTS + 1;
      await nfa.connect(user1).createAgent(
        user1.address, ethers.ZeroAddress, "ipfs://paid", defaultMetadata,
        { value: MINT_FEE }
      );

      expect(await nfa.isFreeMint(tokenId)).to.be.false;

      await nfa.connect(user1).transferFrom(user1.address, user2.address, tokenId);
      expect(await nfa.ownerOf(tokenId)).to.equal(user2.address);
    });
  });
});
```

### Funding and Withdrawal Tests

```js
describe("Agent funding", function () {
  it("funds an agent with BNB", async function () {
    const { nfa, user1 } = await deployWithAgentsFixture();
    const amount = ethers.parseEther("0.5");

    await expect(
      nfa.connect(user1).fundAgent(1, { value: amount })
    ).to.emit(nfa, "AgentFunded").withArgs(1, user1.address, amount);

    const state = await nfa.getAgentState(1);
    expect(state.balance).to.equal(amount);
  });

  it("allows anyone to fund any agent", async function () {
    const { nfa, user2 } = await deployWithAgentsFixture();
    const amount = ethers.parseEther("0.1");

    await nfa.connect(user2).fundAgent(1, { value: amount });
    const state = await nfa.getAgentState(1);
    expect(state.balance).to.equal(amount);
  });
});

describe("Agent withdrawal", function () {
  it("allows token owner to withdraw", async function () {
    const { nfa, user1 } = await deployWithAgentsFixture();
    const fundAmount = ethers.parseEther("1.0");
    const withdrawAmount = ethers.parseEther("0.5");

    await nfa.connect(user1).fundAgent(1, { value: fundAmount });

    await expect(
      nfa.connect(user1).withdrawFromAgent(1, withdrawAmount)
    ).to.changeEtherBalance(user1, withdrawAmount);

    const state = await nfa.getAgentState(1);
    expect(state.balance).to.equal(fundAmount - withdrawAmount);
  });

  it("reverts withdrawal by non-owner", async function () {
    const { nfa, user1, user2 } = await deployWithAgentsFixture();

    await nfa.connect(user1).fundAgent(1, { value: ethers.parseEther("1.0") });

    await expect(
      nfa.connect(user2).withdrawFromAgent(1, ethers.parseEther("0.5"))
    ).to.be.reverted;
  });

  it("reverts withdrawal exceeding balance", async function () {
    const { nfa, user1 } = await deployWithAgentsFixture();

    await nfa.connect(user1).fundAgent(1, { value: ethers.parseEther("0.5") });

    await expect(
      nfa.connect(user1).withdrawFromAgent(1, ethers.parseEther("1.0"))
    ).to.be.reverted;
  });
});
```

### Access Control Tests

```js
describe("Access control", function () {
  it("only owner can set treasury", async function () {
    const { nfa, user1 } = await deployFixture();
    await expect(
      nfa.connect(user1).setTreasury(user1.address)
    ).to.be.reverted;
  });

  it("only owner can pause", async function () {
    const { nfa, user1 } = await deployFixture();
    await expect(
      nfa.connect(user1).setPaused(true)
    ).to.be.reverted;
  });

  it("only owner can grant free mints", async function () {
    const { nfa, user1, user2 } = await deployFixture();
    await expect(
      nfa.connect(user1).grantAdditionalFreeMints(user2.address, 5)
    ).to.be.reverted;
  });

  it("only token owner can set agent status", async function () {
    const { nfa, user2 } = await deployWithAgentsFixture();
    await expect(
      nfa.connect(user2).setAgentStatus(1, false)
    ).to.be.reverted;
  });

  it("only token owner can set logic address", async function () {
    const { nfa, user2 } = await deployWithAgentsFixture();
    await expect(
      nfa.connect(user2).setLogicAddress(1, ethers.ZeroAddress)
    ).to.be.reverted;
  });

  it("only token owner can update metadata", async function () {
    const { nfa, user2, defaultMetadata } = await deployWithAgentsFixture();
    await expect(
      nfa.connect(user2).updateAgentMetadata(1, "ipfs://new", defaultMetadata)
    ).to.be.reverted;
  });
});
```

### Metadata and Status Tests

```js
describe("Agent status", function () {
  it("toggles agent status", async function () {
    const { nfa, user1 } = await deployWithAgentsFixture();

    await nfa.connect(user1).setAgentStatus(1, false);
    let state = await nfa.getAgentState(1);
    expect(state.active).to.be.false;

    await nfa.connect(user1).setAgentStatus(1, true);
    state = await nfa.getAgentState(1);
    expect(state.active).to.be.true;
  });

  it("emits AgentStatusChanged event", async function () {
    const { nfa, user1 } = await deployWithAgentsFixture();
    await expect(
      nfa.connect(user1).setAgentStatus(1, false)
    ).to.emit(nfa, "AgentStatusChanged").withArgs(1, false);
  });
});

describe("Metadata updates", function () {
  it("updates agent metadata", async function () {
    const { nfa, user1 } = await deployWithAgentsFixture();

    const newMetadata = {
      persona: JSON.stringify({ name: "Updated" }),
      experience: "Updated experience",
      voiceHash: "newvoice",
      animationURI: "ipfs://newanim",
      vaultURI: "ipfs://newvault",
      vaultHash: ethers.keccak256(ethers.toUtf8Bytes("vault content")),
    };

    await nfa.connect(user1).updateAgentMetadata(1, "ipfs://newuri", newMetadata);

    const meta = await nfa.getAgentMetadata(1);
    expect(meta.experience).to.equal("Updated experience");
    expect(meta.vaultURI).to.equal("ipfs://newvault");
  });

  it("emits MetadataUpdated event", async function () {
    const { nfa, user1, defaultMetadata } = await deployWithAgentsFixture();
    await expect(
      nfa.connect(user1).updateAgentMetadata(1, "ipfs://new", defaultMetadata)
    ).to.emit(nfa, "MetadataUpdated").withArgs(1, "ipfs://new");
  });
});
```

---

## Debugging Failed Tests

### Common error messages and causes

- **"Incorrect fee"** — sent wrong `msg.value`; check if free mints remain
- **"Free mints must be to self"** — tried to mint free token to different address
- **"Not token owner"** — wrong signer; check `connect(correctUser)`
- **"Contract is paused"** — call `setPaused(false)` in setup
- **"Invalid logic address"** — passed EOA instead of contract address
- **"Insufficient balance"** — tried to withdraw more than agent balance

### Debugging approach

1. Read the full error message (use `--verbose` flag).
2. Check which `require` or custom error is triggered.
3. Verify test setup (correct fixture, correct signer).
4. Add `console.log` in the contract temporarily for deeper debugging.
5. Use Hardhat's `console.sol` import for in-contract logging.

---

## Gas Profiling

```bash
REPORT_GAS=true npx hardhat test
```

This outputs a table showing gas usage per function call. Use it to:

- Identify expensive operations
- Compare gas before and after optimizations
- Set gas expectations in tests

### Example gas assertions

```js
it("mint gas should be under 400k", async function () {
  const tx = await nfa.connect(user1).createAgent(
    user1.address, ethers.ZeroAddress, "ipfs://meta", defaultMetadata
  );
  const receipt = await tx.wait();
  expect(receipt.gasUsed).to.be.lt(400000n);
});
```

---

## Edge Cases to Always Test

### Boundary conditions

- Mint the last free token (free mints = 1, then mint)
- Withdraw exact full balance (balance goes to 0)
- Fund with 0 value (should it revert or no-op?)
- Set logic address to self (contract calling itself)
- Update metadata with empty strings
- Transfer paid token to the zero address (should revert)
- Call functions on non-existent token IDs

### Concurrency patterns

- Two users minting simultaneously (no collision on token IDs)
- Fund and withdraw in the same block
- Multiple metadata updates in a single block

### Upgrade edge cases

- Upgrade while contract is paused
- Upgrade with agents that have non-zero balances
- Upgrade with agents that have bound logic contracts
- Call V2 functions from V1 ABI (should fail gracefully)

---

## Coverage Reporting

```bash
npx hardhat coverage
```

Generates an HTML report in `coverage/index.html`. Target metrics:

| Category | Target |
|----------|--------|
| Statements | > 95% |
| Branches | > 90% |
| Functions | 100% |
| Lines | > 95% |

Review uncovered lines to identify missing test cases. Pay special attention to:
- Error branches (require/revert paths)
- Edge cases in conditional logic
- Admin-only functions
- Transfer restriction hooks

---

## Output Format

When asked for testing help, respond with:

1. **Test goal** (what behavior is being verified)
2. **Complete test code** (setup, action, assertions)
3. **Expected outcomes** (pass/fail conditions)
4. **Edge cases to add** (what else should be tested)
5. **Failure diagnosis** if a test is failing

---

## Related Skills

- `bap578`
- `bap578-upgrade`
- `bap578-security-audit`
