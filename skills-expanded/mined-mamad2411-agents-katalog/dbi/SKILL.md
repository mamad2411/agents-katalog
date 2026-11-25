---
name: DBI
description: R DBI package for database interface. Use for connecting to and querying databases with a common interface.
---

# DBI

Database interface.

## Connection

```r
library(DBI)

# SQLite
con <- dbConnect(RSQLite::SQLite(), "database.sqlite")
con <- dbConnect(RSQLite::SQLite(), ":memory:")

# PostgreSQL
con <- dbConnect(
  RPostgres::Postgres(),
  dbname = "mydb",
  host = "localhost",
  port = 5432,
  user = "user",
  password = "password"
)

# MySQL/MariaDB
con <- dbConnect(
  RMariaDB::MariaDB(),
  dbname = "mydb",
  host = "localhost",
  user = "user",
 password = "password"
)

# Disconnect
dbDisconnect(con)
```

## Queries

```r
# Execute query
result <- dbGetQuery(con, "SELECT * FROM table WHERE x > 10")

# Execute statement (no return)
dbExecute(con, "UPDATE table SET x = 1 WHERE id = 5")
dbExecute(con, "DELETE FROM table WHERE id = 5")

# Parameterized queries (safe from SQL injection)
dbGetQuery(con, "SELECT * FROM table WHERE id = ?", params = list(5))
dbGetQuery(con, "SELECT * FROM table WHERE name = $1", params = list("John"))

# Send query (for large results)
res <- dbSendQuery(con, "SELECT * FROM large_table")
while (!dbHasCompleted(res)) {
  chunk <- dbFetch(res, n = 1000)
  # Process chunk
}
dbClearResult(res)
```

## Tables

```r
# List tables
dbListTables(con)

# Check if table exists
dbExistsTable(con, "table_name")

# Read table
df <- dbReadTable(con, "table_name")

# Write table
dbWriteTable(con, "new_table", df)
dbWriteTable(con, "table", df, append = TRUE)
dbWriteTable(con, "table", df, overwrite = TRUE)

# Remove table
dbRemoveTable(con, "table_name")

# List fields
dbListFields(con, "table_name")
```

## Transactions

```r
# Begin transaction
dbBegin(con)

tryCatch({
  dbExecute(con, "INSERT INTO table VALUES (1, 'a')")
  dbExecute(con, "INSERT INTO table VALUES (2, 'b')")
  dbCommit(con)
}, error = function(e) {
  dbRollback(con)
  stop(e)
})

# With transaction helper
dbWithTransaction(con, {
  dbExecute(con, "INSERT INTO table VALUES (1, 'a')")
  dbExecute(con, "INSERT INTO table VALUES (2, 'b')")
})
```

## Metadata

```r
# Connection info
dbGetInfo(con)

# Query info
res <- dbSendQuery(con, "SELECT * FROM table")
dbGetInfo(res)
dbColumnInfo(res)
dbGetRowCount(res)
dbGetRowsAffected(res)
dbClearResult(res)
```

## Data Types

```r
# Quote identifiers
dbQuoteIdentifier(con, "table_name")
dbQuoteIdentifier(con, c("schema", "table"))

# Quote strings
dbQuoteString(con, "value")

# Quote literals
dbQuoteLiteral(con, 42)
dbQuoteLiteral(con, Sys.Date())
```

## Batch Operations

```r
# Append many rows efficiently
dbAppendTable(con, "table", df)

# Create table from data frame
dbCreateTable(con, "new_table", df)
```
