---
name: amazon-worklink
description: "Amazon WorkLink API skill. Use when working with Amazon WorkLink for associateDomain, associateWebsiteAuthorizationProvider, associateWebsiteCertificateAuthority. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon WorkLink
API version: 2018-09-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /tags/{ResourceArn} -- verify access
3. POST /associateDomain -- create first associateDomain

## Endpoints

33 endpoints across 31 groups. See references/api-spec.lap for full details.

### associateDomain
| Method | Path | Description |
|--------|------|-------------|
| POST | /associateDomain | Specifies a domain to be associated to Amazon WorkLink. |

### associateWebsiteAuthorizationProvider
| Method | Path | Description |
|--------|------|-------------|
| POST | /associateWebsiteAuthorizationProvider | Associates a website authorization provider with a specified fleet. This is used to authorize users against associated websites in the company network. |

### associateWebsiteCertificateAuthority
| Method | Path | Description |
|--------|------|-------------|
| POST | /associateWebsiteCertificateAuthority | Imports the root certificate of a certificate authority (CA) used to obtain TLS certificates used by associated websites within the company network. |

### createFleet
| Method | Path | Description |
|--------|------|-------------|
| POST | /createFleet | Creates a fleet. A fleet consists of resources and the configuration that delivers associated websites to authorized users who download and set up the Amazon WorkLink app. |

### deleteFleet
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteFleet | Deletes a fleet. Prevents users from accessing previously associated websites. |

### describeAuditStreamConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeAuditStreamConfiguration | Describes the configuration for delivering audit streams to the customer account. |

### describeCompanyNetworkConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeCompanyNetworkConfiguration | Describes the networking configuration to access the internal websites associated with the specified fleet. |

### describeDevice
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeDevice | Provides information about a user's device. |

### describeDevicePolicyConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeDevicePolicyConfiguration | Describes the device policy configuration for the specified fleet. |

### describeDomain
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeDomain | Provides information about the domain. |

### describeFleetMetadata
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeFleetMetadata | Provides basic information for the specified fleet, excluding identity provider, networking, and device configuration details. |

### describeIdentityProviderConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeIdentityProviderConfiguration | Describes the identity provider configuration of the specified fleet. |

### describeWebsiteCertificateAuthority
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeWebsiteCertificateAuthority | Provides information about the certificate authority. |

### disassociateDomain
| Method | Path | Description |
|--------|------|-------------|
| POST | /disassociateDomain | Disassociates a domain from Amazon WorkLink. End users lose the ability to access the domain with Amazon WorkLink. |

### disassociateWebsiteAuthorizationProvider
| Method | Path | Description |
|--------|------|-------------|
| POST | /disassociateWebsiteAuthorizationProvider | Disassociates a website authorization provider from a specified fleet. After the disassociation, users can't load any associated websites that require this authorization provider. |

### disassociateWebsiteCertificateAuthority
| Method | Path | Description |
|--------|------|-------------|
| POST | /disassociateWebsiteCertificateAuthority | Removes a certificate authority (CA). |

### listDevices
| Method | Path | Description |
|--------|------|-------------|
| POST | /listDevices | Retrieves a list of devices registered with the specified fleet. |

### listDomains
| Method | Path | Description |
|--------|------|-------------|
| POST | /listDomains | Retrieves a list of domains associated to a specified fleet. |

### listFleets
| Method | Path | Description |
|--------|------|-------------|
| POST | /listFleets | Retrieves a list of fleets for the current account and Region. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | Retrieves a list of tags for the specified resource. |
| POST | /tags/{ResourceArn} | Adds or overwrites one or more tags for the specified resource, such as a fleet. Each tag consists of a key and an optional value. If a resource already has a tag with the same key, this operation updates its value. |
| DELETE | /tags/{ResourceArn} | Removes one or more tags from the specified resource. |

### listWebsiteAuthorizationProviders
| Method | Path | Description |
|--------|------|-------------|
| POST | /listWebsiteAuthorizationProviders | Retrieves a list of website authorization providers associated with a specified fleet. |

