---
name: r-data
description: R data manipulation, formats, and database packages. Use for data wrangling with dplyr/data.table, reading files (CSV, Excel, JSON, Arrow), and database connections (SQL, MongoDB, Redis).
---

# R Data Skill

## Sub-skills

| Sub-skill | Description |
|-----------|-------------|
| [r-data-manipulation](r-data-manipulation/SKILL.md) | dplyr, data.table, tidyr |
| [r-data-formats](r-data-formats/SKILL.md) | CSV, Excel, JSON, Arrow, Parquet |
| [r-data-database](r-data-database/SKILL.md) | SQL, MongoDB, Redis connections |

Data manipulation, formats, and database management in R.

## Data Manipulation

| Package | Description |
|---------|-------------|
| **dplyr** ★ | Fast data frames manipulation and database query |
| **data.table** ★ | Fast manipulation with concise syntax |
| **tidyr** | Tidy messy data with spread/gather |
| **reshape2** ★ | Flexible reshape and aggregate |
| **broom** ★ | Convert models to tidy data frames |
| **tidyverse** | Meta-package for data science |
| **lubridate** | Date/time manipulation |
| **stringr** ★ | Consistent string processing |
| **stringi** ★ | ICU-based string processing |
| **fuzzyjoin** | Join on inexact matching |
| **rlist** | Non-tabular data manipulation |
| **bigmemory** | Shared memory matrices |
| **snakecase** | Case conversion |
| **DataExplorer** | Fast EDA with minimum code |

## Data Formats

| Package | Description |
|---------|-------------|
| **arrow** ★ | Apache Arrow interface |
| **fst** ★ | Lightning fast serialization |
| **feather** ★ | Fast binary data frame storage |
| **readr** ★ | Fast tabular data reading |
| **readxl** ★ | Read Excel files |
| **haven** | Read SPSS, Stata, SAS |
| **jsonlite** | JSON parsing |
| **vroom** | Fast delimited file reading |
| **rio** | Swiss-Army Knife for Data I/O |
| **qs** | Quick serialization |
| **writexl** | Write Excel files |
| **yaml** | YAML conversion |
| **readODS** | Read OpenDocument Spreadsheets |
| **RcppTOML** | TOML file parsing |

## Database Management

| Package | Description |
|---------|-------------|
| **DBI** | Common database interface |
| **odbc** | ODBC connections (DBI interface) |
| **RSQLite** | SQLite interface |
| **RPostgres** | PostgreSQL (DBI-compliant) |
| **RMariaDB** | MariaDB/MySQL interface |
| **RMySQL** | MySQL interface |
| **ROracle** | Oracle database interface |
| **RODBC** | ODBC database access |
| **RJDBC** | JDBC interface |
| **mongolite** | MongoDB streaming client |
| **rmongodb** | MongoDB driver |
| **redux** | Redis client |
| **elastic** | Elasticsearch HTTP API |
| **RNeo4j** | Neo4j graph database |
| **RCassandra** | Apache Cassandra interface |
| **RHive** | Apache Hive integration |
| **rpostgis** | PostGIS spatial interface |

## Quick Examples

```r
# dplyr pipeline
library(dplyr)
df %>%
  filter(x > 10) %>%
  select(a, b) %>%
  mutate(c = a + b) %>%
  group_by(category) %>%
  summarise(mean = mean(c))

# data.table
library(data.table)
dt <- as.data.table(df)
dt[x > 10, .(mean = mean(c)), by = category]

# Read various formats
readr::read_csv("data.csv")
readxl::read_excel("data.xlsx")
arrow::read_parquet("data.parquet")
jsonlite::fromJSON("data.json")

# Database query
library(DBI)
con <- dbConnect(RSQLite::SQLite(), "db.sqlite")
dbGetQuery(con, "SELECT * FROM table WHERE x > 10")
dbDisconnect(con)
```

## Resources

- dplyr: https://dplyr.tidyverse.org/
- data.table: https://rdatatable.gitlab.io/data.table/
- arrow: https://arrow.apache.org/docs/r/
- DBI: https://dbi.r-dbi.org/
