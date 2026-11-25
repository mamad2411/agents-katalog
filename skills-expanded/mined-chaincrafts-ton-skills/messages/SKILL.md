# Messages

Use this skill when a TON product feature depends on understanding what message is being sent, why it is being sent, and how to verify the outcome.

## Inputs

- user or system action being modeled
- destination contract or account
- payload and value requirements
- confirmation rule used by the product

## Process

1. restate the feature as a message-level intent
2. identify the destination, value, and payload boundaries that matter
3. review the assumptions the receiving side will make about that message
4. connect product confirmation logic to the actual message outcome
5. inspect failures by comparing intended message shape to the one actually produced

## Guardrails

- do not design a payment or wallet flow without naming the message it depends on
- do not collapse transport, payload, and business outcome into one generic success state
- do not treat failed confirmation as sufficient evidence of malformed messages without inspection
- do not rely on vague transaction wording when message-level reasoning is required

## Output

- a clear message model for the feature
- explicit payload and destination assumptions
- a verification path tied to message outcomes rather than vague UI events
