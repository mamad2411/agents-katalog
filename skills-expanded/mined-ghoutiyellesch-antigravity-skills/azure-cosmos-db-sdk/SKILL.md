---
name: azure-cosmos-db-sdk
description: Consolidated Azure Cosmos DB SDK skill for data plane and management operations across Python, Java, Rust, TypeScript, and .NET.
allowed-tools: Read Write Edit Glob Grep Bash WebSearch WebFetch
---

# Azure Cosmos DB SDK (Multi-Language)

This consolidated skill covers Azure Cosmos DB operations across all major languages (Python, Java, Rust, TypeScript, .NET).

## Core Concepts

- **Data Plane SDKs**: Used for CRUD operations on documents, queries, bulk operations, and container management.
- **Management Plane SDKs** (Resource Manager): Used to create accounts, databases, and containers via ARM templates or management APIs.
- **Authentication**: Always prefer Azure Active Directory (AAD) via `DefaultAzureCredential` from the `azure-identity` package over connection strings or account keys.

## Cross-Language Best Practices

1. **Authentication**: Use `DefaultAzureCredential` across all languages.
2. **Parameterized Queries**: Always use parameterized queries (e.g., `SELECT * FROM c WHERE c.partitionKey = @category`) to prevent SQL injection and improve plan caching.
3. **Partition Keys**: Always specify partition keys in your queries to avoid inefficient cross-partition queries.
4. **Bulk Operations**: For multiple writes, use bulk execution modes/methods available in your language SDK.
5. **Rate Limiting (429 Errors)**: Implement retry logic with exponential backoff for 429 "Too Many Requests" errors. Most SDKs have this built-in but configure it appropriately.
6. **Optimistic Concurrency**: Use `ETags` to handle concurrent updates and prevent lost updates (`IfMatch` condition).

## Language-Specific Package References

### TypeScript / Node.js
- **Install**: `npm install @azure/cosmos @azure/identity`
- **Key Classes**: `CosmosClient`, `Database`, `Container`, `Item`

### Python
- **Install**: `pip install azure-cosmos azure-identity`
- **Key Classes**: `CosmosClient`, `DatabaseProxy`, `ContainerProxy`

### Java
- **Install**: `com.azure:azure-cosmos`, `com.azure:azure-identity`
- **Key Classes**: `CosmosClient`, `CosmosDatabase`, `CosmosContainer`

### .NET (C#)
- **Install**: `Azure.Data.Cosmos` or `Microsoft.Azure.Cosmos`
- **Key Classes**: `CosmosClient`, `Database`, `Container`

### Rust
- **Install**: `azure_data_cosmos`
- **Key Classes**: `CosmosClient`, `DatabaseClient`, `CollectionClient`

## Example Usage (Conceptual)

When a user asks to write Cosmos DB code in any of these languages:
1. Import the specific Cosmos package and the `identity` package.
2. Initialize the client using `DefaultAzureCredential`.
3. Fetch the database and container clients.
4. Perform the CRUD or Query operation using standard NoSQL syntax.
