---
name: dune-to-allium
description: Convert Dune (Trino) SQL queries to Allium (Snowflake) SQL. SQL dialect conversions (Trino → Snowflake) apply to all chains. Comprehensive Solana and EVM chain mappings included.
allowed-tools: Read, Grep, Glob, Bash(uv:*), Bash(python*:*), Bash(curl:*), WebSearch
---

# Dune → Allium Query Conversion Skill

Convert Dune Analytics (Trino) SQL queries to Allium (Snowflake) SQL. SQL dialect conversions apply to all chains. Comprehensive Solana and EVM chain mappings included.

## Prerequisites

- **Allium API key** in `~/.allium/credentials`:
  ```
  API_KEY=allium_...
  QUERY_ID=...
  ```
  Get your key at https://app.allium.so/settings/api-keys. If `QUERY_ID` is missing, the `allium_query.py` script creates one automatically.
- (Optional) `DUNE_API_KEY` in project `.env` file for automated result fetching via `dune_query.py`. Alternatively, run the original query in the [Dune app](https://dune.com) and export results manually.

## Conversion Workflow

### Step 1: Accept Dune SQL

Get the Dune query via one of:

- **Pasted SQL**: User pastes Dune SQL directly
- **Saved query ID**: Fetch results via Dune API for comparison:
  ```bash
  uv run ~/.claude/skills/dune-to-allium/scripts/dune_query.py QUERY_ID --json > dune_results.json
  ```

> **Note**: Dune API free tier only supports fetching results of saved queries by ID. It does NOT support executing arbitrary SQL.

### Step 2: Identify Dune-Specific Tables and Syntax

Scan the query for:

1. **Dune tables** — Look up each in [SOLANA_MAPPINGS.md](SOLANA_MAPPINGS.md) table mappings section
2. **Dune column names** — Map using the column mappings section
3. **Trino-specific SQL** — Identify array functions, date syntax, unnest patterns
4. **Dune parameters** — `{{param}}` syntax needs replacement

Common Dune tables and their Allium equivalents:

| Dune Table | Allium Table | Special Handling |
|------------|-------------|------------------|
| `solana.instruction_calls` | `solana.raw.instructions` UNION `solana.raw.inner_instructions` | Always UNION both |
| `solana.account_activity` | `solana.assets.transfers` | Different approach entirely |
| `tokens_solana.transfers` | `solana.assets.transfers` | Amount is pre-normalized |
| `jupiter_solana.aggregator_swaps` | `solana.dex.aggregator_trades` | Different granularity! |
| `prices.usd` | `common.prices.hourly` | Different column names |
| `solana.transactions` | `solana.raw.transactions` | |

### Step 3: Apply Table Mappings

For each Dune table, apply the conversion from [SOLANA_MAPPINGS.md](SOLANA_MAPPINGS.md):

#### Instructions (CRITICAL — most common conversion)

```sql
-- Dune: single table
FROM solana.instruction_calls
WHERE executing_account = '{program}' AND tx_success = true

-- Allium: UNION outer + inner, use parent_tx_success
WITH all_instructions AS (
    SELECT * FROM solana.raw.instructions
    WHERE program_id = '{program}' AND parent_tx_success = true
      AND block_timestamp >= '{start}' AND block_timestamp < '{end}'
    UNION ALL
    SELECT * FROM solana.raw.inner_instructions
    WHERE program_id = '{program}' AND parent_tx_success = true
      AND block_timestamp >= '{start}' AND block_timestamp < '{end}'
)
```

#### Account Activity → Transfers

```sql
-- Dune: balance changes
FROM solana.account_activity
WHERE address = '{addr}' AND tx_success = true

-- Allium: use transfers table (do NOT use balances with LAG)
FROM solana.assets.transfers
WHERE to_address = '{addr}'
  AND transfer_type IN ('spl_token_transfer', 'sol_transfer')
```

### Step 4: Apply SQL Dialect Conversions

Apply these Trino → Snowflake transformations:

| Find | Replace With |
|------|-------------|
| `account_arguments[N]` | `accounts[N-1]` (subtract 1) |
| `cardinality(arr)` | `ARRAY_SIZE(arr)` |
| `CROSS JOIN UNNEST(arr) AS t(val)` | `, LATERAL FLATTEN(input => arr) f` (use `f.value`) |
| `NOW()` | `CURRENT_TIMESTAMP()` |
| `INTERVAL '7' DAY` | `INTERVAL '7 days'` |
| `FROM_UTF8(data)` | `TRY_TO_VARCHAR(data, 'UTF-8')` |
| `block_time` | `block_timestamp` |
| `tx_id` | `txn_id` |
| `executing_account` | `program_id` |
| `tx_success` | `parent_tx_success` (instructions) or `success` (transactions) |
| `approx_distinct(col)` | `APPROX_COUNT_DISTINCT(col)` |

Full reference: [SOLANA_MAPPINGS.md](SOLANA_MAPPINGS.md) SQL dialect section.

### Step 5: Handle Structural Differences

Check [KNOWN_DIFFERENCES.md](KNOWN_DIFFERENCES.md) for expected deltas:

- **Pricing**: Allium prices more tokens → ~76% higher `transfers_usd_value`
- **Jupiter swaps**: Different granularity (legs vs aggregated swaps)
- **Transfer types**: Filter `transfer_type IN ('spl_token_transfer', 'sol_transfer')` to exclude account closures
- **Amounts**: Allium `amount` is pre-normalized — remove any `/ pow(10, decimals)` division

### Step 6: Add Timestamp Filters

**CRITICAL**: Solana tables are massive. Always add tight timestamp filters:

```sql
WHERE block_timestamp >= '2024-01-01'::TIMESTAMP
  AND block_timestamp < '2024-01-02'::TIMESTAMP
```

Queries without timestamp filters on Solana tables will time out.

### Step 7: Run Converted Query

Write the converted SQL to a `.sql` file in the project directory, then execute via the Allium Explorer API:

```bash
uv run ~/.claude/skills/dune-to-allium/scripts/allium_query.py --file converted_query.sql
```

Or with inline SQL:

```bash
uv run ~/.claude/skills/dune-to-allium/scripts/allium_query.py "SELECT * FROM ethereum.raw.blocks LIMIT 10"
```

Add `--json` to get machine-readable output:

```bash
uv run ~/.claude/skills/dune-to-allium/scripts/allium_query.py --file converted_query.sql --json > /tmp/allium_results.json
```

### Step 8: Compare Results (Optional)

If you have Dune results to compare against:

```bash
# Fetch Dune results
uv run ~/.claude/skills/dune-to-allium/scripts/dune_query.py QUERY_ID --json > /tmp/dune_results.json

# Run Allium query and save results
uv run ~/.claude/skills/dune-to-allium/scripts/allium_query.py --file converted_query.sql --json > /tmp/allium_results.json

# Compare
uv run ~/.claude/skills/dune-to-allium/scripts/compare_results.py /tmp/dune_results.json /tmp/allium_results.json
```

The comparison tool auto-maps known column name differences (e.g., `tx_id` ↔ `txn_id`).

### Investigating Dune Spellbook Filters

When results differ due to Dune spellbook filtering logic (wash trading filters, hardcoded date exclusions, etc.), search the public spellbook repo:

- Search `github.com/duneanalytics/spellbook` for the table or model name
- Look for `WHERE` clauses, CTEs named `filter`, or hardcoded address/date exclusions
- ~90% of discrepancies come from spellbook filters, not data differences

## Checklist

Before finalizing a conversion, verify:

### All Chains
- [ ] `block_time` → `block_timestamp`
- [ ] `NOW()` → `CURRENT_TIMESTAMP()`
- [ ] `INTERVAL '7' DAY` → `INTERVAL '7 days'`
- [ ] `SUM(...) FILTER (WHERE ...)` → `SUM(CASE WHEN ... THEN ... ELSE 0 END)`
- [ ] `CROSS JOIN UNNEST` → `LATERAL FLATTEN`
- [ ] `cardinality()` → `ARRAY_SIZE()`
- [ ] Array indices shifted by -1 (Trino is 1-based, Snowflake is 0-based)
- [ ] `query_XXXXX` references identified and inlined or flagged as blocking
- [ ] `get_href()` calls removed (Dune UI function)
- [ ] Dune parameters (`{{param}}`) replaced with values or Snowflake variables

### Solana-Specific
- [ ] All `instruction_calls` references use UNION of outer + inner instructions
- [ ] `tx_id` → `txn_id`
- [ ] Success filter uses `parent_tx_success = true` (not JOIN)
- [ ] `transfer_type` filter applied when using `solana.assets.transfers`
- [ ] Removed `/ pow(10, decimals)` if using Allium's `amount` column

### EVM-Specific
- [ ] `{chain}.transactions` → `{chain}.raw.transactions`
- [ ] `{chain}.logs` → `{chain}.raw.logs`
- [ ] Decoded tables → `{chain}.decoded.logs` / `{chain}.decoded.traces` with filters
- [ ] Spellbook table dependencies identified (e.g., `staking_ethereum.info`)
- [ ] ERC20 transfers: `amount` is pre-normalized — remove `/ pow(10, decimals)`
- [ ] DEX queries: combine `dex.orderflow` + `dex.trades` (exclude overlapping txs)
- [ ] Column names: `TRANSACTION_HASH` (not `TX_HASH`), `USD_AMOUNT` (not `AMOUNT_USD`) in `dex.trades`
- [ ] BSC chain prefix: `bsc.*` (not `bnb.*` or `binance.*`)

## Reference Files

- [SOLANA_MAPPINGS.md](SOLANA_MAPPINGS.md) — Solana table/column mappings + all SQL dialect conversions (Trino → Snowflake)
- [EVM_MAPPINGS.md](EVM_MAPPINGS.md) — EVM chain table/column mappings (Ethereum, Arbitrum, Base, etc.)
- [KNOWN_DIFFERENCES.md](KNOWN_DIFFERENCES.md) — Expected result deltas and why they occur
