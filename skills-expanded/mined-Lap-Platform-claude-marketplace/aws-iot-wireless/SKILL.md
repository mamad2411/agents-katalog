---
name: aws-iot-wireless
description: "AWS IoT Wireless API skill. Use when working with AWS IoT Wireless for partner-accounts, fuota-tasks, multicast-groups. Covers 112 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Wireless
API version: 2020-11-22

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /event-configurations-resource-types -- verify access
3. POST /partner-accounts -- create first partner-accounts

## Endpoints

112 endpoints across 24 groups. See references/api-spec.lap for full details.

### partner-accounts
| Method | Path | Description |
|--------|------|-------------|
| POST | /partner-accounts | Associates a partner account with your AWS account. |
| DELETE | /partner-accounts/{PartnerAccountId} | Disassociates your AWS account from a partner account. If PartnerAccountId and PartnerType are null, disassociates your AWS account from all partner accounts. |
| GET | /partner-accounts/{PartnerAccountId} | Gets information about a partner account. If PartnerAccountId and PartnerType are null, returns all partner accounts. |
| GET | /partner-accounts | Lists the partner accounts associated with your AWS account. |
| PATCH | /partner-accounts/{PartnerAccountId} | Updates properties of a partner account. |

### fuota-tasks
| Method | Path | Description |
|--------|------|-------------|
| PUT | /fuota-tasks/{Id}/multicast-group | Associate a multicast group with a FUOTA task. |
| PUT | /fuota-tasks/{Id}/wireless-device | Associate a wireless device with a FUOTA task. |
| POST | /fuota-tasks | Creates a FUOTA task. |
| DELETE | /fuota-tasks/{Id} | Deletes a FUOTA task. |
| DELETE | /fuota-tasks/{Id}/multicast-groups/{MulticastGroupId} | Disassociates a multicast group from a fuota task. |
| DELETE | /fuota-tasks/{Id}/wireless-devices/{WirelessDeviceId} | Disassociates a wireless device from a FUOTA task. |
| GET | /fuota-tasks/{Id} | Gets information about a FUOTA task. |
| GET | /fuota-tasks | Lists the FUOTA tasks registered to your AWS account. |
| GET | /fuota-tasks/{Id}/multicast-groups | List all multicast groups associated with a fuota task. |
| PUT | /fuota-tasks/{Id} | Starts a FUOTA task. |
| PATCH | /fuota-tasks/{Id} | Updates properties of a FUOTA task. |

### multicast-groups
| Method | Path | Description |
|--------|------|-------------|
| PUT | /multicast-groups/{Id}/wireless-device | Associates a wireless device with a multicast group. |
| DELETE | /multicast-groups/{Id}/session | Cancels an existing multicast group session. |
| POST | /multicast-groups | Creates a multicast group. |
| DELETE | /multicast-groups/{Id} | Deletes a multicast group if it is not in use by a fuota task. |
| DELETE | /multicast-groups/{Id}/wireless-devices/{WirelessDeviceId} | Disassociates a wireless device from a multicast group. |
| GET | /multicast-groups/{Id} | Gets information about a multicast group. |
| GET | /multicast-groups/{Id}/session | Gets information about a multicast group session. |
| GET | /multicast-groups | Lists the multicast groups registered to your AWS account. |
| POST | /multicast-groups/{Id}/data | Sends the specified data to a multicast group. |
| PATCH | /multicast-groups/{Id}/bulk | Starts a bulk association of all qualifying wireless devices with a multicast group. |
| POST | /multicast-groups/{Id}/bulk | Starts a bulk disassociatin of all qualifying wireless devices from a multicast group. |
| PUT | /multicast-groups/{Id}/session | Starts a multicast group session. |
| PATCH | /multicast-groups/{Id} | Updates properties of a multicast group session. |

