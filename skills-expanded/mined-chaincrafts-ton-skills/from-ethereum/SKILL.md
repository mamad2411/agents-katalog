# From Ethereum

Use this skill when Ethereum habits are distorting how a TON feature is being designed, explained, or debugged.

## Inputs

- the original EVM-based assumption or implementation plan
- the TON workflow being built
- the user-facing outcome that must still hold after translation
- the infrastructure or wallet surfaces involved

## Process

1. name the exact Ethereum analogy the team is relying on
2. identify the TON primitive that actually owns that behavior
3. restate the workflow using TON accounts, messages, wallet contracts, or infrastructure terms
4. remove UI copy, backend logic, and review notes that still assume EVM semantics
5. verify the translated plan with a concrete recipe or compare page before implementation

## Guardrails

- do not preserve an Ethereum term if it hides a different TON execution model
- do not treat wallet approval as equivalent to final business success
- do not collapse account, contract, and deployment concepts into one vague "address" model
- do not select RPC or explorer infrastructure by analogy alone

## Output

- a TON-native description of the workflow
- a list of discarded Ethereum assumptions
- a safer implementation path grounded in actual TON behavior
