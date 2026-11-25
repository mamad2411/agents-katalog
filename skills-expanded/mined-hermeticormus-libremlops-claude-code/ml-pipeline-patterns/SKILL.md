---
name: "ml-pipeline-patterns"
description: "ML data pipeline patterns with code: Apache Beam DoFns, branching and fan-out, streaming features in Flink, dbt incremental feature models, Great Expectations validation, and backfill strategy. Use when building batch or streaming pipelines that feed models."
---

# ML Pipeline Patterns

Expert patterns for building batch and streaming ML data pipelines with Apache Beam, Spark, dbt, and orchestrators.

## Pattern 1: Apache Beam DoFn Pattern

The `DoFn` is Beam's per-element processing unit. Structure it to handle setup, processing, and teardown correctly.

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class NormalizeFeaturesFn(beam.DoFn):
    """Normalize numerical features using precomputed statistics."""

    def setup(self):
        # Called once per worker. Load shared resources here.
        import json
        with open('feature_stats.json') as f:
            self.stats = json.load(f)

    def process(self, element: dict):
        """Yield normalized record. Yield nothing to filter."""
        try:
            for feature, stat in self.stats.items():
                if feature in element and element[feature] is not None:
                    mean, std = stat['mean'], stat['std']
                    if std > 0:
                        element[f"{feature}_normalized"] = (element[feature] - mean) / std
            yield element
        except Exception as e:
            # Route to dead-letter queue via tagged output
            yield beam.pvalue.TaggedOutput('errors', {
                'record': element,
                'error': str(e)
            })

def build_pipeline(input_path: str, output_path: str):
    options = PipelineOptions(
        runner='DataflowRunner',
        project='my-gcp-project',
        region='us-central1',
        temp_location='gs://my-bucket/temp',
        job_name='normalize-features'
    )

    with beam.Pipeline(options=options) as p:
        results = (
            p
            | 'ReadParquet' >> beam.io.ReadFromParquet(input_path)
            | 'Normalize' >> beam.ParDo(NormalizeFeaturesFn()).with_outputs('errors', main='main')
        )

        # Write main output
        results.main | 'WriteFeatures' >> beam.io.WriteToParquet(output_path)

        # Write dead-letter for investigation
        results.errors | 'WriteErrors' >> beam.io.WriteToText(
            output_path.replace('features', 'errors')
        )
```

## Pattern 2: Pipeline Branching and Fanout

Process a single input PCollection into multiple output streams.

```python
import apache_beam as beam

def run_branching_pipeline(input_path: str, output_prefix: str):
    with beam.Pipeline() as p:
        raw = p | 'Read' >> beam.io.ReadFromParquet(input_path)

        # Branch 1: High-value users → real-time feature store
        (raw
         | 'FilterHighValue' >> beam.Filter(lambda x: x.get('ltv', 0) > 1000)
         | 'ExtractRTFeatures' >> beam.Map(extract_realtime_features)
         | 'WriteRedis' >> beam.ParDo(WriteToRedisFn()))

        # Branch 2: All users → batch feature store
        (raw
         | 'ExtractBatchFeatures' >> beam.Map(extract_batch_features)
         | 'WriteParquet' >> beam.io.WriteToParquet(f"{output_prefix}/batch"))

        # Branch 3: New users → cold start pipeline
        (raw
         | 'FilterNew' >> beam.Filter(lambda x: x.get('days_since_signup', 999) < 7)
         | 'ExtractColdStartFeatures' >> beam.Map(extract_cold_start_features)
         | 'WriteColdStart' >> beam.io.WriteToParquet(f"{output_prefix}/cold_start"))
```

## Pattern 3: Streaming Feature Computation (Flink)

Compute rolling window features in real time.

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.common import Time, WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema

def build_streaming_pipeline():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(4)
    env.enable_checkpointing(60_000)  # checkpoint every 60 seconds

    kafka_props = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'feature-pipeline'
    }

    source = FlinkKafkaConsumer(
        topics='user-events',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    (env
     .add_source(source)
     .map(parse_event)
     .assign_timestamps_and_watermarks(
         WatermarkStrategy.for_bounded_out_of_orderness(Time.seconds(10))
         .with_timestamp_assigner(EventTimestampAssigner())
     )
     .key_by(lambda e: e['user_id'])
     .window(TumblingEventTimeWindows.of(Time.minutes(5)))
     .aggregate(UserActivityAggregator())
     .add_sink(FlinkKafkaProducer(
         topic='user-features',
         serialization_schema=SimpleStringSchema(),
         producer_config={'bootstrap.servers': 'kafka:9092'}
     ))
    )

    env.execute("streaming-user-features")
```

## Pattern 4: dbt Incremental Feature Model

Efficient feature computation for large datasets using incremental materialization.