### wireless-devices
| Method | Path | Description |
|--------|------|-------------|
| PUT | /wireless-devices/{Id}/thing | Associates a wireless device with a thing. |
| POST | /wireless-devices | Provisions a wireless device. |
| DELETE | /wireless-devices/{Id}/data | Remove queued messages from the downlink queue. |
| DELETE | /wireless-devices/{Id} | Deletes a wireless device. |
| PATCH | /wireless-devices/{Identifier}/deregister | Deregister a wireless device from AWS IoT Wireless. |
| DELETE | /wireless-devices/{Id}/thing | Disassociates a wireless device from its currently associated thing. |
| GET | /wireless-devices/{Identifier} | Gets information about a wireless device. |
| GET | /wireless-devices/{Id}/statistics | Gets operating information about a wireless device. |
| GET | /wireless-devices/{Id}/data | List queued messages in the downlink queue. |
| GET | /wireless-devices | Lists the wireless devices registered to your AWS account. |
| POST | /wireless-devices/{Id}/data | Sends a decrypted application data frame to a device. |
| POST | /wireless-devices/{Id}/test | Simulates a provisioned device by sending an uplink data payload of Hello. |
| PATCH | /wireless-devices/{Id} | Updates properties of a wireless device. |

### wireless-gateways
| Method | Path | Description |
|--------|------|-------------|
| PUT | /wireless-gateways/{Id}/certificate | Associates a wireless gateway with a certificate. |
| PUT | /wireless-gateways/{Id}/thing | Associates a wireless gateway with a thing. |
| POST | /wireless-gateways | Provisions a wireless gateway.  When provisioning a wireless gateway, you might run into duplication errors for the following reasons.   If you specify a GatewayEui value that already exists.   If you used a ClientRequestToken with the same parameters within the last 10 minutes.   To avoid this error, make sure that you use unique identifiers and parameters for each request within the specified time period. |
| POST | /wireless-gateways/{Id}/tasks | Creates a task for a wireless gateway. |
| DELETE | /wireless-gateways/{Id} | Deletes a wireless gateway.  When deleting a wireless gateway, you might run into duplication errors for the following reasons.   If you specify a GatewayEui value that already exists.   If you used a ClientRequestToken with the same parameters within the last 10 minutes.   To avoid this error, make sure that you use unique identifiers and parameters for each request within the specified time period. |
| DELETE | /wireless-gateways/{Id}/tasks | Deletes a wireless gateway task. |
| DELETE | /wireless-gateways/{Id}/certificate | Disassociates a wireless gateway from its currently associated certificate. |
| DELETE | /wireless-gateways/{Id}/thing | Disassociates a wireless gateway from its currently associated thing. |
| GET | /wireless-gateways/{Identifier} | Gets information about a wireless gateway. |
| GET | /wireless-gateways/{Id}/certificate | Gets the ID of the certificate that is currently associated with a wireless gateway. |
| GET | /wireless-gateways/{Id}/firmware-information | Gets the firmware version and other information about a wireless gateway. |
| GET | /wireless-gateways/{Id}/statistics | Gets operating information about a wireless gateway. |
| GET | /wireless-gateways/{Id}/tasks | Gets information about a wireless gateway task. |
| GET | /wireless-gateways | Lists the wireless gateways registered to your AWS account. |
| PATCH | /wireless-gateways/{Id} | Updates properties of a wireless gateway. |

### destinations
| Method | Path | Description |
|--------|------|-------------|
| POST | /destinations | Creates a new destination that maps a device message to an AWS IoT rule. |
| DELETE | /destinations/{Name} | Deletes a destination. |
| GET | /destinations/{Name} | Gets information about a destination. |
| GET | /destinations | Lists the destinations registered to your AWS account. |
| PATCH | /destinations/{Name} | Updates properties of a destination. |

### device-profiles
| Method | Path | Description |
|--------|------|-------------|
| POST | /device-profiles | Creates a new device profile. |
| DELETE | /device-profiles/{Id} | Deletes a device profile. |
| GET | /device-profiles/{Id} | Gets information about a device profile. |
| GET | /device-profiles | Lists the device profiles registered to your AWS account. |

### network-analyzer-configurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /network-analyzer-configurations | Creates a new network analyzer configuration. |
| DELETE | /network-analyzer-configurations/{ConfigurationName} | Deletes a network analyzer configuration. |
| GET | /network-analyzer-configurations/{ConfigurationName} | Get network analyzer configuration. |
| GET | /network-analyzer-configurations | Lists the network analyzer configurations. |
| PATCH | /network-analyzer-configurations/{ConfigurationName} | Update network analyzer configuration. |

