---
name: aws-batch
description: "AWS Batch API skill. Use when working with AWS Batch for canceljob, createcomputeenvironment, createjobqueue. Covers 25 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Batch
API version: 2016-08-10

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/tags/{resourceArn} -- verify access
3. POST /v1/canceljob -- create first canceljob

## Endpoints

25 endpoints across 23 groups. See references/api-spec.lap for full details.

### canceljob
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/canceljob | Cancels a job in an Batch job queue. Jobs that are in a SUBMITTED, PENDING, or RUNNABLE state are cancelled and the job status is updated to FAILED.  A PENDING job is canceled after all dependency jobs are completed. Therefore, it may take longer than expected to cancel a job in PENDING status. When you try to cancel an array parent job in PENDING, Batch attempts to cancel all child jobs. The array parent job is canceled when all child jobs are completed.  Jobs that progressed to the STARTING or RUNNING state aren't canceled. However, the API operation still succeeds, even if no job is canceled. These jobs must be terminated with the TerminateJob operation. |

### createcomputeenvironment
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/createcomputeenvironment | Creates an Batch compute environment. You can create MANAGED or UNMANAGED compute environments. MANAGED compute environments can use Amazon EC2 or Fargate resources. UNMANAGED compute environments can only use EC2 resources. In a managed compute environment, Batch manages the capacity and instance types of the compute resources within the environment. This is based on the compute resource specification that you define or the launch template that you specify when you create the compute environment. Either, you can choose to use EC2 On-Demand Instances and EC2 Spot Instances. Or, you can use Fargate and Fargate Spot capacity in your managed compute environment. You can optionally set a maximum price so that Spot Instances only launch when the Spot Instance price is less than a specified percentage of the On-Demand price.  Multi-node parallel jobs aren't supported on Spot Instances.  In an unmanaged compute environment, you can manage your own EC2 compute resources and have flexibility with how you configure your compute resources. For example, you can use custom AMIs. However, you must verify that each of your AMIs meet the Amazon ECS container instance AMI specification. For more information, see container instance AMIs in the Amazon Elastic Container Service Developer Guide. After you created your unmanaged compute environment, you can use the DescribeComputeEnvironments operation to find the Amazon ECS cluster that's associated with it. Then, launch your container instances into that Amazon ECS cluster. For more information, see Launching an Amazon ECS container instance in the Amazon Elastic Container Service Developer Guide.  To create a compute environment that uses EKS resources, the caller must have permissions to call eks:DescribeCluster.   Batch doesn't automatically upgrade the AMIs in a compute environment after it's created. For example, it also doesn't update the AMIs in your compute environment when a newer version of the Amazon ECS optimized AMI is available. You're responsible for the management of the guest operating system. This includes any updates and security patches. You're also responsible for any additional application software or utilities that you install on the compute resources. There are two ways to use a new AMI for your Batch jobs. The original method is to complete these steps:   Create a new compute environment with the new AMI.   Add the compute environment to an existing job queue.   Remove the earlier compute environment from your job queue.   Delete the earlier compute environment.   In April 2022, Batch added enhanced support for updating compute environments. For more information, see Updating compute environments. To use the enhanced updating of compute environments to update AMIs, follow these rules:   Either don't set the service role (serviceRole) parameter or set it to the AWSBatchServiceRole service-linked role.   Set the allocation strategy (allocationStrategy) parameter to BEST_FIT_PROGRESSIVE, SPOT_CAPACITY_OPTIMIZED, or SPOT_PRICE_CAPACITY_OPTIMIZED.   Set the update to latest image version (updateToLatestImageVersion) parameter to true. The updateToLatestImageVersion parameter is used when you update a compute environment. This parameter is ignored when you create a compute environment.   Don't specify an AMI ID in imageId, imageIdOverride (in  ec2Configuration ), or in the launch template (launchTemplate). In that case, Batch selects the latest Amazon ECS optimized AMI that's supported by Batch at the time the infrastructure update is initiated. Alternatively, you can specify the AMI ID in the imageId or imageIdOverride parameters, or the launch template identified by the LaunchTemplate properties. Changing any of these properties starts an infrastructure update. If the AMI ID is specified in the launch template, it can't be replaced by specifying an AMI ID in either the imageId or imageIdOverride parameters. It can only be replaced by specifying a different launch template, or if the launch template version is set to $Default or $Latest, by setting either a new default version for the launch template (if $Default) or by adding a new version to the launch template (if $Latest).   If these rules are followed, any update that starts an infrastructure update causes the AMI ID to be re-selected. If the version setting in the launch template (launchTemplate) is set to $Latest or $Default, the latest or default version of the launch template is evaluated up at the time of the infrastructure update, even if the launchTemplate wasn't updated. |

### createjobqueue
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/createjobqueue | Creates an Batch job queue. When you create a job queue, you associate one or more compute environments to the queue and assign an order of preference for the compute environments. You also set a priority to the job queue that determines the order that the Batch scheduler places jobs onto its associated compute environments. For example, if a compute environment is associated with more than one job queue, the job queue with a higher priority is given preference for scheduling jobs to that compute environment. |

### createschedulingpolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/createschedulingpolicy | Creates an Batch scheduling policy. |

### deletecomputeenvironment
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/deletecomputeenvironment | Deletes an Batch compute environment. Before you can delete a compute environment, you must set its state to DISABLED with the UpdateComputeEnvironment API operation and disassociate it from any job queues with the UpdateJobQueue API operation. Compute environments that use Fargate resources must terminate all active jobs on that compute environment before deleting the compute environment. If this isn't done, the compute environment enters an invalid state. |

