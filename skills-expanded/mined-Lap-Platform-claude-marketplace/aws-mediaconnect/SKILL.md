---
name: aws-mediaconnect
description: "AWS MediaConnect API skill. Use when working with AWS MediaConnect for bridges, flows, gateways. Covers 52 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS MediaConnect
API version: 2018-11-14

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/bridges -- verify access
3. POST /v1/bridges/{bridgeArn}/outputs -- create first outputs

## Endpoints

52 endpoints across 8 groups. See references/api-spec.lap for full details.

### bridges
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/bridges/{bridgeArn}/outputs | Adds outputs to an existing bridge. |
| POST | /v1/bridges/{bridgeArn}/sources | Adds sources to an existing bridge. |
| POST | /v1/bridges | Creates a new bridge. The request must include one source. |
| DELETE | /v1/bridges/{bridgeArn} | Deletes a bridge. Before you can delete a bridge, you must stop the bridge. |
| GET | /v1/bridges/{bridgeArn} | Displays the details of a bridge. |
| GET | /v1/bridges | Displays a list of bridges that are associated with this account and an optionally specified Arn. This request returns a paginated result. |
| DELETE | /v1/bridges/{bridgeArn}/outputs/{outputName} | Removes an output from a bridge. |
| DELETE | /v1/bridges/{bridgeArn}/sources/{sourceName} | Removes a source from a bridge. |
| PUT | /v1/bridges/{bridgeArn} | Updates the bridge |
| PUT | /v1/bridges/{bridgeArn}/outputs/{outputName} | Updates an existing bridge output. |
| PUT | /v1/bridges/{bridgeArn}/sources/{sourceName} | Updates an existing bridge source. |
| PUT | /v1/bridges/{bridgeArn}/state | Updates the bridge state |

### flows
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/flows/{flowArn}/mediaStreams | Adds media streams to an existing flow. After you add a media stream to a flow, you can associate it with a source and/or an output that uses the ST 2110 JPEG XS or CDI protocol. |
| POST | /v1/flows/{flowArn}/outputs | Adds outputs to an existing flow. You can create up to 50 outputs per flow. |
| POST | /v1/flows/{flowArn}/source | Adds Sources to flow |
| POST | /v1/flows/{flowArn}/vpcInterfaces | Adds VPC interfaces to flow |
| POST | /v1/flows | Creates a new flow. The request must include one source. The request optionally can include outputs (up to 50) and entitlements (up to 50). |
| DELETE | /v1/flows/{flowArn} | Deletes a flow. Before you can delete a flow, you must stop the flow. |
| GET | /v1/flows/{flowArn} | Displays the details of a flow. The response includes the flow ARN, name, and Availability Zone, as well as details about the source, outputs, and entitlements. |
| GET | /v1/flows/{flowArn}/source-metadata | Displays details of the flow's source stream. The response contains information about the contents of the stream and its programs. |
| GET | /v1/flows/{flowArn}/source-thumbnail | Displays the thumbnail details of a flow's source stream. |
| POST | /v1/flows/{flowArn}/entitlements | Grants entitlements to an existing flow. |
| GET | /v1/flows | Displays a list of flows that are associated with this account. This request returns a paginated result. |
| DELETE | /v1/flows/{flowArn}/mediaStreams/{mediaStreamName} | Removes a media stream from a flow. This action is only available if the media stream is not associated with a source or output. |
| DELETE | /v1/flows/{flowArn}/outputs/{outputArn} | Removes an output from an existing flow. This request can be made only on an output that does not have an entitlement associated with it. If the output has an entitlement, you must revoke the entitlement instead. When an entitlement is revoked from a flow, the service automatically removes the associated output. |
| DELETE | /v1/flows/{flowArn}/source/{sourceArn} | Removes a source from an existing flow. This request can be made only if there is more than one source on the flow. |
| DELETE | /v1/flows/{flowArn}/vpcInterfaces/{vpcInterfaceName} | Removes a VPC Interface from an existing flow. This request can be made only on a VPC interface that does not have a Source or Output associated with it. If the VPC interface is referenced by a Source or Output, you must first delete or update the Source or Output to no longer reference the VPC interface. |
| DELETE | /v1/flows/{flowArn}/entitlements/{entitlementArn} | Revokes an entitlement from a flow. Once an entitlement is revoked, the content becomes unavailable to the subscriber and the associated output is removed. |
| POST | /v1/flows/start/{flowArn} | Starts a flow. |
| POST | /v1/flows/stop/{flowArn} | Stops a flow. |
| PUT | /v1/flows/{flowArn} | Updates flow |
| PUT | /v1/flows/{flowArn}/entitlements/{entitlementArn} | You can change an entitlement's description, subscribers, and encryption. If you change the subscribers, the service will remove the outputs that are are used by the subscribers that are removed. |
| PUT | /v1/flows/{flowArn}/mediaStreams/{mediaStreamName} | Updates an existing media stream. |
| PUT | /v1/flows/{flowArn}/outputs/{outputArn} | Updates an existing flow output. |
| PUT | /v1/flows/{flowArn}/source/{sourceArn} | Updates the source of a flow. |

### gateways
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/gateways | Creates a new gateway. The request must include at least one network (up to 4). |
| DELETE | /v1/gateways/{gatewayArn} | Deletes a gateway. Before you can delete a gateway, you must deregister its instances and delete its bridges. |
| GET | /v1/gateways/{gatewayArn} | Displays the details of a gateway. The response includes the gateway ARN, name, and CIDR blocks, as well as details about the networks. |
| GET | /v1/gateways | Displays a list of gateways that are associated with this account. This request returns a paginated result. |

