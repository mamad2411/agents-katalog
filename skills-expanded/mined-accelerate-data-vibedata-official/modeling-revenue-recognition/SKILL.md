---
name: modeling-revenue-recognition
description: >
  Use when modeling ASC 606 revenue recognition in dbt on Microsoft Fabric,
  including performance obligations, transaction price allocation, deferred
  revenue, contract modifications, or silver/gold revenue reporting layers.
tools: Read, Write, Edit, Glob, Grep, Bash
type: domain
domain: revenue recognition
version: 1.0.2
---

# Modeling Revenue Recognition in dbt on Fabric

Patterns for implementing ASC 606 revenue recognition in a dbt medallion architecture on Fabric. Focuses on what Claude gets wrong: entity classification, grain decisions, allocation logic in SQL, and the bronze-to-gold pipeline for contracts with multiple performance obligations.

## Quick Reference

### Entity Classification

Revenue domain entities fall into two categories. Getting this wrong causes fan-out or collapsed aggregates.

| Entity | Model Type | Grain (one row = ) | Natural Key |
|---|---|---|---|
| Customer | `dim_customer` | One customer | `customer_id` from CRM |
| Product / SKU | `dim_product` | One sellable item or service | `product_id` from catalog |
| Contract | `dim_contract` | One executed contract | `contract_id` from ERP |
| Contract Line Item | `fct_contract_line` | One line on a contract | `contract_id` + `line_number` |
| Performance Obligation | `fct_performance_obligation` | One distinct promise within a contract | `contract_id` + `obligation_id` |
| Transaction Price Allocation | `fct_price_allocation` | One allocation of price to one obligation | `contract_id` + `obligation_id` |
| Revenue Recognition Event | `fct_revenue_recognition` | One recognition event per obligation per period | `obligation_id` + `period_id` |
| Invoice Line | `fct_invoice_line` | One line item on an invoice | `invoice_id` + `line_number` |
| Deferred Revenue | `fct_deferred_revenue` | One deferred balance per obligation per period | `obligation_id` + `period_id` |

**Critical grain rule**: `fct_revenue_recognition` grain is one recognition event per performance obligation per accounting period. Mixing obligation-level and contract-level rows in the same model is the #1 cause of wrong revenue totals.

### Dimensions vs Facts -- Decision Rule

- **Dimension**: Entity changes slowly, is referenced by facts, describes context. Revenue dimensions are thin -- customer, product, contract metadata.
- **Fact**: Entity records an event or measurable occurrence. Revenue facts are where the money lives -- recognition events, allocations, invoices, deferred balances.

**Common mistake**: Modeling `dim_contract` with financial amounts. Contracts are dimensions (who, when, terms). The money flows through `fct_contract_line` and `fct_performance_obligation`.

## ASC 606 Five-Step Model to Medallion Layers

Each ASC 606 step maps to a specific medallion layer. This is the core mapping Claude needs.

### Step 1: Identify the Contract -- Bronze

**What happens**: Raw contract data lands from ERP/CRM.

**Bronze models**:
- `stg_erp__contracts` -- raw contract header (parties, dates, status)
- `stg_erp__contract_lines` -- raw line items (products, quantities, list prices)
- `stg_crm__customers` -- customer master data

**Key fields to preserve**: `contract_start_date`, `contract_end_date`, `contract_status`, `customer_id`, `currency_code`. Drop nothing -- bronze is lossless.

**Fabric-specific**: Use `datetime2` for contract dates. `date` type truncates time components that matter for same-day contract amendments.

### Step 2: Identify Performance Obligations -- Silver

**What happens**: Business logic determines which promises in the contract are distinct.

**Silver model**: `int_performance_obligations`

```sql
-- int_performance_obligations.sql
-- Grain: one row per distinct performance obligation per contract
with contract_lines as (
    select * from {{ ref('stg_erp__contract_lines') }}
),
obligation_classification as (
    select
        contract_id,
        line_number,
        product_id,
        -- A good or service is distinct if the customer can benefit
        -- from it on its own AND it is separately identifiable
        case
            when is_standalone_capable = 1
                and is_separately_identifiable = 1
            then 'distinct'
            when is_standalone_capable = 1
                and is_separately_identifiable = 0
            then 'combined'  -- combine with other promises
            else 'combined'
        end as obligation_type,
        -- Combined obligations get a single obligation_id
        case
            when is_separately_identifiable = 1
            then cast(contract_id as varchar) + '-' + cast(line_number as varchar)
            else cast(contract_id as varchar) + '-COMBINED'
        end as obligation_id
    from contract_lines
)
select * from obligation_classification
```