### service-profiles
| Method | Path | Description |
|--------|------|-------------|
| POST | /service-profiles | Creates a new service profile. |
| DELETE | /service-profiles/{Id} | Deletes a service profile. |
| GET | /service-profiles/{Id} | Gets information about a service profile. |
| GET | /service-profiles | Lists the service profiles registered to your AWS account. |

### wireless-gateway-task-definitions
| Method | Path | Description |
|--------|------|-------------|
| POST | /wireless-gateway-task-definitions | Creates a gateway task definition. |
| DELETE | /wireless-gateway-task-definitions/{Id} | Deletes a wireless gateway task definition. Deleting this task definition does not affect tasks that are currently in progress. |
| GET | /wireless-gateway-task-definitions/{Id} | Gets information about a wireless gateway task definition. |
| GET | /wireless-gateway-task-definitions | List the wireless gateway tasks definitions registered to your AWS account. |

### wireless_device_import_task
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /wireless_device_import_task/{Id} | Delete an import task. |
| GET | /wireless_device_import_task/{Id} | Get information about an import task and count of device onboarding summary information for the import task. |
| GET | /wireless_device_import_task | List the Sidewalk devices in an import task and their onboarding status. |
| POST | /wireless_device_import_task | Start import task for provisioning Sidewalk devices in bulk using an S3 CSV file. |
| PATCH | /wireless_device_import_task/{Id} | Update an import task to add more devices to the task. |

### event-configurations-resource-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /event-configurations-resource-types | Get the event configuration based on resource types. |
| PATCH | /event-configurations-resource-types | Update the event configuration based on resource types. |

### log-levels
| Method | Path | Description |
|--------|------|-------------|
| GET | /log-levels | Returns current default log levels or log levels by resource types. Based on resource types, log levels can be for wireless device log options or wireless gateway log options. |
| GET | /log-levels/{ResourceIdentifier} | Fetches the log-level override, if any, for a given resource-ID and resource-type. It can be used for a wireless device or a wireless gateway. |
| PUT | /log-levels/{ResourceIdentifier} | Sets the log-level override for a resource-ID and resource-type. This option can be specified for a wireless gateway or a wireless device. A limit of 200 log level override can be set per account. |
| DELETE | /log-levels | Removes the log-level overrides for all resources; both wireless devices and wireless gateways. |
| DELETE | /log-levels/{ResourceIdentifier} | Removes the log-level override, if any, for a specific resource-ID and resource-type. It can be used for a wireless device or a wireless gateway. |
| POST | /log-levels | Set default log level, or log levels by resource types. This can be for wireless device log options or wireless gateways log options and is used to control the log messages that'll be displayed in CloudWatch. |

### metric-configuration
| Method | Path | Description |
|--------|------|-------------|
| GET | /metric-configuration | Get the metric configuration status for this AWS account. |
| PUT | /metric-configuration | Update the summary metric configuration. |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| POST | /metrics | Get the summary metrics for this AWS account. |

### positions
| Method | Path | Description |
|--------|------|-------------|
| GET | /positions/{ResourceIdentifier} | Get the position information for a given resource.  This action is no longer supported. Calls to retrieve the position information should use the GetResourcePosition API operation instead. |
| PATCH | /positions/{ResourceIdentifier} | Update the position information of a resource.  This action is no longer supported. Calls to update the position information should use the UpdateResourcePosition API operation instead. |

### position-configurations
| Method | Path | Description |
|--------|------|-------------|
| GET | /position-configurations/{ResourceIdentifier} | Get position configuration for a given resource.  This action is no longer supported. Calls to retrieve the position configuration should use the GetResourcePosition API operation instead. |
| GET | /position-configurations | List position configurations for a given resource, such as positioning solvers.  This action is no longer supported. Calls to retrieve position information should use the GetResourcePosition API operation instead. |
| PUT | /position-configurations/{ResourceIdentifier} | Put position configuration for a given resource.  This action is no longer supported. Calls to update the position configuration should use the UpdateResourcePosition API operation instead. |

### position-estimate
| Method | Path | Description |
|--------|------|-------------|
| POST | /position-estimate | Get estimated position information as a payload in GeoJSON format. The payload measurement data is resolved using solvers that are provided by third-party vendors. |

