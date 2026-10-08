---
name: r-data-formats
description: R data format packages for reading/writing files. Use for CSV (readr, vroom), Excel (readxl, writexl), JSON (jsonlite), Parquet (arrow), and fast serialization (fst, qs).
---

# R Data Formats

Reading and writing various data formats.

## CSV/TSV

```r
# readr (tidyverse)
library(readr)
df <- read_csv("data.csv")
df <- read_tsv("data.tsv")
df <- read_delim("data.txt", delim = "|")
write_csv(df, "output.csv")

# vroom (faster for large files)
library(vroom)
df <- vroom("data.csv")
df <- vroom(c("file1.csv", "file2.csv"))  # Multiple files

# Base R
df <- read.csv("data.csv", stringsAsFactors = FALSE)
write.csv(df, "output.csv", row.names = FALSE)

# data.table (fastest)
library(data.table)
dt <- fread("data.csv")
fwrite(dt, "output.csv")
```

## Excel

```r
# Read
library(readxl)
df <- read_excel("data.xlsx")
df <- read_excel("data.xlsx", sheet = "Sheet2")
df <- read_excel("data.xlsx", range = "A1:D100")
excel_sheets("data.xlsx")  # List sheets

# Write
library(writexl)
write_xlsx(df, "output.xlsx")
write_xlsx(list(sheet1 = df1, sheet2 = df2), "output.xlsx")

# openxlsx (more features)
library(openxlsx)
wb <- createWorkbook()
addWorksheet(wb, "Data")
writeData(wb, "Data", df)
saveWorkbook(wb, "output.xlsx")
```

## JSON

```r
library(jsonlite)

# Read
df <- fromJSON("data.json")
data <- fromJSON('{"name": "test", "value": 123}')

# Write
json <- toJSON(df, pretty = TRUE)
write_json(df, "output.json")

# API responses
resp <- httr::GET("https://api.example.com/data")
data <- fromJSON(httr::content(resp, "text"))
```

## Arrow/Parquet

```r
library(arrow)

# Parquet (columnar, compressed)
df <- read_parquet("data.parquet")
write_parquet(df, "output.parquet")

# Feather (fast binary)
df <- read_feather("data.feather")
write_feather(df, "output.feather")

# Arrow datasets (large/partitioned)
ds <- open_dataset("data_dir/", format = "parquet")
ds %>% filter(x > 10) %>% collect()
```

## Fast Serialization

```r
# fst (fastest for data frames)
library(fst)
write_fst(df, "data.fst", compress = 100)
df <- read_fst("data.fst")
df <- read_fst("data.fst", columns = c("a", "b"))

# qs (general R objects)
library(qs)
qsave(obj, "data.qs")
obj <- qread("data.qs")

# RDS (base R)
saveRDS(obj, "data.rds")
obj <- readRDS("data.rds")
```

## Other Formats

```r
# SPSS, Stata, SAS
library(haven)
df <- read_sav("data.sav")   # SPSS
df <- read_dta("data.dta")   # Stata
df <- read_sas("data.sas7bdat")  # SAS

# YAML
library(yaml)
data <- yaml.load_file("config.yaml")
write_yaml(data, "output.yaml")

# XML
library(xml2)
doc <- read_xml("data.xml")

# rio (auto-detect format)
library(rio)
df <- import("data.xlsx")
df <- import("data.sav")
export(df, "output.csv")
```

## Format Comparison

| Format | Speed | Size | Features |
|--------|-------|------|----------|
| CSV | Slow | Large | Universal |
| Parquet | Fast | Small | Columnar, types |
| fst | Fastest | Medium | R-specific |
| Feather | Fast | Medium | Cross-language |
| RDS | Medium | Medium | Any R object |
