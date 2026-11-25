---
name: aws-codedeploy
description: "AWS CodeDeploy API skill. Use when working with AWS CodeDeploy for root. Covers 47 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS CodeDeploy
API version: 2014-10-06

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
| POST | / | Adds tags to on-premises instances. |
| POST | / | Gets information about one or more application revisions. The maximum number of application revisions that can be returned is 25. |
| POST | / | Gets information about one or more applications. The maximum number of applications that can be returned is 100. |
| POST | / | Gets information about one or more deployment groups. |
| POST | / | This method works, but is deprecated. Use BatchGetDeploymentTargets instead.    Returns an array of one or more instances associated with a deployment. This method works with EC2/On-premises and Lambda compute platforms. The newer BatchGetDeploymentTargets works with all compute platforms. The maximum number of instances that can be returned is 25. |
| POST | / | Returns an array of one or more targets associated with a deployment. This method works with all compute types and should be used instead of the deprecated BatchGetDeploymentInstances. The maximum number of targets that can be returned is 25.  The type of targets returned depends on the deployment's compute platform or deployment method:     EC2/On-premises: Information about Amazon EC2 instance targets.     Lambda: Information about Lambda functions targets.     Amazon ECS: Information about Amazon ECS service targets.     CloudFormation: Information about targets of blue/green deployments initiated by a CloudFormation stack update. |
| POST | / | Gets information about one or more deployments. The maximum number of deployments that can be returned is 25. |
| POST | / | Gets information about one or more on-premises instances. The maximum number of on-premises instances that can be returned is 25. |
| POST | / | For a blue/green deployment, starts the process of rerouting traffic from instances in the original environment to instances in the replacement environment without waiting for a specified wait time to elapse. (Traffic rerouting, which is achieved by registering instances in the replacement environment with the load balancer, can start as soon as all instances have a status of Ready.) |
| POST | / | Creates an application. |
| POST | / | Deploys an application revision through the specified deployment group. |
| POST | / | Creates a deployment configuration. |
| POST | / | Creates a deployment group to which application revisions are deployed. |
| POST | / | Deletes an application. |
| POST | / | Deletes a deployment configuration.  A deployment configuration cannot be deleted if it is currently in use. Predefined configurations cannot be deleted. |
| POST | / | Deletes a deployment group. |
| POST | / | Deletes a GitHub account connection. |
| POST | / | Deletes resources linked to an external ID. This action only applies if you have configured blue/green deployments through CloudFormation.   It is not necessary to call this action directly. CloudFormation calls it on your behalf when it needs to delete stack resources. This action is offered publicly in case you need to delete resources to comply with General Data Protection Regulation (GDPR) requirements. |
| POST | / | Deregisters an on-premises instance. |
| POST | / | Gets information about an application. |
| POST | / | Gets information about an application revision. |
| POST | / | Gets information about a deployment.   The content property of the appSpecContent object in the returned revision is always null. Use GetApplicationRevision and the sha256 property of the returned appSpecContent object to get the content of the deployment’s AppSpec file. |
| POST | / | Gets information about a deployment configuration. |
| POST | / | Gets information about a deployment group. |
| POST | / | Gets information about an instance as part of a deployment. |
| POST | / | Returns information about a deployment target. |
| POST | / | Gets information about an on-premises instance. |
| POST | / | Lists information about revisions for an application. |
| POST | / | Lists the applications registered with the user or Amazon Web Services account. |
| POST | / | Lists the deployment configurations with the user or Amazon Web Services account. |
| POST | / | Lists the deployment groups for an application registered with the Amazon Web Services user or Amazon Web Services account. |
| POST | / | The newer BatchGetDeploymentTargets should be used instead because it works with all compute types. ListDeploymentInstances throws an exception if it is used with a compute platform other than EC2/On-premises or Lambda.    Lists the instance for a deployment associated with the user or Amazon Web Services account. |
| POST | / | Returns an array of target IDs that are associated a deployment. |
| POST | / | Lists the deployments in a deployment group for an application registered with the user or Amazon Web Services account. |
| POST | / | Lists the names of stored connections to GitHub accounts. |
| POST | / | Gets a list of names for one or more on-premises instances. Unless otherwise specified, both registered and deregistered on-premises instance names are listed. To list only registered or deregistered on-premises instance names, use the registration status parameter. |
| POST | / | Returns a list of tags for the resource identified by a specified Amazon Resource Name (ARN). Tags are used to organize and categorize your CodeDeploy resources. |
| POST | / | Sets the result of a Lambda validation function. The function validates lifecycle hooks during a deployment that uses the Lambda or Amazon ECS compute platform. For Lambda deployments, the available lifecycle hooks are BeforeAllowTraffic and AfterAllowTraffic. For Amazon ECS deployments, the available lifecycle hooks are BeforeInstall, AfterInstall, AfterAllowTestTraffic, BeforeAllowTraffic, and AfterAllowTraffic. Lambda validation functions return Succeeded or Failed. For more information, see AppSpec 'hooks' Section for an Lambda Deployment  and AppSpec 'hooks' Section for an Amazon ECS Deployment. |
| POST | / | Registers with CodeDeploy a revision for the specified application. |
| POST | / | Registers an on-premises instance.  Only one IAM ARN (an IAM session ARN or IAM user ARN) is supported in the request. You cannot use both. |
| POST | / | Removes one or more tags from one or more on-premises instances. |
| POST | / | In a blue/green deployment, overrides any specified wait time and starts terminating instances immediately after the traffic routing is complete. |
| POST | / | Attempts to stop an ongoing deployment. |
| POST | / | Associates the list of tags in the input Tags parameter with the resource identified by the ResourceArn input parameter. |
| POST | / | Disassociates a resource from a list of tags. The resource is identified by the ResourceArn input parameter. The tags are identified by the list of keys in the TagKeys input parameter. |
| POST | / | Changes the name of an application. |
| POST | / | Changes information about a deployment group. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
