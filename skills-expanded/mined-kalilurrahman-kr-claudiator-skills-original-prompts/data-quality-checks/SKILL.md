---
name: data-quality-checks
description: Design data quality validation with Great Expectations, custom checks, and automated monitoring. Outputs validation rules, anomaly detection, and data lineage.
argument-hint: [data sources, quality requirements, validation frequency]
allowed-tools: Read, Write, Bash
---

# Data Quality Checks

Design automated data quality validation for pipelines. Not manual inspection — automated checks with Great Expectations, custom validators, and anomaly detection.

## Process

1. **Define quality dimensions.** Completeness, accuracy, consistency, timeliness, validity.
2. **Identify critical data.** Revenue data, user PII, regulatory fields.
3. **Create expectations.** Schema validation, range checks, uniqueness constraints.
4. **Automate validation.** Run checks on every pipeline execution.
5. **Handle failures.** Alert, quarantine bad data, or fail pipeline.
6. **Track quality metrics.** Pass/fail rates, data freshness, anomaly trends.
7. **Document lineage.** Track data flow from source to destination.

## Output Format

### Data Quality: [Dataset Name]

**Framework:** Great Expectations  
**Expectations:** 45 checks (schema, ranges, uniqueness)  
**Validation:** On every ETL run  
**Failure Policy:** Quarantine + alert on critical failures  
**SLA:** Data freshness < 1 hour

---

## Quality Dimensions

| Dimension | Definition | Example Check |
|-----------|-----------|---------------|
| **Completeness** | No missing required data | Non-null for critical columns |
| **Accuracy** | Data reflects reality | Email format valid, dates in past |
| **Consistency** | Same meaning across systems | User ID format consistent |
| **Timeliness** | Data available when needed | Orders loaded within 1 hour |
| **Validity** | Values in acceptable ranges | Age between 0-120, prices > 0 |
| **Uniqueness** | No duplicates where expected | Primary keys unique |

---

## Great Expectations

### Setup
```python
import great_expectations as gx

# Create data context
context = gx.get_context()

# Connect to data source
datasource = context.sources.add_pandas("my_datasource")

# Add data asset (CSV, Parquet, Database table)
data_asset = datasource.add_csv_asset(
    name="orders",
    filepath_or_buffer="data/orders.csv"
)

# Create batch request
batch_request = data_asset.build_batch_request()
```

### Create Expectation Suite
```python
# Create suite
suite = context.add_expectation_suite(
    expectation_suite_name="orders_suite"
)

# Add expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="orders_suite"
)

# Schema validation
validator.expect_table_columns_to_match_ordered_list(
    column_list=["order_id", "user_id", "product_id", "amount", "created_at"]
)

# Column type validation
validator.expect_column_values_to_be_of_type("order_id", "int64")
validator.expect_column_values_to_be_of_type("amount", "float64")

# Not null
validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_not_be_null("user_id")

# Unique
validator.expect_column_values_to_be_unique("order_id")

# Range checks
validator.expect_column_values_to_be_between(
    "amount",
    min_value=0,
    max_value=100000
)

# Date in past
validator.expect_column_values_to_be_dateutil_parseable("created_at")
validator.expect_column_values_to_be_between(
    "created_at",
    min_value="2020-01-01",
    max_value="now"
)

# Save suite
validator.save_expectation_suite(discard_failed_expectations=False)
```

### Run Validation
```python
# Validate new batch
checkpoint = context.add_checkpoint(
    name="orders_checkpoint",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": "orders_suite"
        }
    ]
)

# Run checkpoint
result = checkpoint.run()

# Check results
if result["success"]:
    print("✅ All checks passed")
else:
    print("❌ Validation failed")
    for validation in result["run_results"].values():
        for check in validation["validation_result"]["results"]:
            if not check["success"]:
                print(f"Failed: {check['expectation_config']['expectation_type']}")
```

---

## Custom Validators

