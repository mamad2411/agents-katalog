---
name: aws-server-migration-service
description: "AWS Server Migration Service API skill. Use when working with AWS Server Migration Service for root. Covers 35 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Server Migration Service
API version: 2016-10-24

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

35 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates an application. An application consists of one or more server groups. Each server group contain one or more servers. |
| POST | / | Creates a replication job. The replication job schedules periodic replication runs to replicate your server to Amazon Web Services. Each replication run creates an Amazon Machine Image (AMI). |
| POST | / | Deletes the specified application. Optionally deletes the launched stack associated with the application and all Server Migration Service replication jobs for servers in the application. |
| POST | / | Deletes the launch configuration for the specified application. |
| POST | / | Deletes the replication configuration for the specified application. |
| POST | / | Deletes the validation configuration for the specified application. |
| POST | / | Deletes the specified replication job. After you delete a replication job, there are no further replication runs. Amazon Web Services deletes the contents of the Amazon S3 bucket used to store Server Migration Service artifacts. The AMIs created by the replication runs are not deleted. |
| POST | / | Deletes all servers from your server catalog. |
| POST | / | Disassociates the specified connector from Server Migration Service. After you disassociate a connector, it is no longer available to support replication jobs. |
| POST | / | Generates a target change set for a currently launched stack and writes it to an Amazon S3 object in the customer’s Amazon S3 bucket. |
| POST | / | Generates an CloudFormation template based on the current launch configuration and writes it to an Amazon S3 object in the customer’s Amazon S3 bucket. |
| POST | / | Retrieve information about the specified application. |
| POST | / | Retrieves the application launch configuration associated with the specified application. |
| POST | / | Retrieves the application replication configuration associated with the specified application. |
| POST | / | Retrieves information about a configuration for validating an application. |
| POST | / | Retrieves output from validating an application. |
| POST | / | Describes the connectors registered with the Server Migration Service. |
| POST | / | Describes the specified replication job or all of your replication jobs. |
| POST | / | Describes the replication runs for the specified replication job. |
| POST | / | Describes the servers in your server catalog. Before you can describe your servers, you must import them using ImportServerCatalog. |
| POST | / | Allows application import from Migration Hub. |
| POST | / | Gathers a complete list of on-premises servers. Connectors must be installed and monitoring all servers to import. This call returns immediately, but might take additional time to retrieve all the servers. |
| POST | / | Launches the specified application as a stack in CloudFormation. |
| POST | / | Retrieves summaries for all applications. |
| POST | / | Provides information to Server Migration Service about whether application validation is successful. |
| POST | / | Creates or updates the launch configuration for the specified application. |
| POST | / | Creates or updates the replication configuration for the specified application. |
| POST | / | Creates or updates a validation configuration for the specified application. |
| POST | / | Starts replicating the specified application by creating replication jobs for each server in the application. |
| POST | / | Starts an on-demand replication run for the specified application. |
| POST | / | Starts an on-demand replication run for the specified replication job. This replication run starts immediately. This replication run is in addition to the ones already scheduled. There is a limit on the number of on-demand replications runs that you can request in a 24-hour period. |
| POST | / | Stops replicating the specified application by deleting the replication job for each server in the application. |
| POST | / | Terminates the stack for the specified application. |
| POST | / | Updates the specified application. |
| POST | / | Updates the specified settings for the specified replication job. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
