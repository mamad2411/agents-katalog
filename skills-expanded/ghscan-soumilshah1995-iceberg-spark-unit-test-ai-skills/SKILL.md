---
name: spark-iceberg-unit-test
description: Generate automated unit tests for Spark Iceberg pipelines. Use when the user has a Spark/Iceberg pipeline and wants test scripts, pytest fixtures, or CI-ready tests. Produces requirements-test.txt, run_tests_in_docker.sh, tests/conftest.py, and tests/test_*.py with DDL, merge (insert/update/dedup), and before/after count checks. Trigger on "generate tests for pipeline", "unit test spark iceberg", "test generation", or when the user points to prompt.md or this skill.
---

# Spark Iceberg unit test generation

Generate **only** these four artifacts (no extra folders):

| # | File | Purpose |
|---|------|--------|
| 1 | `requirements-test.txt` | Test deps: pyspark (pinned), pytest, pyarrow |
| 2 | `run_tests_in_docker.sh` | Docker script: Bookworm + Java 17, pytest |
| 3 | `tests/conftest.py` | Spark session fixture, EXPECTED_SCHEMA, path to pipeline |
| 4 | `tests/test_<pipeline_or_table>.py` | TestDDL, TestMergeInsert/Update/Dedup, schema sanity |

---

## 1. Infer from the pipeline

Before generating, extract from the pipeline code:

- **Table name(s)** — fully qualified (catalog.namespace.table) or parts.
- **Schema** — column names and types from `CREATE TABLE` / DDL (map to `StructType` + `StructField`: StringType, IntegerType, LongType, DoubleType, FloatType, TimestampType, DateType, BooleanType).
- **DDL entrypoint** — e.g. `create_table_if_not_exists(spark)`.
- **Merge entrypoint** — SQL template or function (e.g. `merge_into_table(spark, df)` or MERGE SQL with staging view).
- **Merge key** — column(s) in `ON` (e.g. `id`).
- **Dedup/ordering** — e.g. `ROW_NUMBER() ... ORDER BY event_time DESC`.

---

## 2. File stubs (generate these four files)

Replace placeholders from the pipeline: `<TABLE_NAME>`, `<PIPELINE_DIR>`, `<COLUMNS>`, merge SQL if different.

### 2.1 `requirements-test.txt`

```text
# Pin PySpark to match Iceberg runtime (3.4). Spark 3.5+ causes SQLContext.conf() / DirectByteBuffer issues with Iceberg 1.3.x and Java 21.
pyspark>=3.4.0,<3.5.0
pytest>=7.0.0
pyarrow
```

---

### 2.2 `run_tests_in_docker.sh`

```bash
#!/usr/bin/env bash
# Run CI-style test job in a local container.
# Usage: ./run_tests_in_docker.sh   (from this directory)
# Requires: Docker.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
IMAGE="python:3.11-bookworm"

echo "Running tests in Docker (image: $IMAGE)..."
echo "Project dir: $SCRIPT_DIR"
echo ""

docker run --rm \
  -v "$SCRIPT_DIR:/app" \
  -w /app \
  "$IMAGE" \
  bash -c '
    set -e
    echo "==> Installing Java 17 (Spark/Iceberg need Java 17; Java 21 causes DirectByteBuffer errors)..."
    apt-get update -qq && apt-get install -y -qq openjdk-17-jre-headless
    export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
    echo "    JAVA_HOME=$JAVA_HOME"
    java -version
    echo "==> Installing Python deps..."
    pip install -q -r requirements-test.txt
    export PYSPARK_DRIVER_PYTHON=python3
    export PYSPARK_PYTHON=python3
    echo "==> Running pytest..."
    pytest tests/ -v
  '

echo ""
echo "Done. Exit code: $?"
```

**Notes:** Use `python:3.11-bookworm` (not slim) so `openjdk-17-jre-headless` is available. Java 17 required.

---

### 2.3 `tests/conftest.py`

