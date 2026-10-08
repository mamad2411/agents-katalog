---
name: dbplyr
description: R dbplyr package for database backends. Use for dplyr verbs on database tables with lazy evaluation.
---

# dbplyr Package

dplyr backend for databases with lazy evaluation.

## Connect and Use

```r
library(dplyr)
library(dbplyr)
library(DBI)

con <- dbConnect(RSQLite::SQLite(), "database.db")

# Reference table (lazy)
tbl_flights <- tbl(con, "flights")

# dplyr verbs (translated to SQL)
result <- tbl_flights %>%
  filter(year == 2023) %>%
  group_by(carrier) %>%
  summarise(
    n = n(),
    avg_delay = mean(arr_delay, na.rm = TRUE)
  ) %>%
  arrange(desc(n))

# View SQL
show_query(result)

# Execute and collect
df <- collect(result)
```

## SQL Translation

```r
# See generated SQL
tbl_flights %>%
  filter(distance > 1000) %>%
  select(carrier, flight, distance) %>%
  show_query()

# Custom SQL
tbl(con, sql("SELECT * FROM flights WHERE year = 2023"))
```

## Window Functions

```r
tbl_flights %>%
  group_by(carrier) %>%
  mutate(
    rank = row_number(),
    pct = percent_rank()
  ) %>%
  show_query()
```

## Compute/Copy

```r
# Create temp table from query
tbl_flights %>%
  filter(month == 1) %>%
  compute("jan_flights")

# Copy local df to database
copy_to(con, local_df, "new_table")
```

## Disconnect

```r
dbDisconnect(con)
```
