---
name: volcano-locks
description: Use for Volcano project locks, distributed leases, leader election, renewable lock guards, fencing tokens, lock contention, and safe backend worker coordination.
---
# Volcano Locks Skill

## Role and pairing

Use project locks when backend workers in one project must elect one holder for
work such as a migration or scheduled rollup. Pair this skill with `volcano-sdk`
and `volcano-platform`.

Locks require a service key with `locks.manage` or full access. Never expose the
key or lease token in browser code.

Use the project's language:

| Project signal | SDK pattern |
|---|---|
| `package.json`, `.ts`, `.js` | JavaScript/TypeScript callback and result envelope |
| `pyproject.toml`, `requirements.txt`, `.py` | Python context manager and typed exceptions |
| `Gemfile`, `.gemspec`, `.rb` | Ruby block and typed exceptions |

## Run work while holding a lock

Prefer the automatic lease helper for work that can outlive one lease period.
It renews the lease and releases it when the callback, context, or block exits.

### JavaScript and TypeScript

```ts
const result = await volcano.locks.withLock(
  'daily-rollup',
  { ttl: 30 },
  async ({ signal, lease }) => runRollup({ signal, fencingToken: lease.fencingToken }),
);

if (result.error) throw result.error;
if (!result.acquired) return { skipped: true };
```

The callback must stop when `signal` is aborted. Contention returns
`{ acquired: false, error: null }`.

### Python

```python
with client.locks.with_lock("daily-rollup", ttl=30) as guard:
    run_rollup(fencing_token=guard.lease.fencing_token)
    if guard.lost:
        raise RuntimeError("Lock ownership was lost")
```

### Ruby

```ruby
client.locks.with_lock("daily-rollup", ttl: 30) do |guard|
  run_rollup(fencing_token: guard.lease.fencing_token)
  raise "Lock ownership was lost" if guard.lost?
end
```

Python and Ruby raise typed SDK exceptions for acquisition or renewal failures.
Stop protected work when the guard reports ownership loss.

## Manage a lease directly

```ts
const acquired = await volcano.locks.acquire('migration', { ttl: 30 });
if (acquired.error) throw acquired.error;
if (!acquired.acquired || !acquired.lease) return;

try {
  const renewed = await volcano.locks.renew('migration', acquired.lease, { ttl: 30 });
  if (renewed.error) throw renewed.error;
} finally {
  const released = await volcano.locks.release('migration', acquired.lease);
  if (released.error) console.error(released.error);
}
```

| JavaScript/TypeScript | Python | Ruby |
|---|---|---|
| `acquire`, `renew`, `release`, `get`, `forceRelease` | `acquire`, `renew`, `release`, `get`, `force_release` | `acquire`, `renew`, `release`, `get`, `force_release` |
| returns result envelopes | returns values or raises typed exceptions | returns values or raises typed exceptions |

Use direct methods only when the automatic lease lifecycle does not fit. Python
and Ruby `renew` return a new immutable lease, so retain the returned value.
Keep the lease private because its token proves ownership.

## Fencing tokens

A delayed holder can continue working after its lease expires. Pass
`lease.fencingToken` to the protected storage operation and reject values lower
than the highest token already accepted.

```sql
UPDATE rollup_state
SET cursor = $1, fencing_token = $2
WHERE id = $3 AND fencing_token <= $2;
```

The lease alone does not block a stale write. The storage check does.

## Inspect and recover

```ts
const { state, error } = await volcano.locks.get('migration');
if (error) throw error;
if (state?.held) console.log(state.expiresAt, state.fencingToken);

const released = await volcano.locks.forceRelease('migration');
if (released.error) throw released.error;
```

Use `forceRelease` only after stopping the old holder and confirming the
protected resource checks fencing tokens. The old holder can run until its next
renewal fails.

## Limits and retries

- Keys use letters, digits, `.`, `_`, `:`, and `-`, up to 128 characters.
- TTL is 5 seconds through 90 days.
- Renewal replaces the expiry; it does not add time to the old expiry.
- Lock requests share a 600-per-minute project limit.
- Rate-limit errors expose `retryAfter` in seconds.
- Acquisition retries one transport failure or HTTP 503 with the same ownership
  and request IDs. Do not invent a new ID for the same uncertain acquisition.

## Verification

- Start two holders and confirm only one reports `acquired: true`.
- Confirm the holder releases after success and failure.
- Confirm the callback stops when renewal aborts its signal.
- Confirm protected writes reject a lower fencing token.
