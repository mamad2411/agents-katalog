# AGENTS.md — Workspace Rules & Autonomous Agent Reference

Refer to [AGENT.md](AGENT.md) for the complete engineering reference, scoring formulas, and category playbooks.

## Strict Rules
1. **NEVER read, view, or inspect `.env` or `.env.*` files.**
2. **NEVER execute shell commands that print environment variables.**
3. **NEVER search for or read external ground truth answer keys.**
4. **Dev (1.0000) and Holdout (1.0000) regression locks are immutable.**
5. **Always verify using `bun run typecheck && bun test && bun run loop-eval`.**

---

## Autonomous AI Financial Controller Agent & Grounded Tools Specification

The AI Finance Controller Agent is an autonomous, multi-step reconciliation controller powered by Vercel AI SDK (`ai@7.0.83`) and grounded deterministic financial operations. Located in `src/pipeline/controller-agent.ts`.

### 1. Multi-Step Agent Reasoning Loop
- **Architecture**: Operates on a sequential multi-step loop (`Plan` $\to$ `Tool Execution` $\to$ `Observe Evidence` $\to$ `Deterministic Verification` $\to$ `Respond`).
- **Bounded Stopping Condition**: Uses `stopWhen: stepCountIs(5)` to prevent infinite recursion while allowing in-depth investigative traversals.
- **Provider Resilience**: Integrates cascading provider fallbacks (Groq $\to$ OpenRouter $\to$ Cerebras $\to$ OpenAI) and an immediate zero-dependency deterministic multi-tool dispatcher for offline operation and network resilience.
- **Audit Trace Logging**: All tool invocations, duration benchmarks, and reasoning paths are logged to `logs/reasoning-trace.jsonl`.

### 2. The 10 Grounded Financial Controller Tools

| # | Tool Name | Description & Grounding Scope | Guardrails & Verification |
|---|---|---|---|
| 1 | `get_run_summary` | Fetches aggregate reconciliation run statistics, record counts, tier breakdown (T1/T2/T3), execution duration, and model used. | Deterministic summary from `RunResult`. |
| 2 | `get_cash_position` | Retrieves multi-currency cash balances, cleared vs. in-transit variance, and complete Bank Reconciliation Statements (BRS). | Decimal fixed-point arithmetic balance validation. |
| 3 | `get_exceptions` | Queries unresolved exception ledger with filtering by `reasonCode` and `currency`. | Filtered slices with reason codes and candidate counts. |
| 4 | `get_exception_detail` | Retrieves side-by-side field diffs, candidate pool records, and actionable finance recommendations for a specific `recordId`. | Computes vendor similarity, amount delta, and drift days. |
| 5 | `explain_match` | Provides verifiable math justification (amounts, counterpart IDs, settlement timestamps, reference overlap) for matched records. | Strict Decimal equality check ($\Delta \le 0.05$). |
| 6 | `force_match` | Proposes a manual override match for exceptions. | **HITL Guardrail**: Requires human controller token authorization before mutating state. Verifies math and FX corridor. |
| 7 | `mark_as_suspense` | Routes unresolvable transactions to suspense clearing (`GL-9999-SUSPENSE-CLEARING`). | **HITL Guardrail**: Generates an approval request token and automated double-entry GL journal template. |
| 8 | `re_run_residuals` | Re-evaluates residual exception pool under calibrated tolerances without modifying base datasets. | Calibrated confidence floor ($\ge 0.70$). |
| 9 | `simulate_what_if` | Simulates tolerance changes or payment gateway MDR adjustments (e.g. 2.36% fee) without state mutation. | Quantifies recoverable match count and projected dollar volume. |
| 10 | `export_audit_proof` | Produces cryptographically signed audit certificate with SHA-256 digests and Merkle root. | Verifies compliance checklist (SOX 404, Section 194 TDS, GST MDR, ISO-20022). |

### 3. Human-in-the-Loop (HITL) Guardrails & Confirmation Flow
- **High-Risk Actions**: `force_match` and `mark_as_suspense` never execute state mutations autonomously.
- **Approval Tokens**: Generate cryptographically unique tokens (`TOKEN_MATCH_...`, `TOKEN_SUSPENSE_...`) registered in `pendingActionApprovals`.
- **API Endpoints**:
  - `GET /api/agent/pending-approvals`: Lists all awaiting approval requests.
  - `POST /api/agent/approve-action`: Accepts `{ token, decision: "approve" | "reject", comment }` with idempotency guard.
  - `GET /api/agent/tools`: Returns the 10 registered tool definitions and descriptions.

