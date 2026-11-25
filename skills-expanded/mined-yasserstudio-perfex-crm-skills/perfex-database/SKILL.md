---
name: perfex-database
description: Use whenever the user writes SQL DDL for a Perfex CRM module, adds a foreign key referencing `tblcontacts`, `tblstaff`, `tblclients`, `tblinvoices`, or any `tbl*` core table, designs `tbl<module>_<entity>` schema, writes `install.php` / `uninstall.php` DDL, writes a migration or `ALTER TABLE`, or debugs "Cannot add foreign key constraint" / "incompatible" errors. Also trigger when the user says "FK won't create in Perfex", "my module's table has wrong collation", "schema in staging differs from prod", "add a column to my Perfex module table", or mentions `db_prefix()` in a DDL context, `utf8mb4_unicode_ci`, or `VARCHAR(191)` vs `VARCHAR(255)`. Prevents the UNSIGNED-INT-vs-signed-INT trap that silently drops foreign-key constraints pointing at Perfex core tables.
license: MIT
metadata:
  author: yasserstudio
  version: "1.5.0"
---

# Perfex Database Patterns

You are a Perfex CRM database engineer. Your job is to design module-owned tables and migrations that integrate cleanly with Perfex core — matching signed-INT foreign-key conventions, utf8mb4 collation, idempotent DDL — and to handle real-world schema drift between committed `install.php` and the production database.

Perfex uses MySQL/MariaDB with InnoDB, utf8mb4_unicode_ci, and a configurable table prefix (default `tbl`). All custom tables live in the same database as core — namespace them by module name to avoid collisions.

## Table naming

```
tbl<module>_<entity>
```

Examples: `tblmymodule_sessions`, `tblmymodule_logs`. Always use `db_prefix()` in code — the prefix is user-configurable.

## Foreign keys to core tables — the #1 trap

**Perfex core uses signed `INT`, not `UNSIGNED`.** If you create a FK on `UNSIGNED INT` pointing at `tblcontacts.id`, MySQL will reject the constraint with "incompatible" error or silently skip it on older MariaDB versions.

```sql
-- ❌ WRONG — will fail or silently drop the constraint
CREATE TABLE `tblmymodule_items` (
  `id`         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `contact_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_mymodule_contact` FOREIGN KEY (`contact_id`)
    REFERENCES `tblcontacts`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ✅ RIGHT — match core's signed INT
CREATE TABLE `tblmymodule_items` (
  `id`         INT NOT NULL AUTO_INCREMENT,
  `contact_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_mymodule_contact` FOREIGN KEY (`contact_id`)
    REFERENCES `tblcontacts`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Core tables that are common FK targets:
| Table | PK column | Type |
|---|---|---|
| `tblcontacts` | `id` | `INT` |
| `tblstaff` | `staffid` | `INT` |
| `tblclients` | `userid` | `INT` |
| `tblinvoices` | `id` | `INT` |
| `tblcontracts` | `id` | `INT` |
| `tblleads` | `id` | `INT` |

## Charset/collation

Always `utf8mb4 / utf8mb4_unicode_ci` to match Perfex core. Mismatched collation on a FK column also fails constraint creation.

## `install.php` DDL

```php
<?php
defined('BASEPATH') or exit('No direct script access allowed');

$CI =& get_instance();

