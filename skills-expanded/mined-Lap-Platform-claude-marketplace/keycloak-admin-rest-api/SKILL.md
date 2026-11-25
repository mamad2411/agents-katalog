---
name: keycloak-admin-rest-api
description: "Keycloak Admin REST API skill. Use when working with Keycloak Admin REST for root, {id}, {realm}. Covers 281 endpoints."
version: 1.0.0
generator: lapsh
---

# Keycloak Admin REST API
API version: 1

## Auth
Bearer bearer

## Base URL
Not specified.

## Setup
1. Set Authorization header with your Bearer token
2. GET / -- verify access
3. POST / -- create first resource

## Endpoints

281 endpoints across 3 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Get themes, social providers, auth providers, and event listeners available on this server |
| POST | / | Import a realm   Imports a realm from a full representation of that realm. |

### {id}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{id}/name | Need this for admin console to display simple name of provider when displaying client detail   KEYCLOAK-4328 |

### {realm}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{realm} | Get the top-level representation of the realm   It will not include nested information like User and Client representations. |
| PUT | /{realm} | Update the top-level information of the realm   Any user, roles or client information in the representation  will be ignored. |
| DELETE | /{realm} | Delete the realm |
| GET | /{realm}/admin-events | Get admin events   Returns all admin events, or filters events based on URL query parameters listed here |
| DELETE | /{realm}/admin-events | Delete all admin events |
| DELETE | /{realm}/attack-detection/brute-force/users | Clear any user login failures for all users   This can release temporary disabled users |
| GET | /{realm}/attack-detection/brute-force/users/{userId} | Get status of a username in brute force detection |
| DELETE | /{realm}/attack-detection/brute-force/users/{userId} | Clear any user login failures for the user   This can release temporary disabled user |
| GET | /{realm}/authentication/authenticator-providers | Get authenticator providers   Returns a list of authenticator providers. |
| GET | /{realm}/authentication/client-authenticator-providers | Get client authenticator providers   Returns a list of client authenticator providers. |
| GET | /{realm}/authentication/config-description/{providerId} | Get authenticator provider’s configuration description |
| GET | /{realm}/authentication/config/{id} | Get authenticator configuration |
| PUT | /{realm}/authentication/config/{id} | Update authenticator configuration |
| DELETE | /{realm}/authentication/config/{id} | Delete authenticator configuration |
| POST | /{realm}/authentication/executions | Add new authentication execution |
| GET | /{realm}/authentication/executions/{executionId} | Get Single Execution |
| DELETE | /{realm}/authentication/executions/{executionId} | Delete execution |
| POST | /{realm}/authentication/executions/{executionId}/config | Update execution with new configuration |
| POST | /{realm}/authentication/executions/{executionId}/lower-priority | Lower execution’s priority |
| POST | /{realm}/authentication/executions/{executionId}/raise-priority | Raise execution’s priority |
| GET | /{realm}/authentication/flows | Get authentication flows   Returns a list of authentication flows. |
| POST | /{realm}/authentication/flows | Create a new authentication flow |
| POST | /{realm}/authentication/flows/{flowAlias}/copy | Copy existing authentication flow under a new name   The new name is given as 'newName' attribute of the passed JSON object |
| GET | /{realm}/authentication/flows/{flowAlias}/executions | Get authentication executions for a flow |
| PUT | /{realm}/authentication/flows/{flowAlias}/executions | Update authentication executions of a flow |
| POST | /{realm}/authentication/flows/{flowAlias}/executions/execution | Add new authentication execution to a flow |
| POST | /{realm}/authentication/flows/{flowAlias}/executions/flow | Add new flow with new execution to existing flow |
| GET | /{realm}/authentication/flows/{id} | Get authentication flow for id |
| PUT | /{realm}/authentication/flows/{id} | Update an authentication flow |
| DELETE | /{realm}/authentication/flows/{id} | Delete an authentication flow |
| GET | /{realm}/authentication/form-action-providers | Get form action providers   Returns a list of form action providers. |
| GET | /{realm}/authentication/form-providers | Get form providers   Returns a list of form providers. |
| GET | /{realm}/authentication/per-client-config-description | Get configuration descriptions for all clients |
| POST | /{realm}/authentication/register-required-action | Register a new required actions |
| GET | /{realm}/authentication/required-actions | Get required actions   Returns a list of required actions. |
| GET | /{realm}/authentication/required-actions/{alias} | Get required action for alias |
| PUT | /{realm}/authentication/required-actions/{alias} | Update required action |
| DELETE | /{realm}/authentication/required-actions/{alias} | Delete required action |
| POST | /{realm}/authentication/required-actions/{alias}/lower-priority | Lower required action’s priority |
| POST | /{realm}/authentication/required-actions/{alias}/raise-priority | Raise required action’s priority |
| GET | /{realm}/authentication/unregistered-required-actions | Get unregistered required actions   Returns a list of unregistered required actions. |
| POST | /{realm}/clear-keys-cache | Clear cache of external public keys (Public keys of clients or Identity providers) |
| POST | /{realm}/clear-realm-cache | Clear realm cache |
| POST | /{realm}/clear-user-cache | Clear user cache |
| POST | /{realm}/client-description-converter | Base path for importing clients under this realm. |
| GET | /{realm}/client-registration-policy/providers | Base path for retrieve providers with the configProperties properly filled |
| GET | /{realm}/client-scopes | Get client scopes belonging to the realm   Returns a list of client scopes belonging to the realm |
| POST | /{realm}/client-scopes | Create a new client scope   Client Scope’s name must be unique! |
| GET | /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2} | Get mapper by id |
| PUT | /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2} | Update the mapper |
| DELETE | /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2} | Delete the mapper |
| GET | /{realm}/client-scopes/{id} | Get representation of the client scope |
| PUT | /{realm}/client-scopes/{id} | Update the client scope |
| DELETE | /{realm}/client-scopes/{id} | Delete the client scope |
| POST | /{realm}/client-scopes/{id}/protocol-mappers/add-models | Create multiple mappers |
| GET | /{realm}/client-scopes/{id}/protocol-mappers/models | Get mappers |
| POST | /{realm}/client-scopes/{id}/protocol-mappers/models | Create a mapper |
| GET | /{realm}/client-scopes/{id}/protocol-mappers/protocol/{protocol} | Get mappers by name for a specific protocol |
| GET | /{realm}/client-scopes/{id}/scope-mappings | Get all scope mappings for the client |
| GET | /{realm}/client-scopes/{id}/scope-mappings/clients/{client} | Get the roles associated with a client’s scope   Returns roles for the client. |
| POST | /{realm}/client-scopes/{id}/scope-mappings/clients/{client} | Add client-level roles to the client’s scope |
| DELETE | /{realm}/client-scopes/{id}/scope-mappings/clients/{client} | Remove client-level roles from the client’s scope. |
| GET | /{realm}/client-scopes/{id}/scope-mappings/clients/{client}/available | The available client-level roles   Returns the roles for the client that can be associated with the client’s scope |
| GET | /{realm}/client-scopes/{id}/scope-mappings/clients/{client}/composite | Get effective client roles   Returns the roles for the client that are associated with the client’s scope. |
| GET | /{realm}/client-scopes/{id}/scope-mappings/realm | Get realm-level roles associated with the client’s scope |
| POST | /{realm}/client-scopes/{id}/scope-mappings/realm | Add a set of realm-level roles to the client’s scope |
| DELETE | /{realm}/client-scopes/{id}/scope-mappings/realm | Remove a set of realm-level roles from the client’s scope |
| GET | /{realm}/client-scopes/{id}/scope-mappings/realm/available | Get realm-level roles that are available to attach to this client’s scope |
| GET | /{realm}/client-scopes/{id}/scope-mappings/realm/composite | Get effective realm-level roles associated with the client’s scope   What this does is recurse  any composite roles associated with the client’s scope and adds the roles to this lists. |
| GET | /{realm}/client-session-stats | Get client session stats   Returns a JSON map. |
| GET | /{realm}/clients | Get clients belonging to the realm   Returns a list of clients belonging to the realm |
| POST | /{realm}/clients | Create a new client   Client’s client_id must be unique! |
| GET | /{realm}/clients-initial-access |  |
| POST | /{realm}/clients-initial-access | Create a new initial access token. |
| DELETE | /{realm}/clients-initial-access/{id} |  |
| GET | /{realm}/clients/{id1}/protocol-mappers/models/{id2} | Get mapper by id |
| PUT | /{realm}/clients/{id1}/protocol-mappers/models/{id2} | Update the mapper |
| DELETE | /{realm}/clients/{id1}/protocol-mappers/models/{id2} | Delete the mapper |
| GET | /{realm}/clients/{id} | Get representation of the client |
| PUT | /{realm}/clients/{id} | Update the client |
| DELETE | /{realm}/clients/{id} | Delete the client |
| GET | /{realm}/clients/{id}/certificates/{attr} | Get key info |
| POST | /{realm}/clients/{id}/certificates/{attr}/download | Get a keystore file for the client, containing private key and public certificate |
| POST | /{realm}/clients/{id}/certificates/{attr}/generate | Generate a new certificate with new key pair |
| POST | /{realm}/clients/{id}/certificates/{attr}/generate-and-download | Generate a new keypair and certificate, and get the private key file   Generates a keypair and certificate and serves the private key in a specified keystore format. |
| POST | /{realm}/clients/{id}/certificates/{attr}/upload | Upload certificate and eventually private key |
| POST | /{realm}/clients/{id}/certificates/{attr}/upload-certificate | Upload only certificate, not private key |
| GET | /{realm}/clients/{id}/client-secret | Get the client secret |
| POST | /{realm}/clients/{id}/client-secret | Generate a new secret for the client |
| GET | /{realm}/clients/{id}/default-client-scopes | Get default client scopes. |
| PUT | /{realm}/clients/{id}/default-client-scopes/{clientScopeId} |  |
| DELETE | /{realm}/clients/{id}/default-client-scopes/{clientScopeId} |  |
| GET | /{realm}/clients/{id}/evaluate-scopes/generate-example-access-token | Create JSON with payload of example access token |
| GET | /{realm}/clients/{id}/evaluate-scopes/protocol-mappers | Return list of all protocol mappers, which will be used when generating tokens issued for particular client. |
| GET | /{realm}/clients/{id}/evaluate-scopes/scope-mappings/{roleContainerId}/granted | Get effective scope mapping of all roles of particular role container, which this client is defacto allowed to have in the accessToken issued for him. |
| GET | /{realm}/clients/{id}/evaluate-scopes/scope-mappings/{roleContainerId}/not-granted | Get roles, which this client doesn’t have scope for and can’t have them in the accessToken issued for him. |
| GET | /{realm}/clients/{id}/installation/providers/{providerId} |  |
| GET | /{realm}/clients/{id}/management/permissions | Return object stating whether client Authorization permissions have been initialized or not and a reference |
| PUT | /{realm}/clients/{id}/management/permissions | Return object stating whether client Authorization permissions have been initialized or not and a reference |
| POST | /{realm}/clients/{id}/nodes | Register a cluster node with the client   Manually register cluster node to this client - usually it’s not needed to call this directly as adapter should handle  by sending registration request to Keycloak |
| DELETE | /{realm}/clients/{id}/nodes/{node} | Unregister a cluster node from the client |
| GET | /{realm}/clients/{id}/offline-session-count | Get application offline session count   Returns a number of offline user sessions associated with this client   {      "count": number  } |
| GET | /{realm}/clients/{id}/offline-sessions | Get offline sessions for client   Returns a list of offline user sessions associated with this client |
| GET | /{realm}/clients/{id}/optional-client-scopes | Get optional client scopes. |
| PUT | /{realm}/clients/{id}/optional-client-scopes/{clientScopeId} |  |
| DELETE | /{realm}/clients/{id}/optional-client-scopes/{clientScopeId} |  |
| POST | /{realm}/clients/{id}/protocol-mappers/add-models | Create multiple mappers |
| GET | /{realm}/clients/{id}/protocol-mappers/models | Get mappers |
| POST | /{realm}/clients/{id}/protocol-mappers/models | Create a mapper |
| GET | /{realm}/clients/{id}/protocol-mappers/protocol/{protocol} | Get mappers by name for a specific protocol |
| POST | /{realm}/clients/{id}/push-revocation | Push the client’s revocation policy to its admin URL   If the client has an admin URL, push revocation policy to it. |
| POST | /{realm}/clients/{id}/registration-access-token | Generate a new registration access token for the client |
| GET | /{realm}/clients/{id}/roles | Get all roles for the realm or client |
| POST | /{realm}/clients/{id}/roles | Create a new role for the realm or client |
| GET | /{realm}/clients/{id}/roles/{role-name} | Get a role by name |
| PUT | /{realm}/clients/{id}/roles/{role-name} | Update a role by name |
| DELETE | /{realm}/clients/{id}/roles/{role-name} | Delete a role by name |
| GET | /{realm}/clients/{id}/roles/{role-name}/composites | Get composites of the role |
| POST | /{realm}/clients/{id}/roles/{role-name}/composites | Add a composite to the role |
| DELETE | /{realm}/clients/{id}/roles/{role-name}/composites | Remove roles from the role’s composite |
| GET | /{realm}/clients/{id}/roles/{role-name}/composites/clients/{client} | An app-level roles for the specified app for the role’s composite |
| GET | /{realm}/clients/{id}/roles/{role-name}/composites/realm | Get realm-level roles of the role’s composite |
| GET | /{realm}/clients/{id}/roles/{role-name}/groups | Return List of Groups that have the specified role name |
| GET | /{realm}/clients/{id}/roles/{role-name}/management/permissions | Return object stating whether role Authoirzation permissions have been initialized or not and a reference |
| PUT | /{realm}/clients/{id}/roles/{role-name}/management/permissions | Return object stating whether role Authoirzation permissions have been initialized or not and a reference |
| GET | /{realm}/clients/{id}/roles/{role-name}/users | Return List of Users that have the specified role name |
| GET | /{realm}/clients/{id}/scope-mappings | Get all scope mappings for the client |
| GET | /{realm}/clients/{id}/scope-mappings/clients/{client} | Get the roles associated with a client’s scope   Returns roles for the client. |
| POST | /{realm}/clients/{id}/scope-mappings/clients/{client} | Add client-level roles to the client’s scope |
| DELETE | /{realm}/clients/{id}/scope-mappings/clients/{client} | Remove client-level roles from the client’s scope. |
| GET | /{realm}/clients/{id}/scope-mappings/clients/{client}/available | The available client-level roles   Returns the roles for the client that can be associated with the client’s scope |
| GET | /{realm}/clients/{id}/scope-mappings/clients/{client}/composite | Get effective client roles   Returns the roles for the client that are associated with the client’s scope. |
| GET | /{realm}/clients/{id}/scope-mappings/realm | Get realm-level roles associated with the client’s scope |
| POST | /{realm}/clients/{id}/scope-mappings/realm | Add a set of realm-level roles to the client’s scope |
| DELETE | /{realm}/clients/{id}/scope-mappings/realm | Remove a set of realm-level roles from the client’s scope |
| GET | /{realm}/clients/{id}/scope-mappings/realm/available | Get realm-level roles that are available to attach to this client’s scope |
| GET | /{realm}/clients/{id}/scope-mappings/realm/composite | Get effective realm-level roles associated with the client’s scope   What this does is recurse  any composite roles associated with the client’s scope and adds the roles to this lists. |
| GET | /{realm}/clients/{id}/service-account-user | Get a user dedicated to the service account |
| GET | /{realm}/clients/{id}/session-count | Get application session count   Returns a number of user sessions associated with this client   {      "count": number  } |
| GET | /{realm}/clients/{id}/test-nodes-available | Test if registered cluster nodes are available   Tests availability by sending 'ping' request to all cluster nodes. |
| GET | /{realm}/clients/{id}/user-sessions | Get user sessions for client   Returns a list of user sessions associated with this client |
| GET | /{realm}/components |  |
| POST | /{realm}/components |  |
| GET | /{realm}/components/{id} |  |
| PUT | /{realm}/components/{id} |  |
| DELETE | /{realm}/components/{id} |  |
| GET | /{realm}/components/{id}/sub-component-types | List of subcomponent types that are available to configure for a particular parent component. |
| GET | /{realm}/credential-registrators |  |
| GET | /{realm}/default-default-client-scopes | Get realm default client scopes. |
| PUT | /{realm}/default-default-client-scopes/{clientScopeId} |  |
| DELETE | /{realm}/default-default-client-scopes/{clientScopeId} |  |
| GET | /{realm}/default-groups | Get group hierarchy. |
| PUT | /{realm}/default-groups/{groupId} |  |
| DELETE | /{realm}/default-groups/{groupId} |  |
| GET | /{realm}/default-optional-client-scopes | Get realm optional client scopes. |
| PUT | /{realm}/default-optional-client-scopes/{clientScopeId} |  |
| DELETE | /{realm}/default-optional-client-scopes/{clientScopeId} |  |
| GET | /{realm}/events | Get events   Returns all events, or filters them based on URL query parameters listed here |
| DELETE | /{realm}/events | Delete all events |
| GET | /{realm}/events/config | Get the events provider configuration   Returns JSON object with events provider configuration |
| PUT | /{realm}/events/config | Update the events provider   Change the events provider and/or its configuration |
| GET | /{realm}/group-by-path/{path} |  |
| GET | /{realm}/groups | Get group hierarchy. |
| POST | /{realm}/groups | create or add a top level realm groupSet or create child. |
| GET | /{realm}/groups/count | Returns the groups counts. |
| GET | /{realm}/groups/{id} |  |
| PUT | /{realm}/groups/{id} | Update group, ignores subgroups. |
| DELETE | /{realm}/groups/{id} |  |
| POST | /{realm}/groups/{id}/children | Set or create child. |
| GET | /{realm}/groups/{id}/management/permissions | Return object stating whether client Authorization permissions have been initialized or not and a reference |
| PUT | /{realm}/groups/{id}/management/permissions | Return object stating whether client Authorization permissions have been initialized or not and a reference |
| GET | /{realm}/groups/{id}/members | Get users   Returns a list of users, filtered according to query parameters |
| GET | /{realm}/groups/{id}/role-mappings | Get role mappings |
| GET | /{realm}/groups/{id}/role-mappings/clients/{client} | Get client-level role mappings for the user, and the app |
| POST | /{realm}/groups/{id}/role-mappings/clients/{client} | Add client-level roles to the user role mapping |
| DELETE | /{realm}/groups/{id}/role-mappings/clients/{client} | Delete client-level roles from user role mapping |
| GET | /{realm}/groups/{id}/role-mappings/clients/{client}/available | Get available client-level roles that can be mapped to the user |
| GET | /{realm}/groups/{id}/role-mappings/clients/{client}/composite | Get effective client-level role mappings   This recurses any composite roles |
| GET | /{realm}/groups/{id}/role-mappings/realm | Get realm-level role mappings |
| POST | /{realm}/groups/{id}/role-mappings/realm | Add realm-level role mappings to the user |
| DELETE | /{realm}/groups/{id}/role-mappings/realm | Delete realm-level role mappings |
| GET | /{realm}/groups/{id}/role-mappings/realm/available | Get realm-level roles that can be mapped |
| GET | /{realm}/groups/{id}/role-mappings/realm/composite | Get effective realm-level role mappings   This will recurse all composite roles to get the result. |
| POST | /{realm}/identity-provider/import-config | Import identity provider from uploaded JSON file |
| GET | /{realm}/identity-provider/instances | Get identity providers |
| POST | /{realm}/identity-provider/instances | Create a new identity provider |
| GET | /{realm}/identity-provider/instances/{alias} | Get the identity provider |
| PUT | /{realm}/identity-provider/instances/{alias} | Update the identity provider |
| DELETE | /{realm}/identity-provider/instances/{alias} | Delete the identity provider |
| GET | /{realm}/identity-provider/instances/{alias}/export | Export public broker configuration for identity provider |
| GET | /{realm}/identity-provider/instances/{alias}/management/permissions | Return object stating whether client Authorization permissions have been initialized or not and a reference |
| PUT | /{realm}/identity-provider/instances/{alias}/management/permissions | Return object stating whether client Authorization permissions have been initialized or not and a reference |
| GET | /{realm}/identity-provider/instances/{alias}/mapper-types | Get mapper types for identity provider |
| GET | /{realm}/identity-provider/instances/{alias}/mappers | Get mappers for identity provider |
| POST | /{realm}/identity-provider/instances/{alias}/mappers | Add a mapper to identity provider |
| GET | /{realm}/identity-provider/instances/{alias}/mappers/{id} | Get mapper by id for the identity provider |
| PUT | /{realm}/identity-provider/instances/{alias}/mappers/{id} | Update a mapper for the identity provider |
| DELETE | /{realm}/identity-provider/instances/{alias}/mappers/{id} | Delete a mapper for the identity provider |
| GET | /{realm}/identity-provider/providers/{provider_id} | Get identity providers |
| GET | /{realm}/keys |  |
| POST | /{realm}/logout-all | Removes all user sessions. |
| POST | /{realm}/partial-export | Partial export of existing realm into a JSON file. |
| POST | /{realm}/partialImport | Partial import from a JSON file to an existing realm. |
| POST | /{realm}/push-revocation | Push the realm’s revocation policy to any client that has an admin url associated with it. |
| GET | /{realm}/roles | Get all roles for the realm or client |
| POST | /{realm}/roles | Create a new role for the realm or client |
| GET | /{realm}/roles-by-id/{role-id} | Get a specific role’s representation |
| PUT | /{realm}/roles-by-id/{role-id} | Update the role |
| DELETE | /{realm}/roles-by-id/{role-id} | Delete the role |
| GET | /{realm}/roles-by-id/{role-id}/composites | Get role’s children   Returns a set of role’s children provided the role is a composite. |
| POST | /{realm}/roles-by-id/{role-id}/composites | Make the role a composite role by associating some child roles |
| DELETE | /{realm}/roles-by-id/{role-id}/composites | Remove a set of roles from the role’s composite |
| GET | /{realm}/roles-by-id/{role-id}/composites/clients/{client} | Get client-level roles for the client that are in the role’s composite |
| GET | /{realm}/roles-by-id/{role-id}/composites/realm | Get realm-level roles that are in the role’s composite |
| GET | /{realm}/roles-by-id/{role-id}/management/permissions | Return object stating whether role Authoirzation permissions have been initialized or not and a reference |
| PUT | /{realm}/roles-by-id/{role-id}/management/permissions | Return object stating whether role Authoirzation permissions have been initialized or not and a reference |
| GET | /{realm}/roles/{role-name} | Get a role by name |
| PUT | /{realm}/roles/{role-name} | Update a role by name |
| DELETE | /{realm}/roles/{role-name} | Delete a role by name |
| GET | /{realm}/roles/{role-name}/composites | Get composites of the role |
| POST | /{realm}/roles/{role-name}/composites | Add a composite to the role |
| DELETE | /{realm}/roles/{role-name}/composites | Remove roles from the role’s composite |
| GET | /{realm}/roles/{role-name}/composites/clients/{client} | An app-level roles for the specified app for the role’s composite |
| GET | /{realm}/roles/{role-name}/composites/realm | Get realm-level roles of the role’s composite |
| GET | /{realm}/roles/{role-name}/groups | Return List of Groups that have the specified role name |
| GET | /{realm}/roles/{role-name}/management/permissions | Return object stating whether role Authoirzation permissions have been initialized or not and a reference |
| PUT | /{realm}/roles/{role-name}/management/permissions | Return object stating whether role Authoirzation permissions have been initialized or not and a reference |
| GET | /{realm}/roles/{role-name}/users | Return List of Users that have the specified role name |
| DELETE | /{realm}/sessions/{session} | Remove a specific user session. |
| POST | /{realm}/testLDAPConnection | Test LDAP connection |
| POST | /{realm}/testSMTPConnection |  |
| GET | /{realm}/user-storage/{id}/name | Need this for admin console to display simple name of provider when displaying user detail   KEYCLOAK-4328 |
| POST | /{realm}/user-storage/{id}/remove-imported-users | Remove imported users |
| POST | /{realm}/user-storage/{id}/sync | Trigger sync of users   Action can be "triggerFullSync" or "triggerChangedUsersSync" |
| POST | /{realm}/user-storage/{id}/unlink-users | Unlink imported users from a storage provider |
| POST | /{realm}/user-storage/{parentId}/mappers/{id}/sync | Trigger sync of mapper data related to ldap mapper (roles, groups, …​)   direction is "fedToKeycloak" or "keycloakToFed" |
| GET | /{realm}/users | Get users   Returns a list of users, filtered according to query parameters |
| POST | /{realm}/users | Create a new user   Username must be unique. |
| GET | /{realm}/users-management-permissions |  |
| PUT | /{realm}/users-management-permissions |  |
| GET | /{realm}/users/count | Returns the number of users that match the given criteria. |
| GET | /{realm}/users/{id} | Get representation of the user |
| PUT | /{realm}/users/{id} | Update the user |
| DELETE | /{realm}/users/{id} | Delete the user |
| GET | /{realm}/users/{id}/configured-user-storage-credential-types | Return credential types, which are provided by the user storage where user is stored. |
| GET | /{realm}/users/{id}/consents | Get consents granted by the user |
| DELETE | /{realm}/users/{id}/consents/{client} | Revoke consent and offline tokens for particular client from user |
| GET | /{realm}/users/{id}/credentials |  |
| DELETE | /{realm}/users/{id}/credentials/{credentialId} | Remove a credential for a user |
| POST | /{realm}/users/{id}/credentials/{credentialId}/moveAfter/{newPreviousCredentialId} | Move a credential to a position behind another credential |
| POST | /{realm}/users/{id}/credentials/{credentialId}/moveToFirst | Move a credential to a first position in the credentials list of the user |
| PUT | /{realm}/users/{id}/credentials/{credentialId}/userLabel | Update a credential label for a user |
| PUT | /{realm}/users/{id}/disable-credential-types | Disable all credentials for a user of a specific type |
| PUT | /{realm}/users/{id}/execute-actions-email | Send a update account email to the user   An email contains a link the user can click to perform a set of required actions. |
| GET | /{realm}/users/{id}/federated-identity | Get social logins associated with the user |
| POST | /{realm}/users/{id}/federated-identity/{provider} | Add a social login provider to the user |
| DELETE | /{realm}/users/{id}/federated-identity/{provider} | Remove a social login provider from user |
| GET | /{realm}/users/{id}/groups |  |
| GET | /{realm}/users/{id}/groups/count |  |
| PUT | /{realm}/users/{id}/groups/{groupId} |  |
| DELETE | /{realm}/users/{id}/groups/{groupId} |  |
| POST | /{realm}/users/{id}/impersonation | Impersonate the user |
| POST | /{realm}/users/{id}/logout | Remove all user sessions associated with the user   Also send notification to all clients that have an admin URL to invalidate the sessions for the particular user. |
| GET | /{realm}/users/{id}/offline-sessions/{clientId} | Get offline sessions associated with the user and client |
| PUT | /{realm}/users/{id}/reset-password | Set up a new password for the user. |
| GET | /{realm}/users/{id}/role-mappings | Get role mappings |
| GET | /{realm}/users/{id}/role-mappings/clients/{client} | Get client-level role mappings for the user, and the app |
| POST | /{realm}/users/{id}/role-mappings/clients/{client} | Add client-level roles to the user role mapping |
| DELETE | /{realm}/users/{id}/role-mappings/clients/{client} | Delete client-level roles from user role mapping |
| GET | /{realm}/users/{id}/role-mappings/clients/{client}/available | Get available client-level roles that can be mapped to the user |
| GET | /{realm}/users/{id}/role-mappings/clients/{client}/composite | Get effective client-level role mappings   This recurses any composite roles |
| GET | /{realm}/users/{id}/role-mappings/realm | Get realm-level role mappings |
| POST | /{realm}/users/{id}/role-mappings/realm | Add realm-level role mappings to the user |
| DELETE | /{realm}/users/{id}/role-mappings/realm | Delete realm-level role mappings |
| GET | /{realm}/users/{id}/role-mappings/realm/available | Get realm-level roles that can be mapped |
| GET | /{realm}/users/{id}/role-mappings/realm/composite | Get effective realm-level role mappings   This will recurse all composite roles to get the result. |
| PUT | /{realm}/users/{id}/send-verify-email | Send an email-verification email to the user   An email contains a link the user can click to verify their email address. |
| GET | /{realm}/users/{id}/sessions | Get sessions associated with the user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all name?" -> GET /{id}/name
- "List all admin-events?" -> GET /{realm}/admin-events
- "Get user details?" -> GET /{realm}/attack-detection/brute-force/users/{userId}
- "Delete a user?" -> DELETE /{realm}/attack-detection/brute-force/users/{userId}
- "List all authenticator-providers?" -> GET /{realm}/authentication/authenticator-providers
- "List all client-authenticator-providers?" -> GET /{realm}/authentication/client-authenticator-providers
- "Get config-description details?" -> GET /{realm}/authentication/config-description/{providerId}
- "Get config details?" -> GET /{realm}/authentication/config/{id}
- "Update a config?" -> PUT /{realm}/authentication/config/{id}
- "Delete a config?" -> DELETE /{realm}/authentication/config/{id}
- "Create a execution?" -> POST /{realm}/authentication/executions
- "Get execution details?" -> GET /{realm}/authentication/executions/{executionId}
- "Delete a execution?" -> DELETE /{realm}/authentication/executions/{executionId}
- "Create a config?" -> POST /{realm}/authentication/executions/{executionId}/config
- "Create a lower-priority?" -> POST /{realm}/authentication/executions/{executionId}/lower-priority
- "Create a raise-priority?" -> POST /{realm}/authentication/executions/{executionId}/raise-priority
- "List all flows?" -> GET /{realm}/authentication/flows
- "Create a flow?" -> POST /{realm}/authentication/flows
- "Create a copy?" -> POST /{realm}/authentication/flows/{flowAlias}/copy
- "List all executions?" -> GET /{realm}/authentication/flows/{flowAlias}/executions
- "Create a execution?" -> POST /{realm}/authentication/flows/{flowAlias}/executions/execution
- "Create a flow?" -> POST /{realm}/authentication/flows/{flowAlias}/executions/flow
- "Get flow details?" -> GET /{realm}/authentication/flows/{id}
- "Update a flow?" -> PUT /{realm}/authentication/flows/{id}
- "Delete a flow?" -> DELETE /{realm}/authentication/flows/{id}
- "List all form-action-providers?" -> GET /{realm}/authentication/form-action-providers
- "List all form-providers?" -> GET /{realm}/authentication/form-providers
- "List all per-client-config-description?" -> GET /{realm}/authentication/per-client-config-description
- "Create a register-required-action?" -> POST /{realm}/authentication/register-required-action
- "List all required-actions?" -> GET /{realm}/authentication/required-actions
- "Get required-action details?" -> GET /{realm}/authentication/required-actions/{alias}
- "Update a required-action?" -> PUT /{realm}/authentication/required-actions/{alias}
- "Delete a required-action?" -> DELETE /{realm}/authentication/required-actions/{alias}
- "Create a lower-priority?" -> POST /{realm}/authentication/required-actions/{alias}/lower-priority
- "Create a raise-priority?" -> POST /{realm}/authentication/required-actions/{alias}/raise-priority
- "List all unregistered-required-actions?" -> GET /{realm}/authentication/unregistered-required-actions
- "Create a clear-keys-cache?" -> POST /{realm}/clear-keys-cache
- "Create a clear-realm-cache?" -> POST /{realm}/clear-realm-cache
- "Create a clear-user-cache?" -> POST /{realm}/clear-user-cache
- "Create a client-description-converter?" -> POST /{realm}/client-description-converter
- "List all providers?" -> GET /{realm}/client-registration-policy/providers
- "List all client-scopes?" -> GET /{realm}/client-scopes
- "Create a client-scope?" -> POST /{realm}/client-scopes
- "Get model details?" -> GET /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}
- "Update a model?" -> PUT /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}
- "Delete a model?" -> DELETE /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}
- "Get client-scope details?" -> GET /{realm}/client-scopes/{id}
- "Update a client-scope?" -> PUT /{realm}/client-scopes/{id}
- "Delete a client-scope?" -> DELETE /{realm}/client-scopes/{id}
- "Create a add-model?" -> POST /{realm}/client-scopes/{id}/protocol-mappers/add-models
- "List all models?" -> GET /{realm}/client-scopes/{id}/protocol-mappers/models
- "Create a model?" -> POST /{realm}/client-scopes/{id}/protocol-mappers/models
- "Get protocol details?" -> GET /{realm}/client-scopes/{id}/protocol-mappers/protocol/{protocol}
- "List all scope-mappings?" -> GET /{realm}/client-scopes/{id}/scope-mappings
- "Get client details?" -> GET /{realm}/client-scopes/{id}/scope-mappings/clients/{client}
- "Delete a client?" -> DELETE /{realm}/client-scopes/{id}/scope-mappings/clients/{client}
- "List all available?" -> GET /{realm}/client-scopes/{id}/scope-mappings/clients/{client}/available
- "List all composite?" -> GET /{realm}/client-scopes/{id}/scope-mappings/clients/{client}/composite
- "List all realm?" -> GET /{realm}/client-scopes/{id}/scope-mappings/realm
- "Create a realm?" -> POST /{realm}/client-scopes/{id}/scope-mappings/realm
- "List all available?" -> GET /{realm}/client-scopes/{id}/scope-mappings/realm/available
- "List all composite?" -> GET /{realm}/client-scopes/{id}/scope-mappings/realm/composite
- "List all client-session-stats?" -> GET /{realm}/client-session-stats
- "Search clients?" -> GET /{realm}/clients
- "Create a client?" -> POST /{realm}/clients
- "List all clients-initial-access?" -> GET /{realm}/clients-initial-access
- "Create a clients-initial-access?" -> POST /{realm}/clients-initial-access
- "Delete a clients-initial-access?" -> DELETE /{realm}/clients-initial-access/{id}
- "Get model details?" -> GET /{realm}/clients/{id1}/protocol-mappers/models/{id2}
- "Update a model?" -> PUT /{realm}/clients/{id1}/protocol-mappers/models/{id2}
- "Delete a model?" -> DELETE /{realm}/clients/{id1}/protocol-mappers/models/{id2}
- "Get client details?" -> GET /{realm}/clients/{id}
- "Update a client?" -> PUT /{realm}/clients/{id}
- "Delete a client?" -> DELETE /{realm}/clients/{id}
- "Get certificate details?" -> GET /{realm}/clients/{id}/certificates/{attr}
- "Create a download?" -> POST /{realm}/clients/{id}/certificates/{attr}/download
- "Create a generate?" -> POST /{realm}/clients/{id}/certificates/{attr}/generate
- "Create a generate-and-download?" -> POST /{realm}/clients/{id}/certificates/{attr}/generate-and-download
- "Create a upload?" -> POST /{realm}/clients/{id}/certificates/{attr}/upload
- "Create a upload-certificate?" -> POST /{realm}/clients/{id}/certificates/{attr}/upload-certificate
- "List all client-secret?" -> GET /{realm}/clients/{id}/client-secret
- "Create a client-secret?" -> POST /{realm}/clients/{id}/client-secret
- "List all default-client-scopes?" -> GET /{realm}/clients/{id}/default-client-scopes
- "Update a default-client-scope?" -> PUT /{realm}/clients/{id}/default-client-scopes/{clientScopeId}
- "Delete a default-client-scope?" -> DELETE /{realm}/clients/{id}/default-client-scopes/{clientScopeId}
- "List all generate-example-access-token?" -> GET /{realm}/clients/{id}/evaluate-scopes/generate-example-access-token
- "List all protocol-mappers?" -> GET /{realm}/clients/{id}/evaluate-scopes/protocol-mappers
- "List all granted?" -> GET /{realm}/clients/{id}/evaluate-scopes/scope-mappings/{roleContainerId}/granted
- "List all not-granted?" -> GET /{realm}/clients/{id}/evaluate-scopes/scope-mappings/{roleContainerId}/not-granted
- "Get provider details?" -> GET /{realm}/clients/{id}/installation/providers/{providerId}
- "List all permissions?" -> GET /{realm}/clients/{id}/management/permissions
- "Create a node?" -> POST /{realm}/clients/{id}/nodes
- "Delete a node?" -> DELETE /{realm}/clients/{id}/nodes/{node}
- "List all offline-session-count?" -> GET /{realm}/clients/{id}/offline-session-count
- "List all offline-sessions?" -> GET /{realm}/clients/{id}/offline-sessions
- "List all optional-client-scopes?" -> GET /{realm}/clients/{id}/optional-client-scopes
- "Update a optional-client-scope?" -> PUT /{realm}/clients/{id}/optional-client-scopes/{clientScopeId}
- "Delete a optional-client-scope?" -> DELETE /{realm}/clients/{id}/optional-client-scopes/{clientScopeId}
- "Create a add-model?" -> POST /{realm}/clients/{id}/protocol-mappers/add-models
- "List all models?" -> GET /{realm}/clients/{id}/protocol-mappers/models
- "Create a model?" -> POST /{realm}/clients/{id}/protocol-mappers/models
- "Get protocol details?" -> GET /{realm}/clients/{id}/protocol-mappers/protocol/{protocol}
- "Create a push-revocation?" -> POST /{realm}/clients/{id}/push-revocation
- "Create a registration-access-token?" -> POST /{realm}/clients/{id}/registration-access-token
- "Search roles?" -> GET /{realm}/clients/{id}/roles
- "Create a role?" -> POST /{realm}/clients/{id}/roles
- "Get role details?" -> GET /{realm}/clients/{id}/roles/{role-name}
- "Update a role?" -> PUT /{realm}/clients/{id}/roles/{role-name}
- "Delete a role?" -> DELETE /{realm}/clients/{id}/roles/{role-name}
- "List all composites?" -> GET /{realm}/clients/{id}/roles/{role-name}/composites
- "Create a composite?" -> POST /{realm}/clients/{id}/roles/{role-name}/composites
- "Get client details?" -> GET /{realm}/clients/{id}/roles/{role-name}/composites/clients/{client}
- "List all realm?" -> GET /{realm}/clients/{id}/roles/{role-name}/composites/realm
- "List all groups?" -> GET /{realm}/clients/{id}/roles/{role-name}/groups
- "List all permissions?" -> GET /{realm}/clients/{id}/roles/{role-name}/management/permissions
- "List all users?" -> GET /{realm}/clients/{id}/roles/{role-name}/users
- "List all scope-mappings?" -> GET /{realm}/clients/{id}/scope-mappings
- "Get client details?" -> GET /{realm}/clients/{id}/scope-mappings/clients/{client}
- "Delete a client?" -> DELETE /{realm}/clients/{id}/scope-mappings/clients/{client}
- "List all available?" -> GET /{realm}/clients/{id}/scope-mappings/clients/{client}/available
- "List all composite?" -> GET /{realm}/clients/{id}/scope-mappings/clients/{client}/composite
- "List all realm?" -> GET /{realm}/clients/{id}/scope-mappings/realm
- "Create a realm?" -> POST /{realm}/clients/{id}/scope-mappings/realm
- "List all available?" -> GET /{realm}/clients/{id}/scope-mappings/realm/available
- "List all composite?" -> GET /{realm}/clients/{id}/scope-mappings/realm/composite
- "List all service-account-user?" -> GET /{realm}/clients/{id}/service-account-user
- "List all session-count?" -> GET /{realm}/clients/{id}/session-count
- "List all test-nodes-available?" -> GET /{realm}/clients/{id}/test-nodes-available
- "List all user-sessions?" -> GET /{realm}/clients/{id}/user-sessions
- "List all components?" -> GET /{realm}/components
- "Create a component?" -> POST /{realm}/components
- "Get component details?" -> GET /{realm}/components/{id}
- "Update a component?" -> PUT /{realm}/components/{id}
- "Delete a component?" -> DELETE /{realm}/components/{id}
- "List all sub-component-types?" -> GET /{realm}/components/{id}/sub-component-types
- "List all credential-registrators?" -> GET /{realm}/credential-registrators
- "List all default-default-client-scopes?" -> GET /{realm}/default-default-client-scopes
- "Update a default-default-client-scope?" -> PUT /{realm}/default-default-client-scopes/{clientScopeId}
- "Delete a default-default-client-scope?" -> DELETE /{realm}/default-default-client-scopes/{clientScopeId}
- "List all default-groups?" -> GET /{realm}/default-groups
- "Update a default-group?" -> PUT /{realm}/default-groups/{groupId}
- "Delete a default-group?" -> DELETE /{realm}/default-groups/{groupId}
- "List all default-optional-client-scopes?" -> GET /{realm}/default-optional-client-scopes
- "Update a default-optional-client-scope?" -> PUT /{realm}/default-optional-client-scopes/{clientScopeId}
- "Delete a default-optional-client-scope?" -> DELETE /{realm}/default-optional-client-scopes/{clientScopeId}
- "List all events?" -> GET /{realm}/events
- "List all config?" -> GET /{realm}/events/config
- "Get group-by-path details?" -> GET /{realm}/group-by-path/{path}
- "Search groups?" -> GET /{realm}/groups
- "Create a group?" -> POST /{realm}/groups
- "Search count?" -> GET /{realm}/groups/count
- "Get group details?" -> GET /{realm}/groups/{id}
- "Update a group?" -> PUT /{realm}/groups/{id}
- "Delete a group?" -> DELETE /{realm}/groups/{id}
- "Create a children?" -> POST /{realm}/groups/{id}/children
- "List all permissions?" -> GET /{realm}/groups/{id}/management/permissions
- "List all members?" -> GET /{realm}/groups/{id}/members
- "List all role-mappings?" -> GET /{realm}/groups/{id}/role-mappings
- "Get client details?" -> GET /{realm}/groups/{id}/role-mappings/clients/{client}
- "Delete a client?" -> DELETE /{realm}/groups/{id}/role-mappings/clients/{client}
- "List all available?" -> GET /{realm}/groups/{id}/role-mappings/clients/{client}/available
- "List all composite?" -> GET /{realm}/groups/{id}/role-mappings/clients/{client}/composite
- "List all realm?" -> GET /{realm}/groups/{id}/role-mappings/realm
- "Create a realm?" -> POST /{realm}/groups/{id}/role-mappings/realm
- "List all available?" -> GET /{realm}/groups/{id}/role-mappings/realm/available
- "List all composite?" -> GET /{realm}/groups/{id}/role-mappings/realm/composite
- "Create a import-config?" -> POST /{realm}/identity-provider/import-config
- "List all instances?" -> GET /{realm}/identity-provider/instances
- "Create a instance?" -> POST /{realm}/identity-provider/instances
- "Get instance details?" -> GET /{realm}/identity-provider/instances/{alias}
- "Update a instance?" -> PUT /{realm}/identity-provider/instances/{alias}
- "Delete a instance?" -> DELETE /{realm}/identity-provider/instances/{alias}
- "List all export?" -> GET /{realm}/identity-provider/instances/{alias}/export
- "List all permissions?" -> GET /{realm}/identity-provider/instances/{alias}/management/permissions
- "List all mapper-types?" -> GET /{realm}/identity-provider/instances/{alias}/mapper-types
- "List all mappers?" -> GET /{realm}/identity-provider/instances/{alias}/mappers
- "Create a mapper?" -> POST /{realm}/identity-provider/instances/{alias}/mappers
- "Get mapper details?" -> GET /{realm}/identity-provider/instances/{alias}/mappers/{id}
- "Update a mapper?" -> PUT /{realm}/identity-provider/instances/{alias}/mappers/{id}
- "Delete a mapper?" -> DELETE /{realm}/identity-provider/instances/{alias}/mappers/{id}
- "Get provider details?" -> GET /{realm}/identity-provider/providers/{provider_id}
- "List all keys?" -> GET /{realm}/keys
- "Create a logout-all?" -> POST /{realm}/logout-all
- "Create a partial-export?" -> POST /{realm}/partial-export
- "Create a partialImport?" -> POST /{realm}/partialImport
- "Create a push-revocation?" -> POST /{realm}/push-revocation
- "Search roles?" -> GET /{realm}/roles
- "Create a role?" -> POST /{realm}/roles
- "Get roles-by-id details?" -> GET /{realm}/roles-by-id/{role-id}
- "Update a roles-by-id?" -> PUT /{realm}/roles-by-id/{role-id}
- "Delete a roles-by-id?" -> DELETE /{realm}/roles-by-id/{role-id}
- "List all composites?" -> GET /{realm}/roles-by-id/{role-id}/composites
- "Create a composite?" -> POST /{realm}/roles-by-id/{role-id}/composites
- "Get client details?" -> GET /{realm}/roles-by-id/{role-id}/composites/clients/{client}
- "List all realm?" -> GET /{realm}/roles-by-id/{role-id}/composites/realm
- "List all permissions?" -> GET /{realm}/roles-by-id/{role-id}/management/permissions
- "Get role details?" -> GET /{realm}/roles/{role-name}
- "Update a role?" -> PUT /{realm}/roles/{role-name}
- "Delete a role?" -> DELETE /{realm}/roles/{role-name}
- "List all composites?" -> GET /{realm}/roles/{role-name}/composites
- "Create a composite?" -> POST /{realm}/roles/{role-name}/composites
- "Get client details?" -> GET /{realm}/roles/{role-name}/composites/clients/{client}
- "List all realm?" -> GET /{realm}/roles/{role-name}/composites/realm
- "List all groups?" -> GET /{realm}/roles/{role-name}/groups
- "List all permissions?" -> GET /{realm}/roles/{role-name}/management/permissions
- "List all users?" -> GET /{realm}/roles/{role-name}/users
- "Delete a session?" -> DELETE /{realm}/sessions/{session}
- "Create a testLDAPConnection?" -> POST /{realm}/testLDAPConnection
- "Create a testSMTPConnection?" -> POST /{realm}/testSMTPConnection
- "List all name?" -> GET /{realm}/user-storage/{id}/name
- "Create a remove-imported-user?" -> POST /{realm}/user-storage/{id}/remove-imported-users
- "Create a sync?" -> POST /{realm}/user-storage/{id}/sync
- "Create a unlink-user?" -> POST /{realm}/user-storage/{id}/unlink-users
- "Create a sync?" -> POST /{realm}/user-storage/{parentId}/mappers/{id}/sync
- "Search users?" -> GET /{realm}/users
- "Create a user?" -> POST /{realm}/users
- "List all users-management-permissions?" -> GET /{realm}/users-management-permissions
- "Search count?" -> GET /{realm}/users/count
- "Get user details?" -> GET /{realm}/users/{id}
- "Update a user?" -> PUT /{realm}/users/{id}
- "Delete a user?" -> DELETE /{realm}/users/{id}
- "List all configured-user-storage-credential-types?" -> GET /{realm}/users/{id}/configured-user-storage-credential-types
- "List all consents?" -> GET /{realm}/users/{id}/consents
- "Delete a consent?" -> DELETE /{realm}/users/{id}/consents/{client}
- "List all credentials?" -> GET /{realm}/users/{id}/credentials
- "Delete a credential?" -> DELETE /{realm}/users/{id}/credentials/{credentialId}
- "Create a moveToFirst?" -> POST /{realm}/users/{id}/credentials/{credentialId}/moveToFirst
- "List all federated-identity?" -> GET /{realm}/users/{id}/federated-identity
- "Delete a federated-identity?" -> DELETE /{realm}/users/{id}/federated-identity/{provider}
- "Search groups?" -> GET /{realm}/users/{id}/groups
- "Search count?" -> GET /{realm}/users/{id}/groups/count
- "Update a group?" -> PUT /{realm}/users/{id}/groups/{groupId}
- "Delete a group?" -> DELETE /{realm}/users/{id}/groups/{groupId}
- "Create a impersonation?" -> POST /{realm}/users/{id}/impersonation
- "Create a logout?" -> POST /{realm}/users/{id}/logout
- "Get offline-session details?" -> GET /{realm}/users/{id}/offline-sessions/{clientId}
- "List all role-mappings?" -> GET /{realm}/users/{id}/role-mappings
- "Get client details?" -> GET /{realm}/users/{id}/role-mappings/clients/{client}
- "Delete a client?" -> DELETE /{realm}/users/{id}/role-mappings/clients/{client}
- "List all available?" -> GET /{realm}/users/{id}/role-mappings/clients/{client}/available
- "List all composite?" -> GET /{realm}/users/{id}/role-mappings/clients/{client}/composite
- "List all realm?" -> GET /{realm}/users/{id}/role-mappings/realm
- "Create a realm?" -> POST /{realm}/users/{id}/role-mappings/realm
- "List all available?" -> GET /{realm}/users/{id}/role-mappings/realm/available
- "List all composite?" -> GET /{realm}/users/{id}/role-mappings/realm/composite
- "List all sessions?" -> GET /{realm}/users/{id}/sessions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
