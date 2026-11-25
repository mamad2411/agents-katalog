---
name: eerc-avalanche-skill
description: Activate this skill when you need to design, implement, or explain private eERC tokens on Avalanche (C-Chain, Fuji, or L1), compare ERC-20 vs eERC, choose between Standalone/Converter, integrate selective auditing, or resolve questions about zk-SNARKs, ElGamal, BabyJubJub, Poseidon, compliance (KYC/AML), and private deployment/transfer flows.
---

# eERC on Avalanche: Practical Developer Guide

This skill guides you from zero to production for building solutions with `eERC` (Encrypted ERC) on Avalanche, prioritizing **real privacy + auditability + EVM compatibility**.

## When to use this skill

Use it when the prompt mentions needs like:
- "I want privacy in balances or transfer amounts"
- "I need to comply without exposing data publicly"
- "Converter or Standalone for my token?"
- "How do I migrate from public ERC-20 to eERC?"
- "How does eERC work with zk proofs?"

## Expected outcome

By the end of the workflow you should have:
- Chosen deployment mode (`Standalone` or `Converter`) with justification.
- Defined eERC architecture (contracts, auditor permissions, user flow).
- Technical implementation plan for Avalanche.
- Production criteria (costs, security, compliance, operations).

## Recommended workflow

### Step 1: Confirm if eERC is really needed

1. Identify what data must be confidential:
   - balances
   - amounts
   - counterparties
   - total supply (optional)
2. Verify if total transparency of ERC-20/721/1155 breaks the use case.
3. If the project is regulated (finance, RWA, enterprise), flag selective audit requirements from the start.

Read reference:
- `references/01-context-standards-and-limits.md` (when you need to justify why traditional ERCs don't suffice).

### Step 2: Define deployment mode

Choose **Standalone** if:
- The token is born private from scratch.
- You want to hide total supply.
- The system is natively confidential.

Choose **Converter** if:
- An ERC-20 is already deployed.
- You need optional privacy (wrap/unwrap).
- Public and private circuits coexist.

Read reference:
- `references/02-deployment-modes-and-cases.md` (for quick decision based on product and business).

### Step 3: Design minimal eERC architecture

Include as base:
- `encryptedERC` / encrypted balance storage.
- `Registrar` for auditor keys/permissions.
- `Proof Verifier` to validate zk proofs.
- Audit management (onboarding, rotation, revocation).

Critical decisions:
- What metadata remains public.
- Who can decrypt and under what events.
- Access policy by jurisdiction (if applicable).

Read reference:
- `references/03-cryptography-and-components.md` (if you have doubts about how zk, ElGamal, and Poseidon fit together).

### Step 4: Implement user operational flow

Typical private flow:
1. Create tx and encrypt amount (ElGamal/BabyJubJub).
2. Generate zk proof (Groth16 by default).
3. Verify proof on-chain.
4. Update encrypted balances.
5. Allow selective auditing only if enabled.

Explorers will show that the transaction occurred, but not amounts/balances.

Read reference:
- `references/04-eerc-flow-and-operations.md` (to translate the flow to UX/backend).

### Step 5: Deployment plan on Avalanche

Minimum checklist:
- Environment (Fuji recommended for testing).
- `.env` variables and operational keys.
- Deploy core contracts.
- Register users/auditor.
- Test deposit, transfer, withdraw.

For Converter, validate complete cycle:
- ERC-20 -> eERC (deposit/wrap)
- Private transfer
- eERC -> ERC-20 (withdraw/unwrap)

Read reference:
- `references/05-deploy-converter-step-by-step.md` (if you need concrete operational sequence).

### Step 6: Hardening for production

Always review:
- Gas cost for proof verification.
- Key management and auditor rotation.
- Compliance controls (KYC/AML, jurisdictional restrictions).
- Monitoring and response plan for cryptographic or operational failures.

## Best practices for using this skill in an agent session

1. First ask for business context (what data is sensitive and who needs to see it).
2. Then execute the `Standalone vs Converter` decision.
3. Then land architecture + transaction flow.
4. Close with implementation plan and Fuji testing before mainnet/L1.

If user information is missing, ask only the minimum:
- New token or existing ERC-20?
- What regulatory actor needs access?
- What should remain public?
