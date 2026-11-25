---
name: amazon-elasticsearch-service
description: "Amazon Elasticsearch Service API skill. Use when working with Amazon Elasticsearch Service for 2015-01-01. Covers 51 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Elasticsearch Service
API version: 2015-01-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /2015-01-01/es/reservedInstanceOfferings -- verify access
3. POST /2015-01-01/tags -- create first tags

## Endpoints

51 endpoints across 1 groups. See references/api-spec.lap for full details.

### 2015-01-01
| Method | Path | Description |
|--------|------|-------------|
| PUT | /2015-01-01/es/ccs/inboundConnection/{ConnectionId}/accept | Allows the destination domain owner to accept an inbound cross-cluster search connection request. |
| POST | /2015-01-01/tags | Attaches tags to an existing Elasticsearch domain. Tags are a set of case-sensitive key value pairs. An Elasticsearch domain may have up to 10 tags. See  Tagging Amazon Elasticsearch Service Domains for more information. |
| POST | /2015-01-01/packages/associate/{PackageID}/{DomainName} | Associates a package with an Amazon ES domain. |
| POST | /2015-01-01/es/domain/{DomainName}/authorizeVpcEndpointAccess | Provides access to an Amazon OpenSearch Service domain through the use of an interface VPC endpoint. |
| POST | /2015-01-01/es/domain/{DomainName}/config/cancel | Cancels a pending configuration change on an Amazon OpenSearch Service domain. |
| POST | /2015-01-01/es/serviceSoftwareUpdate/cancel | Cancels a scheduled service software update for an Amazon ES domain. You can only perform this operation before the AutomatedUpdateDate and when the UpdateStatus is in the PENDING_UPDATE state. |
| POST | /2015-01-01/es/domain | Creates a new Elasticsearch domain. For more information, see Creating Elasticsearch Domains in the Amazon Elasticsearch Service Developer Guide. |
| POST | /2015-01-01/es/ccs/outboundConnection | Creates a new cross-cluster search connection from a source domain to a destination domain. |
| POST | /2015-01-01/packages | Create a package for use with Amazon ES domains. |
| POST | /2015-01-01/es/vpcEndpoints | Creates an Amazon OpenSearch Service-managed VPC endpoint. |
| DELETE | /2015-01-01/es/domain/{DomainName} | Permanently deletes the specified Elasticsearch domain and all of its data. Once a domain is deleted, it cannot be recovered. |
| DELETE | /2015-01-01/es/role | Deletes the service-linked role that Elasticsearch Service uses to manage and maintain VPC domains. Role deletion will fail if any existing VPC domains use the role. You must delete any such Elasticsearch domains before deleting the role. See Deleting Elasticsearch Service Role in VPC Endpoints for Amazon Elasticsearch Service Domains. |
| DELETE | /2015-01-01/es/ccs/inboundConnection/{ConnectionId} | Allows the destination domain owner to delete an existing inbound cross-cluster search connection. |
| DELETE | /2015-01-01/es/ccs/outboundConnection/{ConnectionId} | Allows the source domain owner to delete an existing outbound cross-cluster search connection. |
| DELETE | /2015-01-01/packages/{PackageID} | Delete the package. |
| DELETE | /2015-01-01/es/vpcEndpoints/{VpcEndpointId} | Deletes an Amazon OpenSearch Service-managed interface VPC endpoint. |
| GET | /2015-01-01/es/domain/{DomainName}/autoTunes | Provides scheduled Auto-Tune action details for the Elasticsearch domain, such as Auto-Tune action type, description, severity, and scheduled date. |
| GET | /2015-01-01/es/domain/{DomainName}/progress | Returns information about the current blue/green deployment happening on a domain, including a change ID, status, and progress stages. |
| GET | /2015-01-01/es/domain/{DomainName} | Returns domain configuration information about the specified Elasticsearch domain, including the domain ID, domain endpoint, and domain ARN. |
| GET | /2015-01-01/es/domain/{DomainName}/config | Provides cluster configuration information about the specified Elasticsearch domain, such as the state, creation date, update version, and update date for cluster options. |
| POST | /2015-01-01/es/domain-info | Returns domain configuration information about the specified Elasticsearch domains, including the domain ID, domain endpoint, and domain ARN. |
| GET | /2015-01-01/es/instanceTypeLimits/{ElasticsearchVersion}/{InstanceType} | Describe Elasticsearch Limits for a given InstanceType and ElasticsearchVersion. When modifying existing Domain, specify the  DomainName  to know what Limits are supported for modifying. |
| POST | /2015-01-01/es/ccs/inboundConnection/search | Lists all the inbound cross-cluster search connections for a destination domain. |
| POST | /2015-01-01/es/ccs/outboundConnection/search | Lists all the outbound cross-cluster search connections for a source domain. |
| POST | /2015-01-01/packages/describe | Describes all packages available to Amazon ES. Includes options for filtering, limiting the number of results, and pagination. |
| GET | /2015-01-01/es/reservedInstanceOfferings | Lists available reserved Elasticsearch instance offerings. |
| GET | /2015-01-01/es/reservedInstances | Returns information about reserved Elasticsearch instances for this account. |
| POST | /2015-01-01/es/vpcEndpoints/describe | Describes one or more Amazon OpenSearch Service-managed VPC endpoints. |
| POST | /2015-01-01/packages/dissociate/{PackageID}/{DomainName} | Dissociates a package from the Amazon ES domain. |
| GET | /2015-01-01/es/compatibleVersions | Returns a list of upgrade compatible Elastisearch versions. You can optionally pass a  DomainName  to get all upgrade compatible Elasticsearch versions for that specific domain. |
| GET | /2015-01-01/packages/{PackageID}/history | Returns a list of versions of the package, along with their creation time and commit message. |
| GET | /2015-01-01/es/upgradeDomain/{DomainName}/history | Retrieves the complete history of the last 10 upgrades that were performed on the domain. |
| GET | /2015-01-01/es/upgradeDomain/{DomainName}/status | Retrieves the latest status of the last upgrade or upgrade eligibility check that was performed on the domain. |
| GET | /2015-01-01/domain | Returns the name of all Elasticsearch domains owned by the current user's account. |
| GET | /2015-01-01/packages/{PackageID}/domains | Lists all Amazon ES domains associated with the package. |
| GET | /2015-01-01/es/instanceTypes/{ElasticsearchVersion} | List all Elasticsearch instance types that are supported for given ElasticsearchVersion |
| GET | /2015-01-01/es/versions | List all supported Elasticsearch versions |
| GET | /2015-01-01/domain/{DomainName}/packages | Lists all packages associated with the Amazon ES domain. |
| GET | /2015-01-01/tags/ | Returns all tags for the given Elasticsearch domain. |
| GET | /2015-01-01/es/domain/{DomainName}/listVpcEndpointAccess | Retrieves information about each principal that is allowed to access a given Amazon OpenSearch Service domain through the use of an interface VPC endpoint. |
| GET | /2015-01-01/es/vpcEndpoints | Retrieves all Amazon OpenSearch Service-managed VPC endpoints in the current account and Region. |
| GET | /2015-01-01/es/domain/{DomainName}/vpcEndpoints | Retrieves all Amazon OpenSearch Service-managed VPC endpoints associated with a particular domain. |
| POST | /2015-01-01/es/purchaseReservedInstanceOffering | Allows you to purchase reserved Elasticsearch instances. |
| PUT | /2015-01-01/es/ccs/inboundConnection/{ConnectionId}/reject | Allows the destination domain owner to reject an inbound cross-cluster search connection request. |
| POST | /2015-01-01/tags-removal | Removes the specified set of tags from the specified Elasticsearch domain. |
| POST | /2015-01-01/es/domain/{DomainName}/revokeVpcEndpointAccess | Revokes access to an Amazon OpenSearch Service domain that was provided through an interface VPC endpoint. |
| POST | /2015-01-01/es/serviceSoftwareUpdate/start | Schedules a service software update for an Amazon ES domain. |
| POST | /2015-01-01/es/domain/{DomainName}/config | Modifies the cluster configuration of the specified Elasticsearch domain, setting as setting the instance type and the number of instances. |
| POST | /2015-01-01/packages/update | Updates a package for use with Amazon ES domains. |
| POST | /2015-01-01/es/vpcEndpoints/update | Modifies an Amazon OpenSearch Service-managed interface VPC endpoint. |
| POST | /2015-01-01/es/upgradeDomain | Allows you to either upgrade your domain or perform an Upgrade eligibility check to a compatible Elasticsearch version. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a tag?" -> POST /2015-01-01/tags
- "Create a authorizeVpcEndpointAccess?" -> POST /2015-01-01/es/domain/{DomainName}/authorizeVpcEndpointAccess
- "Create a cancel?" -> POST /2015-01-01/es/domain/{DomainName}/config/cancel
- "Create a cancel?" -> POST /2015-01-01/es/serviceSoftwareUpdate/cancel
- "Create a domain?" -> POST /2015-01-01/es/domain
- "Create a outboundConnection?" -> POST /2015-01-01/es/ccs/outboundConnection
- "Create a package?" -> POST /2015-01-01/packages
- "Create a vpcEndpoint?" -> POST /2015-01-01/es/vpcEndpoints
- "Delete a domain?" -> DELETE /2015-01-01/es/domain/{DomainName}
- "Delete a inboundConnection?" -> DELETE /2015-01-01/es/ccs/inboundConnection/{ConnectionId}
- "Delete a outboundConnection?" -> DELETE /2015-01-01/es/ccs/outboundConnection/{ConnectionId}
- "Delete a package?" -> DELETE /2015-01-01/packages/{PackageID}
- "Delete a vpcEndpoint?" -> DELETE /2015-01-01/es/vpcEndpoints/{VpcEndpointId}
- "List all autoTunes?" -> GET /2015-01-01/es/domain/{DomainName}/autoTunes
- "List all progress?" -> GET /2015-01-01/es/domain/{DomainName}/progress
- "Get domain details?" -> GET /2015-01-01/es/domain/{DomainName}
- "List all config?" -> GET /2015-01-01/es/domain/{DomainName}/config
- "Create a domain-info?" -> POST /2015-01-01/es/domain-info
- "Get instanceTypeLimit details?" -> GET /2015-01-01/es/instanceTypeLimits/{ElasticsearchVersion}/{InstanceType}
- "Create a search?" -> POST /2015-01-01/es/ccs/inboundConnection/search
- "Create a search?" -> POST /2015-01-01/es/ccs/outboundConnection/search
- "Create a describe?" -> POST /2015-01-01/packages/describe
- "List all reservedInstanceOfferings?" -> GET /2015-01-01/es/reservedInstanceOfferings
- "List all reservedInstances?" -> GET /2015-01-01/es/reservedInstances
- "Create a describe?" -> POST /2015-01-01/es/vpcEndpoints/describe
- "List all compatibleVersions?" -> GET /2015-01-01/es/compatibleVersions
- "List all history?" -> GET /2015-01-01/packages/{PackageID}/history
- "List all history?" -> GET /2015-01-01/es/upgradeDomain/{DomainName}/history
- "List all status?" -> GET /2015-01-01/es/upgradeDomain/{DomainName}/status
- "List all domain?" -> GET /2015-01-01/domain
- "List all domains?" -> GET /2015-01-01/packages/{PackageID}/domains
- "Get instanceType details?" -> GET /2015-01-01/es/instanceTypes/{ElasticsearchVersion}
- "List all versions?" -> GET /2015-01-01/es/versions
- "List all packages?" -> GET /2015-01-01/domain/{DomainName}/packages
- "List all tags?" -> GET /2015-01-01/tags/
- "List all listVpcEndpointAccess?" -> GET /2015-01-01/es/domain/{DomainName}/listVpcEndpointAccess
- "List all vpcEndpoints?" -> GET /2015-01-01/es/vpcEndpoints
- "List all vpcEndpoints?" -> GET /2015-01-01/es/domain/{DomainName}/vpcEndpoints
- "Create a purchaseReservedInstanceOffering?" -> POST /2015-01-01/es/purchaseReservedInstanceOffering
- "Create a tags-removal?" -> POST /2015-01-01/tags-removal
- "Create a revokeVpcEndpointAccess?" -> POST /2015-01-01/es/domain/{DomainName}/revokeVpcEndpointAccess
- "Create a start?" -> POST /2015-01-01/es/serviceSoftwareUpdate/start
- "Create a config?" -> POST /2015-01-01/es/domain/{DomainName}/config
- "Create a update?" -> POST /2015-01-01/packages/update
- "Create a update?" -> POST /2015-01-01/es/vpcEndpoints/update
- "Create a upgradeDomain?" -> POST /2015-01-01/es/upgradeDomain
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