if (!$CI->db->table_exists(db_prefix() . 'mymodule_items')) {
    $CI->db->query('
        CREATE TABLE `' . db_prefix() . 'mymodule_items` (
            `id`         INT NOT NULL AUTO_INCREMENT,
            `contact_id` INT NOT NULL,
            `name`       VARCHAR(191) NOT NULL,
            `created_at` DATETIME NOT NULL,
            PRIMARY KEY (`id`),
            KEY `idx_contact` (`contact_id`),
            CONSTRAINT `fk_mymodule_contact` FOREIGN KEY (`contact_id`)
                REFERENCES `' . db_prefix() . 'contacts`(`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ');
}
```

Always `if (!table_exists(...))` — activation hooks can run twice if the admin clicks twice or a module is re-activated.

## VARCHAR length: use 191, not 255

MySQL's default `utf8mb4` index-key limit is 767 bytes. `VARCHAR(255)` on a utf8mb4 indexed column overflows. Use `VARCHAR(191)` on any column that will be indexed (unique keys, FKs, lookups). Non-indexed columns can be longer.

## Production drift is real

The `install.php` committed to the repo is the schema at the moment the module was first activated. Over a multi-year lifespan:
- Columns get added manually via phpMyAdmin
- Columns get renamed on staging and never reconciled
- Indexes disappear after a mysqldump/restore

**Before assuming a column exists in production, verify.** Use `SHOW CREATE TABLE` against the live DB. Don't trust `install.php`. Don't trust even a schema migration log.

## Migration pattern — use Perfex's module migrations

Perfex **has** a module migration system (`App_module_migration`, since 2.3). Don't roll your own on `app_init` unless you're repairing drift on an install you can't re-version.

```
modules/my_module/
├── my_module.php        # header: Version: 1.1.2
└── migrations/
    ├── 110_version_110.php
    ├── 111_version_111.php
    └── 112_version_112.php
```

```php
// modules/my_module/migrations/110_version_110.php
defined('BASEPATH') or exit('No direct script access allowed');

class Migration_Version_110 extends App_module_migration
{
    public function up()
    {
        $CI = &get_instance();
        if (!$CI->db->field_exists('new_column', db_prefix() . 'mymodule_items')) {
            $CI->db->query('ALTER TABLE `' . db_prefix() . 'mymodule_items` ADD `new_column` VARCHAR(191) NULL');
        }
    }
}
```

How it works — every one of these is a real trap:
- The target version is the module header `Version:` **with dots stripped**: `1.1.0` → `110`, `1.1.2` → `112`. Filenames must match `/^\d{3}_(\w+)$/` and the class is `Migration_Version_<n>`. Keep the header at three single-digit components or the numbering breaks.
- **Pending migration numbers must be consecutive.** `version()` aborts with `migration_sequence_gap` if two files in the range differ by more than 1 — so `110` → `120` fails outright when an install skips a release. Bump the *last* version component by one per migration (`1.1.0` → `1.1.1` → `1.1.2`); core's own bundled modules number `110, 111, 112…` for this reason.
- **Every `Version:` bump needs a migration file with exactly that number, even with no schema change.** `to_latest()` calls `version(<header number>)`, which returns `migration_not_found` and aborts if `migrations/<n>_*.php` doesn't exist — the Upgrade Database link then errors forever and `installed_version` never advances. Ship an empty `up()` for code-only releases:
  ```php
  class Migration_Version_113 extends App_module_migration { public function up() { /* no schema change in 1.1.3 */ } }
  ```
- The installed version lives in **`tblmodules.installed_version`** (set on first activation from the header), not in `tbloptions`. Migrations between the installed and target numbers run in filename order, each updating `installed_version` as it completes — so a failure mid-sequence leaves the module at the last successful step.
- **Upgrades are not automatic.** When the header version exceeds `installed_version`, Setup → Modules shows an **Upgrade Database** link and the admin must click it (`admin/modules/upgrade_database/<module>`). A deploy alone changes nothing — tell the admin, or your new columns won't exist.
- `up()` still needs `field_exists()` / `table_exists()` guards: a migration that throws halfway through `up()` leaves `installed_version` at the previous step, so that same file re-runs in full on the next click — and the DDL that did succeed is now applied twice.
- `$this->ci->load->dbforge()` is pre-loaded for you; remember dbforge auto-prefixes (see below).

### Fallback: `app_init` self-migration (drift repair only)

If you can't bump the header (e.g. a table was hand-edited on prod and you need to reconcile without a release), an option-gated `app_init` check works. It runs on **every request**, so keep it to one cheap `get_option()` read:

```php
// In module_name.php
hooks()->add_action('app_init', 'my_module_maybe_migrate');

function my_module_maybe_migrate() {
    $installed = get_option('my_module_schema_version') ?: '0';
    if (version_compare($installed, '1.1.0', '<')) {
        my_module_migrate_to_110();
        update_option('my_module_schema_version', '1.1.0');
    }
}

function my_module_migrate_to_110() {
    $CI =& get_instance();
    if (!$CI->db->field_exists('new_column', db_prefix() . 'mymodule_items')) {
        $CI->db->query('ALTER TABLE `' . db_prefix() . 'mymodule_items` ADD `new_column` VARCHAR(191) NULL');
    }
}
```

Always check `field_exists()` / `table_exists()` before DDL — migrations MUST be idempotent. `app_init` fires on every page load.

## The `dbforge->add_column` prefix trap

CI3's `dbforge->add_column()` **auto-prepends** `$this->db->dbprefix` to the table name. If you also pass `db_prefix()`, you get a double prefix and the query fails silently or errors on a non-existent table.

```php
// ❌ WRONG — produces ALTER TABLE `tbltblitems`
$this->dbforge->add_column(db_prefix() . 'items', [
    'new_col' => ['type' => 'VARCHAR(191)', 'null' => true],
]);

// ✅ RIGHT — dbforge adds the prefix itself
$this->dbforge->add_column('items', [
    'new_col' => ['type' => 'VARCHAR(191)', 'null' => true],
]);
```

Note: `$this->db->list_fields()` does NOT auto-prefix — you must pass `db_prefix() . 'tablename'` there. The inconsistency is a CI3 quirk.

```php
// list_fields needs the prefix, add_column does not
$columns = $this->db->list_fields(db_prefix() . 'items');     // ✅
$this->dbforge->add_column('items', $field);                   // ✅
```

## Query builder vs raw SQL

Prefer CI's query builder — it parameterizes automatically:

```php
// ✅ safe
$CI->db->where('contact_id', $id);
$CI->db->insert(db_prefix() . 'mymodule_items', $data);

// ❌ SQL injection risk
$CI->db->query("SELECT * FROM " . db_prefix() . "mymodule_items WHERE id = $id");
```

If you must use raw SQL (complex JOINs, DDL), use `$CI->db->escape()` or bind parameters:
```php
$CI->db->query('SELECT * FROM `' . db_prefix() . 'mymodule_items` WHERE id = ?', [$id]);
```

## Atomic updates for race safety

Whenever you're consuming a one-time token or claiming a lock, update-then-check:

```php
$CI->db->where('token', $token);
$CI->db->where('used', 0);
$CI->db->update(db_prefix() . 'mymodule_tokens', ['used' => 1, 'used_at' => date('Y-m-d H:i:s')]);

if ($CI->db->affected_rows() !== 1) {
    // token was already consumed in a concurrent request
    return false;
}
```

See `perfex-security` for the full token lifecycle pattern.

## `list_fields()` vs `field_exists()` — choosing the right check

Both verify column existence, but they serve different purposes:

```php
// field_exists — checks a single column, cheap, returns bool
if (!$CI->db->field_exists('new_col', db_prefix() . 'mymodule_items')) {
    // add the column
}

// list_fields — returns ALL column names as array, one SHOW COLUMNS query
$columns = $CI->db->list_fields(db_prefix() . 'mymodule_items');
if (!in_array('new_col', $columns)) {
    // add the column
}
```

**Use `field_exists()`** when checking one or two specific columns (migrations, guards). **Use `list_fields()`** when you need to check multiple columns in a loop — one query beats N `field_exists()` calls. Both require `db_prefix()` in the table name (unlike `dbforge`).

## Dynamic column pattern (multi-currency pricing)

Perfex core uses a dynamic column pattern for per-currency item pricing. Instead of a separate table, it adds `rate_currency_{currency_id}` columns to `tblitems` on demand:

```php
$columns = $this->db->list_fields(db_prefix() . 'items');
$this->load->dbforge();

foreach ($currencies as $currency) {
    $col = 'rate_currency_' . $currency['id'];
    if ($currency['isdefault'] == 0 && !in_array($col, $columns)) {
        $this->dbforge->add_column('items', [
            $col => [
                'type' => 'decimal(15,' . get_decimal_places() . ')',
                'null' => true,
            ],
        ]);
    }
}
```

Key behaviors:
- Base currency price lives in the `rate` column; non-base currencies get `rate_currency_X`
- Columns are created on first save via `dbforge` (see `Invoice_items_model::add()`)
- When a currency is deleted, `Currencies_model::delete()` drops the matching column
- Import/export discovers columns via `list_fields()` — columns must exist before import can populate them
- The model detects these columns by prefix: `strpos($column, 'rate_currency_') !== false`

This pattern works for any feature where you need per-entity pricing across a small, admin-managed set of variants. Don't use it for high-cardinality dimensions — a junction table is better past ~10 columns.

## Backup before destructive ops

Before any `ALTER TABLE`, `DROP COLUMN`, or `UPDATE` without WHERE, dump the target table:
```bash
mysqldump -u USER -p DB tblmymodule_items > /tmp/pre_migration_$(date +%s).sql
```

## Related skills

- **`perfex-module-dev`** — `install.php` is where module schema lives; this skill covers the DDL inside it.
- **`perfex-customfields`** — `tblcustomfields` schema quirks (`only_admin`, the `disalow_client_to_edit` typo) that affect DDL generation.
- **`perfex-security`** — the atomic-UPDATE-with-`affected_rows()` pattern for race-safe token consumption.

## Upstream docs

- CI3 database: https://codeigniter.com/userguide3/database/
- MySQL utf8mb4 index limit: https://dev.mysql.com/doc/refman/8.0/en/innodb-limits.html

---

*Verified against Perfex CRM 3.4.0 core source on 2026-09-15 with `scripts/verify-against-core.sh`. Version-specific notes in the text are from official changelogs.*
