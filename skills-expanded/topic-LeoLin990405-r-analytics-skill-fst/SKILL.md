---
name: fst
description: R fst package for fast serialization of data frames. Use for ultra-fast reading/writing of data frames with compression.
---

# fst

Lightning fast serialization of data frames.

## Basic Usage

```r
library(fst)

# Write
write_fst(df, "data.fst")

# Read
df <- read_fst("data.fst")
```

## Compression

```r
# Compression levels (0-100)
write_fst(df, "data.fst", compress = 0)    # No compression, fastest
write_fst(df, "data.fst", compress = 50)   # Default, balanced
write_fst(df, "data.fst", compress = 100)  # Maximum compression

# Check compression ratio
fst.metadata("data.fst")
```

## Selective Reading

```r
# Read specific columns
df <- read_fst("data.fst", columns = c("id", "name", "value"))

# Read row range
df <- read_fst("data.fst", from = 1000, to = 2000)

# Combine both
df <- read_fst("data.fst",
  columns = c("id", "value"),
  from = 1, to = 10000
)
```

## Metadata

```r
# Get file metadata without reading
meta <- fst.metadata("data.fst")

# Number of rows
meta$nrOfRows

# Column names
meta$columnNames

# Column types
meta$columnTypes
```

## Data Types Supported

```r
# Supported types
# - integer, double, logical, character
# - factor (with levels preserved)
# - Date, POSIXct
# - raw (byte vectors)
# - IDate, ITime (data.table)

# Example with various types
df <- data.frame(
  int_col = 1:100,
  dbl_col = runif(100),
  chr_col = letters[1:100 %% 26 + 1],
  fct_col = factor(rep(c("A", "B"), 50)),
  date_col = Sys.Date() + 1:100,
  lgl_col = sample(c(TRUE, FALSE), 100, replace = TRUE)
)

write_fst(df, "typed_data.fst")
```

## Performance Tips

```r
# For maximum speed, use compress = 0
write_fst(df, "fast.fst", compress = 0)

# For minimum file size, use compress = 100
write_fst(df, "small.fst", compress = 100)

# Read only needed columns for large files
df <- read_fst("large.fst", columns = c("key_col"))

# Use row ranges for sampling
sample_df <- read_fst("large.fst", from = 1, to = 1000)
```

## Comparison with Other Formats

```r
# fst is typically:
# - 10-100x faster than CSV
# - 2-5x faster than RDS
# - Comparable to arrow/parquet for speed
# - Smaller files than RDS with compression

# Benchmark example
library(microbenchmark)
microbenchmark(
  fst = write_fst(df, "test.fst"),
  rds = saveRDS(df, "test.rds"),
  csv = write.csv(df, "test.csv"),
  times = 10
)
```

## Thread Control

```r
# Set number of threads
threads_fst(4)

# Get current thread count
threads_fst()
```
