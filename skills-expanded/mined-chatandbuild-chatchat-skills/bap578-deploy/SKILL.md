---
id: bap578-deploy
name: BAP-578 Deployment
description: Use this skill when deploying, verifying, configuring, or validating BAP-578 Non-Fungible Agent contracts on BNB Chain testnet or mainnet, from environment setup through post-deployment checks.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Deployment

Use this skill to deploy, verify, configure, and validate BAP-578 Non-Fungible Agents contracts on BNB Chain testnet and mainnet. This covers the complete deployment lifecycle from environment setup through post-deployment verification.

---

## When to use this skill

- Setting up the development environment for the first time.
- Deploying the contract to BSC Testnet for testing.
- Deploying to BSC Mainnet for production.
- Verifying the contract source on BscScan.
- Running post-deployment checks to confirm correct configuration.
- Configuring treasury, free mints, and other admin settings after deployment.
- Troubleshooting deployment failures.

---

## The Four Identity Questions (Deployment View)

### 1) Who are you?

The deployment process is the bridge between code and a live contract. It creates the proxy and implementation on-chain, sets initial configuration, and establishes the contract's identity (name, symbol, owner, treasury). After deployment, the contract exists at a permanent proxy address that users will interact with forever.

### 2) What do you remember?

Deployment records include the proxy address, implementation address, deployer address, initialization parameters, deployment block number, and transaction hashes. These are critical for verification, upgrade planning, and incident response.

### 3) What can you do?

- Deploy the UUPS proxy and implementation contract
- Initialize with name, symbol, and treasury address
- Verify source code on BscScan
- Configure post-deployment settings (free mints, treasury, pause state)
- Run automated verification checks
- Generate deployment reports

### 4) How can I trust it?

Deployment trust comes from:

- Source code verification on BscScan (anyone can read the code)
- Post-deployment checks confirming correct initialization
- Transparent deployment scripts (reproducible)
- Test deployment on testnet before mainnet

---

## Prerequisites

### Required tools

- Node.js v18+ (check with `node --version`)
- npm or yarn
- Git
- A funded wallet (BSC Testnet faucet for testnet, real BNB for mainnet)

### Required accounts

- BscScan API key (for contract verification)
- RPC endpoint (public or dedicated provider)

---

## Environment Setup

### Step 1: Clone and install

```bash
cd non-fungible-agents-BAP-578
npm install
```

### Step 2: Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
# Deployer wallet private key (NEVER commit this)
DEPLOYER_PRIVATE_KEY=0xYourPrivateKeyHere

# RPC URLs
BSC_TESTNET_RPC_URL=your_bsc_testnet_rpc_url
BSC_MAINNET_RPC_URL=your_bsc_mainnet_rpc_url

# BscScan API key (for verification)
BSCSCAN_API_KEY=your_bscscan_api_key

# Treasury address (receives mint fees)
TREASURY_ADDRESS=0xYourTreasuryAddress

