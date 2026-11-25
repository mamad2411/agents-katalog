---
name: drive-api
description: "Drive API skill. Use when working with Drive for about, changes, channels. Covers 48 endpoints."
version: 1.0.0
generator: lapsh
---

# Drive API
API version: v3

## Auth
OAuth2 | OAuth2

## Base URL
https://www.googleapis.com/drive/v3

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /about -- verify access
3. POST /changes/watch -- create first watch

## Endpoints

48 endpoints across 6 groups. See references/api-spec.lap for full details.

### about
| Method | Path | Description |
|--------|------|-------------|
| GET | /about | Gets information about the user, the user's Drive, and system capabilities. |

### changes
| Method | Path | Description |
|--------|------|-------------|
| GET | /changes | Lists the changes for a user or shared drive. |
| GET | /changes/startPageToken | Gets the starting pageToken for listing future changes. |
| POST | /changes/watch | Subscribes to changes for a user. To use this method, you must include the pageToken query parameter. |

### channels
| Method | Path | Description |
|--------|------|-------------|
| POST | /channels/stop | Stop watching resources through this channel |

### drives
| Method | Path | Description |
|--------|------|-------------|
| GET | /drives | Lists the user's shared drives. |
| POST | /drives | Creates a shared drive. |
| DELETE | /drives/{driveId} | Permanently deletes a shared drive for which the user is an organizer. The shared drive cannot contain any untrashed items. |
| GET | /drives/{driveId} | Gets a shared drive's metadata by ID. |
| PATCH | /drives/{driveId} | Updates the metadata for a shared drive. |
| POST | /drives/{driveId}/hide | Hides a shared drive from the default view. |
| POST | /drives/{driveId}/unhide | Restores a shared drive to the default view. |

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /files | Lists or searches files. |
| POST | /files | Creates a file. |
| GET | /files/generateIds | Generates a set of file IDs which can be provided in create or copy requests. |
| DELETE | /files/trash | Permanently deletes all of the user's trashed files. |
| DELETE | /files/{fileId} | Permanently deletes a file owned by the user without moving it to the trash. If the file belongs to a shared drive the user must be an organizer on the parent. If the target is a folder, all descendants owned by the user are also deleted. |
| GET | /files/{fileId} | Gets a file's metadata or content by ID. |
| PATCH | /files/{fileId} | Updates a file's metadata and/or content. When calling this method, only populate fields in the request that you want to modify. When updating fields, some fields might change automatically, such as modifiedDate. This method supports patch semantics. |
| GET | /files/{fileId}/comments | Lists a file's comments. |
| POST | /files/{fileId}/comments | Creates a comment on a file. |
| DELETE | /files/{fileId}/comments/{commentId} | Deletes a comment. |
| GET | /files/{fileId}/comments/{commentId} | Gets a comment by ID. |
| PATCH | /files/{fileId}/comments/{commentId} | Updates a comment with patch semantics. |
| GET | /files/{fileId}/comments/{commentId}/replies | Lists a comment's replies. |
| POST | /files/{fileId}/comments/{commentId}/replies | Creates a reply to a comment. |
| DELETE | /files/{fileId}/comments/{commentId}/replies/{replyId} | Deletes a reply. |
| GET | /files/{fileId}/comments/{commentId}/replies/{replyId} | Gets a reply by ID. |
| PATCH | /files/{fileId}/comments/{commentId}/replies/{replyId} | Updates a reply with patch semantics. |
| POST | /files/{fileId}/copy | Creates a copy of a file and applies any requested updates with patch semantics. Folders cannot be copied. |
| GET | /files/{fileId}/export | Exports a Google Workspace document to the requested MIME type and returns exported byte content. Note that the exported content is limited to 10MB. |
| GET | /files/{fileId}/listLabels | Lists the labels on a file. |
| POST | /files/{fileId}/modifyLabels | Modifies the set of labels on a file. |
| GET | /files/{fileId}/permissions | Lists a file's or shared drive's permissions. |
| POST | /files/{fileId}/permissions | Creates a permission for a file or shared drive. For more information on creating permissions, see Share files, folders & drives. |
| DELETE | /files/{fileId}/permissions/{permissionId} | Deletes a permission. |
| GET | /files/{fileId}/permissions/{permissionId} | Gets a permission by ID. |
| PATCH | /files/{fileId}/permissions/{permissionId} | Updates a permission with patch semantics. |
| GET | /files/{fileId}/revisions | Lists a file's revisions. |
| DELETE | /files/{fileId}/revisions/{revisionId} | Permanently deletes a file version. You can only delete revisions for files with binary content in Google Drive, like images or videos. Revisions for other files, like Google Docs or Sheets, and the last remaining file version can't be deleted. |
| GET | /files/{fileId}/revisions/{revisionId} | Gets a revision's metadata or content by ID. |
| PATCH | /files/{fileId}/revisions/{revisionId} | Updates a revision with patch semantics. |
| POST | /files/{fileId}/watch | Subscribes to changes to a file. |

