---
name: gateway-rest-api
description: "Gateway REST API skill. Use when working with Gateway REST for tyk. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# Gateway REST API
API version: 1.9

## Auth
ApiKey keyId in path

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /tyk/keys/ -- verify access
3. POST /tyk/keys/create -- create first create

## Endpoints

18 endpoints across 1 groups. See references/api-spec.lap for full details.

### tyk
| Method | Path | Description |
|--------|------|-------------|
| GET | /tyk/keys/ | Gets a list of *key* IDs (will only work with non-hashed installations) |
| POST | /tyk/keys/create | Create a new *API token* with the *session object* defined in the body |
| PUT | /tyk/keys/{keyId} | Update an *API token* with the *session object* defined in the body, this operatin overwrites the existing object |
| POST | /tyk/keys/{keyId} | Add a pre-specified *API token* with the *session object* defined in the body, this operatin creates a custom token that dsoes not use the gateway naming convention for tokens |
| DELETE | /tyk/keys/{keyId} | Remove this *API token* from the gateway, this will completely destroy the token and metadata associated with the token and instantly stop access from being granted |
| GET | /tyk/apis/ | Gets a list of *API Definition* objects that are currently live on the gateway |
| POST | /tyk/apis/ | Create an *API Definition* object |
| GET | /tyk/apis/{apiID} | Gets an *API Definition* object, if it exists |
| DELETE | /tyk/apis/{apiID} | Deletes an *API Definition* object, if it exists |
| PUT | /tyk/apis/{apiID} | Updates an *API Definition* object, if it exists |
| GET | /tyk/health/ | Gets the health check values for an API if it is being recorded |
| GET | /tyk/reload/ | Will reload the targetted gateway |
| GET | /tyk/reload/group | Will reload the cluster via the targeted gateway |
| POST | /tyk/oauth/clients/create | Create a new OAuth client |
| DELETE | /tyk/oauth/clients/{apiId}/{clientId} | Delete the OAuth client |
| GET | /tyk/oauth/clients/{apiId} | Get a list of OAuth clients bound to this back end |
| POST | /tyk/oauth/authorize-client/ | The final request from an authorising party for a redirect URI during the Tyk OAuth flow |
| DELETE | /tyk/oauth/refresh/{keyId} | Invalidate a refresh token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all keys?" -> GET /tyk/keys/
- "Create a create?" -> POST /tyk/keys/create
- "Update a key?" -> PUT /tyk/keys/{keyId}
- "Delete a key?" -> DELETE /tyk/keys/{keyId}
- "List all apis?" -> GET /tyk/apis/
- "Create a apis?" -> POST /tyk/apis/
- "Get apis details?" -> GET /tyk/apis/{apiID}
- "Delete a apis?" -> DELETE /tyk/apis/{apiID}
- "Update a apis?" -> PUT /tyk/apis/{apiID}
- "List all health?" -> GET /tyk/health/
- "List all reload?" -> GET /tyk/reload/
- "List all group?" -> GET /tyk/reload/group
- "Create a create?" -> POST /tyk/oauth/clients/create
- "Delete a client?" -> DELETE /tyk/oauth/clients/{apiId}/{clientId}
- "Get client details?" -> GET /tyk/oauth/clients/{apiId}
- "Create a authorize-client?" -> POST /tyk/oauth/authorize-client/
- "Delete a refresh?" -> DELETE /tyk/oauth/refresh/{keyId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
