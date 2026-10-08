# Pramanik — Cursor AI Rules

You are working on Pramanik, a privacy-preserving KYC oracle for institutional DeFi built on Chainlink CRE.

## Project Context

Read these files for full context before making any changes:
- DEVELOPMENT.md — complete technical reference
- .cursor/context/PRODUCT.md — product and problem overview
- .cursor/context/ARCHITECTURE.md — system architecture
- .cursor/context/CONTRACTS.md — smart contract specifications
- .cursor/context/CRE_WORKFLOW.md — CRE workflow specifications
- .cursor/context/CONVENTIONS.md — coding conventions

## Critical Rules

### Never Do This
- Never commit .env files
- Never hardcode private keys, API keys, or contract addresses in source code
- Never use Node.js built-ins in CRE workflow code (no node:crypto, no Buffer, no fs)
- Never use async/await in CRE workflows — use .result() pattern
- Never use axios or node-fetch in CRE workflows — use SDK's ConfidentialHTTPClient
- Never allow non-oracle addresses to call setAttestation() or revokeAttestation()
- Never store PII in any variable that exits the extractEligibility() function
- Never add console.log to Solidity contracts (use events)

### Always Do This
- Use Bun (not Node.js) for CRE workflow compilation and running
- Use viem for all encoding/hashing in CRE workflows (WASM-compatible)
- Use Zod to validate all external data (config, API responses, event payloads)
- Use OpenZeppelin 5.x for all standard contract implementations
- Add NatSpec comments to every public Solidity function
- Emit events for every state change in smart contracts
- Save deployed contract addresses to .addresses.json immediately after deployment
- Use conventional commits: feat:, fix:, chore:, docs:

### Architecture Rules
- All private data processing happens inside TEE — nothing private exits the enclave
- Only the oracle address can write to EligibilityRegistry
- Withdrawal from vault is always allowed — never gate exit
- extractEligibility() must remain a pure function with no side effects
- All workflow config (URLs, addresses, rules) goes in config.json — zero hardcoding
- Provider adapters must implement the KYCProvider interface — no direct API calls in workflow

## Tech Stack (Use Exact Versions)
- Solidity: ^0.8.24
- OpenZeppelin: 5.x
- Hardhat: 2.x
- viem: 2.x
- Zod: 3.x
- Express.js: 4.x
- React + Vite + TypeScript: latest
- wagmi + RainbowKit: 2.x
- Bun: latest
- @chainlink/cre-sdk: latest (npm)

## Build Order Priority
Always build in this order:
1. Smart contracts (everything depends on their addresses)
2. Mock API (CRE needs it running to test)
3. CRE workflows (needs contracts + API deployed)
4. Admin API (built on top of contracts)
5. Frontend (last — just a UI layer)
