---
name: azure-data-toolkit
description: Consolidated toolkit for azure-data. Covers azure-data-tables-java, azure-data-tables-py
---
# Azure Data Toolkit

## Core Capabilities
# Azure Data Toolkit

# Azure Tables SDK for Java

Build table storage applications using the Azure Tables SDK for Java. Works with both Azure Table Storage and Cosmos DB Table API.

## Installation

```xml
<dependency>
  <groupId>com.azure</groupId>
  <artifactId>azure-data-tables</artifactId>
  <version>12.6.0-beta.1</version>
</dependency>
```

## Client Creation

### With Connection String

```java
import com.azure.data.tables.TableServiceClient;
import com.azure.data.tables.TableServiceClientBuilder;
import com.azure.data.tables.TableClient;

TableServiceClient serviceClient = new TableServiceClientBuilder()
    .connectionString("<your-connection-string>")
    .buildClient();
```

### With Shared Key

```java
import com.azure.core.credential.AzureNamedKeyCredential;

AzureNamedKeyCredential credential = new AzureNamedKeyCredential(
    "<account-name>",
    "<account-key>");

TableServiceClient serviceClient = new TableServiceClientBuilder()
    .endpoint("<your-table-account-url>")
    .credential(credential)
    .buildClient();
```

### With SAS Token

```java
TableServiceClient serviceClient = new TableServiceClientBuilder()
    .endpoint("<your-table-account-url>")
    .sasToken("<sas-token>")
    .buildClient();
```

### With DefaultAzureCredential (Storage only)

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

