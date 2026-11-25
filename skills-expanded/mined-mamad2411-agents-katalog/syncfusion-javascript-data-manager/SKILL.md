---
name: syncfusion-javascript-data-manager
description: Implements Syncfusion TypeScript/JavaScript(ES6+) DataManager for local/remote binding, CRUD, querying, caching, and middleware. Supports JsonAdaptor, ODataAdaptor, ODataV4Adaptor, UrlAdaptor, WebApiAdaptor, WebMethodAdaptor, RemoteSaveAdaptor, GraphQLAdaptor, CustomDataAdaptor, and CustomAdaptor. Covers Query class, filtering, sorting, paging, grouping, persistence, offline mode, caching, and error handling.

metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "DataManager"
---

# DataManager for TypeScript/JavaScript - Complete Guide

## Table of Contents

- [Key Concepts](#key-concepts)
- [10 Adaptors Reference](#10-adaptors-reference)
- [Navigation Guide](#navigation-guide)
- [Quick Start](#quick-start)
- [Common Error Handling](#common-error-handling)

---


## ⚠️ Security & Trust Boundary

- This skill generates code only, the agent does not execute data operations or fetch remote endpoints — all DataManager interactions occur solely within the user's application at runtime.
- Generated code must treat all third-party API responses as untrusted input, never bind to unvalidated or user-provided URLs, and ensure authentication is enforced on all remote endpoints.

---

## Key Concepts

### 10 Adaptor Types (Decision Guide)

| Scenario | Adaptor | When to Use |
|----------|---------|------------|
| **Local arrays** | JsonAdaptor | In-memory JavaScript arrays, no server needed |
| **ASP.NET Web API** | WebApiAdaptor | ASP.NET backend returning Items/Count format |
| **Generic REST** | UrlAdaptor | Standard REST APIs with result/count format |
| **Client + Server** | RemoteSaveAdaptor | Client-side filtering, server-side CRUD |
| **OData v3** | ODataAdaptor | Legacy OData v3 services |
| **OData v4** | ODataV4Adaptor | Modern OData v4 with expand relations |
| **Legacy ASP.NET** | WebMethodAdaptor | ASMX web methods (deprecated) |
| **GraphQL** | GraphQLAdaptor | GraphQL endpoints |
| **Custom Format** | Custom DataAdaptor | Non-standard API response formats |
| **Full Control** | CustomAdaptor | Complete adaptor override |

### Data Binding Types

```
Local Binding
├─ Direct array: new DataManager({ json: data })
├─ JsonAdaptor explicit
└─ Client-side filtering instant

Remote Binding
├─ WebApiAdaptor: ASP.NET specific
├─ UrlAdaptor: Generic REST
├─ ODataAdaptor/V4: Protocol-based
└─ Server processes Query object
```

### Query Operations

```typescript
// Filter/Search
.where('field', 'operator', value)     // Single condition
.where(predicate)                        // Complex predicate

// Sort/Order
.sortBy('field')                         // Ascending
.sortByDescending('field')               // Descending
.orderBy('field')                        // Alias

// Pagination
.take(10)                                // Limit records
.skip(0)                                 // Offset

// Projection
.select(['field1', 'field2'])            // Column selection

// Relationships
.expand('relatedTable')                  // OData expand

// Grouping & Aggregation
.group('field')                          // Group by
.aggregate('sum', 'field')               // Calculate
```

---

## 10 Adaptors Reference

### Decision Tree: Which Adaptor?

```
Does your data come from?
│
├─ JavaScript array in memory?
│  └─ JsonAdaptor
│
├─ Web Server / REST API?
│  ├─ ASP.NET Web API (backend specific)?
│  │  └─ WebApiAdaptor (Items/Count format)
│  ├─ Generic REST endpoint?
│  │  └─ UrlAdaptor (result/count format)
│  ├─ Need offline with server-side CRUD?
│  │  └─ RemoteSaveAdaptor
│  └─ Custom format (non-standard)?
│     └─ CustomDataAdaptor
│
├─ OData Service?
│  ├─ OData v3 (legacy)?
│  │  └─ ODataAdaptor
│  └─ OData v4 (modern)?
│     └─ ODataV4Adaptor (with expand)
│
├─ GraphQL Endpoint?
│  └─ GraphQLAdaptor
│
├─ Legacy ASP.NET ASMX?
│  └─ WebMethodAdaptor
│
└─ Custom/Proprietary?
   ├─ Custom request/response format?
   │  └─ CustomDataAdaptor
   └─ Need complete adaptor override?
      └─ CustomAdaptor
```

---

## Documentation Navigation Guide

### 📄 Getting Started & Setup
**Read:** [Getting Started](references/getting-started.md)
- Installation (@syncfusion/ej2-data)
- Browser requirements
- First DataManager example
- Local array binding
- Remote API binding

### 📄 Understand the Concepts
**Read:** [Overview](references/overview.md)
- What is DataManager?
- Key features
- When to use DataManager
- Architecture

### 📄 Data Binding (Local & Remote)
**Read:** [Data Binding](references/data-binding.md)
- Local arrays with JsonAdaptor
- Remote APIs (REST, OData)
- Error handling (HTTP 0, 400, 401, 404, 500)
- Promise patterns (.then/.catch)
- Async/await examples
- Loading states

### 📄 Build Complex Queries
**Read:** [Querying](references/querying.md)
- from() - specify resource
- where() - 15+ filter operators (equal, contains, startswith, greaterThan, etc.)
- select() - column projection
- orderBy/sortBy - multiple sort columns
- take/skip - pagination
- group() - data grouping
- aggregate() - sum, avg, count, min, max
- Complex predicate-based filtering

### 📄 CRUD: Insert, Update, Delete
**Read:** [CRUD Operations](references/crud-operations.md)
- insert() - single & batch records
- update() & remove() with keyField parameter
- remove() - delete by ID
- saveChanges() - batch mixed operations
- Error handling & validation
- Response formats (Items/Count, result/count)
- Conflict resolution

### 📄 All 10 Adaptors Explained
**Read:** [Adaptors Guide](references/adaptors-guide.md)
- Complete adaptor decision tree
- Each adaptor with:
  * When to use
  * Configuration example
  * Usage example
  * Backend response format
  * C# or JavaScript backend patterns
- Comparison matrix
- CORS configuration

### 📄 Middleware & Request Customization
**Read:** [Applying Middleware Logic](references/applying-middleware-logic.md)
- Pre-request middleware (add headers, tokens)
- Post-request middleware (transform responses)
- JWT authentication patterns
- Custom headers (static & dynamic)
- Request/response transformation
- Error handling with retry
- Middleware execution order

### 📄 Browser State Persistence
**Read:** [State Persistence](references/dataManager-persistence.md)
- enablePersistence - save query state
- localStorage integration
- Excluding specific queries from persistence
- Reapplying saved state on reload

### 📄 Advanced Scenarios & Optimization
**Read:** [Advanced Scenarios](references/advanced-scenarios.md)
- Offline mode (download once, filter client-side)
- Load-on-demand pagination
- Deferred execution (Promises)
- Async/await patterns
- Memory management
- Performance optimization
- Troubleshooting

### 📄 API References
**Read:** [API - DataManager](references/api-dataManager.md)
- executeQuery() method
- executeLocal() method
- insert(), update(), remove()
- saveChanges() for batch operations

**Read:** [API - Query](references/api-query.md)
- All Query builder methods
- where(), select(), from(), group()
- take(), skip(), orderBy()
- aggregate(), expand()

**Read:** [API - Deferred](references/api-deferred.md)
- Promise-based async handling
- then(), catch(), finally()
- Error callbacks

---

## Quick Start

### Setup

```typescript
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url/orders',
  adaptor: new WebApiAdaptor()
});
```

### Query Example

```typescript
// Fetch with filtering & sorting
dataManager.executeQuery(
  new Query()
    .where('Freight', 'greaterThan', 30)
    .sortByDescending('OrderDate')
    .take(20)
).then((result) => {
  console.log('Orders:', result.result);
  console.log('Total:', result.count);
}).catch((error) => {
  console.error('Error:', error);
});
```

### CRUD Operations

```typescript
// Insert (data first, then tableName)
await dataManager.insert({ CustomerID: 'VINET', Freight: 32.50 }, 'Orders');

// Update (keyField, value object, tableName)
await dataManager.update('OrderID', 
  { OrderID: 10248, Freight: 45.50 }, 
  'Orders'
);

// Delete (keyField, keyValue, tableName)
await dataManager.remove('OrderID', 10248, 'Orders');
```

---

## Common Error Handling

### HTTP Status Codes

| Status | Meaning | Solution |
|--------|---------|----------|
| 0 | Network error | Check internet connection |
| 400 | Bad request | Verify data format |
| 401 | Unauthorized | Check authentication token |
| 403 | Forbidden | Verify permissions |
| 404 | Not found | Check endpoint URL |
| 409 | Conflict | Data already exists, refresh data |
| 500 | Server error | Check backend logs |

### Error Handling Pattern

```typescript
// Promise-based
dataManager.executeQuery(new Query())
  .then((result) => {
    // Success: result.result, result.count
  })
  .catch((error) => {
    if (error.status === 401) {
      console.error('Unauthorized - login required');
    } else if (error.status === 500) {
      console.error('Server error');
    } else {
      console.error('Error:', error.message);
    }
  });

// Async/Await
try {
  const result = await dataManager.executeQuery(new Query());
  console.log('Data:', result.result);
} catch (error) {
  console.error('Error status:', error.status);
}
```

---

## 10 Key Properties

```typescript
const config = {
  url: 'api.example.com/orders',        // Remote endpoint
  json: localArray,                              // Local data array
  adaptor: new WebApiAdaptor(),                 // Protocol handler
  
  // Caching & Performance
  enableCache: true,                            // Enable result caching
  timeTillExpiration: 10 * 60 * 1000,          // Cache TTL (10 mins, default: no expiry)
  
  // Persistence
  enablePersistence: true,                      // Enable state persistence
  id: 'dataManager_1',                          // Persistence ID
  ignoreOnPersist: ['temp', 'debug'],          // Properties to exclude
  // HTTP headers
  crossDomain: true,                            // CORS enabled
  offline: false,                               // Offline mode
  timeZoneHandling: true                        // Timezone offset handling
};
```

---

## Framework Variants

### TypeScript

```typescript
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

const dm = new DataManager({
  url: 'api.example.com/orders',
  adaptor: new WebApiAdaptor()
});

dm.executeQuery(new Query().take(10)).then((result) => {
  console.log(result.result);
});
```

### JavaScript (ES6)

```javascript
const { DataManager, WebApiAdaptor, Query } = require('@syncfusion/ej2-data');

const dm = new DataManager({
  url: 'api.example.com/orders',
  adaptor: new WebApiAdaptor()
});

dm.executeQuery(new Query().take(10)).then((result) => {
  console.log(result.result);
});
```

---
