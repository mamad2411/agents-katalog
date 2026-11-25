---
name: data-warehouse-schema
description: Design data warehouse schemas with star/snowflake patterns, dimensions, facts, and slowly changing dimensions. Outputs DDL and ETL integration.
argument-hint: [data sources, query patterns, granularity]
allowed-tools: Read, Write, Bash
---

# Data Warehouse Schema Design

Design dimensional data warehouse schemas for analytics. Not normalized OLTP — star/snowflake schemas, fact tables, dimension tables, slowly changing dimensions (SCD), and query optimization.

## Process

1. **Identify business process.** Sales, inventory, customer behavior.
2. **Choose grain.** Transaction-level, daily aggregates, monthly summaries.
3. **Design dimensions.** Time, customer, product, location (de-normalized).
4. **Create fact tables.** Measures (sales, quantity) + foreign keys to dimensions.
5. **Handle SCDs.** Type 1 (overwrite), Type 2 (history), Type 3 (limited history).
6. **Add indexes.** Clustered on date, bitmap on low-cardinality columns.
7. **Plan aggregates.** Pre-compute common rollups for performance.

## Output Format

### Data Warehouse: [Business Domain]

**Model:** Star schema  
**Grain:** Daily sales transactions  
**Dimensions:** 5 (time, customer, product, store, promotion)  
**Fact Tables:** 2 (sales_facts, inventory_facts)  
**SCD Strategy:** Type 2 for customer/product

---

## Star Schema (Recommended)

### Architecture
```
         dim_time
             |
         dim_customer
             |
fact_sales --+-- dim_product
             |
         dim_store
             |
      dim_promotion
```

**Characteristics:**
- De-normalized dimensions (no sub-dimensions)
- Single fact table joins to all dimensions
- Fast queries (fewer joins)
- Redundant data in dimensions (acceptable)

---

## Fact Table (Sales)

```sql
CREATE TABLE fact_sales (
    sale_id BIGSERIAL PRIMARY KEY,
    
    -- Dimension foreign keys
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    store_key INT NOT NULL,
    promotion_key INT,
    
    -- Measures (metrics)
    quantity_sold INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    cost_amount DECIMAL(10,2) NOT NULL,
    profit_amount DECIMAL(10,2) NOT NULL,
    
    -- Degenerate dimensions (attributes with no separate dimension)
    transaction_number VARCHAR(50),
    payment_method VARCHAR(20),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (date_key) REFERENCES dim_time(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (promotion_key) REFERENCES dim_promotion(promotion_key)
);

-- Indexes for query performance
CREATE INDEX idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_store ON fact_sales(store_key);

-- Composite index for common query patterns
CREATE INDEX idx_fact_sales_date_store ON fact_sales(date_key, store_key);
```

---

## Time Dimension

```sql
CREATE TABLE dim_time (
    date_key INT PRIMARY KEY,  -- YYYYMMDD e.g., 20240115
    
    full_date DATE NOT NULL,
    
    -- Day attributes
    day_of_week VARCHAR(10),
    day_of_month INT,
    day_of_year INT,
    weekday_flag BOOLEAN,  -- TRUE if Mon-Fri
    
    -- Week attributes
    week_of_year INT,
    iso_week VARCHAR(8),  -- 2024-W03
    
    -- Month attributes
    month_number INT,
    month_name VARCHAR(10),
    month_abbr VARCHAR(3),
    year_month VARCHAR(7),  -- 2024-01
    
    -- Quarter attributes
    quarter_number INT,
    quarter_name VARCHAR(6),  -- Q1 2024
    
    -- Year attributes
    year INT,
    fiscal_year INT,
    fiscal_quarter INT,
    
    -- Special flags
    is_holiday BOOLEAN,
    holiday_name VARCHAR(50),
    is_last_day_of_month BOOLEAN,
    
    UNIQUE(full_date)
);

-- Pre-populate time dimension (10 years)
INSERT INTO dim_time
SELECT 
    TO_CHAR(d, 'YYYYMMDD')::INT AS date_key,
    d AS full_date,
    TO_CHAR(d, 'Day') AS day_of_week,
    EXTRACT(DAY FROM d) AS day_of_month,
    EXTRACT(DOY FROM d) AS day_of_year,
    EXTRACT(ISODOW FROM d) <= 5 AS weekday_flag,
    EXTRACT(WEEK FROM d) AS week_of_year,
    TO_CHAR(d, 'IYYY-IW') AS iso_week,
    EXTRACT(MONTH FROM d) AS month_number,
    TO_CHAR(d, 'Month') AS month_name,
    TO_CHAR(d, 'Mon') AS month_abbr,
    TO_CHAR(d, 'YYYY-MM') AS year_month,
    EXTRACT(QUARTER FROM d) AS quarter_number,
    'Q' || EXTRACT(QUARTER FROM d) || ' ' || EXTRACT(YEAR FROM d) AS quarter_name,
    EXTRACT(YEAR FROM d) AS year,
    EXTRACT(YEAR FROM d) AS fiscal_year,
    EXTRACT(QUARTER FROM d) AS fiscal_quarter,
    FALSE AS is_holiday,
    NULL AS holiday_name,
    d = (DATE_TRUNC('MONTH', d) + INTERVAL '1 MONTH - 1 day')::DATE AS is_last_day_of_month
FROM generate_series('2020-01-01'::DATE, '2030-12-31'::DATE, '1 day'::INTERVAL) d;
```