---

## Razorpay Gateway & Standard Web Checkout Integration Reference

The project includes an end-to-end integration with Razorpay Standard Web Checkout and Live Test-Mode API Connector in `src/integrations/razorpay.ts`.

### 1. Checkout & Payment Verification Flow
- **Order Creation**: `POST /api/create-order`
  - Validates amount $\ge 100\text{ paise}$ (₹1.00 minimum).
  - Interacts with `POST https://api.razorpay.com/v1/orders` using HTTP Basic Auth.
  - Falls back seamlessly to offline mock orders when credentials are not configured or offline.
- **Frontend Modal**: Standard Razorpay Web Checkout SDK (`checkout.razorpay.com/v1/checkout.js`).
  - Launches modal with `order_id` and public `key_id`.
  - Handles dismissal, payment failure events, and success callbacks.
- **Signature Verification**: `POST /api/verify-payment`
  - Computes $\text{HMAC-SHA256}(\text{order\_id} + "|" + \text{payment\_id}, \text{KEY\_SECRET})$ with constant-time equality.
  - Secret key `RAZORPAY_KEY_SECRET` remains strictly isolated on the backend.

### 2. 50+ Records Ingestion Pipeline (`POST /api/integrations/razorpay/sync`)
- Ingests test-mode records across `/orders`, `/payments`, `/refunds`, and `/settlements`.
- Normalizes raw payloads to typed `FinRecord` schema with Decimal conversion ($100\text{ paise} = \text{₹}1.00$).
- Detects Indian payment rails: UPI VPAs, IMPS RRNs, NEFT/RTGS UTR numbers, and Razorpay standard MDR deductions ($2.36\% = 2\% \text{ fee} + 18\% \text{ GST}$).
- Offline mock fallback guarantees $50+$ records across all 3 source files (`internal-ledger.json`, `processor-export.json`, `bank-statement.json`) for CI & test stability.

---

## Anti-Reward Hacking & Generalization Mandates for Autonomous Loops (/goal)

To prevent autonomous agents from reward-hacking, memorizing single seeds, or gaming evaluation metrics during `/goal` optimization loops, the following constraints are strictly enforced:

### 1. Blind Evaluation & Aggregate-Only Feedback
- **Blind Mode**: Automated improvement loops should use `bun run loop-eval --blind` or `bun run loop-eval --json`.
- **No Record ID Leakage**: Blind mode suppresses item-level record IDs (`B5054`, `L1023`) and claimed counterpart details so agents cannot hardcode record-specific exceptions or narrow vendor strings.
- **No `error-analysis` in Automated Loops**: `bun run error-analysis` compares directly against ground truth answer keys and is strictly an offline human diagnostic tool. Autonomous agents must NEVER execute `error-analysis` or consume its output during `/goal` loops.

### 2. Multi-Seed Cross-Validation as the Generalization Gatekeeper
- **The Cross-Validation Bar**: Any proposed matcher rule or pipeline change must be verified against independent synthetic populations:
  ```bash
  bun run cross-validate
  # or
  bun run loop-eval --cv
  ```
- **Rejection Criterion**: If a change increases fitness on one seed (e.g. seed 999) but causes regressions, false positives, or variance spikes across unseen seeds (`seeds 42, 123, 555, 777, 2026, 4040`), the change must be immediately reverted.

### 3. Generalizable Accounting Heuristics vs. Prohibited Overfitting
- **Permitted**: Broad financial principles (e.g. ISO-4217 currency checks, double-entry balance constraints, Decimal precision arithmetic, Indian GST/TDS tax withholding formulas, standardized reference token extraction).
- **Prohibited (Reward Hacking)**:
  1. Hardcoding specific record IDs (`recordId === "B5026"`).
  2. Narrow regex matching specific mock vendor names or amounts solely present in one seed.
  3. Artificially widening tolerance thresholds (e.g. 100-day settlement windows or 50% fee allowances) without cryptographic or reference token backing.

### 4. Honest Exceptions Beat False Positive Guesses
- **Scoring Formula**: $\text{Fitness} = \text{Recall} - 2 \times \text{FPR}$.
- Genuinely ambiguous edge cases (near-duplicate collisions, multi-currency splits, unallocated bank suspense entries) must remain honest exceptions. The scoring harness awards full points for honest exceptions on unmatchables, while false matches trigger a severe $-2 \times \text{FPR}$ penalty.

