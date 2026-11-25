---
name: amazon-appconfig
description: "Amazon AppConfig API skill. Use when working with Amazon AppConfig for applications, deploymentstrategies, extensions. Covers 45 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon AppConfig
API version: 2019-10-09

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /settings -- verify access
3. POST /applications -- create first applications

## Endpoints

45 endpoints across 7 groups. See references/api-spec.lap for full details.

### applications
| Method | Path | Description |
|--------|------|-------------|
| POST | /applications | Creates an application. In AppConfig, an application is simply an organizational construct like a folder. This organizational construct has a relationship with some unit of executable code. For example, you could create an application called MyMobileApp to organize and manage configuration data for a mobile application installed by your users. |
| POST | /applications/{ApplicationId}/configurationprofiles | Creates a configuration profile, which is information that enables AppConfig to access the configuration source. Valid configuration sources include the following:   Configuration data in YAML, JSON, and other formats stored in the AppConfig hosted configuration store   Configuration data stored as objects in an Amazon Simple Storage Service (Amazon S3) bucket   Pipelines stored in CodePipeline   Secrets stored in Secrets Manager   Standard and secure string parameters stored in Amazon Web Services Systems Manager Parameter Store   Configuration data in SSM documents stored in the Systems Manager document store   A configuration profile includes the following information:   The URI location of the configuration data.   The Identity and Access Management (IAM) role that provides access to the configuration data.   A validator for the configuration data. Available validators include either a JSON Schema or an Amazon Web Services Lambda function.   For more information, see Create a Configuration and a Configuration Profile in the AppConfig User Guide. |
| POST | /applications/{ApplicationId}/environments | Creates an environment. For each application, you define one or more environments. An environment is a deployment group of AppConfig targets, such as applications in a Beta or Production environment. You can also define environments for application subcomponents such as the Web, Mobile and Back-end components for your application. You can configure Amazon CloudWatch alarms for each environment. The system monitors alarms during a configuration deployment. If an alarm is triggered, the system rolls back the configuration. |
| POST | /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/hostedconfigurationversions | Creates a new configuration in the AppConfig hosted configuration store. If you're creating a feature flag, we recommend you familiarize yourself with the JSON schema for feature flag data. For more information, see Type reference for AWS.AppConfig.FeatureFlags in the AppConfig User Guide. |
| DELETE | /applications/{ApplicationId} | Deletes an application. |
| DELETE | /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId} | Deletes a configuration profile. To prevent users from unintentionally deleting actively-used configuration profiles, enable deletion protection. |
| DELETE | /applications/{ApplicationId}/environments/{EnvironmentId} | Deletes an environment. To prevent users from unintentionally deleting actively-used environments, enable deletion protection. |
| DELETE | /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/hostedconfigurationversions/{VersionNumber} | Deletes a version of a configuration from the AppConfig hosted configuration store. |
| GET | /applications/{ApplicationId} | Retrieves information about an application. |
| GET | /applications/{Application}/environments/{Environment}/configurations/{Configuration} | (Deprecated) Retrieves the latest deployed configuration.  Note the following important information.   This API action is deprecated. Calls to receive configuration data should use the StartConfigurationSession and GetLatestConfiguration APIs instead.     GetConfiguration is a priced call. For more information, see Pricing. |
| GET | /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId} | Retrieves information about a configuration profile. |
| GET | /applications/{ApplicationId}/environments/{EnvironmentId}/deployments/{DeploymentNumber} | Retrieves information about a configuration deployment. |
| GET | /applications/{ApplicationId}/environments/{EnvironmentId} | Retrieves information about an environment. An environment is a deployment group of AppConfig applications, such as applications in a Production environment or in an EU_Region environment. Each configuration deployment targets an environment. You can enable one or more Amazon CloudWatch alarms for an environment. If an alarm is triggered during a deployment, AppConfig roles back the configuration. |
| GET | /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/hostedconfigurationversions/{VersionNumber} | Retrieves information about a specific configuration version. |
| GET | /applications | Lists all applications in your Amazon Web Services account. |
| GET | /applications/{ApplicationId}/configurationprofiles | Lists the configuration profiles for an application. |
| GET | /applications/{ApplicationId}/environments/{EnvironmentId}/deployments | Lists the deployments for an environment in descending deployment number order. |
| GET | /applications/{ApplicationId}/environments | Lists the environments for an application. |
| GET | /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/hostedconfigurationversions | Lists configurations stored in the AppConfig hosted configuration store by version. |
| POST | /applications/{ApplicationId}/environments/{EnvironmentId}/deployments | Starts a deployment. |
| DELETE | /applications/{ApplicationId}/environments/{EnvironmentId}/deployments/{DeploymentNumber} | Stops a deployment. This API action works only on deployments that have a status of DEPLOYING. This action moves the deployment to a status of ROLLED_BACK. |
| PATCH | /applications/{ApplicationId} | Updates an application. |
| PATCH | /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId} | Updates a configuration profile. |
| PATCH | /applications/{ApplicationId}/environments/{EnvironmentId} | Updates an environment. |
| POST | /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/validators | Uses the validators in a configuration profile to validate a configuration. |

