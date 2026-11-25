---
name: aws-app-runner
description: "AWS App Runner API skill. Use when working with AWS App Runner for root. Covers 37 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS App Runner
API version: 2020-05-15

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

37 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Associate your own domain name with the App Runner subdomain URL of your App Runner service. After you call AssociateCustomDomain and receive a successful response, use the information in the CustomDomain record that's returned to add CNAME records to your Domain Name System (DNS). For each mapped domain name, add a mapping to the target App Runner subdomain and one or more certificate validation records. App Runner then performs DNS validation to verify that you own or control the domain name that you associated. App Runner tracks domain validity in a certificate stored in AWS Certificate Manager (ACM). |
| POST | / | Create an App Runner automatic scaling configuration resource. App Runner requires this resource when you create or update App Runner services and you require non-default auto scaling settings. You can share an auto scaling configuration across multiple services. Create multiple revisions of a configuration by calling this action multiple times using the same AutoScalingConfigurationName. The call returns incremental AutoScalingConfigurationRevision values. When you create a service and configure an auto scaling configuration resource, the service uses the latest active revision of the auto scaling configuration by default. You can optionally configure the service to use a specific revision. Configure a higher MinSize to increase the spread of your App Runner service over more Availability Zones in the Amazon Web Services Region. The tradeoff is a higher minimal cost. Configure a lower MaxSize to control your cost. The tradeoff is lower responsiveness during peak demand. |
| POST | / | Create an App Runner connection resource. App Runner requires a connection resource when you create App Runner services that access private repositories from certain third-party providers. You can share a connection across multiple services. A connection resource is needed to access GitHub and Bitbucket repositories. Both require a user interface approval process through the App Runner console before you can use the connection. |
| POST | / | Create an App Runner observability configuration resource. App Runner requires this resource when you create or update App Runner services and you want to enable non-default observability features. You can share an observability configuration across multiple services. Create multiple revisions of a configuration by calling this action multiple times using the same ObservabilityConfigurationName. The call returns incremental ObservabilityConfigurationRevision values. When you create a service and configure an observability configuration resource, the service uses the latest active revision of the observability configuration by default. You can optionally configure the service to use a specific revision. The observability configuration resource is designed to configure multiple features (currently one feature, tracing). This action takes optional parameters that describe the configuration of these features (currently one parameter, TraceConfiguration). If you don't specify a feature parameter, App Runner doesn't enable the feature. |
| POST | / | Create an App Runner service. After the service is created, the action also automatically starts a deployment. This is an asynchronous operation. On a successful call, you can use the returned OperationId and the ListOperations call to track the operation's progress. |
| POST | / | Create an App Runner VPC connector resource. App Runner requires this resource when you want to associate your App Runner service to a custom Amazon Virtual Private Cloud (Amazon VPC). |
| POST | / | Create an App Runner VPC Ingress Connection resource. App Runner requires this resource when you want to associate your App Runner service with an Amazon VPC endpoint. |
| POST | / | Delete an App Runner automatic scaling configuration resource. You can delete a top level auto scaling configuration, a specific revision of one, or all revisions associated with the top level configuration. You can't delete the default auto scaling configuration or a configuration that's used by one or more App Runner services. |
| POST | / | Delete an App Runner connection. You must first ensure that there are no running App Runner services that use this connection. If there are any, the DeleteConnection action fails. |
| POST | / | Delete an App Runner observability configuration resource. You can delete a specific revision or the latest active revision. You can't delete a configuration that's used by one or more App Runner services. |
| POST | / | Delete an App Runner service. This is an asynchronous operation. On a successful call, you can use the returned OperationId and the ListOperations call to track the operation's progress.  Make sure that you don't have any active VPCIngressConnections associated with the service you want to delete. |
| POST | / | Delete an App Runner VPC connector resource. You can't delete a connector that's used by one or more App Runner services. |
| POST | / | Delete an App Runner VPC Ingress Connection resource that's associated with an App Runner service. The VPC Ingress Connection must be in one of the following states to be deleted:     AVAILABLE     FAILED_CREATION     FAILED_UPDATE     FAILED_DELETION |
| POST | / | Return a full description of an App Runner automatic scaling configuration resource. |
| POST | / | Return a description of custom domain names that are associated with an App Runner service. |
| POST | / | Return a full description of an App Runner observability configuration resource. |
| POST | / | Return a full description of an App Runner service. |
| POST | / | Return a description of an App Runner VPC connector resource. |
| POST | / | Return a full description of an App Runner VPC Ingress Connection resource. |
| POST | / | Disassociate a custom domain name from an App Runner service. Certificates tracking domain validity are associated with a custom domain and are stored in AWS Certificate Manager (ACM). These certificates aren't deleted as part of this action. App Runner delays certificate deletion for 30 days after a domain is disassociated from your service. |
| POST | / | Returns a list of active App Runner automatic scaling configurations in your Amazon Web Services account. You can query the revisions for a specific configuration name or the revisions for all active configurations in your account. You can optionally query only the latest revision of each requested name. To retrieve a full description of a particular configuration revision, call and provide one of the ARNs returned by ListAutoScalingConfigurations. |
| POST | / | Returns a list of App Runner connections that are associated with your Amazon Web Services account. |
| POST | / | Returns a list of active App Runner observability configurations in your Amazon Web Services account. You can query the revisions for a specific configuration name or the revisions for all active configurations in your account. You can optionally query only the latest revision of each requested name. To retrieve a full description of a particular configuration revision, call and provide one of the ARNs returned by ListObservabilityConfigurations. |
| POST | / | Return a list of operations that occurred on an App Runner service. The resulting list of OperationSummary objects is sorted in reverse chronological order. The first object on the list represents the last started operation. |
| POST | / | Returns a list of running App Runner services in your Amazon Web Services account. |
| POST | / | Returns a list of the associated App Runner services using an auto scaling configuration. |
| POST | / | List tags that are associated with for an App Runner resource. The response contains a list of tag key-value pairs. |
| POST | / | Returns a list of App Runner VPC connectors in your Amazon Web Services account. |
| POST | / | Return a list of App Runner VPC Ingress Connections in your Amazon Web Services account. |
| POST | / | Pause an active App Runner service. App Runner reduces compute capacity for the service to zero and loses state (for example, ephemeral storage is removed). This is an asynchronous operation. On a successful call, you can use the returned OperationId and the ListOperations call to track the operation's progress. |
| POST | / | Resume an active App Runner service. App Runner provisions compute capacity for the service. This is an asynchronous operation. On a successful call, you can use the returned OperationId and the ListOperations call to track the operation's progress. |
| POST | / | Initiate a manual deployment of the latest commit in a source code repository or the latest image in a source image repository to an App Runner service. For a source code repository, App Runner retrieves the commit and builds a Docker image. For a source image repository, App Runner retrieves the latest Docker image. In both cases, App Runner then deploys the new image to your service and starts a new container instance. This is an asynchronous operation. On a successful call, you can use the returned OperationId and the ListOperations call to track the operation's progress. |
| POST | / | Add tags to, or update the tag values of, an App Runner resource. A tag is a key-value pair. |
| POST | / | Remove tags from an App Runner resource. |
| POST | / | Update an auto scaling configuration to be the default. The existing default auto scaling configuration will be set to non-default automatically. |
| POST | / | Update an App Runner service. You can update the source configuration and instance configuration of the service. You can also update the ARN of the auto scaling configuration resource that's associated with the service. However, you can't change the name or the encryption configuration of the service. These can be set only when you create the service. To update the tags applied to your service, use the separate actions TagResource and UntagResource. This is an asynchronous operation. On a successful call, you can use the returned OperationId and the ListOperations call to track the operation's progress. |
| POST | / | Update an existing App Runner VPC Ingress Connection resource. The VPC Ingress Connection must be in one of the following states to be updated:    AVAILABLE     FAILED_CREATION     FAILED_UPDATE |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
