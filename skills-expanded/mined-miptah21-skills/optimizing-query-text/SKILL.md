---
name: optimizing-query-text
description: |
  Optimizes Snowflake SQL query performance from provided query text. Use when optimizing Snowflake SQL for:
  (1) User provides or pastes a SQL query and asks to optimize, tune, or improve it
  (2) Task mentions "slow query", "make faster", "improve performance", "optimize SQL", or "query tuning"
  (3) Reviewing SQL for performance anti-patterns (function on filter column, implicit joins, etc.)
  (4) User asks why a query is slow or how to speed it up
---

## OUTPUT FORMAT
Return ONLY the optimized SQL query. No markdown formatting, no explanations, no bullet points - just pure SQL that can be executed directly in Snowflake.

## CRITICAL: Semantic Preservation Rules
**The optimized query MUST return IDENTICAL results to the original.**

Before returning ANY optimization, verify:
- **Same columns**: Exact same columns in exact same order with exact same aliases
- **Same rows**: Filter conditions must be semantically equivalent
- **Same ordering**: Preserve `ORDER BY` exactly as written
- **Same limits**: If original has `LIMIT N`, keep `LIMIT N`. If no LIMIT, do NOT add one.

**If you cannot guarantee identical results, return the original query unchanged.**

---

## Pattern 1: Function on Filter Column
**Problem**: Functions on columns in WHERE clause prevent partition pruning and index usage.

### CAN Fix
| Original | Optimized | Why Safe |
|----------|-----------|----------|
| `WHERE DATE(ts) = '2024-01-01'` | `WHERE ts >= '2024-01-01' AND ts < '2024-01-02'` | Equivalent range |
| `WHERE YEAR(dt) = 2024` | `WHERE dt >= '2024-01-01' AND dt < '2025-01-01'` | Equivalent range |
| `WHERE YEAR(dt) BETWEEN 1995 AND 1996` | `WHERE dt >= '1995-01-01' AND dt < '1997-01-01'` | Equivalent range |

### CANNOT Fix
| Pattern | Why Not |
|---------|---------|
| `WHERE YEAR(dt) IN (SELECT year FROM ...)` | Dynamic values, cannot precompute range |
| `WHERE DATE(ts) = DATE(other_col)` | Comparing two columns, both need function |
| `WHERE EXTRACT(DOW FROM dt) = 1` | Day-of-week has no contiguous range |

---

## Pattern 2: Function on JOIN Column
**Problem**: Functions on JOIN columns prevent hash joins, forcing slower nested loop joins.

### CAN Fix
| Original | Optimized | Why Safe |
|----------|-----------|----------|
| `ON CAST(a.id AS VARCHAR) = CAST(b.id AS VARCHAR)` | `ON a.id = b.id` | If both are same type |
| `ON UPPER(a.code) = UPPER(b.code)` | `ON a.code = b.code` | If data is consistently cased |

### CANNOT Fix
| Pattern | Why Not |
|---------|---------|
| `ON CAST(a.id AS VARCHAR) = b.string_id` | Types genuinely differ |
| `ON DATE(a.timestamp) = b.date_col` | Different granularity |

---

## Pattern 3: NOT IN to NOT EXISTS
**Problem**: `NOT IN` has poor performance and unexpected NULL behavior.

### CAN Fix
| Original | Optimized | Why Safe |
|----------|-----------|----------|
| `WHERE id NOT IN (SELECT id FROM t WHERE ...)` | `WHERE NOT EXISTS (SELECT 1 FROM t WHERE t.id = main.id AND ...)` | When subquery column is NOT NULL |

### CANNOT Fix
| Pattern | Why Not |
|---------|---------|
| `WHERE id NOT IN (SELECT nullable_col FROM t)` | NULL semantics differ |
| `WHERE (a, b) NOT IN (SELECT x, y FROM t)` | Multi-column NULL semantics |

---

## Pattern 4: Duplicate Subqueries → CTEs

### CAN Fix
- Subquery appears 2+ times identically → Extract to CTE

### CANNOT Fix
- Correlated subquery (references outer table)
- Subqueries with different filters

---

## Pattern 5: Implicit Joins → Explicit JOIN
Convert `FROM a, b, c WHERE a.id = b.id AND b.id = c.id` to explicit JOIN syntax.
This is always safe — just restructuring, no semantic change.

---

## UNSAFE Optimizations (NEVER apply)
- **UNION to UNION ALL**: UNION deduplicates rows, UNION ALL does not
- **Changing window functions**: Do not modify nested aggregates
- **Adding redundant filters**: Do not duplicate WHERE filters in JOIN ON
- **Changing column names/aliases**: Copy exactly from original
- **Adding early filtering in JOINs**: If filter is in WHERE, do not duplicate in JOIN ON

---

## Principles
1. **Minimal changes**: Make the fewest changes necessary
2. **Preserve structure**: Keep subqueries, CTEs, and overall structure unless clear benefit
3. **When in doubt, don't**: If unsure whether a change preserves semantics, skip it
4. **Copy exactly**: Column names, table aliases, and expressions character-for-character

## Priority Order
1. **Date/time functions on filter columns** — Highest impact
2. **Implicit joins to explicit JOIN** — Always safe
3. **NOT IN to NOT EXISTS** — Only if NULL-safe

## Requirements
- **Results must be identical**: Same rows, same columns, same order
- **Valid Snowflake SQL**: Output must execute without errors
