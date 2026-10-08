---
name: mongolite
description: R mongolite package for MongoDB. Use for connecting to MongoDB databases and performing CRUD operations.
---

# mongolite

MongoDB client for R.

## Connection

```r
library(mongolite)

# Connect to local MongoDB
con <- mongo(collection = "mycollection", db = "mydb")

# Connect with URI
con <- mongo(
  collection = "mycollection",
  db = "mydb",
  url = "mongodb://user:password@host:27017"
)

# With options
con <- mongo(
  collection = "mycollection",
  db = "mydb",
  url = "mongodb://localhost",
  options = ssl_options()
)
```

## Insert

```r
# Insert data frame
con$insert(df)

# Insert single document
con$insert('{"name": "John", "age": 30}')

# Insert multiple documents
con$insert(list(
  list(name = "John", age = 30),
  list(name = "Jane", age = 25)
))
```

## Query

```r
# Find all
df <- con$find()

# Find with query
df <- con$find('{"age": {"$gt": 25}}')

# Select fields
df <- con$find(fields = '{"name": 1, "age": 1, "_id": 0}')

# Sort
df <- con$find(sort = '{"age": -1}')

# Limit
df <- con$find(limit = 10)

# Skip (pagination)
df <- con$find(skip = 10, limit = 10)

# Combined
df <- con$find(
  query = '{"status": "active"}',
  fields = '{"name": 1, "email": 1}',
  sort = '{"created": -1}',
  limit = 100
)
```

## Update

```r
# Update one
con$update('{"name": "John"}', '{"$set": {"age": 31}}')

# Update many
con$update('{"status": "pending"}', '{"$set": {"status": "active"}}', multiple = TRUE)

# Upsert
con$update('{"name": "New"}', '{"$set": {"age": 20}}', upsert = TRUE)

# Replace document
con$replace('{"name": "John"}', '{"name": "John", "age": 32, "city": "NYC"}')
```

## Delete

```r
# Remove one
con$remove('{"name": "John"}', just_one = TRUE)

# Remove many
con$remove('{"status": "inactive"}')

# Remove all
con$remove('{}')

# Drop collection
con$drop()
```

## Aggregation

```r
# Aggregation pipeline
result <- con$aggregate('[
  {"$match": {"status": "active"}},
  {"$group": {"_id": "$category", "count": {"$sum": 1}}},
  {"$sort": {"count": -1}}
]')

# With multiple stages
result <- con$aggregate('[
  {"$match": {"date": {"$gte": {"$date": "2024-01-01"}}}},
  {"$project": {"year": {"$year": "$date"}, "amount": 1}},
  {"$group": {"_id": "$year", "total": {"$sum": "$amount"}}}
]')
```

## Indexes

```r
# Create index
con$index(add = '{"name": 1}')
con$index(add = '{"location": "2dsphere"}')

# List indexes
con$index()

# Remove index
con$index(remove = "name_1")
```

## Count and Distinct

```r
# Count documents
con$count('{"status": "active"}')

# Distinct values
con$distinct("category")
con$distinct("category", '{"status": "active"}')
```

## Iterate

```r
# Iterate over large results
iter <- con$iterate('{"status": "active"}')
while (!is.null(doc <- iter$one())) {
  # Process document
  print(doc$name)
}
```

## GridFS (Large Files)

```r
# Store files
fs <- gridfs(db = "mydb")
fs$upload("large_file.csv")

# Download
fs$download("large_file.csv", "local_copy.csv")

# List files
fs$find()
```
