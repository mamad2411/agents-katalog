---
name: feather
description: R feather package for fast binary data format. Use for fast reading/writing of data frames between R and Python.
---

# feather

Fast on-disk format for data frames.

## Read/Write

```r
library(feather)

# Write feather file
write_feather(df, "data.feather")

# Read feather file
df <- read_feather("data.feather")

# Read specific columns
df <- read_feather("data.feather", columns = c("col1", "col2"))
```

## Metadata

```r
# Get metadata without reading data
meta <- feather_metadata("data.feather")
meta$dim        # Dimensions
meta$types      # Column types
meta$path       # File path
```

## With Arrow

```r
library(arrow)

# Modern replacement using arrow
write_feather(df, "data.feather")
df <- read_feather("data.feather")

# Arrow table
tbl <- arrow_table(df)
write_feather(tbl, "data.feather")
```

## Performance Tips

```r
# Feather is column-oriented
# Best for: wide data, column selection
# Fast for: reading subsets of columns

# Read only needed columns
df <- read_feather("data.feather",
  columns = c("id", "value"))
```

## Cross-Language

```python
# Python (pandas)
import pandas as pd
df = pd.read_feather("data.feather")
df.to_feather("data.feather")
```
