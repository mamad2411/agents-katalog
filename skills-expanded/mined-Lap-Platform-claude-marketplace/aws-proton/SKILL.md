---
name: aws-proton
description: "AWS Proton API skill. Use when working with AWS Proton for root. Covers 87 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Proton
API version: 2020-07-20

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

87 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | In a management account, an environment account connection request is accepted. When the environment account connection request is accepted, Proton can use the associated IAM role to provision environment infrastructure resources in the associated environment account. For more information, see Environment account connections in the Proton User guide. |
| POST | / | Attempts to cancel a component deployment (for a component that is in the IN_PROGRESS deployment status). For more information about components, see Proton components in the Proton User Guide. |
| POST | / | Attempts to cancel an environment deployment on an UpdateEnvironment action, if the deployment is IN_PROGRESS. For more information, see Update an environment in the Proton User guide. The following list includes potential cancellation scenarios.   If the cancellation attempt succeeds, the resulting deployment state is CANCELLED.   If the cancellation attempt fails, the resulting deployment state is FAILED.   If the current UpdateEnvironment action succeeds before the cancellation attempt starts, the resulting deployment state is SUCCEEDED and the cancellation attempt has no effect. |
| POST | / | Attempts to cancel a service instance deployment on an UpdateServiceInstance action, if the deployment is IN_PROGRESS. For more information, see Update a service instance in the Proton User guide. The following list includes potential cancellation scenarios.   If the cancellation attempt succeeds, the resulting deployment state is CANCELLED.   If the cancellation attempt fails, the resulting deployment state is FAILED.   If the current UpdateServiceInstance action succeeds before the cancellation attempt starts, the resulting deployment state is SUCCEEDED and the cancellation attempt has no effect. |
| POST | / | Attempts to cancel a service pipeline deployment on an UpdateServicePipeline action, if the deployment is IN_PROGRESS. For more information, see Update a service pipeline in the Proton User guide. The following list includes potential cancellation scenarios.   If the cancellation attempt succeeds, the resulting deployment state is CANCELLED.   If the cancellation attempt fails, the resulting deployment state is FAILED.   If the current UpdateServicePipeline action succeeds before the cancellation attempt starts, the resulting deployment state is SUCCEEDED and the cancellation attempt has no effect. |
| POST | / | Create an Proton component. A component is an infrastructure extension for a service instance. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | Deploy a new environment. An Proton environment is created from an environment template that defines infrastructure and resources that can be shared across services.  You can provision environments using the following methods:    Amazon Web Services-managed provisioning: Proton makes direct calls to provision your resources.   Self-managed provisioning: Proton makes pull requests on your repository to provide compiled infrastructure as code (IaC) files that your IaC engine uses to provision resources.   For more information, see Environments and Provisioning methods in the Proton User Guide. |
| POST | / | Create an environment account connection in an environment account so that environment infrastructure resources can be provisioned in the environment account from a management account. An environment account connection is a secure bi-directional connection between a management account and an environment account that maintains authorization and permissions. For more information, see Environment account connections in the Proton User guide. |
| POST | / | Create an environment template for Proton. For more information, see Environment Templates in the Proton User Guide. You can create an environment template in one of the two following ways:   Register and publish a standard environment template that instructs Proton to deploy and manage environment infrastructure.   Register and publish a customer managed environment template that connects Proton to your existing provisioned infrastructure that you manage. Proton doesn't manage your existing provisioned infrastructure. To create an environment template for customer provisioned and managed infrastructure, include the provisioning parameter and set the value to CUSTOMER_MANAGED. For more information, see Register and publish an environment template in the Proton User Guide. |
| POST | / | Create a new major or minor version of an environment template. A major version of an environment template is a version that isn't backwards compatible. A minor version of an environment template is a version that's backwards compatible within its major version. |
| POST | / | Create and register a link to a repository. Proton uses the link to repeatedly access the repository, to either push to it (self-managed provisioning) or pull from it (template sync). You can share a linked repository across multiple resources (like environments using self-managed provisioning, or synced templates). When you create a repository link, Proton creates a service-linked role for you. For more information, see Self-managed provisioning, Template bundles, and Template sync configurations in the Proton User Guide. |
| POST | / | Create an Proton service. An Proton service is an instantiation of a service template and often includes several service instances and pipeline. For more information, see Services in the Proton User Guide. |
| POST | / | Create a service instance. |
| POST | / | Create the Proton Ops configuration file. |
| POST | / | Create a service template. The administrator creates a service template to define standardized infrastructure and an optional CI/CD service pipeline. Developers, in turn, select the service template from Proton. If the selected service template includes a service pipeline definition, they provide a link to their source code repository. Proton then deploys and manages the infrastructure defined by the selected service template. For more information, see Proton templates in the Proton User Guide. |
| POST | / | Create a new major or minor version of a service template. A major version of a service template is a version that isn't backward compatible. A minor version of a service template is a version that's backward compatible within its major version. |
| POST | / | Set up a template to create new template versions automatically by tracking a linked repository. A linked repository is a repository that has been registered with Proton. For more information, see CreateRepository. When a commit is pushed to your linked repository, Proton checks for changes to your repository template bundles. If it detects a template bundle change, a new major or minor version of its template is created, if the version doesn’t already exist. For more information, see Template sync configurations in the Proton User Guide. |
| POST | / | Delete an Proton component resource. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | Delete the deployment. |
| POST | / | Delete an environment. |
| POST | / | In an environment account, delete an environment account connection. After you delete an environment account connection that’s in use by an Proton environment, Proton can’t manage the environment infrastructure resources until a new environment account connection is accepted for the environment account and associated environment. You're responsible for cleaning up provisioned resources that remain without an environment connection. For more information, see Environment account connections in the Proton User guide. |
| POST | / | If no other major or minor versions of an environment template exist, delete the environment template. |
| POST | / | If no other minor versions of an environment template exist, delete a major version of the environment template if it's not the Recommended version. Delete the Recommended version of the environment template if no other major versions or minor versions of the environment template exist. A major version of an environment template is a version that's not backward compatible. Delete a minor version of an environment template if it isn't the Recommended version. Delete a Recommended minor version of the environment template if no other minor versions of the environment template exist. A minor version of an environment template is a version that's backward compatible. |
| POST | / | De-register and unlink your repository. |
| POST | / | Delete a service, with its instances and pipeline.  You can't delete a service if it has any service instances that have components attached to them. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | Delete the Proton Ops file. |
| POST | / | If no other major or minor versions of the service template exist, delete the service template. |
| POST | / | If no other minor versions of a service template exist, delete a major version of the service template if it's not the Recommended version. Delete the Recommended version of the service template if no other major versions or minor versions of the service template exist. A major version of a service template is a version that isn't backwards compatible. Delete a minor version of a service template if it's not the Recommended version. Delete a Recommended minor version of the service template if no other minor versions of the service template exist. A minor version of a service template is a version that's backwards compatible. |
| POST | / | Delete a template sync configuration. |
| POST | / | Get detail data for Proton account-wide settings. |
| POST | / | Get detailed data for a component. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | Get detailed data for a deployment. |
| POST | / | Get detailed data for an environment. |
| POST | / | In an environment account, get the detailed data for an environment account connection. For more information, see Environment account connections in the Proton User guide. |
| POST | / | Get detailed data for an environment template. |
| POST | / | Get detailed data for a major or minor version of an environment template. |
| POST | / | Get detail data for a linked repository. |
| POST | / | Get the sync status of a repository used for Proton template sync. For more information about template sync, see .  A repository sync status isn't tied to the Proton Repository resource (or any other Proton resource). Therefore, tags on an Proton Repository resource have no effect on this action. Specifically, you can't use these tags to control access to this action using Attribute-based access control (ABAC). For more information about ABAC, see ABAC in the Proton User Guide. |
| POST | / | Get counts of Proton resources. For infrastructure-provisioning resources (environments, services, service instances, pipelines), the action returns staleness counts. A resource is stale when it's behind the recommended version of the Proton template that it uses and it needs an update to become current. The action returns staleness counts (counts of resources that are up-to-date, behind a template major version, or behind a template minor version), the total number of resources, and the number of resources that are in a failed state, grouped by resource type. Components, environments, and service templates return less information - see the components, environments, and serviceTemplates field descriptions. For context, the action also returns the total number of each type of Proton template in the Amazon Web Services account. For more information, see Proton dashboard in the Proton User Guide. |
| POST | / | Get detailed data for a service. |
| POST | / | Get detailed data for a service instance. A service instance is an instantiation of service template and it runs in a specific environment. |
| POST | / | Get the status of the synced service instance. |
| POST | / | Get detailed data for the service sync blocker summary. |
| POST | / | Get detailed information for the service sync configuration. |
| POST | / | Get detailed data for a service template. |
| POST | / | Get detailed data for a major or minor version of a service template. |
| POST | / | Get detail data for a template sync configuration. |
| POST | / | Get the status of a template sync. |
| POST | / | Get a list of component Infrastructure as Code (IaC) outputs. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | List provisioned resources for a component with details. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | List components with summary data. You can filter the result list by environment, service, or a single service instance. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | List deployments. You can filter the result list by environment, service, or a single service instance. |
| POST | / | View a list of environment account connections. For more information, see Environment account connections in the Proton User guide. |
| POST | / | List the infrastructure as code outputs for your environment. |
| POST | / | List the provisioned resources for your environment. |
| POST | / | List major or minor versions of an environment template with detail data. |
| POST | / | List environment templates. |
| POST | / | List environments with detail data summaries. |
| POST | / | List linked repositories with detail data. |
| POST | / | List repository sync definitions with detail data. |
| POST | / | Get a list service of instance Infrastructure as Code (IaC) outputs. |
| POST | / | List provisioned resources for a service instance with details. |
| POST | / | List service instances with summary data. This action lists service instances of all services in the Amazon Web Services account. |
| POST | / | Get a list of service pipeline Infrastructure as Code (IaC) outputs. |
| POST | / | List provisioned resources for a service and pipeline with details. |
| POST | / | List major or minor versions of a service template with detail data. |
| POST | / | List service templates with detail data. |
| POST | / | List services with summaries of detail data. |
| POST | / | List tags for a resource. For more information, see Proton resources and tagging in the Proton User Guide. |
| POST | / | Notify Proton of status changes to a provisioned resource when you use self-managed provisioning. For more information, see Self-managed provisioning in the Proton User Guide. |
| POST | / | In a management account, reject an environment account connection from another environment account. After you reject an environment account connection request, you can't accept or use the rejected environment account connection. You can’t reject an environment account connection that's connected to an environment. For more information, see Environment account connections in the Proton User guide. |
| POST | / | Tag a resource. A tag is a key-value pair of metadata that you associate with an Proton resource. For more information, see Proton resources and tagging in the Proton User Guide. |
| POST | / | Remove a customer tag from a resource. A tag is a key-value pair of metadata associated with an Proton resource. For more information, see Proton resources and tagging in the Proton User Guide. |
| POST | / | Update Proton settings that are used for multiple services in the Amazon Web Services account. |
| POST | / | Update a component. There are a few modes for updating a component. The deploymentType field defines the mode.  You can't update a component while its deployment status, or the deployment status of a service instance attached to it, is IN_PROGRESS.  For more information about components, see Proton components in the Proton User Guide. |
| POST | / | Update an environment. If the environment is associated with an environment account connection, don't update or include the protonServiceRoleArn and provisioningRepository parameter to update or connect to an environment account connection. You can only update to a new environment account connection if that connection was created in the same environment account that the current environment account connection was created in. The account connection must also be associated with the current environment. If the environment isn't associated with an environment account connection, don't update or include the environmentAccountConnectionId parameter. You can't update or connect the environment to an environment account connection if it isn't already associated with an environment connection. You can update either the environmentAccountConnectionId or protonServiceRoleArn parameter and value. You can’t update both. If the environment was configured for Amazon Web Services-managed provisioning, omit the provisioningRepository parameter. If the environment was configured for self-managed provisioning, specify the provisioningRepository parameter and omit the protonServiceRoleArn and environmentAccountConnectionId parameters. For more information, see Environments and Provisioning methods in the Proton User Guide. There are four modes for updating an environment. The deploymentType field defines the mode.     NONE  In this mode, a deployment doesn't occur. Only the requested metadata parameters are updated.     CURRENT_VERSION  In this mode, the environment is deployed and updated with the new spec that you provide. Only requested parameters are updated. Don’t include minor or major version parameters when you use this deployment-type.     MINOR_VERSION  In this mode, the environment is deployed and updated with the published, recommended (latest) minor version of the current major version in use, by default. You can also specify a different minor version of the current major version in use.     MAJOR_VERSION  In this mode, the environment is deployed and updated with the published, recommended (latest) major and minor version of the current template, by default. You can also specify a different major version that's higher than the major version in use and a minor version. |
| POST | / | In an environment account, update an environment account connection to use a new IAM role. For more information, see Environment account connections in the Proton User guide. |
| POST | / | Update an environment template. |
| POST | / | Update a major or minor version of an environment template. |
| POST | / | Edit a service description or use a spec to add and delete service instances.  Existing service instances and the service pipeline can't be edited using this API. They can only be deleted.  Use the description parameter to modify the description. Edit the spec parameter to add or delete instances.  You can't delete a service instance (remove it from the spec) if it has an attached component. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | Update a service instance. There are a few modes for updating a service instance. The deploymentType field defines the mode.  You can't update a service instance while its deployment status, or the deployment status of a component attached to it, is IN_PROGRESS. For more information about components, see Proton components in the Proton User Guide. |
| POST | / | Update the service pipeline. There are four modes for updating a service pipeline. The deploymentType field defines the mode.     NONE  In this mode, a deployment doesn't occur. Only the requested metadata parameters are updated.     CURRENT_VERSION  In this mode, the service pipeline is deployed and updated with the new spec that you provide. Only requested parameters are updated. Don’t include major or minor version parameters when you use this deployment-type.     MINOR_VERSION  In this mode, the service pipeline is deployed and updated with the published, recommended (latest) minor version of the current major version in use, by default. You can specify a different minor version of the current major version in use.     MAJOR_VERSION  In this mode, the service pipeline is deployed and updated with the published, recommended (latest) major and minor version of the current template by default. You can specify a different major version that's higher than the major version in use and a minor version. |
| POST | / | Update the service sync blocker by resolving it. |
| POST | / | Update the Proton Ops config file. |
| POST | / | Update a service template. |
| POST | / | Update a major or minor version of a service template. |
| POST | / | Update template sync configuration parameters, except for the templateName and templateType. Repository details (branch, name, and provider) should be of a linked repository. A linked repository is a repository that has been registered with Proton. For more information, see CreateRepository. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
