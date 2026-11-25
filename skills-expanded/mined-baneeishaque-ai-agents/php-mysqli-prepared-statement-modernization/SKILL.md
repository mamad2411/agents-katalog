---
name: php-mysqli-prepared-statement-modernization
description: Modernizes legacy PHP mysqli endpoints from string-interpolated SQL to prepared statements with bind_param.
category: PHP-Tools
---

# PHP mysqli Prepared-Statement Modernization Skill

> **Skill ID:** `php-mysqli-prepared-statement-modernization`<br>
> **Version:** 1.0.0<br>
> **Type:** Atomic + examples

## Description

Modernize legacy PHP `mysqli` endpoints that use **string-interpolated
SQL** into **prepared statements with `bind_param`**, with three
mandatory side-effects per endpoint:

1. **SQL-injection elimination** — the user-input string concatenation is
   replaced by `?` placeholders + typed bind.
2. **Wire-compat preservation** — the JSON response shape consumed by
   existing clients (Android, Dart, etc.) MUST NOT change. Additive
   fields are permitted; removed / renamed / reshaped fields are NOT.
3. **Error-mode pinning** — `mysqli_report(MYSQLI_REPORT_ERROR |
   MYSQLI_REPORT_STRICT)` is set at the top of any endpoint that wraps
   work in a transaction, so `mysqli_sql_exception` is raised reliably
   even on pre-PHP-8.1 runtimes (where strict error mode is opt-in).

For destructive endpoints (DELETE / UPDATE) the modernization ALSO
wraps the work in an explicit `begin_transaction` / `commit` /
`rollback` block — both to surface FK `RESTRICT` errors as recoverable
exceptions and to future-proof for audit-log row inserts in the same
unit of work. See
[`mysql-fk-hardening-workflow`](../mysql-fk-hardening-workflow/SKILL.md)
for the broader rationale.

## When to Apply

- Existing `mysqli` endpoints with `$con->query("... '" . filter_input(...) . "' ...")`.
- Endpoints whose response shape is consumed by deployed mobile / desktop clients
  (i.e. you cannot freely reshape JSON).
- Destructive endpoints (DELETE / UPDATE) lacking transaction wrapping.

Do NOT apply when:
- The codebase has already migrated to PDO — different idiom; the bind syntax differs.
- The endpoint is read-only AND has zero user input — no SQL-injection vector.

## Procedure

### Step 1 — Identify wire shape

Before editing, **read the existing JSON response** and write down every
field name and type that the response emits. New code MUST emit at least
this same set with the same types.

```bash
grep -E 'json_encode|echo' http_API/<endpoint>.php
```

### Step 2 — Prepared-statement skeleton

For a read endpoint:

```php
<?php
include_once 'config.php';

$param = filter_input(INPUT_GET, 'param') ?? '';

$stmt = $con->prepare("SELECT `id` FROM `tbl` WHERE `col` = ? LIMIT 1");
$stmt->bind_param('s', $param);
$stmt->execute();
$row = $stmt->get_result()->fetch_assoc();

echo json_encode([
    'count' => $row ? 1 : 0,
    'id'    => $row['id'] ?? null,
]);
```

For a destructive endpoint (with transaction wrap + report-strict):

```php
<?php
include_once 'config.php';

mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$id = filter_input(INPUT_POST, 'id', FILTER_VALIDATE_INT);
if ($id === false || $id === null) {
    echo json_encode(['status' => '1', 'error' => 'invalid or missing id']);
    return;
}

$con->begin_transaction();
try {
    $stmt = $con->prepare("DELETE FROM `tbl` WHERE `id` = ?");
    $stmt->bind_param('i', $id);
    $stmt->execute();
    $affected = $stmt->affected_rows;
    $stmt->close();
    $con->commit();
    echo json_encode(['status' => '0', 'affected_rows' => $affected]);
} catch (mysqli_sql_exception $e) {
    $con->rollback();
    echo json_encode(['status' => '1', 'error' => $e->getMessage()]);
}
```

### Step 3 — Bind-type cheatsheet

| Type char | PHP type | Use case |
|---|---|---|
| `i` | int | integer columns (incl. FKs to INT PKs) |
| `s` | string | text columns (incl. dates / timestamps formatted as strings) |
| `d` | double | numeric / decimal columns |
| `b` | blob | binary blobs (sent in chunks via `send_long_data`) |

### Step 4 — `LIMIT 1` for known-singleton SELECTs

Login / lookup-by-PK queries MUST add `LIMIT 1`. The optimizer can stop
scanning earlier; the server returns less data; and ambiguous logic
(what if two users share a username?) becomes explicit.

### Step 5 — Self-Parent Guard (insert / update endpoints)

For endpoints that INSERT or UPDATE a row with a self-referencing FK
column, install the app-layer guard BEFORE running the query:

