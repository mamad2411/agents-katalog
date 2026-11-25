---
name: ec2-image-builder
description: "EC2 Image Builder API skill. Use when working with EC2 Image Builder for CancelImageCreation, CancelLifecycleExecution, CreateComponent. Covers 73 endpoints."
version: 1.0.0
generator: lapsh
---

# EC2 Image Builder
API version: 2019-12-02

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /GetComponent -- verify access
3. POST /ListComponentBuildVersions -- create first ListComponentBuildVersions

## Endpoints

73 endpoints across 71 groups. See references/api-spec.lap for full details.

### CancelImageCreation
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CancelImageCreation | CancelImageCreation cancels the creation of Image. This operation can only be used on images in a non-terminal state. |

### CancelLifecycleExecution
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CancelLifecycleExecution | Cancel a specific image lifecycle policy runtime instance. |

### CreateComponent
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateComponent | Creates a new component that can be used to build, validate, test, and assess your image. The component is based on a YAML document that you specify using exactly one of the following methods:   Inline, using the data property in the request body.   A URL that points to a YAML document file stored in Amazon S3, using the uri property in the request body. |

### CreateContainerRecipe
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateContainerRecipe | Creates a new container recipe. Container recipes define how images are configured, tested, and assessed. |

### CreateDistributionConfiguration
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateDistributionConfiguration | Creates a new distribution configuration. Distribution configurations define and configure the outputs of your pipeline. |

### CreateImage
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateImage | Creates a new image. This request will create a new image along with all of the configured output resources defined in the distribution configuration. You must specify exactly one recipe for your image, using either a ContainerRecipeArn or an ImageRecipeArn. |

### CreateImagePipeline
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateImagePipeline | Creates a new image pipeline. Image pipelines enable you to automate the creation and distribution of images. |

### CreateImageRecipe
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateImageRecipe | Creates a new image recipe. Image recipes define how images are configured, tested, and assessed. |

### CreateInfrastructureConfiguration
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateInfrastructureConfiguration | Creates a new infrastructure configuration. An infrastructure configuration defines the environment in which your image will be built and tested. |

### CreateLifecyclePolicy
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateLifecyclePolicy | Create a lifecycle policy resource. |

### CreateWorkflow
| Method | Path | Description |
|--------|------|-------------|
| PUT | /CreateWorkflow | Create a new workflow or a new version of an existing workflow. |

### DeleteComponent
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteComponent | Deletes a component build version. |

### DeleteContainerRecipe
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteContainerRecipe | Deletes a container recipe. |

### DeleteDistributionConfiguration
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteDistributionConfiguration | Deletes a distribution configuration. |

### DeleteImage
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteImage | Deletes an Image Builder image resource. This does not delete any EC2 AMIs or ECR container images that are created during the image build process. You must clean those up separately, using the appropriate Amazon EC2 or Amazon ECR console actions, or API or CLI commands.   To deregister an EC2 Linux AMI, see Deregister your Linux AMI in the  Amazon EC2 User Guide .   To deregister an EC2 Windows AMI, see Deregister your Windows AMI in the  Amazon EC2 Windows Guide .   To delete a container image from Amazon ECR, see Deleting an image in the Amazon ECR User Guide. |

### DeleteImagePipeline
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteImagePipeline | Deletes an image pipeline. |

### DeleteImageRecipe
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteImageRecipe | Deletes an image recipe. |

### DeleteInfrastructureConfiguration
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteInfrastructureConfiguration | Deletes an infrastructure configuration. |

### DeleteLifecyclePolicy
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteLifecyclePolicy | Delete the specified lifecycle policy resource. |

### DeleteWorkflow
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteWorkflow | Deletes a specific workflow resource. |

### GetComponent
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetComponent | Gets a component object. |

### GetComponentPolicy
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetComponentPolicy | Gets a component policy. |

### GetContainerRecipe
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetContainerRecipe | Retrieves a container recipe. |

### GetContainerRecipePolicy
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetContainerRecipePolicy | Retrieves the policy for a container recipe. |

