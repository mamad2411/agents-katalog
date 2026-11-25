---
name: aws-greengrass
description: "AWS Greengrass API skill. Use when working with AWS Greengrass for greengrass, tags. Covers 92 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Greengrass
API version: 2017-06-07

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /greengrass/servicerole -- verify access
3. POST /greengrass/definition/connectors -- create first connectors

## Endpoints

92 endpoints across 2 groups. See references/api-spec.lap for full details.

### greengrass
| Method | Path | Description |
|--------|------|-------------|
| PUT | /greengrass/groups/{GroupId}/role | Associates a role with a group. Your Greengrass core will use the role to access AWS cloud services. The role's permissions should allow Greengrass core Lambda functions to perform actions against the cloud. |
| PUT | /greengrass/servicerole | Associates a role with your account. AWS IoT Greengrass will use the role to access your Lambda functions and AWS IoT resources. This is necessary for deployments to succeed. The role must have at least minimum permissions in the policy ''AWSGreengrassResourceAccessRolePolicy''. |
| POST | /greengrass/definition/connectors | Creates a connector definition. You may provide the initial version of the connector definition now or use ''CreateConnectorDefinitionVersion'' at a later time. |
| POST | /greengrass/definition/connectors/{ConnectorDefinitionId}/versions | Creates a version of a connector definition which has already been defined. |
| POST | /greengrass/definition/cores | Creates a core definition. You may provide the initial version of the core definition now or use ''CreateCoreDefinitionVersion'' at a later time. Greengrass groups must each contain exactly one Greengrass core. |
| POST | /greengrass/definition/cores/{CoreDefinitionId}/versions | Creates a version of a core definition that has already been defined. Greengrass groups must each contain exactly one Greengrass core. |
| POST | /greengrass/groups/{GroupId}/deployments | Creates a deployment. ''CreateDeployment'' requests are idempotent with respect to the ''X-Amzn-Client-Token'' token and the request parameters. |
| POST | /greengrass/definition/devices | Creates a device definition. You may provide the initial version of the device definition now or use ''CreateDeviceDefinitionVersion'' at a later time. |
| POST | /greengrass/definition/devices/{DeviceDefinitionId}/versions | Creates a version of a device definition that has already been defined. |
| POST | /greengrass/definition/functions | Creates a Lambda function definition which contains a list of Lambda functions and their configurations to be used in a group. You can create an initial version of the definition by providing a list of Lambda functions and their configurations now, or use ''CreateFunctionDefinitionVersion'' later. |
| POST | /greengrass/definition/functions/{FunctionDefinitionId}/versions | Creates a version of a Lambda function definition that has already been defined. |
| POST | /greengrass/groups | Creates a group. You may provide the initial version of the group or use ''CreateGroupVersion'' at a later time. Tip: You can use the ''gg_group_setup'' package (https://github.com/awslabs/aws-greengrass-group-setup) as a library or command-line application to create and deploy Greengrass groups. |
| POST | /greengrass/groups/{GroupId}/certificateauthorities | Creates a CA for the group. If a CA already exists, it will rotate the existing CA. |
| POST | /greengrass/groups/{GroupId}/versions | Creates a version of a group which has already been defined. |
| POST | /greengrass/definition/loggers | Creates a logger definition. You may provide the initial version of the logger definition now or use ''CreateLoggerDefinitionVersion'' at a later time. |
| POST | /greengrass/definition/loggers/{LoggerDefinitionId}/versions | Creates a version of a logger definition that has already been defined. |
| POST | /greengrass/definition/resources | Creates a resource definition which contains a list of resources to be used in a group. You can create an initial version of the definition by providing a list of resources now, or use ''CreateResourceDefinitionVersion'' later. |
| POST | /greengrass/definition/resources/{ResourceDefinitionId}/versions | Creates a version of a resource definition that has already been defined. |
| POST | /greengrass/updates | Creates a software update for a core or group of cores (specified as an IoT thing group.) Use this to update the OTA Agent as well as the Greengrass core software. It makes use of the IoT Jobs feature which provides additional commands to manage a Greengrass core software update job. |
| POST | /greengrass/definition/subscriptions | Creates a subscription definition. You may provide the initial version of the subscription definition now or use ''CreateSubscriptionDefinitionVersion'' at a later time. |
| POST | /greengrass/definition/subscriptions/{SubscriptionDefinitionId}/versions | Creates a version of a subscription definition which has already been defined. |
| DELETE | /greengrass/definition/connectors/{ConnectorDefinitionId} | Deletes a connector definition. |
| DELETE | /greengrass/definition/cores/{CoreDefinitionId} | Deletes a core definition. |
| DELETE | /greengrass/definition/devices/{DeviceDefinitionId} | Deletes a device definition. |
| DELETE | /greengrass/definition/functions/{FunctionDefinitionId} | Deletes a Lambda function definition. |
| DELETE | /greengrass/groups/{GroupId} | Deletes a group. |
| DELETE | /greengrass/definition/loggers/{LoggerDefinitionId} | Deletes a logger definition. |
| DELETE | /greengrass/definition/resources/{ResourceDefinitionId} | Deletes a resource definition. |
| DELETE | /greengrass/definition/subscriptions/{SubscriptionDefinitionId} | Deletes a subscription definition. |
| DELETE | /greengrass/groups/{GroupId}/role | Disassociates the role from a group. |
| DELETE | /greengrass/servicerole | Disassociates the service role from your account. Without a service role, deployments will not work. |
| GET | /greengrass/groups/{GroupId}/role | Retrieves the role associated with a particular group. |
| GET | /greengrass/bulk/deployments/{BulkDeploymentId}/status | Returns the status of a bulk deployment. |
| GET | /greengrass/things/{ThingName}/connectivityInfo | Retrieves the connectivity information for a core. |
| GET | /greengrass/definition/connectors/{ConnectorDefinitionId} | Retrieves information about a connector definition. |
| GET | /greengrass/definition/connectors/{ConnectorDefinitionId}/versions/{ConnectorDefinitionVersionId} | Retrieves information about a connector definition version, including the connectors that the version contains. Connectors are prebuilt modules that interact with local infrastructure, device protocols, AWS, and other cloud services. |
| GET | /greengrass/definition/cores/{CoreDefinitionId} | Retrieves information about a core definition version. |
| GET | /greengrass/definition/cores/{CoreDefinitionId}/versions/{CoreDefinitionVersionId} | Retrieves information about a core definition version. |
| GET | /greengrass/groups/{GroupId}/deployments/{DeploymentId}/status | Returns the status of a deployment. |
| GET | /greengrass/definition/devices/{DeviceDefinitionId} | Retrieves information about a device definition. |
| GET | /greengrass/definition/devices/{DeviceDefinitionId}/versions/{DeviceDefinitionVersionId} | Retrieves information about a device definition version. |
| GET | /greengrass/definition/functions/{FunctionDefinitionId} | Retrieves information about a Lambda function definition, including its creation time and latest version. |
| GET | /greengrass/definition/functions/{FunctionDefinitionId}/versions/{FunctionDefinitionVersionId} | Retrieves information about a Lambda function definition version, including which Lambda functions are included in the version and their configurations. |
| GET | /greengrass/groups/{GroupId} | Retrieves information about a group. |
| GET | /greengrass/groups/{GroupId}/certificateauthorities/{CertificateAuthorityId} | Retreives the CA associated with a group. Returns the public key of the CA. |
| GET | /greengrass/groups/{GroupId}/certificateauthorities/configuration/expiry | Retrieves the current configuration for the CA used by the group. |
| GET | /greengrass/groups/{GroupId}/versions/{GroupVersionId} | Retrieves information about a group version. |
| GET | /greengrass/definition/loggers/{LoggerDefinitionId} | Retrieves information about a logger definition. |
| GET | /greengrass/definition/loggers/{LoggerDefinitionId}/versions/{LoggerDefinitionVersionId} | Retrieves information about a logger definition version. |
| GET | /greengrass/definition/resources/{ResourceDefinitionId} | Retrieves information about a resource definition, including its creation time and latest version. |
| GET | /greengrass/definition/resources/{ResourceDefinitionId}/versions/{ResourceDefinitionVersionId} | Retrieves information about a resource definition version, including which resources are included in the version. |
| GET | /greengrass/servicerole | Retrieves the service role that is attached to your account. |
| GET | /greengrass/definition/subscriptions/{SubscriptionDefinitionId} | Retrieves information about a subscription definition. |
| GET | /greengrass/definition/subscriptions/{SubscriptionDefinitionId}/versions/{SubscriptionDefinitionVersionId} | Retrieves information about a subscription definition version. |
| GET | /greengrass/things/{ThingName}/runtimeconfig | Get the runtime configuration of a thing. |
| GET | /greengrass/bulk/deployments/{BulkDeploymentId}/detailed-reports | Gets a paginated list of the deployments that have been started in a bulk deployment operation, and their current deployment status. |
| GET | /greengrass/bulk/deployments | Returns a list of bulk deployments. |
| GET | /greengrass/definition/connectors/{ConnectorDefinitionId}/versions | Lists the versions of a connector definition, which are containers for connectors. Connectors run on the Greengrass core and contain built-in integration with local infrastructure, device protocols, AWS, and other cloud services. |
| GET | /greengrass/definition/connectors | Retrieves a list of connector definitions. |
| GET | /greengrass/definition/cores/{CoreDefinitionId}/versions | Lists the versions of a core definition. |
| GET | /greengrass/definition/cores | Retrieves a list of core definitions. |
| GET | /greengrass/groups/{GroupId}/deployments | Returns a history of deployments for the group. |
| GET | /greengrass/definition/devices/{DeviceDefinitionId}/versions | Lists the versions of a device definition. |
| GET | /greengrass/definition/devices | Retrieves a list of device definitions. |
| GET | /greengrass/definition/functions/{FunctionDefinitionId}/versions | Lists the versions of a Lambda function definition. |
| GET | /greengrass/definition/functions | Retrieves a list of Lambda function definitions. |
| GET | /greengrass/groups/{GroupId}/certificateauthorities | Retrieves the current CAs for a group. |
| GET | /greengrass/groups/{GroupId}/versions | Lists the versions of a group. |
| GET | /greengrass/groups | Retrieves a list of groups. |
| GET | /greengrass/definition/loggers/{LoggerDefinitionId}/versions | Lists the versions of a logger definition. |
| GET | /greengrass/definition/loggers | Retrieves a list of logger definitions. |
| GET | /greengrass/definition/resources/{ResourceDefinitionId}/versions | Lists the versions of a resource definition. |
| GET | /greengrass/definition/resources | Retrieves a list of resource definitions. |
| GET | /greengrass/definition/subscriptions/{SubscriptionDefinitionId}/versions | Lists the versions of a subscription definition. |
| GET | /greengrass/definition/subscriptions | Retrieves a list of subscription definitions. |
| POST | /greengrass/groups/{GroupId}/deployments/$reset | Resets a group's deployments. |
| POST | /greengrass/bulk/deployments | Deploys multiple groups in one operation. This action starts the bulk deployment of a specified set of group versions. Each group version deployment will be triggered with an adaptive rate that has a fixed upper limit. We recommend that you include an ''X-Amzn-Client-Token'' token in every ''StartBulkDeployment'' request. These requests are idempotent with respect to the token and the request parameters. |
| PUT | /greengrass/bulk/deployments/{BulkDeploymentId}/$stop | Stops the execution of a bulk deployment. This action returns a status of ''Stopping'' until the deployment is stopped. You cannot start a new bulk deployment while a previous deployment is in the ''Stopping'' state. This action doesn't rollback completed deployments or cancel pending deployments. |
| PUT | /greengrass/things/{ThingName}/connectivityInfo | Updates the connectivity information for the core. Any devices that belong to the group which has this core will receive this information in order to find the location of the core and connect to it. |
| PUT | /greengrass/definition/connectors/{ConnectorDefinitionId} | Updates a connector definition. |
| PUT | /greengrass/definition/cores/{CoreDefinitionId} | Updates a core definition. |
| PUT | /greengrass/definition/devices/{DeviceDefinitionId} | Updates a device definition. |
| PUT | /greengrass/definition/functions/{FunctionDefinitionId} | Updates a Lambda function definition. |
| PUT | /greengrass/groups/{GroupId} | Updates a group. |
| PUT | /greengrass/groups/{GroupId}/certificateauthorities/configuration/expiry | Updates the Certificate expiry time for a group. |
| PUT | /greengrass/definition/loggers/{LoggerDefinitionId} | Updates a logger definition. |
| PUT | /greengrass/definition/resources/{ResourceDefinitionId} | Updates a resource definition. |
| PUT | /greengrass/definition/subscriptions/{SubscriptionDefinitionId} | Updates a subscription definition. |
| PUT | /greengrass/things/{ThingName}/runtimeconfig | Updates the runtime configuration of a thing. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resource-arn} | Retrieves a list of resource tags for a resource arn. |
| POST | /tags/{resource-arn} | Adds tags to a Greengrass resource. Valid resources are 'Group', 'ConnectorDefinition', 'CoreDefinition', 'DeviceDefinition', 'FunctionDefinition', 'LoggerDefinition', 'SubscriptionDefinition', 'ResourceDefinition', and 'BulkDeployment'. |
| DELETE | /tags/{resource-arn} | Remove resource tags from a Greengrass Resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a connector?" -> POST /greengrass/definition/connectors
- "Create a version?" -> POST /greengrass/definition/connectors/{ConnectorDefinitionId}/versions
- "Create a core?" -> POST /greengrass/definition/cores
- "Create a version?" -> POST /greengrass/definition/cores/{CoreDefinitionId}/versions
- "Create a deployment?" -> POST /greengrass/groups/{GroupId}/deployments
- "Create a device?" -> POST /greengrass/definition/devices
- "Create a version?" -> POST /greengrass/definition/devices/{DeviceDefinitionId}/versions
- "Create a function?" -> POST /greengrass/definition/functions
- "Create a version?" -> POST /greengrass/definition/functions/{FunctionDefinitionId}/versions
- "Create a group?" -> POST /greengrass/groups
- "Create a certificateauthority?" -> POST /greengrass/groups/{GroupId}/certificateauthorities
- "Create a version?" -> POST /greengrass/groups/{GroupId}/versions
- "Create a logger?" -> POST /greengrass/definition/loggers
- "Create a version?" -> POST /greengrass/definition/loggers/{LoggerDefinitionId}/versions
- "Create a resource?" -> POST /greengrass/definition/resources
- "Create a version?" -> POST /greengrass/definition/resources/{ResourceDefinitionId}/versions
- "Create a update?" -> POST /greengrass/updates
- "Create a subscription?" -> POST /greengrass/definition/subscriptions
- "Create a version?" -> POST /greengrass/definition/subscriptions/{SubscriptionDefinitionId}/versions
- "Delete a connector?" -> DELETE /greengrass/definition/connectors/{ConnectorDefinitionId}
- "Delete a core?" -> DELETE /greengrass/definition/cores/{CoreDefinitionId}
- "Delete a device?" -> DELETE /greengrass/definition/devices/{DeviceDefinitionId}
- "Delete a function?" -> DELETE /greengrass/definition/functions/{FunctionDefinitionId}
- "Delete a group?" -> DELETE /greengrass/groups/{GroupId}
- "Delete a logger?" -> DELETE /greengrass/definition/loggers/{LoggerDefinitionId}
- "Delete a resource?" -> DELETE /greengrass/definition/resources/{ResourceDefinitionId}
- "Delete a subscription?" -> DELETE /greengrass/definition/subscriptions/{SubscriptionDefinitionId}
- "List all role?" -> GET /greengrass/groups/{GroupId}/role
- "List all status?" -> GET /greengrass/bulk/deployments/{BulkDeploymentId}/status
- "List all connectivityInfo?" -> GET /greengrass/things/{ThingName}/connectivityInfo
- "Get connector details?" -> GET /greengrass/definition/connectors/{ConnectorDefinitionId}
- "Get version details?" -> GET /greengrass/definition/connectors/{ConnectorDefinitionId}/versions/{ConnectorDefinitionVersionId}
- "Get core details?" -> GET /greengrass/definition/cores/{CoreDefinitionId}
- "Get version details?" -> GET /greengrass/definition/cores/{CoreDefinitionId}/versions/{CoreDefinitionVersionId}
- "List all status?" -> GET /greengrass/groups/{GroupId}/deployments/{DeploymentId}/status
- "Get device details?" -> GET /greengrass/definition/devices/{DeviceDefinitionId}
- "Get version details?" -> GET /greengrass/definition/devices/{DeviceDefinitionId}/versions/{DeviceDefinitionVersionId}
- "Get function details?" -> GET /greengrass/definition/functions/{FunctionDefinitionId}
- "Get version details?" -> GET /greengrass/definition/functions/{FunctionDefinitionId}/versions/{FunctionDefinitionVersionId}
- "Get group details?" -> GET /greengrass/groups/{GroupId}
- "Get certificateauthority details?" -> GET /greengrass/groups/{GroupId}/certificateauthorities/{CertificateAuthorityId}
- "List all expiry?" -> GET /greengrass/groups/{GroupId}/certificateauthorities/configuration/expiry
- "Get version details?" -> GET /greengrass/groups/{GroupId}/versions/{GroupVersionId}
- "Get logger details?" -> GET /greengrass/definition/loggers/{LoggerDefinitionId}
- "Get version details?" -> GET /greengrass/definition/loggers/{LoggerDefinitionId}/versions/{LoggerDefinitionVersionId}
- "Get resource details?" -> GET /greengrass/definition/resources/{ResourceDefinitionId}
- "Get version details?" -> GET /greengrass/definition/resources/{ResourceDefinitionId}/versions/{ResourceDefinitionVersionId}
- "List all servicerole?" -> GET /greengrass/servicerole
- "Get subscription details?" -> GET /greengrass/definition/subscriptions/{SubscriptionDefinitionId}
- "Get version details?" -> GET /greengrass/definition/subscriptions/{SubscriptionDefinitionId}/versions/{SubscriptionDefinitionVersionId}
- "List all runtimeconfig?" -> GET /greengrass/things/{ThingName}/runtimeconfig
- "List all detailed-reports?" -> GET /greengrass/bulk/deployments/{BulkDeploymentId}/detailed-reports
- "List all deployments?" -> GET /greengrass/bulk/deployments
- "List all versions?" -> GET /greengrass/definition/connectors/{ConnectorDefinitionId}/versions
- "List all connectors?" -> GET /greengrass/definition/connectors
- "List all versions?" -> GET /greengrass/definition/cores/{CoreDefinitionId}/versions
- "List all cores?" -> GET /greengrass/definition/cores
- "List all deployments?" -> GET /greengrass/groups/{GroupId}/deployments
- "List all versions?" -> GET /greengrass/definition/devices/{DeviceDefinitionId}/versions
- "List all devices?" -> GET /greengrass/definition/devices
- "List all versions?" -> GET /greengrass/definition/functions/{FunctionDefinitionId}/versions
- "List all functions?" -> GET /greengrass/definition/functions
- "List all certificateauthorities?" -> GET /greengrass/groups/{GroupId}/certificateauthorities
- "List all versions?" -> GET /greengrass/groups/{GroupId}/versions
- "List all groups?" -> GET /greengrass/groups
- "List all versions?" -> GET /greengrass/definition/loggers/{LoggerDefinitionId}/versions
- "List all loggers?" -> GET /greengrass/definition/loggers
- "List all versions?" -> GET /greengrass/definition/resources/{ResourceDefinitionId}/versions
- "List all resources?" -> GET /greengrass/definition/resources
- "List all versions?" -> GET /greengrass/definition/subscriptions/{SubscriptionDefinitionId}/versions
- "List all subscriptions?" -> GET /greengrass/definition/subscriptions
- "Get tag details?" -> GET /tags/{resource-arn}
- "Create a $reset?" -> POST /greengrass/groups/{GroupId}/deployments/$reset
- "Create a deployment?" -> POST /greengrass/bulk/deployments
- "Delete a tag?" -> DELETE /tags/{resource-arn}
- "Update a connector?" -> PUT /greengrass/definition/connectors/{ConnectorDefinitionId}
- "Update a core?" -> PUT /greengrass/definition/cores/{CoreDefinitionId}
- "Update a device?" -> PUT /greengrass/definition/devices/{DeviceDefinitionId}
- "Update a function?" -> PUT /greengrass/definition/functions/{FunctionDefinitionId}
- "Update a group?" -> PUT /greengrass/groups/{GroupId}
- "Update a logger?" -> PUT /greengrass/definition/loggers/{LoggerDefinitionId}
- "Update a resource?" -> PUT /greengrass/definition/resources/{ResourceDefinitionId}
- "Update a subscription?" -> PUT /greengrass/definition/subscriptions/{SubscriptionDefinitionId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
