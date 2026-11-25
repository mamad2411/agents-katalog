---
name: graphrbacmanagementclient
description: "GraphRbacManagementClient API skill. Use when working with GraphRbacManagementClient for {tenantID}. Covers 56 endpoints."
version: 1.0.0
generator: lapsh
---

# GraphRbacManagementClient
API version: 1.6

## Auth
OAuth2

## Base URL
https://graph.windows.net

## Setup
1. Configure auth: OAuth2
2. GET /{tenantID}/me -- verify access
3. POST /{tenantID}/applications -- create first applications

## Endpoints

56 endpoints across 1 groups. See references/api-spec.lap for full details.

### {tenantID}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{tenantID}/me | Gets the details for the currently logged-in user. |
| GET | /{tenantID}/me/ownedObjects | Get the list of directory objects that are owned by the user. |
| POST | /{tenantID}/applications | Create a new application. |
| GET | /{tenantID}/applications | Lists applications by filter parameters. |
| POST | /{tenantID}/deletedApplications/{objectId}/restore | Restores the deleted application in the directory. |
| GET | /{tenantID}/deletedApplications | Gets a list of deleted applications in the directory. |
| DELETE | /{tenantID}/deletedApplications/{applicationObjectId} | Hard-delete an application. |
| DELETE | /{tenantID}/applications/{applicationObjectId} | Delete an application. |
| GET | /{tenantID}/applications/{applicationObjectId} | Get an application by object ID. |
| PATCH | /{tenantID}/applications/{applicationObjectId} | Update an existing application. |
| GET | /{tenantID}/applications/{applicationObjectId}/owners | Directory objects that are owners of the application. |
| POST | /{tenantID}/applications/{applicationObjectId}/$links/owners | Add an owner to an application. |
| DELETE | /{tenantID}/applications/{applicationObjectId}/$links/owners/{ownerObjectId} | Remove a member from owners. |
| GET | /{tenantID}/applications/{applicationObjectId}/keyCredentials | Get the keyCredentials associated with an application. |
| PATCH | /{tenantID}/applications/{applicationObjectId}/keyCredentials | Update the keyCredentials associated with an application. |
| GET | /{tenantID}/applications/{applicationObjectId}/passwordCredentials | Get the passwordCredentials associated with an application. |
| PATCH | /{tenantID}/applications/{applicationObjectId}/passwordCredentials | Update passwordCredentials associated with an application. |
| POST | /{tenantID}/isMemberOf | Checks whether the specified user, group, contact, or service principal is a direct or transitive member of the specified group. |
| DELETE | /{tenantID}/groups/{groupObjectId}/$links/members/{memberObjectId} | Remove a member from a group. |
| POST | /{tenantID}/groups/{groupObjectId}/$links/members | Add a member to a group. |
| POST | /{tenantID}/groups | Create a group in the directory. |
| GET | /{tenantID}/groups | Gets list of groups for the current tenant. |
| GET | /{tenantID}/groups/{objectId}/members | Gets the members of a group. |
| GET | /{tenantID}/groups/{objectId} | Gets group information from the directory. |
| DELETE | /{tenantID}/groups/{objectId} | Delete a group from the directory. |
| POST | /{tenantID}/groups/{objectId}/getMemberGroups | Gets a collection of object IDs of groups of which the specified group is a member. |
| GET | /{tenantID}/groups/{objectId}/owners | Directory objects that are owners of the group. |
| POST | /{tenantID}/groups/{objectId}/$links/owners | Add an owner to a group. |
| DELETE | /{tenantID}/groups/{objectId}/$links/owners/{ownerObjectId} | Remove a member from owners. |
| POST | /{tenantID}/servicePrincipals | Creates a service principal in the directory. |
| GET | /{tenantID}/servicePrincipals | Gets a list of service principals from the current tenant. |
| GET | /{tenantID}/servicePrincipalsByAppId/{applicationID}/objectId | Gets an object id for a given application id from the current tenant. |
| PATCH | /{tenantID}/servicePrincipals/{objectId} | Updates a service principal in the directory. |
| DELETE | /{tenantID}/servicePrincipals/{objectId} | Deletes a service principal from the directory. |
| GET | /{tenantID}/servicePrincipals/{objectId} | Gets service principal information from the directory. Query by objectId or pass a filter to query by appId |
| GET | /{tenantID}/servicePrincipals/{objectId}/appRoleAssignedTo | Principals (users, groups, and service principals) that are assigned to this service principal. |
| GET | /{tenantID}/servicePrincipals/{objectId}/appRoleAssignments | Applications that the service principal is assigned to. |
| GET | /{tenantID}/servicePrincipals/{objectId}/owners | Directory objects that are owners of this service principal. |
| POST | /{tenantID}/servicePrincipals/{objectId}/$links/owners | Add an owner to a service principal. |
| DELETE | /{tenantID}/servicePrincipals/{objectId}/$links/owners/{ownerObjectId} | Remove a member from owners. |
| GET | /{tenantID}/servicePrincipals/{objectId}/keyCredentials | Get the keyCredentials associated with the specified service principal. |
| PATCH | /{tenantID}/servicePrincipals/{objectId}/keyCredentials | Update the keyCredentials associated with a service principal. |
| GET | /{tenantID}/servicePrincipals/{objectId}/passwordCredentials | Gets the passwordCredentials associated with a service principal. |
| PATCH | /{tenantID}/servicePrincipals/{objectId}/passwordCredentials | Updates the passwordCredentials associated with a service principal. |
| POST | /{tenantID}/users | Create a new user. |
| GET | /{tenantID}/users | Gets list of users for the current tenant. |
| GET | /{tenantID}/users/{upnOrObjectId} | Gets user information from the directory. |
| PATCH | /{tenantID}/users/{upnOrObjectId} | Updates a user. |
| DELETE | /{tenantID}/users/{upnOrObjectId} | Delete a user. |
| POST | /{tenantID}/users/{objectId}/getMemberGroups | Gets a collection that contains the object IDs of the groups of which the user is a member. |
| POST | /{tenantID}/getObjectsByObjectIds | Gets the directory objects specified in a list of object IDs. You can also specify which resource collections (users, groups, etc.) should be searched by specifying the optional types parameter. |
| GET | /{tenantID}/domains | Gets a list of domains for the current tenant. |
| GET | /{tenantID}/domains/{domainName} | Gets a specific domain in the current tenant. |
| GET | /{tenantID}/oauth2PermissionGrants | Queries OAuth2 permissions grants for the relevant SP ObjectId of an app. |
| POST | /{tenantID}/oauth2PermissionGrants | Grants OAuth2 permissions for the relevant resource Ids of an app. |
| DELETE | /{tenantID}/oauth2PermissionGrants/{objectId} | Delete a OAuth2 permission grant for the relevant resource Ids of an app. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all me?" -> GET /{tenantID}/me
- "List all ownedObjects?" -> GET /{tenantID}/me/ownedObjects
- "Create a application?" -> POST /{tenantID}/applications
- "List all applications?" -> GET /{tenantID}/applications
- "Create a restore?" -> POST /{tenantID}/deletedApplications/{objectId}/restore
- "List all deletedApplications?" -> GET /{tenantID}/deletedApplications
- "Delete a deletedApplication?" -> DELETE /{tenantID}/deletedApplications/{applicationObjectId}
- "Delete a application?" -> DELETE /{tenantID}/applications/{applicationObjectId}
- "Get application details?" -> GET /{tenantID}/applications/{applicationObjectId}
- "Partially update a application?" -> PATCH /{tenantID}/applications/{applicationObjectId}
- "List all owners?" -> GET /{tenantID}/applications/{applicationObjectId}/owners
- "Create a owner?" -> POST /{tenantID}/applications/{applicationObjectId}/$links/owners
- "Delete a owner?" -> DELETE /{tenantID}/applications/{applicationObjectId}/$links/owners/{ownerObjectId}
- "List all keyCredentials?" -> GET /{tenantID}/applications/{applicationObjectId}/keyCredentials
- "List all passwordCredentials?" -> GET /{tenantID}/applications/{applicationObjectId}/passwordCredentials
- "Create a isMemberOf?" -> POST /{tenantID}/isMemberOf
- "Delete a member?" -> DELETE /{tenantID}/groups/{groupObjectId}/$links/members/{memberObjectId}
- "Create a member?" -> POST /{tenantID}/groups/{groupObjectId}/$links/members
- "Create a group?" -> POST /{tenantID}/groups
- "List all groups?" -> GET /{tenantID}/groups
- "List all members?" -> GET /{tenantID}/groups/{objectId}/members
- "Get group details?" -> GET /{tenantID}/groups/{objectId}
- "Delete a group?" -> DELETE /{tenantID}/groups/{objectId}
- "Create a getMemberGroup?" -> POST /{tenantID}/groups/{objectId}/getMemberGroups
- "List all owners?" -> GET /{tenantID}/groups/{objectId}/owners
- "Create a owner?" -> POST /{tenantID}/groups/{objectId}/$links/owners
- "Delete a owner?" -> DELETE /{tenantID}/groups/{objectId}/$links/owners/{ownerObjectId}
- "Create a servicePrincipal?" -> POST /{tenantID}/servicePrincipals
- "List all servicePrincipals?" -> GET /{tenantID}/servicePrincipals
- "List all objectId?" -> GET /{tenantID}/servicePrincipalsByAppId/{applicationID}/objectId
- "Partially update a servicePrincipal?" -> PATCH /{tenantID}/servicePrincipals/{objectId}
- "Delete a servicePrincipal?" -> DELETE /{tenantID}/servicePrincipals/{objectId}
- "Get servicePrincipal details?" -> GET /{tenantID}/servicePrincipals/{objectId}
- "List all appRoleAssignedTo?" -> GET /{tenantID}/servicePrincipals/{objectId}/appRoleAssignedTo
- "List all appRoleAssignments?" -> GET /{tenantID}/servicePrincipals/{objectId}/appRoleAssignments
- "List all owners?" -> GET /{tenantID}/servicePrincipals/{objectId}/owners
- "Create a owner?" -> POST /{tenantID}/servicePrincipals/{objectId}/$links/owners
- "Delete a owner?" -> DELETE /{tenantID}/servicePrincipals/{objectId}/$links/owners/{ownerObjectId}
- "List all keyCredentials?" -> GET /{tenantID}/servicePrincipals/{objectId}/keyCredentials
- "List all passwordCredentials?" -> GET /{tenantID}/servicePrincipals/{objectId}/passwordCredentials
- "Create a user?" -> POST /{tenantID}/users
- "List all users?" -> GET /{tenantID}/users
- "Get user details?" -> GET /{tenantID}/users/{upnOrObjectId}
- "Partially update a user?" -> PATCH /{tenantID}/users/{upnOrObjectId}
- "Delete a user?" -> DELETE /{tenantID}/users/{upnOrObjectId}
- "Create a getMemberGroup?" -> POST /{tenantID}/users/{objectId}/getMemberGroups
- "Create a getObjectsByObjectId?" -> POST /{tenantID}/getObjectsByObjectIds
- "List all domains?" -> GET /{tenantID}/domains
- "Get domain details?" -> GET /{tenantID}/domains/{domainName}
- "List all oauth2PermissionGrants?" -> GET /{tenantID}/oauth2PermissionGrants
- "Create a oauth2PermissionGrant?" -> POST /{tenantID}/oauth2PermissionGrants
- "Delete a oauth2PermissionGrant?" -> DELETE /{tenantID}/oauth2PermissionGrants/{objectId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