```python
"""Shared pytest fixtures: local Spark + Iceberg. Run from project root: pytest tests/ -v"""

import os
import sys
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType  # add as needed

# Pipeline import path — so "import pipeline" works (parent of tests/ or <PIPELINE_DIR>)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

TEST_CATALOG = "local"
TEST_NAMESPACE = "default"
TEST_TABLE = "<TABLE_NAME>"
WAREHOUSE_DIR = "/tmp/iceberg_test_warehouse"
FULL_TABLE = f"`{TEST_CATALOG}`.`{TEST_NAMESPACE}`.`{TEST_TABLE}`"

EXPECTED_SCHEMA = StructType([
    StructField("tenant", StringType(), True),
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("event_time", TimestampType(), True),
    # ... one StructField per DDL column, same order and types
])

@pytest.fixture(scope="session")
def spark():
    os.makedirs(WAREHOUSE_DIR, exist_ok=True)
    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("pipeline-tests")
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.3.0")
        .config(f"spark.sql.catalog.{TEST_CATALOG}", "org.apache.iceberg.spark.SparkCatalog")
        .config(f"spark.sql.catalog.{TEST_CATALOG}.type", "hadoop")
        .config(f"spark.sql.catalog.{TEST_CATALOG}.warehouse", WAREHOUSE_DIR)
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("ERROR")
    yield session
    session.stop()
```

---

### 2.4 `tests/test_<pipeline_or_table>.py`

Replace `<pipeline_or_table>` with e.g. `pipeline` or table name. Adapt `_make_row`, `SOURCE_SCHEMA`, merge SQL, and DDL call to the pipeline.

```python
"""Unit tests for <pipeline/table>. Run: pytest tests/ -v"""

from datetime import datetime
import pytest
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

from conftest import TEST_CATALOG, TEST_NAMESPACE, TEST_TABLE, EXPECTED_SCHEMA, FULL_TABLE
import pipeline  # or: from pipeline import create_table_if_not_exists, merge_into_table

SOURCE_SCHEMA = StructType([
    StructField("tenant", StringType(), True),
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("event_time", TimestampType(), True),
])

def _drop_table(spark):
    spark.sql(f"DROP TABLE IF EXISTS {FULL_TABLE}")

def _make_row(id_, name, amount, tenant="acme", event_time=None):
    return Row(
        tenant=tenant,
        id=id_,
        name=name,
        amount=float(amount),
        event_time=event_time or datetime(2024, 1, 1),
    )

def _run_merge(spark, rows):
    df = spark.createDataFrame(rows, schema=SOURCE_SCHEMA)
    df.createOrReplaceTempView("staging")
    spark.sql(f"""
        MERGE INTO {FULL_TABLE} AS target
        USING (
            SELECT * FROM (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY event_time DESC) AS rn
                FROM staging
            ) WHERE rn = 1
        ) AS source
        ON target.id = source.id
        WHEN MATCHED     THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)
    spark.catalog.dropTempView("staging")

@pytest.fixture(autouse=True)
def fresh_table(spark):
    _drop_table(spark)
    pipeline.create_table_if_not_exists(spark)
    yield
    _drop_table(spark)


class TestDDL:
    def test_column_order(self, spark):
        actual = [f.name for f in spark.table(FULL_TABLE).schema.fields]
        expected = [f.name for f in EXPECTED_SCHEMA.fields]
        assert actual == expected, f"Order: got {actual}, expected {expected}"

    def test_column_dtypes(self, spark):
        for i, exp in enumerate(EXPECTED_SCHEMA.fields):
            actual = spark.table(FULL_TABLE).schema.fields[i]
            assert actual.dataType == exp.dataType, f"Col {exp.name}: expected {exp.dataType}, got {actual.dataType}"

    def test_table_empty_after_create(self, spark):
        assert spark.table(FULL_TABLE).count() == 0

    def test_create_idempotent(self, spark):
        pipeline.create_table_if_not_exists(spark)
        assert spark.table(FULL_TABLE).count() == 0


class TestMergeInsert:
    def test_insert_row_count(self, spark):
        rows = [_make_row(1, "A", 10.0), _make_row(2, "B", 20.0)]
        before = len(rows)
        _run_merge(spark, rows)
        after = spark.table(FULL_TABLE).count()
        assert after == before, f"Before merge {before}, after merge {after}"

    def test_insert_value_readback(self, spark):
        rows = [_make_row(42, "Charlie", 999.99)]
        _run_merge(spark, rows)
        row = spark.table(FULL_TABLE).collect()[0]
        assert row.id == 42 and row.name == "Charlie" and row.amount == 999.99

    def test_insert_empty_staging(self, spark):
        before = spark.table(FULL_TABLE).count()
        _run_merge(spark, [])
        after = spark.table(FULL_TABLE).count()
        assert after == before, f"Empty merge should not change count: {before} -> {after}"

    def test_insert_single_row(self, spark):
        rows = [_make_row(1, "Single", 50.0)]
        _run_merge(spark, rows)
        assert spark.table(FULL_TABLE).count() == 1
        row = spark.table(FULL_TABLE).collect()[0]
        assert row.id == 1 and row.name == "Single" and row.amount == 50.0


class TestMergeUpdate:
    def test_update_same_key(self, spark):
        _run_merge(spark, [_make_row(1, "Old", 100.0, event_time=datetime(2024, 1, 1))])
        _run_merge(spark, [_make_row(1, "New", 200.0, event_time=datetime(2024, 6, 1))])
        assert spark.table(FULL_TABLE).count() == 1
        row = spark.table(FULL_TABLE).collect()[0]
        assert row.name == "New" and row.amount == 200.0


class TestMergeDedup:
    def test_dedup_keeps_latest(self, spark):
        rows = [
            _make_row(1, "Old", 50.0, event_time=datetime(2024, 1, 1)),
            _make_row(1, "New", 150.0, event_time=datetime(2024, 9, 1)),
        ]
        _run_merge(spark, rows)
        assert spark.table(FULL_TABLE).count() == 1
        row = spark.table(FULL_TABLE).collect()[0]
        assert row.name == "New" and row.amount == 150.0

    def test_dedup_multiple_keys(self, spark):
        rows = [
            _make_row(1, "A1", 10.0, event_time=datetime(2024, 1, 1)),
            _make_row(1, "A2", 20.0, event_time=datetime(2024, 2, 1)),
            _make_row(2, "B1", 30.0, event_time=datetime(2024, 1, 1)),
            _make_row(2, "B2", 40.0, event_time=datetime(2024, 2, 1)),
        ]
        _run_merge(spark, rows)
        assert spark.table(FULL_TABLE).count() == 2
        rows_result = spark.table(FULL_TABLE).orderBy("id").collect()
        assert rows_result[0].name == "A2" and rows_result[0].amount == 20.0
        assert rows_result[1].name == "B2" and rows_result[1].amount == 40.0


class TestSchemaSanity:
    def test_schema_after_merge(self, spark):
        rows = [_make_row(1, "Test", 100.0)]
        _run_merge(spark, rows)
        actual_schema = spark.table(FULL_TABLE).schema
        assert len(actual_schema.fields) == len(EXPECTED_SCHEMA.fields)
        for i, exp_field in enumerate(EXPECTED_SCHEMA.fields):
            actual_field = actual_schema.fields[i]
            assert actual_field.name == exp_field.name
            assert actual_field.dataType == exp_field.dataType
```