### GetDistributionConfiguration
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetDistributionConfiguration | Gets a distribution configuration. |

### GetImage
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetImage | Gets an image. |

### GetImagePipeline
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetImagePipeline | Gets an image pipeline. |

### GetImagePolicy
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetImagePolicy | Gets an image policy. |

### GetImageRecipe
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetImageRecipe | Gets an image recipe. |

### GetImageRecipePolicy
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetImageRecipePolicy | Gets an image recipe policy. |

### GetInfrastructureConfiguration
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetInfrastructureConfiguration | Gets an infrastructure configuration. |

### GetLifecycleExecution
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetLifecycleExecution | Get the runtime information that was logged for a specific runtime instance of the lifecycle policy. |

### GetLifecyclePolicy
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetLifecyclePolicy | Get details for the specified image lifecycle policy. |

### GetWorkflow
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetWorkflow | Get a workflow resource object. |

### GetWorkflowExecution
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetWorkflowExecution | Get the runtime information that was logged for a specific runtime instance of the workflow. |

### GetWorkflowStepExecution
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetWorkflowStepExecution | Get the runtime information that was logged for a specific runtime instance of the workflow step. |

### ImportComponent
| Method | Path | Description |
|--------|------|-------------|
| PUT | /ImportComponent | Imports a component and transforms its data into a component document. |

### ImportVmImage
| Method | Path | Description |
|--------|------|-------------|
| PUT | /ImportVmImage | When you export your virtual machine (VM) from its virtualization environment, that process creates a set of one or more disk container files that act as snapshots of your VM’s environment, settings, and data. The Amazon EC2 API ImportImage action uses those files to import your VM and create an AMI. To import using the CLI command, see import-image  You can reference the task ID from the VM import to pull in the AMI that the import created as the base image for your Image Builder recipe. |

### ListComponentBuildVersions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListComponentBuildVersions | Returns the list of component build versions for the specified semantic version.  The semantic version has four nodes: &lt;major&gt;.&lt;minor&gt;.&lt;patch&gt;/&lt;build&gt;. You can assign values for the first three, and can filter on all of them.  Filtering: With semantic versioning, you have the flexibility to use wildcards (x) to specify the most recent versions or nodes when selecting the base image or components for your recipe. When you use a wildcard in any node, all nodes to the right of the first wildcard must also be wildcards. |

### ListComponents
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListComponents | Returns the list of components that can be filtered by name, or by using the listed filters to streamline results. Newly created components can take up to two minutes to appear in the ListComponents API Results.  The semantic version has four nodes: &lt;major&gt;.&lt;minor&gt;.&lt;patch&gt;/&lt;build&gt;. You can assign values for the first three, and can filter on all of them.  Filtering: With semantic versioning, you have the flexibility to use wildcards (x) to specify the most recent versions or nodes when selecting the base image or components for your recipe. When you use a wildcard in any node, all nodes to the right of the first wildcard must also be wildcards. |

### ListContainerRecipes
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListContainerRecipes | Returns a list of container recipes. |

### ListDistributionConfigurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListDistributionConfigurations | Returns a list of distribution configurations. |

### ListImageBuildVersions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImageBuildVersions | Returns a list of image build versions. |

### ListImagePackages
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImagePackages | List the Packages that are associated with an Image Build Version, as determined by Amazon Web Services Systems Manager Inventory at build time. |

### ListImagePipelineImages
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImagePipelineImages | Returns a list of images created by the specified pipeline. |

### ListImagePipelines
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImagePipelines | Returns a list of image pipelines. |

### ListImageRecipes
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImageRecipes | Returns a list of image recipes. |

### ListImageScanFindingAggregations
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImageScanFindingAggregations | Returns a list of image scan aggregations for your account. You can filter by the type of key that Image Builder uses to group results. For example, if you want to get a list of findings by severity level for one of your pipelines, you might specify your pipeline with the imagePipelineArn filter. If you don't specify a filter, Image Builder returns an aggregation for your account. To streamline results, you can use the following filters in your request:    accountId     imageBuildVersionArn     imagePipelineArn     vulnerabilityId |

