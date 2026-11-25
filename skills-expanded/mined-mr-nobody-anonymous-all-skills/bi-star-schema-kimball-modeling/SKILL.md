---
name: bi-star-schema-kimball-modeling
description: "Architect production Kimball star schemas with slowly changing dimensions (SCD Types 1, 2, and 3), conformed dimensions, and additive/semi-additive fact tables."
category: business-intelligence
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - business-intelligence
  - data-warehouse
  - kimball
  - star-schema
  - sql
---

# Kimball Dimensional Modeling & Enterprise Data Warehouse Schema Design

## Overview & Core Principles
Architect production Kimball star schemas with slowly changing dimensions (SCD Types 1, 2, and 3), conformed dimensions, and additive/semi-additive fact tables.

### Dimensional Modeling Architecture
1. **Four-Step Design Process**:
   - Select Business Process (e.g., Retail Sales, Claims Adjudication, Subscription Invoicing).
   - Declare the Grain (atomic level of measurement, e.g., one row per line-item on an invoice).
   - Identify the Dimensions (Who, What, Where, When, Why, How).
   - Identify the Facts (numeric additive, semi-additive, or non-additive business metrics).
2. **SCD Type 2 Pattern**:
```sql
CREATE TABLE dim_customer (
    customer_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_bk VARCHAR(64) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    tier VARCHAR(32),
    effective_start_date TIMESTAMP NOT NULL,
    effective_end_date TIMESTAMP NOT NULL DEFAULT '9999-12-31 23:59:59',
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);
```
3. **Design Invariants**:
   - Facts MUST connect to Dimensions exclusively via integer surrogate keys (`sk`), never natural business keys (`bk`).
   - Fact tables must never be directly joined to other fact tables; use drill-conformed dimension navigation.