**Notes:** If the pipeline uses a merge function instead of raw SQL, call e.g. `pipeline.merge_into_table(spark, df)` in `_run_merge` and use the pipeline’s staging view name. Match `SOURCE_SCHEMA` and `_make_row` to the table schema. DDL: use `pipeline.create_table_if_not_exists(spark)` (no extra args if the pipeline uses module-level table name).

---

## 3. Implementation notes

- **PySpark pin:** Use `pyspark>=3.4.0,<3.5.0` with `iceberg-spark-runtime-3.4_2.12`; Spark 3.5+ and Java 21 cause NoSuchMethodError.
- **Docker:** Use `python:3.11-bookworm` and `openjdk-17-jre-headless`; set `JAVA_HOME`.
- **Session spark:** One SparkSession in conftest; autouse `fresh_table` per test file.
- **Assert messages:** e.g. `assert a == b, f"Expected {b}, got {a}"`.

---

## 4. Checklist before delivering

- [ ] Exactly four files: `requirements-test.txt`, `run_tests_in_docker.sh`, `tests/conftest.py`, `tests/test_*.py`.
- [ ] `requirements-test.txt`: pyspark pin, pytest, pyarrow.
- [ ] `run_tests_in_docker.sh`: Bookworm, Java 17, `pytest tests/ -v`.
- [ ] `conftest.py`: sys.path to pipeline, EXPECTED_SCHEMA, session `spark` with Iceberg Hadoop catalog.
- [ ] `test_*.py`: TestDDL (order, dtypes, empty, idempotent); merge insert/update/dedup with count checks and value readback; optional empty staging, single row, schema sanity.

---

## 5. How to run (tell the user)

- **Local:** `pip install -r requirements-test.txt` then `pytest tests/ -v`.
- **Docker:** `./run_tests_in_docker.sh`.

No AWS or S3 required.