### ListImageScanFindings
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImageScanFindings | Returns a list of image scan findings for your account. |

### ListImages
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListImages | Returns the list of images that you have access to. Newly created images can take up to two minutes to appear in the ListImages API Results. |

### ListInfrastructureConfigurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListInfrastructureConfigurations | Returns a list of infrastructure configurations. |

### ListLifecycleExecutionResources
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListLifecycleExecutionResources | List resources that the runtime instance of the image lifecycle identified for lifecycle actions. |

### ListLifecycleExecutions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListLifecycleExecutions | Get the lifecycle runtime history for the specified resource. |

### ListLifecyclePolicies
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListLifecyclePolicies | Get a list of lifecycle policies in your Amazon Web Services account. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns the list of tags for the specified resource. |
| POST | /tags/{resourceArn} | Adds a tag to a resource. |
| DELETE | /tags/{resourceArn} | Removes a tag from a resource. |

### ListWaitingWorkflowSteps
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListWaitingWorkflowSteps | Get a list of workflow steps that are waiting for action for workflows in your Amazon Web Services account. |

### ListWorkflowBuildVersions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListWorkflowBuildVersions | Returns a list of build versions for a specific workflow resource. |

### ListWorkflowExecutions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListWorkflowExecutions | Returns a list of workflow runtime instance metadata objects for a specific image build version. |

### ListWorkflowStepExecutions
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListWorkflowStepExecutions | Returns runtime data for each step in a runtime instance of the workflow that you specify in the request. |

### ListWorkflows
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListWorkflows | Lists workflow build versions based on filtering parameters. |

### PutComponentPolicy
| Method | Path | Description |
|--------|------|-------------|
| PUT | /PutComponentPolicy | Applies a policy to a component. We recommend that you call the RAM API CreateResourceShare to share resources. If you call the Image Builder API PutComponentPolicy, you must also call the RAM API PromoteResourceShareCreatedFromPolicy in order for the resource to be visible to all principals with whom the resource is shared. |