### event-configurations
| Method | Path | Description |
|--------|------|-------------|
| GET | /event-configurations/{Identifier} | Get the event configuration for a particular resource identifier. |
| GET | /event-configurations | List event configurations where at least one event topic has been enabled. |
| PATCH | /event-configurations/{Identifier} | Update the event configuration for a particular resource identifier. |

### resource-positions
| Method | Path | Description |
|--------|------|-------------|
| GET | /resource-positions/{ResourceIdentifier} | Get the position information for a given wireless device or a wireless gateway resource. The position information uses the  World Geodetic System (WGS84). |
| PATCH | /resource-positions/{ResourceIdentifier} | Update the position information of a given wireless device or a wireless gateway resource. The position coordinates are based on the  World Geodetic System (WGS84). |

### service-endpoint
| Method | Path | Description |
|--------|------|-------------|
| GET | /service-endpoint | Gets the account-specific endpoint for Configuration and Update Server (CUPS) protocol or LoRaWAN Network Server (LNS) connections. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | Lists the tags (metadata) you have assigned to the resource. |
| POST | /tags | Adds a tag to a resource. |
| DELETE | /tags | Removes one or more tags from a resource. |

### wireless_device_import_tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /wireless_device_import_tasks | List wireless devices that have been added to an import task. |

