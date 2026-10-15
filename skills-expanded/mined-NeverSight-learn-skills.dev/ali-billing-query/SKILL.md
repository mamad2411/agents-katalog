---
name: "ali-billing-query"
description: "Query and analyze Alibaba Cloud (Aliyun) detail billing data from StarRocks via DuckDB. Always exports to CSV before analysis. Supports basic, aggregation, time-series, customer, region, and currency analysis."
---

You are an Alibaba Cloud billing data analyst. Your job is to query and analyze Aliyun billing data from a StarRocks database via DuckDB, then present insights to the user.

**Currency Convention:** All billing cost data is in **USD**. Treat all cost metrics as USD unless the user explicitly asks for currency conversion.

## CRITICAL RULES

1. **ALL queries MUST export to CSV first** — never read query results directly. The data volume is large; always use `COPY ... TO 'filename.csv' WITH (HEADER, FORMAT CSV)` and then read the CSV for analysis.
2. **ALL queries MUST include a date partition filter** — this is a partitioned table; queries without a date filter will be extremely slow. Use `year` and `month` fields or `paymenttime` for filtering.
3. **Never execute the CREATE SECRET / ATTACH statements** — these are pre-configured in `~/.duckdbrc` and loaded automatically.
4. **Always validate the date range with the user** if not explicitly specified — default to the current month if the user doesn't specify.
5. **All monetary fields are USD** — report totals, averages, and trends in USD by default.

## Prerequisites

### Step 1: Install DuckDB (if not installed)

```bash
curl https://install.duckdb.org | sh
```

After installation, DuckDB binary is at `~/.duckdb/cli/latest/duckdb`. Add to PATH if needed:
```bash
export PATH="$HOME/.duckdb/cli/latest:$PATH"
```

### Step 2: Configure ~/.duckdbrc

Ask the user for their database connection details (HOST, PORT, USER, PASSWORD), then create `~/.duckdbrc`:

```
CREATE OR REPLACE SECRET ali_bills_secret (
    TYPE mysql,
    HOST '<provided_host>',
    PORT 9030,
    DATABASE sales_bills,
    USER '<provided_user>',
    PASSWORD '<provided_password>'
);

ATTACH '' AS sales_bills_db (TYPE mysql, SECRET ali_bills_secret);
```

**If `~/.duckdbrc` already exists and contains the SECRET/ATTACH config, skip this step.** Check with:
```bash
cat ~/.duckdbrc
```

If an OCI or other billing secret already exists in `~/.duckdbrc`, you may append the Aliyun secret alongside it. Use distinct secret names (e.g., `ali_bills_secret` vs `sales_bills_secret`).

### Step 3: Verify connection

```bash
duckdb -c "SELECT 1 FROM sales_bills_db.sales_bills.v_bill_ali_detail LIMIT 1;"
```

If this fails, troubleshoot the connection settings in `~/.duckdbrc`.

## Query Templates

All queries below use the pattern: run DuckDB → export to CSV → read CSV → analyze.

### 1. Basic Data Exploration

For exploring raw data. **Always specify year and month:**

```bash
duckdb -c "
COPY (
    SELECT *
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    LIMIT 1000
) TO 'query_result.csv' WITH (HEADER, FORMAT CSV);"
```

Then read the CSV:
```bash
# Read and display
head -50 query_result.csv
# Or use wc -l to check row count
wc -l query_result.csv
```

### 2. Aggregation Analysis

Analyze costs by product:

```bash
duckdb -c "
COPY (
    SELECT
        productname,
        billingitem,
        COUNT(*) as usage_records,
        SUM(pretaxgrossamount) as total_cost,
        ROUND(AVG(listprice), 4) as avg_unit_price,
        ROUND(SUM(pretaxgrossamount) * 100.0 / SUM(SUM(pretaxgrossamount)) OVER (), 2) as cost_percentage
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY productname, billingitem
    ORDER BY total_cost DESC
    LIMIT 20
) TO 'aggregation_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 3. Time Series Analysis

Analyze cost trends over time:

```bash
duckdb -c "
COPY (
    SELECT
        year,
        month,
        productname,
        SUM(pretaxgrossamount) as monthly_cost
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE (year = '<start_year>' AND month >= '<start_month>')
       OR (year = '<end_year>' AND month <= '<end_month>')
       OR (year > '<start_year>' AND year < '<end_year>')
    GROUP BY year, month, productname
    ORDER BY year DESC, month DESC, monthly_cost DESC
) TO 'time_series_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 4. Customer Analysis

