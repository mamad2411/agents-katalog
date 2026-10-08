---
name: jsonlite
description: R jsonlite package for JSON parsing. Use for reading, writing, and converting JSON data.
---

# jsonlite

JSON parsing and generation.

## Read JSON

```r
library(jsonlite)

# From file
data <- fromJSON("file.json")

# From string
data <- fromJSON('{"name": "John", "age": 30}')

# From URL
data <- fromJSON("https://api.example.com/data")

# Options
data <- fromJSON("file.json",
  simplifyVector = TRUE,
  simplifyDataFrame = TRUE,
  simplifyMatrix = TRUE,
  flatten = TRUE
)
```

## Write JSON

```r
# To string
json <- toJSON(df)
json <- toJSON(df, pretty = TRUE)

# To file
write_json(df, "output.json")
write_json(df, "output.json", pretty = TRUE)

# Options
json <- toJSON(df,
  pretty = TRUE,
  auto_unbox = TRUE,
  na = "null",
  null = "null",
  digits = 4,
  Date = "ISO8601"
)
```

## Data Frame Conversion

```r
# Data frame to JSON
df <- data.frame(x = 1:3, y = c("a", "b", "c"))
toJSON(df)
# [{"x":1,"y":"a"},{"x":2,"y":"b"},{"x":3,"y":"c"}]

# Row-oriented
toJSON(df, dataframe = "rows")

# Column-oriented
toJSON(df, dataframe = "columns")
# {"x":[1,2,3],"y":["a","b","c"]}

# Values only
toJSON(df, dataframe = "values")
# [[1,"a"],[2,"b"],[3,"c"]]
```

## Nested JSON

```r
# Flatten nested
data <- fromJSON("nested.json", flatten = TRUE)

# Access nested elements
data$nested$field
data[["nested"]][["field"]]

# Unnest with tidyr
library(tidyr)
df %>% unnest_wider(nested_col)
```

## Streaming

```r
# Stream large files
stream_in(file("large.json"))

# Stream out
con <- file("output.json", open = "wb")
stream_out(df, con)
close(con)

# NDJSON (newline-delimited)
stream_in(file("data.ndjson"))
stream_out(df, file("output.ndjson"))
```

## API Requests

```r
# GET request
data <- fromJSON("https://api.example.com/data")

# With httr
library(httr)
resp <- GET("https://api.example.com/data")
data <- fromJSON(content(resp, "text"))

# POST with JSON body
resp <- POST(
  "https://api.example.com/data",
  body = toJSON(list(key = "value")),
  content_type_json()
)
```

## Validation

```r
# Validate JSON
validate('{"valid": true}')  # TRUE
validate('{invalid}')        # FALSE

# Minify
minify('{ "x" : 1 }')  # {"x":1}

# Prettify
prettify('{"x":1}')
```
