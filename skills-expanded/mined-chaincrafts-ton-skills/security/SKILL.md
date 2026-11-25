# Security

Use this skill when reviewing a TON product for security risks before launch or after a significant change.

## Inputs

- smart contract source code and deployment configuration
- frontend signing and session logic
- backend fulfillment and verification flows
- integration points with indexers, APIs, and third-party services

## Process

1. enumerate all message handlers and verify access control on each
2. check for replay protection across out-of-order and cross-shard delivery
3. bound all iteration and storage operations against gas exhaustion
4. verify bounce handlers preserve contract invariants
5. audit frontend trust boundaries around TON Connect sessions
6. confirm backend fulfillment depends on on-chain evidence, not client assertion

## Guardrails

- do not assume message ordering is guaranteed across shards
- do not skip bounce handling analysis even for simple contracts
- do not treat wallet connection as equivalent to transaction authorization
- do not rely on client-side assertions for fulfillment decisions

## Output

- a threat model tailored to the specific product
- concrete remediation steps for each identified risk
- verification evidence that mitigations work under adversarial conditions
