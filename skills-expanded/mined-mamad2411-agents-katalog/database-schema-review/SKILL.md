---
name: database-schema-review
description: Runs a structured review of a project's database schema design and migration safety, then reports the results as one table (check, area, status, evidence, recommendation). Covers normalization and data modeling (under-normalized vs. unjustified over-normalization, schema matching actual business entities), data types and constraints (appropriate column types, NOT NULL usage, CHECK constraints/enums for fixed value sets), referential integrity (foreign keys declared at the DB level, ON DELETE/ON UPDATE cascade behavior, orphan-record risk), uniqueness and identity (unique constraints vs. check-then-insert races, primary key/surrogate-key/UUID choice), migration safety (backward-compatible rolling deploys, expand/contract pattern, reversibility, DDL transactions, lock/downtime impact of large-table migrations), schema-vs-application drift, auditability/soft-delete conventions, and multi-tenancy data isolation at the schema level. This is a schema-design and migration-safety review, not a query-performance-tuning review (index-for-a-specific-slow-query analysis and N+1 detection belong to performance-audit) and not an application-security review (SQL injection belongs to cybersecurity-check). Use this whenever the user asks for a "database schema review", "schema review", "schema audit", "schema design review", "database design review", "migration review", "migration safety review", "migration audit", "data model review", "datenmodell prüfen", "datenbankschema prüfen", "datenbankschema-review", "datenbank-audit", "datenbankdesign prüfen", "migrationsprüfung", "migrations-audit", "schema-check", or asks about any specific item this covers ("is this schema normalized", "normalisierung prüfen", "foreign key check", "referenzielle integrität prüfen", "missing foreign keys", "cascade delete behavior", "unique constraint check", "race condition on insert", "primary key choice", "UUID vs auto-increment", "backward compatible migration", "zero-downtime migration", "expand and contract migration", "safe migration pattern", "reversible migration", "rollback plan for migration", "locking migration on large table", "schema drift", "does the schema match the ORM models", "soft delete consistency", "audit columns", "created_at updated_at tracking", "mandantentrennung prüfen", "tenant isolation", "multi-tenancy schema check") — even if they only name one or two of these and not "schema review" explicitly.
---

# Database Schema & Migration Safety Review

A structured, evidence-based review of a project's database schema design and migration history —
not a query-performance tuning pass and not an application-security review. It investigates the
actual migration files/schema definitions and reports one table the user can act on.

Out of scope, by design:

- **Query performance tuning.** Deciding whether a specific slow query needs an index, and
  detecting N+1 query patterns, is `performance-audit`'s job (see its
  `references/backend-performance.md`, checks B3–B4). This skill only cares about indexing that
  exists *for data-integrity reasons* — e.g. a unique constraint that happens to be backed by an
  index — not indexing chosen purely to speed up a particular read.
- **Application security.** SQL/NoSQL injection and other application-security concerns are
  `cybersecurity-check`'s job (see its `references/security.md`, check S1). This skill only checks
  whether integrity rules (uniqueness, required fields, valid value sets, relationships) are
  enforced at the database level — not whether the application safely constructs queries.

A finding belongs here only if its primary concern is schema design correctness or migration
safety, not raw query speed or injection risk.

## Ground rules

- **Evidence or it didn't happen.** Every row needs a concrete pointer — a specific migration file
  and its actual `CREATE TABLE`/`ALTER TABLE` statement, an ORM model's actual column/attribute
  definitions, a schema-dump excerpt, or a `psql \d`/`information_schema` query's real output.
  Never write "the schema looks fine," "seems normalized," or "probably has an index" — either you
  read the actual column definition/constraint/migration and can quote it, or you say plainly you
  couldn't check it.
- **This is schema design and migration safety, not query performance tuning, and not application
  security.** State both boundaries above once, up front, in the report so the user knows where to
  go for the adjacent concerns. The one exception: indexing for data-integrity purposes (unique
  constraints, PK design) is explicitly in scope here — it's the "does this uniquely identify a
  row" question, not the "is this query fast" question.
