---
name: fintech-patterns
version: 1.0.0
min_mindforge_version: 10.2.0
status: stable
triggers: fintech architecture, payment processing system, PCI-DSS compliance, double-entry ledger, financial reconciliation, KYC workflow, AML detection, transaction processing, financial regulation, banking integration, money movement, payment rail design
compose: payment-integration
---

# Skill — Fintech Patterns

## When this skill activates
This skill activates when building payment processing systems, implementing double-entry accounting ledgers, handling financial transactions, integrating with banking APIs, ensuring PCI-DSS compliance, or implementing KYC/AML regulatory workflows.

## Mandatory actions when this skill is active

### Before writing any code
1. Design ledger architecture using double-entry accounting principles: every transaction creates equal and opposite debits/credits, with immutable transaction logs, balance snapshots for performance, and idempotency keys to prevent duplicate charges
2. Map regulatory compliance requirements: PCI-DSS scope (SAQ-A for payment gateway, SAQ-D for card storage), KYC verification levels (identity document, address proof, sanctions screening), AML transaction monitoring thresholds (structuring patterns, velocity checks, geographic risk)
3. Document money movement flows with state machines: pending → authorized → captured → settled (for cards), initiated → processing → completed → reconciled (for ACH), with explicit rollback/refund paths and partial capture support

### During implementation
- Implement financial primitives with arbitrary-precision arithmetic: use Decimal types (never floats) for all monetary amounts, store values in smallest currency unit (cents/paise), handle currency conversion with mid-market rates and spread transparency
- Build idempotent transaction endpoints: require client-generated idempotency keys (UUID v4), cache results for 24 hours, return identical response for duplicate requests (201 for first, 200 for subsequent), prevent phantom charges during network retries
- Design ledger tables with append-only semantics: never UPDATE transaction records, use compensating transactions for corrections, store audit trail with user attribution, implement row-level checksums for tamper detection
- Implement three-phase commit for distributed transactions: reserve funds (pessimistic lock), execute payment processing (call external API), commit or rollback based on response, with automatic retry logic for transient failures and dead letter queue for manual review
- Enforce PCI-DSS compliance boundaries: tokenize card data immediately (Stripe/Adyen tokens), never log full PAN, redact card numbers in UI (show last 4 digits), use TLS 1.2+ for payment gateway communication, implement network segmentation between card data environment and application servers

### After implementation
- Execute financial reconciliation: match internal ledger balances against bank statements (daily), payment gateway settlement reports (batch ID reconciliation), and third-party wallet providers, with automated alerting for discrepancies >$10 or >0.1%
- Validate transaction integrity: sum of all debits equals sum of all credits (ledger balance proof), account balance equals sum of transaction deltas (aggregate consistency check), no orphaned transactions without matching counterparty entries
- Conduct security testing specific to financial systems: SQL injection in payment search, authorization bypass for fund transfers, race conditions in balance checks (concurrent withdrawals), replay attacks on payment endpoints, and IDOR vulnerabilities in transaction history APIs

## Self-check before task completion
- [ ] All monetary amounts use Decimal/BigDecimal types with explicit currency codes (ISO 4217), never floating-point arithmetic
- [ ] Transaction endpoints are idempotent with client-provided idempotency keys, cached responses for duplicate requests
- [ ] Ledger implements double-entry accounting with immutable transaction records, audit trails, and balance proof validation
- [ ] PCI-DSS scope is minimized: no full card numbers stored, tokenization at payment entry point, encryption for sensitive data (AES-256-GCM)
- [ ] KYC/AML workflows implemented: identity verification (document upload + liveness check), sanctions screening (OFAC/EU lists), transaction monitoring (velocity limits, geographic risk scoring)
- [ ] Financial reconciliation automated: daily bank statement matching, payment gateway settlement verification, alerting for discrepancies
- [ ] State machine transitions documented: pending → processing → settled → reconciled, with explicit rollback/refund paths and timeout handling
