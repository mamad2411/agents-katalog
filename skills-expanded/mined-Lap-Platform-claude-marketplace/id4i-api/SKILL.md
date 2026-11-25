---
name: id4i-api
description: "ID4i API skill. Use when working with ID4i for account, api, go. Covers 107 endpoints."
version: 1.0.0
generator: lapsh
---

# ID4i API
API version: 1.0.2

## Auth
ApiKey Authorization in header

## Base URL
https://backend.id4i.de/

## Setup
1. Set your API key in the appropriate header
2. GET /api/v1/apikeys -- verify access
3. POST /account/password -- create first password

## Endpoints

107 endpoints across 5 groups. See references/api-spec.lap for full details.

### account
| Method | Path | Description |
|--------|------|-------------|
| POST | /account/password | Request password reset |
| PUT | /account/password | Verify password reset |
| POST | /account/registration | Register user |
| PUT | /account/registration | Complete registration |
| POST | /account/verification | Verify registration |

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/apikeys | Find API key by organization |
| POST | /api/v1/apikeys | Create API key |
| GET | /api/v1/apikeys/privileges | List all privileges |
| GET | /api/v1/apikeys/{key} | Show API key |
| PUT | /api/v1/apikeys/{key} | Update API keys |
| DELETE | /api/v1/apikeys/{key} | Delete API key |
| GET | /api/v1/apikeys/{key}/privileges | List privileges |
| POST | /api/v1/apikeys/{key}/privileges | Add privilege |
| DELETE | /api/v1/apikeys/{key}/privileges | Remove privilege |
| GET | /api/v1/apikeys/{key}/privileges/{privilege}/id4ns | ID4ns of a privilege |
| POST | /api/v1/apikeys/{key}/privileges/{privilege}/id4ns | Add ID4ns of a privilege |
| DELETE | /api/v1/apikeys/{key}/privileges/{privilege}/id4ns | Remove id4ns of a privilege |
| GET | /api/v1/billing/{organizationId} | Get billing amount of services for a given organization |
| GET | /api/v1/billing/{organizationId}/positions | Get billing positions for a given organization |
| GET | /api/v1/changelog/organization/{organizationId}/ | List change log entries of an organization |
| POST | /api/v1/collections | Create collection |
| GET | /api/v1/collections/{id4n} | Find collection |
| DELETE | /api/v1/collections/{id4n} | Delete collection |
| PATCH | /api/v1/collections/{id4n} | Update collection |
| GET | /api/v1/collections/{id4n}/elements | List contents of the collection |
| POST | /api/v1/collections/{id4n}/elements | Add elements to collection |
| DELETE | /api/v1/collections/{id4n}/elements | Remove elements from collection |
| GET | /api/v1/countries | List countries |
| GET | /api/v1/documents/{id4n} | List documents |
| GET | /api/v1/documents/{id4n}/{organizationId} | List organization specific documents |
| POST | /api/v1/documents/{id4n}/{organizationId} | Create an document for an id4n |
| PUT | /api/v1/documents/{id4n}/{organizationId} | Put an document for an id4n |
| GET | /api/v1/documents/{id4n}/{organizationId}/{fileName} | Read document contents |
| DELETE | /api/v1/documents/{id4n}/{organizationId}/{fileName} | Delete a document |
| GET | /api/v1/documents/{id4n}/{organizationId}/{fileName}/metadata | Retrieve a document (meta-data only, no content) |
| PATCH | /api/v1/documents/{id4n}/{organizationId}/{fileName}/metadata | Update a document |
| POST | /api/v1/guids | Create GUID(s) |
| GET | /api/v1/guids/withoutCollection | Retrieve GUIDs not in any collection |
| GET | /api/v1/guids/{id4n} | Retrieve GUID information |
| PATCH | /api/v1/guids/{id4n} | Change GUID information. |
| GET | /api/v1/history/{id4n} | List history |
| POST | /api/v1/history/{id4n} | Add history item |
| GET | /api/v1/history/{id4n}/{organizationId} | DEPRECATED - List history |
| GET | /api/v1/history/{id4n}/{organizationId}/{sequenceId} | Get history item |
| PATCH | /api/v1/history/{id4n}/{organizationId}/{sequenceId} | Update history item |
| PUT | /api/v1/history/{id4n}/{organizationId}/{sequenceId}/visibility | Set history item visibility |
| GET | /api/v1/id4ns/{id4n} | Retrieve ID4n information |
| GET | /api/v1/id4ns/{id4n}/alias | Get all aliases for the given GUID or Collection. |
| POST | /api/v1/id4ns/{id4n}/alias/{aliasType} | Add alias for GUID or Collection |
| DELETE | /api/v1/id4ns/{id4n}/alias/{aliasType} | Remove aliases from GUID or Collection |
| GET | /api/v1/id4ns/{id4n}/collections | Retrieve collections of an ID |
| GET | /api/v1/id4ns/{id4n}/properties | Retrieve ID4n properties |
| DELETE | /api/v1/id4ns/{id4n}/properties | Delete ID4n properties |
| PATCH | /api/v1/id4ns/{id4n}/properties | Patch ID4n properties |
| POST | /api/v1/import/gs1 | Import GS1/MAPP codes |
| GET | /api/v1/info | Retrieve version information about ID4i |
| GET | /api/v1/microstorage/{id4n}/{organization} | Read data from microstorage |
| PUT | /api/v1/microstorage/{id4n}/{organization} | Write data to microstorage |
| GET | /api/v1/multiple/id4ns/properties | Get multiple ID4n properties |
| POST | /api/v1/organizations | Create organization |
| GET | /api/v1/organizations/{organizationId} | Find organization by id/namespace |
| PUT | /api/v1/organizations/{organizationId} | Update organization |
| DELETE | /api/v1/organizations/{organizationId} | Delete organization |
| GET | /api/v1/organizations/{organizationId}/addresses/billing | Retrieve billing address |
| PUT | /api/v1/organizations/{organizationId}/addresses/billing | Store billing address |
| DELETE | /api/v1/organizations/{organizationId}/addresses/billing | Remove billing address |
| GET | /api/v1/organizations/{organizationId}/addresses/default | Retrieve address |
| PUT | /api/v1/organizations/{organizationId}/addresses/default | Store address |
| GET | /api/v1/organizations/{organizationId}/collections | Get collections of organization |
| POST | /api/v1/organizations/{organizationId}/logo | Update organization logo |
| DELETE | /api/v1/organizations/{organizationId}/logo | Delete organization logo |
| GET | /api/v1/organizations/{organizationId}/messaging |  |
| PATCH | /api/v1/organizations/{organizationId}/messaging |  |
| POST | /api/v1/organizations/{organizationId}/messaging/enqueueCustomMessage | Enqueue a custom message |
| GET | /api/v1/organizations/{organizationId}/partner | Get partners of an organization |
| PUT | /api/v1/organizations/{organizationId}/partner | Add partner |
| DELETE | /api/v1/organizations/{organizationId}/partner | Remove partner |
| GET | /api/v1/organizations/{organizationId}/privileges | List my privileges |
| GET | /api/v1/organizations/{organizationId}/roles | List users and their roles |
| GET | /api/v1/organizations/{organizationId}/users | Find users in organization |
| POST | /api/v1/organizations/{organizationId}/users/invite | Invite Users |
| GET | /api/v1/organizations/{organizationId}/users/{username}/roles | Get user roles by username |
| POST | /api/v1/organizations/{organizationId}/users/{username}/roles | Add role(s) to user |
| DELETE | /api/v1/organizations/{organizationId}/users/{username}/roles | Remove role(s) from user |
| GET | /api/v1/public/documents/{id4n} | List public documents |
| GET | /api/v1/public/documents/{id4n}/{organizationId}/{fileName} | Read public document contents |
| GET | /api/v1/public/documents/{id4n}/{organizationId}/{fileName}/metadata | Retrieve a public document (meta-data only, no content) |
| GET | /api/v1/public/history/{id4n} | Shows the public history of the given GUID |
| GET | /api/v1/public/image/{imageID} | Resolve image |
| GET | /api/v1/public/organizations/{organizationId} | Read public organization information |
| GET | /api/v1/public/routes/{id4n} | Retrieve all public routes for a GUID |
| GET | /api/v1/roles | List roles |
| GET | /api/v1/routingfiles/{id4n} | Retrieve routing file |
| PUT | /api/v1/routingfiles/{id4n} | Store routing file |
| GET | /api/v1/routingfiles/{id4n}/route/{type} | Retrieve current route of a GUID (or ID4N) |
| GET | /api/v1/routingfiles/{id4n}/routes/{type} | Retrieve all routes of a GUID (or ID4N) |
| GET | /api/v1/search/guids | Search for GUIDs by alias |
| GET | /api/v1/search/guids/aliases/types | List all supported alias types |
| PUT | /api/v1/transfers/{id4n}/receiveInfo | Transfer a GUID or collection, obtaining it (i.e. becoming the holder) and if allowed also taking ownership |
| GET | /api/v1/transfers/{id4n}/sendInfo | Show transfer preparation information |
| PUT | /api/v1/transfers/{id4n}/sendInfo | Prepare an object for transfer |
| GET | /api/v1/user/organizations | Retrieve organizations of user |
| GET | /api/v1/users | Find users |
| GET | /api/v1/users/{username} | Find by username |

