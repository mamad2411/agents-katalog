---
name: aws-elastic-beanstalk
description: "AWS Elastic Beanstalk API skill. Use when working with AWS Elastic Beanstalk for root. Covers 47 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Elastic Beanstalk
API version: 2010-12-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

47 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Cancels in-progress environment configuration update or application version deployment. |
| POST | / | Applies a scheduled managed action immediately. A managed action can be applied only if its status is Scheduled. Get the status and action ID of a managed action with DescribeEnvironmentManagedActions. |
| POST | / | Add or change the operations role used by an environment. After this call is made, Elastic Beanstalk uses the associated operations role for permissions to downstream services during subsequent calls acting on this environment. For more information, see Operations roles in the AWS Elastic Beanstalk Developer Guide. |
| POST | / | Checks if the specified CNAME is available. |
| POST | / | Create or update a group of environments that each run a separate component of a single application. Takes a list of version labels that specify application source bundles for each of the environments to create or update. The name of each environment and other required information must be included in the source bundles in an environment manifest named env.yaml. See Compose Environments for details. |
| POST | / | Creates an application that has one configuration template named default and no application versions. |
| POST | / | Creates an application version for the specified application. You can create an application version from a source bundle in Amazon S3, a commit in AWS CodeCommit, or the output of an AWS CodeBuild build as follows: Specify a commit in an AWS CodeCommit repository with SourceBuildInformation. Specify a build in an AWS CodeBuild with SourceBuildInformation and BuildConfiguration. Specify a source bundle in S3 with SourceBundle  Omit both SourceBuildInformation and SourceBundle to use the default sample application.  After you create an application version with a specified Amazon S3 bucket and key location, you can't change that Amazon S3 location. If you change the Amazon S3 location, you receive an exception when you attempt to launch an environment from the application version. |
| POST | / | Creates an AWS Elastic Beanstalk configuration template, associated with a specific Elastic Beanstalk application. You define application configuration settings in a configuration template. You can then use the configuration template to deploy different versions of the application with the same configuration settings. Templates aren't associated with any environment. The EnvironmentName response element is always null. Related Topics    DescribeConfigurationOptions     DescribeConfigurationSettings     ListAvailableSolutionStacks |
| POST | / | Launches an AWS Elastic Beanstalk environment for the specified application using the specified configuration. |
| POST | / | Create a new version of your custom platform. |
| POST | / | Creates a bucket in Amazon S3 to store application versions, logs, and other files used by Elastic Beanstalk environments. The Elastic Beanstalk console and EB CLI call this API the first time you create an environment in a region. If the storage location already exists, CreateStorageLocation still returns the bucket name but does not create a new bucket. |
| POST | / | Deletes the specified application along with all associated versions and configurations. The application versions will not be deleted from your Amazon S3 bucket.  You cannot delete an application that has a running environment. |
| POST | / | Deletes the specified version from the specified application.  You cannot delete an application version that is associated with a running environment. |
| POST | / | Deletes the specified configuration template.  When you launch an environment using a configuration template, the environment gets a copy of the template. You can delete or modify the environment's copy of the template without affecting the running environment. |
| POST | / | Deletes the draft configuration associated with the running environment. Updating a running environment with any configuration changes creates a draft configuration set. You can get the draft configuration using DescribeConfigurationSettings while the update is in progress or if the update fails. The DeploymentStatus for the draft configuration indicates whether the deployment is in process or has failed. The draft configuration remains in existence until it is deleted with this action. |
| POST | / | Deletes the specified version of a custom platform. |
| POST | / | Returns attributes related to AWS Elastic Beanstalk that are associated with the calling AWS account. The result currently has one set of attributes—resource quotas. |
| POST | / | Retrieve a list of application versions. |
| POST | / | Returns the descriptions of existing applications. |
| POST | / | Describes the configuration options that are used in a particular configuration template or environment, or that a specified solution stack defines. The description includes the values the options, their default values, and an indication of the required action on a running environment if an option value is changed. |
| POST | / | Returns a description of the settings for the specified configuration set, that is, either a configuration template or the configuration set associated with a running environment. When describing the settings for the configuration set associated with a running environment, it is possible to receive two sets of setting descriptions. One is the deployed configuration set, and the other is a draft configuration of an environment that is either in the process of deployment or that failed to deploy. Related Topics    DeleteEnvironmentConfiguration |
| POST | / | Returns information about the overall health of the specified environment. The DescribeEnvironmentHealth operation is only available with AWS Elastic Beanstalk Enhanced Health. |
| POST | / | Lists an environment's completed and failed managed actions. |
| POST | / | Lists an environment's upcoming and in-progress managed actions. |
| POST | / | Returns AWS resources for this environment. |
| POST | / | Returns descriptions for existing environments. |
| POST | / | Returns list of event descriptions matching criteria up to the last 6 weeks.  This action returns the most recent 1,000 events from the specified NextToken. |
| POST | / | Retrieves detailed information about the health of instances in your AWS Elastic Beanstalk. This operation requires enhanced health reporting. |
| POST | / | Describes a platform version. Provides full details. Compare to ListPlatformVersions, which provides summary information about a list of platform versions. For definitions of platform version and other platform-related terms, see AWS Elastic Beanstalk Platforms Glossary. |
| POST | / | Disassociate the operations role from an environment. After this call is made, Elastic Beanstalk uses the caller's permissions for permissions to downstream services during subsequent calls acting on this environment. For more information, see Operations roles in the AWS Elastic Beanstalk Developer Guide. |
| POST | / | Returns a list of the available solution stack names, with the public version first and then in reverse chronological order. |
| POST | / | Lists the platform branches available for your account in an AWS Region. Provides summary information about each platform branch. For definitions of platform branch and other platform-related terms, see AWS Elastic Beanstalk Platforms Glossary. |
| POST | / | Lists the platform versions available for your account in an AWS Region. Provides summary information about each platform version. Compare to DescribePlatformVersion, which provides full details about a single platform version. For definitions of platform version and other platform-related terms, see AWS Elastic Beanstalk Platforms Glossary. |
| POST | / | Return the tags applied to an AWS Elastic Beanstalk resource. The response contains a list of tag key-value pairs. Elastic Beanstalk supports tagging of all of its resources. For details about resource tagging, see Tagging Application Resources. |
| POST | / | Deletes and recreates all of the AWS resources (for example: the Auto Scaling group, load balancer, etc.) for a specified environment and forces a restart. |
| POST | / | Initiates a request to compile the specified type of information of the deployed environment.  Setting the InfoType to tail compiles the last lines from the application server log files of every Amazon EC2 instance in your environment.   Setting the InfoType to bundle compresses the application server log files for every Amazon EC2 instance into a .zip file. Legacy and .NET containers do not support bundle logs.   Use RetrieveEnvironmentInfo to obtain the set of logs.  Related Topics    RetrieveEnvironmentInfo |
| POST | / | Causes the environment to restart the application container server running on each Amazon EC2 instance. |
| POST | / | Retrieves the compiled information from a RequestEnvironmentInfo request. Related Topics    RequestEnvironmentInfo |
| POST | / | Swaps the CNAMEs of two environments. |
| POST | / | Terminates the specified environment. |
| POST | / | Updates the specified application to have the specified properties.  If a property (for example, description) is not provided, the value remains unchanged. To clear these properties, specify an empty string. |
| POST | / | Modifies lifecycle settings for an application. |
| POST | / | Updates the specified application version to have the specified properties.  If a property (for example, description) is not provided, the value remains unchanged. To clear properties, specify an empty string. |
| POST | / | Updates the specified configuration template to have the specified properties or configuration option values.  If a property (for example, ApplicationName) is not provided, its value remains unchanged. To clear such properties, specify an empty string.  Related Topics    DescribeConfigurationOptions |
| POST | / | Updates the environment description, deploys a new application version, updates the configuration settings to an entirely new configuration template, or updates select configuration option values in the running environment.  Attempting to update both the release and configuration is not allowed and AWS Elastic Beanstalk returns an InvalidParameterCombination error.   When updating the configuration settings to a new template or individual settings, a draft configuration is created and DescribeConfigurationSettings for this environment returns two setting descriptions with different DeploymentStatus values. |
| POST | / | Update the list of tags applied to an AWS Elastic Beanstalk resource. Two lists can be passed: TagsToAdd for tags to add or update, and TagsToRemove. Elastic Beanstalk supports tagging of all of its resources. For details about resource tagging, see Tagging Application Resources. If you create a custom IAM user policy to control permission to this operation, specify one of the following two virtual actions (or both) instead of the API operation name:  elasticbeanstalk:AddTags  Controls permission to call UpdateTagsForResource and pass a list of tags to add in the TagsToAdd parameter.  elasticbeanstalk:RemoveTags  Controls permission to call UpdateTagsForResource and pass a list of tag keys to remove in the TagsToRemove parameter.   For details about creating a custom user policy, see Creating a Custom User Policy. |
| POST | / | Takes a set of configuration settings and either a configuration template or environment, and determines whether those values are valid. This action returns a list of messages indicating any errors or warnings associated with the selection of option values. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
