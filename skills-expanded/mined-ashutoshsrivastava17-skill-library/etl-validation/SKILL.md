---
name: etl-validation
description: >
  Validate ETL/ELT pipelines end-to-end: source-to-target mapping verification,
  row count reconciliation, data type validation, transformation logic testing,
  and regression testing. Produce a validation report with pass/fail status per check.
  TRIGGER when: user says /etl-validation, "validate ETL", "test pipeline",
  "data pipeline validation", "source to target testing", or "ETL reconciliation".
argument-hint: "[pipeline name or source-target pair]"
user-invocable: true
---

# ETL/ELT Pipeline Validation

You are an expert data engineer specializing in pipeline quality assurance. When the user asks you to validate an ETL or ELT pipeline, follow this structured process to ensure data moves correctly from source to target.

## Step 1: Pipeline Inventory

Gather context about the pipeline under test:

| Attribute | Detail |
|-----------|--------|
| Pipeline name | Unique identifier for the pipeline |
| Source system(s) | Database, API, file, streaming platform |
| Target system(s) | Data warehouse, data lake, downstream service |
| Orchestrator | Airflow, dbt, Fivetran, Glue, Spark, custom |
| Schedule / trigger | Cron, event-driven, manual |
| SLA | Expected completion time, freshness requirement |
| Last successful run | Timestamp of most recent success |
| Known issues | Any existing bugs or limitations |
| Transformation complexity | Low (copy), Medium (joins/filters), High (complex logic) |

## Step 2: Source-to-Target Mapping Validation

Verify every field maps correctly from source to target.

### Mapping Matrix

| Source Table | Source Column | Source Type | Target Table | Target Column | Target Type | Transform Rule | Status |
|-------------|-------------|------------|-------------|--------------|------------|---------------|--------|
| ... | ... | ... | ... | ... | ... | Direct / Derived / Aggregated / Lookup | Pass / Fail |

### Checks to Execute

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| All source fields accounted for | Compare source schema to mapping doc | No unmapped source fields (unless intentionally excluded) |
| All target fields sourced | Compare target schema to mapping doc | Every target field has a defined source |
| Data type compatibility | Compare source type to target type | No lossy conversions (e.g., FLOAT to INT) |
| Naming conventions | Review target column names | Follow target system naming standards |
| Transformation documentation | Each derived field has logic documented | 100% of derived fields documented |

## Step 3: Row Count Reconciliation

Verify record counts match expectations at every stage.

| Checkpoint | Query / Method | Expected | Actual | Delta | Status |
|-----------|---------------|----------|--------|-------|--------|
| Source total rows | COUNT(*) on source | -- | -- | -- | -- |
| After extraction | COUNT(*) post-extract | = Source | -- | -- | -- |
| After filtering | COUNT(*) post-filter | Source - filtered | -- | -- | -- |
| After deduplication | COUNT(*) post-dedup | Filtered - dupes | -- | -- | -- |
| After joins | COUNT(*) post-join | Depends on join type | -- | -- | -- |
| Target total rows | COUNT(*) on target | = After all transforms | -- | -- | -- |

**Reconciliation Rules:**

- **Full load**: Target count = Source count (after filters/dedup)
- **Incremental load**: Target delta = Source delta for the load window
- **SCD Type 2**: Target rows >= Source rows (historical records add rows)
- **Aggregation**: Target rows < Source rows; verify GROUP BY cardinality

**Acceptable Variance**: Define per pipeline (typically 0% for transactional, < 0.1% for large analytical loads).

## Step 4: Data Type and Schema Validation

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| Column count match | Compare target DDL to expected schema | Exact match |
| Data type match | Compare each column type | All types match specification |
| Nullable constraints | Check NOT NULL columns for nulls | Zero nulls in NOT NULL columns |
| Primary key integrity | COUNT(DISTINCT pk) = COUNT(*) | No duplicates |
| Foreign key integrity | All FK values exist in parent table | 100% referential integrity |
| String length | MAX(LEN(col)) <= declared length | No truncation |
| Precision / scale | Decimal values maintain precision | No rounding errors |
| Encoding | Character set compatibility | No mojibake or encoding errors |

## Step 5: Transformation Logic Verification

For each transformation rule, validate correctness:

### Test Strategy per Transform Type

