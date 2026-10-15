---
name: nft-developer-skill
description: Use when ERC721/ERC1155 NFT development, Hardhat, Soulbound tokens, or Sepolia deployment comes up. Provides context for NFT mint, verify, and deploy commands.
---

# nft-developer-skill — Agent Context

Hardhat-based NFT development toolkit for EVM blockchains (Sepolia testnet).
Provides ERC1155 and ERC721 template contracts with owner-only mint and optional Soulbound mode.

## Environment

- **Network**: Sepolia testnet
- **RPC**: Alchemy (`ALCHEMY_API_KEY` in `.env.local`)
- **Deployer**: `WALLET_PRIVATE_KEY` in `.env.local`
- **Etherscan**: `ETHERSCAN_API_KEY` in `.env.local`

## Contract templates

| File | Standard | Features |
|---|---|---|
| `contracts/ERC1155Base.sol` | ERC1155 | Owner mint, per-token URI (`setTokenURI`), optional Soulbound |
| `contracts/ERC721Base.sol` | ERC721 | Owner mint, auto-increment tokenId, per-token URI at mint, optional Soulbound |

Both contracts take a `bool soulbound` constructor argument:
- `true` → transfers blocked after mint (credentials, memberships)
- `false` → standard transferable NFT (collectibles, art)

## Commands

### Compile
```bash
npx hardhat compile
```

### Deploy

**ERC1155Base:**
```bash
CONTRACT=ERC1155Base NAME="Collection Name" SOULBOUND=true \
  npx hardhat run scripts/deploy.js --network sepolia
```

**ERC721Base:**
```bash
CONTRACT=ERC721Base NAME="Collection Name" SYMBOL="SYM" SOULBOUND=false \
  npx hardhat run scripts/deploy.js --network sepolia
```

Deploy prints the verify command. Run it immediately after deploy.

### Verify on Etherscan

**ERC1155Base:**
```bash
npx hardhat verify --network sepolia <address> "<Name>" <true|false>
```

**ERC721Base:**
```bash
npx hardhat verify --network sepolia <address> "<Name>" "<SYMBOL>" <true|false>
```

### Set token URI (ERC1155)

Use Hardhat console or add a script:
```js
const c = await ethers.getContractAt("ERC1155Base", "<address>");
await c.setTokenURI(1, "https://...");
```

### Mint

**ERC1155:**
```bash
CONTRACT_ADDRESS=0x... TOKEN_STANDARD=1155 MINT_TO=0x... MINT_TOKEN_ID=1 MINT_AMOUNT=1 \
  npx hardhat run scripts/mint.js --network sepolia
```

**ERC721:**
```bash
CONTRACT_ADDRESS=0x... TOKEN_STANDARD=721 MINT_TO=0x... MINT_TOKEN_URI=https://... \
  npx hardhat run scripts/mint.js --network sepolia
```

## Typical workflow

1. Write or extend a contract in `contracts/`
2. `npx hardhat compile`
3. Deploy with `scripts/deploy.js`
4. Verify on Etherscan immediately (command is printed by deploy)
5. Set token URIs if ERC1155 (`setTokenURI`)
6. Mint with `scripts/mint.js`

## Security

`.env.local` contains the private key. Never display it in responses.
