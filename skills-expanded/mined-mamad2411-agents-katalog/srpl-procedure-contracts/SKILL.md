---
name: srpl-procedure-contracts
description: "Use for SRPL procedure semantics, ProcedureContract, ContractHash and compatibility."
category: andromeda-srpl
---

# srpl-procedure-contracts

## When to use
Work touches SRPL procedures or contracts.

## Purpose
Use for SRPL procedure semantics, ProcedureContract, ContractHash and compatibility.

## Process
- Ensure explicit types, cardinalities, permissions, read/write sets, isolation and resource policy.
- Hash canonical semantic forms, not source text.
- Detect breaking/additive/deprecated/rejected changes.
- Reject SQL dynamic text and implicit result shapes.

## Expected output
- Procedure contract design/review.

## Guardrails
- No SELECT *, no implicit NULL, no shape-shifting records.

## Andromeda baseline
- Rust 1.95.0 / Edition 2024 / resolver 3.
- QUIC + custom Protobuf RPC; no gRPC and no JSON native protocol.
- Procedure-only application surface and SRPL contracts.
- WAL before visible commit; recovery and audit are mission-critical.
- Worker artifacts belong under `.work/codex/<task-slug>/`.