| Transform Type | Test Method | Sample Size |
|---------------|------------|-------------|
| Direct copy | Source value = Target value for sampled rows | Min 1,000 rows or 1% |
| Type cast | Verify no data loss (e.g., timestamp precision) | All edge values |
| Lookup / join | Verify join keys resolve correctly, handle nulls | All distinct key values |
| Aggregation | Manually compute aggregate for a subset, compare | 5-10 groups |
| Conditional logic | Test each branch with representative data | All branches covered |
| String manipulation | Verify trim, concat, case conversion, parsing | Edge cases (empty, null, max length) |
| Date logic | Test timezone handling, fiscal calendar, epoch conversion | Boundary dates |
| Calculated fields | Recompute formula independently, compare | Random sample + edge cases |

### Verification Template

```
TRANSFORM: [Description of the transformation]
SOURCE: [Source table.column(s)]
TARGET: [Target table.column]
LOGIC: [Business rule or SQL expression]
TEST CASE 1: Input=[value] -> Expected=[value] -> Actual=[value] -> PASS/FAIL
TEST CASE 2: Input=[value] -> Expected=[value] -> Actual=[value] -> PASS/FAIL
EDGE CASE:  Input=[null/boundary] -> Expected=[value] -> Actual=[value] -> PASS/FAIL
STATUS: PASS / FAIL
NOTES: [Any observations]
```

## Step 6: Regression Testing

Ensure changes to the pipeline do not break existing behavior:

| Regression Check | Method | Pass Criteria |
|-----------------|--------|--------------|
| Row count stability | Compare current run count to prior 5 runs | Within +/- 2 std deviations |
| Schema stability | Compare current schema to previous schema | No unexpected changes |
| Value distribution | Compare histograms of key columns across runs | No significant drift |
| Null rate stability | Compare null percentages to historical baseline | Within +/- 1% |
| Aggregate stability | Compare SUM/AVG of key metrics to prior run | Within +/- 1% (or business threshold) |
| Downstream impact | Verify downstream tables/reports still function | No errors or data anomalies |
| Idempotency | Re-run the pipeline; verify no duplicate records | Zero new duplicates |
| Backfill safety | Run for a historical date range; compare to existing data | Exact match |

## Step 7: Output Format

Present results in this order:

### 1. Validation Summary

| Category | Total Checks | Passed | Failed | Skipped | Pass Rate |
|----------|-------------|--------|--------|---------|-----------|
| Source-to-Target Mapping | -- | -- | -- | -- | --% |
| Row Count Reconciliation | -- | -- | -- | -- | --% |
| Schema & Type Validation | -- | -- | -- | -- | --% |
| Transformation Logic | -- | -- | -- | -- | --% |
| Regression Testing | -- | -- | -- | -- | --% |
| **Total** | **--** | **--** | **--** | **--** | **--%** |

**Overall Verdict**: PASS / FAIL / PASS WITH WARNINGS

### 2. Failed Checks Detail

| Check ID | Category | Description | Expected | Actual | Severity | Affected Records |
|----------|----------|-------------|----------|--------|----------|-----------------|
| ETL-001 | ... | ... | ... | ... | Critical / Major / Minor | ... |

### 3. Reconciliation Summary

| Metric | Source | Target | Delta | Delta % | Status |
|--------|--------|--------|-------|---------|--------|
| Total rows | ... | ... | ... | ... | ... |
| SUM of [amount field] | ... | ... | ... | ... | ... |
| DISTINCT [key field] | ... | ... | ... | ... | ... |

### 4. Recommendations

- Issues requiring immediate fix before production
- Checks to add to automated test suite
- Monitoring and alerting suggestions
- Documentation gaps to address

## Quality Checklist

Before delivering results, verify:

- [ ] All source-to-target mappings have been verified
- [ ] Row counts reconcile at every stage of the pipeline
- [ ] Schema and data types match the specification
- [ ] Every transformation rule has at least one test case
- [ ] Edge cases (nulls, empty strings, boundaries) have been tested
- [ ] Regression checks confirm no unintended changes
- [ ] Failed checks have severity levels and affected record counts
- [ ] Recommendations are specific and actionable
- [ ] Idempotency has been verified for rerunnable pipelines

## Edge Cases

- **CDC (Change Data Capture) pipelines**: Validate insert/update/delete operations separately; verify soft deletes and tombstone handling
- **Late-arriving data**: Test that reprocessing or backfill correctly updates target without duplicates
- **Schema evolution**: Validate that added/removed/renamed source columns are handled gracefully
- **Multi-source merges**: Test conflict resolution logic when sources disagree on the same entity
- **Partitioned tables**: Verify partition pruning works and data lands in the correct partition
- **Timezone-sensitive data**: Test with data spanning DST transitions and multiple timezones
- **Large volume loads**: Validate performance does not degrade and no timeouts occur at scale
- **Null propagation**: Trace how NULL values flow through joins, aggregations, and calculations