### listWebsiteCertificateAuthorities
| Method | Path | Description |
|--------|------|-------------|
| POST | /listWebsiteCertificateAuthorities | Retrieves a list of certificate authorities added for the current account and Region. |

### restoreDomainAccess
| Method | Path | Description |
|--------|------|-------------|
| POST | /restoreDomainAccess | Moves a domain to ACTIVE status if it was in the INACTIVE status. |

### revokeDomainAccess
| Method | Path | Description |
|--------|------|-------------|
| POST | /revokeDomainAccess | Moves a domain to INACTIVE status if it was in the ACTIVE status. |

### signOutUser
| Method | Path | Description |
|--------|------|-------------|
| POST | /signOutUser | Signs the user out from all of their devices. The user can sign in again if they have valid credentials. |

### updateAuditStreamConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateAuditStreamConfiguration | Updates the audit stream configuration for the fleet. |

### updateCompanyNetworkConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateCompanyNetworkConfiguration | Updates the company network configuration for the fleet. |

### updateDevicePolicyConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateDevicePolicyConfiguration | Updates the device policy configuration for the fleet. |

### updateDomainMetadata
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateDomainMetadata | Updates domain metadata, such as DisplayName. |

### UpdateFleetMetadata
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateFleetMetadata | Updates fleet metadata, such as DisplayName. |

### updateIdentityProviderConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateIdentityProviderConfiguration | Updates the identity provider configuration for the fleet. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a associateDomain?" -> POST /associateDomain
- "Create a associateWebsiteAuthorizationProvider?" -> POST /associateWebsiteAuthorizationProvider
- "Create a associateWebsiteCertificateAuthority?" -> POST /associateWebsiteCertificateAuthority
- "Create a createFleet?" -> POST /createFleet
- "Create a deleteFleet?" -> POST /deleteFleet
- "Create a describeAuditStreamConfiguration?" -> POST /describeAuditStreamConfiguration
- "Create a describeCompanyNetworkConfiguration?" -> POST /describeCompanyNetworkConfiguration
- "Create a describeDevice?" -> POST /describeDevice
- "Create a describeDevicePolicyConfiguration?" -> POST /describeDevicePolicyConfiguration
- "Create a describeDomain?" -> POST /describeDomain
- "Create a describeFleetMetadata?" -> POST /describeFleetMetadata
- "Create a describeIdentityProviderConfiguration?" -> POST /describeIdentityProviderConfiguration
- "Create a describeWebsiteCertificateAuthority?" -> POST /describeWebsiteCertificateAuthority
- "Create a disassociateDomain?" -> POST /disassociateDomain
- "Create a disassociateWebsiteAuthorizationProvider?" -> POST /disassociateWebsiteAuthorizationProvider
- "Create a disassociateWebsiteCertificateAuthority?" -> POST /disassociateWebsiteCertificateAuthority
- "Create a listDevice?" -> POST /listDevices
- "Create a listDomain?" -> POST /listDomains
- "Create a listFleet?" -> POST /listFleets
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Create a listWebsiteAuthorizationProvider?" -> POST /listWebsiteAuthorizationProviders
- "Create a listWebsiteCertificateAuthority?" -> POST /listWebsiteCertificateAuthorities
- "Create a restoreDomainAccess?" -> POST /restoreDomainAccess
- "Create a revokeDomainAccess?" -> POST /revokeDomainAccess
- "Create a signOutUser?" -> POST /signOutUser
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Create a updateAuditStreamConfiguration?" -> POST /updateAuditStreamConfiguration
- "Create a updateCompanyNetworkConfiguration?" -> POST /updateCompanyNetworkConfiguration
- "Create a updateDevicePolicyConfiguration?" -> POST /updateDevicePolicyConfiguration
- "Create a updateDomainMetadata?" -> POST /updateDomainMetadata
- "Create a UpdateFleetMetadata?" -> POST /UpdateFleetMetadata
- "Create a updateIdentityProviderConfiguration?" -> POST /updateIdentityProviderConfiguration
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
