---
name: fintech-pro
description: "Payments, compliance, auditing, reconciliation, fraud detection, ledger. Use when building or reviewing financial technology systems."
---

# FinTech Pro

## Purpose

Build production financial systems: payment processing, double-entry ledger, compliance (KYC/AML), reconciliation, fraud detection, and audit trails.

## When to Use

**Use this when:**
- Building payment processing, money movement, or ledger systems
- Designing financial data models: accounts, transactions, ledger entries, reconciliation records
- Implementing compliance features such as KYC/AML checks, audit trails, or regulatory reporting

**Use this ESPECIALLY when:**
- Any code touches monetary values — float arithmetic must be replaced with integer-cent storage immediately
- Adding a payment endpoint — idempotency keys, double-entry ledger entries, and DB transactions are all required together
- Designing audit logging — the log must be immutable and capture before/after state for every financial mutation

**Don't skip when:**
- Integrating with an external payment provider — reconciliation gaps discovered weeks later are painful to fix retroactively
- Building reporting or export features — read/write connection separation protects write throughput under heavy reporting load

## Core Patterns

### 1. Double-Entry Ledger

```sql
-- Every transaction is a debit AND a credit
CREATE TABLE ledger_entries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id  UUID NOT NULL REFERENCES transactions(id),
    account_id      UUID NOT NULL REFERENCES accounts(id),
    entry_type      TEXT NOT NULL CHECK (entry_type IN ('debit', 'credit')),
    amount          BIGINT NOT NULL,  -- Cents (integer math, no floats)
    currency        TEXT NOT NULL DEFAULT 'USD',
    description     TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE transactions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status          TEXT NOT NULL CHECK (status IN ('pending', 'settled', 'failed', 'reversed')),
    idempotency_key TEXT UNIQUE,  -- Prevent double processing
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    settled_at      TIMESTAMPTZ
);

CREATE INDEX idx_ledger_account ON ledger_entries(account_id, created_at DESC);
CREATE INDEX idx_ledger_transaction ON ledger_entries(transaction_id);
CREATE INDEX idx_transactions_idempotency ON transactions(idempotency_key);
```

### 2. Idempotent Payment Processing

```typescript
async function processPayment(request: PaymentRequest): Promise<PaymentResult> {
  // Idempotency check (safe retry)
  const existing = await db.transactions.findUnique({
    where: { idempotency_key: request.idempotencyKey }
  })
  if (existing) return existing  // Return same result, don't re-process

  // Validate
  const account = await db.accounts.findUnique({ where: { id: request.accountId } })
  if (account.balance < request.amount) throw AppError.badRequest('Insufficient funds')

  // Process in transaction
  const transaction = await db.$transaction(async (tx) => {
    // Debit sender
    await tx.ledgerEntries.create({
      data: { account_id: senderId, entry_type: 'debit', amount: request.amount }
    })
    // Credit receiver
    await tx.ledgerEntries.create({
      data: { account_id: receiverId, entry_type: 'credit', amount: request.amount }
    })
    // Update balances
    await tx.accounts.update({ where: { id: senderId }, data: { balance: { decrement: request.amount } } })
    await tx.accounts.update({ where: { id: receiverId }, data: { balance: { increment: request.amount } } })

    return tx.transactions.create({
      data: { idempotency_key: request.idempotencyKey, status: 'settled' }
    })
  })

  return transaction
}
```

### 3. Reconciliation

```typescript
// Compare internal records with external (bank, Stripe, etc.)
async function reconcile(date: Date): Promise<ReconciliationResult> {
  const internal = await db.ledgerEntries.findMany({
    where: { created_at: { gte: date, lt: addDays(date, 1) } }
  })
  const external = await stripe.balanceTransactions.list({ created: { gte: date.unix() } })

  const differences: Difference[] = []
  for (const ext of external) {
    const match = internal.find(i => i.idempotency_key === ext.id)
    if (!match) differences.push({ source: 'external', transaction: ext.id, amount: ext.amount })
  }

  if (differences.length > 0) {
    await alertFinance(`Reconciliation mismatch for ${date}: ${differences.length} differences`)
  }
  return { date, internalCount: internal.length, externalCount: external.length, differences }
}
```

### 4. Audit Trail

```sql
-- Immutable audit log (append-only)
CREATE TABLE audit_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,      -- 'account', 'transaction', 'user'
    entity_id   UUID NOT NULL,
    action      TEXT NOT NULL,       -- 'created', 'updated', 'deleted', 'status_change'
    changes     JSONB,              -- { before: {}, after: {} }
    actor_id    UUID NOT NULL,
    ip_address  INET,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Make it immutable via trigger (no updates/deletes)
CREATE FUNCTION prevent_audit_modification() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'Audit log is immutable';
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_audit_immutable
    BEFORE UPDATE OR DELETE ON audit_log
    FOR EACH ROW EXECUTE FUNCTION prevent_audit_modification();
```

### Checklist

- [ ] All monetary values stored as integers (cents/satoshis, never floats)
- [ ] Double-entry ledger for all financial transactions
- [ ] Idempotency keys on all payment endpoints
- [ ] Database transactions wrap every money movement
- [ ] Reconciliation process automated (daily matching)
- [ ] Immutable audit log with before/after snapshots
- [ ] KYC/AML checks before first transaction
- [ ] Separate read/write DB connections (reporting doesn't affect writes)
- [ ] Statement/export generation (PDF, CSV)
- [ ] Fraud detection rules (velocity, amount thresholds, geo anomalies)

## Related Skills

- **postgres-pro** — design ledger table schemas, partitioned audit logs, and reconciliation query plans that back fintech data models
- **security-reviewer** — audit payment endpoints for injection risks, insecure token storage, and access control on financial records
- **soc2-audit-prep** — map audit trail design, access logging, and data retention policies to SOC 2 Type II control requirements
- **gdpr-compliance-scanner** — scan customer financial data storage, PII handling in transaction records, and right-to-erasure implications
- **cloud-security-auditor** — review infrastructure handling cardholder data for PCI DSS scope, encryption at rest, and network segmentation
- **backend-senior-engineer** — design the domain model and service boundaries for accounts, transactions, and fraud detection before implementation
- **ecommerce-pro** — reference for checkout and payment integration patterns when a fintech system powers an e-commerce storefront
- **code-reviewer** — validate payment API contracts for idempotency key conventions, error codes, and webhook signature verification