- **Don't invent scope you can't check, and don't silently drop scope either.** If the project has
  no relational database at all, or schema/migrations aren't tracked in the repo, say so — mark the
  row `➖ N/A` with a one-line reason (e.g. "no relational database in this project — document store
  only, see note below" or "migrations live in a separate ops repo not available here"). Every
  check in this skill gets a row in the output; none are quietly skipped.
- **Read the actual current schema, don't assume it from the ORM model class alone.** An ORM
  model's attribute list is a *claim* about the schema, not proof of it — the migration history
  (or a live schema dump) is the source of truth. Where the two disagree, that disagreement is
  itself a finding (see DB15).
- **Be genuinely thorough.** Don't stop after checking the two or three largest tables because the
  table is getting long — a data-integrity gap on a less-obvious table (a join table, a lookup
  table) is just as real a finding as one on the main entity table.

## Workflow

1. **Identify the database engine(s) and how schema/migrations are managed.** Postgres/MySQL/SQL
   Server/SQLite/etc., and whether the project uses ORM-managed migrations (EF Core Migrations,
   Django migrations, Rails ActiveRecord migrations, Alembic, Sequelize/TypeORM migrations),
   schema-as-code tools (Prisma schema, Flyway SQL migrations, Liquibase changelogs), or hand-rolled
   raw SQL migration files. This determines where the source of truth lives and which conventions
   (reversibility support, transaction wrapping) are available by default.
2. **Read the actual current schema before judging anything.** Reconstruct it from the full
   migration history (read every migration file in order, not just the latest one — a column added
   in migration 3 and altered in migration 47 needs both read to know its current type) or from a
   schema dump/`information_schema` query if migrations aren't the source of truth. Don't infer the
   schema from ORM model classes or documentation alone; treat those as claims to verify against the
   actual migration/dump evidence (see DB15).
3. **Investigate, don't assume.** Read the real `CREATE TABLE`/`ALTER TABLE` statements, real
   constraint definitions, real migration diffs — not just table/column names that sound
   reasonable. A column named `email` with no `UNIQUE` or `NOT NULL` constraint is a real finding
   even though the name suggests it should have both.
4. **Report as one table** in the format below, most severe integrity/safety risks first within
   each area, followed by a prioritized punch list and a separate needs-review list.

## Normalization & data modeling

**DB1 — Normalization level matches actual access patterns.** Flag both directions, not just one:
  - *Under-normalized:* the same fact (a customer's name, an address, a price) is stored
    redundantly in multiple tables/rows with no single source of truth, so updating it in one place
    leaves stale copies elsewhere (a classic update anomaly). Look for repeated column groups across
    tables that should instead be a foreign key to one canonical row.
  - *Unjustified over-normalization:* a simple, frequently-read piece of data is split across three
    or more joined tables with no documented reason, forcing every read of that data through
    multiple joins. This is a legitimate design *if* there's a documented reason (a comment, an ADR,
    a deliberate denormalization-for-read-performance note saying why it's split) — flag it only
    when the split looks accidental or over-engineered relative to how the data is actually queried,
    not merely because joins exist.

**DB2 — Schema matches the actual domain's entities and relationships.** Check whether tables
correspond to how the business actually models its data, not a convenient technical shortcut. A
`users` table that conflates genuinely distinct concepts (e.g. internal staff accounts and external
customer accounts, each with different lifecycle/required fields, jammed into one table with a
`type` discriminator and a pile of nullable columns that only apply to one type) is a modeling
smell — check for tell-tale signs: many nullable columns that are only ever populated for a subset
of rows based on a `type`/`role` column, or a relationship that's modeled as a loose string/enum
field where a proper foreign key to a real entity table would express it.

## Data types & constraints

**DB3 — Column types are appropriate for the data.** Check for:
  - Dates, timestamps, numbers, or booleans stored as free-text `VARCHAR`/`TEXT` instead of the
    engine's native `DATE`/`TIMESTAMP`/numeric/`BOOLEAN` types — this loses validation, sorting, and
    range-query correctness at the database level.
  - An oversized type where a smaller one is exact and sufficient (a `BIGINT` for a value that will
    never exceed a few thousand, `DECIMAL(18,2)` for a flag that's really a boolean) — not a
    critical issue alone, but worth flagging when it's paired with other modeling looseness.
  - `TEXT`/unbounded `VARCHAR` used for a column whose maximum length is actually knowable and
    bounded (a country code, a status string, a postal code) — an unbounded type there forgoes a
    cheap, useful constraint.

**DB4 — NOT NULL is applied where a value is actually always required.** Check columns that the
application logic treats as always-present (a required field in a form, a field read without a
null check downstream) and confirm the database also enforces `NOT NULL` — not just the
application's validation layer. Leaving a column nullable "just in case" when the domain never
allows a missing value pushes a data-integrity guarantee onto every future writer of that table
(the application, a script, a manual fix, another service) instead of the database enforcing it
once, centrally.

**DB5 — CHECK constraints or enum types back columns with a known fixed value set.** For a column
that can only ever hold one of a small, known set of values (a status field, a type discriminator,
a currency code), check whether that's enforced at the database level (`CHECK (status IN (...))`,
a native `ENUM` type, or a foreign key to a lookup table) rather than relying purely on
application-layer validation — an app-only check is bypassable by any other writer and doesn't
survive a future refactor that forgets to re-validate.

## Referential integrity

**DB6 — Foreign key constraints are actually declared at the database level.** For every
relationship the application model assumes (an `order.customer_id` referencing `customers.id`),
confirm the migration/schema actually declares a `FOREIGN KEY` constraint — not just that the ORM
model has a navigation property or the application code always populates the ID correctly.
Application-only enforcement is bypassable by any other writer to the database: a script, another
service sharing the database, or a manual production fix. Grep the migration history for the
table's creation/alteration and confirm the constraint clause is actually present, not inferred
from a plausibly-named column.

**DB7 — ON DELETE/ON UPDATE cascade behavior is a deliberate choice.** For each foreign key found,
check what happens on delete/update of the referenced row: `CASCADE`, `RESTRICT`/`NO ACTION`, or
`SET NULL`. Flag any FK left at the driver/ORM's silent default when that default doesn't match the
relationship's actual intended behavior — e.g. `CASCADE` on a relationship where losing the child
rows silently on parent deletion would be a data-loss surprise, or no cascade rule at all on a
relationship that should clean up dependent rows, leaving the delete to fail or leaving orphans
depending on the engine's default. The evidence for a ✅ here is a comment/decision record or a
cascade clause that clearly matches the domain, not merely "a cascade rule exists."

**DB8 — Orphan-record risk where the application models a relationship with no DB-level FK.** Cross
-reference the application's model relationships (ORM associations, code that joins two tables by
an ID column) against the actual FK constraints found in DB6. Any relationship present in the
application model but absent as a real constraint is a live orphan-record risk — a delete or a
buggy write anywhere in the system can leave dangling references with nothing to prevent or flag it.

## Uniqueness & identity

**DB9 — Unique constraints on business-unique columns.** For any column the business treats as
uniquely identifying (email address, external/third-party ID, username, slug, tax ID), check for an
actual `UNIQUE` constraint or unique index at the database level — not application code that does a
"check if it exists, then insert" sequence, which is race-condition-prone under concurrent requests
(two simultaneous signups with the same email can both pass the "not found" check before either
inserts). A ✅ here requires the constraint to exist in the schema, regardless of what the
application layer additionally does.

**DB10 — Primary key choice is appropriate and its tradeoffs are considered.** Check whether each
table's primary key is a sensible natural key (only when the natural value is truly immutable and
guaranteed unique) or a surrogate key (auto-increment integer or UUID), and specifically for UUID
primary keys, whether the known tradeoff was considered: a random (v4) UUID as a clustered/primary
index key causes index fragmentation and worse insert locality than a sequential integer or a
time-ordered UUID (v7/ULID/COMB-style). This skill only flags the design choice and whether its
tradeoff appears considered (e.g. a v7/ordered UUID chosen deliberately, or a comment/ADR
acknowledging the fragmentation tradeoff for a v4 UUID) — it does not measure the actual index
fragmentation impact, which is `performance-audit` territory.