### gateway-instances
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v1/gateway-instances/{gatewayInstanceArn} | Deregisters an instance. Before you deregister an instance, all bridges running on the instance must be stopped. If you want to deregister an instance without stopping the bridges, you must use the --force option. |
| GET | /v1/gateway-instances/{gatewayInstanceArn} | Displays the details of an instance. |
| GET | /v1/gateway-instances | Displays a list of instances associated with the AWS account. This request returns a paginated result. You can use the filterArn property to display only the instances associated with the selected Gateway Amazon Resource Name (ARN). |
| PUT | /v1/gateway-instances/{gatewayInstanceArn} | Updates the configuration of an existing Gateway Instance. |

### offerings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/offerings/{offeringArn} | Displays the details of an offering. The response includes the offering description, duration, outbound bandwidth, price, and Amazon Resource Name (ARN). |
| GET | /v1/offerings | Displays a list of all offerings that are available to this account in the current AWS Region. If you have an active reservation (which means you've purchased an offering that has already started and hasn't expired yet), your account isn't eligible for other offerings. |
| POST | /v1/offerings/{offeringArn} | Submits a request to purchase an offering. If you already have an active reservation, you can't purchase another offering. |

### reservations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/reservations/{reservationArn} | Displays the details of a reservation. The response includes the reservation name, state, start date and time, and the details of the offering that make up the rest of the reservation (such as price, duration, and outbound bandwidth). |
| GET | /v1/reservations | Displays a list of all reservations that have been purchased by this account in the current AWS Region. This list includes all reservations in all states (such as active and expired). |

### entitlements
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/entitlements | Displays a list of all entitlements that have been granted to this account. This request returns 20 results per page. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | List all tags on an AWS Elemental MediaConnect resource |
| POST | /tags/{resourceArn} | Associates the specified tags to a resource with the specified resourceArn. If existing tags on a resource are not specified in the request parameters, they are not changed. When a resource is deleted, the tags associated with that resource are deleted as well. |
| DELETE | /tags/{resourceArn} | Deletes specified tags from a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a output?" -> POST /v1/bridges/{bridgeArn}/outputs
- "Create a source?" -> POST /v1/bridges/{bridgeArn}/sources
- "Create a mediaStream?" -> POST /v1/flows/{flowArn}/mediaStreams
- "Create a output?" -> POST /v1/flows/{flowArn}/outputs
- "Create a source?" -> POST /v1/flows/{flowArn}/source
- "Create a vpcInterface?" -> POST /v1/flows/{flowArn}/vpcInterfaces
- "Create a bridge?" -> POST /v1/bridges
- "Create a flow?" -> POST /v1/flows
- "Create a gateway?" -> POST /v1/gateways
- "Delete a bridge?" -> DELETE /v1/bridges/{bridgeArn}
- "Delete a flow?" -> DELETE /v1/flows/{flowArn}
- "Delete a gateway?" -> DELETE /v1/gateways/{gatewayArn}
- "Delete a gateway-instance?" -> DELETE /v1/gateway-instances/{gatewayInstanceArn}
- "Get bridge details?" -> GET /v1/bridges/{bridgeArn}
- "Get flow details?" -> GET /v1/flows/{flowArn}
- "List all source-metadata?" -> GET /v1/flows/{flowArn}/source-metadata
- "List all source-thumbnail?" -> GET /v1/flows/{flowArn}/source-thumbnail
- "Get gateway details?" -> GET /v1/gateways/{gatewayArn}
- "Get gateway-instance details?" -> GET /v1/gateway-instances/{gatewayInstanceArn}
- "Get offering details?" -> GET /v1/offerings/{offeringArn}
- "Get reservation details?" -> GET /v1/reservations/{reservationArn}
- "Create a entitlement?" -> POST /v1/flows/{flowArn}/entitlements
- "List all bridges?" -> GET /v1/bridges
- "List all entitlements?" -> GET /v1/entitlements
- "List all flows?" -> GET /v1/flows
- "List all gateway-instances?" -> GET /v1/gateway-instances
- "List all gateways?" -> GET /v1/gateways
- "List all offerings?" -> GET /v1/offerings
- "List all reservations?" -> GET /v1/reservations
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a output?" -> DELETE /v1/bridges/{bridgeArn}/outputs/{outputName}
- "Delete a source?" -> DELETE /v1/bridges/{bridgeArn}/sources/{sourceName}
- "Delete a mediaStream?" -> DELETE /v1/flows/{flowArn}/mediaStreams/{mediaStreamName}
- "Delete a output?" -> DELETE /v1/flows/{flowArn}/outputs/{outputArn}
- "Delete a source?" -> DELETE /v1/flows/{flowArn}/source/{sourceArn}
- "Delete a vpcInterface?" -> DELETE /v1/flows/{flowArn}/vpcInterfaces/{vpcInterfaceName}
- "Delete a entitlement?" -> DELETE /v1/flows/{flowArn}/entitlements/{entitlementArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Update a bridge?" -> PUT /v1/bridges/{bridgeArn}
- "Update a output?" -> PUT /v1/bridges/{bridgeArn}/outputs/{outputName}
- "Update a source?" -> PUT /v1/bridges/{bridgeArn}/sources/{sourceName}
- "Update a flow?" -> PUT /v1/flows/{flowArn}
- "Update a entitlement?" -> PUT /v1/flows/{flowArn}/entitlements/{entitlementArn}
- "Update a mediaStream?" -> PUT /v1/flows/{flowArn}/mediaStreams/{mediaStreamName}
- "Update a output?" -> PUT /v1/flows/{flowArn}/outputs/{outputArn}
- "Update a source?" -> PUT /v1/flows/{flowArn}/source/{sourceArn}
- "Update a gateway-instance?" -> PUT /v1/gateway-instances/{gatewayInstanceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
