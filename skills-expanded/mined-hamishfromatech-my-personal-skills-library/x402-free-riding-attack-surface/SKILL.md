---
name: x402-free-riding-attack-surface
description: Applies the first systematic security analysis of x402 agent payments (Ling, Huang, Du, Chen, Zhou, Wu & Wang, arXiv:2605.30998, May 29/June 22 2026; disclosed to vendors before publication) — five formal invariants, four reproducible flaw classes (cross-resource substitution, duplicate-settlement race, allowance overdraft, denial of settlement) with measured resource-leakage ratios up to 100%, and a composed defense triple with zero attacks in 500 adversarial trials at 2.8% overhead. Use when [building or auditing an x402 seller integration, answering 'is my agent payment setup safe?', designing facilitators or per-request settlement rails, or explaining why agent-payment security is now measurable]. NOT for [refundable commerce escrow design — use agent-settlement-protocol-asp-2026 — or non-x402 rails].
---

# x402 Free-Riding: The Formal Attack Surface for Agent Payments

## Why this changes the conversation

For most of its life, x402 security was examined the way early crypto was: one vendor disclosure at a time, one "we found a bug and patched it" at a time. That changed in May 2026, when a research group published the first **systematic** security analysis of x402 — not as a single artifact but as a stack: HTTP semantics, per-chain schemes, SDKs, and deployment choices. The paper is *"Free-Riding the Agentic Web: A Systematic Security Analysis of x402 Payments"* (Ling, Huang, Du, Chen, Zhou, Wu & Wang; submitted May 29, 2026, revised June 22, 2026). It opens by noting the protocol had crossed **130 million all-time transactions** and is embedded in Google Cloud, Cloudflare, and Stripe — then walks through four flaw classes whose measured resource-leakage ratios reach **100%**. All findings were disclosed to affected vendors before publication.

The structural insight: three of the four flaw classes are **merchant-side**. The headline crypto-safety story is usually about payers being drained. Here the service provider streams output it never gets paid for — up to all of it — and can be silently subsidizing free riders without knowing.

## The five invariants any x402 payment must satisfy

| Invariant | Meaning |
|---|---|
| I1 Payment Integrity | If a resource was delivered, a confirmed on-chain transfer from payer to merchant exists. |
| I2 Value Consistency | The transaction value covers the negotiated price. |
| I3 Context Binding | A payment authorization is cryptographically bound to the resource it pays for. |
| I4 Authorization Uniqueness | A nonce-bearing authorization is consumed exactly once, across all concurrent requests. |
| I5 Execution Conservation | Expensive execution begins only after payment is confirmed or locked. |

Each flaw class below violates one or more invariants, resolved to the layer responsible — protocol, SDK, or deployment.

## The four flaw classes

### F1 — Cross-resource substitution (violates I3)
The signed authorization commits to merchant, value, nonce, and expiry — **not to the resource**. A valid signature obtained for resource `r_a` can be detached and re-attached to any other request `r_b` at the same price; verification cannot tell the difference. Reproduced in **100/100 rounds**.

The stack problem: TypeScript and Python SDKs omit the resource check entirely; Java verifies a mutable JSON field it shouldn't trust; Go blindly trusts the stateless facilitator. The fix is protocol-level, not per-implementation: **cryptographic context binding** — extend the EIP-712 schema so the payer signs `Sign(merchant, value, nonce, expiry, H(Method∥URI∥Body))`. Replay against a different resource becomes invalid regardless of implementation quality.

### F2 — Duplicate-settlement race (violates I4)
Verification and settlement are deliberately decoupled in the verify-settle flow; a window opens between the facilitator's validity report and chain confirmation. Multiple requests carrying the same one-time authorization can all clear verification before any reaches on-chain consumption. Reproduction: fifty rounds of twenty concurrent requests produced duplicate delivery in **6% of rounds** — two distinct HTTP 200s with different payloads, one settlement. Related gap: one Python adapter gates settlement on a 2xx status, so a 302 redirect gets served without settling at all.

Fix: **stateful nonce linearization** — a pending-state layer at facilitator ingress using atomic check-and-lock (nonce accepted only if state is null → pending → used after on-chain confirmation).

