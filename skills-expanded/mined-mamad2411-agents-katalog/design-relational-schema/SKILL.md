---
name: design-relational-schema
description: Designs a normalized relational schema from requirements — entities, relationships, PK strategy (surrogate bigint vs natural vs UUIDv7/ULID), 1:1/1:N/M:N and inheritance modeling, 3NF/BCNF normalization, invariants encoded as UNIQUE/CHECK/FK/exclusion constraints, and deliberate read-path denormalization with stated consistency tradeoffs.
when_to_use: When starting a new database or a new table cluster and you need the logical+physical model — turning requirements/an ERD into tables, choosing keys, modeling cardinalities and inheritance, normalizing, then deciding where to denormalize. Distinct from db-migration-safety (altering a live table safely) and optimize-sql-query (speeding up a query against an existing schema).
---

## When to Use

Reach for this skill when you're designing the **shape of the data**, before any table exists:

- "Model these requirements / this ERD as tables"
- "Should this PK be a UUID or a bigint? natural or surrogate? composite?"
- "How do I model users↔roles (M:N) / orders→items (1:N) / a polymorphic comment?"
- "Normalize this — I've got repeating columns / update anomalies / duplicated data"
- "Where should I denormalize for a read-heavy dashboard, and what breaks?"
- Choosing column types: enum vs lookup table, soft vs hard delete, audit columns, money/time precision

NOT this skill:
- Changing a table that already has rows/traffic (locks, backfills, rollback) → **db-migration-safety**
- A query against an existing schema is slow → **optimize-sql-query**
- You need an append-only, replayable, audit-complete domain model → **design-event-sourcing-cqrs**
- Computing prices/tax/rounding/FX (the math, not the column type) → **money-decimal-arithmetic**
- Storing/converting/comparing timestamps & DST correctly → **datetime-timezone-correctness**
- Shaping items/documents for a non-relational store (DynamoDB/Mongo/Cassandra) around access patterns → **model-nosql-data**

## Steps

1. **Extract entities, attributes, relationships from requirements — nouns→tables, verbs→relationships.** List each entity, its attributes, and for every pair the cardinality (1:1 / 1:N / M:N) and optionality (mandatory vs nullable side). Mark each attribute's identity role: is it a candidate key (naturally unique, immutable), or descriptive? Write functional dependencies (`A → B`: A determines B) — they drive normalization in step 3. One table = one entity type; if an attribute is itself a list ("tags", "phone numbers"), it's a separate table, not a CSV column or `jsonb` dumping ground.

2. **Pick a PK strategy per table — default to surrogate, choose the integer/UUID flavor deliberately.**

   | Strategy | Use when | Avoid when |
   |---|---|---|
   | **`bigint GENERATED ALWAYS AS IDENTITY`** | Single-DB, internal IDs, smallest/fastest index, FK-heavy — **default** | IDs leak to clients/URLs and count/sequence is sensitive; multi-master inserts |
   | **`uuid` v7 / ULID** (time-ordered) | IDs generated client-side or across shards, exposed in URLs, need merge without collision | You can use bigint and don't expose the ID — 16B vs 8B and bigger indexes |
   | **`uuid` v4** (random) | Only if unguessability matters *and* you accept index-locality cost | Hot insert paths — random UUIDs fragment B-tree pages and bloat WAL |
   | **Natural key** (email, ISO code, slug) | Truly immutable, single-attribute, externally governed (`country.iso2`, `currency.code`) | It can ever change or isn't guaranteed unique — a changing PK cascades through every FK |
   | **Composite key** | Junction tables (`(a_id, b_id)`); rows identified only by the combination | A tempting single surrogate would be simpler and the combo isn't queried as a unit |

   Rules: use a **surrogate `bigint` IDENTITY by default**; reach for **UUIDv7/ULID (not v4)** the moment IDs cross a process boundary or are client-generated; never expose a sequential surrogate where the sequence is sensitive (use UUIDv7 instead); a natural key still deserves a `UNIQUE` constraint even when you also keep a surrogate PK. Never use `serial`/`SERIAL` (legacy, ownership/permission footguns) — use `GENERATED ALWAYS AS IDENTITY`.

3. **Normalize 1NF → 2NF → 3NF/BCNF; stop at BCNF.** Eliminate the anomaly classes in order:
   - **1NF** — atomic columns, no repeating groups, no arrays-as-CSV. Split `phone1, phone2, phone3` and `tags TEXT` into child rows.
   - **2NF** — no non-key attribute depends on *part* of a composite key. In `order_item(order_id, product_id, product_name)`, `product_name` depends only on `product_id` → move it to `product`.
   - **3NF** — no transitive dependency (non-key → non-key). `employee(id, dept_id, dept_name)`: `dept_name` depends on `dept_id`, not `id` → split out `department`.
   - **BCNF** — every determinant is a candidate key. Fixes the rare overlapping-candidate-key case 3NF misses.

   Target **3NF as the floor, BCNF where a determinant anomaly exists.** Each non-key fact lives in exactly one place; a fact changes via exactly one `UPDATE` to one row. Do **not** model attribute-value pairs generically (EAV: `entity/attribute/value` rows) — it destroys typing, FKs, and constraints; make real typed columns instead.

