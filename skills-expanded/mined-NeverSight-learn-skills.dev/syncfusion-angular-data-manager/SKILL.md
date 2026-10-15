---
name: syncfusion-angular-data-manager
description: Implements Syncfusion Angular DataManager for local/remote binding, CRUD, querying, caching, and middleware. Supports JsonAdaptor, ODataAdaptor, ODataV4Adaptor, UrlAdaptor, WebApiAdaptor, WebMethodAdaptor, RemoteSaveAdaptor, GraphQLAdaptor, CustomDataAdaptor, and CustomAdaptor. Covers Query class, filtering, sorting, paging, grouping, persistence, offline mode, caching, and error handling.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Management"
---

# Syncfusion Angular DataManager

## When to Use This Skill

**Use this skill when you need to:**
- Bind local JSON arrays to Angular components
- Connect Angular apps to remote REST, OData, or GraphQL services
- Implement querying, filtering, sorting, and paging on data
- Perform CRUD operations (Create, Read, Update, Delete) with data persistence
- Work offline and sync data when reconnected
- Transform and filter data using Query class
- Customize data communication with middleware
- Cache data to reduce server requests
- Handle different data source protocols automatically

**This is your primary reference for:**
- Any data operation in Syncfusion Angular components
- Universal data binding across all components
- Data source configuration and selection
- Async operations and error handling
- Performance optimization with caching

---

## Component Overview

The **DataManager** is Syncfusion's universal data management module that acts as a bridge between your Angular application and any data source. It provides:

- **10 Built-in Adaptors** — Support for JSON, OData v3/v4, REST, Web API, Web Methods, GraphQL, and custom sources
- **Query Class** — Powerful filtering, sorting, grouping, and paging API
- **CRUD Operations** — Insert, update, delete with automatic handling
- **Promise-based Async** — Native JavaScript Promise support
- **Middleware Customization** — Pre/post request hooks for authentication and transformation
- **Offline Support** — Work without server connection, sync when online
- **Caching** — Reduce server load and improve performance
- **Type Safety** — Full TypeScript definitions

---

## ⚠️ Security & Trust Boundary

- This skill generates code only, the agent does not execute data operations or fetch remote endpoints — all DataManager interactions occur solely within the user's application at runtime.
- Generated code must treat all third-party API responses as untrusted input, never bind to unvalidated or user-provided URLs, and ensure authentication is enforced on all remote endpoints.

---

## Key Concepts & Trigger Keywords

| Concept | When to Use | Key Methods |
|---------|------------|------------|
| **Local Data Binding** | Working with in-memory JSON arrays | JsonAdaptor, executeLocal |
| **Remote Data Binding** | Calling API endpoints for data | UrlAdaptor, WebApiAdaptor, executeQuery |
| **Query Construction** | Filtering, sorting, grouping data | from(), where(), select(), sortBy(), take() |
| **CRUD Operations** | Managing records (add, edit, delete) | insert(), update(), remove(), saveChanges() |
| **Adaptor Selection** | Choosing the right data source type | 10 adaptors with decision tree |
| **Error Handling** | Managing failure scenarios | .catch(), try/catch, error status checking |
| **Offline Mode** | Working without server connection | offline property, localStorage |
| **Caching** | Improving performance | enableCache, cache clearing strategies |
| **Middleware** | Customizing requests/responses | applyPreRequestMiddlewares, applyPostMiddlewares |
| **Async Patterns** | Sequential and parallel operations | async/await, Promise.all(), then/catch |

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** Starting new DataManager implementation, understanding package setup, learning TypeScript imports, configuring your first DataManager instance

**Topics covered:**
- Package installation and dependencies
- Module imports and TypeScript types
- Creating DataManager instances
- Difference between executeLocal and executeQuery
- Basic query execution patterns

---

### Data Binding - Local and Remote
📄 **Read:** [references/data-binding.md](references/data-binding.md)

**When to read:** Deciding between client-side and server-side processing, implementing local JSON binding, connecting to remote APIs, understanding executeLocal vs executeQuery patterns

**Topics covered:**
- Local binding with json property
- Remote binding with url + adaptor
- Client-side vs server-side processing
- Promise-based async patterns
- Basic error handling

---

### Querying and Filtering
📄 **Read:** [references/querying-and-filtering.md](references/querying-and-filtering.md)

**When to read:** Building queries, filtering by multiple conditions, sorting results, searching data, pagination, grouping records, advanced predicates

**Topics covered:**
- Query class fundamentals
- from() and select() methods
- where() with operators and predicates
- sortBy(), orderBy(), orderByDescending()
- take(), skip() for pagination
- search() method
- Grouping and aggregation