### PutContainerRecipePolicy
| Method | Path | Description |
|--------|------|-------------|
| PUT | /PutContainerRecipePolicy | Applies a policy to a container image. We recommend that you call the RAM API CreateResourceShare (https://docs.aws.amazon.com//ram/latest/APIReference/API_CreateResourceShare.html) to share resources. If you call the Image Builder API PutContainerImagePolicy, you must also call the RAM API PromoteResourceShareCreatedFromPolicy (https://docs.aws.amazon.com//ram/latest/APIReference/API_PromoteResourceShareCreatedFromPolicy.html) in order for the resource to be visible to all principals with whom the resource is shared. |

### PutImagePolicy
| Method | Path | Description |
|--------|------|-------------|
| PUT | /PutImagePolicy | Applies a policy to an image. We recommend that you call the RAM API CreateResourceShare to share resources. If you call the Image Builder API PutImagePolicy, you must also call the RAM API PromoteResourceShareCreatedFromPolicy in order for the resource to be visible to all principals with whom the resource is shared. |

### PutImageRecipePolicy
| Method | Path | Description |
|--------|------|-------------|
| PUT | /PutImageRecipePolicy | Applies a policy to an image recipe. We recommend that you call the RAM API CreateResourceShare to share resources. If you call the Image Builder API PutImageRecipePolicy, you must also call the RAM API PromoteResourceShareCreatedFromPolicy in order for the resource to be visible to all principals with whom the resource is shared. |

### SendWorkflowStepAction
| Method | Path | Description |
|--------|------|-------------|
| PUT | /SendWorkflowStepAction | Pauses or resumes image creation when the associated workflow runs a WaitForAction step. |

### StartImagePipelineExecution
| Method | Path | Description |
|--------|------|-------------|
| PUT | /StartImagePipelineExecution | Manually triggers a pipeline to create an image. |

### StartResourceStateUpdate
| Method | Path | Description |
|--------|------|-------------|
| PUT | /StartResourceStateUpdate | Begin asynchronous resource state update for lifecycle changes to the specified image resources. |

### UpdateDistributionConfiguration
| Method | Path | Description |
|--------|------|-------------|
| PUT | /UpdateDistributionConfiguration | Updates a new distribution configuration. Distribution configurations define and configure the outputs of your pipeline. |

### UpdateImagePipeline
| Method | Path | Description |
|--------|------|-------------|
| PUT | /UpdateImagePipeline | Updates an image pipeline. Image pipelines enable you to automate the creation and distribution of images. You must specify exactly one recipe for your image, using either a containerRecipeArn or an imageRecipeArn.  UpdateImagePipeline does not support selective updates for the pipeline. You must specify all of the required properties in the update request, not just the properties that have changed. |

### UpdateInfrastructureConfiguration
| Method | Path | Description |
|--------|------|-------------|
| PUT | /UpdateInfrastructureConfiguration | Updates a new infrastructure configuration. An infrastructure configuration defines the environment in which your image will be built and tested. |

### UpdateLifecyclePolicy
| Method | Path | Description |
|--------|------|-------------|
| PUT | /UpdateLifecyclePolicy | Update the specified lifecycle policy. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all GetComponent?" -> GET /GetComponent
- "List all GetComponentPolicy?" -> GET /GetComponentPolicy
- "List all GetContainerRecipe?" -> GET /GetContainerRecipe
- "List all GetContainerRecipePolicy?" -> GET /GetContainerRecipePolicy
- "List all GetDistributionConfiguration?" -> GET /GetDistributionConfiguration
- "List all GetImage?" -> GET /GetImage
- "List all GetImagePipeline?" -> GET /GetImagePipeline
- "List all GetImagePolicy?" -> GET /GetImagePolicy
- "List all GetImageRecipe?" -> GET /GetImageRecipe
- "List all GetImageRecipePolicy?" -> GET /GetImageRecipePolicy
- "List all GetInfrastructureConfiguration?" -> GET /GetInfrastructureConfiguration
- "List all GetLifecycleExecution?" -> GET /GetLifecycleExecution
- "List all GetLifecyclePolicy?" -> GET /GetLifecyclePolicy
- "List all GetWorkflow?" -> GET /GetWorkflow
- "List all GetWorkflowExecution?" -> GET /GetWorkflowExecution
- "List all GetWorkflowStepExecution?" -> GET /GetWorkflowStepExecution
- "Create a ListComponentBuildVersion?" -> POST /ListComponentBuildVersions
- "Create a ListComponent?" -> POST /ListComponents
- "Create a ListContainerRecipe?" -> POST /ListContainerRecipes
- "Create a ListDistributionConfiguration?" -> POST /ListDistributionConfigurations
- "Create a ListImageBuildVersion?" -> POST /ListImageBuildVersions
- "Create a ListImagePackage?" -> POST /ListImagePackages
- "Create a ListImagePipelineImage?" -> POST /ListImagePipelineImages
- "Create a ListImagePipeline?" -> POST /ListImagePipelines
- "Create a ListImageRecipe?" -> POST /ListImageRecipes
- "Create a ListImageScanFindingAggregation?" -> POST /ListImageScanFindingAggregations
- "Create a ListImageScanFinding?" -> POST /ListImageScanFindings
- "Create a ListImage?" -> POST /ListImages
- "Create a ListInfrastructureConfiguration?" -> POST /ListInfrastructureConfigurations
- "Create a ListLifecycleExecutionResource?" -> POST /ListLifecycleExecutionResources
- "Create a ListLifecycleExecution?" -> POST /ListLifecycleExecutions
- "Create a ListLifecyclePolicy?" -> POST /ListLifecyclePolicies
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a ListWaitingWorkflowStep?" -> POST /ListWaitingWorkflowSteps
- "Create a ListWorkflowBuildVersion?" -> POST /ListWorkflowBuildVersions
- "Create a ListWorkflowExecution?" -> POST /ListWorkflowExecutions
- "Create a ListWorkflowStepExecution?" -> POST /ListWorkflowStepExecutions
- "Create a ListWorkflow?" -> POST /ListWorkflows
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