### deploymentstrategies
| Method | Path | Description |
|--------|------|-------------|
| POST | /deploymentstrategies | Creates a deployment strategy that defines important criteria for rolling out your configuration to the designated targets. A deployment strategy includes the overall duration required, a percentage of targets to receive the deployment during each interval, an algorithm that defines how percentage grows, and bake time. |
| GET | /deploymentstrategies/{DeploymentStrategyId} | Retrieves information about a deployment strategy. A deployment strategy defines important criteria for rolling out your configuration to the designated targets. A deployment strategy includes the overall duration required, a percentage of targets to receive the deployment during each interval, an algorithm that defines how percentage grows, and bake time. |
| GET | /deploymentstrategies | Lists deployment strategies. |
| PATCH | /deploymentstrategies/{DeploymentStrategyId} | Updates a deployment strategy. |

### extensions
| Method | Path | Description |
|--------|------|-------------|
| POST | /extensions | Creates an AppConfig extension. An extension augments your ability to inject logic or behavior at different points during the AppConfig workflow of creating or deploying a configuration. You can create your own extensions or use the Amazon Web Services authored extensions provided by AppConfig. For an AppConfig extension that uses Lambda, you must create a Lambda function to perform any computation and processing defined in the extension. If you plan to create custom versions of the Amazon Web Services authored notification extensions, you only need to specify an Amazon Resource Name (ARN) in the Uri field for the new extension version.   For a custom EventBridge notification extension, enter the ARN of the EventBridge default events in the Uri field.   For a custom Amazon SNS notification extension, enter the ARN of an Amazon SNS topic in the Uri field.   For a custom Amazon SQS notification extension, enter the ARN of an Amazon SQS message queue in the Uri field.    For more information about extensions, see Extending workflows in the AppConfig User Guide. |
| DELETE | /extensions/{ExtensionIdentifier} | Deletes an AppConfig extension. You must delete all associations to an extension before you delete the extension. |
| GET | /extensions/{ExtensionIdentifier} | Returns information about an AppConfig extension. |
| GET | /extensions | Lists all custom and Amazon Web Services authored AppConfig extensions in the account. For more information about extensions, see Extending workflows in the AppConfig User Guide. |
| PATCH | /extensions/{ExtensionIdentifier} | Updates an AppConfig extension. For more information about extensions, see Extending workflows in the AppConfig User Guide. |

### extensionassociations
| Method | Path | Description |
|--------|------|-------------|
| POST | /extensionassociations | When you create an extension or configure an Amazon Web Services authored extension, you associate the extension with an AppConfig application, environment, or configuration profile. For example, you can choose to run the AppConfig deployment events to Amazon SNS Amazon Web Services authored extension and receive notifications on an Amazon SNS topic anytime a configuration deployment is started for a specific application. Defining which extension to associate with an AppConfig resource is called an extension association. An extension association is a specified relationship between an extension and an AppConfig resource, such as an application or a configuration profile. For more information about extensions and associations, see Extending workflows in the AppConfig User Guide. |
| DELETE | /extensionassociations/{ExtensionAssociationId} | Deletes an extension association. This action doesn't delete extensions defined in the association. |
| GET | /extensionassociations/{ExtensionAssociationId} | Returns information about an AppConfig extension association. For more information about extensions and associations, see Extending workflows in the AppConfig User Guide. |
| GET | /extensionassociations | Lists all AppConfig extension associations in the account. For more information about extensions and associations, see Extending workflows in the AppConfig User Guide. |
| PATCH | /extensionassociations/{ExtensionAssociationId} | Updates an association. For more information about extensions and associations, see Extending workflows in the AppConfig User Guide. |