4. **Model cardinalities explicitly — the FK lives on the "many" side.**
   - **1:N** — FK column on the child (many) side pointing at the parent's PK. `order.customer_id → customer.id`. The direction is not a choice: the many side carries the FK.
   - **M:N** — a junction (associative) table with a composite PK of both FKs: `enrollment(student_id, course_id, PRIMARY KEY(student_id, course_id))`. Relationship attributes (`enrolled_at`, `grade`) live on the junction.
   - **1:1** — share a PK: the dependent table's PK *is* an FK to the parent (`user_profile.user_id PK REFERENCES user(id)`). Use only for optional/rarely-loaded columns; otherwise just add the columns to the parent.
   - **Inheritance/polymorphism** — pick one, don't mix:

     | Pattern | Shape | Use when |
     |---|---|---|
     | Single-table | one table, nullable subtype columns, `kind` discriminator | few subtypes, mostly shared columns — **default** |
     | Class-table | base table + one child table per subtype, shared PK | subtypes have many distinct, NOT-NULL-able columns |
     | Concrete-table | one full table per subtype, no base | subtypes never queried together |

     For a polymorphic FK ("comment on a post *or* a photo"), **avoid the nullable-`(target_type, target_id)` pair** — it can't have a real FK. Prefer separate nullable FK columns each with its own real `REFERENCES` plus a `CHECK` that exactly one is set.

5. **Encode every invariant as a constraint in the DDL, not in app code.** If the database can enforce it, the database enforces it — app checks race and drift.
   - `NOT NULL` on every column that is logically required (default to NOT NULL; justify each nullable column).
   - `UNIQUE` on each natural/candidate key and on business-unique combos.
   - `FOREIGN KEY ... ON DELETE` — choose the action deliberately: `CASCADE` (children are parts of the parent), `RESTRICT`/`NO ACTION` (default; refuse to orphan), `SET NULL` (only if the FK is legitimately optional).
   - `CHECK` for value rules (`amount_minor >= 0`, `status IN (...)`, `start_at < end_at`).
   - **Partial unique index** for conditional uniqueness: `CREATE UNIQUE INDEX ON users(email) WHERE deleted_at IS NULL;` (one active email, history allowed).
   - **Exclusion constraint** for "no overlap" (e.g. no double-booking a room): `EXCLUDE USING gist (room_id WITH =, during WITH &&)`.

   ```sql
   CREATE TABLE booking (
     id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
     room_id    bigint NOT NULL REFERENCES room(id) ON DELETE RESTRICT,
     guest_id   bigint NOT NULL REFERENCES guest(id) ON DELETE RESTRICT,
     during     tstzrange NOT NULL,
     status     text NOT NULL DEFAULT 'held' CHECK (status IN ('held','confirmed','cancelled')),
     created_at timestamptz NOT NULL DEFAULT now(),
     updated_at timestamptz NOT NULL DEFAULT now(),
     CONSTRAINT no_double_booking
       EXCLUDE USING gist (room_id WITH =, during WITH &&) WHERE (status <> 'cancelled')
   );
   ```

6. **Decide the cross-cutting column conventions once, apply everywhere.**
   - **Soft vs hard delete** — default **hard delete** with `ON DELETE` rules. Use soft delete (`deleted_at timestamptz NULL`) only when you must retain history or undo; then *every* uniqueness and FK must account for it (partial indexes `WHERE deleted_at IS NULL`, filtered FKs) or you reintroduce duplicates and dangling references.
   - **Audit columns** — `created_at timestamptz NOT NULL DEFAULT now()`, `updated_at timestamptz NOT NULL DEFAULT now()` (kept current by a trigger), and `created_by/updated_by` FKs where attribution matters. Full row history → separate `*_history` table or → **design-event-sourcing-cqrs**, not bolted onto the live row.
   - **Enum vs lookup table** — small, fixed, code-coupled set (`status`) → `CHECK (x IN (...))` or a native enum. Editable-by-users or carrying extra attributes (label, sort order, active flag) → a lookup table with an FK. Don't ship a `roles` lookup table of three forever-fixed values; don't ship a CHECK list for something product managers edit weekly.
   - **Types** — money as `NUMERIC(precision, scale)` or integer minor units, **never `float`/`real`/`double`** (see **money-decimal-arithmetic**); timestamps as `timestamptz` storing UTC instants, never naive `timestamp` (see **datetime-timezone-correctness**); text as `text` (not `varchar(n)` unless a real domain limit exists); booleans as `boolean`, not `0/1` ints or `'Y'/'N'`.

