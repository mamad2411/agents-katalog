---
name: rio
description: R rio package for data import/export. Use for reading/writing any file format with a single function.
---

# rio

Swiss-Army Knife for Data I/O.

## Basic Usage

```r
library(rio)

# Import any format
df <- import("data.csv")
df <- import("data.xlsx")
df <- import("data.json")
df <- import("data.sav")    # SPSS
df <- import("data.dta")    # Stata
df <- import("data.sas7bdat") # SAS

# Export any format
export(df, "output.csv")
export(df, "output.xlsx")
export(df, "output.json")
```

## Supported Formats

```r
# Text formats
import("data.csv")
import("data.tsv")
import("data.txt")
import("data.psv")  # pipe-separated

# Excel
import("data.xlsx")
import("data.xls")

# Statistical software
import("data.sav")      # SPSS
import("data.dta")      # Stata
import("data.sas7bdat") # SAS
import("data.por")      # SPSS portable
import("data.xpt")      # SAS transport

# Other formats
import("data.json")
import("data.xml")
import("data.html")
import("data.yml")
import("data.rds")
import("data.rdata")
import("data.feather")
import("data.parquet")
import("data.fst")
import("data.qs")
```

## Excel Sheets

```r
# Specific sheet
df <- import("data.xlsx", which = 2)
df <- import("data.xlsx", sheet = "Sheet2")

# All sheets
sheets <- import_list("data.xlsx")
# Returns named list of data frames
```

## Multiple Files

```r
# Import multiple files
files <- list.files(pattern = "*.csv")
data_list <- import_list(files)

# Bind into single data frame
df <- import_list(files, rbind = TRUE)

# With file identifier
df <- import_list(files, rbind = TRUE, rbind_label = "source")
```

## Export Options

```r
# CSV options
export(df, "output.csv", row.names = FALSE)

# Excel options
export(df, "output.xlsx", overwrite = TRUE)

# Multiple sheets
export(list(sheet1 = df1, sheet2 = df2), "output.xlsx")

# Compressed
export(df, "output.csv.gz")
```

## Format Detection

```r
# rio detects format from extension
# Override with format argument
df <- import("data.txt", format = "csv")
df <- import("data", format = "tsv")

# Check supported formats
rio:::.import_formats
rio:::.export_formats
```

## Conversion

```r
# Direct file conversion
convert("input.csv", "output.xlsx")
convert("input.sav", "output.csv")
convert("input.dta", "output.rds")
```

## Character Encoding

```r
# Specify encoding
df <- import("data.csv", encoding = "UTF-8")
df <- import("data.csv", encoding = "latin1")

export(df, "output.csv", fileEncoding = "UTF-8")
```

## Handling Issues

```r
# Skip rows
df <- import("data.csv", skip = 5)

# No header
df <- import("data.csv", header = FALSE)

# Custom NA values
df <- import("data.csv", na.strings = c("", "NA", "NULL"))

# Column types
df <- import("data.csv", colClasses = c("character", "numeric"))
```