### go
| Method | Path | Description |
|--------|------|-------------|
| GET | /go/{guid} | Forward |

### login
| Method | Path | Description |
|--------|------|-------------|
| POST | /login | ID4i API Login |

### whois
| Method | Path | Description |
|--------|------|-------------|
| GET | /whois/{id4n} | Resolve owner of id4n |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a password?" -> POST /account/password
- "Create a registration?" -> POST /account/registration
- "Create a verification?" -> POST /account/verification
- "List all apikeys?" -> GET /api/v1/apikeys
- "Create a apikey?" -> POST /api/v1/apikeys
- "List all privileges?" -> GET /api/v1/apikeys/privileges
- "Get apikey details?" -> GET /api/v1/apikeys/{key}
- "Update a apikey?" -> PUT /api/v1/apikeys/{key}
- "Delete a apikey?" -> DELETE /api/v1/apikeys/{key}
- "List all privileges?" -> GET /api/v1/apikeys/{key}/privileges
- "Create a privilege?" -> POST /api/v1/apikeys/{key}/privileges
- "List all id4ns?" -> GET /api/v1/apikeys/{key}/privileges/{privilege}/id4ns
- "Create a id4n?" -> POST /api/v1/apikeys/{key}/privileges/{privilege}/id4ns
- "Get billing details?" -> GET /api/v1/billing/{organizationId}
- "List all positions?" -> GET /api/v1/billing/{organizationId}/positions
- "Get organization details?" -> GET /api/v1/changelog/organization/{organizationId}/
- "Create a collection?" -> POST /api/v1/collections
- "Get collection details?" -> GET /api/v1/collections/{id4n}
- "Delete a collection?" -> DELETE /api/v1/collections/{id4n}
- "Partially update a collection?" -> PATCH /api/v1/collections/{id4n}
- "List all elements?" -> GET /api/v1/collections/{id4n}/elements
- "Create a element?" -> POST /api/v1/collections/{id4n}/elements
- "List all countries?" -> GET /api/v1/countries
- "Get document details?" -> GET /api/v1/documents/{id4n}
- "Get document details?" -> GET /api/v1/documents/{id4n}/{organizationId}
- "Update a document?" -> PUT /api/v1/documents/{id4n}/{organizationId}
- "Get document details?" -> GET /api/v1/documents/{id4n}/{organizationId}/{fileName}
- "Delete a document?" -> DELETE /api/v1/documents/{id4n}/{organizationId}/{fileName}
- "List all metadata?" -> GET /api/v1/documents/{id4n}/{organizationId}/{fileName}/metadata
- "Create a guid?" -> POST /api/v1/guids
- "List all withoutCollection?" -> GET /api/v1/guids/withoutCollection
- "Get guid details?" -> GET /api/v1/guids/{id4n}
- "Partially update a guid?" -> PATCH /api/v1/guids/{id4n}
- "Get history details?" -> GET /api/v1/history/{id4n}
- "Get history details?" -> GET /api/v1/history/{id4n}/{organizationId}
- "Get history details?" -> GET /api/v1/history/{id4n}/{organizationId}/{sequenceId}
- "Partially update a history?" -> PATCH /api/v1/history/{id4n}/{organizationId}/{sequenceId}
- "Get id4n details?" -> GET /api/v1/id4ns/{id4n}
- "List all alias?" -> GET /api/v1/id4ns/{id4n}/alias
- "Delete a alia?" -> DELETE /api/v1/id4ns/{id4n}/alias/{aliasType}
- "List all collections?" -> GET /api/v1/id4ns/{id4n}/collections
- "List all properties?" -> GET /api/v1/id4ns/{id4n}/properties
- "Create a gs1?" -> POST /api/v1/import/gs1
- "List all info?" -> GET /api/v1/info
- "Get microstorage details?" -> GET /api/v1/microstorage/{id4n}/{organization}
- "Update a microstorage?" -> PUT /api/v1/microstorage/{id4n}/{organization}
- "List all properties?" -> GET /api/v1/multiple/id4ns/properties
- "Create a organization?" -> POST /api/v1/organizations
- "Get organization details?" -> GET /api/v1/organizations/{organizationId}
- "Update a organization?" -> PUT /api/v1/organizations/{organizationId}
- "Delete a organization?" -> DELETE /api/v1/organizations/{organizationId}
- "List all billing?" -> GET /api/v1/organizations/{organizationId}/addresses/billing
- "List all default?" -> GET /api/v1/organizations/{organizationId}/addresses/default
- "List all collections?" -> GET /api/v1/organizations/{organizationId}/collections
- "Create a logo?" -> POST /api/v1/organizations/{organizationId}/logo
- "List all messaging?" -> GET /api/v1/organizations/{organizationId}/messaging
- "Create a enqueueCustomMessage?" -> POST /api/v1/organizations/{organizationId}/messaging/enqueueCustomMessage
- "List all partner?" -> GET /api/v1/organizations/{organizationId}/partner
- "List all privileges?" -> GET /api/v1/organizations/{organizationId}/privileges
- "List all roles?" -> GET /api/v1/organizations/{organizationId}/roles
- "List all users?" -> GET /api/v1/organizations/{organizationId}/users
- "Create a invite?" -> POST /api/v1/organizations/{organizationId}/users/invite
- "List all roles?" -> GET /api/v1/organizations/{organizationId}/users/{username}/roles
- "Create a role?" -> POST /api/v1/organizations/{organizationId}/users/{username}/roles
- "Get document details?" -> GET /api/v1/public/documents/{id4n}
- "Get document details?" -> GET /api/v1/public/documents/{id4n}/{organizationId}/{fileName}
- "List all metadata?" -> GET /api/v1/public/documents/{id4n}/{organizationId}/{fileName}/metadata
- "Get history details?" -> GET /api/v1/public/history/{id4n}
- "Get image details?" -> GET /api/v1/public/image/{imageID}
- "Get organization details?" -> GET /api/v1/public/organizations/{organizationId}
- "Get route details?" -> GET /api/v1/public/routes/{id4n}
- "List all roles?" -> GET /api/v1/roles
- "Get routingfile details?" -> GET /api/v1/routingfiles/{id4n}
- "Update a routingfile?" -> PUT /api/v1/routingfiles/{id4n}
- "Get route details?" -> GET /api/v1/routingfiles/{id4n}/route/{type}
- "Get route details?" -> GET /api/v1/routingfiles/{id4n}/routes/{type}
- "List all guids?" -> GET /api/v1/search/guids
- "List all types?" -> GET /api/v1/search/guids/aliases/types
- "List all sendInfo?" -> GET /api/v1/transfers/{id4n}/sendInfo
- "List all organizations?" -> GET /api/v1/user/organizations
- "List all users?" -> GET /api/v1/users
- "Get user details?" -> GET /api/v1/users/{username}
- "Get go details?" -> GET /go/{guid}
- "Create a login?" -> POST /login
- "Get whois details?" -> GET /whois/{id4n}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