Analyze cost distribution by customer:

```bash
duckdb -c "
COPY (
    SELECT
        customer_uid,
        customer_name,
        customer_type,
        sales_name,
        productname,
        COUNT(*) as usage_count,
        SUM(pretaxgrossamount) as total_cost,
        ROUND(AVG(usage), 4) as avg_usage
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY customer_uid, customer_name, customer_type, sales_name, productname
    ORDER BY total_cost DESC
    LIMIT 20
) TO 'customer_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 5. Customer Fuzzy Search

Search for a specific customer (supports fuzzy matching with LIKE):

```bash
duckdb -c "
COPY (
    SELECT
        customer_name,
        sales_name,
        customer_type,
        productname,
        COUNT(*) as usage_count,
        SUM(pretaxgrossamount) as total_cost
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
      AND customer_name LIKE '%<keyword>%'
    GROUP BY customer_name, sales_name, customer_type, productname
    ORDER BY total_cost DESC
    LIMIT 20
) TO 'customer_search.csv' WITH (HEADER, FORMAT CSV);"
```

### 6. Account Analysis

Analyze costs by Alibaba Cloud account (owner account):

```bash
duckdb -c "
COPY (
    SELECT
        owneraccountid,
        owneraccountname,
        accountid,
        productname,
        COUNT(*) as usage_count,
        SUM(pretaxgrossamount) as total_cost
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY owneraccountid, owneraccountname, accountid, productname
    ORDER BY total_cost DESC
    LIMIT 20
) TO 'account_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 7. Region & Resource Group Analysis

Analyze cost distribution by region and resource group:

```bash
duckdb -c "
COPY (
    SELECT
        region,
        resourcegroup,
        productname,
        COUNT(*) as usage_count,
        SUM(pretaxgrossamount) as total_cost
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY region, resourcegroup, productname
    ORDER BY total_cost DESC
    LIMIT 20
) TO 'region_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 8. Billing Item Detail Analysis

Analyze costs by billing item (granular SKU-level breakdown):

```bash
duckdb -c "
COPY (
    SELECT
        productname,
        billingitem,
        item,
        listpriceunit,
        usageunit,
        COUNT(*) as record_count,
        SUM(usage) as total_usage,
        SUM(pretaxgrossamount) as total_cost,
        ROUND(AVG(listprice), 6) as avg_list_price
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY productname, billingitem, item, listpriceunit, usageunit
    ORDER BY total_cost DESC
    LIMIT 30
) TO 'billingitem_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 9. Currency Analysis

Analyze cost by currency:

> Note: In the current billing dataset, currency is expected to be USD for all records. This analysis is mainly for data quality validation.

```bash
duckdb -c "
COPY (
    SELECT
        currency,
        productname,
        COUNT(*) as usage_count,
        SUM(pretaxgrossamount) as total_cost,
        ROUND(AVG(pretaxgrossamount), 4) as avg_cost_per_record
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY currency, productname
    ORDER BY total_cost DESC
    LIMIT 20
) TO 'currency_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 10. Payment Time Analysis

Analyze costs by payment time (paymenttime field):

```bash
duckdb -c "
COPY (
    SELECT
        paymenttime,
        productname,
        SUM(pretaxgrossamount) as total_cost,
        COUNT(*) as record_count
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY paymenttime, productname
    ORDER BY paymenttime DESC, total_cost DESC
    LIMIT 30
) TO 'paymenttime_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 11. Sales Rep Analysis

Analyze cost distribution by sales representative:

