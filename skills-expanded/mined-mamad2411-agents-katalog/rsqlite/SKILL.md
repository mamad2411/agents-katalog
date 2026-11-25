---
name: RSQLite
description: R RSQLite package for SQLite databases. Use for embedded SQLite database connections.
---

# RSQLite Package

SQLite database interface.

## Connect

```r
library(DBI)
library(RSQLite)

# File database
con <- dbConnect(SQLite(), "database.db")

# In-memory
con <- dbConnect(SQLite(), ":memory:")
```

## Basic Operations

```r
# Write table
dbWriteTable(con, "mtcars", mtcars)

# List tables
dbListTables(con)

# Read table
df <- dbReadTable(con, "mtcars")

# Query
result <- dbGetQuery(con, "SELECT * FROM mtcars WHERE mpg > 20")

# Remove table
dbRemoveTable(con, "mtcars")
```

## Parameterized Queries

```r
# Safe from SQL injection
dbGetQuery(con,
  "SELECT * FROM users WHERE id = ?",
  params = list(user_id)
)

# Named parameters
dbGetQuery(con,
  "SELECT * FROM users WHERE name = :name AND age > :age",
  params = list(name = "John", age = 25)
)
```

## Transactions

```r
dbBegin(con)
tryCatch({
  dbExecute(con, "INSERT INTO ...")
  dbExecute(con, "UPDATE ...")
  dbCommit(con)
}, error = function(e) {
  dbRollback(con)
  stop(e)
})
```

## Disconnect

```r
dbDisconnect(con)
```
