# Smart Contracts

Use this skill when developing, analyzing, or deploying a smart contract to the TON blockchain.

## Inputs

- required contract logic and data structures
- performance and security guarantees
- messaging patterns between actors

## Process

1. identify state variables and state init structure
2. map out valid and invalid message paths
3. bound data sizes to avoid gas limit exhaustion
4. implement bounce handling and replay limits
5. write validation and unit tests
6. deploy contract and verify operations

## Guardrails

- do not store large nested structures without dictionaries
- do not process unbounded lists in a single transaction
- do not forget to handle bounded errors and un-parsable messages

## Output

- safe and testable FunC or Tact source
- verified state transitions
- reliable compiled boc deployment artifacts
