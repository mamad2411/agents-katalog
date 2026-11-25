# Jettons

Use this skill when a TON product accepts, sends, or displays custom fungible tokens (Jettons).

## Inputs

- the Jetton master address the product needs to interact with
- user wallet addresses that hold or will receive Jettons
- transfer amounts, forward payloads, and tracking identifiers

## Process

1. resolve the user's Jetton wallet address from the master contract
2. construct a transfer message with correct destination, amount, and forward payload
3. submit the transfer via TON Connect or direct signing
4. verify the transfer landed by checking the recipient Jetton wallet on-chain
5. handle failures: bounced messages, insufficient balance, gas exhaustion

## Guardrails

- do not hard-code Jetton wallet addresses; always derive from the master contract
- do not trust the client to confirm transfer success; verify on-chain
- do not assume a user has a deployed Jetton wallet before the first transfer
- do not skip forward payload when tracking is needed for fulfillment

## Output

- correct Jetton wallet resolution logic
- safe transfer message construction
- on-chain verification of completed transfers
