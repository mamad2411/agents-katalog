---
name: aws-network-manager
description: "AWS Network Manager API skill. Use when working with AWS Network Manager for attachments, global-networks, connect-attachments. Covers 85 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Network Manager
API version: 2019-07-05

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /global-networks -- verify access
3. POST /attachments/{attachmentId}/accept -- create first accept

## Endpoints

85 endpoints across 13 groups. See references/api-spec.lap for full details.

### attachments
| Method | Path | Description |
|--------|------|-------------|
| POST | /attachments/{attachmentId}/accept | Accepts a core network attachment request.  Once the attachment request is accepted by a core network owner, the attachment is created and connected to a core network. |
| DELETE | /attachments/{attachmentId} | Deletes an attachment. Supports all attachment types. |
| GET | /attachments | Returns a list of core network attachments. |
| POST | /attachments/{attachmentId}/reject | Rejects a core network attachment request. |

### global-networks
| Method | Path | Description |
|--------|------|-------------|
| POST | /global-networks/{globalNetworkId}/connect-peer-associations | Associates a core network Connect peer with a device and optionally, with a link.  If you specify a link, it must be associated with the specified device. You can only associate core network Connect peers that have been created on a core network Connect attachment on a core network. |
| POST | /global-networks/{globalNetworkId}/customer-gateway-associations | Associates a customer gateway with a device and optionally, with a link. If you specify a link, it must be associated with the specified device.  You can only associate customer gateways that are connected to a VPN attachment on a transit gateway or core network registered in your global network. When you register a transit gateway or core network, customer gateways that are connected to the transit gateway are automatically included in the global network. To list customer gateways that are connected to a transit gateway, use the DescribeVpnConnections EC2 API and filter by transit-gateway-id. You cannot associate a customer gateway with more than one device and link. |
| POST | /global-networks/{globalNetworkId}/link-associations | Associates a link to a device. A device can be associated to multiple links and a link can be associated to multiple devices. The device and link must be in the same global network and the same site. |
| POST | /global-networks/{globalNetworkId}/transit-gateway-connect-peer-associations | Associates a transit gateway Connect peer with a device, and optionally, with a link. If you specify a link, it must be associated with the specified device.  You can only associate transit gateway Connect peers that have been created on a transit gateway that's registered in your global network. You cannot associate a transit gateway Connect peer with more than one device and link. |
| POST | /global-networks/{globalNetworkId}/connections | Creates a connection between two devices. The devices can be a physical or virtual appliance that connects to a third-party appliance in a VPC, or a physical appliance that connects to another physical appliance in an on-premises network. |
| POST | /global-networks/{globalNetworkId}/devices | Creates a new device in a global network. If you specify both a site ID and a location, the location of the site is used for visualization in the Network Manager console. |
| POST | /global-networks | Creates a new, empty global network. |
| POST | /global-networks/{globalNetworkId}/links | Creates a new link for a specified site. |
| POST | /global-networks/{globalNetworkId}/sites | Creates a new site in a global network. |
| DELETE | /global-networks/{globalNetworkId}/connections/{connectionId} | Deletes the specified connection in your global network. |
| DELETE | /global-networks/{globalNetworkId}/devices/{deviceId} | Deletes an existing device. You must first disassociate the device from any links and customer gateways. |
| DELETE | /global-networks/{globalNetworkId} | Deletes an existing global network. You must first delete all global network objects (devices, links, and sites), deregister all transit gateways, and delete any core networks. |
| DELETE | /global-networks/{globalNetworkId}/links/{linkId} | Deletes an existing link. You must first disassociate the link from any devices and customer gateways. |
| DELETE | /global-networks/{globalNetworkId}/sites/{siteId} | Deletes an existing site. The site cannot be associated with any device or link. |
| DELETE | /global-networks/{globalNetworkId}/transit-gateway-registrations/{transitGatewayArn} | Deregisters a transit gateway from your global network. This action does not delete your transit gateway, or modify any of its attachments. This action removes any customer gateway associations. |
| GET | /global-networks | Describes one or more global networks. By default, all global networks are described. To describe the objects in your global network, you must use the appropriate Get* action. For example, to list the transit gateways in your global network, use GetTransitGatewayRegistrations. |
| DELETE | /global-networks/{globalNetworkId}/connect-peer-associations/{connectPeerId} | Disassociates a core network Connect peer from a device and a link. |
| DELETE | /global-networks/{globalNetworkId}/customer-gateway-associations/{customerGatewayArn} | Disassociates a customer gateway from a device and a link. |
| DELETE | /global-networks/{globalNetworkId}/link-associations | Disassociates an existing device from a link. You must first disassociate any customer gateways that are associated with the link. |
| DELETE | /global-networks/{globalNetworkId}/transit-gateway-connect-peer-associations/{transitGatewayConnectPeerArn} | Disassociates a transit gateway Connect peer from a device and link. |
| GET | /global-networks/{globalNetworkId}/connect-peer-associations | Returns information about a core network Connect peer associations. |
| GET | /global-networks/{globalNetworkId}/connections | Gets information about one or more of your connections in a global network. |
| GET | /global-networks/{globalNetworkId}/customer-gateway-associations | Gets the association information for customer gateways that are associated with devices and links in your global network. |
| GET | /global-networks/{globalNetworkId}/devices | Gets information about one or more of your devices in a global network. |
| GET | /global-networks/{globalNetworkId}/link-associations | Gets the link associations for a device or a link. Either the device ID or the link ID must be specified. |
| GET | /global-networks/{globalNetworkId}/links | Gets information about one or more links in a specified global network. If you specify the site ID, you cannot specify the type or provider in the same request. You can specify the type and provider in the same request. |
| GET | /global-networks/{globalNetworkId}/network-resource-count | Gets the count of network resources, by resource type, for the specified global network. |
| GET | /global-networks/{globalNetworkId}/network-resource-relationships | Gets the network resource relationships for the specified global network. |
| GET | /global-networks/{globalNetworkId}/network-resources | Describes the network resources for the specified global network. The results include information from the corresponding Describe call for the resource, minus any sensitive information such as pre-shared keys. |
| POST | /global-networks/{globalNetworkId}/network-routes | Gets the network routes of the specified global network. |
| GET | /global-networks/{globalNetworkId}/network-telemetry | Gets the network telemetry of the specified global network. |
| GET | /global-networks/{globalNetworkId}/route-analyses/{routeAnalysisId} | Gets information about the specified route analysis. |
| GET | /global-networks/{globalNetworkId}/sites | Gets information about one or more of your sites in a global network. |
| GET | /global-networks/{globalNetworkId}/transit-gateway-connect-peer-associations | Gets information about one or more of your transit gateway Connect peer associations in a global network. |
| GET | /global-networks/{globalNetworkId}/transit-gateway-registrations | Gets information about the transit gateway registrations in a specified global network. |
| POST | /global-networks/{globalNetworkId}/transit-gateway-registrations | Registers a transit gateway in your global network. Not all Regions support transit gateways for global networks. For a list of the supported Regions, see Region Availability in the Amazon Web Services Transit Gateways for Global Networks User Guide. The transit gateway can be in any of the supported Amazon Web Services Regions, but it must be owned by the same Amazon Web Services account that owns the global network. You cannot register a transit gateway in more than one global network. |
| POST | /global-networks/{globalNetworkId}/route-analyses | Starts analyzing the routing path between the specified source and destination. For more information, see Route Analyzer. |
| PATCH | /global-networks/{globalNetworkId}/connections/{connectionId} | Updates the information for an existing connection. To remove information for any of the parameters, specify an empty string. |
| PATCH | /global-networks/{globalNetworkId}/devices/{deviceId} | Updates the details for an existing device. To remove information for any of the parameters, specify an empty string. |
| PATCH | /global-networks/{globalNetworkId} | Updates an existing global network. To remove information for any of the parameters, specify an empty string. |
| PATCH | /global-networks/{globalNetworkId}/links/{linkId} | Updates the details for an existing link. To remove information for any of the parameters, specify an empty string. |
| PATCH | /global-networks/{globalNetworkId}/network-resources/{resourceArn}/metadata | Updates the resource metadata for the specified global network. |
| PATCH | /global-networks/{globalNetworkId}/sites/{siteId} | Updates the information for an existing site. To remove information for any of the parameters, specify an empty string. |