### Business Logic Validation
```python
def validate_order_total(df):
    """Custom check: order total = sum of line items"""
    violations = []
    
    for order_id in df['order_id'].unique():
        order_rows = df[df['order_id'] == order_id]
        
        expected_total = order_rows['line_item_amount'].sum()
        actual_total = order_rows['order_total'].iloc[0]
        
        if abs(expected_total - actual_total) > 0.01:
            violations.append({
                'order_id': order_id,
                'expected': expected_total,
                'actual': actual_total
            })
    
    return {
        'passed': len(violations) == 0,
        'violations': violations
    }

# Run check
result = validate_order_total(df)
if not result['passed']:
    alert(f"{len(result['violations'])} orders have incorrect totals")
```

### Referential Integrity
```python
def check_referential_integrity(orders_df, users_df):
    """All user_ids in orders must exist in users table"""
    
    orphaned_orders = orders_df[~orders_df['user_id'].isin(users_df['user_id'])]
    
    if len(orphaned_orders) > 0:
        return {
            'passed': False,
            'error': f"{len(orphaned_orders)} orders reference non-existent users",
            'sample': orphaned_orders.head(10).to_dict()
        }
    
    return {'passed': True}
```

---

## Anomaly Detection

### Statistical Anomalies
```python
import numpy as np
from scipy import stats

def detect_anomalies_zscore(df, column, threshold=3):
    """Detect outliers using Z-score"""
    
    mean = df[column].mean()
    std = df[column].std()
    
    z_scores = np.abs((df[column] - mean) / std)
    anomalies = df[z_scores > threshold]
    
    return {
        'count': len(anomalies),
        'percentage': len(anomalies) / len(df) * 100,
        'samples': anomalies.head(10)
    }

# Usage
anomalies = detect_anomalies_zscore(df, 'amount', threshold=3)

if anomalies['percentage'] > 5:
    alert(f"High anomaly rate: {anomalies['percentage']:.1f}%")
```

### Time Series Anomalies
```python
def detect_volume_anomaly(df, date_column, threshold_pct=50):
    """Detect unusual daily volumes"""
    
    daily_counts = df.groupby(df[date_column].dt.date).size()
    
    # Calculate baseline (30-day moving average)
    baseline = daily_counts.rolling(window=30).mean()
    
    # Today's volume
    today = daily_counts.iloc[-1]
    expected = baseline.iloc[-1]
    
    pct_change = abs((today - expected) / expected) * 100
    
    if pct_change > threshold_pct:
        return {
            'anomaly_detected': True,
            'today_volume': today,
            'expected_volume': expected,
            'change_pct': pct_change
        }
    
    return {'anomaly_detected': False}

# Alert if today's volume is 50% different from baseline
result = detect_volume_anomaly(df, 'created_at')
if result['anomaly_detected']:
    alert(f"Volume anomaly: {result['today_volume']} vs {result['expected_volume']} expected")
```

---

## Schema Validation

### Strict Schema
```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType

expected_schema = StructType([
    StructField("order_id", IntegerType(), nullable=False),
    StructField("user_id", IntegerType(), nullable=False),
    StructField("amount", FloatType(), nullable=False),
    StructField("status", StringType(), nullable=False),
    StructField("created_at", TimestampType(), nullable=False)
])

def validate_schema(df, expected_schema):
    """Validate DataFrame schema matches expected"""
    
    if df.schema != expected_schema:
        # Find differences
        expected_cols = {f.name: f.dataType for f in expected_schema.fields}
        actual_cols = {f.name: f.dataType for f in df.schema.fields}
        
        missing = set(expected_cols.keys()) - set(actual_cols.keys())
        extra = set(actual_cols.keys()) - set(expected_cols.keys())
        type_mismatch = []
        
        for col in set(expected_cols.keys()) & set(actual_cols.keys()):
            if expected_cols[col] != actual_cols[col]:
                type_mismatch.append({
                    'column': col,
                    'expected': expected_cols[col],
                    'actual': actual_cols[col]
                })
        
        raise SchemaValidationError({
            'missing_columns': list(missing),
            'extra_columns': list(extra),
            'type_mismatches': type_mismatch
        })
    
    return True
```

---