### teamdrives
| Method | Path | Description |
|--------|------|-------------|
| GET | /teamdrives | Deprecated use drives.list instead. |
| POST | /teamdrives | Deprecated use drives.create instead. |
| DELETE | /teamdrives/{teamDriveId} | Deprecated use drives.delete instead. |
| GET | /teamdrives/{teamDriveId} | Deprecated use drives.get instead. |
| PATCH | /teamdrives/{teamDriveId} | Deprecated use drives.update instead |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all about?" -> GET /about
- "List all changes?" -> GET /changes
- "List all startPageToken?" -> GET /changes/startPageToken
- "Create a watch?" -> POST /changes/watch
- "Create a stop?" -> POST /channels/stop
- "Search drives?" -> GET /drives
- "Create a drive?" -> POST /drives
- "Delete a drive?" -> DELETE /drives/{driveId}
- "Get drive details?" -> GET /drives/{driveId}
- "Partially update a drive?" -> PATCH /drives/{driveId}
- "Create a hide?" -> POST /drives/{driveId}/hide
- "Create a unhide?" -> POST /drives/{driveId}/unhide
- "Search files?" -> GET /files
- "Create a file?" -> POST /files
- "List all generateIds?" -> GET /files/generateIds
- "Delete a file?" -> DELETE /files/{fileId}
- "Get file details?" -> GET /files/{fileId}
- "Partially update a file?" -> PATCH /files/{fileId}
- "List all comments?" -> GET /files/{fileId}/comments
- "Create a comment?" -> POST /files/{fileId}/comments
- "Delete a comment?" -> DELETE /files/{fileId}/comments/{commentId}
- "Get comment details?" -> GET /files/{fileId}/comments/{commentId}
- "Partially update a comment?" -> PATCH /files/{fileId}/comments/{commentId}
- "List all replies?" -> GET /files/{fileId}/comments/{commentId}/replies
- "Create a reply?" -> POST /files/{fileId}/comments/{commentId}/replies
- "Delete a reply?" -> DELETE /files/{fileId}/comments/{commentId}/replies/{replyId}
- "Get reply details?" -> GET /files/{fileId}/comments/{commentId}/replies/{replyId}
- "Partially update a reply?" -> PATCH /files/{fileId}/comments/{commentId}/replies/{replyId}
- "Create a copy?" -> POST /files/{fileId}/copy
- "List all export?" -> GET /files/{fileId}/export
- "List all listLabels?" -> GET /files/{fileId}/listLabels
- "Create a modifyLabel?" -> POST /files/{fileId}/modifyLabels
- "List all permissions?" -> GET /files/{fileId}/permissions
- "Create a permission?" -> POST /files/{fileId}/permissions
- "Delete a permission?" -> DELETE /files/{fileId}/permissions/{permissionId}
- "Get permission details?" -> GET /files/{fileId}/permissions/{permissionId}
- "Partially update a permission?" -> PATCH /files/{fileId}/permissions/{permissionId}
- "List all revisions?" -> GET /files/{fileId}/revisions
- "Delete a revision?" -> DELETE /files/{fileId}/revisions/{revisionId}
- "Get revision details?" -> GET /files/{fileId}/revisions/{revisionId}
- "Partially update a revision?" -> PATCH /files/{fileId}/revisions/{revisionId}
- "Create a watch?" -> POST /files/{fileId}/watch
- "Search teamdrives?" -> GET /teamdrives
- "Create a teamdrive?" -> POST /teamdrives
- "Delete a teamdrive?" -> DELETE /teamdrives/{teamDriveId}
- "Get teamdrive details?" -> GET /teamdrives/{teamDriveId}
- "Partially update a teamdrive?" -> PATCH /teamdrives/{teamDriveId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