# Contract name and symbol
TOKEN_NAME="Non-Fungible Agents"
TOKEN_SYMBOL="NFA"
```

### Step 3: Verify Hardhat config

The `hardhat.config.js` should include BSC network configurations:

```js
require("@nomicfoundation/hardhat-toolbox");
require("@openzeppelin/hardhat-upgrades");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: { enabled: true, runs: 200 },
    },
  },
  networks: {
    bscTestnet: {
      url: process.env.BSC_TESTNET_RPC_URL,
      accounts: [process.env.DEPLOYER_PRIVATE_KEY],
      chainId: 97,
    },
    bsc: {
      url: process.env.BSC_MAINNET_RPC_URL,
      accounts: [process.env.DEPLOYER_PRIVATE_KEY],
      chainId: 56,
    },
  },
  etherscan: {
    apiKey: {
      bscTestnet: process.env.BSCSCAN_API_KEY,
      bsc: process.env.BSCSCAN_API_KEY,
    },
  },
};
```

---

## Deployment Steps

### Step 1: Compile

```bash
npm run compile
# or
npx hardhat compile
```

Expected output: compiled contracts in `artifacts/` directory with no errors.

### Step 2: Run tests

```bash
npm test
```

All tests must pass before deployment. Do not deploy with failing tests.

### Step 3: Deploy to testnet

```bash
npm run deploy:testnet
# or
npx hardhat run scripts/deploy.js --network bscTestnet
```

### Deployment script

```js
const { ethers, upgrades } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);
  console.log("Balance:", ethers.formatEther(
    await ethers.provider.getBalance(deployer.address)
  ), "BNB");

  const treasuryAddress = process.env.TREASURY_ADDRESS;
  const tokenName = process.env.TOKEN_NAME || "Non-Fungible Agents";
  const tokenSymbol = process.env.TOKEN_SYMBOL || "NFA";

  console.log("\nDeploying NonFungibleAgents...");
  console.log("  Name:", tokenName);
  console.log("  Symbol:", tokenSymbol);
  console.log("  Treasury:", treasuryAddress);

  const NFA = await ethers.getContractFactory("NonFungibleAgents");
  const nfa = await upgrades.deployProxy(
    NFA,
    [tokenName, tokenSymbol, treasuryAddress],
    {
      kind: "uups",
      initializer: "initialize",
    }
  );

  await nfa.waitForDeployment();

  const proxyAddress = await nfa.getAddress();
  const implAddress = await upgrades.erc1967.getImplementationAddress(proxyAddress);

  console.log("\n✅ Deployment successful!");
  console.log("  Proxy address:", proxyAddress);
  console.log("  Implementation:", implAddress);
  console.log("  Owner:", await nfa.owner());
  console.log("  Treasury:", await nfa.treasuryAddress());
  console.log("  Paused:", await nfa.paused());

  // Save deployment info
  const fs = require("fs");
  const deploymentInfo = {
    network: (await ethers.provider.getNetwork()).name,
    chainId: (await ethers.provider.getNetwork()).chainId.toString(),
    proxy: proxyAddress,
    implementation: implAddress,
    deployer: deployer.address,
    treasury: treasuryAddress,
    blockNumber: await ethers.provider.getBlockNumber(),
    timestamp: new Date().toISOString(),
  };

  fs.writeFileSync(
    `deployment-${deploymentInfo.network}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("\nDeployment info saved to deployment-" + deploymentInfo.network + ".json");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

### Step 4: Verify on BscScan

```bash
npx hardhat verify --network bscTestnet IMPLEMENTATION_ADDRESS
```

For proxies, you may also need to verify the proxy:

```bash
npx hardhat verify --network bscTestnet PROXY_ADDRESS
```

If automatic verification fails, use the BscScan web UI:
1. Go to the contract address on BscScan.
2. Click "Contract" → "Verify and Publish".
3. Select compiler version, optimization settings.
4. Paste flattened source code.

### Step 5: Post-deployment configuration

After deployment, configure optional settings:

```js
const nfa = await ethers.getContractAt("NonFungibleAgents", PROXY_ADDRESS);

// Set free mints per user (if different from default)
await nfa.setFreeMintsPerUser(3);

// Grant additional free mints to specific addresses
await nfa.grantAdditionalFreeMints("0xPartnerAddress", 10);

// Verify configuration
console.log("Free mints per user:", await nfa.freeMintsPerUser());
console.log("Treasury:", await nfa.treasuryAddress());
console.log("Owner:", await nfa.owner());
console.log("Paused:", await nfa.paused());
```

---

## Post-Deployment Verification Checklist

Run this checklist after every deployment:

- [ ] Proxy address recorded and saved
- [ ] Implementation address recorded and saved
- [ ] `owner()` returns deployer address (or intended owner)
- [ ] `treasuryAddress()` returns correct treasury
- [ ] `paused()` returns `false`
- [ ] `getTotalSupply()` returns `0`
- [ ] Test free mint succeeds
- [ ] Test paid mint succeeds (after exhausting free mints)
- [ ] Test `getAgentState()` returns correct data
- [ ] Test `getAgentMetadata()` returns correct data
- [ ] Source code verified on BscScan
- [ ] Deployment info saved to file

### Automated verification script

```js
async function verifyDeployment(proxyAddress) {
  const nfa = await ethers.getContractAt("NonFungibleAgents", proxyAddress);

  const checks = [];

  // Basic state checks
  const owner = await nfa.owner();
  checks.push({ name: "Owner set", pass: owner !== ethers.ZeroAddress, value: owner });

  const treasury = await nfa.treasuryAddress();
  checks.push({ name: "Treasury set", pass: treasury !== ethers.ZeroAddress, value: treasury });

  const paused = await nfa.paused();
  checks.push({ name: "Not paused", pass: !paused, value: paused });

  const supply = await nfa.getTotalSupply();
  checks.push({ name: "Supply is 0", pass: supply === 0n, value: supply.toString() });

  // Test mint
  try {
    const [deployer] = await ethers.getSigners();
    const tx = await nfa.createAgent(
      deployer.address,
      ethers.ZeroAddress,
      "ipfs://test-deployment",
      {
        persona: '{"name":"DeployTest"}',
        experience: "Deployment verification agent",
        voiceHash: "",
        animationURI: "",
        vaultURI: "",
        vaultHash: ethers.ZeroHash,
      }
    );
    await tx.wait();
    checks.push({ name: "Test mint", pass: true, value: "Token #1 minted" });

    const state = await nfa.getAgentState(1);
    checks.push({ name: "State readable", pass: state.active === true, value: "Active" });

    const meta = await nfa.getAgentMetadata(1);
    checks.push({ name: "Metadata readable", pass: meta.experience.length > 0, value: meta.experience });
  } catch (e) {
    checks.push({ name: "Test mint", pass: false, value: e.message });
  }

  // Print results
  console.log("\n=== Deployment Verification ===");
  for (const check of checks) {
    const icon = check.pass ? "✅" : "❌";
    console.log(`${icon} ${check.name}: ${check.value}`);
  }

  const allPassed = checks.every((c) => c.pass);
  console.log(allPassed ? "\n✅ All checks passed!" : "\n❌ Some checks failed!");
  return allPassed;
}
```

---

## Mainnet Deployment

### Additional precautions for mainnet

1. **Double-check treasury address.** Fees go here permanently. Use a multisig.
2. **Verify deployer balance.** Ensure enough BNB for deployment gas.
3. **Review all environment variables.** Wrong RPC URL = wrong chain.
4. **Deploy during low-gas periods** if possible.
5. **Have the team review the deployment script** before execution.
6. **Record the deployment transaction hash** for audit trail.

### Mainnet command

```bash
npx hardhat run scripts/deploy.js --network bsc
```

### Post-mainnet steps

1. Verify source on BscScan immediately.
2. Run the automated verification script.
3. Transfer ownership to a multisig (if not already the deployer).
4. Announce deployment with proxy address.
5. Update frontend config with the new contract address.

---

## Network Configuration Reference

### BSC Testnet

```
Chain ID:     97
Currency:     tBNB
Block time:   ~3 seconds
```

### BSC Mainnet

```
Chain ID:     56
Currency:     BNB
Block time:   ~3 seconds
```

---

## Common Deployment Errors

**"Insufficient funds"**
- Deployer wallet doesn't have enough BNB for gas.
- Solution: Fund the wallet via faucet (testnet) or transfer (mainnet).

**"Nonce too high" / "Nonce too low"**
- Transaction count mismatch.
- Solution: Reset nonce in Hardhat config or wait for pending transactions.

**"Contract size exceeds limit"**
- Contract bytecode too large (24KB limit).
- Solution: Enable optimizer, increase runs, or split into libraries.

**"Verification failed"**
- Compiler version or settings mismatch.
- Solution: Ensure exact same compiler version and optimizer settings.

**"Already initialized"**
- Proxy was already initialized.
- Solution: This means deploy succeeded but script re-ran. Check proxy address.

---

## Multi-Environment Deployment Strategy

### Environment progression

```
Local Hardhat → BSC Testnet → BSC Mainnet
     │                │              │
   Development    Staging       Production
   (instant)     (verify)     (permanent)
```

### Local development deployment

For rapid iteration, deploy to Hardhat's local network:

```bash
npx hardhat node
# In another terminal:
npx hardhat run scripts/deploy.js --network localhost
```

Benefits: instant confirmation, free gas, full control. Resets on restart.

### Testnet deployment

BSC Testnet mirrors mainnet behavior with free tBNB:

1. Get tBNB from the BSC Testnet faucet.
2. Deploy with `--network bscTestnet`.
3. Verify on testnet BscScan.
4. Run full integration tests against the deployed contract.
5. Test with a frontend connected to testnet.

### Mainnet deployment

Only after testnet is fully verified:

1. Double-check all environment variables.
2. Ensure treasury is a multisig.
3. Deploy with `--network bsc`.
4. Verify immediately.
5. Run post-deployment verification script.
6. Announce deployment.

---

## Gas Cost Estimates

Estimated gas costs for BAP-578 operations on BSC:

| Operation | Estimated Gas | ~Cost at 5 gwei |
|-----------|--------------|-----------------|
| Deploy proxy | ~500,000 | ~0.0025 BNB |
| Deploy implementation | ~3,500,000 | ~0.0175 BNB |
| Initialize | ~200,000 | ~0.001 BNB |
| createAgent (free) | ~350,000 | ~0.00175 BNB |
| createAgent (paid) | ~380,000 | ~0.0019 BNB |
| fundAgent | ~50,000 | ~0.00025 BNB |
| withdrawFromAgent | ~60,000 | ~0.0003 BNB |
| updateAgentMetadata | ~150,000 | ~0.00075 BNB |
| setLogicAddress | ~50,000 | ~0.00025 BNB |
| setAgentStatus | ~30,000 | ~0.00015 BNB |

**Total deployment cost:** ~0.02-0.03 BNB (including first test mint)

Note: Actual gas costs vary with network congestion and contract size. Always check current gas prices before mainnet deployment.

---

## Security Checklist Before Deployment

Before deploying to any network, verify:

- [ ] All tests pass (`npm test`)
- [ ] No compiler warnings
- [ ] Optimizer enabled (200 runs recommended)
- [ ] Deployer private key is not committed to git
- [ ] `.env` is in `.gitignore`
- [ ] Treasury address is a multisig (for mainnet)
- [ ] Contract source will be verified on block explorer
- [ ] `_authorizeUpgrade` is `onlyOwner`
- [ ] `_disableInitializers()` in constructor
- [ ] ReentrancyGuard is used on fund operations
- [ ] No `selfdestruct` in the contract
- [ ] Solidity version is ≥ 0.8.20

---

## Ownership Transfer

After deployment, consider transferring ownership to a more secure setup:

### Transfer to multisig

```js
const nfa = await ethers.getContractAt("NonFungibleAgents", PROXY_ADDRESS);

// Transfer ownership to a Safe multisig
const MULTISIG_ADDRESS = "0xYourSafeAddress";
await nfa.transferOwnership(MULTISIG_ADDRESS);

// Verify
console.log("New owner:", await nfa.owner());
```

### Two-step ownership transfer (safer)

If the contract supports OpenZeppelin's Ownable2Step:

```js
// Step 1: Current owner proposes new owner
await nfa.transferOwnership(MULTISIG_ADDRESS);

// Step 2: New owner accepts (from multisig)
await nfa.connect(multisigSigner).acceptOwnership();
```

---

## CI/CD Integration

### GitHub Actions deployment workflow

```yaml
name: Deploy to Testnet
on:
  push:
    branches: [main]
    paths: [contracts/**]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm install
      - run: npm test
      - run: npx hardhat run scripts/deploy.js --network bscTestnet
        env:
          DEPLOYER_PRIVATE_KEY: ${{ secrets.DEPLOYER_KEY }}
          BSC_TESTNET_RPC_URL: ${{ secrets.BSC_TESTNET_RPC }}
          BSCSCAN_API_KEY: ${{ secrets.BSCSCAN_KEY }}
          TREASURY_ADDRESS: ${{ vars.TREASURY_ADDRESS }}
```

**Important:** Never put mainnet deployment in CI/CD without manual approval gates.

---

## Deployment Report Template

```
BAP-578 Deployment Report
═════════════════════════
Date:           2026-03-06
Network:        BSC Testnet (97)
Deployer:       0xDeployerAddress

Addresses:
  Proxy:          0xProxyAddress
  Implementation: 0xImplAddress
  Treasury:       0xTreasuryAddress

Configuration:
  Token name:     Non-Fungible Agents
  Token symbol:   NFA
  Free mints:     3 per user
  Mint fee:       0.01 BNB
  Paused:         false

Verification:
  BscScan:        ✅ Verified
  Test mint:      ✅ Passed
  State reads:    ✅ Working
  Events:         ✅ Emitting

Gas costs:
  Deploy proxy:   ~500,000 gas
  Deploy impl:    ~3,500,000 gas
  Initialize:     ~200,000 gas
  Total cost:     ~0.025 BNB
```

---

## Output Format

When asked for deployment help, respond with:

1. **Prerequisites** (tools, accounts, funding)
2. **Commands to run** (step by step)
3. **Expected outputs** (addresses, confirmations)
4. **Verification steps** (BscScan, test mint, state checks)
5. **Post-deploy configuration** (treasury, free mints, etc.)
6. **Troubleshooting** for common errors

---

## Related Skills

- `bap578`
- `bap578-testing`
- `bap578-security-audit`
