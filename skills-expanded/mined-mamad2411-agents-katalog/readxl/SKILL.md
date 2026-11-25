---
name: readxl
description: R readxl package for reading Excel files. Use for importing .xls and .xlsx files.
---

# readxl

Read Excel files.

## Basic Reading

```r
library(readxl)

# Read first sheet
df <- read_excel("file.xlsx")

# Read specific sheet
df <- read_excel("file.xlsx", sheet = "Sheet2")
df <- read_excel("file.xlsx", sheet = 2)

# Read .xls files
df <- read_excel("file.xls")
```

## Options

```r
df <- read_excel("file.xlsx",
  # Sheet
  sheet = 1,
  
  # Range
  range = "A1:D100",
  range = "Sheet2!A1:D100",
  range = cell_rows(1:100),
  range = cell_cols("A:D"),
  
  # Column names
  col_names = TRUE,
  col_names = c("a", "b", "c"),
  
  # Column types
  col_types = c("text", "numeric", "date", "skip"),
  col_types = "guess",
  
  # Skip/limit
  skip = 2,
  n_max = 1000,
  
  # Missing values
  na = c("", "NA", "N/A", "-"),
  
  # Trimming
  trim_ws = TRUE
)
```

## Column Types

```r
# Specify types
df <- read_excel("file.xlsx", col_types = c(
  "skip",      # Skip column
  "guess",     # Guess type
  "logical",   # TRUE/FALSE
  "numeric",   # Numbers
  "date",      # Dates
  "text",      # Text
  "list"       # Mixed types
))

# All as text
df <- read_excel("file.xlsx", col_types = "text")
```

## Sheet Information

```r
# List sheets
excel_sheets("file.xlsx")

# Read all sheets
sheets <- excel_sheets("file.xlsx")
all_data <- lapply(sheets, function(s) read_excel("file.xlsx", sheet = s))
names(all_data) <- sheets

# With purrr
library(purrr)
all_data <- map(excel_sheets("file.xlsx"), ~ read_excel("file.xlsx", sheet = .x))
```

## Cell Ranges

```r
# Specific range
df <- read_excel("file.xlsx", range = "B2:E50")

# Named range
df <- read_excel("file.xlsx", range = "MyNamedRange")

# Cell helpers
range = cell_rows(1:100)
range = cell_cols("A:D")
range = cell_limits(c(1, 1), c(100, 4))
range = anchored("B2", dim = c(100, 4))
```

## Multiple Files

```r
# Read multiple files
files <- list.files(pattern = "\\.xlsx$")
all_data <- lapply(files, read_excel)

# With file names
all_data <- lapply(files, function(f) {
  df <- read_excel(f)
  df$source <- f
  df
})
all_data <- do.call(rbind, all_data)
```