**What Claude gets wrong**: Treating every line item as a separate performance obligation. A software license bundled with implementation services is often ONE obligation (not separately identifiable) unless the customer could benefit from the services independently.

### Step 3: Determine Transaction Price -- Silver

**What happens**: Calculate the total consideration, including variable amounts.

**Silver model**: `int_transaction_price`

```sql
-- int_transaction_price.sql
-- Grain: one row per contract
with contracts as (
    select * from {{ ref('stg_erp__contracts') }}
),
variable_consideration as (
    select
        contract_id,
        base_contract_amount,
        -- Variable consideration: use expected value or most likely amount
        -- Expected value: probability-weighted sum (use for large populations)
        -- Most likely amount: single most likely outcome (use for binary outcomes)
        case
            when variable_consideration_method = 'expected_value'
            then sum(outcome_amount * outcome_probability)
            when variable_consideration_method = 'most_likely'
            then max(case when is_most_likely = 1 then outcome_amount end)
            else 0
        end as variable_consideration_amount,
        -- Constraint: include variable consideration only to the extent
        -- a significant reversal is NOT probable
        case
            when reversal_probability > 0.5 then 0
            else variable_consideration_amount
        end as constrained_variable_amount
    from contracts
    left join {{ ref('stg_erp__variable_outcomes') }}
        using (contract_id)
    group by contract_id, base_contract_amount, variable_consideration_method
)
select
    contract_id,
    base_contract_amount + coalesce(constrained_variable_amount, 0)
        as transaction_price
from variable_consideration
```

**Key rule**: Variable consideration (discounts, rebates, penalties, bonuses) must be estimated AND constrained. The constraint test -- "is a significant revenue reversal probable?" -- belongs in a silver `int_` model, not in gold.

### Step 4: Allocate Transaction Price -- Silver

**What happens**: Transaction price is allocated to each performance obligation based on relative standalone selling prices.

**Silver model**: `int_price_allocation`

```sql
-- int_price_allocation.sql
-- Grain: one row per performance obligation per contract
with obligations as (
    select * from {{ ref('int_performance_obligations') }}
),
transaction_prices as (
    select * from {{ ref('int_transaction_price') }}
),
standalone_prices as (
    select * from {{ ref('int_standalone_selling_prices') }}
),
allocation as (
    select
        o.contract_id,
        o.obligation_id,
        o.product_id,
        tp.transaction_price,
        sp.standalone_selling_price,
        -- Relative standalone selling price method
        sp.standalone_selling_price
            / sum(sp.standalone_selling_price) over (partition by o.contract_id)
            * tp.transaction_price
            as allocated_amount
    from obligations o
    join transaction_prices tp on o.contract_id = tp.contract_id
    join standalone_prices sp on o.product_id = sp.product_id
)
select * from allocation
```

**Allocation methods** (implement in `int_standalone_selling_prices`):

| Method | When to use | SQL pattern |
|---|---|---|
| Observable price | Product sold standalone in similar circumstances | Direct lookup from price list |
| Adjusted market assessment | Observable price unavailable; estimate what market would pay | Competitor pricing adjusted for entity's costs + margin |
| Expected cost plus margin | No market data; cost is known | `cost * (1 + target_margin_pct)` |
| Residual | SSP highly variable or uncertain for ONE obligation | `transaction_price - sum(other_obligations_ssp)` |

**Residual method constraint**: Only permitted when SSP is highly variable or uncertain. Cannot use residual for more than one obligation in the same contract.

### Step 5: Recognize Revenue -- Gold

**What happens**: Revenue is recognized when (or as) each performance obligation is satisfied.

**Gold models**: `fct_revenue_recognition`, `fct_deferred_revenue`