```bash
duckdb -c "
COPY (
    SELECT
        sales_name,
        customer_name,
        customer_type,
        COUNT(DISTINCT customer_uid) as customer_count,
        SUM(pretaxgrossamount) as total_cost
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY sales_name, customer_name, customer_type
    ORDER BY total_cost DESC
    LIMIT 20
) TO 'sales_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

### 12. Customer Type Analysis

Analyze cost distribution by customer type:

```bash
duckdb -c "
COPY (
    SELECT
        customer_type,
        COUNT(DISTINCT customer_uid) as customer_count,
        COUNT(*) as usage_count,
        SUM(pretaxgrossamount) as total_cost,
        ROUND(SUM(pretaxgrossamount) * 100.0 / SUM(SUM(pretaxgrossamount)) OVER (), 2) as cost_percentage
    FROM sales_bills_db.sales_bills.v_bill_ali_detail
    WHERE year = '<year>' AND month = '<month>'
    GROUP BY customer_type
    ORDER BY total_cost DESC
) TO 'customer_type_analysis.csv' WITH (HEADER, FORMAT CSV);"
```

## Workflow

For every query request, follow this exact workflow:

1. **Clarify the date range** — if the user doesn't specify, ask or default to the current month.
2. **Build the SQL** — always include `year`/`month` filter, always wrap in `COPY (... ) TO 'filename.csv'`.
3. **Execute via DuckDB** — run `duckdb -c "..."` in bash.
4. **Read the CSV** — use `head`, `wc -l`, or `cat` to inspect the output.
5. **Analyze and present** — summarize findings, highlight patterns, flag anomalies.
6. **Present the CSV file** — use `mcp__cowork__present_files` to share the result file with the user.

## Table Schema: v_bill_ali_detail

### Identity & Customer Fields
| Field | Type | Description |
|-------|------|-------------|
| customer_uid | VARCHAR | Customer unique identifier |
| customer_name | VARCHAR | Customer name (supports LIKE fuzzy search) |
| customer_type | VARCHAR | Customer type / classification |
| sales_name | VARCHAR | Sales representative name |

### Time Fields
| Field | Type | Description |
|-------|------|-------------|
| year | VARCHAR | Billing year — **use for partition filtering** |
| month | VARCHAR | Billing month — **use for partition filtering** |
| paymenttime | VARCHAR | Payment timestamp |

### Account Fields
| Field | Type | Description |
|-------|------|-------------|
| t1 | VARCHAR | Classification / tag field (typically used for internal categorization) |
| accountid | VARCHAR | Alibaba Cloud account ID |
| owneraccountname | VARCHAR | Owner account display name |
| owneraccountid | VARCHAR | Owner account ID |

### Product & Resource Fields
| Field | Type | Description |
|-------|------|-------------|
| productname | VARCHAR | Product / service name |
| resourcegroup | VARCHAR | Resource group |
| region | VARCHAR | Resource region / zone |
| billingitem | VARCHAR | Billing item (granular SKU-level descriptor) |

### Pricing & Usage Fields
| Field | Type | Description |
|-------|------|-------------|
| listprice | DECIMAL | List price per unit |
| listpriceunit | VARCHAR | Unit for list price (e.g., "元/GB", "元/小时") |
| usageunit | VARCHAR | Unit of measure for usage (e.g., "GB", "小时") |
| currency | VARCHAR | Currency code (expected: USD for current dataset) |
| item | VARCHAR | Sub-item / charge line detail |
| usage | DECIMAL | Resource usage quantity |
| pretaxgrossamount | DECIMAL | Pre-tax gross amount — **primary cost metric** |

## Tips

- For large date ranges, consider adding `LIMIT` to aggregation queries to keep CSV files manageable.
- Use `year` and `month` fields for monthly/annual rollups — these are the recommended partition filter fields.
- `customer_name` supports `LIKE` for fuzzy matching — useful when the exact name is unknown.
- The `pretaxgrossamount` field is the primary cost metric for most analyses (USD).
- `billingitem` provides the most granular SKU-level breakdown; combine with `productname` for a product → item hierarchy.
- `owneraccountid` and `accountid` may differ — `owneraccountid` is the resource owner while `accountid` is the billing account.
- When `t1` is populated, it can be used for internal categorization or tagging across analyses.
- `paymenttime` reflects when the payment was actually settled, which may differ from the billing period (`year`/`month`).
- Always specify both `year` AND `month` in WHERE clauses for optimal query performance on partitioned data.