## Migration safety

**DB11 — Migrations are backward-compatible with the currently-deployed application during a
rolling deploy.** The risk: during a rolling deploy, old application instances keep running against
the new schema for some period. A migration that drops or renames a column the still-running old
code reads/writes will break those instances mid-deploy. Check for the expand/contract pattern on
any column rename or type-incompatible change: a new column is added and dual-written first, data
is backfilled, reads are switched over, and only then — in a later, separate migration/deploy — is
the old column dropped. A single migration that does a destructive rename or drop in one step,
where the application isn't taken fully offline for the deploy, is a real finding.

**DB12 — Migrations are reversible or have a documented rollback plan.** Check whether the
migration tool's down/rollback method is actually implemented (not left as a no-op or throwing "not
supported") for migrations that are safely reversible, and for the ones that genuinely aren't
(a destructive data transformation, a dropped column with data loss) confirm there's an explicit,
written rollback plan (a documented "restore from backup taken before this migration" note) rather
than silence on what happens if the deploy needs to be rolled back.

**DB13 — Migrations run within a transaction where the engine supports DDL transactions, or have a
clear failure story otherwise.** Postgres supports transactional DDL (a migration can be wrapped so
a mid-migration failure rolls back cleanly); MySQL largely does not (DDL statements implicitly
commit). Check the actual migration runner's transaction behavior for the engine in use — for an
engine without transactional DDL, confirm there's a clear answer to "what happens if this multi-
statement migration fails on statement 3 of 5" (a resumable/idempotent migration design, or at
least a documented manual-recovery procedure) rather than an unexamined assumption that it always
completes.