Two recognition patterns:

| Pattern | Trigger | Example | SQL approach |
|---|---|---|---|
| Point-in-time | Control transfers at a moment | Product delivery, license key activation | `recognition_date = transfer_date`, full `allocated_amount` in one period |
| Over time | Control transfers progressively | SaaS subscription, construction, consulting | Pro-rata across periods using output or input method |

```sql
-- fct_revenue_recognition.sql
-- Grain: one recognition event per obligation per accounting period
{{ config(materialized='incremental', unique_key=['obligation_id', 'period_id'], incremental_strategy='merge') }}

with allocations as (
    select * from {{ ref('int_price_allocation') }}
),
recognition_schedule as (
    select * from {{ ref('int_recognition_schedule') }}
),
recognized as (
    select
        a.contract_id,
        a.obligation_id,
        rs.period_id,
        rs.recognition_date,
        a.allocated_amount * rs.recognition_pct as recognized_amount,
        a.allocated_amount as total_obligation_amount,
        rs.recognition_method,  -- 'point_in_time' or 'over_time'
        rs.cumulative_pct
    from allocations a
    join recognition_schedule rs
        on a.obligation_id = rs.obligation_id
)
select * from recognized
{% if is_incremental() %}
where recognition_date > (
    select dateadd(day, -3, max(recognition_date)) from {{ this }}
)
{% endif %}
```

## Metric Formulas

Exact formulas. Do not paraphrase -- use these definitions.

### Recognized Revenue (Period)

```sql
-- Revenue recognized in a specific period
select sum(recognized_amount) as recognized_revenue
from {{ ref('fct_revenue_recognition') }}
where recognition_date >= @period_start
  and recognition_date <= @period_end
```

### Deferred Revenue (Balance)

```sql
-- Deferred revenue balance at a point in time
-- = total allocated but not yet recognized
select sum(allocated_amount - cumulative_recognized) as deferred_revenue
from (
    select
        pa.obligation_id,
        pa.allocated_amount,
        coalesce(sum(rr.recognized_amount), 0) as cumulative_recognized
    from {{ ref('int_price_allocation') }} pa
    left join {{ ref('fct_revenue_recognition') }} rr
        on pa.obligation_id = rr.obligation_id
        and rr.recognition_date <= @as_of_date
    group by pa.obligation_id, pa.allocated_amount
) balances
where allocated_amount > cumulative_recognized
```

### Contract Asset / Contract Liability

```sql
-- Contract asset: revenue recognized > amounts billed (entity has right to payment)
-- Contract liability: amounts billed > revenue recognized (deferred revenue)
select
    contract_id,
    sum(cumulative_recognized) as cumulative_recognized,
    sum(cumulative_billed) as cumulative_billed,
    sum(cumulative_recognized) - sum(cumulative_billed) as net_position,
    case
        when sum(cumulative_recognized) > sum(cumulative_billed) then 'contract_asset'
        else 'contract_liability'
    end as position_type
from {{ ref('int_contract_position') }}
group by contract_id
```

### Remaining Performance Obligation (RPO)

```sql
-- RPO = allocated price not yet recognized across all open contracts
select sum(allocated_amount - cumulative_recognized) as rpo
from {{ ref('int_price_allocation') }} pa
join {{ ref('dim_contract') }} c on pa.contract_id = c.contract_id
left join (
    select obligation_id, sum(recognized_amount) as cumulative_recognized
    from {{ ref('fct_revenue_recognition') }}
    group by obligation_id
) rr on pa.obligation_id = rr.obligation_id
where c.contract_status = 'active'
```

## Deferred Revenue Model

`fct_deferred_revenue` tracks the liability balance over time. This is a period snapshot model, not an event model.

