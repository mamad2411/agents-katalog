---
name: anchore-engine-api-server
description: "Anchore Engine API Server API skill. Use when working with Anchore Engine API Server for root, health, version. Covers 112 endpoints."
version: 1.0.0
generator: lapsh
---

# Anchore Engine API Server
API version: 0.1.20

## Auth
ApiKey username in formData

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET / -- verify access
3. POST /policies -- create first policies

## Endpoints

112 endpoints across 21 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Simple status check |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check, returns 200 and no body if service is running |

### version
| Method | Path | Description |
|--------|------|-------------|
| GET | /version | Returns the version object for the service, including db schema version info |

### policies
| Method | Path | Description |
|--------|------|-------------|
| GET | /policies | List policies |
| POST | /policies | Add a new policy |
| GET | /policies/{policyId} | Get specific policy |
| PUT | /policies/{policyId} | Update policy |
| DELETE | /policies/{policyId} | Delete policy |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions | List all subscriptions |
| POST | /subscriptions | Add a subscription of a specific type |
| GET | /subscriptions/{subscriptionId} | Get a specific subscription set |
| PUT | /subscriptions/{subscriptionId} | Update an existing and specific subscription |
| DELETE | /subscriptions/{subscriptionId} | Delete subscriptions of a specific type |

### summaries
| Method | Path | Description |
|--------|------|-------------|
| GET | /summaries/imagetags | List all visible image digests and tags |

### images
| Method | Path | Description |
|--------|------|-------------|
| POST | /images | Submit a new image for analysis by the engine |
| GET | /images | List all visible images |
| DELETE | /images | Bulk mark images for deletion |
| GET | /images/{imageDigest} | Get image metadata |
| DELETE | /images/{imageDigest} | Delete an image analysis |
| GET | /images/by_id/{imageId} | Lookup image by docker imageId |
| DELETE | /images/by_id/{imageId} | Delete image by docker imageId |
| GET | /images/{imageDigest}/check | Check policy evaluation status for image |
| GET | /images/by_id/{imageId}/check | Check policy evaluation status for image |
| GET | /images/{imageDigest}/vuln | Get vulnerability types |
| GET | /images/{imageDigest}/vuln/{vtype} | Get vulnerabilities by type |
| GET | /images/by_id/{imageId}/vuln | Get vulnerability types |
| GET | /images/by_id/{imageId}/vuln/{vtype} | Get vulnerabilities by type |
| GET | /images/{imageDigest}/content | List image content types |
| GET | /images/by_id/{imageId}/content | List image content types |
| GET | /images/{imageDigest}/content/{ctype} | Get the content of an image by type |
| GET | /images/{imageDigest}/content/files | Get the content of an image by type files |
| GET | /images/{imageDigest}/content/java | Get the content of an image by type java |
| GET | /images/{imageDigest}/content/malware | Get the content of an image by type malware |
| GET | /images/by_id/{imageId}/content/{ctype} | Get the content of an image by type |
| GET | /images/by_id/{imageId}/content/files | Get the content of an image by type files |
| GET | /images/by_id/{imageId}/content/java | Get the content of an image by type java |
| GET | /images/{imageDigest}/artifacts/retrieved_files | Return a list of analyzer artifacts of the specified type |
| GET | /images/{imageDigest}/artifacts/file_content_search | Return a list of analyzer artifacts of the specified type |
| GET | /images/{imageDigest}/artifacts/secret_search | Return a list of analyzer artifacts of the specified type |
| GET | /images/{imageDigest}/metadata | List image metadata types |
| GET | /images/{imageDigest}/sboms/native | Get image sbom in the native Anchore format |
| GET | /images/{imageDigest}/metadata/{mtype} | Get the metadata of an image by type |

### import
| Method | Path | Description |
|--------|------|-------------|
| POST | /import/images | Import an anchore image tar.gz archive file. This is a deprecated API replaced by the "/imports/images" route |

### repositories
| Method | Path | Description |
|--------|------|-------------|
| POST | /repositories | Add repository to watch |

