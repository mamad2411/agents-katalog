---
name: auditing-wallet-flows
description: Audit frontend and client-side wallet flows in an Ethereum TypeScript repo, including connect state, network switching, signing, rejection handling, and transaction UX. Use when reviewing wallet UX, injected-provider handling, connect or disconnect flows, wrong-network handling, transaction pending states, or signing error paths.
argument-hint: "[target-path-or-scope]"
disable-model-invocation: false
user-invocable: true
---

# Auditing Wallet Flows

Audit the wallet-facing experience without redesigning unrelated application structure.

Inspect:

- wallet connect and disconnect flow
- injected-provider discovery and fallback behavior
- wrong-network and unsupported-network handling
- signature rejection, transaction rejection, and pending state UX
- duplicated provider or client construction
- browser-only assumptions leaking into shared runtime code

Use `references/wallet-audit-checklist.md` to keep the pass consistent.

Output contract:

- Wallet flow area audited
- Evidence files
- Confirmed risks
- Missing verification
- Recommended next skill
