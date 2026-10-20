---
name: crud-completeness
description: Use when implementing complete CRUD operations, including Create, Read, Update, Delete patterns with proper validation, error handling, and business logic. Includes soft delete, restore, bulk operations, and CRUD best practices. Based on enterprise application patterns and API design standards.
license: MIT
---

# CRUD Completeness Skill — Tech Lead

## Overview

This skill provides comprehensive guidance for implementing complete CRUD (Create, Read, Update, Delete) operations. It covers validation, error handling, soft delete, restore, bulk operations, and CRUD best practices following enterprise application patterns and API design standards.

## When to Use

**Use this skill when:**

- Implementing complete CRUD operations for resources
- Designing Create, Read, Update, Delete endpoints
- Adding validation to CRUD operations
- Implementing error handling for CRUD
- Designing soft delete patterns
- Implementing restore functionality
- Creating bulk CRUD operations
- Adding optimistic concurrency control
- Implementing CRUD permissions
- Designing CRUD API documentation
- Adding audit logging to CRUD
- Implementing CRUD caching strategies
- Creating CRUD validation schemas
- Designing CRUD response formats
- Implementing CRUD rate limiting
- Adding CRUD metrics and monitoring
- Designing CRUD security controls
- Implementing CRUD data validation
- Creating CRUD input validation
- Adding CRUD output formatting
- Designing CRUD pagination
- Implementing CRUD filtering
- Adding CRUD sorting

**Do NOT use this skill when:**

- Writing application business logic (use domain-driven skill)
- Designing database schemas (use database-design skill)
- Writing API endpoint specifications (use api-design skill)
- Performing security audits (use security-auditor skill)
- Writing SQL queries (use sql-best-practices skill)
- Designing multi-page website layouts (use design-system skill)
- Analyzing deployment configurations (use deployment skill)
- Writing documentation (use documentation-best-practices skill)

## CRUD Operations

### Complete CRUD Endpoint Set

```
┌─────────────────────────────────────────────────────────────┐
│              Complete CRUD Endpoints                        │
├─────────────────────────────────────────────────────────────┤
│  CREATE:  POST   /api/v1/resources                         │
│  READ:    GET    /api/v1/resources                         │
│  READ:    GET    /api/v1/resources/:id                     │
│  UPDATE:  PATCH  /api/v1/resources/:id                     │
│  REPLACE: PUT    /api/v1/resources/:id                     │
│  DELETE:  DELETE /api/v1/resources/:id                     │
│  RESTORE: POST   /api/v1/resources/:id/restore             │
│  BULK:    POST   /api/v1/resources/bulk                    │
│  BULK:    PATCH  /api/v1/resources/bulk                    │
│  BULK:    DELETE /api/v1/resources/bulk                    │
└─────────────────────────────────────────────────────────────┘
```

### CRUD Request/Response Patterns

```
┌─────────────────────────────────────────────────────────────┐
│              CRUD Request/Response                          │
├─────────────────────────────────────────────────────────────┤
│  CREATE                                                     │
│  POST /api/v1/resources                                     │
│  Request:  { name, description, ... }                       │
│  Response: 201 { data: resource, meta: { requestId } }      │
│                                                              │
│  READ (List)                                                │
│  GET /api/v1/resources?filter[status]=active&sort=-createdAt│
│  Response: 200 { data: [...], pagination: {...} }           │
│                                                              │
│  READ (Detail)                                              │
│  GET /api/v1/resources/:id?include=related                  │
│  Response: 200 { data: resource, included: [...] }          │
│                                                              │
│  UPDATE                                                     │
│  PATCH /api/v1/resources/:id                                │
│  Request:  { name: "Updated" }                              │
│  Response: 200 { data: resource }                           │
│                                                              │
│  DELETE (Soft)                                              │
│  DELETE /api/v1/resources/:id                               │
│  Response: 200 { data: { deleted: true } }                  │
│                                                              │
│  RESTORE                                                    │
│  POST /api/v1/resources/:id/restore                         │
│  Response: 200 { data: resource }                           │
└─────────────────────────────────────────────────────────────┘
```

## Validation Patterns

### CRUD Validation Schema

```typescript
// Create validation
const createSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(1000).optional(),
  status: z.enum(['active', 'inactive', 'pending']).default('pending'),
  priority: z.number().int().min(1).max(5).optional(),
  tags: z.array(z.string()).max(10).optional(),
});

// Update validation
const updateSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  description: z.string().max(1000).optional(),
  status: z.enum(['active', 'inactive', 'pending']).optional(),
  priority: z.number().int().min(1).max(5).optional(),
  tags: z.array(z.string()).max(10).optional(),
});
```

