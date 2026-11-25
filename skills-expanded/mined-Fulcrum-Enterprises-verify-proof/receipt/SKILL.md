---
name: receipt
description: Keep an agent run receipt, a tamper-evident record of what an agent did (prompts, tool calls, results, outputs) that stores only fingerprints, then anchor it on ProofLedger as one proof, or verify a receipt someone hands you, offline. Use when the user wants proof of what an agent did without keeping what it saw, or asks to check an agent run receipt.
---

# Agent run receipts

Use the `verify-proof` MCP tools. A receipt is a hash chain over the steps of a run. Each step keeps only a SHA-256 fingerprint of its content (salted with a per-run secret), the step type, the time and an optional short label. The content is never written to the receipt and never sent anywhere. Anchoring sends only the chain head, one hash, to ProofLedger (one API proof).

## Record a run

1. Call `start_run_receipt` with a path for the receipt file (for example `<run id>.receipt.json`) and the user's id for the run. Add `agent_name` and `model` if known.
2. For each step, call `add_receipt_step` with the exact text of the step: `prompt` for what the agent was asked, `tool_call` for a call as sent (its JSON), `tool_result` for what came back, `output` for what the agent produced, `note` for anything else. Keep labels short and non-sensitive (the tool name, "customer message"); they are stored in clear.
3. When the run is done, call `anchor_run_receipt`. It needs `PROOFLEDGER_API_KEY`; if it is missing, show the user the steps it returns to get a free key. The anchor usually lands within a minute; if the tool says it has not, call it again later to save the bundle.
4. Tell the user where the receipt is, the proof id, the Polygon transaction and the certificate link, and that `verify-proof receipt verify <file>` checks it offline.

## Check a receipt

1. Call `verify_run_receipt` with the receipt path. It recomputes the chain and checks the head against the bundle inside the receipt, with no network call and no account.
2. To check what one step was, pass `step_index` and the exact `step_content`; this needs the receipt's secret, which the owner may have redacted before sharing.
3. Report plainly: the chain is intact or not, the head is anchored or not, and the block explorer link for the transaction.

## What a receipt shows

- That this exact sequence of steps, in this order, with these fingerprints and times, existed by the anchor time, and has not been changed since.
- Given a step's content and the secret, that the step was made from that exact content.
- Not that the agent's answers were correct, not who ran the agent, and nothing about the content of steps the owner does not disclose.