## Data Freshness Checks

```python
from datetime import datetime, timedelta

def check_data_freshness(df, timestamp_column, max_age_hours=1):
    """Ensure data is recent enough"""
    
    latest_timestamp = df[timestamp_column].max()
    age = datetime.now() - latest_timestamp
    
    if age > timedelta(hours=max_age_hours):
        return {
            'fresh': False,
            'latest_timestamp': latest_timestamp,
            'age_hours': age.total_seconds() / 3600,
            'max_age_hours': max_age_hours
        }
    
    return {'fresh': True}

# SLA: Orders data must be < 1 hour old
freshness = check_data_freshness(orders_df, 'created_at', max_age_hours=1)

if not freshness['fresh']:
    alert(f"Stale data: {freshness['age_hours']:.1f} hours old")
```

---

## Automated Quality Pipeline

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def validate_data_quality(**context):
    """Run all quality checks"""
    
    # Load data
    df = pd.read_parquet('s3://bucket/orders/latest.parquet')
    
    checks = []
    
    # 1. Schema validation
    try:
        validate_schema(df, expected_schema)
        checks.append({'check': 'schema', 'passed': True})
    except Exception as e:
        checks.append({'check': 'schema', 'passed': False, 'error': str(e)})
    
    # 2. Completeness
    null_counts = df.isnull().sum()
    critical_nulls = null_counts[['order_id', 'user_id', 'amount']]
    if critical_nulls.sum() > 0:
        checks.append({'check': 'completeness', 'passed': False})
    else:
        checks.append({'check': 'completeness', 'passed': True})
    
    # 3. Uniqueness
    duplicates = df.duplicated(subset=['order_id']).sum()
    checks.append({
        'check': 'uniqueness',
        'passed': duplicates == 0,
        'duplicates': duplicates
    })
    
    # 4. Value ranges
    invalid_amounts = (df['amount'] < 0).sum() + (df['amount'] > 100000).sum()
    checks.append({
        'check': 'value_ranges',
        'passed': invalid_amounts == 0,
        'violations': invalid_amounts
    })
    
    # 5. Freshness
    freshness = check_data_freshness(df, 'created_at')
    checks.append({'check': 'freshness', 'passed': freshness['fresh']})
    
    # 6. Anomaly detection
    anomalies = detect_anomalies_zscore(df, 'amount')
    checks.append({
        'check': 'anomalies',
        'passed': anomalies['percentage'] < 5,
        'anomaly_rate': anomalies['percentage']
    })
    
    # Summarize
    total_checks = len(checks)
    passed_checks = sum(1 for c in checks if c['passed'])
    
    print(f"Quality Score: {passed_checks}/{total_checks} ({passed_checks/total_checks*100:.0f}%)")
    
    # Store results
    save_quality_results(checks)
    
    # Fail task if critical checks fail
    critical_failed = [c for c in checks if not c['passed'] and c['check'] in ['schema', 'completeness', 'uniqueness']]
    if critical_failed:
        raise ValueError(f"Critical quality checks failed: {critical_failed}")

# Airflow DAG
with DAG('data_quality_validation', start_date=datetime(2024, 1, 1), schedule_interval='@hourly') as dag:
    
    validate = PythonOperator(
        task_id='validate_quality',
        python_callable=validate_data_quality
    )
```

---

## Quality Metrics Dashboard

```python
from prometheus_client import Counter, Gauge, Histogram

# Metrics
data_quality_score = Gauge(
    'data_quality_score',
    'Percentage of checks passed',
    ['dataset']
)

data_quality_checks_total = Counter(
    'data_quality_checks_total',
    'Total quality checks run',
    ['dataset', 'check_type', 'result']
)

data_freshness_hours = Gauge(
    'data_freshness_hours',
    'Data age in hours',
    ['dataset']
)

def record_quality_metrics(dataset_name, checks):
    """Record quality metrics in Prometheus"""
    
    passed = sum(1 for c in checks if c['passed'])
    total = len(checks)
    score = (passed / total) * 100
    
    data_quality_score.labels(dataset=dataset_name).set(score)
    
    for check in checks:
        data_quality_checks_total.labels(
            dataset=dataset_name,
            check_type=check['check'],
            result='pass' if check['passed'] else 'fail'
        ).inc()
