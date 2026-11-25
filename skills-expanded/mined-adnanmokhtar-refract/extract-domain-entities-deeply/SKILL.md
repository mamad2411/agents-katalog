---
name: extract-domain-entities-deeply
description: Round-two deep extraction of domain entities — reads ORM/model/schema definitions + migrations + repositories + tests + docs to produce a structured map (entities, fields with types/constraints, relationships, lifecycle events, invariants). Used by /setup-project Phase 2.7 in REFINE mode to upgrade round-one business-domain detection from "this is a billing app" to "billing has 7 entities with 9 invariants — here they are with file:line citations." Output is the substrate for Phase 4.6-DEEP rewrites of domain-related artifacts.
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: extract-domain-entities-deeply

## Purpose

Round-one Phase 2.x detects the *kind* of business domain ("billing", "healthcare", "e-commerce") from folder names + dependency manifests + entity-name keywords. That is enough for the floor (matching pack overlays). It is NOT enough for round-two depth.

This skill produces the project's actual domain map — the kind of document a senior engineer joining the team would write after a week of code reading. Output is anchorable: every claim ties to `file:line`. Generic prose is forbidden.

## Premise

- Real source is the truth. Read every domain entity file in full — class declaration, field decorators, relationships, hooks, computed properties, custom methods — before composing a row.
- Walk the migration history for index + constraint lineage; the model file alone misses dropped/renamed columns.
- Every entity, field, relationship, lifecycle event, invariant, and repository method cites `<path:line>` resolving at the current commit.
- Empty extraction is honest — an entity with `invariants: []` is correct when no DB / model / service / test enforcement exists; record `enforcement: none` explicitly.
- Fabrication — inventing an entity the codebase doesn't have, an invariant no code enforces, a relationship not declared in the model — corrupts every domain-related artifact that reads this section.

## Mechanical halt

- Hand-wave entries — `etc.`, `...`, `usual fields`, `appears to be aggregate root`, an invariant without a `citation:` line, a relationship without on-delete behavior, an entity without ≥1 field — REFUSE to write the row.
- Re-read the source file and regenerate the row, OR downgrade the entity (or the whole domain) to `[REFINE-WEAK: domain=<name>]`.
- If the business-domain has fewer than 3 entities AND the quality gate fails, record `<NOT-DETECTED: domain=<name>: <N> entities, threshold 3>` per Step 8's validate rule.
- Never inflate by promoting infrastructure tables (audit logs, queue jobs, schedule rows) into the domain — cross-domain references go in `cross_entity_invariants`, not in the entity list.

## When to use

- `/setup-project --refine` Phase 2.7 — once per detected business-domain.
- Manually, when a developer says "the domain has shifted" and wants round-two entity depth without a full `--refine`. NOT dispatched by `/refresh-knowledge`: that command re-runs round-one extraction (`extract-codebase-overview` + its Step-13 chain) and does not enter Phases 2.7-2.12.
- Manually when authoring `ai/business-domain.md` for a project that has substantial schema but a generic round-one extraction.

## Inputs

- `business_domain_name` — from Phase 2.x detection (e.g. `billing`, `healthcare`, `ecommerce`).
- `entity_paths` (optional) — pre-narrowed list of model / schema directories. If absent, the skill auto-discovers from the codebase profile.
- `output_section` — section path inside `.claude/_refine-extract.md` to write to (default: `## Domain entities — <business_domain_name>`).

## Procedure

### Step 1 — Discover entity definition files

Search in this priority order (stop at first hit class, then continue across all hits within that class):