```php
$parent_account_id = filter_input(INPUT_POST, 'parent_account_id', FILTER_VALIDATE_INT);
if ($parent_account_id !== null && $parent_account_id !== false
    && (int)$parent_account_id === (int)$account_id) {
    http_response_code(400);
    echo json_encode([
        'status' => '1',
        'error'  => 'parent_account_id must not equal account_id',
    ]);
    return;
}
```

This pairs with the DB-side trigger from
[`mariadb-check-autoincrement-trigger-fallback`](../mariadb-check-autoincrement-trigger-fallback/SKILL.md)
for defense-in-depth.

### Step 6 — DELETE-first with diagnostic fallback (FK-protected rows)

When deleting a row protected by `ON DELETE RESTRICT` FKs (e.g. a parent
account referenced by child accounts and/or transactions), the naive
preflight pattern (`SELECT EXISTS(blocker_1); SELECT EXISTS(blocker_2);
… ; DELETE … WHERE not_blocked`) pays for every blocker check on EVERY
call, including the common happy path where no blockers exist.

Prefer **DELETE-first**: run the DELETE, and produce a diagnostic
resultset enumerating ALL active blockers only when the engine raises
`errno 1451` (SQLSTATE `23000`). Crucially, you MUST enumerate blockers
in the diagnostic path — never just parse the constraint name from the
1451 message, because the engine stops at the **first** tripped FK and
reports only that one; you cannot tell from a single failed DELETE
whether the other FKs would also have blocked it.

Three portability tiers, in order of preference for a MariaDB-only
deployment:

| Tier | Form | MySQL 5.x/8.x | MariaDB ≥ 10.1 | Round-trips happy / blocked | Schema object | Prepared? |
|---|---|---|---|---|---|---|
| **A** | Top-level `BEGIN NOT ATOMIC` + `DECLARE EXIT HANDLER FOR 1451` | ❌ syntax error | ✅ | 1 / 1 | none | no (compound blocks cannot be prepared) |
| **B** | `CREATE PROCEDURE sp_delete_X` + `CALL sp_delete_X(?)` | ✅ | ✅ | 1 / 1 | yes (1 routine) | yes (`CALL ?`) |
| **C** | App-side `try { DELETE } catch (1451) { diagnostic SELECT }` | ✅ | ✅ | 1 / **2** | none | yes (both) |

#### Tier A — MariaDB-only, top-level compound block

```sql
BEGIN NOT ATOMIC
  DECLARE EXIT HANDLER FOR 1451
    SELECT 'blocked'   AS outcome,
           EXISTS(SELECT 1 FROM accounts WHERE parent_account_id=X) AS has_children,
           EXISTS(SELECT 1 FROM transactionsv2
                  WHERE from_account_id=X OR to_account_id=X)       AS has_transactions,
           0 AS affected_rows;
  DELETE FROM accounts WHERE account_id=X;
  SELECT CASE WHEN ROW_COUNT()=1 THEN 'deleted' ELSE 'not_found' END AS outcome,
         0 AS has_children, 0 AS has_transactions,
         ROW_COUNT() AS affected_rows;
END
```

Issued via single `$con->query($block)`; outcome decoded by a PHP
`switch ($row['outcome'])`. Constraint: compound blocks cannot be
prepared in MariaDB, so the int param MUST be validated via
`FILTER_VALIDATE_INT` before interpolation. See
`Account-Ledger-Server-PHP/http_API/delete_account.php` for the
canonical implementation, and
`Account-Ledger-Server-PHP/docs/portability.md` § *Efficiency-
ceiling deep dives* for the field-tested explainers on **why
Tier B was not adopted for perf** (stored-routine cache angle),
**why composite covering indexes on the FK columns do not help**
(index-merge is already optimal), and **what `mysqli_report`
polling-vs-exception mode means** for per-endpoint rollout.

#### Tier B — MySQL + MariaDB portable, stored procedure

```sql
CREATE PROCEDURE sp_delete_account(IN p_account_id INT)
BEGIN
  DECLARE EXIT HANDLER FOR 1451
    SELECT 'blocked' AS outcome,
           EXISTS(SELECT 1 FROM accounts WHERE parent_account_id=p_account_id) AS has_children,
           EXISTS(SELECT 1 FROM transactionsv2
                  WHERE from_account_id=p_account_id OR to_account_id=p_account_id) AS has_transactions,
           0 AS affected_rows;
  DELETE FROM accounts WHERE account_id=p_account_id;
  SELECT CASE WHEN ROW_COUNT()=1 THEN 'deleted' ELSE 'not_found' END AS outcome,
         0 AS has_children, 0 AS has_transactions,
         ROW_COUNT() AS affected_rows;
END;
```

PHP side: `$stmt = $con->prepare("CALL sp_delete_account(?)"); $stmt->bind_param('i', $account_id);`.
Adds a schema object (one stored routine) plus a `GRANT EXECUTE` for
the app user; in exchange, the same SQL works on MySQL 5.x/8.x and
MariaDB without rewrite, and the parameter is bound (no interpolation).