### connect-attachments
| Method | Path | Description |
|--------|------|-------------|
| POST | /connect-attachments | Creates a core network Connect attachment from a specified core network attachment.  A core network Connect attachment is a GRE-based tunnel attachment that you can use to establish a connection between a core network and an appliance. A core network Connect attachment uses an existing VPC attachment as the underlying transport mechanism. |
| GET | /connect-attachments/{attachmentId} | Returns information about a core network Connect attachment. |

### connect-peers
| Method | Path | Description |
|--------|------|-------------|
| POST | /connect-peers | Creates a core network Connect peer for a specified core network connect attachment between a core network and an appliance. The peer address and transit gateway address must be the same IP address family (IPv4 or IPv6). |
| DELETE | /connect-peers/{connectPeerId} | Deletes a Connect peer. |
| GET | /connect-peers/{connectPeerId} | Returns information about a core network Connect peer. |
| GET | /connect-peers | Returns a list of core network Connect peers. |

### core-networks
| Method | Path | Description |
|--------|------|-------------|
| POST | /core-networks | Creates a core network as part of your global network, and optionally, with a core network policy. |
| DELETE | /core-networks/{coreNetworkId} | Deletes a core network along with all core network policies. This can only be done if there are no attachments on a core network. |
| DELETE | /core-networks/{coreNetworkId}/core-network-policy-versions/{policyVersionId} | Deletes a policy version from a core network. You can't delete the current LIVE policy. |
| POST | /core-networks/{coreNetworkId}/core-network-change-sets/{policyVersionId}/execute | Executes a change set on your core network. Deploys changes globally based on the policy submitted.. |
| GET | /core-networks/{coreNetworkId} | Returns information about the LIVE policy for a core network. |
| GET | /core-networks/{coreNetworkId}/core-network-change-events/{policyVersionId} | Returns information about a core network change event. |
| GET | /core-networks/{coreNetworkId}/core-network-change-sets/{policyVersionId} | Returns a change set between the LIVE core network policy and a submitted policy. |
| GET | /core-networks/{coreNetworkId}/core-network-policy | Returns details about a core network policy. You can get details about your current live policy or any previous policy version. |
| GET | /core-networks/{coreNetworkId}/core-network-policy-versions | Returns a list of core network policy versions. |
| GET | /core-networks | Returns a list of owned and shared core networks. |
| POST | /core-networks/{coreNetworkId}/core-network-policy | Creates a new, immutable version of a core network policy. A subsequent change set is created showing the differences between the LIVE policy and the submitted policy. |
| POST | /core-networks/{coreNetworkId}/core-network-policy-versions/{policyVersionId}/restore | Restores a previous policy version as a new, immutable version of a core network policy. A subsequent change set is created showing the differences between the LIVE policy and restored policy. |
| PATCH | /core-networks/{coreNetworkId} | Updates the description of a core network. |

