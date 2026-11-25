---
name: vroom
description: R vroom package for fast reading of delimited files. Use for reading large CSV/TSV files with lazy loading.
---

# vroom

Lightning fast reading of delimited files.

## Basic Reading

```r
library(vroom)

# Read CSV
df <- vroom("file.csv")
df <- vroom("file.tsv")

# Multiple files
df <- vroom(c("file1.csv", "file2.csv"))
df <- vroom(list.files(pattern = "*.csv"))

# Compressed files
df <- vroom("file.csv.gz")
df <- vroom("file.csv.bz2")
df <- vroom("file.csv.xz")
```

## Column Selection

```r
# Select columns
df <- vroom("file.csv", col_select = c(id, name, value))
df <- vroom("file.csv", col_select = 1:5)
df <- vroom("file.csv", col_select = starts_with("x"))

# Exclude columns
df <- vroom("file.csv", col_select = -c(temp, unused))
```

## Column Types

```r
# Specify types
df <- vroom("file.csv", col_types = cols(
  id = col_integer(),
  name = col_character(),
  value = col_double(),
  date = col_date(format = "%Y-%m-%d"),
  flag = col_logical()
))

# Compact specification
df <- vroom("file.csv", col_types = "icdDl")
# i=integer, c=character, d=double, D=date, l=logical

# Default type
df <- vroom("file.csv", col_types = cols(.default = col_character()))
```

## Delimiters

```r
# Custom delimiter
df <- vroom("file.txt", delim = "|")
df <- vroom("file.txt", delim = "\t")
df <- vroom("file.txt", delim = ";")

# Fixed width
df <- vroom_fwf("file.txt", col_positions = fwf_widths(c(10, 20, 5)))
```

## Performance Options

```r
# Altrep (lazy loading)
df <- vroom("file.csv", altrep = TRUE)  # Default

# Materialize all data
df <- vroom("file.csv", altrep = FALSE)

# Number of threads
df <- vroom("file.csv", num_threads = 4)

# Progress bar
df <- vroom("file.csv", progress = TRUE)
```

## Writing

```r
# Write delimited
vroom_write(df, "output.csv")
vroom_write(df, "output.tsv", delim = "\t")

# Compressed output
vroom_write(df, "output.csv.gz")

# Append
vroom_write(df, "output.csv", append = TRUE)
```

## Handling Issues

```r
# Skip rows
df <- vroom("file.csv", skip = 5)

# No header
df <- vroom("file.csv", col_names = FALSE)
df <- vroom("file.csv", col_names = c("a", "b", "c"))

# Comment lines
df <- vroom("file.csv", comment = "#")

# NA values
df <- vroom("file.csv", na = c("", "NA", "NULL", "-999"))

# Locale
df <- vroom("file.csv", locale = locale(
  decimal_mark = ",",
  grouping_mark = ".",
  encoding = "UTF-8"
))
```

## Chunked Reading

```r
# Read in chunks
callback <- function(chunk, pos) {
  # Process chunk
  result <- chunk %>% filter(value > 100)
  return(result)
}

df <- vroom("large_file.csv",
  chunk_size = 100000,
  callback = callback
)
```