### F3 — Allowance overdraft (violates I2 and I5)
Under the `upto` dynamic-pricing scheme, the payer signs a spending cap rather than an exact amount, and per-deduction settlements carry no nonce. Verification degrades "from a cryptographic proof of a specific payment event to a stateful check of a remaining limit" — a TOCTOU race. A payer sets allowance to the floor and fires N concurrent requests whose aggregate cost exceeds the cap; all pass the snapshot check and stream output; on-chain, only the first few settle — **after full delivery**.

Measured: a 50-request burst delivered 47,277 wei of value but settled 1,057 wei — a **97.76% leakage ratio**; the long-context variant reaches ~100%.

Fix: **reserve-commit two-phase locking** — escrow the cap before execution, release actual cost to the merchant, refund the difference on completion.

### F4 — Denial of settlement (violates I1 and I5)
A deployment default, not a contract flaw: rate-limit asymmetry between service ingress and settlement egress. Verification ingress is provisioned high; settlement defaults to ~10 tx/s. Flood valid requests: every one is verified and served, but settlement requests beyond the limit get 429s. A 50 req/s burst settled only 5 of 50 — **86.95% leakage**, rising to 100% when the limit blocks everything. A client-driven variant: terminate the TCP connection before the settlement callback fires.

Fix: **failure-closed design** — couple the rate limiter and billing to request ingress, reserving billing capacity before forwarding to the inference engine. The paper's principle: *reliability issues should result in denial of service, not denial of payment.*

## The defense triple (composed)

| Defense | What it does |
|---|---|
| G1 Cryptographic rate limiting | Per-session nonces tracked against payment nonce, per-session token cap, per-token price floor. |
| G2 Adaptive billing | Price the hidden "thinking" compute directly, weighting each token by its expected hidden-compute multiplier — cuts per-call reasoning cost 47%. |
| G3 Bounded-loss streaming | Checkpoint every Δ tokens and settle cumulative cost before continuing — caps worst-case leakage per interruption at ~$0.00047. |

Composed result: **zero successful attacks in 500 adversarial trials**; attacker leverage inverted from 8.7× to 0.9× at **2.8% overhead**.

## The proven structural limit

The paper proves no output-only pay-per-token pricing can be both fair to honest users and bounded against inflation of hidden reasoning tokens — the price of fairness is a **√(1+Θ) manipulation gap**. Fairness and bound are in structural tension; choose which you are defending.

## Builder audit checklist

Before trusting any per-request settlement integration, answer four questions:
1. Is my authorization bound to the resource (context binding, not just merchant/value/nonce)?
2. Is my nonce consumed exactly once across concurrent requests (stateful linearization, not snapshot checks)?
3. Do I lock funds before executing (reserve-commit, not post-hoc settlement)?
4. Do I fail closed on the settlement path (denial of service, not denial of payment)?

If any answer is no, the leak class is known and measured.

## Honest caveats

- Peer-reviewed venue not stated at extraction time; reproduction numbers are author-run (with vendor pre-disclosure, which strengthens them).
- Scale figures (130M transactions; 180M+ / $47.5M in the API-Economy companion) are protocol-side counts, not merchant-side P&L.
- Fix maturity varies: F1 requires a protocol change; F2–F4 are deployable now by sellers/facilitators.
- The five invariants are the analysis frame; other rails (MPP sessions, AP2 authorization) have their own surfaces not covered here.

## Pairs with

`agent-settlement-protocol-asp-2026` (the commerce escrow layer above x402 — this paper is the metered-layer security complement), `x402-production-checklist` (the seven-step seller checklist; add the four-question audit there), `agentic-trust-security-protocols-2026`, `mcp-security-trust`, `agent-settlement-protocol-asp-2026`'s formal-analysis reference (Jiang et al. 18 shared principles).

## A-Tech alignment

- **Open source:** the invariants + flaw taxonomy are a portable audit template for any per-request settlement rail; reproduction harness is the open-science pattern applied to payments.
- **Privacy:** leakage here is revenue leakage, not data leakage — but the gateway-side tier-selection pattern transfers to data-tier routing (see contributor pricing skills).
- **Financial freedom:** a solo dev selling API access on x402 can lose up to 100% of streamed value silently; the 2.8% overhead defense is the difference between a business and a subsidy.
- **Practical:** four-question audit fits in a one-page code review; the attack-surface formalization turns "is it safe?" from a vibe into a checklist.