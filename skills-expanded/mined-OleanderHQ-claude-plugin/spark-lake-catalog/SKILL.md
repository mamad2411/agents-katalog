---
name: spark-lake-catalog
description: >-
  Spark patterns for reading and writing oleander lake catalog tables:
  spark.table(), append vs overwrite, and avoiding driver-side writes. Use
  when building Spark jobs that read or write Iceberg tables in the oleander
  catalog.
---

# oleander Spark Lake Catalog

Use this skill when reading from or writing to the oleander lake catalog in a Spark job.

For shared catalog conventions such as table naming, namespaces, and avoiding raw storage paths, also use `lake-catalog`.

## Reading tables

Use `spark.table()` with the fully qualified table name:

```python
df = spark.table("oleander.default.sf_311")
```

Do not construct raw storage paths for Iceberg tables. Use catalog-qualified names so Spark reads the table through the Iceberg catalog.

## Writing tables

**Append** (add rows to an existing or new table):

```python
df.writeTo("oleander.my_namespace.my_table").append()
```

**Overwrite** (replace table contents):

```python
df.write.mode("overwrite").saveAsTable("oleander.my_namespace.my_table")
```

Use `writeTo(...).append()` for incremental pipelines. Use `write.mode("overwrite").saveAsTable(...)` when replacing the full result set each run.

## Prefer Spark writes over driver writes

Avoid collecting data to the driver and then writing from Python memory. Keep writes as Spark DataFrame operations so Iceberg handles the transaction, partitioning, and metadata correctly.

Bad:

```python
rows = df.collect()
# write rows from Python memory
```

Good:

```python
df.write.mode("overwrite").saveAsTable("oleander.my_namespace.my_table")
```

## Parameterize table names

Accept table names as arguments or environment variables so scripts are reusable:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input-table", default="oleander.default.sf_311")
parser.add_argument("--output-catalog", default="oleander.my_namespace")
args = parser.parse_args()

df = spark.table(args.input_table)
df.write.mode("overwrite").saveAsTable(f"{args.output_catalog}.results")
```

## Cache reused tables, then unpersist

If a table is read and used in multiple downstream transforms, cache it once and unpersist when done:

```python
df = spark.table("oleander.default.sf_311")
df.cache()
# ... multiple transforms ...
df.unpersist()
```

Do not cache tables that are only used once.
