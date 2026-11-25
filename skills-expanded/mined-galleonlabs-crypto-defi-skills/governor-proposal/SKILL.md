---
name: governor-proposal
description: "Use when reviewing an OpenZeppelin Governor or Cactus-listed proposal, checking clock, quorum, Timelock and exact calldata through execution."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.2.1"
---

# Governor proposal

Produce a contract-grounded proposal brief or lifecycle ledger. Cactus, formerly Tally, helps discover proposals; the deployed Governor and Timelock determine consequential state.

## Bind proposal identity and clock

Collect chain, Governor, proposal ID and canonical description. Read deployed verified ABI/version and actual targets, native values, calldata and description hash. Recompute proposal identity with the matching contract convention and compare events; a human title alone cannot identify executable actions.

Read `state`, `proposalSnapshot`, `proposalDeadline`, `clock` and `CLOCK_MODE` when supported. Resolve token/governor clock rather than assuming the deadline is an EVM block or estimating with a universal block interval. For a different Governor generation or custom extension inspect its actual ABI and counting rules.

## Read voting and payload risk

Inspect proposer/eligibility, voting power at the proposal snapshot, counting mode, quorum at the required historical timepoint and vote totals. Cactus GraphQL requires an API key; missing access does not prevent public contract reads through existing RPC. Avoid unsupported GraphQL fields and paginate indexed data.

Decode every target call, value and delegate/upgrade/permission change. Resolve recipient, affected contract, implementation and cross-chain dependencies. Compare payload with the description and identify any mismatch before preparing a vote or execution handoff. Passing quorum is a voting result, not proof the payload is safe or executed.

## Track queue, readiness and execution

Resolve the actual Timelock role/delay and whether this Governor requires a queue. Read queue/ETA, cancellation and readiness state. A succeeded proposal can still be unqueued, delayed or canceled. Permissionless method availability does not grant user authority to execute it.

Return the exact unsigned action and required value only within requested scope. For an executed proposal inspect receipt/events and affected contract state. Cross-chain messages can leave destination work pending after source execution. If a send or queue response is ambiguous, reconcile the original proposal/operation identity before repeating.

## Worked result

Synthetic Governor clock is timestamp-based. Proposal succeeded; Timelock operation becomes ready at 14:00 UTC, current time 13:45. Report succeeded/queued, 15 minutes until the recorded readiness time. Do not convert the timestamp into block height or call the proposal executed. Destination effects, if any, still need their own proof.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
