---
name: RPostgres
description: R RPostgres package for PostgreSQL databases. Use for PostgreSQL connections with modern DBI interface.
---

# RPostgres Package

PostgreSQL database interface.

## Connect

```r
library(DBI)
library(RPostgres)

con <- dbConnect(
  Postgres(),
  dbname = "mydb",
  host = "localhost",
  port = 5432,
  user = "user",
  password = "password"
)

# With connection string
con <- dbConnect(
  Postgres(),
  "postgresql://user:password@localhost:5432/mydb"
)
```

## Basic Operations

```r
# Query
df <- dbGetQuery(con, "SELECT * FROM users LIMIT 100")

# Write table
dbWriteTable(con, "new_table", df)

# Append
dbWriteTable(con, "existing", df, append = TRUE)

# Overwrite
dbWriteTable(con, "existing", df, overwrite = TRUE)
```

## Parameterized Queries

```r
dbGetQuery(con,
  "SELECT * FROM users WHERE id = $1 AND status = $2",
  params = list(123, "active")
)
```

## COPY Protocol (Fast)

```r
# Fast bulk insert
dbWriteTable(con, "big_table", big_df, copy = TRUE)
```

## Schemas

```r
# Specify schema
dbWriteTable(con, Id(schema = "analytics", table = "events"), df)
dbReadTable(con, Id(schema = "analytics", table = "events"))
```

## Disconnect

```r
dbDisconnect(con)
```