1. **ORM model classes** — language-specific patterns:
   - Python / Django: `models.py` files; classes inheriting from `models.Model` / `AbstractBaseUser` / `MPTTModel`.
   - Python / SQLAlchemy: classes inheriting from `Base` / `DeclarativeBase`; `Table()` calls.
   - Python / Pydantic: classes inheriting from `BaseModel` (when used as schemas, not models — note the distinction).
   - Node / TypeScript / TypeORM: classes decorated with `@Entity()`.
   - Node / TypeScript / Prisma: `schema.prisma` model blocks.
   - Node / TypeScript / Sequelize: `Model.init()` calls or `@Table` decorators.
   - Node / TypeScript / Mongoose: `Schema()` calls; `model('<Name>', schema)` calls.
   - Node / TypeScript / Drizzle: `pgTable()` / `mysqlTable()` calls.
   - Java / JPA: classes annotated `@Entity`.
   - Go / GORM: structs with `gorm:` tags.
   - .NET / EF Core: classes registered in `OnModelCreating` or with `DbSet<T>`.
   - Ruby / ActiveRecord: classes inheriting from `ApplicationRecord` / `ActiveRecord::Base`.
2. **Schema files** — `schema.prisma`, `schema.rb` (Rails dump), `*.sql` migration files, OpenAPI / GraphQL schema.
3. **DTOs / serializers** — Pydantic / Zod / class-validator / Marshmallow / Joi schemas (these expose the *external* shape; the model is the *internal*).
4. **Migration history** — `migrations/` directory walked in order to reconstruct lineage (added fields, dropped fields, renamed fields, type changes).

Filter to entities that match the `business_domain_name` topic — drop infrastructure entities (audit logs, schedule rows, queue jobs) unless the domain explicitly is one of those.

### Step 2 — Read every domain entity in full

For each filtered entity:

- **Class name** + file path + line number of class declaration.
- **Fields**: name, type, nullable, default, validation rules (min/max, regex, choices), DB column name if different.
- **Relationships**: `OneToOne`, `OneToMany`, `ManyToMany`, polymorphic, FK target, on-delete behavior, cascade rules.
- **Indexes**: declared on the model (e.g. `class Meta: indexes = [...]`), and from migrations.
- **Computed properties**: `@property`, `@computed`, getters that derive a value from other fields — these often encode invariants.
- **Save / pre-save hooks**: `clean()`, `before_save`, `@PreUpdate`, etc. — these encode invariants.
- **Custom methods** that look domain-relevant (e.g. `Invoice.finalize()`, `Subscription.cancel()`, `Order.fulfill()`).

### Step 3 — Identify lifecycle events

Lifecycle events are the verbs of the domain. Find them in:

- Methods named like state-transitions: `cancel`, `finalize`, `void`, `refund`, `ship`, `fulfill`, `activate`, `suspend`, `archive`, `restore`.
- State-machine libraries: `django-fsm`, `xstate`, `stateless`, `aasm`, `transitions`.
- Status fields with enumerations: a `status: Literal['draft', 'sent', 'paid']` is a state machine.
- Event publishers: `publish('invoice.paid', ...)`, `EventBus.emit(...)`, `events.append(...)`, signals (`post_save`, `pre_delete`).
- Webhook senders / domain-event tables: `outbox` / `domain_events` table inserts.

Record: event name, entity, trigger (which method emits it), side effects (DB writes, external calls in same transaction).

### Step 4 — Extract invariants

Invariants are the "must always be true" rules. Find them in:

