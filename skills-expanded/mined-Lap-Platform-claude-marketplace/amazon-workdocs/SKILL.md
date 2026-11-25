---
name: amazon-workdocs
description: "Amazon WorkDocs API skill. Use when working with Amazon WorkDocs for api. Covers 44 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon WorkDocs
API version: 2016-05-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /api/v1/activities -- verify access
3. POST /api/v1/users/{UserId}/activation -- create first activation

## Endpoints

44 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /api/v1/documents/{DocumentId}/versions/{VersionId} | Aborts the upload of the specified document version that was previously initiated by InitiateDocumentVersionUpload. The client should make this call only when it no longer intends to upload the document version, or fails to do so. |
| POST | /api/v1/users/{UserId}/activation | Activates the specified user. Only active users can access Amazon WorkDocs. |
| POST | /api/v1/resources/{ResourceId}/permissions | Creates a set of permissions for the specified folder or document. The resource permissions are overwritten if the principals already have different permissions. |
| POST | /api/v1/documents/{DocumentId}/versions/{VersionId}/comment | Adds a new comment to the specified document version. |
| PUT | /api/v1/resources/{ResourceId}/customMetadata | Adds one or more custom properties to the specified resource (a folder, document, or version). |
| POST | /api/v1/folders | Creates a folder with the specified name and parent folder. |
| PUT | /api/v1/resources/{ResourceId}/labels | Adds the specified list of labels to the given resource (a document or folder) |
| POST | /api/v1/organizations/{OrganizationId}/subscriptions | Configure Amazon WorkDocs to use Amazon SNS notifications. The endpoint receives a confirmation message, and must confirm the subscription. For more information, see Setting up notifications for an IAM user or role in the Amazon WorkDocs Developer Guide. |
| POST | /api/v1/users | Creates a user in a Simple AD or Microsoft AD directory. The status of a newly created user is "ACTIVE". New users can access Amazon WorkDocs. |
| DELETE | /api/v1/users/{UserId}/activation | Deactivates the specified user, which revokes the user's access to Amazon WorkDocs. |
| DELETE | /api/v1/documents/{DocumentId}/versions/{VersionId}/comment/{CommentId} | Deletes the specified comment from the document version. |
| DELETE | /api/v1/resources/{ResourceId}/customMetadata | Deletes custom metadata from the specified resource. |
| DELETE | /api/v1/documents/{DocumentId} | Permanently deletes the specified document and its associated metadata. |
| DELETE | /api/v1/documentVersions/{DocumentId}/versions/{VersionId} | Deletes a specific version of a document. |
| DELETE | /api/v1/folders/{FolderId} | Permanently deletes the specified folder and its contents. |
| DELETE | /api/v1/folders/{FolderId}/contents | Deletes the contents of the specified folder. |
| DELETE | /api/v1/resources/{ResourceId}/labels | Deletes the specified list of labels from a resource. |
| DELETE | /api/v1/organizations/{OrganizationId}/subscriptions/{SubscriptionId} | Deletes the specified subscription from the specified organization. |
| DELETE | /api/v1/users/{UserId} | Deletes the specified user from a Simple AD or Microsoft AD directory.  Deleting a user immediately and permanently deletes all content in that user's folder structure. Site retention policies do NOT apply to this type of deletion. |
| GET | /api/v1/activities | Describes the user activities in a specified time period. |
| GET | /api/v1/documents/{DocumentId}/versions/{VersionId}/comments | List all the comments for the specified document version. |
| GET | /api/v1/documents/{DocumentId}/versions | Retrieves the document versions for the specified document. By default, only active versions are returned. |
| GET | /api/v1/folders/{FolderId}/contents | Describes the contents of the specified folder, including its documents and subfolders. By default, Amazon WorkDocs returns the first 100 active document and folder metadata items. If there are more results, the response includes a marker that you can use to request the next set of results. You can also request initialized documents. |
| GET | /api/v1/groups | Describes the groups specified by the query. Groups are defined by the underlying Active Directory. |
| GET | /api/v1/organizations/{OrganizationId}/subscriptions | Lists the specified notification subscriptions. |
| GET | /api/v1/resources/{ResourceId}/permissions | Describes the permissions of a specified resource. |
| GET | /api/v1/me/root | Describes the current user's special folders; the RootFolder and the RecycleBin. RootFolder is the root of user's files and folders and RecycleBin is the root of recycled items. This is not a valid action for SigV4 (administrative API) clients. This action requires an authentication token. To get an authentication token, register an application with Amazon WorkDocs. For more information, see Authentication and Access Control for User Applications in the Amazon WorkDocs Developer Guide. |
| GET | /api/v1/users | Describes the specified users. You can describe all users or filter the results (for example, by status or organization). By default, Amazon WorkDocs returns the first 24 active or pending users. If there are more results, the response includes a marker that you can use to request the next set of results. |
| GET | /api/v1/me | Retrieves details of the current user for whom the authentication token was generated. This is not a valid action for SigV4 (administrative API) clients. This action requires an authentication token. To get an authentication token, register an application with Amazon WorkDocs. For more information, see Authentication and Access Control for User Applications in the Amazon WorkDocs Developer Guide. |
| GET | /api/v1/documents/{DocumentId} | Retrieves details of a document. |
| GET | /api/v1/documents/{DocumentId}/path | Retrieves the path information (the hierarchy from the root folder) for the requested document. By default, Amazon WorkDocs returns a maximum of 100 levels upwards from the requested document and only includes the IDs of the parent folders in the path. You can limit the maximum number of levels. You can also request the names of the parent folders. |
| GET | /api/v1/documents/{DocumentId}/versions/{VersionId} | Retrieves version metadata for the specified document. |
| GET | /api/v1/folders/{FolderId} | Retrieves the metadata of the specified folder. |
| GET | /api/v1/folders/{FolderId}/path | Retrieves the path information (the hierarchy from the root folder) for the specified folder. By default, Amazon WorkDocs returns a maximum of 100 levels upwards from the requested folder and only includes the IDs of the parent folders in the path. You can limit the maximum number of levels. You can also request the parent folder names. |
| GET | /api/v1/resources | Retrieves a collection of resources, including folders and documents. The only CollectionType supported is SHARED_WITH_ME. |
| POST | /api/v1/documents | Creates a new document object and version object. The client specifies the parent folder ID and name of the document to upload. The ID is optionally specified when creating a new version of an existing document. This is the first step to upload a document. Next, upload the document to the URL returned from the call, and then call UpdateDocumentVersion. To cancel the document upload, call AbortDocumentVersionUpload. |
| DELETE | /api/v1/resources/{ResourceId}/permissions | Removes all the permissions from the specified resource. |
| DELETE | /api/v1/resources/{ResourceId}/permissions/{PrincipalId} | Removes the permission for the specified principal from the specified resource. |
| POST | /api/v1/documentVersions/restore/{DocumentId} | Recovers a deleted version of an Amazon WorkDocs document. |
| POST | /api/v1/search | Searches metadata and the content of folders, documents, document versions, and comments. |
| PATCH | /api/v1/documents/{DocumentId} | Updates the specified attributes of a document. The user must have access to both the document and its parent folder, if applicable. |
| PATCH | /api/v1/documents/{DocumentId}/versions/{VersionId} | Changes the status of the document version to ACTIVE.  Amazon WorkDocs also sets its document container to ACTIVE. This is the last step in a document upload, after the client uploads the document to an S3-presigned URL returned by InitiateDocumentVersionUpload. |
| PATCH | /api/v1/folders/{FolderId} | Updates the specified attributes of the specified folder. The user must have access to both the folder and its parent folder, if applicable. |
| PATCH | /api/v1/users/{UserId} | Updates the specified attributes of the specified user, and grants or revokes administrative privileges to the Amazon WorkDocs site. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a version?" -> DELETE /api/v1/documents/{DocumentId}/versions/{VersionId}
- "Create a activation?" -> POST /api/v1/users/{UserId}/activation
- "Create a permission?" -> POST /api/v1/resources/{ResourceId}/permissions
- "Create a comment?" -> POST /api/v1/documents/{DocumentId}/versions/{VersionId}/comment
- "Create a folder?" -> POST /api/v1/folders
- "Create a subscription?" -> POST /api/v1/organizations/{OrganizationId}/subscriptions
- "Create a user?" -> POST /api/v1/users
- "Delete a comment?" -> DELETE /api/v1/documents/{DocumentId}/versions/{VersionId}/comment/{CommentId}
- "Delete a document?" -> DELETE /api/v1/documents/{DocumentId}
- "Delete a version?" -> DELETE /api/v1/documentVersions/{DocumentId}/versions/{VersionId}
- "Delete a folder?" -> DELETE /api/v1/folders/{FolderId}
- "Delete a subscription?" -> DELETE /api/v1/organizations/{OrganizationId}/subscriptions/{SubscriptionId}
- "Delete a user?" -> DELETE /api/v1/users/{UserId}
- "List all activities?" -> GET /api/v1/activities
- "List all comments?" -> GET /api/v1/documents/{DocumentId}/versions/{VersionId}/comments
- "List all versions?" -> GET /api/v1/documents/{DocumentId}/versions
- "List all contents?" -> GET /api/v1/folders/{FolderId}/contents
- "List all groups?" -> GET /api/v1/groups
- "List all subscriptions?" -> GET /api/v1/organizations/{OrganizationId}/subscriptions
- "List all permissions?" -> GET /api/v1/resources/{ResourceId}/permissions
- "List all root?" -> GET /api/v1/me/root
- "Search users?" -> GET /api/v1/users
- "List all me?" -> GET /api/v1/me
- "Get document details?" -> GET /api/v1/documents/{DocumentId}
- "List all path?" -> GET /api/v1/documents/{DocumentId}/path
- "Get version details?" -> GET /api/v1/documents/{DocumentId}/versions/{VersionId}
- "Get folder details?" -> GET /api/v1/folders/{FolderId}
- "List all path?" -> GET /api/v1/folders/{FolderId}/path
- "List all resources?" -> GET /api/v1/resources
- "Create a document?" -> POST /api/v1/documents
- "Delete a permission?" -> DELETE /api/v1/resources/{ResourceId}/permissions/{PrincipalId}
- "Create a search?" -> POST /api/v1/search
- "Partially update a document?" -> PATCH /api/v1/documents/{DocumentId}
- "Partially update a version?" -> PATCH /api/v1/documents/{DocumentId}/versions/{VersionId}
- "Partially update a folder?" -> PATCH /api/v1/folders/{FolderId}
- "Partially update a user?" -> PATCH /api/v1/users/{UserId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