### deletejobqueue
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/deletejobqueue | Deletes the specified job queue. You must first disable submissions for a queue with the UpdateJobQueue operation. All jobs in the queue are eventually terminated when you delete a job queue. The jobs are terminated at a rate of about 16 jobs each second. It's not necessary to disassociate compute environments from a queue before submitting a DeleteJobQueue request. |

### deleteschedulingpolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/deleteschedulingpolicy | Deletes the specified scheduling policy. You can't delete a scheduling policy that's used in any job queues. |

### deregisterjobdefinition
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/deregisterjobdefinition | Deregisters an Batch job definition. Job definitions are permanently deleted after 180 days. |

### describecomputeenvironments
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/describecomputeenvironments | Describes one or more of your compute environments. If you're using an unmanaged compute environment, you can use the DescribeComputeEnvironment operation to determine the ecsClusterArn that you launch your Amazon ECS container instances into. |

### describejobdefinitions
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/describejobdefinitions | Describes a list of job definitions. You can specify a status (such as ACTIVE) to only return job definitions that match that status. |

### describejobqueues
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/describejobqueues | Describes one or more of your job queues. |

### describejobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/describejobs | Describes a list of Batch jobs. |

### describeschedulingpolicies
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/describeschedulingpolicies | Describes one or more of your scheduling policies. |

### getjobqueuesnapshot
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/getjobqueuesnapshot | Provides a list of the first 100 RUNNABLE jobs associated to a single job queue. |

### listjobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/listjobs | Returns a list of Batch jobs. You must specify only one of the following items:   A job queue ID to return a list of jobs in that job queue   A multi-node parallel job ID to return a list of nodes for that job   An array job ID to return a list of the children for that job   You can filter the results by job status with the jobStatus parameter. If you don't specify a status, only RUNNING jobs are returned. |

### listschedulingpolicies
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/listschedulingpolicies | Returns a list of Batch scheduling policies. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/tags/{resourceArn} | Lists the tags for an Batch resource. Batch resources that support tags are compute environments, jobs, job definitions, job queues, and scheduling policies. ARNs for child jobs of array and multi-node parallel (MNP) jobs aren't supported. |
| POST | /v1/tags/{resourceArn} | Associates the specified tags to a resource with the specified resourceArn. If existing tags on a resource aren't specified in the request parameters, they aren't changed. When a resource is deleted, the tags that are associated with that resource are deleted as well. Batch resources that support tags are compute environments, jobs, job definitions, job queues, and scheduling policies. ARNs for child jobs of array and multi-node parallel (MNP) jobs aren't supported. |
| DELETE | /v1/tags/{resourceArn} | Deletes specified tags from an Batch resource. |

### registerjobdefinition
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/registerjobdefinition | Registers an Batch job definition. |

### submitjob
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/submitjob | Submits an Batch job from a job definition. Parameters that are specified during SubmitJob override parameters defined in the job definition. vCPU and memory requirements that are specified in the resourceRequirements objects in the job definition are the exception. They can't be overridden this way using the memory and vcpus parameters. Rather, you must specify updates to job definition parameters in a resourceRequirements object that's included in the containerOverrides parameter.  Job queues with a scheduling policy are limited to 500 active fair share identifiers at a time.    Jobs that run on Fargate resources can't be guaranteed to run for more than 14 days. This is because, after 14 days, Fargate resources might become unavailable and job might be terminated. |

### terminatejob
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/terminatejob | Terminates a job in a job queue. Jobs that are in the STARTING or RUNNING state are terminated, which causes them to transition to FAILED. Jobs that have not progressed to the STARTING state are cancelled. |

### updatecomputeenvironment
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/updatecomputeenvironment | Updates an Batch compute environment. |

### updatejobqueue
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/updatejobqueue | Updates a job queue. |

### updateschedulingpolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/updateschedulingpolicy | Updates a scheduling policy. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a canceljob?" -> POST /v1/canceljob
- "Create a createcomputeenvironment?" -> POST /v1/createcomputeenvironment
- "Create a createjobqueue?" -> POST /v1/createjobqueue
- "Create a createschedulingpolicy?" -> POST /v1/createschedulingpolicy
- "Create a deletecomputeenvironment?" -> POST /v1/deletecomputeenvironment
- "Create a deletejobqueue?" -> POST /v1/deletejobqueue
- "Create a deleteschedulingpolicy?" -> POST /v1/deleteschedulingpolicy
- "Create a deregisterjobdefinition?" -> POST /v1/deregisterjobdefinition
- "Create a describecomputeenvironment?" -> POST /v1/describecomputeenvironments
- "Create a describejobdefinition?" -> POST /v1/describejobdefinitions
- "Create a describejobqueue?" -> POST /v1/describejobqueues
- "Create a describejob?" -> POST /v1/describejobs
- "Create a describeschedulingpolicy?" -> POST /v1/describeschedulingpolicies
- "Create a getjobqueuesnapshot?" -> POST /v1/getjobqueuesnapshot
- "Create a listjob?" -> POST /v1/listjobs
- "Create a listschedulingpolicy?" -> POST /v1/listschedulingpolicies
- "Get tag details?" -> GET /v1/tags/{resourceArn}
- "Create a registerjobdefinition?" -> POST /v1/registerjobdefinition
- "Create a submitjob?" -> POST /v1/submitjob
- "Create a terminatejob?" -> POST /v1/terminatejob
- "Delete a tag?" -> DELETE /v1/tags/{resourceArn}
- "Create a updatecomputeenvironment?" -> POST /v1/updatecomputeenvironment
- "Create a updatejobqueue?" -> POST /v1/updatejobqueue
- "Create a updateschedulingpolicy?" -> POST /v1/updateschedulingpolicy
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
