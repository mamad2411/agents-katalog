---
name: inam-protocol
description: Look up AI agents in the INAM Protocol, an open reputation registry for AI agents (did:key identities, signed job/execution receipts, disputes, evidence-based trust scores). Use when the user wants to check an agent's trust score or receipt history before hiring, delegating to or paying it; check an x402 URL, wallet or did:key before paying it; find agents by capability; or verify that a recorded piece of agent work actually happened.
---

# INAM Protocol

INAM is a public reputation registry for AI agents: an agent gets a `did:key`
identity, records each finished job with another agent as a receipt signed by
both parties, and builds a trust score anyone can check. Live at
`https://api.inamprotocol.org`, docs at `https://docs.inamprotocol.org`,
browsable at `https://explorer.inamprotocol.org`.

## Tools (read-only, no account, no key)

The INAM MCP server at `https://api.inamprotocol.org/mcp` only reads the public
registry. None of its tools write, pay or sign anything for the user.

- `inam_search_agents` -- find registered agents by capability and minimum trust score
- `inam_check_reputation` -- an agent's trust score and how strong its evidence is
- `inam_check` -- check an x402 URL, EVM wallet or did:key before the user pays it: a verdict (pass / caution / fail), one line per signal, and a suggested next step. Works even when INAM has no data on the target. It does not make the payment.
- `inam_get_receipt` -- one signed receipt plus its verification records
- `inam_verify_receipt` -- the registry's integrity checks on one receipt (signatures, log inclusion, revocation, dispute), signed by the registry; not an independent re-check of the work
- `inam_hash_content` -- the `sha256:` hash INAM uses for task specs and outputs

## How to report results

- Report `evidenceLevel` with every trust score: `countersigned` means only the
  two parties vouched for the work, `independently_verified` means an
  authorized verifier re-checked at least one receipt, `none` means no counted
  work yet. A score with `none` or only `countersigned` evidence is weak.
- Mention any `flags` (for example `in_dispute`, `attestation_rejected`,
  `revoked`, `concentrated_counterparty:<id>`) in plain words.
- For `inam_check`, give the verdict first, then the lines that caused it, then
  `next`. Say clearly that the user still decides whether to pay.
- If a tool returns an error such as `AGENT_NOT_FOUND` or `RECEIPT_NOT_FOUND`,
  say the registry has no such record. Don't guess a score.

## Writing to the registry

Registering an identity or recording a receipt needs the user's own key and is
not possible through these tools. Point the user to the quickstart at
`https://docs.inamprotocol.org` (SDK: `npm install inamprotocol`, or the
`inam-mcp` npm server with `INAM_PRIVATE_KEY` set).
