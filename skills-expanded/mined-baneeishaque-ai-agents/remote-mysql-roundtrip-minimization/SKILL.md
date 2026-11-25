---
name: remote-mysql-roundtrip-minimization
description: Pack multiple inter-dependent MySQL statements (e.g., guard SELECTs + a guarded DELETE) into a single network round-trip via `mysqli::multi_query`, for PHP web servers whose database is hosted on a separate remote host. Includes the four design alternatives (N-roundtrip → optimistic-only → optimistic+fallback → multi_query packed) and the read-protocol for multi-result-set responses.
category: Database
---

# Remote MySQL Round-Trip Minimization Skill (v1)

> **Skill ID:** `remote-mysql-roundtrip-minimization`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## 1. When to Apply

Apply this skill when:

- The PHP web tier and the MySQL database are on **separate hosts** (e.g., app on Render,
  DB on Helio / PlanetScale / managed RDS), so every query incurs real network latency.
- An endpoint issues **≥ 2 statements that share intent** — typically guard SELECTs followed
  by a mutating INSERT/UPDATE/DELETE that depends on the guard outcome, or fan-out reads that
  populate a single response.
- The mutation has **safe race semantics under `NOT EXISTS` guards** (i.e., the mutation
  itself can re-check the precondition atomically).

Do NOT apply when:

- App and DB share a host / Unix socket — round-trip cost is negligible.
- Statements are independent and the caller doesn't care about ordering (use parallel
  connections instead).
- The mutation cannot embed its own precondition (then optimistic+fallback is the ceiling).

## 2. Prerequisite — Server Capability Probe (MANDATORY)