---

### CRUD Operations
📄 **Read:** [references/crud-operations.md](references/crud-operations.md)

**When to read:** Adding new records, updating existing data, deleting records, batch operations, CRUD method parameters, persisting changes to server

**Topics covered:**
- Insert (add new records)
- Update (modify existing records)
- Remove (delete records)
- keyField in CRUD method parameters
- saveChanges() for batch operations
- Error handling and validation

---

### 10 Adaptors Guide - Complete Reference
📄 **Read:** [references/adaptors-guide.md](references/adaptors-guide.md)

**When to read:** Selecting appropriate data source, understanding adaptor differences, implementing specific adaptor patterns, working with different API types

**Topics covered:**
- **JsonAdaptor** — Local JavaScript arrays, no server calls
- **ODataAdaptor** — OData v3 service endpoints
- **ODataV4Adaptor** — OData v4 protocol support
- **UrlAdaptor** — Generic RESTful API endpoints
- **WebApiAdaptor** — ASP.NET Web API integration
- **WebMethodAdaptor** — ASP.NET Web Methods
- **RemoteSaveAdaptor** — Client-side queries + server-side CRUD
- **GraphQLAdaptor** — GraphQL query language support
- **CustomDataAdaptor** — Custom request/response handling
- **CustomAdaptor** — Extending built-in adaptors
- Adaptor decision tree
- Comparison matrix for all 10
- Code examples for each adaptor

---

### Middleware Customization
📄 **Read:** [references/middleware-customization.md](references/middleware-customization.md)

**When to read:** Adding authentication headers, transforming requests/responses, logging API calls, implementing custom business logic

**Topics covered:**
- Pre-request middleware (applyPreRequestMiddlewares)
- Post-request middleware (applyPostMiddlewares)
- Custom headers (Authorization, etc.)
- Authentication patterns (Bearer tokens)
- Request/response transformation
- Error handling in middleware

---

### Caching and Offline Mode
📄 **Read:** [references/caching-offline-mode.md](references/caching-offline-mode.md)

**When to read:** Improving performance with caching, working offline when server unavailable, implementing sync strategies, managing data persistence

**Topics covered:**
- Offline property configuration
- localStorage for data persistence
- Cache auto-clearing on CRUD
- Manual cache management
- Online/offline workflow
- Sync strategies

---

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

**When to read:** Load on demand for large datasets, lazy loading relationships, pagination strategies, deferred operations, async/await patterns, memory management, state persistence

**Topics covered:**
- Load on demand pattern
- Lazy loading with expand()
- Pagination (client & server-side)
- Deferred operations with Promises
- Async/await patterns
- Promise.all() for parallel operations
- Error handling with status codes
- Memory management strategies
- Type safety with TypeScript
- State persistence patterns

---

### How-To Recipes
📄 **Read:** [references/how-to-recipes.md](references/how-to-recipes.md)

**When to read:** Quick solutions for common scenarios, best practices, troubleshooting, pattern examples

**Topics covered:**
- Work in offline mode
- Send additional parameters
- Add custom headers
- Implement authentication
- Handle errors gracefully
- Common patterns
- Performance optimization tips
- Troubleshooting guides

---

## Quick Start Example

### Setup and Basic Data Binding

**Step 1: Install Package**

```bash
npm install @syncfusion/ej2-data
```

**Step 2: Create Component**

```typescript
import { Component, OnInit } from '@angular/core';
import { DataManager, Query, JsonAdaptor, ReturnOption } from '@syncfusion/ej2-data';

@Component({
  selector: 'app-data-demo',
  templateUrl: './data-demo.component.html',
  styleUrls: ['./data-demo.component.css']
})
export class DataDemoComponent implements OnInit {
  public orders: object[];

  ngOnInit(): void {
    // Local data
    const data = [
      { OrderID: 10248, CustomerID: 'VINET', EmployeeID: 5, ShipCity: 'Reims' },
      { OrderID: 10249, CustomerID: 'TOMSP', EmployeeID: 6, ShipCity: 'Münster' },
      { OrderID: 10250, CustomerID: 'HANAR', EmployeeID: 4, ShipCity: 'Rio de Janeiro' }
    ];

    // Create DataManager with local data
    const dataManager = new DataManager({
      json: data,
      adaptor: new JsonAdaptor()
    });

    // Execute query
    this.orders = dataManager.executeLocal(
      new Query().where('EmployeeID', 'equal', 5)
    );
  }
}
```

**Step 3: Display in Template**

