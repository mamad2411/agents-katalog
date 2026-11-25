---
name: concurrency-security
description: TOCTOU prevention, distributed locking, idempotency keys, race condition detection for Node.js and serverless environments. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When handling payments, inventory, reservations, file uploads, or any shared mutable state in concurrent/serverless code. Pair with security-reviewer, backend-dev, concurrency specialist.
---

# Concurrency Security (Grok Port)

Patterns to prevent race conditions, double-spend, double-processing, and state corruption under concurrency. Grok-native: Production Contract (ledger for every shared-state decision), preflight checks, friction from real double-charge incidents, compound to shared helpers, palace for "why we used advisory lock here", claim-verif on "this is atomic".

## TOCTOU Prevention (Time-of-Check to Time-of-Use)
```ts
// WRONG
const balance = await db.accounts.findUnique({ where: { id } });
if (balance.amount >= amount) {
  await db.accounts.update({ where: { id }, data: { amount: balance.amount - amount } });
}

// CORRECT: atomic in one statement (or DB constraint)
const updated = await db.$executeRaw`
  UPDATE accounts
  SET amount = amount - ${amount}
  WHERE id = ${id} AND amount >= ${amount}
  RETURNING *
`;
if (updated.count === 0) throw new Error('Insufficient funds or concurrent update');
```

Node FS TOCTOU:
```ts
// WRONG
if (fs.existsSync(filePath)) fs.writeFileSync(filePath, data);

// CORRECT
const fh = await open(filePath, 'wx'); // fails if exists
await fh.writeFile(data); await fh.close();
```

## Distributed Locking (Redis)
```ts
async function acquireLock(key: string, ttlMs: number): Promise<string | null> {
  const token = crypto.randomUUID();
  const result = await redis.set(`lock:${key}`, token, 'NX', 'PX', ttlMs);
  return result === 'OK' ? token : null;
}

async function releaseLock(key: string, token: string) {
  const script = `if redis.call("GET", KEYS[1]) == ARGV[1] then return redis.call("DEL", KEYS[1]) else return 0 end`;
  await redis.eval(script, 1, `lock:${key}`, token);
}
```

Redlock for multi-node quorum when single Redis is not enough.

## PostgreSQL Advisory Locks
```ts
async function withAdvisoryLock<T>(lockId: number, fn: () => Promise<T>): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query('SELECT pg_advisory_lock($1)', [lockId]);
    return await fn();
  } finally {
    await client.query('SELECT pg_advisory_unlock($1)', [lockId]);
    client.release();
  }
}
```

## Idempotency Keys (middleware + table)
Store (key, statusCode, responseBody, expiresAt). On duplicate key return previous response. Unique constraint + TTL cleanup.

## Atomic DB Ops
- `SELECT ... FOR UPDATE` (pessimistic)
- `ON CONFLICT ... DO UPDATE` (upsert, no read gap)
- Conditional updates with version/ETag (optimistic)

## Double-Submit / Webhook Idempotency
- Client: generate key once per form, send in header.
- Webhook: INSERT event_id with unique constraint; on 23505 return 200 "already processed".

## Serverless Cold-Start Races
Use cloud atomic primitives (DynamoDB conditional put, S3 If-None-Match, etc.). Never in-process flags.

## Testing Races
```ts
// Fire N concurrent operations, assert exactly 1 succeeds for debit of full balance
const results = await Promise.allSettled(Array.from({length:10}, () => debitAccount(id, 100)));
const successes = results.filter(r => r.status==='fulfilled').length;
assert(successes === 1);
```

## Grok Integration (Production Contract)
- Primary: security-reviewer + backend-dev.
- Fire on_security_audit, on_api_feature, on_db_change, on_infra_change for any shared-state, payment, reservation, or file handling code.
- Pre-Flight (mandatory for money/inventory/reservation paths): "Is every check-then-act path replaced by atomic op or lock? Idempotency key on all POST/PUT that must be safe to retry? Distributed lock or advisory lock for cross-instance critical sections? Test with concurrent load? What is the failure mode (fail-closed)?"
- Ledger: record every shared mutable resource decision + chosen guard (atomic / lock / idempotency) with task_id + rationale.
- Handoff: list of protected operations, mechanism used, test results (concurrent run), failure mode (what happens on lock timeout or duplicate key).
- Friction + compound: every "user charged twice because two cold starts both saw balance >= amount" or "file overwritten because exists check then write" → compound to preflight "add concurrency guard checklist" or shared atomic helper.
- Palace: "Used Postgres advisory lock for payment processor queue because single-writer semantics required and we already had DB; rejected Redis Redlock because added infra dependency and we wanted exactly-once via DB tx".
- Claim-verification: Two-pass. Grep "if (balance" or "existsSync" or "acquireLock" → read_file actual code + run concurrent test → "Atomic UPDATE with condition exists at services/payment.ts:31 and concurrent test asserts exactly 1 success ✓VERIFIED". Never claim "idempotent" or "no double spend" without reading the guard + evidence.
- Pair with: sast-patterns, concurrency patterns in backend, test-enforcement, preflight, compound-learnings, memory-palace (store "why advisory vs Redlock").

## When to Activate
- Any code touching money, inventory, seats, files, or shared counters under concurrency.
- All serverless POST/PUT handlers that create or mutate.
- Swarm Phase 2 (backend/security) + Phase 3 (audit).
- Before deploys of payment/reservation flows (shipper + security-reviewer).

See .grok/skills/sast-patterns/SKILL.md, backend-patterns, security-review, preflight, test-enforcement. Always test with parallel load (not just sequential). Production Contract: ledger + handoff + preflight + friction on every shared-state change.

"Works in testing" means nothing for concurrency. Only atomic ops, locks, or idempotency + verification under load count.
