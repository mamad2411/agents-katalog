---
name: aws-codestar-connections
description: "AWS CodeStar connections API skill. Use when working with AWS CodeStar connections for root. Covers 27 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS CodeStar connections
API version: 2019-12-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

27 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a connection that can then be given to other Amazon Web Services services like CodePipeline so that it can access third-party code repositories. The connection is in pending status until the third-party connection handshake is completed from the console. |
| POST | / | Creates a resource that represents the infrastructure where a third-party provider is installed. The host is used when you create connections to an installed third-party provider type, such as GitHub Enterprise Server. You create one host for all connections to that provider.  A host created through the CLI or the SDK is in `PENDING` status by default. You can make its status `AVAILABLE` by setting up the host in the console. |
| POST | / | Creates a link to a specified external Git repository. A repository link allows Git sync to monitor and sync changes to files in a specified Git repository. |
| POST | / | Creates a sync configuration which allows Amazon Web Services to sync content from a Git repository to update a specified Amazon Web Services resource. Parameters for the sync configuration are determined by the sync type. |
| POST | / | The connection to be deleted. |
| POST | / | The host to be deleted. Before you delete a host, all connections associated to the host must be deleted.  A host cannot be deleted if it is in the VPC_CONFIG_INITIALIZING or VPC_CONFIG_DELETING state. |
| POST | / | Deletes the association between your connection and a specified external Git repository. |
| POST | / | Deletes the sync configuration for a specified repository and connection. |
| POST | / | Returns the connection ARN and details such as status, owner, and provider type. |
| POST | / | Returns the host ARN and details such as status, provider type, endpoint, and, if applicable, the VPC configuration. |
| POST | / | Returns details about a repository link. A repository link allows Git sync to monitor and sync changes from files in a specified Git repository. |
| POST | / | Returns details about the sync status for a repository. A repository sync uses Git sync to push and pull changes from your remote repository. |
| POST | / | Returns the status of the sync with the Git repository for a specific Amazon Web Services resource. |
| POST | / | Returns a list of the most recent sync blockers. |
| POST | / | Returns details about a sync configuration, including the sync type and resource name. A sync configuration allows the configuration to sync (push and pull) changes from the remote repository for a specified branch in a Git repository. |
| POST | / | Lists the connections associated with your account. |
| POST | / | Lists the hosts associated with your account. |
| POST | / | Lists the repository links created for connections in your account. |
| POST | / | Lists the repository sync definitions for repository links in your account. |
| POST | / | Returns a list of sync configurations for a specified repository. |
| POST | / | Gets the set of key-value pairs (metadata) that are used to manage the resource. |
| POST | / | Adds to or modifies the tags of the given resource. Tags are metadata that can be used to manage a resource. |
| POST | / | Removes tags from an Amazon Web Services resource. |
| POST | / | Updates a specified host with the provided configurations. |
| POST | / | Updates the association between your connection and a specified external Git repository. A repository link allows Git sync to monitor and sync changes to files in a specified Git repository. |
| POST | / | Allows you to update the status of a sync blocker, resolving the blocker and allowing syncing to continue. |
| POST | / | Updates the sync configuration for your connection and a specified external Git repository. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
