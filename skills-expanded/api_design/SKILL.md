---
name: api-design
description: API design best practices for REST, GraphQL, gRPC, and WebSocket.
---

# API Design

Principles and patterns for designing great APIs.

## REST API Design

### Resource Naming
- Use nouns, not verbs: `/users` not `/getUsers`
- Plural for collections: `/users`, `/users/123`
- Nest for relationships: `/users/123/orders`
- Use kebab-case: `/order-items` not `/orderItems`

### HTTP Methods
- `GET`: Read (safe, idempotent)
- `POST`: Create (non-idempotent)
- `PUT`: Full replace (idempotent)
- `PATCH`: Partial update (non-idempotent)
- `DELETE`: Remove (idempotent)

### Status Codes
- `200`: Success
- `201`: Created
- `204`: No content
- `400`: Bad request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not found
- `409`: Conflict
- `422`: Unprocessable entity
- `429`: Too many requests
- `500`: Internal error

### Versioning
- URL: `/api/v1/users`
- Header: `Accept: application/vnd.api+json;version=1`
- Query: `?version=1`

### Pagination
- Offset: `?page=2&limit=20`
- Cursor: `?after=cursor_token&limit=20` (preferred for large datasets)
- Links: `Link` header or JSON response with next/prev URLs

## GraphQL Design
- Schema-first design
- Descriptive names and descriptions
- Input types for mutations
- Connections for list types (Relay spec)
- DataLoader for N+1 prevention
- Persisted queries for production

## gRPC Design
- Protobuf schema-first
- Use streaming for large data or real-time
- Meaningful error codes (gRPC status codes)
- Deadlines and cancellation propagation
- Interceptors for cross-cutting concerns

## WebSocket Design
- Heartbeat/ping-pong for connection health
- Reconnection logic on client
- Message framing (type, id, payload)
- Backpressure handling
- Channel/room management

## API Documentation
- OpenAPI 3.x for REST
- GraphQL SDL for GraphQL
- AsyncAPI for event-driven/WebSocket
- Include examples, error responses, auth flows
- Keep docs in sync with implementation