#### Tier C — fully portable, two-round-trip blocked path

```php
try {
    $stmt = $con->prepare("DELETE FROM accounts WHERE account_id=?");
    $stmt->bind_param('i', $account_id);
    $stmt->execute();
    // $stmt->affected_rows === 1 => deleted; === 0 => not_found
} catch (mysqli_sql_exception $e) {
    if ($e->getCode() === 1451) {
        // SECOND round-trip: enumerate ALL active blockers
        $diag = $con->query("SELECT
            EXISTS(SELECT 1 FROM accounts WHERE parent_account_id=$id) AS has_children,
            EXISTS(SELECT 1 FROM transactionsv2
                   WHERE from_account_id=$id OR to_account_id=$id) AS has_transactions");
        // …
    } else { throw $e; }
}
```

Use when the target deployment may swap between MySQL and MariaDB
(e.g. Aurora MySQL, RDS MySQL 8.0, PlanetScale, Vitess, TiDB) AND the
extra RTT on the blocked path is acceptable.

#### Decision rubric

- **MariaDB-locked, prefer least schema surface** → Tier A.
- **Multi-engine target OR org migration risk** → Tier B (stored
  procedure migration recipe).
- **No DDL permission OR no routine support (some hosted DBaaS)** →
  Tier C.

#### Common anti-pattern to avoid

`DELETE-first; on 1451, parse constraint name from error message` is
NOT a valid replacement for any tier above. It cannot enumerate
multiple simultaneous blockers because the engine stops at the
first-tripped FK; the user is forced into a staggered
delete-children → retry → delete-transactions → retry cycle.

## Wire-Compat Failure Modes

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Renamed JSON key | Client throws `KeyError` / shows null | Keep legacy key; add new key alongside if needed. |
| Changed type (string → int) | Client deserialization fails (Gson, Moshi, json_decode strict) | Cast back to original type before `json_encode`. |
| Removed key | Same as rename | Add it back, even as null. |
| Top-level shape change (object → array) | Total client breakage | Forbidden. |
| **Pre-existing key typos** (`st atus`, `user name`) | Latent bug — clients may never have read these keys | **Fix silently** — these never worked. Document in commit body. |

The two reference examples shipped with this skill both had pre-existing
key typos (`st atus` and `user name`) in the BEFORE versions. The
modernization fixed them while preserving the intended shape.

## Reference Examples

| File | Before | After | Concerns demonstrated |
|---|---|---|---|
| `select_User.php` | [examples/select_User.before.php](examples/select_User.before.php) | [examples/select_User.after.php](examples/select_User.after.php) | Read endpoint; prepared statement; `LIMIT 1`; wire-compat with `user_count` + `id`; pre-existing `user name` typo fixed. |
| `delete_Transaction_v2.php` | [examples/delete_Transaction_v2.before.php](examples/delete_Transaction_v2.before.php) | [examples/delete_Transaction_v2.after.php](examples/delete_Transaction_v2.after.php) | DELETE endpoint; transaction wrap; `mysqli_report` strict; additive `affected_rows`; pre-existing `st atus` typo fixed. |

## Pitfalls

| Pitfall | Mitigation |
|---|---|
| `bind_param` with wrong type char (`s` for int) | Most drivers coerce silently; harder to debug. Match cheatsheet (Step 3). |
| Forgot `$stmt->close()` before second `prepare` on same `$con` | Some PHP versions throw "Commands out of sync". Always `close()`. |
| `mysqli_report` set globally pollutes other endpoints | Acceptable when set per-endpoint at top; do NOT set in `config.php` without coordinating with read endpoints. |
| Transaction wrap on non-InnoDB table | Silently no-ops; FK RESTRICT errors never raised. Verify engine via [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) `probe-server-flavor.py`. |
| Editing in the workflow/backup repo, not the canonical PHP repo | Run [`canonical-source-vs-workflow-repo-audit`](../canonical-source-vs-workflow-repo-audit/SKILL.md) `audit-repo-role.py <path>` FIRST. |

## Related Skills

- [`mysql-fk-hardening-workflow`](../mysql-fk-hardening-workflow/SKILL.md) — transaction-wrap rationale (FK RESTRICT surfacing).
- [`mariadb-check-autoincrement-trigger-fallback`](../mariadb-check-autoincrement-trigger-fallback/SKILL.md) — self-parent guard DB-side pairing.
- [`canonical-source-vs-workflow-repo-audit`](../canonical-source-vs-workflow-repo-audit/SKILL.md) — pre-edit repo-role check.
- [`remote-mysql-roundtrip-minimization`](../remote-mysql-roundtrip-minimization/SKILL.md) — broader server roundtrip discipline.
