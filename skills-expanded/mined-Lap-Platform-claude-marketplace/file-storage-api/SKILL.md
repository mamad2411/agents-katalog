---
name: file-storage-api
description: "File storage API skill. Use when working with File storage for file-storage. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# File storage API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /file-storage/files -- verify access
3. POST /file-storage/files -- create first files

## Endpoints

33 endpoints across 1 groups. See references/api-spec.lap for full details.

### file-storage
| Method | Path | Description |
|--------|------|-------------|
| GET | /file-storage/files | List Files |
| POST | /file-storage/files | Upload file |
| POST | /file-storage/files/search | Search Files |
| GET | /file-storage/files/{id} | Get File |
| PATCH | /file-storage/files/{id} | Rename or move File |
| DELETE | /file-storage/files/{id} | Delete File |
| GET | /file-storage/files/{id}/download | Download File |
| GET | /file-storage/files/{id}/export | Export File |
| POST | /file-storage/folders | Create Folder |
| GET | /file-storage/folders/{id} | Get Folder |
| PATCH | /file-storage/folders/{id} | Rename or move Folder |
| DELETE | /file-storage/folders/{id} | Delete Folder |
| POST | /file-storage/folders/{id}/copy | Copy Folder |
| GET | /file-storage/shared-links | List Shared Links |
| POST | /file-storage/shared-links | Create Shared Link |
| GET | /file-storage/shared-links/{id} | Get Shared Link |
| PATCH | /file-storage/shared-links/{id} | Update Shared Link |
| DELETE | /file-storage/shared-links/{id} | Delete Shared Link |
| POST | /file-storage/upload-sessions | Start Upload Session |
| GET | /file-storage/upload-sessions/{id} | Get Upload Session |
| PUT | /file-storage/upload-sessions/{id} | Upload part of File to Upload Session |
| DELETE | /file-storage/upload-sessions/{id} | Abort Upload Session |
| POST | /file-storage/upload-sessions/{id}/finish | Finish Upload Session |
| GET | /file-storage/drives | List Drives |
| POST | /file-storage/drives | Create Drive |
| GET | /file-storage/drives/{id} | Get Drive |
| PATCH | /file-storage/drives/{id} | Update Drive |
| DELETE | /file-storage/drives/{id} | Delete Drive |
| GET | /file-storage/drive-groups | List DriveGroups |
| POST | /file-storage/drive-groups | Create DriveGroup |
| GET | /file-storage/drive-groups/{id} | Get DriveGroup |
| PATCH | /file-storage/drive-groups/{id} | Update DriveGroup |
| DELETE | /file-storage/drive-groups/{id} | Delete DriveGroup |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all files?" -> GET /file-storage/files
- "Create a file?" -> POST /file-storage/files
- "Create a search?" -> POST /file-storage/files/search
- "Get file details?" -> GET /file-storage/files/{id}
- "Partially update a file?" -> PATCH /file-storage/files/{id}
- "Delete a file?" -> DELETE /file-storage/files/{id}
- "List all download?" -> GET /file-storage/files/{id}/download
- "List all export?" -> GET /file-storage/files/{id}/export
- "Create a folder?" -> POST /file-storage/folders
- "Get folder details?" -> GET /file-storage/folders/{id}
- "Partially update a folder?" -> PATCH /file-storage/folders/{id}
- "Delete a folder?" -> DELETE /file-storage/folders/{id}
- "Create a copy?" -> POST /file-storage/folders/{id}/copy
- "List all shared-links?" -> GET /file-storage/shared-links
- "Create a shared-link?" -> POST /file-storage/shared-links
- "Get shared-link details?" -> GET /file-storage/shared-links/{id}
- "Partially update a shared-link?" -> PATCH /file-storage/shared-links/{id}
- "Delete a shared-link?" -> DELETE /file-storage/shared-links/{id}
- "Create a upload-session?" -> POST /file-storage/upload-sessions
- "Get upload-session details?" -> GET /file-storage/upload-sessions/{id}
- "Update a upload-session?" -> PUT /file-storage/upload-sessions/{id}
- "Delete a upload-session?" -> DELETE /file-storage/upload-sessions/{id}
- "Create a finish?" -> POST /file-storage/upload-sessions/{id}/finish
- "List all drives?" -> GET /file-storage/drives
- "Create a drive?" -> POST /file-storage/drives
- "Get drive details?" -> GET /file-storage/drives/{id}
- "Partially update a drive?" -> PATCH /file-storage/drives/{id}
- "Delete a drive?" -> DELETE /file-storage/drives/{id}
- "List all drive-groups?" -> GET /file-storage/drive-groups
- "Create a drive-group?" -> POST /file-storage/drive-groups
- "Get drive-group details?" -> GET /file-storage/drive-groups/{id}
- "Partially update a drive-group?" -> PATCH /file-storage/drive-groups/{id}
- "Delete a drive-group?" -> DELETE /file-storage/drive-groups/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