7. **Denormalize only on a measured read hot path, and write down what you traded.** Start fully normalized; denormalize a specific column **only** when a real, frequent read can't be served cheaply by a join/index. Each denormalization is a stated consistency contract:

   | Technique | Buys you | Costs you (must be stated) |
   |---|---|---|
   | Derived/rollup column (`post.comment_count`) | O(1) read, no aggregate join | Must update on every child write — trigger or app, or it drifts |
   | Duplicated parent attribute (`order_item.product_name` at sale time) | Stable historical snapshot | Diverges from source by design — that's the point; document it |
   | Materialized view | Precomputed report | Staleness window; explicit `REFRESH` (concurrently) needed |
   | Pre-joined wide read table | Single-table dashboard read | Whole second write path to keep in sync |

   Default: keep it normalized and add an index first. A rollup counter maintained by a trigger is acceptable; copying mutable data you then have to keep in sync in two places is a liability — only when the read win is proven. Record for each: *what's duplicated, who keeps it consistent, and the acceptable staleness*.

8. **Output the DDL plus an access-pattern → table/index map.** Deliver: (a) `CREATE TABLE` statements with all constraints from steps 5–6, (b) the FK graph, (c) a table mapping each top query/access pattern to the table(s) and the index that serves it (so every hot read has a supporting index and no table has unused indexes). This map is the proof the schema serves the real queries, not just an abstract model.

## Common Errors

- **EAV ("flexible schema") tables.** `entity/attribute/value` rows throw away typing, FKs, and constraints and turn every read into a self-join pivot. Use real typed columns; if attributes are genuinely open-ended, a single typed `jsonb` column beats EAV.
- **Float money.** `price float` loses cents to binary rounding — `0.1 + 0.2 ≠ 0.3`. Use `NUMERIC` or integer minor units; defer the math rules to money-decimal-arithmetic.
- **Nullable-FK soup / polymorphic `(type, id)`.** A `parent_type text, parent_id bigint` pair can't have a foreign key, so the DB can't stop dangling references. Use separate real FK columns + a `CHECK` that exactly one is non-null.
- **Natural key as PK that later changes.** Making `email` or a username the PK means a single edit cascades through every referencing FK. Keep a surrogate PK; put `UNIQUE` on the natural key.
- **Random UUID (v4) PK on a hot insert path.** Random keys scatter B-tree inserts, bloating the index and WAL. Use UUID**v7**/ULID (time-ordered) when you need a UUID, or a `bigint` when the ID isn't exposed.
- **Soft delete without filtered constraints.** `deleted_at` plus a plain `UNIQUE(email)` blocks a user from re-registering a freed email, and plain FKs still "see" deleted parents. Make uniqueness and lookups partial: `WHERE deleted_at IS NULL`.
- **Over-normalizing tiny fixed sets.** A 3-value lookup table joined on every query adds a join for no benefit. A `CHECK (x IN (...))` enum is fine for small, code-coupled, rarely-changing sets.
- **Storing lists in a column.** `tags TEXT` as CSV (or an unindexed array) can't be FK'd, constrained, or joined cleanly. Model it as a child/junction table.
- **`varchar(255)` cargo-culting and naive `timestamp`.** Arbitrary length caps cause silent truncation; `timestamp` without time zone loses the offset. Use `text` and `timestamptz`.
- **Missing `ON DELETE` action.** Defaulting blindly leaves you with either accidental orphans or surprise cascade deletes. Choose `CASCADE`/`RESTRICT`/`SET NULL` per FK on purpose.
- **Denormalizing speculatively.** Duplicating data "for speed" before any query proves slow doubles your write paths and invites drift. Normalize first, index, measure, then denormalize the proven hot path.

## Verify

1. **3NF check:** For each table, every non-key column depends on the key, the whole key, and nothing but the key. Name any transitive (`non-key → non-key`) or partial dependency you allowed and justify it as a deliberate denormalization — otherwise split it.
2. **Anomaly probe:** Pick one update, one insert, and one delete per core entity. Confirm each touches exactly one row in one place with no way to leave the data inconsistent (no second copy to forget).
3. **Constraint coverage:** Every invariant you stated in step 1 maps to an actual `NOT NULL`/`UNIQUE`/`CHECK`/`FK`/exclusion/partial-index in the DDL — not to an app-layer comment. List any invariant *not* enforced by the DB and why.
4. **Referential integrity:** Every FK names an explicit `ON DELETE` action; no polymorphic `(type, id)` pair lacks a real FK; every junction table has a composite PK of its two FKs.
5. **Key sanity:** Every table has a PK; no natural key that can change is used as a PK; sequential surrogates aren't exposed where the sequence is sensitive; UUID columns are v7/ULID unless v4 is justified.
6. **Type sanity:** No money in `float`; timestamps are `timestamptz` (UTC); no CSV/array masquerading as a relationship; enums vs lookup chosen per the step-6 rule.
7. **Access-pattern map:** Every listed top query is served by an existing index/PK; every index supports at least one stated query (no orphan indexes); each denormalized column has a named owner-of-consistency and a stated staleness bound.

Done = the schema is at 3NF (BCNF where a determinant anomaly existed) with every stated invariant enforced by a DB constraint, every PK/FK and `ON DELETE` chosen deliberately, no float money / naive timestamps / EAV / polymorphic-FK soup, and an access-pattern→table/index map in which every hot read has a supporting index and every denormalization carries a written consistency tradeoff.