### wireless_single_device_import_task
| Method | Path | Description |
|--------|------|-------------|
| POST | /wireless_single_device_import_task | Start import task for a single wireless device. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a partner-account?" -> POST /partner-accounts
- "Create a destination?" -> POST /destinations
- "Create a device-profile?" -> POST /device-profiles
- "Create a fuota-task?" -> POST /fuota-tasks
- "Create a multicast-group?" -> POST /multicast-groups
- "Create a network-analyzer-configuration?" -> POST /network-analyzer-configurations
- "Create a service-profile?" -> POST /service-profiles
- "Create a wireless-device?" -> POST /wireless-devices
- "Create a wireless-gateway?" -> POST /wireless-gateways
- "Create a task?" -> POST /wireless-gateways/{Id}/tasks
- "Create a wireless-gateway-task-definition?" -> POST /wireless-gateway-task-definitions
- "Delete a destination?" -> DELETE /destinations/{Name}
- "Delete a device-profile?" -> DELETE /device-profiles/{Id}
- "Delete a fuota-task?" -> DELETE /fuota-tasks/{Id}
- "Delete a multicast-group?" -> DELETE /multicast-groups/{Id}
- "Delete a network-analyzer-configuration?" -> DELETE /network-analyzer-configurations/{ConfigurationName}
- "Delete a service-profile?" -> DELETE /service-profiles/{Id}
- "Delete a wireless-device?" -> DELETE /wireless-devices/{Id}
- "Delete a wireless_device_import_task?" -> DELETE /wireless_device_import_task/{Id}
- "Delete a wireless-gateway?" -> DELETE /wireless-gateways/{Id}
- "Delete a wireless-gateway-task-definition?" -> DELETE /wireless-gateway-task-definitions/{Id}
- "Delete a partner-account?" -> DELETE /partner-accounts/{PartnerAccountId}
- "Delete a multicast-group?" -> DELETE /fuota-tasks/{Id}/multicast-groups/{MulticastGroupId}
- "Delete a wireless-device?" -> DELETE /fuota-tasks/{Id}/wireless-devices/{WirelessDeviceId}
- "Delete a wireless-device?" -> DELETE /multicast-groups/{Id}/wireless-devices/{WirelessDeviceId}
- "Get destination details?" -> GET /destinations/{Name}
- "Get device-profile details?" -> GET /device-profiles/{Id}
- "List all event-configurations-resource-types?" -> GET /event-configurations-resource-types
- "Get fuota-task details?" -> GET /fuota-tasks/{Id}
- "List all log-levels?" -> GET /log-levels
- "List all metric-configuration?" -> GET /metric-configuration
- "Create a metric?" -> POST /metrics
- "Get multicast-group details?" -> GET /multicast-groups/{Id}
- "List all session?" -> GET /multicast-groups/{Id}/session
- "Get network-analyzer-configuration details?" -> GET /network-analyzer-configurations/{ConfigurationName}
- "Get partner-account details?" -> GET /partner-accounts/{PartnerAccountId}
- "Get position details?" -> GET /positions/{ResourceIdentifier}
- "Get position-configuration details?" -> GET /position-configurations/{ResourceIdentifier}
- "Create a position-estimate?" -> POST /position-estimate
- "Get event-configuration details?" -> GET /event-configurations/{Identifier}
- "Get log-level details?" -> GET /log-levels/{ResourceIdentifier}
- "Get resource-position details?" -> GET /resource-positions/{ResourceIdentifier}
- "List all service-endpoint?" -> GET /service-endpoint
- "Get service-profile details?" -> GET /service-profiles/{Id}
- "Get wireless-device details?" -> GET /wireless-devices/{Identifier}
- "Get wireless_device_import_task details?" -> GET /wireless_device_import_task/{Id}
- "List all statistics?" -> GET /wireless-devices/{Id}/statistics
- "Get wireless-gateway details?" -> GET /wireless-gateways/{Identifier}
- "List all certificate?" -> GET /wireless-gateways/{Id}/certificate
- "List all firmware-information?" -> GET /wireless-gateways/{Id}/firmware-information
- "List all statistics?" -> GET /wireless-gateways/{Id}/statistics
- "List all tasks?" -> GET /wireless-gateways/{Id}/tasks
- "Get wireless-gateway-task-definition details?" -> GET /wireless-gateway-task-definitions/{Id}
- "List all destinations?" -> GET /destinations
- "List all device-profiles?" -> GET /device-profiles
- "List all wireless_device_import_task?" -> GET /wireless_device_import_task
- "List all event-configurations?" -> GET /event-configurations
- "List all fuota-tasks?" -> GET /fuota-tasks
- "List all multicast-groups?" -> GET /multicast-groups
- "List all multicast-groups?" -> GET /fuota-tasks/{Id}/multicast-groups
- "List all network-analyzer-configurations?" -> GET /network-analyzer-configurations
- "List all partner-accounts?" -> GET /partner-accounts
- "List all position-configurations?" -> GET /position-configurations
- "List all data?" -> GET /wireless-devices/{Id}/data
- "List all service-profiles?" -> GET /service-profiles
- "List all tags?" -> GET /tags
- "List all wireless_device_import_tasks?" -> GET /wireless_device_import_tasks
- "List all wireless-devices?" -> GET /wireless-devices
- "List all wireless-gateway-task-definitions?" -> GET /wireless-gateway-task-definitions
- "List all wireless-gateways?" -> GET /wireless-gateways
- "Update a position-configuration?" -> PUT /position-configurations/{ResourceIdentifier}
- "Update a log-level?" -> PUT /log-levels/{ResourceIdentifier}
- "Delete a log-level?" -> DELETE /log-levels/{ResourceIdentifier}
- "Create a data?" -> POST /multicast-groups/{Id}/data
- "Create a data?" -> POST /wireless-devices/{Id}/data
- "Create a bulk?" -> POST /multicast-groups/{Id}/bulk
- "Update a fuota-task?" -> PUT /fuota-tasks/{Id}
- "Create a wireless_single_device_import_task?" -> POST /wireless_single_device_import_task
- "Create a wireless_device_import_task?" -> POST /wireless_device_import_task
- "Create a tag?" -> POST /tags
- "Create a test?" -> POST /wireless-devices/{Id}/test
- "Partially update a destination?" -> PATCH /destinations/{Name}
- "Partially update a fuota-task?" -> PATCH /fuota-tasks/{Id}
- "Create a log-level?" -> POST /log-levels
- "Partially update a multicast-group?" -> PATCH /multicast-groups/{Id}
- "Partially update a network-analyzer-configuration?" -> PATCH /network-analyzer-configurations/{ConfigurationName}
- "Partially update a partner-account?" -> PATCH /partner-accounts/{PartnerAccountId}
- "Partially update a position?" -> PATCH /positions/{ResourceIdentifier}
- "Partially update a event-configuration?" -> PATCH /event-configurations/{Identifier}
- "Partially update a resource-position?" -> PATCH /resource-positions/{ResourceIdentifier}
- "Partially update a wireless-device?" -> PATCH /wireless-devices/{Id}
- "Partially update a wireless_device_import_task?" -> PATCH /wireless_device_import_task/{Id}
- "Partially update a wireless-gateway?" -> PATCH /wireless-gateways/{Id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
