---
name: ziros-rust-proof-tool-doctrine
description: Use when choosing between RefinedRust, Verus, Kani, Thrust, Flux, Creusot, and Prusti for ZirOS Rust surfaces, or when shaping code so the proof-bearing boundary fits the permanent doctrine.
---

# ZirOS Rust Proof Tool Doctrine

Use this skill when the task is to choose a Rust verification tool, shape a new
boundary so it is proofable, review a Rust surface for proof-lane fit, or
decide whether evidence can honestly affect ZirOS truth surfaces.

## Start Here

Read these first, in order:

1. `/Users/sicarii/Desktop/ZirOS/AGENTS.md`
2. `/Users/sicarii/Desktop/ZirOS/docs/CANONICAL_TRUTH.md`
3. `/Users/sicarii/Desktop/ZirOS/docs/FORMAL_TOOLCHAIN_INTEGRATION.md`
4. `/Users/sicarii/Desktop/ZirOS/docs/SECURITY.md`
5. `/Users/sicarii/Desktop/ZirOS/zkf-ir-spec/src/verification.rs`
6. `/Users/sicarii/Desktop/ZirOS/formal/refinedrust/README.md`
7. `/Users/sicarii/Desktop/ZirOS/scripts/run_refinedrust_proofs.sh`
8. `/Users/sicarii/Desktop/ZirOS/scripts/run_thrust_checks.sh`

Then use:

- `references/tool-matrix.md`
- `references/decision-tree-and-evidence.md`

## Trigger Conditions

Use this skill when a request mentions any of:

- `RefinedRust`
- `Verus`
- `Kani`
- `Thrust`
- `Flux`
- `Creusot`
- `Prusti`
- "which proof tool"
- "which verifier"
- "unsafe Rust verification"
- "refinement type"
- "can this count in the ledger"
- "how should this module be structured for proof"

## Core Doctrine

- RefinedRust is the default development lane for unsafe, FFI, raw-pointer, and
  layout-sensitive Rust.
- Verus is the default theorem lane for safe proof-core logic and shell
  contracts.
- Kani and Thrust are support lanes only.
- Flux, Creusot, and Prusti are comparison-only in this checkout.
- No tool in this skill proves protocol cryptography by itself.

## Workflow

1. Classify the target:
   - `unsafe_or_layout_capsule`
   - `safe_proof_core`
   - `bounded_regression`
   - `comparison_only`
   - `protocol_proof`
2. Route with `references/decision-tree-and-evidence.md`.
3. Check whether the requested claim is counted, bounded, support-only, or just
   comparative.
4. Refuse claim inflation. Do not let bounded or comparison evidence become a
   ledger upgrade.
5. If the target is too broad for RefinedRust, recommend capsule extraction.

## Output Template

Answer in this shape:

- `primary lane`
- `secondary lane`
- `why this fits`
- `why the other lanes do not fit`
- `evidence required`
- `capsule extraction advice`
- `red flags`

## Hard Rules

- Do not count Kani.
- Do not count Thrust.
- Do not present Flux, Creusot, or Prusti as admitted assurance lanes.
- Do not describe RefinedRust translation output without a passing `dune build`
  as a counted theorem.
- Do not let unsafe or layout-sensitive code stay broad when it can be split
  into a narrow proof-bearing capsule.
- Do not use any tool here to claim Groth16, FRI, Nova, or HyperNova protocol
  soundness.

## Reporting Rules

- Lead with the lane recommendation.
- Be explicit about whether the result could affect `mechanized_total`.
- Name the concrete evidence path and runner command when applicable.
- If recommending RefinedRust, explain where to cut the capsule boundary.
- If rejecting a tool, say why in terms of ZirOS doctrine rather than generic
  preference.