`mysqli::multi_query` requires the server to accept `CLIENT_MULTI_STATEMENTS`. Some managed
hosts disable it. Before adopting this skill, **probe the live target server** via
[`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md):

```bash
python3 .agents/skills/mysql-capability-probe-pymysql/scripts/probe-runner.py \
    --probe   .agents/skills/mysql-capability-probe-pymysql/scripts/probe-multi-statement.py \
    --secrets ~/<private-config-repo>/<project>/act.secrets
```

Exit 0 = proceed; exit 1 = fall back to design (c) optimistic+fallback (§3.3).

## 3. The Four Design Alternatives

### 3.1 Baseline — N Round-Trips (REJECTED)

```php
$exists  = $con->query("SELECT COUNT(*) FROM accounts WHERE account_id=$id");          // RT 1
$kids    = $con->query("SELECT COUNT(*) FROM accounts WHERE parent_account_id=$id");    // RT 2
$txns    = $con->query("SELECT COUNT(*) FROM transactionsv2 WHERE ...=$id");            // RT 3
if ($kids == 0 && $txns == 0) {
    $con->query("DELETE FROM accounts WHERE account_id=$id");                           // RT 4
}
```

**Verdict:** 4 round-trips for the happy path. Unacceptable when each RT is 50-200 ms.

### 3.2 Optimistic-Only — 1 Round-Trip, but No Diagnostic

```php
$con->query("DELETE FROM accounts a WHERE a.account_id=$id
    AND NOT EXISTS (SELECT 1 FROM (SELECT account_id FROM accounts WHERE parent_account_id=$id) c)
    AND NOT EXISTS (SELECT 1 FROM transactionsv2 WHERE from_account_id=$id OR to_account_id=$id)");
if ($con->affected_rows == 0) {
    // Why? Don't know. Could be: account not found, or had children, or had transactions.
}
```

**Verdict:** 1 RT always, but the failure mode is opaque — caller cannot tell the user
*why* the deletion was rejected. Acceptable only when "rejected" is enough info.

### 3.3 Optimistic + Diagnostic Fallback — 1 RT Happy, 2 RT Sad

```php
$con->query("DELETE ...");           // RT 1
if ($con->affected_rows == 0) {
    $row = $con->query("SELECT counts...")->fetch_assoc();  // RT 2 (only on failure)
    // Build precise error message from $row.
}
```

**Verdict:** Optimal happy-path cost; sad path still incurs 2 RT. Use this when the server
does NOT support multi-statement.

### 3.4 Multi-Query Packed — Always 1 Round-Trip ✅ (TARGET PATTERN)

```php
$sql = "SELECT (SELECT COUNT(*) FROM accounts WHERE account_id='$id') AS account_exists,
               (SELECT COUNT(*) FROM accounts WHERE parent_account_id='$id') AS child_count,
               (SELECT COUNT(*) FROM transactionsv2 WHERE from_account_id='$id'
                                                       OR to_account_id='$id') AS transaction_count;
        DELETE a FROM accounts a WHERE a.account_id='$id'
          AND NOT EXISTS (SELECT 1 FROM (SELECT account_id FROM accounts
                                          WHERE parent_account_id='$id') c)
          AND NOT EXISTS (SELECT 1 FROM transactionsv2 WHERE from_account_id='$id'
                                                          OR to_account_id='$id');";

if (!$con->multi_query($sql)) { /* network/syntax error */ }

$row      = $con->store_result()->fetch_assoc();   // first result set: the counts
$con->next_result();                                // advance to DELETE result set
$affected = $con->affected_rows;                    // rows the DELETE actually removed

if ($affected > 0)                  /* success */
elseif ($row['account_exists']==0)  /* "Account not found" */
else                                /* "Cannot delete: $child_count children, $tx transactions" */
```

**Verdict:** ✅ Always 1 RT, with full diagnostic data captured even on failure.

Canonical reference implementation:
[`examples/delete_account.php`](examples/delete_account.php).

## 4. Read Protocol for Multi-Result-Set Responses

`mysqli::multi_query` returns multiple result sets. The read sequence is strict:

```php
$ok = $con->multi_query($sql);                  // dispatches all statements
if (!$ok) { /* immediate error — typically syntax */ }

// FIRST result set
$result = $con->store_result();                  // null if first statement was a mutation
if ($result) {
    $row = $result->fetch_assoc();              // or fetch_all(MYSQLI_ASSOC) for multi-row
    $result->free();
}

// Advance to subsequent result sets
while ($con->next_result()) {
    $r = $con->store_result();
    if ($r) {
        // SELECT result set
        $r->free();
    } else {
        // Mutation result set — check $con->affected_rows / $con->insert_id IMMEDIATELY
        // before the next next_result() call.
    }
}
```

Key gotchas:

1. `affected_rows` and `insert_id` reflect the **current** result set only — capture them
   into a local variable before advancing.
2. `store_result()` returns `false` (not `null`) on mutation statements — distinguish via
   `mysqli_more_results()` / `mysqli_field_count()` if needed.
3. You MUST consume every result set before issuing the next `multi_query`, or the
   connection enters `Commands out of sync` state.

## 5. Statement-Design Constraints

### 5.1 Derived-Table Wrapper for Self-Referential DELETE

MySQL forbids referencing the DELETE target table directly inside a subquery in the same
statement. Wrap in a derived table:

```sql
-- ❌ MySQL Error 1093 — You can't specify target table 'accounts' for update in FROM clause
DELETE FROM accounts WHERE account_id=? AND NOT EXISTS (
    SELECT 1 FROM accounts WHERE parent_account_id=?
);

-- ✅ Wrap in a derived table to break the self-reference
DELETE FROM accounts WHERE account_id=? AND NOT EXISTS (
    SELECT 1 FROM (SELECT account_id FROM accounts WHERE parent_account_id=?) c
);
```

### 5.2 Race-Safety Decision Matrix (TOCTOU between SELECT and DELETE)

Even within one `multi_query` packet, the SELECT-gate and the DELETE-mutation are NOT
atomic. A concurrent INSERT of a child row between them would create an orphaned
constraint. Three layered defences exist:

| Option | Mechanism | Scope of protection | Cost | Verdict |
| --- | --- | --- | --- | --- |
| **A** Guard on the mutation | `WHERE @hc=0 AND @ht=0` (or `NOT EXISTS` re-checked inside DELETE) plus `affected_rows` inspection | Same connection only — concurrent inserter can still slip in between this packet's SELECT and DELETE; the guard merely refuses to delete if the gate flipped on THIS connection's view | Zero | **Mandatory baseline** — always keep guards on the DELETE itself |
| **B** Row-level pessimistic lock | Wrap in a transaction; `SELECT … FOR UPDATE` on the parent and on the EXISTS targets under `REPEATABLE READ` (gap-locks included) | Locks parent row + gap-locks the index range that `NOT EXISTS` scans; concurrent INSERT into that range blocks. Does NOT protect against ungated DELETEs from other code paths | Per-request lock + transaction round-trip overhead; risk of deadlocks; only effective on InnoDB | **Optional** when ungated paths are absent and the workload is low-contention |
| **C** Declarative FK with `ON DELETE RESTRICT` | `ALTER TABLE child ADD CONSTRAINT … FOREIGN KEY (col) REFERENCES parent(pk) ON DELETE RESTRICT` | Database-enforced **forever** across all code paths; concurrent INSERT of a child blocks the parent DELETE atomically | One-time migration cost; requires **InnoDB** on both sides; requires **zero orphans** before ALTER (otherwise ERROR 1452); FKs do **NOT** validate NULL values (top-level rows with NULL parent column are always allowed) | **Preferred long-term defence** when the schema can carry it |

Prerequisites for Option C, verifiable in one shot via
[`probe-fk-readiness.py`](../mysql-capability-probe-pymysql/scripts/probe-fk-readiness.py):

- Both tables use the InnoDB engine. **MyISAM silently drops FK clauses** — the ALTER
  succeeds, the constraint is never created. Convert with
  `ALTER TABLE t ENGINE=InnoDB;` first.
- Required indexes exist on the FK columns (see §5.4).
- Zero orphan rows in the child column.
- The top-level-row encoding for self-referential parents is genuinely NULL (FKs ignore
  NULL); any sentinel like `0` must either be converted to NULL or excluded via a
  trigger-enforced check.

Combine A (always) with C (when feasible). B is reserved for transitional periods
between A-only and C-ready.

### 5.3 Input Sanitisation (Security Caveat)

The reference example uses string interpolation for brevity. **In production, sanitise
or cast inputs** — `mysqli::multi_query` does NOT accept prepared-statement bindings the
way `mysqli::prepare` does. Common defensive patterns:

```php
$id = (int) filter_input(INPUT_POST, 'account_id', FILTER_SANITIZE_NUMBER_INT);
// or
$id = $con->real_escape_string(filter_input(INPUT_POST, 'account_id'));
```

For untyped string fields, consider splitting into a `prepare`-able SELECT and a
`multi_query` mutation if security outweighs the round-trip savings.

### 5.4 Index Prerequisite Verification

Every EXISTS / NOT EXISTS gate added to a packed multi-query must hit an index that
seeks to a single row (or fails fast). Without it, the gate degrades to a full table
scan and the round-trip saving is wiped out by I/O.

Required-index discovery and DDL application:

```bash
# Probe — read-only, exits 0 only when ALL declared indexes exist
python3 .agents/skills/mysql-capability-probe-pymysql/scripts/probe-required-indexes.py \
    --secrets /path/to/secrets.env \
    --check accounts.account_id \
    --check accounts.parent_account_id \
    --check transactionsv2.from_account_id \
    --check transactionsv2.to_account_id

# Apply — idempotent, no-op if the index already exists
python3 .agents/skills/mysql-capability-probe-pymysql/scripts/apply-indexes.py \
    --secrets /path/to/secrets.env \
    --index transactionsv2.from_account_id \
    --index transactionsv2.to_account_id
```

Both scripts are KEY=VALUE-secrets compatible and route through
[`mise-tool-management`](../mise-tool-management/SKILL.md) Layer 5 via
[`probe-runner.py`](../mysql-capability-probe-pymysql/scripts/probe-runner.py) when
invoked from a project whose `mise.toml` does NOT pin python.

### 5.5 EXISTS over COUNT for Pure Gates

When the surfaced fact is **"does any matching row exist?"** rather than **"how many
rows match?"**, prefer `EXISTS` over `COUNT(*)`:

```sql
-- ❌ Forces a full or index scan to count every match
SELECT COUNT(*) FROM child WHERE parent_id=?;

-- ✅ Short-circuits on first match; planner stops after one row
SELECT EXISTS(SELECT 1 FROM child WHERE parent_id=?);
```

Use `COUNT` only when the integer is shown to the user or fed into arithmetic.
For binary gates, `EXISTS` reduces work to one index seek + one row read.

### 5.6 UNION Aggregation Pitfall

`UNION` deduplicates result rows. Combining two single-literal probes via plain
`UNION` collapses them to **at most one row** — destroying any attempt to count
or distinguish them:

```sql
-- ❌ Always returns 0 or 1 row regardless of how many rows match either leg —
--    UNION dedupes (1) and (1) to a single (1).
SELECT COUNT(*) FROM (
    SELECT 1 FROM transactionsv2 WHERE from_account_id=?
    UNION
    SELECT 1 FROM transactionsv2 WHERE to_account_id=?
) t;

-- ✅ Either: project the primary key so UNION cannot dedupe to one row…
SELECT COUNT(*) FROM (
    SELECT id FROM transactionsv2 WHERE from_account_id=?
    UNION
    SELECT id FROM transactionsv2 WHERE to_account_id=?
) t;

-- ✅ …or use UNION ALL when you do not need deduplication…
SELECT COUNT(*) FROM (
    SELECT 1 FROM transactionsv2 WHERE from_account_id=?
    UNION ALL
    SELECT 1 FROM transactionsv2 WHERE to_account_id=?
) t;

-- ✅ …or split into two EXISTS connected by OR (best for pure-gate semantics)
SELECT EXISTS(SELECT 1 FROM transactionsv2 WHERE from_account_id=?)
    OR EXISTS(SELECT 1 FROM transactionsv2 WHERE to_account_id=?);
```

The third form is preferred in packed multi-query gates because each `EXISTS`
short-circuits independently and both can ride dedicated single-column indexes.

### 5.7 Robust Multi-Result-Set Read Loop

Packed multi-queries that mix `SELECT … INTO @vars` (no result set), `DELETE`
(no result set), and a trailing `SELECT @vars` (one result set) break the naive
single-`store_result()` pattern: the first `store_result()` returns `false` because
the first statement produces no row set, and the trailing SELECT is never reached.

The robust pattern walks every result set, capturing the first non-null one:

```php
$row = null;
do {
    if ($res = $con->store_result()) {
        $row = $res->fetch_assoc();
        $res->free();
    }
} while ($con->more_results() && $con->next_result());
```

This pattern is correct regardless of which statement in the packet produces
the row set, and it drains the connection so a subsequent `multi_query` will not
fail with `Commands out of sync`. The reference example
[`examples/delete_account.php`](examples/delete_account.php) uses this loop.

## 6. Composition

| Delegated Concern | Skill |
| --- | --- |
| Server capability probe | [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) |
| Probe stdout/stderr capture | [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) |
| Probe python invocation | [`mise-tool-management`](../mise-tool-management/SKILL.md) §Layer 5 |
| Secrets file resolution | [`dev-env-private-config-symlink`](../dev-env-private-config-symlink/SKILL.md) |
| Commit grouping after refactor | [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) |
- [`php-mysqli-prepared-statement-modernization`](../php-mysqli-prepared-statement-modernization/SKILL.md) —
  PHP-side counterpart: while this skill minimizes roundtrips at the probe/orchestration layer, the PHP skill minimizes per-endpoint roundtrips by replacing string-interpolated SQL with prepared statements that the server can cache.

## 7. Prohibited Behaviors

- Adopting `multi_query` without first probing the live target server (§2).
- Removing `NOT EXISTS` guards from the mutation "because the SELECT already checked" —
  the two are not transactionally atomic (§5.2).
- Mixing prepared-statement binding placeholders inside a `multi_query` string — they are
  silently ignored, leading to either SQL injection (interpolated values) or empty
  parameter slots.
- Skipping the `next_result()` loop — orphaned result sets corrupt the connection state
  for the next query on the same `$con`.
- Using string interpolation in production without input sanitisation (§5.3).

## 8. Cross-References

- [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) — the
  mandatory upstream probe.
- [`examples/delete_account.php`](examples/delete_account.php) — canonical reference
  implementation as actually deployed in Account-Ledger-Server-PHP.
- MySQL Reference Manual — *Multiple Statement Execution* and *mysqli::multi_query*.
