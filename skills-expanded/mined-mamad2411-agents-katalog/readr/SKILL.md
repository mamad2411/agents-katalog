---
name: readr
description: R readr package for reading rectangular data. Use for fast CSV, TSV, and fixed-width file reading.
---

# readr

Fast rectangular data reading.

## Read Functions

```r
library(readr)

# CSV
df <- read_csv("file.csv")
df <- read_csv("file.csv", col_names = FALSE)
df <- read_csv("file.csv", skip = 2)
df <- read_csv("file.csv", n_max = 1000)

# TSV
df <- read_tsv("file.tsv")

# Delimited
df <- read_delim("file.txt", delim = "|")

# Fixed width
df <- read_fwf("file.txt", fwf_widths(c(10, 5, 8)))
df <- read_fwf("file.txt", fwf_positions(c(1, 11, 16), c(10, 15, 23)))

# Lines
lines <- read_lines("file.txt")

# Whole file
text <- read_file("file.txt")
```

## Column Specification

```r
# Explicit types
df <- read_csv("file.csv", col_types = cols(
  id = col_integer(),
  name = col_character(),
  value = col_double(),
  date = col_date(format = "%Y-%m-%d"),
  flag = col_logical()
))

# Column types
col_logical()
col_integer()
col_double()
col_character()
col_factor(levels = c("A", "B", "C"))
col_date(format = "")
col_datetime(format = "")
col_time(format = "")
col_number()
col_skip()
col_guess()

# Shorthand
df <- read_csv("file.csv", col_types = "icdDl")
# i = integer, c = character, d = double, D = date, l = logical
# n = number, _ = skip, ? = guess
```

## Options

```r
df <- read_csv("file.csv",
  # Column names
  col_names = TRUE,
  col_names = c("a", "b", "c"),
  
  # Skip/limit
  skip = 0,
  n_max = Inf,
  skip_empty_rows = TRUE,
  
  # Missing values
  na = c("", "NA", "NULL", "-999"),
  
  # Locale
  locale = locale(
    encoding = "UTF-8",
    decimal_mark = ".",
    grouping_mark = ",",
    date_format = "%Y-%m-%d",
    tz = "UTC"
  ),
  
  # Quoting
  quote = "\"",
  
  # Comments
  comment = "#",
  
  # Trimming
  trim_ws = TRUE,
  
  # Progress
  progress = TRUE
)
```

## Write Functions

```r
# CSV
write_csv(df, "output.csv")
write_csv(df, "output.csv", na = "")
write_csv(df, "output.csv", append = TRUE)

# TSV
write_tsv(df, "output.tsv")

# Delimited
write_delim(df, "output.txt", delim = "|")

# Excel-friendly CSV
write_excel_csv(df, "output.csv")

# Lines
write_lines(lines, "output.txt")

# File
write_file(text, "output.txt")
```

## Parsing

```r
# Parse vectors
parse_integer(c("1", "2", "3"))
parse_double(c("1.5", "2.5"))
parse_number("$1,234.56")
parse_logical(c("TRUE", "FALSE", "T", "F"))
parse_date("2024-01-15")
parse_datetime("2024-01-15 10:30:00")
parse_factor(c("A", "B", "A"), levels = c("A", "B", "C"))

# Guess parser
guess_parser(c("1", "2", "3"))
```

## Problems

```r
# Check for parsing problems
df <- read_csv("file.csv")
problems(df)

# Stop on problems
df <- read_csv("file.csv", col_types = cols(.default = col_character()))
```