### deployementstrategies
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /deployementstrategies/{DeploymentStrategyId} | Deletes a deployment strategy. |

### settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /settings | Returns information about the status of the DeletionProtection parameter. |
| PATCH | /settings | Updates the value of the DeletionProtection parameter. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | Retrieves the list of key-value tags assigned to the resource. |
| POST | /tags/{ResourceArn} | Assigns metadata to an AppConfig resource. Tags help organize and categorize your AppConfig resources. Each tag consists of a key and an optional value, both of which you define. You can specify a maximum of 50 tags for a resource. |
| DELETE | /tags/{ResourceArn} | Deletes a tag key and value from an AppConfig resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a application?" -> POST /applications
- "Create a configurationprofile?" -> POST /applications/{ApplicationId}/configurationprofiles
- "Create a deploymentstrategy?" -> POST /deploymentstrategies
- "Create a environment?" -> POST /applications/{ApplicationId}/environments
- "Create a extension?" -> POST /extensions
- "Create a extensionassociation?" -> POST /extensionassociations
- "Create a hostedconfigurationversion?" -> POST /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/hostedconfigurationversions
- "Delete a application?" -> DELETE /applications/{ApplicationId}
- "Delete a configurationprofile?" -> DELETE /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}
- "Delete a deployementstrategy?" -> DELETE /deployementstrategies/{DeploymentStrategyId}
- "Delete a environment?" -> DELETE /applications/{ApplicationId}/environments/{EnvironmentId}
- "Delete a extension?" -> DELETE /extensions/{ExtensionIdentifier}
- "Delete a extensionassociation?" -> DELETE /extensionassociations/{ExtensionAssociationId}
- "Delete a hostedconfigurationversion?" -> DELETE /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/hostedconfigurationversions/{VersionNumber}
- "List all settings?" -> GET /settings
- "Get application details?" -> GET /applications/{ApplicationId}
- "Get configuration details?" -> GET /applications/{Application}/environments/{Environment}/configurations/{Configuration}
- "Get configurationprofile details?" -> GET /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}
- "Get deployment details?" -> GET /applications/{ApplicationId}/environments/{EnvironmentId}/deployments/{DeploymentNumber}
- "Get deploymentstrategy details?" -> GET /deploymentstrategies/{DeploymentStrategyId}
- "Get environment details?" -> GET /applications/{ApplicationId}/environments/{EnvironmentId}
- "Get extension details?" -> GET /extensions/{ExtensionIdentifier}
- "Get extensionassociation details?" -> GET /extensionassociations/{ExtensionAssociationId}
- "Get hostedconfigurationversion details?" -> GET /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/hostedconfigurationversions/{VersionNumber}
- "List all applications?" -> GET /applications
- "List all configurationprofiles?" -> GET /applications/{ApplicationId}/configurationprofiles
- "List all deploymentstrategies?" -> GET /deploymentstrategies
- "List all deployments?" -> GET /applications/{ApplicationId}/environments/{EnvironmentId}/deployments
- "List all environments?" -> GET /applications/{ApplicationId}/environments
- "List all extensionassociations?" -> GET /extensionassociations
- "List all extensions?" -> GET /extensions
- "List all hostedconfigurationversions?" -> GET /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/hostedconfigurationversions
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Create a deployment?" -> POST /applications/{ApplicationId}/environments/{EnvironmentId}/deployments
- "Delete a deployment?" -> DELETE /applications/{ApplicationId}/environments/{EnvironmentId}/deployments/{DeploymentNumber}
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Partially update a application?" -> PATCH /applications/{ApplicationId}
- "Partially update a configurationprofile?" -> PATCH /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}
- "Partially update a deploymentstrategy?" -> PATCH /deploymentstrategies/{DeploymentStrategyId}
- "Partially update a environment?" -> PATCH /applications/{ApplicationId}/environments/{EnvironmentId}
- "Partially update a extension?" -> PATCH /extensions/{ExtensionIdentifier}
- "Partially update a extensionassociation?" -> PATCH /extensionassociations/{ExtensionAssociationId}
- "Create a validator?" -> POST /applications/{ApplicationId}/configurationprofiles/{ConfigurationProfileId}/validators
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