### site-to-site-vpn-attachments
| Method | Path | Description |
|--------|------|-------------|
| POST | /site-to-site-vpn-attachments | Creates an Amazon Web Services site-to-site VPN attachment on an edge location of a core network. |
| GET | /site-to-site-vpn-attachments/{attachmentId} | Returns information about a site-to-site VPN attachment. |

### transit-gateway-peerings
| Method | Path | Description |
|--------|------|-------------|
| POST | /transit-gateway-peerings | Creates a transit gateway peering connection. |
| GET | /transit-gateway-peerings/{peeringId} | Returns information about a transit gateway peer. |

### transit-gateway-route-table-attachments
| Method | Path | Description |
|--------|------|-------------|
| POST | /transit-gateway-route-table-attachments | Creates a transit gateway route table attachment. |
| GET | /transit-gateway-route-table-attachments/{attachmentId} | Returns information about a transit gateway route table attachment. |

### vpc-attachments
| Method | Path | Description |
|--------|------|-------------|
| POST | /vpc-attachments | Creates a VPC attachment on an edge location of a core network. |
| GET | /vpc-attachments/{attachmentId} | Returns information about a VPC attachment. |
| PATCH | /vpc-attachments/{attachmentId} | Updates a VPC attachment. |

### peerings
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /peerings/{peeringId} | Deletes an existing peering connection. |
| GET | /peerings | Lists the peerings for a core network. |

