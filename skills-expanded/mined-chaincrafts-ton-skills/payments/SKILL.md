# Payments

Use this skill when a TON product needs to collect value, trigger paid access, or turn wallet approval into a verifiable business outcome.

## Inputs

- payment intent and fulfillment rule
- wallet initiation path
- chain-side action being requested
- confirmation signal required by the product

## Process

1. define the exact state transition that counts as a successful payment
2. map that transition to the signed wallet action and the post-signature evidence you can verify
3. separate wallet approval, chain confirmation, and fulfillment in both code and UI
4. make retries safe for the user and idempotent for the product
5. document recovery behavior for rejection, timeout, and interrupted sessions

## Guardrails

- do not fulfill on intent creation alone
- do not label wallet approval as final payment confirmation
- do not let duplicate retries produce ambiguous product state
- do not hide unresolved pending payments from support and operations surfaces

## Output

- a payment state machine with clear checkpoints
- verifiable fulfillment criteria
- recovery paths for failed or interrupted payment attempts