```html
<table>
  <thead>
    <tr>
      <th>Order ID</th>
      <th>Customer ID</th>
      <th>Employee ID</th>
      <th>Ship City</th>
    </tr>
  </thead>
  <tbody>
    <tr *ngFor="let order of orders">
      <td>{{ order.OrderID }}</td>
      <td>{{ order.CustomerID }}</td>
      <td>{{ order.EmployeeID }}</td>
      <td>{{ order.ShipCity }}</td>
    </tr>
  </tbody>
</table>
```

---

## Common Patterns

### Remote Server with Promise

```typescript
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

// Using Promise
dataManager.executeQuery(new Query().take(10))
  .then((result: ReturnOption) => {
    this.orders = result.result;
  })
  .catch((error) => {
    console.error('Failed to fetch orders:', error);
  });
```

### Async/Await Pattern

```typescript
async fetchOrders(): Promise<void> {
  try {
    const result = await this.dataManager.executeQuery(
      new Query().take(10)
    );
    this.orders = result.result;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Filtering with Predicates

```typescript
const query = new Query()
  .where('EmployeeID', 'equal', 5)
  .where('ShipCity', 'startswith', 'Rio');

const result = dataManager.executeLocal(query);
```

### Server-side Operations

```typescript
const query = new Query()
  .select(['OrderID', 'CustomerID', 'EmployeeID'])
  .where('EmployeeID', 'greaterThan', 3)
  .sortBy('OrderID')
  .take(10)
  .skip(0);

dataManager.executeQuery(query).then((result: ReturnOption) => {
  this.orders = result.result;
  this.totalRecords = result.count;
});
```

---

## Key Properties Reference

| Property | Type | Purpose |
|----------|------|---------|
| `json` | `array` | Local data array |
| `url` | `string` | Remote service endpoint |
| `adaptor` | `Adaptor` | Data source type handler |
| `headers` | `object[]` | Custom HTTP headers |
| `offline` | `boolean` | Enable offline mode |
| `enableCache` | `boolean` | Enable response caching |
| `crossDomain` | `boolean` | Enable cross-domain requests |
| `cachingPageSize` | `number` | Paging record count |
| `timeTillExpiration` | `number` | Cache TTL in milliseconds (default: infinite) |
| `ignoreOnPersist` | `string[]` | Properties to exclude from persistence |
| `timeZoneHandling` | `boolean` | Enable timezone offset handling |

---

## Error Handling Best Practices

```typescript
dataManager.executeQuery(query)
  .then((result: ReturnOption) => {
    if (result.result) {
      this.items = result.result;
    }
  })
  .catch((error: any) => {
    if (error.status === 401) {
      // Redirect to login
      console.error('Unauthorized');
    } else if (error.status === 403) {
      // Access denied
      console.error('Forbidden');
    } else if (error.status === 500) {
      // Server error
      console.error('Server error');
    } else if (error.status === 0) {
      // Network error
      console.error('Network error - check connectivity');
    }
  });
```

---

## Common Use Cases

### Use Case 1: Display Data Table
Start with [getting-started.md](references/getting-started.md) → [data-binding.md](references/data-binding.md) → [querying-and-filtering.md](references/querying-and-filtering.md)

### Use Case 2: Implement CRUD Form
Start with [adaptors-guide.md](references/adaptors-guide.md) → [crud-operations.md](references/crud-operations.md) → [advanced-features.md](references/advanced-features.md)

### Use Case 3: Work with Multiple Data Sources
Start with [adaptors-guide.md](references/adaptors-guide.md) (decision tree) → specific adaptor pattern → [middleware-customization.md](references/middleware-customization.md)

### Use Case 4: Optimize Large Datasets
Start with [advanced-features.md](references/advanced-features.md) → [caching-offline-mode.md](references/caching-offline-mode.md) → [how-to-recipes.md](references/how-to-recipes.md)

---

## TypeScript Type Safety

```typescript
// Define your data model
interface Order {
  OrderID: number;
  CustomerID: string;
  EmployeeID: number;
  ShipCity: string;
}

// Use generics for type safety
const dataManager: DataManager<Order> = new DataManager({
  json: orders,
  adaptor: new JsonAdaptor()
});

// Typed results
const result = await dataManager.executeQuery(new Query());
const typedOrders: Order[] = result.result as Order[];
```

---

## Performance Optimization Tips

1. **Use proper adaptor** — Select adaptor matching your backend
2. **Filter early** — Push filtering to server when possible
3. **Enable caching** — Reduce redundant server calls
4. **Lazy load** — Load data on demand for large datasets
5. **Pagination** — Limit records per request
6. **Offline mode** — Load once, work offline
7. **Select columns** — Fetch only needed fields

---
