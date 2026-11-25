# Telegram Mini Apps

Use this skill when the TON experience runs inside Telegram and the product has to coordinate Telegram runtime state with wallet-driven actions.

## Inputs

- launch and re-entry conditions
- required Telegram capabilities
- wallet-dependent actions
- mobile-first UX constraints

## Process

1. map what comes from Telegram, what comes from your backend, and what comes from wallet state
2. define the cold-open flow before optimizing the warm-open flow
3. make wallet-dependent actions resumable after reopen or reconnect
4. keep the UI robust when Telegram context changes faster than on-chain confirmation
5. test the path where the user leaves Telegram and returns mid-flow

## Guardrails

- do not let Telegram init data stand in for wallet authorization
- do not assume a reopened mini app still has valid in-memory state
- do not bury transaction-critical feedback in transient toasts only
- do not design flows that require precise desktop-style input patterns

## Output

- a resumable mini app flow
- clear boundaries between Telegram, app, and wallet state
- mobile-safe recovery behavior for interruptions