```sql
-- fct_deferred_revenue.sql
-- Grain: one row per obligation per period (balance snapshot)
{{ config(materialized='incremental', unique_key=['obligation_id', 'period_id'], incremental_strategy='merge') }}

with obligations as (
    select * from {{ ref('int_price_allocation') }}
),
periods as (
    select * from {{ ref('dim_period') }}
),
recognition_to_date as (
    select
        obligation_id,
        period_id,
        sum(recognized_amount) as cumulative_recognized
    from {{ ref('fct_revenue_recognition') }}
    group by obligation_id, period_id
),
billing_to_date as (
    select
        obligation_id,
        period_id,
        sum(billed_amount) as cumulative_billed
    from {{ ref('int_billing_schedule') }}
    group by obligation_id, period_id
)
select
    o.obligation_id,
    p.period_id,
    p.period_end_date,
    o.allocated_amount as total_obligation_amount,
    coalesce(rtd.cumulative_recognized, 0) as cumulative_recognized,
    coalesce(btd.cumulative_billed, 0) as cumulative_billed,
    coalesce(btd.cumulative_billed, 0)
        - coalesce(rtd.cumulative_recognized, 0)
        as deferred_revenue_balance
from obligations o
cross join periods p
left join recognition_to_date rtd
    on o.obligation_id = rtd.obligation_id
    and p.period_id = rtd.period_id
left join billing_to_date btd
    on o.obligation_id = btd.obligation_id
    and p.period_id = btd.period_id
{% if is_incremental() %}
where p.period_end_date > (
    select dateadd(day, -3, max(period_end_date)) from {{ this }}
)
{% endif %}
```

## Over-Time Recognition Methods

When a performance obligation is satisfied over time, choose a measurement method:

### Output Methods (measure value transferred to customer)

| Method | Formula | Use when |
|---|---|---|
| Units delivered | `units_delivered / total_units` | Homogeneous units (widgets, data records) |
| Milestones completed | `milestones_complete / total_milestones` | Distinct, measurable milestones |
| Time elapsed | `periods_elapsed / total_periods` | Even delivery over contract term (SaaS) |

### Input Methods (measure effort expended)

| Method | Formula | Use when |
|---|---|---|
| Cost-to-cost | `costs_incurred / estimated_total_costs` | Construction, custom development |
| Labor hours | `hours_worked / estimated_total_hours` | Professional services |

**Time-elapsed (straight-line) is the default for SaaS/subscriptions**:

```sql
-- int_recognition_schedule.sql (over-time, straight-line)
select
    obligation_id,
    period_id,
    1.0 / total_periods as recognition_pct,
    'over_time' as recognition_method,
    cast(row_number() over (
        partition by obligation_id order by period_id
    ) as float) / total_periods as cumulative_pct
from obligation_periods
```

## Anti-Patterns

What Claude consistently gets wrong when modeling revenue:

- **Recognizing revenue at invoice date** -- Invoice date is when you bill, not when you recognize. Recognition is driven by performance obligation satisfaction, which may be months before or after the invoice.
- **Mixing grain levels in `fct_revenue_recognition`** -- A model with both contract-level and obligation-level rows produces doubled revenue when summed. One grain, one model.
- **Omitting period boundaries in revenue queries** -- `SUM(amount)` without `WHERE recognition_date BETWEEN @start AND @end` double-counts revenue across periods.
- **Modeling revenue without performance obligations** -- Skipping Step 2 (identify obligations) and going straight from contract to recognition. Multi-element arrangements require obligation-level tracking.
- **Confusing booked vs recognized revenue** -- Booked = contract signed (backlog). Recognized = obligation satisfied (P&L). These are different measures at different grain.
- **Using `stg_` models for allocation logic** -- Allocation rules are business logic. They belong in `int_` models in silver, not in staging.
- **Flat revenue table without time dimension** -- Revenue without `period_id` prevents period-over-period comparison and deferred revenue calculation.
- **Recognizing 100% at contract start for over-time obligations** -- SaaS revenue recognized ratably over the subscription term, not upfront.

## Reference Files

For deeper guidance on specific patterns:

- **[references/entity-mapping.md](references/entity-mapping.md)** -- Complete entity-to-model mapping with source system fields, SCD types, surrogate key strategies, and relationship cardinalities for every revenue domain entity.
- **[references/recognition-rules.md](references/recognition-rules.md)** -- ASC 606 five-step model mapped to dbt transforms with multi-element arrangement patterns, variable consideration estimation, and over-time measurement methods.
- **[references/evaluations.md](references/evaluations.md)** -- Evaluation scenarios for testing skill effectiveness.