### resource-policy
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /resource-policy/{resourceArn} | Deletes a resource policy for the specified resource. This revokes the access of the principals specified in the resource policy. |
| GET | /resource-policy/{resourceArn} | Returns information about a resource policy. |
| POST | /resource-policy/{resourceArn} | Creates or updates a resource policy. |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations/service-access | Gets the status of the Service Linked Role (SLR) deployment for the accounts in a given Amazon Web Services Organization. |
| POST | /organizations/service-access | Enables the Network Manager service for an Amazon Web Services Organization. This can only be called by a management account within the organization. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags for a specified resource. |
| POST | /tags/{resourceArn} | Tags a specified resource. |
| DELETE | /tags/{resourceArn} | Removes tags from a specified resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a accept?" -> POST /attachments/{attachmentId}/accept
- "Create a connect-peer-association?" -> POST /global-networks/{globalNetworkId}/connect-peer-associations
- "Create a customer-gateway-association?" -> POST /global-networks/{globalNetworkId}/customer-gateway-associations
- "Create a link-association?" -> POST /global-networks/{globalNetworkId}/link-associations
- "Create a transit-gateway-connect-peer-association?" -> POST /global-networks/{globalNetworkId}/transit-gateway-connect-peer-associations
- "Create a connect-attachment?" -> POST /connect-attachments
- "Create a connect-peer?" -> POST /connect-peers
- "Create a connection?" -> POST /global-networks/{globalNetworkId}/connections
- "Create a core-network?" -> POST /core-networks
- "Create a device?" -> POST /global-networks/{globalNetworkId}/devices
- "Create a global-network?" -> POST /global-networks
- "Create a link?" -> POST /global-networks/{globalNetworkId}/links
- "Create a site?" -> POST /global-networks/{globalNetworkId}/sites
- "Create a site-to-site-vpn-attachment?" -> POST /site-to-site-vpn-attachments
- "Create a transit-gateway-peering?" -> POST /transit-gateway-peerings
- "Create a transit-gateway-route-table-attachment?" -> POST /transit-gateway-route-table-attachments
- "Create a vpc-attachment?" -> POST /vpc-attachments
- "Delete a attachment?" -> DELETE /attachments/{attachmentId}
- "Delete a connect-peer?" -> DELETE /connect-peers/{connectPeerId}
- "Delete a connection?" -> DELETE /global-networks/{globalNetworkId}/connections/{connectionId}
- "Delete a core-network?" -> DELETE /core-networks/{coreNetworkId}
- "Delete a core-network-policy-version?" -> DELETE /core-networks/{coreNetworkId}/core-network-policy-versions/{policyVersionId}
- "Delete a device?" -> DELETE /global-networks/{globalNetworkId}/devices/{deviceId}
- "Delete a global-network?" -> DELETE /global-networks/{globalNetworkId}
- "Delete a link?" -> DELETE /global-networks/{globalNetworkId}/links/{linkId}
- "Delete a peering?" -> DELETE /peerings/{peeringId}
- "Delete a resource-policy?" -> DELETE /resource-policy/{resourceArn}
- "Delete a site?" -> DELETE /global-networks/{globalNetworkId}/sites/{siteId}
- "Delete a transit-gateway-registration?" -> DELETE /global-networks/{globalNetworkId}/transit-gateway-registrations/{transitGatewayArn}
- "List all global-networks?" -> GET /global-networks
- "Delete a connect-peer-association?" -> DELETE /global-networks/{globalNetworkId}/connect-peer-associations/{connectPeerId}
- "Delete a customer-gateway-association?" -> DELETE /global-networks/{globalNetworkId}/customer-gateway-associations/{customerGatewayArn}
- "Delete a transit-gateway-connect-peer-association?" -> DELETE /global-networks/{globalNetworkId}/transit-gateway-connect-peer-associations/{transitGatewayConnectPeerArn}
- "Create a execute?" -> POST /core-networks/{coreNetworkId}/core-network-change-sets/{policyVersionId}/execute
- "Get connect-attachment details?" -> GET /connect-attachments/{attachmentId}
- "Get connect-peer details?" -> GET /connect-peers/{connectPeerId}
- "List all connect-peer-associations?" -> GET /global-networks/{globalNetworkId}/connect-peer-associations
- "List all connections?" -> GET /global-networks/{globalNetworkId}/connections
- "Get core-network details?" -> GET /core-networks/{coreNetworkId}
- "Get core-network-change-event details?" -> GET /core-networks/{coreNetworkId}/core-network-change-events/{policyVersionId}
- "Get core-network-change-set details?" -> GET /core-networks/{coreNetworkId}/core-network-change-sets/{policyVersionId}
- "List all core-network-policy?" -> GET /core-networks/{coreNetworkId}/core-network-policy
- "List all customer-gateway-associations?" -> GET /global-networks/{globalNetworkId}/customer-gateway-associations
- "List all devices?" -> GET /global-networks/{globalNetworkId}/devices
- "List all link-associations?" -> GET /global-networks/{globalNetworkId}/link-associations
- "List all links?" -> GET /global-networks/{globalNetworkId}/links
- "List all network-resource-count?" -> GET /global-networks/{globalNetworkId}/network-resource-count
- "List all network-resource-relationships?" -> GET /global-networks/{globalNetworkId}/network-resource-relationships
- "List all network-resources?" -> GET /global-networks/{globalNetworkId}/network-resources
- "Create a network-route?" -> POST /global-networks/{globalNetworkId}/network-routes
- "List all network-telemetry?" -> GET /global-networks/{globalNetworkId}/network-telemetry
- "Get resource-policy details?" -> GET /resource-policy/{resourceArn}
- "Get route-analys details?" -> GET /global-networks/{globalNetworkId}/route-analyses/{routeAnalysisId}
- "Get site-to-site-vpn-attachment details?" -> GET /site-to-site-vpn-attachments/{attachmentId}
- "List all sites?" -> GET /global-networks/{globalNetworkId}/sites
- "List all transit-gateway-connect-peer-associations?" -> GET /global-networks/{globalNetworkId}/transit-gateway-connect-peer-associations
- "Get transit-gateway-peering details?" -> GET /transit-gateway-peerings/{peeringId}
- "List all transit-gateway-registrations?" -> GET /global-networks/{globalNetworkId}/transit-gateway-registrations
- "Get transit-gateway-route-table-attachment details?" -> GET /transit-gateway-route-table-attachments/{attachmentId}
- "Get vpc-attachment details?" -> GET /vpc-attachments/{attachmentId}
- "List all attachments?" -> GET /attachments
- "List all connect-peers?" -> GET /connect-peers
- "List all core-network-policy-versions?" -> GET /core-networks/{coreNetworkId}/core-network-policy-versions
- "List all core-networks?" -> GET /core-networks
- "List all service-access?" -> GET /organizations/service-access
- "List all peerings?" -> GET /peerings
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a core-network-policy?" -> POST /core-networks/{coreNetworkId}/core-network-policy
- "Create a transit-gateway-registration?" -> POST /global-networks/{globalNetworkId}/transit-gateway-registrations
- "Create a reject?" -> POST /attachments/{attachmentId}/reject
- "Create a restore?" -> POST /core-networks/{coreNetworkId}/core-network-policy-versions/{policyVersionId}/restore
- "Create a service-access?" -> POST /organizations/service-access
- "Create a route-analys?" -> POST /global-networks/{globalNetworkId}/route-analyses
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a connection?" -> PATCH /global-networks/{globalNetworkId}/connections/{connectionId}
- "Partially update a core-network?" -> PATCH /core-networks/{coreNetworkId}
- "Partially update a device?" -> PATCH /global-networks/{globalNetworkId}/devices/{deviceId}
- "Partially update a global-network?" -> PATCH /global-networks/{globalNetworkId}
- "Partially update a link?" -> PATCH /global-networks/{globalNetworkId}/links/{linkId}
- "Partially update a site?" -> PATCH /global-networks/{globalNetworkId}/sites/{siteId}
- "Partially update a vpc-attachment?" -> PATCH /vpc-attachments/{attachmentId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
