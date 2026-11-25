---
name: odbc
description: R odbc package for ODBC database connections. Use for connecting to any ODBC-compatible database.
---

# odbc Package

ODBC database connections.

## Connect

```r
library(DBI)
library(odbc)

# DSN connection
con <- dbConnect(odbc(), dsn = "MyDSN")

# Connection string
con <- dbConnect(odbc(),
  Driver = "SQL Server",
  Server = "server.example.com",
  Database = "mydb",
  UID = "user",
  PWD = "password"
)

# List available drivers
odbcListDrivers()

# List DSNs
odbcListDataSources()
```

## SQL Server

```r
con <- dbConnect(odbc(),
  Driver = "ODBC Driver 17 for SQL Server",
  Server = "server.example.com",
  Database = "mydb",
  UID = "user",
  PWD = "password",
  Port = 1433
)
```

## MySQL/MariaDB

```r
con <- dbConnect(odbc(),
  Driver = "MySQL ODBC 8.0 Driver",
  Server = "localhost",
  Database = "mydb",
  UID = "user",
  PWD = "password"
)
```

## Basic Operations

```r
# Query
df <- dbGetQuery(con, "SELECT * FROM table")

# Write
dbWriteTable(con, "new_table", df)

# Execute
dbExecute(con, "UPDATE table SET col = 'value'")
```

## Disconnect

```r
dbDisconnect(con)
```
