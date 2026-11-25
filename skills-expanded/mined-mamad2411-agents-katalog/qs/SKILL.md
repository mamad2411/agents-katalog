---
name: qs
description: R qs package for quick serialization of R objects. Use for fast saving/loading of any R object with high compression.
---

# qs

Quick serialization of R objects.

## Basic Usage

```r
library(qs)

# Save any R object
qsave(obj, "data.qs")

# Load
obj <- qread("data.qs")
```

## Presets

```r
# Fast preset (speed priority)
qsave(obj, "data.qs", preset = "fast")

# High preset (compression priority)
qsave(obj, "data.qs", preset = "high")

# Balanced preset (default)
qsave(obj, "data.qs", preset = "balanced")

# Archive preset (maximum compression)
qsave(obj, "data.qs", preset = "archive")

# Uncompressed
qsave(obj, "data.qs", preset = "uncompressed")
```

## Custom Settings

```r
# Custom compression
qsave(obj, "data.qs",
  algorithm = "zstd",      # or "lz4", "zstd_stream", "lz4_stream"
  compress_level = 4,      # 1-22 for zstd, 1-12 for lz4
  nthreads = 4
)

# Shuffle for better compression of numeric data
qsave(obj, "data.qs", shuffle_control = 15)
```

## Supported Objects

```r
# qs supports virtually all R objects:
# - Data frames, tibbles, data.tables
# - Lists, environments
# - Matrices, arrays
# - Functions, formulas
# - S3, S4, R6 objects
# - Factors with levels
# - Attributes preserved

# Complex nested structures
complex_obj <- list(
  df = data.frame(x = 1:100),
  model = lm(y ~ x, data = df),
  func = function(x) x^2,
  env = new.env()
)
qsave(complex_obj, "complex.qs")
```

## Streaming

```r
# Save to connection
con <- file("data.qs", "wb")
qsave(obj, con)
close(con)

# Read from connection
con <- file("data.qs", "rb")
obj <- qread(con)
close(con)

# Save to raw vector
raw_data <- qserialize(obj)

# Load from raw vector
obj <- qdeserialize(raw_data)
```

## Performance

```r
# qs is typically:
# - 3-10x faster than saveRDS
# - Better compression than RDS
# - Supports multithreading

# Benchmark
library(microbenchmark)
microbenchmark(
  qs = qsave(df, "test.qs"),
  rds = saveRDS(df, "test.rds"),
  times = 10
)
```

## Thread Control

```r
# Set threads for save/load
qsave(obj, "data.qs", nthreads = 4)
obj <- qread("data.qs", nthreads = 4)

# Check available threads
qs::qread_threads()
```

## Strict Mode

```r
# Strict mode for reproducibility
qsave(obj, "data.qs", strict = TRUE)

# Validates object integrity on read
obj <- qread("data.qs", strict = TRUE)
```

## Hash Verification

```r
# Save with hash
qsave(obj, "data.qs", check_hash = TRUE)

# Verify on read
obj <- qread("data.qs", validate_checksum = TRUE)
```
