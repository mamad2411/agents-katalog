---
name: arrow
description: R arrow package for Apache Arrow. Use for reading/writing Parquet, Feather, and working with large datasets.
---

# arrow

Apache Arrow interface.

## Read/Write Parquet

```r
library(arrow)

# Read
df <- read_parquet("file.parquet")
df <- read_parquet("file.parquet", col_select = c("a", "b"))

# Write
write_parquet(df, "output.parquet")
write_parquet(df, "output.parquet", compression = "snappy")
write_parquet(df, "output.parquet", compression = "gzip")
```

## Read/Write Feather

```r
# Read
df <- read_feather("file.feather")

# Write
write_feather(df, "output.feather")
write_feather(df, "output.feather", compression = "lz4")
```

## Datasets (Multiple Files)

```r
# Open dataset
ds <- open_dataset("data/")
ds <- open_dataset("data/", format = "parquet")
ds <- open_dataset("data/", format = "csv")

# Query with dplyr
result <- ds %>%
  filter(year == 2024) %>%
  select(a, b, c) %>%
  collect()

# Partitioned data
ds <- open_dataset("data/", partitioning = c("year", "month"))

# Write partitioned
write_dataset(
  df,
  "output/",
  format = "parquet",
  partitioning = c("year", "month")
)
```

## Arrow Tables

```r
# Create Arrow table
tbl <- arrow_table(df)
tbl <- as_arrow_table(df)

# Convert back
df <- as.data.frame(tbl)

# Schema
schema(tbl)
tbl$schema

# Select columns
tbl$a
tbl[c("a", "b")]
```

## Data Types

```r
# Schema specification
schema(
  id = int32(),
  name = utf8(),
  value = float64(),
  date = date32(),
  timestamp = timestamp("us", timezone = "UTC"),
  flag = boolean()
)

# Cast types
tbl$cast(schema(...))
```

## Streaming

```r
# Read in batches
reader <- ParquetFileReader$create("file.parquet")
batch <- reader$ReadRowGroup(0)

# Write in batches
writer <- ParquetFileWriter$create(
  "output.parquet",
  schema = schema(...)
)
writer$WriteTable(tbl)
writer$Close()
```

## CSV with Arrow

```r
# Fast CSV reading
df <- read_csv_arrow("file.csv")
df <- read_csv_arrow("file.csv", col_types = schema(
  id = int32(),
  name = utf8()
))

# Write CSV
write_csv_arrow(df, "output.csv")
```

## Memory Mapping

```r
# Memory-mapped file
tbl <- read_parquet("file.parquet", as_data_frame = FALSE)

# Query without loading all data
result <- tbl %>%
  filter(x > 100) %>%
  collect()
```

## Compression

```r
# Parquet compression options
write_parquet(df, "output.parquet", compression = "snappy")  # Default
write_parquet(df, "output.parquet", compression = "gzip")
write_parquet(df, "output.parquet", compression = "zstd")
write_parquet(df, "output.parquet", compression = "lz4")
write_parquet(df, "output.parquet", compression = "uncompressed")
```