### registries
| Method | Path | Description |
|--------|------|-------------|
| GET | /registries | List configured registries |
| POST | /registries | Add a new registry |
| GET | /registries/{registry} | Get a specific registry configuration |
| PUT | /registries/{registry} | Update/replace a registry configuration |
| DELETE | /registries/{registry} | Delete a registry configuration |

### status
| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Service status |

### system
| Method | Path | Description |
|--------|------|-------------|
| GET | /system | System status |
| GET | /system/feeds | list feeds operations and information |
| POST | /system/feeds | trigger feeds operations |
| PUT | /system/feeds/{feed} | Disable the feed so that it does not sync on subsequent sync operations |
| DELETE | /system/feeds/{feed} | Delete the groups and data for the feed and disable the feed itself |
| PUT | /system/feeds/{feed}/{group} | Disable a specific group within a feed to not sync |
| DELETE | /system/feeds/{feed}/{group} | Delete the group data and disable the group itself |
| GET | /system/services | List system services |
| GET | /system/services/{servicename} | Get a service configuration and state |
| GET | /system/services/{servicename}/{hostid} | Get service config for a specific host |
| DELETE | /system/services/{servicename}/{hostid} | Delete the service config |
| GET | /system/policy_spec | Describe the policy language spec implemented by this service. |
| GET | /system/error_codes | Describe anchore engine error codes. |
| POST | /system/webhooks/{webhook_type}/test | Adds the capabilities to test a webhook delivery for the given notification type |

### event_types
| Method | Path | Description |
|--------|------|-------------|
| GET | /event_types | List Event Types |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | List Events |
| DELETE | /events | Delete Events |
| GET | /events/{eventId} | Get Event |
| DELETE | /events/{eventId} | Delete Event |

### query
| Method | Path | Description |
|--------|------|-------------|
| GET | /query/images/by_vulnerability | List images vulnerable to the specific vulnerability ID. |
| GET | /query/images/by_package | List of images containing given package |
| GET | /query/vulnerabilities | Listing information about given vulnerability |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | List user summaries. Only available to the system admin user. |
| POST | /accounts | Create a new user. Only avaialble to admin user. |
| GET | /accounts/{accountname} | Get info about an user. Only available to admin user. Uses the main user Id, not a username. |
| DELETE | /accounts/{accountname} | Delete the specified account, only allowed if the account is in the disabled state. All users will be deleted along with the account and all resources will be garbage collected |
| PUT | /accounts/{accountname}/state | Update the state of an account to either enabled or disabled. For deletion use the DELETE route |
| GET | /accounts/{accountname}/users | List accounts for the user |
| POST | /accounts/{accountname}/users | Create a new user |
| DELETE | /accounts/{accountname}/users/{username} | Delete a specific user credential by username of the credential. Cannot be the credential used to authenticate the request. |
| GET | /accounts/{accountname}/users/{username} | Get a specific user in the specified account |
| GET | /accounts/{accountname}/users/{username}/credentials | Get current credential summary |
| POST | /accounts/{accountname}/users/{username}/credentials | add/replace credential |
| DELETE | /accounts/{accountname}/users/{username}/credentials | Delete a credential by type |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | List the account for the authenticated user |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user | List authenticated user info |
| GET | /user/credentials | Get current credential summary |
| POST | /user/credentials | add/replace credential |

### archives
| Method | Path | Description |
|--------|------|-------------|
| GET | /archives |  |
| GET | /archives/rules |  |
| POST | /archives/rules |  |
| GET | /archives/rules/{ruleId} |  |
| DELETE | /archives/rules/{ruleId} |  |
| GET | /archives/images |  |
| POST | /archives/images |  |
| GET | /archives/images/{imageDigest} | Returns the archive metadata record identifying the image and tags for the analysis in the archive. |
| DELETE | /archives/images/{imageDigest} | Performs a synchronous archive deletion |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/token | Request a jwt token for subsequent operations, this request is authenticated with normal HTTP auth |

