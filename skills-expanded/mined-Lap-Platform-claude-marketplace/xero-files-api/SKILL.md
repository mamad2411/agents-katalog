---
name: xero-files-api
description: "Xero Files API skill. Use when working with Xero Files for Files, Associations, Folders. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# Xero Files API
API version: 11.1.0

## Auth
OAuth2

## Base URL
https://api.xero.com/files.xro/1.0/

## Setup
1. Configure auth: OAuth2
2. GET /Files -- verify access
3. POST /Files -- create first Files

## Endpoints

18 endpoints across 4 groups. See references/api-spec.lap for full details.

### Files
| Method | Path | Description |
|--------|------|-------------|
| GET | /Files | Retrieves files |
| POST | /Files | Uploads a File to the inbox |
| GET | /Files/{FileId} | Retrieves a file by a unique file ID |
| PUT | /Files/{FileId} | Update a file |
| DELETE | /Files/{FileId} | Deletes a specific file |
| POST | /Files/{FolderId} | Uploads a File to a specific folder |
| GET | /Files/{FileId}/Content | Retrieves the content of a specific file |
| GET | /Files/{FileId}/Associations | Retrieves a specific file associations |
| POST | /Files/{FileId}/Associations | Creates a new file association |
| DELETE | /Files/{FileId}/Associations/{ObjectId} | Deletes an existing file association |

### Associations
| Method | Path | Description |
|--------|------|-------------|
| GET | /Associations/{ObjectId} | Retrieves an association object using a unique object ID |
| GET | /Associations/Count | Retrieves a count of associations for a list of objects. |

### Folders
| Method | Path | Description |
|--------|------|-------------|
| GET | /Folders | Retrieves folders |
| POST | /Folders | Creates a new folder |
| GET | /Folders/{FolderId} | Retrieves specific folder by using a unique folder ID |
| PUT | /Folders/{FolderId} | Updates an existing folder |
| DELETE | /Folders/{FolderId} | Deletes a folder |

### Inbox
| Method | Path | Description |
|--------|------|-------------|
| GET | /Inbox | Retrieves inbox folder |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Files?" -> GET /Files
- "Create a File?" -> POST /Files
- "Get File details?" -> GET /Files/{FileId}
- "Update a File?" -> PUT /Files/{FileId}
- "Delete a File?" -> DELETE /Files/{FileId}
- "List all Content?" -> GET /Files/{FileId}/Content
- "List all Associations?" -> GET /Files/{FileId}/Associations
- "Create a Association?" -> POST /Files/{FileId}/Associations
- "Delete a Association?" -> DELETE /Files/{FileId}/Associations/{ObjectId}
- "Get Association details?" -> GET /Associations/{ObjectId}
- "List all Count?" -> GET /Associations/Count
- "List all Folders?" -> GET /Folders
- "Create a Folder?" -> POST /Folders
- "Get Folder details?" -> GET /Folders/{FolderId}
- "Update a Folder?" -> PUT /Folders/{FolderId}
- "Delete a Folder?" -> DELETE /Folders/{FolderId}
- "List all Inbox?" -> GET /Inbox
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
