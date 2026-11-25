# Wallets

Use this skill when a TON product depends on user wallets, account state, or signed operations.

## Inputs

- wallet-dependent user journeys
- supported wallet surfaces
- expected signing and confirmation behavior
- account-state assumptions made by the product

## Process

1. identify where the product depends on wallet ownership, not just an address string
2. document the account state that must be fresh before each critical action
3. model retries around wallet and account behavior, not only frontend state
4. explain wallet-required steps in product language before adding protocol detail
5. confirm how account changes invalidate cached assumptions

## Guardrails

- do not treat wallet connection as equivalent to transaction approval
- do not assume account state remains fresh after reconnect or backgrounding
- do not hide wallet-specific failure states behind generic network errors
- do not design payment or messaging flows before the wallet model is explicit

## Output

- a correct wallet mental model for the product
- explicit account-state assumptions
- user flows that remain coherent across approval, rejection, and account changes
