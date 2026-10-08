---
name: writexl
description: R writexl package for writing Excel files. Use for creating .xlsx files without Java dependency.
---

# writexl Package

Write Excel files without Java dependency.

## Basic Usage

```r
library(writexl)

# Single sheet
write_xlsx(df, "output.xlsx")

# Multiple sheets
write_xlsx(
  list(
    Sheet1 = df1,
    Sheet2 = df2,
    Results = df3
  ),
  "output.xlsx"
)
```

## Options

```r
write_xlsx(
  df,
  path = "output.xlsx",
  col_names = TRUE,    # Include headers
  format_headers = TRUE # Bold headers
)
```

## With Pipes

```r
library(dplyr)

mtcars %>%
  filter(mpg > 20) %>%
  write_xlsx("filtered.xlsx")
```
