---
name: aws-elemental-medialive
description: "AWS Elemental MediaLive API skill. Use when working with AWS Elemental MediaLive for prod. Covers 92 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Elemental MediaLive
API version: 2017-10-14

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /prod/accountConfiguration -- verify access
3. POST /prod/inputDevices/{inputDeviceId}/accept -- create first accept

## Endpoints

92 endpoints across 1 groups. See references/api-spec.lap for full details.

### prod
| Method | Path | Description |
|--------|------|-------------|
| POST | /prod/inputDevices/{inputDeviceId}/accept | Accept an incoming input device transfer. The ownership of the device will transfer to your AWS account. |
| POST | /prod/batch/delete | Starts delete of resources. |
| POST | /prod/batch/start | Starts existing resources |
| POST | /prod/batch/stop | Stops running resources |
| PUT | /prod/channels/{channelId}/schedule | Update a channel schedule |
| POST | /prod/inputDevices/{inputDeviceId}/cancel | Cancel an input device transfer that you have requested. |
| POST | /prod/claimDevice | Send a request to claim an AWS Elemental device that you have purchased from a third-party vendor. After the request succeeds, you will own the device. |
| POST | /prod/channels | Creates a new channel |
| POST | /prod/inputs | Create an input |
| POST | /prod/inputSecurityGroups | Creates a Input Security Group |
| POST | /prod/multiplexes | Create a new multiplex. |
| POST | /prod/multiplexes/{multiplexId}/programs | Create a new program in the multiplex. |
| POST | /prod/inputs/{inputId}/partners | Create a partner input |
| POST | /prod/tags/{resource-arn} | Create tags for a resource |
| DELETE | /prod/channels/{channelId} | Starts deletion of channel. The associated outputs are also deleted. |
| DELETE | /prod/inputs/{inputId} | Deletes the input end point |
| DELETE | /prod/inputSecurityGroups/{inputSecurityGroupId} | Deletes an Input Security Group |
| DELETE | /prod/multiplexes/{multiplexId} | Delete a multiplex. The multiplex must be idle. |
| DELETE | /prod/multiplexes/{multiplexId}/programs/{programName} | Delete a program from a multiplex. |
| DELETE | /prod/reservations/{reservationId} | Delete an expired reservation. |
| DELETE | /prod/channels/{channelId}/schedule | Delete all schedule actions on a channel. |
| DELETE | /prod/tags/{resource-arn} | Removes tags for a resource |
| GET | /prod/accountConfiguration | Describe account configuration |
| GET | /prod/channels/{channelId} | Gets details about a channel |
| GET | /prod/inputs/{inputId} | Produces details about an input |
| GET | /prod/inputDevices/{inputDeviceId} | Gets the details for the input device |
| GET | /prod/inputDevices/{inputDeviceId}/thumbnailData | Get the latest thumbnail data for the input device. |
| GET | /prod/inputSecurityGroups/{inputSecurityGroupId} | Produces a summary of an Input Security Group |
| GET | /prod/multiplexes/{multiplexId} | Gets details about a multiplex. |
| GET | /prod/multiplexes/{multiplexId}/programs/{programName} | Get the details for a program in a multiplex. |
| GET | /prod/offerings/{offeringId} | Get details for an offering. |
| GET | /prod/reservations/{reservationId} | Get details for a reservation. |
| GET | /prod/channels/{channelId}/schedule | Get a channel schedule |
| GET | /prod/channels/{channelId}/thumbnails | Describe the latest thumbnails data. |
| GET | /prod/channels | Produces list of channels that have been created |
| GET | /prod/inputDeviceTransfers | List input devices that are currently being transferred. List input devices that you are transferring from your AWS account or input devices that another AWS account is transferring to you. |
| GET | /prod/inputDevices | List input devices |
| GET | /prod/inputSecurityGroups | Produces a list of Input Security Groups for an account |
| GET | /prod/inputs | Produces list of inputs that have been created |
| GET | /prod/multiplexes/{multiplexId}/programs | List the programs that currently exist for a specific multiplex. |
| GET | /prod/multiplexes | Retrieve a list of the existing multiplexes. |
| GET | /prod/offerings | List offerings available for purchase. |
| GET | /prod/reservations | List purchased reservations. |
| GET | /prod/tags/{resource-arn} | Produces list of tags that have been created for a resource |
| POST | /prod/offerings/{offeringId}/purchase | Purchase an offering and create a reservation. |
| POST | /prod/inputDevices/{inputDeviceId}/reboot | Send a reboot command to the specified input device. The device will begin rebooting within a few seconds of sending the command. When the reboot is complete, the device’s connection status will change to connected. |
| POST | /prod/inputDevices/{inputDeviceId}/reject | Reject the transfer of the specified input device to your AWS account. |
| POST | /prod/channels/{channelId}/start | Starts an existing channel |
| POST | /prod/inputDevices/{inputDeviceId}/start | Start an input device that is attached to a MediaConnect flow. (There is no need to start a device that is attached to a MediaLive input; MediaLive starts the device when the channel starts.) |
| POST | /prod/inputDevices/{inputDeviceId}/startInputDeviceMaintenanceWindow | Start a maintenance window for the specified input device. Starting a maintenance window will give the device up to two hours to install software. If the device was streaming prior to the maintenance, it will resume streaming when the software is fully installed. Devices automatically install updates while they are powered on and their MediaLive channels are stopped. A maintenance window allows you to update a device without having to stop MediaLive channels that use the device. The device must remain powered on and connected to the internet for the duration of the maintenance. |
| POST | /prod/multiplexes/{multiplexId}/start | Start (run) the multiplex. Starting the multiplex does not start the channels. You must explicitly start each channel. |
| POST | /prod/channels/{channelId}/stop | Stops a running channel |
| POST | /prod/inputDevices/{inputDeviceId}/stop | Stop an input device that is attached to a MediaConnect flow. (There is no need to stop a device that is attached to a MediaLive input; MediaLive automatically stops the device when the channel stops.) |
| POST | /prod/multiplexes/{multiplexId}/stop | Stops a running multiplex. If the multiplex isn't running, this action has no effect. |
| POST | /prod/inputDevices/{inputDeviceId}/transfer | Start an input device transfer to another AWS account. After you make the request, the other account must accept or reject the transfer. |
| PUT | /prod/accountConfiguration | Update account configuration |
| PUT | /prod/channels/{channelId} | Updates a channel. |
| PUT | /prod/channels/{channelId}/channelClass | Changes the class of the channel. |
| PUT | /prod/inputs/{inputId} | Updates an input. |
| PUT | /prod/inputDevices/{inputDeviceId} | Updates the parameters for the input device. |
| PUT | /prod/inputSecurityGroups/{inputSecurityGroupId} | Update an Input Security Group's Whilelists. |
| PUT | /prod/multiplexes/{multiplexId} | Updates a multiplex. |
| PUT | /prod/multiplexes/{multiplexId}/programs/{programName} | Update a program in a multiplex. |
| PUT | /prod/reservations/{reservationId} | Update reservation. |
| POST | /prod/channels/{channelId}/restartChannelPipelines | Restart pipelines in one channel that is currently running. |
| POST | /prod/cloudwatch-alarm-templates | Creates a cloudwatch alarm template to dynamically generate cloudwatch metric alarms on targeted resource types. |
| POST | /prod/cloudwatch-alarm-template-groups | Creates a cloudwatch alarm template group to group your cloudwatch alarm templates and to attach to signal maps for dynamically creating alarms. |
| POST | /prod/eventbridge-rule-templates | Creates an eventbridge rule template to monitor events and send notifications to your targeted resources. |
| POST | /prod/eventbridge-rule-template-groups | Creates an eventbridge rule template group to group your eventbridge rule templates and to attach to signal maps for dynamically creating notification rules. |
| POST | /prod/signal-maps | Initiates the creation of a new signal map. Will discover a new mediaResourceMap based on the provided discoveryEntryPointArn. |
| DELETE | /prod/cloudwatch-alarm-templates/{identifier} | Deletes a cloudwatch alarm template. |
| DELETE | /prod/cloudwatch-alarm-template-groups/{identifier} | Deletes a cloudwatch alarm template group. You must detach this group from all signal maps and ensure its existing templates are moved to another group or deleted. |
| DELETE | /prod/eventbridge-rule-templates/{identifier} | Deletes an eventbridge rule template. |
| DELETE | /prod/eventbridge-rule-template-groups/{identifier} | Deletes an eventbridge rule template group. You must detach this group from all signal maps and ensure its existing templates are moved to another group or deleted. |
| DELETE | /prod/signal-maps/{identifier} | Deletes the specified signal map. |
| GET | /prod/cloudwatch-alarm-templates/{identifier} | Retrieves the specified cloudwatch alarm template. |
| GET | /prod/cloudwatch-alarm-template-groups/{identifier} | Retrieves the specified cloudwatch alarm template group. |
| GET | /prod/eventbridge-rule-templates/{identifier} | Retrieves the specified eventbridge rule template. |
| GET | /prod/eventbridge-rule-template-groups/{identifier} | Retrieves the specified eventbridge rule template group. |
| GET | /prod/signal-maps/{identifier} | Retrieves the specified signal map. |
| GET | /prod/cloudwatch-alarm-template-groups | Lists cloudwatch alarm template groups. |
| GET | /prod/cloudwatch-alarm-templates | Lists cloudwatch alarm templates. |
| GET | /prod/eventbridge-rule-template-groups | Lists eventbridge rule template groups. |
| GET | /prod/eventbridge-rule-templates | Lists eventbridge rule templates. |
| GET | /prod/signal-maps | Lists signal maps. |
| DELETE | /prod/signal-maps/{identifier}/monitor-deployment | Initiates a deployment to delete the monitor of the specified signal map. |
| POST | /prod/signal-maps/{identifier}/monitor-deployment | Initiates a deployment to deploy the latest monitor of the specified signal map. |
| PATCH | /prod/signal-maps/{identifier} | Initiates an update for the specified signal map. Will discover a new signal map if a changed discoveryEntryPointArn is provided. |
| PATCH | /prod/cloudwatch-alarm-templates/{identifier} | Updates the specified cloudwatch alarm template. |
| PATCH | /prod/cloudwatch-alarm-template-groups/{identifier} | Updates the specified cloudwatch alarm template group. |
| PATCH | /prod/eventbridge-rule-templates/{identifier} | Updates the specified eventbridge rule template. |
| PATCH | /prod/eventbridge-rule-template-groups/{identifier} | Updates the specified eventbridge rule template group. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a accept?" -> POST /prod/inputDevices/{inputDeviceId}/accept
- "Create a delete?" -> POST /prod/batch/delete
- "Create a start?" -> POST /prod/batch/start
- "Create a stop?" -> POST /prod/batch/stop
- "Create a cancel?" -> POST /prod/inputDevices/{inputDeviceId}/cancel
- "Create a claimDevice?" -> POST /prod/claimDevice
- "Create a channel?" -> POST /prod/channels
- "Create a input?" -> POST /prod/inputs
- "Create a inputSecurityGroup?" -> POST /prod/inputSecurityGroups
- "Create a multiplexe?" -> POST /prod/multiplexes
- "Create a program?" -> POST /prod/multiplexes/{multiplexId}/programs
- "Create a partner?" -> POST /prod/inputs/{inputId}/partners
- "Delete a channel?" -> DELETE /prod/channels/{channelId}
- "Delete a input?" -> DELETE /prod/inputs/{inputId}
- "Delete a inputSecurityGroup?" -> DELETE /prod/inputSecurityGroups/{inputSecurityGroupId}
- "Delete a multiplexe?" -> DELETE /prod/multiplexes/{multiplexId}
- "Delete a program?" -> DELETE /prod/multiplexes/{multiplexId}/programs/{programName}
- "Delete a reservation?" -> DELETE /prod/reservations/{reservationId}
- "Delete a tag?" -> DELETE /prod/tags/{resource-arn}
- "List all accountConfiguration?" -> GET /prod/accountConfiguration
- "Get channel details?" -> GET /prod/channels/{channelId}
- "Get input details?" -> GET /prod/inputs/{inputId}
- "Get inputDevice details?" -> GET /prod/inputDevices/{inputDeviceId}
- "List all thumbnailData?" -> GET /prod/inputDevices/{inputDeviceId}/thumbnailData
- "Get inputSecurityGroup details?" -> GET /prod/inputSecurityGroups/{inputSecurityGroupId}
- "Get multiplexe details?" -> GET /prod/multiplexes/{multiplexId}
- "Get program details?" -> GET /prod/multiplexes/{multiplexId}/programs/{programName}
- "Get offering details?" -> GET /prod/offerings/{offeringId}
- "Get reservation details?" -> GET /prod/reservations/{reservationId}
- "List all schedule?" -> GET /prod/channels/{channelId}/schedule
- "List all thumbnails?" -> GET /prod/channels/{channelId}/thumbnails
- "List all channels?" -> GET /prod/channels
- "List all inputDeviceTransfers?" -> GET /prod/inputDeviceTransfers
- "List all inputDevices?" -> GET /prod/inputDevices
- "List all inputSecurityGroups?" -> GET /prod/inputSecurityGroups
- "List all inputs?" -> GET /prod/inputs
- "List all programs?" -> GET /prod/multiplexes/{multiplexId}/programs
- "List all multiplexes?" -> GET /prod/multiplexes
- "List all offerings?" -> GET /prod/offerings
- "List all reservations?" -> GET /prod/reservations
- "Get tag details?" -> GET /prod/tags/{resource-arn}
- "Create a purchase?" -> POST /prod/offerings/{offeringId}/purchase
- "Create a reboot?" -> POST /prod/inputDevices/{inputDeviceId}/reboot
- "Create a reject?" -> POST /prod/inputDevices/{inputDeviceId}/reject
- "Create a start?" -> POST /prod/channels/{channelId}/start
- "Create a start?" -> POST /prod/inputDevices/{inputDeviceId}/start
- "Create a startInputDeviceMaintenanceWindow?" -> POST /prod/inputDevices/{inputDeviceId}/startInputDeviceMaintenanceWindow
- "Create a start?" -> POST /prod/multiplexes/{multiplexId}/start
- "Create a stop?" -> POST /prod/channels/{channelId}/stop
- "Create a stop?" -> POST /prod/inputDevices/{inputDeviceId}/stop
- "Create a stop?" -> POST /prod/multiplexes/{multiplexId}/stop
- "Create a transfer?" -> POST /prod/inputDevices/{inputDeviceId}/transfer
- "Update a channel?" -> PUT /prod/channels/{channelId}
- "Update a input?" -> PUT /prod/inputs/{inputId}
- "Update a inputDevice?" -> PUT /prod/inputDevices/{inputDeviceId}
- "Update a inputSecurityGroup?" -> PUT /prod/inputSecurityGroups/{inputSecurityGroupId}
- "Update a multiplexe?" -> PUT /prod/multiplexes/{multiplexId}
- "Update a program?" -> PUT /prod/multiplexes/{multiplexId}/programs/{programName}
- "Update a reservation?" -> PUT /prod/reservations/{reservationId}
- "Create a restartChannelPipeline?" -> POST /prod/channels/{channelId}/restartChannelPipelines
- "Create a cloudwatch-alarm-template?" -> POST /prod/cloudwatch-alarm-templates
- "Create a cloudwatch-alarm-template-group?" -> POST /prod/cloudwatch-alarm-template-groups
- "Create a eventbridge-rule-template?" -> POST /prod/eventbridge-rule-templates
- "Create a eventbridge-rule-template-group?" -> POST /prod/eventbridge-rule-template-groups
- "Create a signal-map?" -> POST /prod/signal-maps
- "Delete a cloudwatch-alarm-template?" -> DELETE /prod/cloudwatch-alarm-templates/{identifier}
- "Delete a cloudwatch-alarm-template-group?" -> DELETE /prod/cloudwatch-alarm-template-groups/{identifier}
- "Delete a eventbridge-rule-template?" -> DELETE /prod/eventbridge-rule-templates/{identifier}
- "Delete a eventbridge-rule-template-group?" -> DELETE /prod/eventbridge-rule-template-groups/{identifier}
- "Delete a signal-map?" -> DELETE /prod/signal-maps/{identifier}
- "Get cloudwatch-alarm-template details?" -> GET /prod/cloudwatch-alarm-templates/{identifier}
- "Get cloudwatch-alarm-template-group details?" -> GET /prod/cloudwatch-alarm-template-groups/{identifier}
- "Get eventbridge-rule-template details?" -> GET /prod/eventbridge-rule-templates/{identifier}
- "Get eventbridge-rule-template-group details?" -> GET /prod/eventbridge-rule-template-groups/{identifier}
- "Get signal-map details?" -> GET /prod/signal-maps/{identifier}
- "List all cloudwatch-alarm-template-groups?" -> GET /prod/cloudwatch-alarm-template-groups
- "List all cloudwatch-alarm-templates?" -> GET /prod/cloudwatch-alarm-templates
- "List all eventbridge-rule-template-groups?" -> GET /prod/eventbridge-rule-template-groups
- "List all eventbridge-rule-templates?" -> GET /prod/eventbridge-rule-templates
- "List all signal-maps?" -> GET /prod/signal-maps
- "Create a monitor-deployment?" -> POST /prod/signal-maps/{identifier}/monitor-deployment
- "Partially update a signal-map?" -> PATCH /prod/signal-maps/{identifier}
- "Partially update a cloudwatch-alarm-template?" -> PATCH /prod/cloudwatch-alarm-templates/{identifier}
- "Partially update a cloudwatch-alarm-template-group?" -> PATCH /prod/cloudwatch-alarm-template-groups/{identifier}
- "Partially update a eventbridge-rule-template?" -> PATCH /prod/eventbridge-rule-templates/{identifier}
- "Partially update a eventbridge-rule-template-group?" -> PATCH /prod/eventbridge-rule-template-groups/{identifier}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
