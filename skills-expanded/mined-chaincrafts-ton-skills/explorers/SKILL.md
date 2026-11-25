# Explorers

Use this skill when a TON workflow needs to be inspected, explained, or cross-checked with a chain-visible surface.

## Inputs

- the address, message, or transaction under inspection
- the expected workflow outcome
- the application-side status currently shown
- any backend or provider data already collected

## Process

1. define the exact chain event or state transition you expect to find
2. inspect the relevant explorer surface for the address, message path, or transaction
3. record the concrete evidence, not just the link
4. compare the explorer finding with backend assumptions and product status
5. turn the result into either a verification rule or a debugging next step

## Guardrails

- do not treat explorer output as the only production contract
- do not use an explorer to compensate for missing product-side state design
- do not assume one explorer's presentation is universal
- do not close an incident before the explorer finding is translated into an actionable fix

## Output

- a verified chain-side explanation of the workflow
- a narrowed debugging path or confirmation rule
- evidence that can be used in review, QA, or incident follow-up