- `class Meta: constraints = [CheckConstraint(...)]`.
- Database-level constraints in migrations (`UNIQUE`, `CHECK`, partial indexes).
- `assert` statements inside model methods.
- `clean()` / validation hook bodies.
- Test files — assertions that always hold (e.g. `assert invoice.amount == sum(line_items.amount for line_items in invoice.line_items)` in a test.
- Domain service classes — methods that explicitly enforce a rule (e.g. `LedgerService.assert_balanced(invoice_id)`).

Record: invariant statement (1 sentence), citation (file:line of the assertion / constraint), enforcement layer (DB / model / service / test / nowhere — the "nowhere" finding is itself important).

### Step 5 — Cross-reference repositories / DAOs

For each entity, find:

- `<Entity>Repository` / `<Entity>DAO` / `<Entity>Manager` classes.
- Custom QuerySet methods (`Invoice.objects.unpaid()`, `Invoice.active()`).
- Stored procedures / DB views / materialized views in migrations.

These show the queries the rest of the app actually runs — which fields are filtered + ordered + grouped most often. That tells you which fields matter for indexing (output goes to Phase 2.11 hot-paths skill) and which fields encode the domain's primary lookups.

### Step 6 — Cross-reference tests

For each entity, find:

- Factory definitions (factory_boy / FactoryBot / Sequelize fixtures / @nestjs/typeorm-seeding).
- Integration tests that exercise the entity's full lifecycle — these reveal the *intended* behavior, including the edge cases the team explicitly tests for.
- Snapshot / fixture files — these reveal the realistic shape of records.

Capture: 1-2 sentences per entity describing "what the team *tests* this entity for."

### Step 7 — Synthesize

Write the output section using this schema:

```yaml
business_domain: <name>
extraction_date: <YYYY-MM-DD>
entity_count: <N>
strong_signals: ["entities", "relationships", "invariants", "lifecycle"]   # or subset if some axes were weak

entities:
  - name: <ClassName>
    path: <file:line>
    purpose: <1-sentence what this entity represents in the business>
    fields:
      - name: <field>
        type: <type>
        nullable: <bool>
        default: <value or None>
        notes: <constraints / validation>
    relationships:
      - to: <OtherEntity>
        kind: <OneToMany|ManyToMany|...>
        on_delete: <CASCADE|RESTRICT|SET_NULL|...>
    invariants:
      - statement: <1-sentence invariant>
        enforcement: <DB|model|service|test|none>
        citation: <file:line>
    lifecycle_events:
      - event: <name>
        trigger: <method-name>
        emitted_at: <file:line>
        side_effects: [<list>]
    indexes:
      - fields: [<list>]
        type: <btree|hash|partial|unique>
        cited: <migration file:line>
    repository_methods:
      - <Repository.method_name> at <file:line>
        # one line per non-trivial query method
    tested_for: <1-sentence what tests cover for this entity>

# Repeat per entity.

cross_entity_invariants:
  # Invariants that span MULTIPLE entities (often the most important ones)
  - statement: <e.g. "LedgerEntry.amount summed by Invoice MUST equal Invoice.total">
    enforcement: <citation>
```

### Step 8 — Validate

Before writing:

- Each entity has at LEAST: name, path, ≥1 field, ≥1 relationship OR ≥1 lifecycle event.
- Each invariant has a `file:line` citation. NO un-cited invariants. (If an invariant is "the team says X but no code enforces it" — explicitly mark `enforcement: none, citation: <docs/postmortem-2025-04.md or runbook>` — the un-enforced invariant is itself a finding.)
- No invented entity names. Cross-check every entity name against the original ORM file list.

## Output

Append to `.claude/_refine-extract.md` under the section heading. Schema-validated against `~/.claude/templates/schemas/_extracted-domain.schema.json` (warns if `--strict` not set).

## Quality gate

- **STRONG**: ≥ 3 entities, ≥ 5 fields per entity on average, ≥ 1 invariant total, ≥ 1 lifecycle event total.
- **WEAK**: any of the above thresholds missed → flag `[REFINE-WEAK: domain=<name>]` in the file. Phase 4.6-DEEP will NOT rewrite domain artifacts based on a WEAK extraction; round-one anchors stay.

## Anti-patterns

- **Inventing entities** that aren't in code (e.g. "I think the project should have an `AuditLog` entity" — no, only what extraction finds).
- **Citing relationships not declared** — every `OneToMany` etc. must come from the actual model decorator / column declaration.
- **Skipping the migration walk** — migrations encode the *history* of the schema, including fields the team renamed or dropped (which often reveals deprecated invariants the round-one detection missed).
- **Treating Pydantic / Zod schemas as entities** when the project also has ORM models — the schema is the boundary; the model is the entity. Be explicit which is which.
- **Cross-domain leakage** — when extracting `billing` entities, exclude `Patient` even if it has an FK from `Invoice`. The `Patient` entity belongs to the `healthcare` domain; cross-domain references go in `cross_entity_invariants`.