```

---

## Data Lineage Tracking

```python
class DataLineageTracker:
    """Track data transformations"""
    
    def __init__(self):
        self.lineage = []
    
    def track_transformation(self, source, target, transformation, record_count):
        """Record a data transformation"""
        self.lineage.append({
            'timestamp': datetime.utcnow(),
            'source': source,
            'target': target,
            'transformation': transformation,
            'record_count': record_count
        })
    
    def visualize(self):
        """Generate lineage graph"""
        # Source → Transform → Target
        for entry in self.lineage:
            print(f"{entry['source']} --[{entry['transformation']}]--> {entry['target']}")

# Usage
tracker = DataLineageTracker()

# ETL pipeline
raw_df = load_raw_data()
tracker.track_transformation('raw_orders.csv', 'cleaned_orders', 'clean_nulls', len(raw_df))

cleaned_df = clean_data(raw_df)
tracker.track_transformation('cleaned_orders', 'enriched_orders', 'join_users', len(cleaned_df))

enriched_df = enrich_data(cleaned_df)
tracker.track_transformation('enriched_orders', 'orders_warehouse', 'load', len(enriched_df))

# Visualize lineage
tracker.visualize()
# raw_orders.csv --[clean_nulls]--> cleaned_orders
# cleaned_orders --[join_users]--> enriched_orders
# enriched_orders --[load]--> orders_warehouse
```

---

## Quarantine Bad Data

```python
def quarantine_invalid_records(df, validation_results):
    """Separate good and bad records"""
    
    # Identify bad records
    bad_mask = pd.Series([False] * len(df))
    
    for check in validation_results:
        if not check['passed'] and 'invalid_indices' in check:
            bad_mask[check['invalid_indices']] = True
    
    # Split data
    good_df = df[~bad_mask]
    bad_df = df[bad_mask]
    
    # Write good data to prod
    good_df.to_parquet('s3://bucket/orders/prod/latest.parquet')
    
    # Write bad data to quarantine
    if len(bad_df) > 0:
        bad_df.to_parquet(f"s3://bucket/orders/quarantine/{datetime.now().isoformat()}.parquet")
        
        alert(f"Quarantined {len(bad_df)} invalid records")
    
    return good_df, bad_df
```

---

## Testing Quality Checks

```python
import pytest

def test_schema_validation():
    # Create test DataFrame with wrong schema
    df = pd.DataFrame({
        'order_id': [1, 2],
        'amount': ['100', '200']  # String instead of float
    })
    
    with pytest.raises(SchemaValidationError):
        validate_schema(df, expected_schema)

def test_freshness_check():
    # Old data
    df = pd.DataFrame({
        'created_at': [datetime.now() - timedelta(hours=5)]
    })
    
    result = check_data_freshness(df, 'created_at', max_age_hours=1)
    assert not result['fresh']
    
    # Fresh data
    df = pd.DataFrame({
        'created_at': [datetime.now() - timedelta(minutes=30)]
    })
    
    result = check_data_freshness(df, 'created_at', max_age_hours=1)
    assert result['fresh']
```

## Rules

- Critical columns (IDs, amounts, timestamps) require not-null checks — data pipeline fails on nulls.
- Schema validation on every run — prevents breaking changes from upstream.
- Range checks on numeric fields — negative amounts, impossible dates caught early.
- Uniqueness on primary keys — duplicates indicate upstream bugs or race conditions.
- Freshness checks with SLA — stale data alerts before users notice.
- Quarantine invalid data, don't drop — allows debugging and potential recovery.
- Anomaly detection with baselines — 50%+ volume change triggers investigation.
- Quality metrics tracked over time — trends reveal degrading data sources.
- Business logic validation (e.g., order total = sum of items) — technical validity ≠ business correctness.
- Automated validation in CI/CD — quality gates prevent bad data reaching production.