```sql
-- models/features/user_purchase_features.sql
{{
  config(
    materialized='incremental',
    unique_key='user_id',
    on_schema_change='sync_all_columns',
    partition_by={
      'field': 'feature_date',
      'data_type': 'date'
    }
  )
}}

WITH purchase_stats AS (
    SELECT
        user_id,
        DATE(event_ts) as feature_date,
        COUNT(*) as purchase_count_30d,
        SUM(amount) as total_spend_30d,
        AVG(amount) as avg_order_value_30d,
        MAX(amount) as max_order_value_30d,
        COUNT(DISTINCT product_category) as category_diversity_30d,
        DATE_DIFF(CURRENT_DATE, MAX(DATE(event_ts)), DAY) as days_since_last_purchase
    FROM {{ ref('stg_purchases') }}
    WHERE event_ts >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    {% if is_incremental() %}
        AND event_ts > (SELECT MAX(feature_date) FROM {{ this }})
    {% endif %}
    GROUP BY 1, 2
)

SELECT * FROM purchase_stats
```

```yaml
# models/features/schema.yml
models:
  - name: user_purchase_features
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns: [user_id, feature_date]
    columns:
      - name: user_id
        tests: [not_null]
      - name: purchase_count_30d
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

## Pattern 5: Great Expectations Pipeline Validation

Integrate data quality checks into pipeline execution.

```python
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest

def validate_feature_batch(df, expectation_suite_name: str = "features.warning") -> bool:
    context = gx.get_context()

    validator = context.get_validator(
        batch_request=RuntimeBatchRequest(
            datasource_name="pandas_datasource",
            data_connector_name="runtime_data_connector",
            data_asset_name="feature_batch",
            runtime_parameters={"batch_data": df},
            batch_identifiers={"batch_id": "pipeline_run"},
        ),
        expectation_suite_name=expectation_suite_name,
    )

    results = validator.validate()

    if not results.success:
        failed = [r for r in results.results if not r.success]
        for r in failed:
            print(f"FAILED: {r.expectation_config.expectation_type} "
                  f"on column {r.expectation_config.kwargs.get('column', 'N/A')}")
        return False
    return True

# Define suite programmatically
def create_feature_suite(validator):
    validator.expect_column_values_to_not_be_null("user_id")
    validator.expect_column_values_to_be_between("purchase_count_30d", min_value=0)
    validator.expect_column_values_to_be_between("avg_order_value_30d", min_value=0)
    validator.expect_table_row_count_to_be_between(min_value=1000)
    validator.expect_column_proportion_of_unique_values_to_be_between(
        "user_id", min_value=0.99  # near-unique
    )
    validator.save_expectation_suite()
```

## Pattern 6: Backfill Strategy

Backfilling historical features without reprocessing everything.

```python
from prefect import flow, task
from datetime import date, timedelta
from typing import Generator

@task(retries=3, retry_delay_seconds=60)
def compute_features_for_date(feature_date: date) -> dict:
    """Idempotent: safe to rerun for same date."""
    # Check if already computed
    output_path = f"s3://features/date={feature_date}/part-0.parquet"
    if s3_exists(output_path):
        return {"date": feature_date, "status": "skipped"}

    # Compute features for this date
    df = load_raw_data(feature_date)
    features = transform_features(df, reference_date=feature_date)
    write_parquet(features, output_path)
    return {"date": feature_date, "status": "computed", "rows": len(features)}

@flow(name="feature-backfill")
def backfill_features(start_date: date, end_date: date, parallelism: int = 4):
    dates = [start_date + timedelta(days=i)
             for i in range((end_date - start_date).days + 1)]

    # Process in parallel chunks
    results = compute_features_for_date.map(dates)
    return results

# Run backfill
backfill_features(
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31),
    parallelism=8
)
```

## Anti-Patterns

### Anti-Pattern 1: No Dead-Letter Queue
Pipelines without error routing drop records silently. Always route failed records to an error path and monitor error rate.

### Anti-Pattern 2: Point-in-Time Leakage
Feature pipelines that use future data relative to the label timestamp. This is training-serving skew at its worst — model appears to work great in training, fails in production. Always filter features by `event_ts < label_ts`.

### Anti-Pattern 3: Non-Idempotent Pipeline Steps
If a step can't be safely re-run without side effects, backfill becomes dangerous. Design every step to be idempotent: check existence before writing, use UPSERT semantics.

### Anti-Pattern 4: Triggering Batch Jobs Without Data Checks
Airflow/Prefect tasks that run regardless of upstream data availability. Add data sensors (`ExternalTaskSensor`, `S3KeySensor`) before computation tasks.

### Anti-Pattern 5: String-Typed Everything in Parquet
Writing all features as strings loses compression and query performance. Use proper dtypes: `int32`, `float32`, `date32`, `categorical`. A float32 Parquet is ~4x smaller than the same data in JSON.