---

## Customer Dimension (SCD Type 2)

```sql
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,  -- Surrogate key
    
    customer_id VARCHAR(50) NOT NULL,  -- Natural key
    
    -- Customer attributes
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    
    -- Address (de-normalized)
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    
    -- Segmentation
    customer_segment VARCHAR(50),  -- Gold, Silver, Bronze
    loyalty_tier VARCHAR(20),
    
    -- SCD Type 2 columns
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customer_id ON dim_customer(customer_id);
CREATE INDEX idx_customer_current ON dim_customer(customer_id, is_current)
    WHERE is_current = TRUE;
```

**SCD Type 2 Example:**
```
customer_key | customer_id | name | segment | effective_date | expiration_date | is_current
-------------|-------------|------|---------|----------------|-----------------|------------
1            | C001        | John | Bronze  | 2023-01-01     | 2023-06-30      | FALSE
2            | C001        | John | Silver  | 2023-07-01     | NULL            | TRUE
```

---

## Product Dimension (SCD Type 2)

```sql
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    
    product_id VARCHAR(50) NOT NULL,  -- SKU
    
    -- Product attributes
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    brand VARCHAR(100),
    
    -- Hierarchy (de-normalized)
    category VARCHAR(100),
    subcategory VARCHAR(100),
    department VARCHAR(100),
    
    -- Attributes
    unit_of_measure VARCHAR(20),
    package_size VARCHAR(50),
    
    -- Pricing
    standard_cost DECIMAL(10,2),
    list_price DECIMAL(10,2),
    
    -- SCD Type 2
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_id ON dim_product(product_id);
CREATE INDEX idx_product_current ON dim_product(product_id, is_current)
    WHERE is_current = TRUE;
```

---

## Store Dimension

```sql
CREATE TABLE dim_store (
    store_key SERIAL PRIMARY KEY,
    
    store_id VARCHAR(20) NOT NULL UNIQUE,
    
    store_name VARCHAR(255) NOT NULL,
    
    -- Location
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    
    -- Attributes
    store_type VARCHAR(50),  -- Mall, Standalone, Airport
    store_size_sqft INT,
    
    -- Hierarchy
    region VARCHAR(50),
    district VARCHAR(50),
    
    -- Manager
    manager_name VARCHAR(100),
    
    opened_date DATE,
    closed_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);
```

---

## Snowflake Schema (Normalized Dimensions)

```
                dim_time
                    |
                dim_customer --> dim_city --> dim_state
                    |
    fact_sales -----+
                    |
                dim_product --> dim_category --> dim_department
                    |
                dim_store
```

**When to use:**
- Reduce dimension table size (millions of rows)
- Strong hierarchies (geography, product taxonomy)
- Storage constraints

**Trade-off:** More joins = slower queries

---

## Slowly Changing Dimensions

### Type 1: Overwrite (No History)
```sql
-- Update existing row
UPDATE dim_customer
SET customer_segment = 'Gold',
    updated_at = CURRENT_TIMESTAMP
WHERE customer_id = 'C001'
  AND is_current = TRUE;
```

### Type 2: Full History (Most Common)
```sql
-- Expire old row
UPDATE dim_customer
SET expiration_date = CURRENT_DATE - 1,
    is_current = FALSE
WHERE customer_id = 'C001'
  AND is_current = TRUE;

-- Insert new row
INSERT INTO dim_customer (
    customer_id, first_name, last_name, customer_segment,
    effective_date, is_current
) VALUES (
    'C001', 'John', 'Doe', 'Gold',
    CURRENT_DATE, TRUE
);
```