### imports
| Method | Path | Description |
|--------|------|-------------|
| POST | /imports/images | Begin the import of an image analyzed by Syft into the system |
| GET | /imports/images | Lists in-progress imports |
| GET | /imports/images/{operation_id} | Get detail on a single import |
| DELETE | /imports/images/{operation_id} | Invalidate operation ID so it can be garbage collected |
| GET | /imports/images/{operation_id}/packages | List uploaded package manifests |
| POST | /imports/images/{operation_id}/packages | Begin the import of an image analyzed by Syft into the system |
| GET | /imports/images/{operation_id}/dockerfile | List uploaded dockerfiles |
| POST | /imports/images/{operation_id}/dockerfile | Begin the import of an image analyzed by Syft into the system |
| GET | /imports/images/{operation_id}/manifest | List uploaded image manifests |
| POST | /imports/images/{operation_id}/manifest | Import a docker or OCI distribution manifest to associate with the image |
| GET | /imports/images/{operation_id}/parent_manifest | List uploaded parent manifests (manifest lists for a tag) |
| POST | /imports/images/{operation_id}/parent_manifest | Import a docker or OCI distribution manifest list to associate with the image |
| GET | /imports/images/{operation_id}/image_config | List uploaded image configs |
| POST | /imports/images/{operation_id}/image_config | Import a docker or OCI image config to associate with the image |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all health?" -> GET /health
- "List all version?" -> GET /version
- "List all policies?" -> GET /policies
- "Create a policy?" -> POST /policies
- "Get policy details?" -> GET /policies/{policyId}
- "Update a policy?" -> PUT /policies/{policyId}
- "Delete a policy?" -> DELETE /policies/{policyId}
- "List all subscriptions?" -> GET /subscriptions
- "Create a subscription?" -> POST /subscriptions
- "Get subscription details?" -> GET /subscriptions/{subscriptionId}
- "Update a subscription?" -> PUT /subscriptions/{subscriptionId}
- "Delete a subscription?" -> DELETE /subscriptions/{subscriptionId}
- "List all imagetags?" -> GET /summaries/imagetags
- "Create a image?" -> POST /images
- "List all images?" -> GET /images
- "Create a image?" -> POST /import/images
- "Get image details?" -> GET /images/{imageDigest}
- "Delete a image?" -> DELETE /images/{imageDigest}
- "Get by_id details?" -> GET /images/by_id/{imageId}
- "Delete a by_id?" -> DELETE /images/by_id/{imageId}
- "List all check?" -> GET /images/{imageDigest}/check
- "List all check?" -> GET /images/by_id/{imageId}/check
- "List all vuln?" -> GET /images/{imageDigest}/vuln
- "Get vuln details?" -> GET /images/{imageDigest}/vuln/{vtype}
- "List all vuln?" -> GET /images/by_id/{imageId}/vuln
- "Get vuln details?" -> GET /images/by_id/{imageId}/vuln/{vtype}
- "List all content?" -> GET /images/{imageDigest}/content
- "List all content?" -> GET /images/by_id/{imageId}/content
- "Get content details?" -> GET /images/{imageDigest}/content/{ctype}
- "List all files?" -> GET /images/{imageDigest}/content/files
- "List all java?" -> GET /images/{imageDigest}/content/java
- "List all malware?" -> GET /images/{imageDigest}/content/malware
- "Get content details?" -> GET /images/by_id/{imageId}/content/{ctype}
- "List all files?" -> GET /images/by_id/{imageId}/content/files
- "List all java?" -> GET /images/by_id/{imageId}/content/java
- "List all retrieved_files?" -> GET /images/{imageDigest}/artifacts/retrieved_files
- "List all file_content_search?" -> GET /images/{imageDigest}/artifacts/file_content_search
- "List all secret_search?" -> GET /images/{imageDigest}/artifacts/secret_search
- "List all metadata?" -> GET /images/{imageDigest}/metadata
- "List all native?" -> GET /images/{imageDigest}/sboms/native
- "Get metadata details?" -> GET /images/{imageDigest}/metadata/{mtype}
- "Create a repository?" -> POST /repositories
- "List all registries?" -> GET /registries
- "Create a registry?" -> POST /registries
- "Get registry details?" -> GET /registries/{registry}
- "Update a registry?" -> PUT /registries/{registry}
- "Delete a registry?" -> DELETE /registries/{registry}
- "List all status?" -> GET /status
- "List all system?" -> GET /system
- "List all feeds?" -> GET /system/feeds
- "Create a feed?" -> POST /system/feeds
- "Update a feed?" -> PUT /system/feeds/{feed}
- "Delete a feed?" -> DELETE /system/feeds/{feed}
- "Update a feed?" -> PUT /system/feeds/{feed}/{group}
- "Delete a feed?" -> DELETE /system/feeds/{feed}/{group}
- "List all services?" -> GET /system/services
- "Get service details?" -> GET /system/services/{servicename}
- "Get service details?" -> GET /system/services/{servicename}/{hostid}
- "Delete a service?" -> DELETE /system/services/{servicename}/{hostid}
- "List all policy_spec?" -> GET /system/policy_spec
- "List all error_codes?" -> GET /system/error_codes
- "List all event_types?" -> GET /event_types
- "List all events?" -> GET /events
- "Get event details?" -> GET /events/{eventId}
- "Delete a event?" -> DELETE /events/{eventId}
- "List all by_vulnerability?" -> GET /query/images/by_vulnerability
- "List all by_package?" -> GET /query/images/by_package
- "List all vulnerabilities?" -> GET /query/vulnerabilities
- "List all accounts?" -> GET /accounts
- "Create a account?" -> POST /accounts
- "Get account details?" -> GET /accounts/{accountname}
- "Delete a account?" -> DELETE /accounts/{accountname}
- "List all users?" -> GET /accounts/{accountname}/users
- "Create a user?" -> POST /accounts/{accountname}/users
- "Delete a user?" -> DELETE /accounts/{accountname}/users/{username}
- "Get user details?" -> GET /accounts/{accountname}/users/{username}
- "List all credentials?" -> GET /accounts/{accountname}/users/{username}/credentials
- "Create a credential?" -> POST /accounts/{accountname}/users/{username}/credentials
- "List all account?" -> GET /account
- "List all user?" -> GET /user
- "List all credentials?" -> GET /user/credentials
- "Create a credential?" -> POST /user/credentials
- "List all archives?" -> GET /archives
- "List all rules?" -> GET /archives/rules
- "Create a rule?" -> POST /archives/rules
- "Get rule details?" -> GET /archives/rules/{ruleId}
- "Delete a rule?" -> DELETE /archives/rules/{ruleId}
- "List all images?" -> GET /archives/images
- "Create a image?" -> POST /archives/images
- "Get image details?" -> GET /archives/images/{imageDigest}
- "Delete a image?" -> DELETE /archives/images/{imageDigest}
- "Create a token?" -> POST /oauth/token
- "Create a test?" -> POST /system/webhooks/{webhook_type}/test
- "Create a image?" -> POST /imports/images
- "List all images?" -> GET /imports/images
- "Get image details?" -> GET /imports/images/{operation_id}
- "Delete a image?" -> DELETE /imports/images/{operation_id}
- "List all packages?" -> GET /imports/images/{operation_id}/packages
- "Create a package?" -> POST /imports/images/{operation_id}/packages
- "List all dockerfile?" -> GET /imports/images/{operation_id}/dockerfile
- "Create a dockerfile?" -> POST /imports/images/{operation_id}/dockerfile
- "List all manifest?" -> GET /imports/images/{operation_id}/manifest
- "Create a manifest?" -> POST /imports/images/{operation_id}/manifest
- "List all parent_manifest?" -> GET /imports/images/{operation_id}/parent_manifest
- "Create a parent_manifest?" -> POST /imports/images/{operation_id}/parent_manifest
- "List all image_config?" -> GET /imports/images/{operation_id}/image_config
- "Create a image_config?" -> POST /imports/images/{operation_id}/image_config
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