**DB14 — Large-table migrations are evaluated for lock/downtime impact on the target engine.** For
migrations likely to run against a large production table — adding a `NOT NULL` column with a
default value, adding an index, adding a foreign key constraint, changing a column type — check
whether the migration accounts for the target engine's actual locking behavior at scale (e.g.
whether the engine/version can add a column with a default without a full table rewrite, whether
the index is created concurrently/online rather than with a blocking lock) rather than only having
been verified against a small local/dev database. Flag any such migration with no evidence it was
considered for the production table's actual size, and note what "works fine in dev" doesn't prove
here.

## Schema-application drift

**DB15 — Tracked migration history matches what the application actually assumes.** Replay the
migration history (read it start to finish, or actually run it against a scratch database if
feasible) and compare the resulting schema against what the ORM models/query code assume exists
(column names, types, nullability, constraints). A mismatch — a column the code reads that no
migration creates, a constraint the ORM model declares that no migration actually adds — is
evidence of an undocumented manual/production schema change that bypassed the migration history,
which is itself a real risk (the next fresh environment built from migrations alone won't match
production). Report the specific discrepancy found, or state that the two were checked and matched
for the tables inspected.

## Auditability & soft-delete conventions

**DB16 — Audit columns exist where the domain has a regulatory/audit requirement.** If the project
handles data with a plausible audit/compliance need (financial transactions, health records,
anything with an access-log or change-history requirement), check for `created_at`/`updated_at`
timestamps and actor tracking (a `created_by`/`updated_by`/`modified_by` column, or a separate audit
log table) on the relevant tables. No such regulatory domain in this project → `➖ N/A`, state that
reasoning briefly rather than skipping the row.