### Type 3: Limited History (Previous Value)
```sql
ALTER TABLE dim_customer
ADD COLUMN previous_segment VARCHAR(50),
ADD COLUMN segment_change_date DATE;

UPDATE dim_customer
SET previous_segment = customer_segment,
    segment_change_date = CURRENT_DATE,
    customer_segment = 'Gold'
WHERE customer_id = 'C001';
```

---

## Aggregate Tables (Performance)

```sql
-- Daily sales summary (pre-aggregated)
CREATE TABLE fact_sales_daily (
    date_key INT NOT NULL,
    store_key INT NOT NULL,
    product_key INT NOT NULL,
    
    total_quantity INT,
    total_revenue DECIMAL(12,2),
    total_cost DECIMAL(12,2),
    total_profit DECIMAL(12,2),
    transaction_count INT,
    
    PRIMARY KEY (date_key, store_key, product_key)
);

-- Monthly sales summary
CREATE TABLE fact_sales_monthly (
    year_month VARCHAR(7) NOT NULL,
    store_key INT NOT NULL,
    
    total_revenue DECIMAL(12,2),
    total_transactions INT,
    avg_transaction_value DECIMAL(10,2),
    
    PRIMARY KEY (year_month, store_key)
);

-- Refresh via scheduled job
INSERT INTO fact_sales_daily
SELECT 
    date_key,
    store_key,
    product_key,
    SUM(quantity_sold),
    SUM(total_amount),
    SUM(cost_amount),
    SUM(profit_amount),
    COUNT(*)
FROM fact_sales
WHERE date_key = TO_CHAR(CURRENT_DATE - 1, 'YYYYMMDD')::INT
GROUP BY date_key, store_key, product_key;
```

---

## Common Queries

### Sales by Month
```sql
SELECT 
    t.year_month,
    SUM(f.total_amount) AS revenue,
    SUM(f.quantity_sold) AS units_sold,
    COUNT(DISTINCT f.customer_key) AS unique_customers
FROM fact_sales f
JOIN dim_time t ON f.date_key = t.date_key
WHERE t.year = 2024
GROUP BY t.year_month
ORDER BY t.year_month;
```

### Top Products by Category
```sql
SELECT 
    p.category,
    p.product_name,
    SUM(f.total_amount) AS revenue,
    RANK() OVER (PARTITION BY p.category ORDER BY SUM(f.total_amount) DESC) AS rank
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_time t ON f.date_key = t.date_key
WHERE t.year = 2024
  AND p.is_current = TRUE
GROUP BY p.category, p.product_name
QUALIFY rank <= 10;
```

### Customer Lifetime Value
```sql
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    MIN(t.full_date) AS first_purchase_date,
    MAX(t.full_date) AS last_purchase_date,
    COUNT(DISTINCT f.sale_id) AS total_transactions,
    SUM(f.total_amount) AS lifetime_value
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_time t ON f.date_key = t.date_key
WHERE c.is_current = TRUE
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY lifetime_value DESC
LIMIT 100;
```

---

## ETL Integration

```python
# Load fact table from OLTP
def load_sales_facts(date):
    """ETL: Extract from OLTP, transform, load to warehouse"""
    
    # Extract from source database
    sales = extract_sales(date)
    
    # Lookup dimension keys
    for sale in sales:
        sale['date_key'] = get_date_key(sale['sale_date'])
        sale['customer_key'] = get_customer_key(sale['customer_id'], sale['sale_date'])
        sale['product_key'] = get_product_key(sale['product_id'], sale['sale_date'])
        sale['store_key'] = get_store_key(sale['store_id'])
    
    # Load to warehouse
    insert_fact_sales(sales)

def get_customer_key(customer_id, as_of_date):
    """Get SCD Type 2 customer key for specific date"""
    return db.query("""
        SELECT customer_key
        FROM dim_customer
        WHERE customer_id = %s
          AND effective_date <= %s
          AND (expiration_date IS NULL OR expiration_date >= %s)
    """, [customer_id, as_of_date, as_of_date])
```

## Rules

- Grain must be clearly defined before schema design — finest level of detail in fact table.
- Surrogate keys (integers) for all dimensions — natural keys can change, surrogates never do.
- Time dimension pre-populated for 10+ years — no runtime generation.
- Fact tables store measures only, no descriptive text — dimensions hold descriptions.
- De-normalize dimensions in star schema — performance over normalization.
- SCD Type 2 for tracking history — customer segments, product prices change over time.
- Indexes on all foreign keys in fact tables — query performance.
- Aggregate tables for common rollups — pre-compute monthly/yearly summaries.
- Never update fact table rows — insert-only for auditability.
- Late-arriving dimensions handled with default "Unknown" row — don't block fact loading.
