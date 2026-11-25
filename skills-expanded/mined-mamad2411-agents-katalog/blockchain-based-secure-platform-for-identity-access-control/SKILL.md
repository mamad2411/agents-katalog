# Blockchain Secure Platform Cursor Rules

You are working in a security-sensitive blockchain and cybersecurity repository. Treat all implementation, documentation, configuration, and test changes as reviewable engineering work.

## Always do

- Read `README.md`, `ARCHITECTURE.md`, `SECURITY.md`, and the applicable ADR before changing behavior.
- State whether the work targets local MVP, testnet, pilot, or production readiness.
- Enforce authorization in the contract and backend; never rely on frontend checks.
- Add tests for authorized and unauthorized callers, invalid transitions, duplicate operations, revocation, and failure recovery when relevant.
- Keep identity documents, personal data, secrets, private keys, seed phrases, and credentials out of code, logs, fixtures, screenshots, and prompts.
- Emit and document stable events for auditable on-chain state transitions.
- Keep indexers idempotent and capable of retry, confirmation, reorganization handling, and reconciliation.
- Update documentation, ADRs, `.env.example`, migrations, and runbooks when interfaces or operations change.
- Validate keyboard behavior, semantic labels, focus, error messages, and accessible states for UI work.

## Never do

- Do not use `tx.origin` for authorization or add hidden administrative bypasses.
- Do not silently broaden a role, minting authority, transfer policy, or data-retention rule.
- Do not treat a UI role label, database projection, wallet address, NFT, hash, or DID reference as stronger evidence than the approved policy allows.
- Do not commit a secret, production address, real identity record, or live deployment credential.
- Do not suppress or delete failing tests to make a task pass.
- Do not claim audit completion, production readiness, legal ownership, or institutional endorsement without evidence.

## Preferred implementation approach

Make the smallest coherent change. Use the repository's default Solidity/Hardhat/OpenZeppelin, FastAPI/Pydantic/Web3.py, PostgreSQL, Next.js/TypeScript, Cypress, axe-core, Docker Compose, and GitHub Actions stack unless an ADR changes it. Use Conventional Commits. Explain trust-boundary, security, privacy, migration, and rollback consequences in the pull request.

When uncertain, ask for the missing invariant or record a conservative assumption. End each task summary with changed files, commands run, test status, known limitations, and follow-up work.
