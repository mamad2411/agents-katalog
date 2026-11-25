---
name: aws-cloud-map
description: "AWS Cloud Map API skill. Use when working with AWS Cloud Map for root. Covers 27 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Cloud Map
API version: 2017-03-14

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
| POST | / | Creates an HTTP namespace. Service instances registered using an HTTP namespace can be discovered using a DiscoverInstances request but can't be discovered using DNS. For the current quota on the number of namespaces that you can create using the same Amazon Web Services account, see Cloud Map quotas in the Cloud Map Developer Guide. |
| POST | / | Creates a private namespace based on DNS, which is visible only inside a specified Amazon VPC. The namespace defines your service naming scheme. For example, if you name your namespace example.com and name your service backend, the resulting DNS name for the service is backend.example.com. Service instances that are registered using a private DNS namespace can be discovered using either a DiscoverInstances request or using DNS. For the current quota on the number of namespaces that you can create using the same Amazon Web Services account, see Cloud Map quotas in the Cloud Map Developer Guide. |
| POST | / | Creates a public namespace based on DNS, which is visible on the internet. The namespace defines your service naming scheme. For example, if you name your namespace example.com and name your service backend, the resulting DNS name for the service is backend.example.com. You can discover instances that were registered with a public DNS namespace by using either a DiscoverInstances request or using DNS. For the current quota on the number of namespaces that you can create using the same Amazon Web Services account, see Cloud Map quotas in the Cloud Map Developer Guide.  The CreatePublicDnsNamespace API operation is not supported in the Amazon Web Services GovCloud (US) Regions. |
| POST | / | Creates a service. This action defines the configuration for the following entities:   For public and private DNS namespaces, one of the following combinations of DNS records in Amazon Route 53:    A     AAAA     A and AAAA     SRV     CNAME      Optionally, a health check   After you create the service, you can submit a RegisterInstance request, and Cloud Map uses the values in the configuration to create the specified entities. For the current quota on the number of instances that you can register using the same namespace and using the same service, see Cloud Map quotas in the Cloud Map Developer Guide. |
| POST | / | Deletes a namespace from the current account. If the namespace still contains one or more services, the request fails. |
| POST | / | Deletes a specified service. If the service still contains one or more registered instances, the request fails. |
| POST | / | Deletes the Amazon Route 53 DNS records and health check, if any, that Cloud Map created for the specified instance. |
| POST | / | Discovers registered instances for a specified namespace and service. You can use DiscoverInstances to discover instances for any type of namespace. DiscoverInstances returns a randomized list of instances allowing customers to distribute traffic evenly across instances. For public and private DNS namespaces, you can also use DNS queries to discover instances. |
| POST | / | Discovers the increasing revision associated with an instance. |
| POST | / | Gets information about a specified instance. |
| POST | / | Gets the current health status (Healthy, Unhealthy, or Unknown) of one or more instances that are associated with a specified service.  There's a brief delay between when you register an instance and when the health status for the instance is available. |
| POST | / | Gets information about a namespace. |
| POST | / | Gets information about any operation that returns an operation ID in the response, such as a CreateHttpNamespace request.  To get a list of operations that match specified criteria, see ListOperations. |
| POST | / | Gets the settings for a specified service. |
| POST | / | Lists summary information about the instances that you registered by using a specified service. |
| POST | / | Lists summary information about the namespaces that were created by the current Amazon Web Services account. |
| POST | / | Lists operations that match the criteria that you specify. |
| POST | / | Lists summary information for all the services that are associated with one or more namespaces. |
| POST | / | Lists tags for the specified resource. |
| POST | / | Creates or updates one or more records and, optionally, creates a health check based on the settings in a specified service. When you submit a RegisterInstance request, the following occurs:   For each DNS record that you define in the service that's specified by ServiceId, a record is created or updated in the hosted zone that's associated with the corresponding namespace.   If the service includes HealthCheckConfig, a health check is created based on the settings in the health check configuration.   The health check, if any, is associated with each of the new or updated records.    One RegisterInstance request must complete before you can submit another request and specify the same service ID and instance ID.  For more information, see CreateService. When Cloud Map receives a DNS query for the specified DNS name, it returns the applicable value:    If the health check is healthy: returns all the records    If the health check is unhealthy: returns the applicable value for the last healthy instance    If you didn't specify a health check configuration: returns all the records   For the current quota on the number of instances that you can register using the same namespace and using the same service, see Cloud Map quotas in the Cloud Map Developer Guide. |
| POST | / | Adds one or more tags to the specified resource. |
| POST | / | Removes one or more tags from the specified resource. |
| POST | / | Updates an HTTP namespace. |
| POST | / | Submits a request to change the health status of a custom health check to healthy or unhealthy. You can use UpdateInstanceCustomHealthStatus to change the status only for custom health checks, which you define using HealthCheckCustomConfig when you create a service. You can't use it to change the status for Route 53 health checks, which you define using HealthCheckConfig. For more information, see HealthCheckCustomConfig. |
| POST | / | Updates a private DNS namespace. |
| POST | / | Updates a public DNS namespace. |
| POST | / | Submits a request to perform the following operations:   Update the TTL setting for existing DnsRecords configurations   Add, update, or delete HealthCheckConfig for a specified service  You can't add, update, or delete a HealthCheckCustomConfig configuration.    For public and private DNS namespaces, note the following:   If you omit any existing DnsRecords or HealthCheckConfig configurations from an UpdateService request, the configurations are deleted from the service.   If you omit an existing HealthCheckCustomConfig configuration from an UpdateService request, the configuration isn't deleted from the service.   When you update settings for a service, Cloud Map also updates the corresponding settings in all the records and health checks that were created by using the specified service. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
