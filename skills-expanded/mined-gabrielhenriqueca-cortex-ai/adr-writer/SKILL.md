# ADR Writer Skill

This skill produces Architecture Decision Records in MADR (Markdown Architecture Decision Records) format.

## When to Write an ADR

An ADR is warranted when:

- A technology is added or removed from the stack
- A significant architectural pattern is introduced or changed
- A trade-off was made that is not obvious from the code
- A decision was hard to make and the reasoning should be preserved
- Future engineers will likely question why something was done this way
- A decision has meaningful consequences if reversed

An ADR is **not** warranted for:

- Implementation details within a module
- Routine refactors with no architectural impact
- Style or tooling preferences already covered by linting rules

## MADR Format

```markdown
# <NNNN>. <Title in Title Case>

Date: <YYYY-MM-DD>
Status: Proposed | Accepted | Deprecated | Superseded by [ADR-XXXX]

## Context and Problem Statement

[2-4 paragraphs. What problem are we solving? What constraints exist?
What are the consequences of not deciding this now? Include links to
relevant issues, prior ADRs, or external references.]

## Decision Drivers

* [Measurable or observable driver — "must support 10k req/s at p99 < 500ms"]
* [Team constraint — "no Rust expertise on the team"]
* [Compliance driver — "GDPR requires data residency in EU"]

## Considered Options

* [Option A — brief label]
* [Option B — brief label]
* [Option C — brief label]
* [Do nothing / status quo — always include if valid]

## Decision Outcome

Chosen option: **"[Option X]"**, because it best satisfies [the most important driver(s)].

### Positive Consequences

* [Concrete benefit]
* [Concrete benefit]

### Negative Consequences / Trade-offs

* [Concrete cost or limitation]
* [What we're giving up]

## Pros and Cons of the Options

### [Option A — full name]

[1-2 sentence description]

* Good, because [argument tied to a decision driver]
* Good, because [argument]
* Bad, because [argument]
* Neutral, because [argument — not good or bad, just different]

### [Option B — full name]

[same structure]

### [Option C — full name]

[same structure]

## Links

* [Related ADR](./NNNN-related-decision.md)
* [GitHub issue or discussion](https://github.com/...)
* [External reference]
```

## Real-World Example: Database Selection

```markdown
# 0005. Use PostgreSQL as Primary Relational Database

Date: 2026-01-15
Status: Accepted

## Context and Problem Statement

We need a primary relational database for the user and order data domain.
The system expects 50k-100k rows/day of write volume and complex ad-hoc
reporting queries by the analytics team. We evaluated three options.

## Decision Drivers

* Must support JSONB for semi-structured product metadata
* Team has 5+ years of PostgreSQL experience
* Must run on Azure (managed service preferred)
* Reporting queries may run 30-60 seconds — must not block OLTP

## Considered Options

* PostgreSQL on Azure Database for PostgreSQL - Flexible Server
* MySQL on Azure Database for MySQL
* SQL Server on Azure SQL Database

## Decision Outcome

Chosen option: **"PostgreSQL on Azure Database for PostgreSQL - Flexible Server"**,
because it best satisfies the JSONB requirement and team familiarity while
offering a fully managed service on Azure.

### Positive Consequences

* Leverages existing team expertise — reduced onboarding cost
* JSONB with GIN indexes handles product metadata without a separate NoSQL store

### Negative Consequences / Trade-offs

* Azure Database for PostgreSQL has fewer enterprise features than Azure SQL
* Read replicas for analytics must be managed manually (vs. Azure SQL's read scale)

## Pros and Cons of the Options

### PostgreSQL on Azure Flexible Server

* Good, because team knows it deeply
* Good, because JSONB eliminates the need for a separate document store
* Bad, because analytics read scaling requires manual replica setup

### MySQL on Azure

* Good, because it is well-supported on Azure
* Bad, because team has no MySQL expertise
* Bad, because JSON support is less mature than PostgreSQL's JSONB

### Azure SQL Database

* Good, because best Azure integration and enterprise tooling
* Bad, because licensing cost is significantly higher
* Bad, because T-SQL differs enough from standard SQL to create friction
```

## Numbering and File Naming

- ADR numbers are zero-padded to 4 digits: `0001`, `0002`, etc.
- File names use kebab-case: `0005-use-postgresql-as-primary-database.md`
- Never reuse a number. Deprecated ADRs keep their number with `Status: Deprecated`.
- Superseded ADRs link to their replacement: `Status: Superseded by [ADR-0012](./0012-migrate-to-cockroachdb.md)`
