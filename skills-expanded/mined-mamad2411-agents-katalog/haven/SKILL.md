---
name: haven
description: R haven package for SPSS, Stata, SAS files. Use for reading/writing .sav, .dta, .sas7bdat files with labels.
---

# haven Package

Read and write SPSS, Stata, and SAS files.

## Read Files

```r
library(haven)

# SPSS
spss <- read_sav("data.sav")
spss <- read_spss("data.sav")  # alias

# Stata
stata <- read_dta("data.dta")
stata <- read_stata("data.dta")  # alias

# SAS
sas <- read_sas("data.sas7bdat")
sas_xpt <- read_xpt("data.xpt")  # transport
```

## Write Files

```r
write_sav(df, "output.sav")
write_dta(df, "output.dta")
write_xpt(df, "output.xpt")
```

## Labels

```r
# Value labels
x <- labelled(c(1, 2, 3), c(Low = 1, Med = 2, High = 3))
val_labels(x)

# Variable labels
var_label(df$age) <- "Age in years"

# Convert to factors
as_factor(x)
as_factor(df)  # all labelled columns

# Remove labels
zap_labels(df)
zap_formats(df)
```

## Tagged NA (Stata/SPSS)

```r
# Create tagged NA
tagged_na("a")
tagged_na("b")

# Check
is_tagged_na(x)
na_tag(x)
```
