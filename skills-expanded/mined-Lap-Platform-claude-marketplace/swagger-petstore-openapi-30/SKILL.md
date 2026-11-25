---
name: swagger-petstore-openapi-30
description: "Swagger Petstore - OpenAPI 3.0 API skill. Use when working with Swagger Petstore - OpenAPI 3.0 for pet, store, user. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# Swagger Petstore - OpenAPI 3.0
API version: 1.0.27

## Auth
OAuth2 | ApiKey api_key in header

## Base URL
/api/v3

## Setup
1. Set your API key in the appropriate header
2. GET /pet/findByStatus -- verify access
3. POST /pet -- create first pet

## Endpoints

19 endpoints across 3 groups. See references/api-spec.lap for full details.

### pet
| Method | Path | Description |
|--------|------|-------------|
| PUT | /pet | Update an existing pet. |
| POST | /pet | Add a new pet to the store. |
| GET | /pet/findByStatus | Finds Pets by status. |
| GET | /pet/findByTags | Finds Pets by tags. |
| GET | /pet/{petId} | Find pet by ID. |
| POST | /pet/{petId} | Updates a pet in the store with form data. |
| DELETE | /pet/{petId} | Deletes a pet. |
| POST | /pet/{petId}/uploadImage | Uploads an image. |

### store
| Method | Path | Description |
|--------|------|-------------|
| GET | /store/inventory | Returns pet inventories by status. |
| POST | /store/order | Place an order for a pet. |
| GET | /store/order/{orderId} | Find purchase order by ID. |
| DELETE | /store/order/{orderId} | Delete purchase order by identifier. |

### user
| Method | Path | Description |
|--------|------|-------------|
| POST | /user | Create user. |
| POST | /user/createWithList | Creates list of users with given input array. |
| GET | /user/login | Logs user into the system. |
| GET | /user/logout | Logs out current logged in user session. |
| GET | /user/{username} | Get user by user name. |
| PUT | /user/{username} | Update user resource. |
| DELETE | /user/{username} | Delete user resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a pet?" -> POST /pet
- "List all findByStatus?" -> GET /pet/findByStatus
- "List all findByTags?" -> GET /pet/findByTags
- "Get pet details?" -> GET /pet/{petId}
- "Delete a pet?" -> DELETE /pet/{petId}
- "Create a uploadImage?" -> POST /pet/{petId}/uploadImage
- "List all inventory?" -> GET /store/inventory
- "Create a order?" -> POST /store/order
- "Get order details?" -> GET /store/order/{orderId}
- "Delete a order?" -> DELETE /store/order/{orderId}
- "Create a user?" -> POST /user
- "Create a createWithList?" -> POST /user/createWithList
- "List all login?" -> GET /user/login
- "List all logout?" -> GET /user/logout
- "Get user details?" -> GET /user/{username}
- "Update a user?" -> PUT /user/{username}
- "Delete a user?" -> DELETE /user/{username}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
