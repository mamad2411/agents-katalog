---
name: adhybridhealthservice
description: "ADHybridHealthService API skill. Use when working with ADHybridHealthService for providers. Covers 77 endpoints."
version: 1.0.0
generator: lapsh
---

# ADHybridHealthService
API version: 2014-01-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ADHybridHealthService/addsservices -- verify access
3. POST /providers/Microsoft.ADHybridHealthService/addsservices -- create first addsservices

## Endpoints

77 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ADHybridHealthService/addsservices | Gets the details of Active Directory Domain Service, for a tenant, that are onboarded to Azure Active Directory Connect Health. |
| POST | /providers/Microsoft.ADHybridHealthService/addsservices | Onboards a service for a given tenant in Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName} | Gets the details of an Active Directory Domain Service for a tenant having Azure AD Premium license and is onboarded to Azure Active Directory Connect Health. |
| DELETE | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName} | Deletes an Active Directory Domain Service which is onboarded to Azure Active Directory Connect Health. |
| PATCH | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName} | Updates an Active Directory Domain Service properties of an onboarded service. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/alerts | Gets the alerts for a given Active Directory Domain Service. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/configuration | Gets the service configurations. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/dimensions/{dimension} | Gets the dimensions for a given dimension type in a server. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/addsservicemembers | Gets the details of the Active Directory Domain servers, for a given Active Directory Domain Service, that are onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/addomainservicemembers | Gets the details of the servers, for a given Active Directory Domain Service, that are onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/features/{featureName}/userpreference | Gets the user preferences for a given feature. |
| DELETE | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/features/{featureName}/userpreference | Deletes the user preferences for a given feature. |
| POST | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/features/{featureName}/userpreference | Adds the user preferences for a given feature. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/forestsummary | Gets the forest summary for a given Active Directory Domain Service, that is onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metrics/{metricName}/groups/{groupName} | Gets the server related metrics for a given metric and group combination. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metrics/{metricName}/groups/{groupName}/average | Gets the average of the metric values for a given metric and group combination. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metrics/{metricName}/groups/{groupName}/sum | Gets the sum of the metric values for a given metric and group combination. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metricmetadata | Gets the service related metrics information. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metricmetadata/{metricName} | Gets the service related metric information. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metricmetadata/{metricName}/groups/{groupName} | Gets the service related metrics for a given metric and group combination. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/replicationdetails | Gets complete domain controller list along with replication details for a given Active Directory Domain Service, that is onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/replicationstatus | Gets Replication status for a given Active Directory Domain Service, that is onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/replicationsummary | Gets complete domain controller list along with replication details for a given Active Directory Domain Service, that is onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers | Gets the details of the servers, for a given Active Directory Domain Controller service, that are onboarded to Azure Active Directory Connect Health Service. |
| POST | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers | Onboards  a server, for a given Active Directory Domain Controller service, to Azure Active Directory Connect Health Service. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers/{serviceMemberId} | Gets the details of a server, for a given Active Directory Domain Controller service, that are onboarded to Azure Active Directory Connect Health Service. |
| DELETE | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers/{serviceMemberId} | Deletes a Active Directory Domain Controller server that has been onboarded to Azure Active Directory Connect Health Service. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers/{serviceMemberId}/alerts | Gets the details of an alert for a given Active Directory Domain Controller service and server combination. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers/{serviceMemberId}/credentials | Gets the credentials of the server which is needed by the agent to connect to Azure Active Directory Connect Health Service. |
| GET | /providers/Microsoft.ADHybridHealthService/addsservices/premiumCheck | Gets the details of Active Directory Domain Services for a tenant having Azure AD Premium license and is onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/operations | Lists the available Azure Data Factory API operations. |
| POST | /providers/Microsoft.ADHybridHealthService/configuration | Onboards a tenant in Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/configuration | Gets the details of a tenant onboarded to Azure Active Directory Connect Health. |
| PATCH | /providers/Microsoft.ADHybridHealthService/configuration | Updates tenant properties for tenants onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/reports/DevOps/IsDevOps | Checks if the user is enabled for Dev Ops access. |
| GET | /providers/Microsoft.ADHybridHealthService/services | Gets the details of services, for a tenant, that are onboarded to Azure Active Directory Connect Health. |
| POST | /providers/Microsoft.ADHybridHealthService/services | Onboards a service for a given tenant in Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/services/premiumCheck | Gets the details of services for a tenant having Azure AD Premium license and is onboarded to Azure Active Directory Connect Health. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName} | Gets the details of a service for a tenant having Azure AD Premium license and is onboarded to Azure Active Directory Connect Health. |
| DELETE | /providers/Microsoft.ADHybridHealthService/services/{serviceName} | Deletes a service which is onboarded to Azure Active Directory Connect Health. |
| PATCH | /providers/Microsoft.ADHybridHealthService/services/{serviceName} | Updates the service properties of an onboarded service. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/alerts | Gets the alerts for a given service. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/checkServiceFeatureAvailibility/{featureName} | Checks if the service has all the pre-requisites met to use a feature. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/exporterrors/counts | Gets the count of latest AAD export errors. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/exporterrors/listV2 | Gets the categorized export errors. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/exportstatus | Gets the export status. |
| POST | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/feedbacktype/alerts/feedback | Adds an alert feedback submitted by customer. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/feedbacktype/alerts/{shortName}/alertfeedback | Gets a list of all alert feedback for a given tenant and alert type. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metrics/{metricName}/groups/{groupName} | Gets the server related metrics for a given metric and group combination. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metrics/{metricName}/groups/{groupName}/average | Gets the average of the metric values for a given metric and group combination. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metrics/{metricName}/groups/{groupName}/sum | Gets the sum of the metric values for a given metric and group combination. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metricmetadata | Gets the service related metrics information. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metricmetadata/{metricName} | Gets the service related metrics information. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metricmetadata/{metricName}/groups/{groupName} | Gets the service related metrics for a given metric and group combination. |
| PATCH | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/monitoringconfiguration | Updates the service level monitoring configuration. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/monitoringconfigurations | Gets the service level monitoring configurations. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/reports/badpassword/details/user | Gets the bad password login attempt report for an user |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers | Gets the details of the servers, for a given service, that are onboarded to Azure Active Directory Connect Health Service. |
| POST | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers | Onboards  a server, for a given service, to Azure Active Directory Connect Health Service. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId} | Gets the details of a server, for a given service, that are onboarded to Azure Active Directory Connect Health Service. |
| DELETE | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId} | Deletes a server that has been onboarded to Azure Active Directory Connect Health Service. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/alerts | Gets the details of an alert for a given service and server combination. |
| GET | /providers/Microsoft.ADHybridHealthService/service/{serviceName}/servicemembers/{serviceMemberId}/connectors | Gets the connector details for a service. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/credentials | Gets the credentials of the server which is needed by the agent to connect to Azure Active Directory Connect Health Service. |
| DELETE | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/data | Deletes the data uploaded by the server to Azure Active Directory Connect Health Service. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/datafreshness | Gets the last time when the server uploaded data to Azure Active Directory Connect Health Service. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/exportstatus | Gets the export status. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/globalconfiguration | Gets the global configuration. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/metrics/{metricName}/groups/{groupName} | Gets the server related metrics for a given metric and group combination. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/serviceconfiguration | Gets the service configuration. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/TenantWhitelisting/{featureName} | Checks if the tenant, to which a service is registered, is listed as allowed to use a feature. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/reports/riskyIp/blobUris | Gets all Risky IP report URIs for the last 7 days. |
| POST | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/reports/riskyIp/generateBlobUri | Initiate the generation of a new Risky IP report. Returns the URI for the new one. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/metrics/{metricName} | Gets the list of connectors and run profile names. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/ipAddressAggregates | Gets the IP address aggregates for a given service. |
| GET | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/ipAddressAggregateSettings | Gets the IP address aggregate settings. |
| PATCH | /providers/Microsoft.ADHybridHealthService/services/{serviceName}/ipAddressAggregateSettings | Updates the IP address aggregate settings alert thresholds. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all addsservices?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices
- "Create a addsservice?" -> POST /providers/Microsoft.ADHybridHealthService/addsservices
- "Get addsservice details?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}
- "Delete a addsservice?" -> DELETE /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}
- "Partially update a addsservice?" -> PATCH /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}
- "List all alerts?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/alerts
- "List all configuration?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/configuration
- "Get dimension details?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/dimensions/{dimension}
- "List all addsservicemembers?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/addsservicemembers
- "Search addomainservicemembers?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/addomainservicemembers
- "List all userpreference?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/features/{featureName}/userpreference
- "Create a userpreference?" -> POST /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/features/{featureName}/userpreference
- "List all forestsummary?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/forestsummary
- "Get group details?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metrics/{metricName}/groups/{groupName}
- "List all average?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metrics/{metricName}/groups/{groupName}/average
- "List all sum?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metrics/{metricName}/groups/{groupName}/sum
- "List all metricmetadata?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metricmetadata
- "Get metricmetadata details?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metricmetadata/{metricName}
- "Get group details?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/metricmetadata/{metricName}/groups/{groupName}
- "List all replicationdetails?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/replicationdetails
- "List all replicationstatus?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/replicationstatus
- "Search replicationsummary?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/replicationsummary
- "List all servicemembers?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers
- "Create a servicemember?" -> POST /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers
- "Get servicemember details?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers/{serviceMemberId}
- "Delete a servicemember?" -> DELETE /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers/{serviceMemberId}
- "List all alerts?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers/{serviceMemberId}/alerts
- "List all credentials?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/{serviceName}/servicemembers/{serviceMemberId}/credentials
- "List all premiumCheck?" -> GET /providers/Microsoft.ADHybridHealthService/addsservices/premiumCheck
- "List all operations?" -> GET /providers/Microsoft.ADHybridHealthService/operations
- "Create a configuration?" -> POST /providers/Microsoft.ADHybridHealthService/configuration
- "List all configuration?" -> GET /providers/Microsoft.ADHybridHealthService/configuration
- "List all IsDevOps?" -> GET /providers/Microsoft.ADHybridHealthService/reports/DevOps/IsDevOps
- "List all services?" -> GET /providers/Microsoft.ADHybridHealthService/services
- "Create a service?" -> POST /providers/Microsoft.ADHybridHealthService/services
- "List all premiumCheck?" -> GET /providers/Microsoft.ADHybridHealthService/services/premiumCheck
- "Get service details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}
- "Delete a service?" -> DELETE /providers/Microsoft.ADHybridHealthService/services/{serviceName}
- "Partially update a service?" -> PATCH /providers/Microsoft.ADHybridHealthService/services/{serviceName}
- "List all alerts?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/alerts
- "Get checkServiceFeatureAvailibility details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/checkServiceFeatureAvailibility/{featureName}
- "List all counts?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/exporterrors/counts
- "List all listV2?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/exporterrors/listV2
- "List all exportstatus?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/exportstatus
- "Create a feedback?" -> POST /providers/Microsoft.ADHybridHealthService/services/{serviceName}/feedbacktype/alerts/feedback
- "List all alertfeedback?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/feedbacktype/alerts/{shortName}/alertfeedback
- "Get group details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metrics/{metricName}/groups/{groupName}
- "List all average?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metrics/{metricName}/groups/{groupName}/average
- "List all sum?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metrics/{metricName}/groups/{groupName}/sum
- "List all metricmetadata?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metricmetadata
- "Get metricmetadata details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metricmetadata/{metricName}
- "Get group details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/metricmetadata/{metricName}/groups/{groupName}
- "List all monitoringconfigurations?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/monitoringconfigurations
- "List all user?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/reports/badpassword/details/user
- "List all servicemembers?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers
- "Create a servicemember?" -> POST /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers
- "Get servicemember details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}
- "Delete a servicemember?" -> DELETE /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}
- "List all alerts?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/alerts
- "List all connectors?" -> GET /providers/Microsoft.ADHybridHealthService/service/{serviceName}/servicemembers/{serviceMemberId}/connectors
- "List all credentials?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/credentials
- "List all datafreshness?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/datafreshness
- "List all exportstatus?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/exportstatus
- "List all globalconfiguration?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/globalconfiguration
- "Get group details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/metrics/{metricName}/groups/{groupName}
- "List all serviceconfiguration?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/serviceconfiguration
- "Get TenantWhitelisting details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/TenantWhitelisting/{featureName}
- "List all blobUris?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/reports/riskyIp/blobUris
- "Create a generateBlobUri?" -> POST /providers/Microsoft.ADHybridHealthService/services/{serviceName}/reports/riskyIp/generateBlobUri
- "Get metric details?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/servicemembers/{serviceMemberId}/metrics/{metricName}
- "List all ipAddressAggregates?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/ipAddressAggregates
- "List all ipAddressAggregateSettings?" -> GET /providers/Microsoft.ADHybridHealthService/services/{serviceName}/ipAddressAggregateSettings
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
