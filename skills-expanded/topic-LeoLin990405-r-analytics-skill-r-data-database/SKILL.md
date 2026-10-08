---
name: r-data-database
description: R database packages for SQL and NoSQL. Use for DBI connections, SQL queries, dbplyr, SQLite, PostgreSQL, MySQL, MongoDB, Redis.
---

# R Database Connections

SQL and NoSQL database access from R.

## DBI (Common Interface)

```r
library(DBI)

# Connect
con <- dbConnect(RSQLite::SQLite(), "database.db")
con <- dbConnect(RPostgres::Postgres(),
  host = "localhost", dbname = "mydb",
  user = "user", password = "pass"
)

# Query
result <- dbGetQuery(con, "SELECT * FROM table WHERE x > 10")

# Execute (no return)
dbExecute(con, "INSERT INTO table VALUES (1, 'a')")
dbExecute(con, "UPDATE table SET x = 10 WHERE id = 1")

# Parameterized queries (safe)
dbGetQuery(con, "SELECT * FROM table WHERE id = ?", params = list(123))

# Tables
dbListTables(con)
dbExistsTable(con, "mytable")
dbWriteTable(con, "newtable", df)
dbReadTable(con, "mytable")
dbRemoveTable(con, "mytable")

# Disconnect
dbDisconnect(con)
```

## dbplyr (dplyr for databases)

```r
library(dplyr)
library(dbplyr)

con <- dbConnect(RSQLite::SQLite(), "database.db")

# Lazy table reference
tbl_db <- tbl(con, "mytable")

# dplyr operations (translated to SQL)
result <- tbl_db %>%
  filter(x > 10) %>%
  select(a, b, c) %>%
  group_by(category) %>%
  summarise(mean = mean(value)) %>%
  collect()  # Execute and bring to R

# View SQL
tbl_db %>% filter(x > 10) %>% show_query()

# Copy local data to database
copy_to(con, df, "temp_table", temporary = TRUE)
```

## SQLite

```r
library(RSQLite)
con <- dbConnect(SQLite(), "mydb.sqlite")

# In-memory database
con <- dbConnect(SQLite(), ":memory:")

dbWriteTable(con, "mtcars", mtcars)
dbGetQuery(con, "SELECT * FROM mtcars WHERE mpg > 20")
dbDisconnect(con)
```

## PostgreSQL

```r
library(RPostgres)
con <- dbConnect(Postgres(),
  host = "localhost",
  port = 5432,
  dbname = "mydb",
  user = "user",
  password = "password"
)

# With connection string
con <- dbConnect(Postgres(),
  "postgresql://user:pass@host:5432/dbname"
)
```

## MySQL/MariaDB

```r
library(RMariaDB)
con <- dbConnect(MariaDB(),
  host = "localhost",
  dbname = "mydb",
  user = "user",
  password = "password"
)
```

## ODBC (Universal)

```r
library(odbc)

# List drivers
odbcListDrivers()

# Connect
con <- dbConnect(odbc(),
  Driver = "SQL Server",
  Server = "server_name",
  Database = "db_name",
  UID = "user",
  PWD = "password"
)

# DSN connection
con <- dbConnect(odbc(), dsn = "my_dsn")
```

## MongoDB

```r
library(mongolite)

# Connect
mongo <- mongo(
  collection = "mycollection",
  db = "mydb",
  url = "mongodb://localhost:27017"
)

# Query
data <- mongo$find('{"x": {"$gt": 10}}')
data <- mongo$find(limit = 100)

# Insert
mongo$insert(df)

# Update
mongo$update('{"id": 1}', '{"$set": {"x": 100}}')

# Aggregate
mongo$aggregate('[
  {"$match": {"x": {"$gt": 10}}},
  {"$group": {"_id": "$category", "count": {"$sum": 1}}}
]')
```

## Redis

```r
library(redux)

r <- redux::hiredis()

# Key-value
r$SET("key", "value")
r$GET("key")

# Hash
r$HSET("hash", "field", "value")
r$HGET("hash", "field")

# List
r$LPUSH("list", "item")
r$LRANGE("list", 0, -1)
```

## Connection Pooling

```r
library(pool)

pool <- dbPool(
  drv = RPostgres::Postgres(),
  dbname = "mydb",
  host = "localhost",
  user = "user",
  password = "password",
  minSize = 1,
  maxSize = 5
)

# Use pool like connection
dbGetQuery(pool, "SELECT * FROM table")

# Close pool
poolClose(pool)
```
