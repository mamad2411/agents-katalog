---
name: aws-iot-greengrass-v2
description: "AWS IoT Greengrass V2 API skill. Use when working with AWS IoT Greengrass V2 for greengrass, tags. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Greengrass V2
API version: 2020-11-30

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /greengrass/servicerole -- verify access
3. POST /greengrass/v2/coreDevices/{coreDeviceThingName}/associateClientDevices -- create first associateClientDevices

## Endpoints

29 endpoints across 2 groups. See references/api-spec.lap for full details.

### greengrass
| Method | Path | Description |
|--------|------|-------------|
| PUT | /greengrass/servicerole | Associates a Greengrass service role with IoT Greengrass for your Amazon Web Services account in this Amazon Web Services Region. IoT Greengrass uses this role to verify the identity of client devices and manage core device connectivity information. The role must include the AWSGreengrassResourceAccessRolePolicy managed policy or a custom policy that defines equivalent permissions for the IoT Greengrass features that you use. For more information, see Greengrass service role in the IoT Greengrass Version 2 Developer Guide. |
| POST | /greengrass/v2/coreDevices/{coreDeviceThingName}/associateClientDevices | Associates a list of client devices with a core device. Use this API operation to specify which client devices can discover a core device through cloud discovery. With cloud discovery, client devices connect to IoT Greengrass to retrieve associated core devices' connectivity information and certificates. For more information, see Configure cloud discovery in the IoT Greengrass V2 Developer Guide.  Client devices are local IoT devices that connect to and communicate with an IoT Greengrass core device over MQTT. You can connect client devices to a core device to sync MQTT messages and data to Amazon Web Services IoT Core and interact with client devices in Greengrass components. For more information, see Interact with local IoT devices in the IoT Greengrass V2 Developer Guide. |
| POST | /greengrass/v2/coreDevices/{coreDeviceThingName}/disassociateClientDevices | Disassociates a list of client devices from a core device. After you disassociate a client device from a core device, the client device won't be able to use cloud discovery to retrieve the core device's connectivity information and certificates. |
| POST | /greengrass/v2/deployments/{deploymentId}/cancel | Cancels a deployment. This operation cancels the deployment for devices that haven't yet received it. If a device already received the deployment, this operation doesn't change anything for that device. |
| POST | /greengrass/v2/createComponentVersion | Creates a component. Components are software that run on Greengrass core devices. After you develop and test a component on your core device, you can use this operation to upload your component to IoT Greengrass. Then, you can deploy the component to other core devices. You can use this operation to do the following:    Create components from recipes  Create a component from a recipe, which is a file that defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform capability. For more information, see IoT Greengrass component recipe reference in the IoT Greengrass V2 Developer Guide. To create a component from a recipe, specify inlineRecipe when you call this operation.    Create components from Lambda functions  Create a component from an Lambda function that runs on IoT Greengrass. This creates a recipe and artifacts from the Lambda function's deployment package. You can use this operation to migrate Lambda functions from IoT Greengrass V1 to IoT Greengrass V2. This function accepts Lambda functions in all supported versions of Python, Node.js, and Java runtimes. IoT Greengrass doesn't apply any additional restrictions on deprecated Lambda runtime versions. To create a component from a Lambda function, specify lambdaFunction when you call this operation.  IoT Greengrass currently supports Lambda functions on only Linux core devices. |
| POST | /greengrass/v2/deployments | Creates a continuous deployment for a target, which is a Greengrass core device or group of core devices. When you add a new core device to a group of core devices that has a deployment, IoT Greengrass deploys that group's deployment to the new device. You can define one deployment for each target. When you create a new deployment for a target that has an existing deployment, you replace the previous deployment. IoT Greengrass applies the new deployment to the target devices. Every deployment has a revision number that indicates how many deployment revisions you define for a target. Use this operation to create a new revision of an existing deployment. For more information, see the Create deployments in the IoT Greengrass V2 Developer Guide. |
| DELETE | /greengrass/v2/components/{arn} | Deletes a version of a component from IoT Greengrass.  This operation deletes the component's recipe and artifacts. As a result, deployments that refer to this component version will fail. If you have deployments that use this component version, you can remove the component from the deployment or update the deployment to use a valid version. |
| DELETE | /greengrass/v2/coreDevices/{coreDeviceThingName} | Deletes a Greengrass core device, which is an IoT thing. This operation removes the core device from the list of core devices. This operation doesn't delete the IoT thing. For more information about how to delete the IoT thing, see DeleteThing in the IoT API Reference. |
| DELETE | /greengrass/v2/deployments/{deploymentId} | Deletes a deployment. To delete an active deployment, you must first cancel it. For more information, see CancelDeployment. Deleting a deployment doesn't affect core devices that run that deployment, because core devices store the deployment's configuration on the device. Additionally, core devices can roll back to a previous deployment that has been deleted. |
| GET | /greengrass/v2/components/{arn}/metadata | Retrieves metadata for a version of a component. |
| DELETE | /greengrass/servicerole | Disassociates the Greengrass service role from IoT Greengrass for your Amazon Web Services account in this Amazon Web Services Region. Without a service role, IoT Greengrass can't verify the identity of client devices or manage core device connectivity information. For more information, see Greengrass service role in the IoT Greengrass Version 2 Developer Guide. |
| GET | /greengrass/v2/components/{arn} | Gets the recipe for a version of a component. |
| GET | /greengrass/v2/components/{arn}/artifacts/{artifactName+} | Gets the pre-signed URL to download a public or a Lambda component artifact. Core devices call this operation to identify the URL that they can use to download an artifact to install. |
| GET | /greengrass/things/{thingName}/connectivityInfo | Retrieves connectivity information for a Greengrass core device. Connectivity information includes endpoints and ports where client devices can connect to an MQTT broker on the core device. When a client device calls the IoT Greengrass discovery API, IoT Greengrass returns connectivity information for all of the core devices where the client device can connect. For more information, see Connect client devices to core devices in the IoT Greengrass Version 2 Developer Guide. |
| GET | /greengrass/v2/coreDevices/{coreDeviceThingName} | Retrieves metadata for a Greengrass core device.  IoT Greengrass relies on individual devices to send status updates to the Amazon Web Services Cloud. If the IoT Greengrass Core software isn't running on the device, or if device isn't connected to the Amazon Web Services Cloud, then the reported status of that device might not reflect its current status. The status timestamp indicates when the device status was last updated. Core devices send status updates at the following times:   When the IoT Greengrass Core software starts   When the core device receives a deployment from the Amazon Web Services Cloud   When the status of any component on the core device becomes BROKEN    At a regular interval that you can configure, which defaults to 24 hours   For IoT Greengrass Core v2.7.0, the core device sends status updates upon local deployment and cloud deployment |
| GET | /greengrass/v2/deployments/{deploymentId} | Gets a deployment. Deployments define the components that run on Greengrass core devices. |
| GET | /greengrass/servicerole | Gets the service role associated with IoT Greengrass for your Amazon Web Services account in this Amazon Web Services Region. IoT Greengrass uses this role to verify the identity of client devices and manage core device connectivity information. For more information, see Greengrass service role in the IoT Greengrass Version 2 Developer Guide. |
| GET | /greengrass/v2/coreDevices/{coreDeviceThingName}/associatedClientDevices | Retrieves a paginated list of client devices that are associated with a core device. |
| GET | /greengrass/v2/components/{arn}/versions | Retrieves a paginated list of all versions for a component. Greater versions are listed first. |
| GET | /greengrass/v2/components | Retrieves a paginated list of component summaries. This list includes components that you have permission to view. |
| GET | /greengrass/v2/coreDevices | Retrieves a paginated list of Greengrass core devices.  IoT Greengrass relies on individual devices to send status updates to the Amazon Web Services Cloud. If the IoT Greengrass Core software isn't running on the device, or if device isn't connected to the Amazon Web Services Cloud, then the reported status of that device might not reflect its current status. The status timestamp indicates when the device status was last updated. Core devices send status updates at the following times:   When the IoT Greengrass Core software starts   When the core device receives a deployment from the Amazon Web Services Cloud   When the status of any component on the core device becomes BROKEN    At a regular interval that you can configure, which defaults to 24 hours   For IoT Greengrass Core v2.7.0, the core device sends status updates upon local deployment and cloud deployment |
| GET | /greengrass/v2/deployments | Retrieves a paginated list of deployments. |
| GET | /greengrass/v2/coreDevices/{coreDeviceThingName}/effectiveDeployments | Retrieves a paginated list of deployment jobs that IoT Greengrass sends to Greengrass core devices. |
| GET | /greengrass/v2/coreDevices/{coreDeviceThingName}/installedComponents | Retrieves a paginated list of the components that a Greengrass core device runs. By default, this list doesn't include components that are deployed as dependencies of other components. To include dependencies in the response, set the topologyFilter parameter to ALL.  IoT Greengrass relies on individual devices to send status updates to the Amazon Web Services Cloud. If the IoT Greengrass Core software isn't running on the device, or if device isn't connected to the Amazon Web Services Cloud, then the reported status of that device might not reflect its current status. The status timestamp indicates when the device status was last updated. Core devices send status updates at the following times:   When the IoT Greengrass Core software starts   When the core device receives a deployment from the Amazon Web Services Cloud   When the status of any component on the core device becomes BROKEN    At a regular interval that you can configure, which defaults to 24 hours   For IoT Greengrass Core v2.7.0, the core device sends status updates upon local deployment and cloud deployment |
| POST | /greengrass/v2/resolveComponentCandidates | Retrieves a list of components that meet the component, version, and platform requirements of a deployment. Greengrass core devices call this operation when they receive a deployment to identify the components to install. This operation identifies components that meet all dependency requirements for a deployment. If the requirements conflict, then this operation returns an error and the deployment fails. For example, this occurs if component A requires version &gt;2.0.0 and component B requires version &lt;2.0.0 of a component dependency. When you specify the component candidates to resolve, IoT Greengrass compares each component's digest from the core device with the component's digest in the Amazon Web Services Cloud. If the digests don't match, then IoT Greengrass specifies to use the version from the Amazon Web Services Cloud.  To use this operation, you must use the data plane API endpoint and authenticate with an IoT device certificate. For more information, see IoT Greengrass endpoints and quotas. |
| PUT | /greengrass/things/{thingName}/connectivityInfo | Updates connectivity information for a Greengrass core device. Connectivity information includes endpoints and ports where client devices can connect to an MQTT broker on the core device. When a client device calls the IoT Greengrass discovery API, IoT Greengrass returns connectivity information for all of the core devices where the client device can connect. For more information, see Connect client devices to core devices in the IoT Greengrass Version 2 Developer Guide. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Retrieves the list of tags for an IoT Greengrass resource. |
| POST | /tags/{resourceArn} | Adds tags to an IoT Greengrass resource. If a tag already exists for the resource, this operation updates the tag's value. |
| DELETE | /tags/{resourceArn} | Removes a tag from an IoT Greengrass resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a associateClientDevice?" -> POST /greengrass/v2/coreDevices/{coreDeviceThingName}/associateClientDevices
- "Create a disassociateClientDevice?" -> POST /greengrass/v2/coreDevices/{coreDeviceThingName}/disassociateClientDevices
- "Create a cancel?" -> POST /greengrass/v2/deployments/{deploymentId}/cancel
- "Create a createComponentVersion?" -> POST /greengrass/v2/createComponentVersion
- "Create a deployment?" -> POST /greengrass/v2/deployments
- "Delete a component?" -> DELETE /greengrass/v2/components/{arn}
- "Delete a coreDevice?" -> DELETE /greengrass/v2/coreDevices/{coreDeviceThingName}
- "Delete a deployment?" -> DELETE /greengrass/v2/deployments/{deploymentId}
- "List all metadata?" -> GET /greengrass/v2/components/{arn}/metadata
- "Get component details?" -> GET /greengrass/v2/components/{arn}
- "Get artifact details?" -> GET /greengrass/v2/components/{arn}/artifacts/{artifactName+}
- "List all connectivityInfo?" -> GET /greengrass/things/{thingName}/connectivityInfo
- "Get coreDevice details?" -> GET /greengrass/v2/coreDevices/{coreDeviceThingName}
- "Get deployment details?" -> GET /greengrass/v2/deployments/{deploymentId}
- "List all servicerole?" -> GET /greengrass/servicerole
- "List all associatedClientDevices?" -> GET /greengrass/v2/coreDevices/{coreDeviceThingName}/associatedClientDevices
- "List all versions?" -> GET /greengrass/v2/components/{arn}/versions
- "List all components?" -> GET /greengrass/v2/components
- "List all coreDevices?" -> GET /greengrass/v2/coreDevices
- "List all deployments?" -> GET /greengrass/v2/deployments
- "List all effectiveDeployments?" -> GET /greengrass/v2/coreDevices/{coreDeviceThingName}/effectiveDeployments
- "List all installedComponents?" -> GET /greengrass/v2/coreDevices/{coreDeviceThingName}/installedComponents
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a resolveComponentCandidate?" -> POST /greengrass/v2/resolveComponentCandidates
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