### Validation Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "name",
        "message": "Name must be between 1 and 100 characters"
      },
      {
        "field": "priority",
        "message": "Priority must be between 1 and 5"
      }
    ]
  },
  "meta": {
    "requestId": "req_123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Soft Delete Pattern

### Soft Delete Implementation

```typescript
// Database schema
interface Resource {
  id: string;
  name: string;
  description?: string;
  status: 'active' | 'inactive' | 'deleted';
  deletedAt?: Date;
  deletedBy?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Soft delete query
const softDelete = async (id: string, userId: string) => {
  return await db.resource.update({
    where: { id },
    data: {
      status: 'deleted',
      deletedAt: new Date(),
      deletedBy: userId,
    },
  });
};

// Restore query
const restore = async (id: string) => {
  return await db.resource.update({
    where: { id },
    data: {
      status: 'active',
      deletedAt: null,
      deletedBy: null,
    },
  });
};

// Soft delete scope
const activeResources = async () => {
  return await db.resource.findMany({
    where: { status: 'active' },
  });
};
```

### Soft Delete API

```
┌─────────────────────────────────────────────────────────────┐
│              Soft Delete API                                │
├─────────────────────────────────────────────────────────────┤
│  DELETE /api/v1/resources/:id                               │
│  └── Status: 200                                            │
│  └── Body: { data: { deleted: true } }                      │
│                                                              │
│  POST /api/v1/resources/:id/restore                         │
│  └── Status: 200                                            │
│  └── Body: { data: resource }                               │
│                                                              │
│  GET /api/v1/resources?include=deleted                      │
│  └── Status: 200                                            │
│  └── Body: { data: [...], includes: [...] }                 │
│                                                              │
│  DELETE /api/v1/resources/:id/force                         │
│  └── Status: 204 (No Content)                               │
│  └── Permanently deletes record                             │
└─────────────────────────────────────────────────────────────┘
```

## Bulk Operations

### Bulk CRUD Pattern

```typescript
// Bulk create
POST /api/v1/resources/bulk
Body: { resources: [{ name: "Item 1" }, { name: "Item 2" }] }
Response: 201 { data: [resource1, resource2] }

// Bulk update
PATCH /api/v1/resources/bulk
Body: { resources: [{ id: "1", name: "Updated 1" }] }
Response: 200 { data: [resource1] }

// Bulk delete
DELETE /api/v1/resources/bulk
Body: { ids: ["1", "2", "3"] }
Response: 200 { data: { deleted: 3 } }
```

## Error Handling

### CRUD Error Codes

```
┌─────────────────────────────────────────────────────────────┐
│              CRUD Error Codes                               │
├─────────────────────────────────────────────────────────────┤
│  CREATE                                                     │
│  └── 400: Validation error                                  │
│  └── 401: Unauthorized                                      │
│  └── 403: Forbidden                                         │
│  └── 409: Duplicate resource                                │
│                                                              │
│  READ                                                       │
│  └── 401: Unauthorized                                      │
│  └── 403: Forbidden                                         │
│  └── 404: Resource not found                                │
│                                                              │
│  UPDATE                                                     │
│  └── 400: Validation error                                  │
│  └── 401: Unauthorized                                      │
│  └── 403: Forbidden                                         │
│  └── 404: Resource not found                                │
│  └── 409: Conflict (version mismatch)                       │
│                                                              │
│  DELETE                                                     │
│  └── 401: Unauthorized                                      │
│  └── 403: Forbidden                                         │
│  └── 404: Resource not found                                │
│  └── 409: Conflict (dependency exists)                      │
└─────────────────────────────────────────────────────────────┘
```

## Optimistic Concurrency

### ETag Pattern

```typescript
// GET returns ETag
Response Headers:
ETag: "abc123"

// UPDATE includes If-Match
Request Headers:
If-Match: "abc123"

// Response for conflict
Status: 409 Conflict
Body: {
  error: {
    code: "CONFLICT",
    message: "Resource was modified by another user"
  }
}
```

## Real-World Impact

**Before this skill:**

- Incomplete CRUD operations
- Missing validation
- Poor error handling
- No soft delete
- Inconsistent API

**After this skill:**

- Complete CRUD operations
- Proper validation and error handling
- Soft delete with restore
- Consistent API patterns

## Cross-References

- **`api-design`** - For API endpoint specifications
- **`database-design`** - For database schema design
- **`security-auditor`** - For CRUD security review

## References

- [RESTful API Design Best Practices](https://restfulapi.net/)
- [API Security Checklist](https://owasp.org/www-project-api-security/)
- [Soft Delete Pattern](https://martinfowler.com/eaaCatalog/softDelete.html)
- [Optimistic Concurrency](https://martinfowler.com/eaaCatalog/optimisticOfflineLock.html)