TableServiceClient serviceClient = new TableServiceClientBuilder()
    .endpoint("<your-table-account-url>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

## Key Concepts

- **TableServiceClient**: Manage tables (create, list, delete)
- **TableClient**: Manage entities within a table (CRUD)
- **Partition Key**: Groups entities for efficient queries
- **Row Key**: Unique identifier within a partition
- **Entity**: A row with up to 252 properties (1MB Storage, 2MB Cosmos)

## Core Patterns

### Create Table

```java
// Create table (throws if exists)
TableClient tableClient = serviceClient.createTable("mytable");

// Create if not exists (no exception)
TableClient tableClient = serviceClient.createTableIfNotExists("mytable");
```

### Get Table Client

```java
// From service client
TableClient tableClient = serviceClient.getTableClient("mytable");

// Direct construction
TableClient tableClient = new TableClientBuilder()
    .connectionString("<connection-string>")
    .tableName("mytable")
    .buildClient();
```

### Create Entity

```java
import com.azure.data.tables.models.TableEntity;

TableEntity entity = new TableEntity("partitionKey", "rowKey")
    .addProperty("Name", "Product A")
    .addProperty("Price", 29.99)
    .addProperty("Quantity", 100)
    .addProperty("IsAvailable", true);

tableClient.createEntity(entity);
```

### Get Entity

```java
TableEntity entity = tableClient.getEntity("partitionKey", "rowKey");

String name = (String) entity.getProperty("Name");
Double price = (Double) entity.getProperty("Price");
System.out.printf("Product: %s, Price: %.2f%n", name, price);
```

### Update Entity

```java
import com.azure.data.tables.models.TableEntityUpdateMode;

// Merge (update only specified properties)
TableEntity updateEntity = new TableEntity("partitionKey", "rowKey")
    .addProperty("Price", 24.99);
tableClient.updateEntity(updateEntity, TableEntityUpdateMode.MERGE);

// Replace (replace entire entity)
TableEntity replaceEntity = new TableEntity("partitionKey", "rowKey")
    .addProperty("Name", "Product A Updated")
    .addProperty("Price", 24.99)
    .addProperty("Quantity", 150);
tableClient.updateEntity(replaceEntity, TableEntityUpdateMode.REPLACE);
```

### Upsert Entity

```java
// Insert or update (merge mode)
tableClient.upsertEntity(entity, TableEntityUpdateMode.MERGE);

// Insert or replace
tableClient.upsertEntity(entity, TableEntityUpdateMode.REPLACE);
```

### Delete Entity

```java
tableClient.deleteEntity("partitionKey", "rowKey");
```

### List Entities

```java
import com.azure.data.tables.models.ListEntitiesOptions;

// List all entities
for (TableEntity entity : tableClient.listEntities()) {
    System.out.printf("%s - %s%n",
        entity.getPartitionKey(),
        entity.getRowKey());
}

// With filtering and selection
ListEntitiesOptions options = new ListEntitiesOptions()
    .setFilter("PartitionKey eq 'sales'")
    .setSelect("Name", "Price");

for (TableEntity entity : tableClient.listEntities(options, null, null)) {
    System.out.printf("%s: %.2f%n",
        entity.getProperty("Name"),
        entity.getProperty("Price"));
}
```

### Query with OData Filter

```java
// Filter by partition key
ListEntitiesOptions options = new ListEntitiesOptions()
    .setFilter("PartitionKey eq 'electronics'");

// Filter with multiple conditions
options.setFilter("PartitionKey eq 'electronics' and Price gt 100");

// Filter with comparison operators
options.setFilter("Quantity ge 10 and Quantity le 100");

// Top N results
options.setTop(10);

for (TableEntity entity : tableClient.listEntities(options, null, null)) {
    System.out.println(entity.getRowKey());
}
```

### Batch Operations (Transactions)

```java
import com.azure.data.tables.models.TableTransactionAction;
import com.azure.data.tables.models.TableTransactionActionType;
import java.util.Arrays;

// All entities must have same partition key
List<TableTransactionAction> actions = Arrays.asList(
    new TableTransactionAction(
        TableTransactionActionType.CREATE,
        new TableEntity("batch", "row1").addProperty("Name", "Item 1")),
    new TableTransactionAction(
        TableTransactionActionType.CREATE,
        new TableEntity("batch", "row2").addProperty("Name", "Item 2")),
    new TableTransactionAction(
        TableTransactionActionType.UPSERT_MERGE,
        new TableEntity("batch", "row3").addProperty("Name", "Item 3"))
);

tableClient.submitTransaction(actions);
```

### List Tables

```java
import com.azure.data.tables.models.TableItem;
import com.azure.data.tables.models.ListTablesOptions;

// List all tables
for (TableItem table : serviceClient.listTables()) {
    System.out.println(table.getName());
}

// Filter tables
ListTablesOptions options = new ListTablesOptions()
    .setFilter("TableName eq 'mytable'");

for (TableItem table : serviceClient.listTables(options, null, null)) {
    System.out.println(table.getName());
}
```

### Delete Table

```java
serviceClient.deleteTable("mytable");
```

## Typed Entities

```java
public class Product implements TableEntity {
    private String partitionKey;
    private String rowKey;
    private OffsetDateTime timestamp;
    private String eTag;
    private String name;
    private double price;
    
    // Getters and setters for all fields
    @Override
    public String getPartitionKey() { return partitionKey; }
    @Override
    public void setPartitionKey(String partitionKey) { this.partitionKey = partitionKey; }
    @Override
    public String getRowKey() { return rowKey; }
    @Override
    public void setRowKey(String rowKey) { this.rowKey = rowKey; }
    // ... other getters/setters
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
}

// Usage
Product product = new Product();
product.setPartitionKey("electronics");
product.setRowKey("laptop-001");
product.setName("Laptop");
product.setPrice(999.99);

tableClient.createEntity(product);
```

## Error Handling

```java
import com.azure.data.tables.models.TableServiceException;

try {
    tableClient.createEntity(entity);
} catch (TableServiceException e) {
    System.out.println("Status: " + e.getResponse().getStatusCode());
    System.out.println("Error: " + e.getMessage());
    // 409 = Conflict (entity exists)
    // 404 = Not Found
}
```

## Environment Variables

```bash
# Storage Account
AZURE_TABLES_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_TABLES_ENDPOINT=https://<account>.table.core.windows.net

# Cosmos DB Table API
COSMOS_TABLE_ENDPOINT=https://<account>.table.cosmosdb.azure.com
```

## Best Practices

1. **Partition Key Design**: Choose keys that distribute load evenly
2. **Batch Operations**: Use transactions for atomic multi-entity updates
3. **Query Optimization**: Always filter by PartitionKey when possible
4. **Select Projection**: Only select needed properties for performance
5. **Entity Size**: Keep entities under 1MB (Storage) or 2MB (Cosmos)

## Trigger Phrases

- "Azure Tables Java"
- "table storage SDK"
- "Cosmos DB Table API"
- "NoSQL key-value storage"
- "partition key row key"
- "table entity CRUD"

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Tables SDK for Python

NoSQL key-value store for structured data (Azure Storage Tables or Cosmos DB Table API).

## Installation

```bash
pip install azure-data-tables azure-identity
```

## Environment Variables

```bash
# Azure Storage Tables
AZURE_STORAGE_ACCOUNT_URL=https://<account>.table.core.windows.net

# Cosmos DB Table API
COSMOS_TABLE_ENDPOINT=https://<account>.table.cosmos.azure.com
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient, TableClient

credential = DefaultAzureCredential()
endpoint = "https://<account>.table.core.windows.net"

# Service client (manage tables)
service_client = TableServiceClient(endpoint=endpoint, credential=credential)

# Table client (work with entities)
table_client = TableClient(endpoint=endpoint, table_name="mytable", credential=credential)
```

## Client Types

| Client | Purpose |
|--------|---------|
| `TableServiceClient` | Create/delete tables, list tables |
| `TableClient` | Entity CRUD, queries |

## Table Operations

```python
# Create table
service_client.create_table("mytable")

# Create if not exists
service_client.create_table_if_not_exists("mytable")

# Delete table
service_client.delete_table("mytable")

# List tables
for table in service_client.list_tables():
    print(table.name)

# Get table client
table_client = service_client.get_table_client("mytable")
```

## Entity Operations

**Important**: Every entity requires `PartitionKey` and `RowKey` (together form unique ID).

### Create Entity

```python
entity = {
    "PartitionKey": "sales",
    "RowKey": "order-001",
    "product": "Widget",
    "quantity": 5,
    "price": 9.99,
    "shipped": False
}

# Create (fails if exists)
table_client.create_entity(entity=entity)

# Upsert (create or replace)
table_client.upsert_entity(entity=entity)
```

### Get Entity

```python
# Get by key (fastest)
entity = table_client.get_entity(
    partition_key="sales",
    row_key="order-001"
)
print(f"Product: {entity['product']}")
```

### Update Entity

```python
# Replace entire entity
entity["quantity"] = 10
table_client.update_entity(entity=entity, mode="replace")

# Merge (update specific fields only)
update = {
    "PartitionKey": "sales",
    "RowKey": "order-001",
    "shipped": True
}
table_client.update_entity(entity=update, mode="merge")
```

### Delete Entity

```python
table_client.delete_entity(
    partition_key="sales",
    row_key="order-001"
)
```

## Query Entities

### Query Within Partition

```python
# Query by partition (efficient)
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales'"
)
for entity in entities:
    print(entity)
```

### Query with Filters

```python
# Filter by properties
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales' and quantity gt 3"
)

# With parameters (safer)
entities = table_client.query_entities(
    query_filter="PartitionKey eq @pk and price lt @max_price",
    parameters={"pk": "sales", "max_price": 50.0}
)
```

### Select Specific Properties

```python
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'sales'",
    select=["RowKey", "product", "price"]
)
```

### List All Entities

```python
# List all (cross-partition - use sparingly)
for entity in table_client.list_entities():
    print(entity)
```

## Batch Operations

```python
from azure.data.tables import TableTransactionError

# Batch operations (same partition only!)
operations = [
    ("create", {"PartitionKey": "batch", "RowKey": "1", "data": "first"}),
    ("create", {"PartitionKey": "batch", "RowKey": "2", "data": "second"}),
    ("upsert", {"PartitionKey": "batch", "RowKey": "3", "data": "third"}),
]

try:
    table_client.submit_transaction(operations)
except TableTransactionError as e:
    print(f"Transaction failed: {e}")
```

## Async Client

```python
from azure.data.tables.aio import TableServiceClient, TableClient
from azure.identity.aio import DefaultAzureCredential

async def table_operations():
    credential = DefaultAzureCredential()
    
    async with TableClient(
        endpoint="https://<account>.table.core.windows.net",
        table_name="mytable",
        credential=credential
    ) as client:
        # Create
        await client.create_entity(entity={
            "PartitionKey": "async",
            "RowKey": "1",
            "data": "test"
        })
        
        # Query
        async for entity in client.query_entities("PartitionKey eq 'async'"):
            print(entity)

import asyncio
asyncio.run(table_operations())
```

## Data Types

| Python Type | Table Storage Type |
|-------------|-------------------|
| `str` | String |
| `int` | Int64 |
| `float` | Double |
| `bool` | Boolean |
| `datetime` | DateTime |
| `bytes` | Binary |
| `UUID` | Guid |

## Best Practices

1. **Design partition keys** for query patterns and even distribution
2. **Query within partitions** whenever possible (cross-partition is expensive)
3. **Use batch operations** for multiple entities in same partition
4. **Use `upsert_entity`** for idempotent writes
5. **Use parameterized queries** to prevent injection
6. **Keep entities small** — max 1MB per entity
7. **Use async client** for high-throughput scenarios

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---
