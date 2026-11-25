# Data Contracts Skill

This skill defines, reviews, and validates data contracts at pipeline layer boundaries using
industry-standard tools and patterns.

## What Is a Data Contract

A data contract is a formal agreement between a data producer and its consumers that specifies:

- **Schema** — field names, types, nullability, and constraints
- **Semantics** — what each field means, its unit, and valid values
- **SLA** — freshness, availability, and completeness guarantees
- **Ownership** — who produces it and who to contact when it breaks

Without contracts, consumers discover schema changes in production. With contracts, changes
are negotiated and versioned.

## Tools

| Tool | Purpose | When to Use |
|---|---|---|
| [datacontract-cli](https://datacontract.com) | Contract definition + validation | Primary contract format |
| dbt contracts + constraints | SQL model-level contracts | dbt projects |
| Great Expectations | Data quality assertions | Batch validation in pipelines |
| Soda Core | SQL-native quality checks | Warehouse-native validation |

## datacontract.com Format

```yaml
# datacontract.yaml
dataContractSpecification: 0.9.3

id: urn:datacontract:orders:order-events:v1
info:
  title: Order Events
  version: 1.0.0
  status: active
  owner: data-platform-team
  contact:
    name: Data Platform
    url: https://github.com/org/team

servers:
  production:
    type: databricks
    catalog: prod
    schema: orders
    table: order_events

terms:
  usage: >
    Downstream consumers may read this table for analytics and ML features.
    Do not write to this table directly.
  limitations: >
    Data is available with T+1 latency. Same-day data is not guaranteed.
  billing: free
  noticePeriod: P3M   # 3 months notice for breaking changes

models:
  order_events:
    description: One row per order state transition
    type: table
    fields:
      order_id:
        type: string
        required: true
        unique: false
        description: UUID of the order. Surrogate key.
        pii: false
      event_type:
        type: string
        required: true
        enum:
          - created
          - paid
          - shipped
          - delivered
          - cancelled
        description: The lifecycle event that triggered this row.
      occurred_at:
        type: timestamp
        required: true
        description: When the event happened in the source system. UTC.
      customer_id:
        type: string
        required: true
        pii: true
        classification: restricted
        description: References customers.customer_id.
      amount_usd:
        type: decimal
        required: false
        precision: 10
        scale: 2
        description: >
          Order value in USD at time of event. Null for non-financial events
          (e.g., shipped, delivered).

quality:
  type: SodaCL
  specification:
    checks for order_events:
      - row_count > 1000
      - missing_count(order_id) = 0
      - duplicate_count(order_id, occurred_at) = 0
      - invalid_count(event_type) = 0:
          valid values: [created, paid, shipped, delivered, cancelled]
      - freshness(occurred_at) < 25h
```

## dbt Contract Example

```yaml
# models/orders/schema.yml
models:
  - name: order_events
    description: One row per order state transition
    config:
      contract:
        enforced: true  # dbt will validate types on run

    constraints:
      - type: not_null
        columns: [order_id, event_type, occurred_at, customer_id]
      - type: unique
        columns: [order_id, event_type]

    columns:
      - name: order_id
        data_type: string
        constraints:
          - type: not_null
      - name: event_type
        data_type: string
        constraints:
          - type: not_null
          - type: accepted_values
            values: [created, paid, shipped, delivered, cancelled]
      - name: occurred_at
        data_type: timestamp
        constraints:
          - type: not_null
      - name: amount_usd
        data_type: decimal(10, 2)
```

## Contract Review Checklist

When reviewing a data contract or pipeline boundary, verify:

**Schema completeness:**
- [ ] All fields have types, nullability, and descriptions
- [ ] PII fields are flagged and classified
- [ ] Enum fields list all valid values
- [ ] Numeric fields specify precision and unit (USD? cents? percentage?)

**Semantic correctness:**
- [ ] Field descriptions explain what the value *means*, not just what it *is*
- [ ] Timestamps specify timezone (UTC assumed? local?)
- [ ] Foreign keys document their reference table

**SLA definition:**
- [ ] Freshness SLA is defined (how stale is acceptable?)
- [ ] Availability SLA is defined (what % uptime?)
- [ ] Completeness: are partial loads acceptable?

**Operational:**
- [ ] Owner is identified with a contact channel
- [ ] Notice period for breaking changes is stated
- [ ] Version is incremented on breaking changes (semver)

## Breaking vs Non-Breaking Changes

| Change | Breaking | Action Required |
|---|---|---|
| Add nullable column | No | Notify consumers, bump minor version |
| Remove column | Yes | Deprecation period, major version bump |
| Rename column | Yes | Alias + deprecation or major version |
| Change type (widening) | Sometimes | Check consumer impact |
| Change type (narrowing) | Yes | Major version bump |
| Add enum value | No (usually) | Check consumer exhaustive handling |
| Remove enum value | Yes | Major version bump |
| Change freshness SLA | Yes | Renegotiate with consumers |
