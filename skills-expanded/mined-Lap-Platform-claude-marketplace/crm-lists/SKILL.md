---
name: crm-lists
description: "CRM Lists API skill. Use when working with CRM Lists for crm. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# CRM Lists
API version: v3

## Auth
OAuth2 | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v3/lists/ -- verify access
3. POST /crm/v3/lists/ -- create first lists

## Endpoints

29 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/v3/lists/ | Fetch Multiple Lists |
| POST | /crm/v3/lists/ | Create List |
| GET | /crm/v3/lists/folders | Retrieves a folder. |
| POST | /crm/v3/lists/folders | Creates a folder |
| PUT | /crm/v3/lists/folders/move-list | Moves a list to a given folder |
| DELETE | /crm/v3/lists/folders/{folderId} | Deletes a folder |
| PUT | /crm/v3/lists/folders/{folderId}/move/{newParentFolderId} | Moves a folder |
| PUT | /crm/v3/lists/folders/{folderId}/rename | Rename a folder |
| GET | /crm/v3/lists/idmapping | Translate Legacy List Id to Modern List Id |
| POST | /crm/v3/lists/idmapping | Translate Legacy List Id to Modern List Id in Batch |
| GET | /crm/v3/lists/object-type-id/{objectTypeId}/name/{listName} | Fetch List by Name |
| POST | /crm/v3/lists/records/memberships/batch/read |  |
| GET | /crm/v3/lists/records/{objectTypeId}/{recordId}/memberships | Get lists record is member of |
| POST | /crm/v3/lists/search | Search Lists |
| GET | /crm/v3/lists/{listId} | Fetch List by ID |
| DELETE | /crm/v3/lists/{listId} | Delete a List |
| GET | /crm/v3/lists/{listId}/memberships | Fetch List Memberships Ordered by ID |
| DELETE | /crm/v3/lists/{listId}/memberships | Delete All Records from a List |
| PUT | /crm/v3/lists/{listId}/memberships/add | Add Records to a List |
| PUT | /crm/v3/lists/{listId}/memberships/add-and-remove | Add and/or Remove Records from a List |
| PUT | /crm/v3/lists/{listId}/memberships/add-from/{sourceListId} | Add All Records from a Source List to a Destination List |
| GET | /crm/v3/lists/{listId}/memberships/join-order | Fetch List Memberships Ordered by Added to List Date |
| PUT | /crm/v3/lists/{listId}/memberships/remove | Remove Records from a List |
| PUT | /crm/v3/lists/{listId}/restore | Restore a List |
| GET | /crm/v3/lists/{listId}/schedule-conversion | Retrieve the conversion details for a list |
| PUT | /crm/v3/lists/{listId}/schedule-conversion | Schedule or update the conversion of a list to static |
| DELETE | /crm/v3/lists/{listId}/schedule-conversion | Cancel the conversion of a list |
| PUT | /crm/v3/lists/{listId}/update-list-filters | Update List Filter Definition |
| PUT | /crm/v3/lists/{listId}/update-list-name | Update List Name |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all lists?" -> GET /crm/v3/lists/
- "Create a list?" -> POST /crm/v3/lists/
- "List all folders?" -> GET /crm/v3/lists/folders
- "Create a folder?" -> POST /crm/v3/lists/folders
- "Delete a folder?" -> DELETE /crm/v3/lists/folders/{folderId}
- "Update a move?" -> PUT /crm/v3/lists/folders/{folderId}/move/{newParentFolderId}
- "List all idmapping?" -> GET /crm/v3/lists/idmapping
- "Create a idmapping?" -> POST /crm/v3/lists/idmapping
- "Get name details?" -> GET /crm/v3/lists/object-type-id/{objectTypeId}/name/{listName}
- "Create a read?" -> POST /crm/v3/lists/records/memberships/batch/read
- "List all memberships?" -> GET /crm/v3/lists/records/{objectTypeId}/{recordId}/memberships
- "Create a search?" -> POST /crm/v3/lists/search
- "Get list details?" -> GET /crm/v3/lists/{listId}
- "Delete a list?" -> DELETE /crm/v3/lists/{listId}
- "List all memberships?" -> GET /crm/v3/lists/{listId}/memberships
- "Update a add-from?" -> PUT /crm/v3/lists/{listId}/memberships/add-from/{sourceListId}
- "List all join-order?" -> GET /crm/v3/lists/{listId}/memberships/join-order
- "List all schedule-conversion?" -> GET /crm/v3/lists/{listId}/schedule-conversion
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
