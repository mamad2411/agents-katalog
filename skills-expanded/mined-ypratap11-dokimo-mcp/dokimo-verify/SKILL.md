---
name: dokimo-verify
description: Check a Dokimo evidence package for an AI agent's revenue record — recompute its Merkle proof locally and, if asked, have Dokimo check the commitment against its on-chain anchor on Base. Use when a user or another agent hands you a Dokimo evidence package (fields like leaf, proof_path, root, rule_version_commitment, and for newer closes summary and binding) and asks whether it is genuine, tampered, or anchored. Requires the dokimo-mcp MCP server.
---

# Dokimo evidence check

Dokimo commits each record of an agent's revenue close into a Merkle tree and
anchors a commitment of the root (plus the rule version, and for newer closes the
close summary) on Base. This skill tells you how to check **one record** of such a
package with the `dokimo-mcp` tools, and how to report the result without
overstating it.

## Setup (once)

The tools come from the `dokimo-mcp` MCP server (MIT-licensed, free):

```bash
pip install dokimo-mcp
```

Add it to your agent's MCP config, for example:

```json
{ "mcpServers": { "dokimo": { "command": "dokimo-mcp" } } }
```

If the tools `recompute_merkle_root`, `verify_evidence_package` and
`dokimo_agent_card` are not available, tell the user the server is not installed
and show them the two steps above. Do not guess a result.

## When to use this

- Someone gives you a Dokimo evidence package and asks "is this real?", "was this
  tampered with?", "is it anchored?", or "verify this".
- Someone asks you to check another agent's revenue claim and supplies a Dokimo
  package for it.

Do **not** use it to judge whether a business number is good, complete, or
correctly accounted — it cannot tell you that (see "What a pass means").

## Network calls (disclosed)

- `recompute_merkle_root` — **no network call.** Pure local hashing.
- `verify_evidence_package` — sends the package to Dokimo's public endpoint
  `https://dokimo.augaster.com/a2a`, which checks the on-chain anchor and returns
  its verdict.
- `dokimo_agent_card` — fetches `https://dokimo.augaster.com/.well-known/agent-card.json`.

Before calling `verify_evidence_package`, make sure the user is fine with the
package being sent to Dokimo. If they are not, do the local recompute only and
point them to `https://dokimo.augaster.com/verify.html` to check the anchor
themselves.

## Steps

1. **Check the package shape.** It needs `leaf` (string), `proof_path` (a list of
   `[sibling_hash, "L" | "R"]`), `root` (string) and `rule_version_commitment`
   (string). A package from a newer (v2) close also needs `summary` and
   `binding`; without them it is checked as legacy v1, which only verifies closes
   anchored before the v2 cutover. If fields are missing, say which ones and stop.
2. **Recompute locally first.** Call `recompute_merkle_root(leaf, proof_path)` and
   compare `recomputed_root` with the package's `root`.
   - Different → the record or its proof was altered. Report **not genuine** and
     stop; no network call is needed.
   - Same → the record is consistent with that root. This alone says nothing
     about the anchor.
3. **Check the anchor (with the user's OK).** Call
   `verify_evidence_package(package)`. Read `verified` and each entry of `checks`
   (`recompute`, `onchain_anchor`, `rule_version_bound`).
4. **Report**, using the wording below.

## How to report

- `verified: true` → "This record's proof reaches the root, and Dokimo reports
  that the commitment (root + rule version, plus the close summary for v2) is
  anchored on Base. This covers this one record."
- `verified: false` → name the check that failed:
  - `recompute` failed → the record or proof was altered.
  - `onchain_anchor` failed → that commitment is not anchored (wrong root, wrong
    rule version, wrong summary, or never anchored).
  - an `error` field → report the error; do not call it a failure of the package.
- Always add: "The verdict is Dokimo's answer and is not signed. To avoid relying
  on Dokimo, recompute locally and read the anchor yourself at
  https://dokimo.augaster.com/verify.html."

## What a pass means — and does not

A pass means, for **one record**: its proof reaches the root, and the commitment
is anchored on-chain. It does **not** mean:

- the close's totals were recomputed from all its records (that needs the full
  package — use `/verify.html`);
- the record set is complete (records left out of a close are not detected);
- the revenue is good, collectable, or correctly accounted;
- the buyer was independent of the seller.

Never describe a result as more than this one-record check: do not call it an
audit or a complete verification, do not say Dokimo signed it, and do not say it
removes the need to rely on anyone.

## Example

User: "Is this Dokimo package legit?" (pastes a package)

1. Shape check passes (v2: has `summary` and `binding`).
2. `recompute_merkle_root` → matches `root`.
3. User agrees to the network check → `verify_evidence_package` →
   `verified: true`.
4. Reply: "This record's proof reaches the root, and Dokimo reports the
   commitment is anchored on Base — for this one record. The verdict is Dokimo's
   unsigned answer; you can check the anchor yourself at
   https://dokimo.augaster.com/verify.html. This doesn't confirm the close's
   totals or that every payment was included."