**DB17 — Soft-delete convention is applied consistently.** If any table uses soft-delete (a
`deleted_at`/`is_deleted` column instead of an actual `DELETE`), check whether that convention is
applied consistently across related tables — a parent table that soft-deletes while a child table
it cascades to hard-deletes (or vice versa) breaks the assumption that "soft-deleted" rows are still
fully present with their relationships intact, and any code path that queries child rows without
also checking the parent's soft-delete state will return orphaned-looking data. No soft-delete
pattern anywhere in this project → `➖ N/A`.

## Multi-tenancy data isolation

**DB18 — Tenant isolation is enforced at the schema/query level, not solely trusted to application
code.** If the system is multi-tenant, check whether tenant separation is backed by the schema
design itself: a `tenant_id` column present (and indexed) on every tenant-scoped table with queries
that filter by it, or a stronger isolation model (separate schema or separate database per tenant).
Flag a design that relies solely on application-layer filtering with no schema-level backstop — a
missing `WHERE tenant_id = ...` in one query path, anywhere in the codebase, becomes a
cross-tenant data leak with nothing at the database level to catch it (e.g. no row-level security
policy, no separate schema boundary). This check's finding is specifically about whether the
*schema* supports or undermines isolation — the full access-control/authorization implications
(who's allowed to request which tenant's data) are `cybersecurity-check`'s territory (its access-
control checks, S11–S12); note that boundary in the report rather than re-doing that review here.
Not a multi-tenant system → `➖ N/A`.

## Output format

Start with 3-4 sentences: what was checked (which database engine(s), which migration/schema-
management tool, and confirmation that the full migration history — not just the latest migration
or the ORM models — was read), what couldn't be reached (no access to a production schema dump to
cross-check against migrations, no non-dev database to replay migrations against, etc.), and the
two boundary notes from Ground rules (not a query-performance review; not an application-security
review) so the user knows where to look for those.

Then ALWAYS use this exact table — one row per check, none omitted:

| # | Check | Bereich/Area | Status | Befund/Evidence | Empfehlung/Recommendation |
|---|---|---|---|---|---|
| 1 | ... | Normalisierung/Datentypen/Referenzielle Integrität/Eindeutigkeit/Migration/Drift/Audit/Multi-Tenancy | ✅/❌/⚠️/➖ | migration file + statement, schema-dump excerpt, or command output | only if not ✅ |

(Match the table's actual language to the conversation's language — the column names above are
illustrative, not a fixed vocabulary. Keep "Befund"/"Evidence" concrete: a migration file path plus
the actual `CREATE TABLE`/`ALTER TABLE` clause, a schema-dump excerpt, or "not found — searched X,
Y, Z". Group rows by area with a subheading or an "Area" column, whichever reads more clearly for
the number of rows involved.)

Status legend:
- ✅ Pass — the safeguard/design choice is present and verified against the actual migration/schema
  evidence (e.g. a real `UNIQUE` constraint, a real `FOREIGN KEY` clause, a real expand/contract
  migration pair)
- ❌ Fail — checked, and the safeguard is missing or the anti-pattern is present (e.g. no `NOT NULL`
  on a field the app treats as required, a destructive rename in a single migration, no FK for a
  relationship the app model assumes)
- ⚠️ Needs manual/DBA review — code review surfaced a plausible concern but confirming it needs a
  judgment call or access this skill didn't have (e.g. "is this denormalization intentional" needs
  a team decision; "will this migration lock the production table" needs the actual table size/
  engine version to confirm)
- ➖ N/A — this check's surface doesn't apply here (state why in one clause — e.g. "no relational
  database in this project", "not multi-tenant", "no soft-delete pattern used anywhere")

End with a **prioritized punch list**: every ❌, ordered by how bad the data-integrity or
deployment-safety consequence would be if left unfixed, each with the one-line fix. Follow it with
a **needs-review list**: every ⚠️, naming who/what would resolve it (a team decision, a DBA check
against real table sizes, a production schema dump to compare against) — don't let these get lost
at the bottom of a long table.
