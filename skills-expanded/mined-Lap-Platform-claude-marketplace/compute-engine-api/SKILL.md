---
name: compute-engine-api
description: "Compute Engine API skill. Use when working with Compute Engine for locations, projects. Covers 694 endpoints."
version: 1.0.0
generator: lapsh
---

# Compute Engine API
API version: v1

## Auth
OAuth2 | OAuth2

## Base URL
https://compute.googleapis.com/compute/v1

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /locations/global/firewallPolicies -- verify access
3. POST /locations/global/firewallPolicies -- create first firewallPolicies

## Endpoints

694 endpoints across 2 groups. See references/api-spec.lap for full details.

### locations
| Method | Path | Description |
|--------|------|-------------|
| GET | /locations/global/firewallPolicies | Lists all the policies that have been configured for the specified folder or organization. |
| POST | /locations/global/firewallPolicies | Creates a new policy in the specified project using the data included in the request. |
| GET | /locations/global/firewallPolicies/listAssociations | Lists associations of a specified target, i.e., organization or folder. |
| DELETE | /locations/global/firewallPolicies/{firewallPolicy} | Deletes the specified policy. |
| GET | /locations/global/firewallPolicies/{firewallPolicy} | Returns the specified firewall policy. |
| PATCH | /locations/global/firewallPolicies/{firewallPolicy} | Patches the specified policy with the data included in the request. |
| POST | /locations/global/firewallPolicies/{firewallPolicy}/addAssociation | Inserts an association for the specified firewall policy. |
| POST | /locations/global/firewallPolicies/{firewallPolicy}/addRule | Inserts a rule into a firewall policy. |
| POST | /locations/global/firewallPolicies/{firewallPolicy}/cloneRules | Copies rules to the specified firewall policy. |
| GET | /locations/global/firewallPolicies/{firewallPolicy}/getAssociation | Gets an association with the specified name. |
| GET | /locations/global/firewallPolicies/{firewallPolicy}/getRule | Gets a rule of the specified priority. |
| POST | /locations/global/firewallPolicies/{firewallPolicy}/move | Moves the specified firewall policy. |
| POST | /locations/global/firewallPolicies/{firewallPolicy}/patchRule | Patches a rule of the specified priority. |
| POST | /locations/global/firewallPolicies/{firewallPolicy}/removeAssociation | Removes an association for the specified firewall policy. |
| POST | /locations/global/firewallPolicies/{firewallPolicy}/removeRule | Deletes a rule of the specified priority. |
| GET | /locations/global/firewallPolicies/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /locations/global/firewallPolicies/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /locations/global/firewallPolicies/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /locations/global/operations | Retrieves a list of Operation resources contained within the specified organization. |
| DELETE | /locations/global/operations/{operation} | Deletes the specified Operations resource. |
| GET | /locations/global/operations/{operation} | Retrieves the specified Operations resource. Gets a list of operations by making a `list()` request. |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{project} | Returns the specified Project resource. To decrease latency for this method, you can optionally omit any unneeded information from the response by using a field mask. This practice is especially recommended for unused quota information (the `quotas` field). To exclude one or more fields, set your request's `fields` query parameter to only include the fields you need. For example, to only include the `id` and `selfLink` fields, add the query parameter `?fields=id,selfLink` to your request. |
| GET | /projects/{project}/aggregated/acceleratorTypes | Retrieves an aggregated list of accelerator types. |
| GET | /projects/{project}/aggregated/addresses | Retrieves an aggregated list of addresses. |
| GET | /projects/{project}/aggregated/autoscalers | Retrieves an aggregated list of autoscalers. |
| GET | /projects/{project}/aggregated/backendServices | Retrieves the list of all BackendService resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/commitments | Retrieves an aggregated list of commitments by region. |
| GET | /projects/{project}/aggregated/diskTypes | Retrieves an aggregated list of disk types. |
| GET | /projects/{project}/aggregated/disks | Retrieves an aggregated list of persistent disks. |
| GET | /projects/{project}/aggregated/forwardingRules | Retrieves an aggregated list of forwarding rules. |
| GET | /projects/{project}/aggregated/healthChecks | Retrieves the list of all HealthCheck resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/instanceGroupManagers | Retrieves the list of managed instance groups and groups them by zone. |
| GET | /projects/{project}/aggregated/instanceGroups | Retrieves the list of instance groups and sorts them by zone. |
| GET | /projects/{project}/aggregated/instanceTemplates | Retrieves the list of all InstanceTemplates resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/instances | Retrieves an aggregated list of all of the instances in your project across all regions and zones. The performance of this method degrades when a filter is specified on a project that has a very large number of instances. |
| GET | /projects/{project}/aggregated/interconnectAttachments | Retrieves an aggregated list of interconnect attachments. |
| GET | /projects/{project}/aggregated/machineTypes | Retrieves an aggregated list of machine types. |
| GET | /projects/{project}/aggregated/networkAttachments | Retrieves the list of all NetworkAttachment resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/networkEdgeSecurityServices | Retrieves the list of all NetworkEdgeSecurityService resources available to the specified project. |
| GET | /projects/{project}/aggregated/networkEndpointGroups | Retrieves the list of network endpoint groups and sorts them by zone. |
| GET | /projects/{project}/aggregated/nodeGroups | Retrieves an aggregated list of node groups. Note: use nodeGroups.listNodes for more details about each group. |
| GET | /projects/{project}/aggregated/nodeTemplates | Retrieves an aggregated list of node templates. |
| GET | /projects/{project}/aggregated/nodeTypes | Retrieves an aggregated list of node types. |
| GET | /projects/{project}/aggregated/operations | Retrieves an aggregated list of all operations. |
| GET | /projects/{project}/aggregated/packetMirrorings | Retrieves an aggregated list of packetMirrorings. |
| GET | /projects/{project}/aggregated/publicDelegatedPrefixes | Lists all PublicDelegatedPrefix resources owned by the specific project across all scopes. |
| GET | /projects/{project}/aggregated/reservations | Retrieves an aggregated list of reservations. |
| GET | /projects/{project}/aggregated/resourcePolicies | Retrieves an aggregated list of resource policies. |
| GET | /projects/{project}/aggregated/routers | Retrieves an aggregated list of routers. |
| GET | /projects/{project}/aggregated/securityPolicies | Retrieves the list of all SecurityPolicy resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/serviceAttachments | Retrieves the list of all ServiceAttachment resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/sslCertificates | Retrieves the list of all SslCertificate resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/sslPolicies | Retrieves the list of all SslPolicy resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/subnetworks | Retrieves an aggregated list of subnetworks. |
| GET | /projects/{project}/aggregated/subnetworks/listUsable | Retrieves an aggregated list of all usable subnetworks in the project. |
| GET | /projects/{project}/aggregated/targetHttpProxies | Retrieves the list of all TargetHttpProxy resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/targetHttpsProxies | Retrieves the list of all TargetHttpsProxy resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/targetInstances | Retrieves an aggregated list of target instances. |
| GET | /projects/{project}/aggregated/targetPools | Retrieves an aggregated list of target pools. |
| GET | /projects/{project}/aggregated/targetTcpProxies | Retrieves the list of all TargetTcpProxy resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/targetVpnGateways | Retrieves an aggregated list of target VPN gateways. |
| GET | /projects/{project}/aggregated/urlMaps | Retrieves the list of all UrlMap resources, regional and global, available to the specified project. |
| GET | /projects/{project}/aggregated/vpnGateways | Retrieves an aggregated list of VPN gateways. |
| GET | /projects/{project}/aggregated/vpnTunnels | Retrieves an aggregated list of VPN tunnels. |
| POST | /projects/{project}/disableXpnHost | Disable this project as a shared VPC host project. |
| POST | /projects/{project}/disableXpnResource | Disable a service resource (also known as service project) associated with this host project. |
| POST | /projects/{project}/enableXpnHost | Enable this project as a shared VPC host project. |
| POST | /projects/{project}/enableXpnResource | Enable service resource (a.k.a service project) for a host project, so that subnets in the host project can be used by instances in the service project. |
| GET | /projects/{project}/getXpnHost | Gets the shared VPC host project that this project links to. May be empty if no link exists. |
| GET | /projects/{project}/getXpnResources | Gets service resources (a.k.a service project) associated with this host project. |
| GET | /projects/{project}/global/addresses | Retrieves a list of global addresses. |
| POST | /projects/{project}/global/addresses | Creates an address resource in the specified project by using the data included in the request. |
| DELETE | /projects/{project}/global/addresses/{address} | Deletes the specified address resource. |
| GET | /projects/{project}/global/addresses/{address} | Returns the specified address resource. |
| POST | /projects/{project}/global/addresses/{resource}/setLabels | Sets the labels on a GlobalAddress. To learn more about labels, read the Labeling Resources documentation. |
| GET | /projects/{project}/global/backendBuckets | Retrieves the list of BackendBucket resources available to the specified project. |
| POST | /projects/{project}/global/backendBuckets | Creates a BackendBucket resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/backendBuckets/{backendBucket} | Deletes the specified BackendBucket resource. |
| GET | /projects/{project}/global/backendBuckets/{backendBucket} | Returns the specified BackendBucket resource. |
| PATCH | /projects/{project}/global/backendBuckets/{backendBucket} | Updates the specified BackendBucket resource with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/global/backendBuckets/{backendBucket} | Updates the specified BackendBucket resource with the data included in the request. |
| POST | /projects/{project}/global/backendBuckets/{backendBucket}/addSignedUrlKey | Adds a key for validating requests with signed URLs for this backend bucket. |
| POST | /projects/{project}/global/backendBuckets/{backendBucket}/deleteSignedUrlKey | Deletes a key for validating requests with signed URLs for this backend bucket. |
| POST | /projects/{project}/global/backendBuckets/{backendBucket}/setEdgeSecurityPolicy | Sets the edge security policy for the specified backend bucket. |
| GET | /projects/{project}/global/backendServices | Retrieves the list of BackendService resources available to the specified project. |
| POST | /projects/{project}/global/backendServices | Creates a BackendService resource in the specified project using the data included in the request. For more information, see Backend services overview . |
| DELETE | /projects/{project}/global/backendServices/{backendService} | Deletes the specified BackendService resource. |
| GET | /projects/{project}/global/backendServices/{backendService} | Returns the specified BackendService resource. |
| PATCH | /projects/{project}/global/backendServices/{backendService} | Patches the specified BackendService resource with the data included in the request. For more information, see Backend services overview. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/global/backendServices/{backendService} | Updates the specified BackendService resource with the data included in the request. For more information, see Backend services overview. |
| POST | /projects/{project}/global/backendServices/{backendService}/addSignedUrlKey | Adds a key for validating requests with signed URLs for this backend service. |
| POST | /projects/{project}/global/backendServices/{backendService}/deleteSignedUrlKey | Deletes a key for validating requests with signed URLs for this backend service. |
| POST | /projects/{project}/global/backendServices/{backendService}/getHealth | Gets the most recent health check results for this BackendService. Example request body: { "group": "/zones/us-east1-b/instanceGroups/lb-backend-example" } |
| POST | /projects/{project}/global/backendServices/{backendService}/setEdgeSecurityPolicy | Sets the edge security policy for the specified backend service. |
| POST | /projects/{project}/global/backendServices/{backendService}/setSecurityPolicy | Sets the Google Cloud Armor security policy for the specified backend service. For more information, see Google Cloud Armor Overview |
| GET | /projects/{project}/global/backendServices/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/global/backendServices/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| GET | /projects/{project}/global/externalVpnGateways | Retrieves the list of ExternalVpnGateway available to the specified project. |
| POST | /projects/{project}/global/externalVpnGateways | Creates a ExternalVpnGateway in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/externalVpnGateways/{externalVpnGateway} | Deletes the specified externalVpnGateway. |
| GET | /projects/{project}/global/externalVpnGateways/{externalVpnGateway} | Returns the specified externalVpnGateway. Get a list of available externalVpnGateways by making a list() request. |
| POST | /projects/{project}/global/externalVpnGateways/{resource}/setLabels | Sets the labels on an ExternalVpnGateway. To learn more about labels, read the Labeling Resources documentation. |
| POST | /projects/{project}/global/externalVpnGateways/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/global/firewallPolicies | Lists all the policies that have been configured for the specified project. |
| POST | /projects/{project}/global/firewallPolicies | Creates a new policy in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/firewallPolicies/{firewallPolicy} | Deletes the specified policy. |
| GET | /projects/{project}/global/firewallPolicies/{firewallPolicy} | Returns the specified network firewall policy. |
| PATCH | /projects/{project}/global/firewallPolicies/{firewallPolicy} | Patches the specified policy with the data included in the request. |
| POST | /projects/{project}/global/firewallPolicies/{firewallPolicy}/addAssociation | Inserts an association for the specified firewall policy. |
| POST | /projects/{project}/global/firewallPolicies/{firewallPolicy}/addRule | Inserts a rule into a firewall policy. |
| POST | /projects/{project}/global/firewallPolicies/{firewallPolicy}/cloneRules | Copies rules to the specified firewall policy. |
| GET | /projects/{project}/global/firewallPolicies/{firewallPolicy}/getAssociation | Gets an association with the specified name. |
| GET | /projects/{project}/global/firewallPolicies/{firewallPolicy}/getRule | Gets a rule of the specified priority. |
| POST | /projects/{project}/global/firewallPolicies/{firewallPolicy}/patchRule | Patches a rule of the specified priority. |
| POST | /projects/{project}/global/firewallPolicies/{firewallPolicy}/removeAssociation | Removes an association for the specified firewall policy. |
| POST | /projects/{project}/global/firewallPolicies/{firewallPolicy}/removeRule | Deletes a rule of the specified priority. |
| GET | /projects/{project}/global/firewallPolicies/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/global/firewallPolicies/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/global/firewallPolicies/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/global/firewalls | Retrieves the list of firewall rules available to the specified project. |
| POST | /projects/{project}/global/firewalls | Creates a firewall rule in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/firewalls/{firewall} | Deletes the specified firewall. |
| GET | /projects/{project}/global/firewalls/{firewall} | Returns the specified firewall. |
| PATCH | /projects/{project}/global/firewalls/{firewall} | Updates the specified firewall rule with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/global/firewalls/{firewall} | Updates the specified firewall rule with the data included in the request. Note that all fields will be updated if using PUT, even fields that are not specified. To update individual fields, please use PATCH instead. |
| GET | /projects/{project}/global/forwardingRules | Retrieves a list of GlobalForwardingRule resources available to the specified project. |
| POST | /projects/{project}/global/forwardingRules | Creates a GlobalForwardingRule resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/forwardingRules/{forwardingRule} | Deletes the specified GlobalForwardingRule resource. |
| GET | /projects/{project}/global/forwardingRules/{forwardingRule} | Returns the specified GlobalForwardingRule resource. Gets a list of available forwarding rules by making a list() request. |
| PATCH | /projects/{project}/global/forwardingRules/{forwardingRule} | Updates the specified forwarding rule with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. Currently, you can only patch the network_tier field. |
| POST | /projects/{project}/global/forwardingRules/{forwardingRule}/setTarget | Changes target URL for the GlobalForwardingRule resource. The new target should be of the same type as the old target. |
| POST | /projects/{project}/global/forwardingRules/{resource}/setLabels | Sets the labels on the specified resource. To learn more about labels, read the Labeling resources documentation. |
| GET | /projects/{project}/global/healthChecks | Retrieves the list of HealthCheck resources available to the specified project. |
| POST | /projects/{project}/global/healthChecks | Creates a HealthCheck resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/healthChecks/{healthCheck} | Deletes the specified HealthCheck resource. |
| GET | /projects/{project}/global/healthChecks/{healthCheck} | Returns the specified HealthCheck resource. |
| PATCH | /projects/{project}/global/healthChecks/{healthCheck} | Updates a HealthCheck resource in the specified project using the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/global/healthChecks/{healthCheck} | Updates a HealthCheck resource in the specified project using the data included in the request. |
| GET | /projects/{project}/global/httpHealthChecks | Retrieves the list of HttpHealthCheck resources available to the specified project. |
| POST | /projects/{project}/global/httpHealthChecks | Creates a HttpHealthCheck resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/httpHealthChecks/{httpHealthCheck} | Deletes the specified HttpHealthCheck resource. |
| GET | /projects/{project}/global/httpHealthChecks/{httpHealthCheck} | Returns the specified HttpHealthCheck resource. |
| PATCH | /projects/{project}/global/httpHealthChecks/{httpHealthCheck} | Updates a HttpHealthCheck resource in the specified project using the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/global/httpHealthChecks/{httpHealthCheck} | Updates a HttpHealthCheck resource in the specified project using the data included in the request. |
| GET | /projects/{project}/global/httpsHealthChecks | Retrieves the list of HttpsHealthCheck resources available to the specified project. |
| POST | /projects/{project}/global/httpsHealthChecks | Creates a HttpsHealthCheck resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/httpsHealthChecks/{httpsHealthCheck} | Deletes the specified HttpsHealthCheck resource. |
| GET | /projects/{project}/global/httpsHealthChecks/{httpsHealthCheck} | Returns the specified HttpsHealthCheck resource. |
| PATCH | /projects/{project}/global/httpsHealthChecks/{httpsHealthCheck} | Updates a HttpsHealthCheck resource in the specified project using the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/global/httpsHealthChecks/{httpsHealthCheck} | Updates a HttpsHealthCheck resource in the specified project using the data included in the request. |
| GET | /projects/{project}/global/images | Retrieves the list of custom images available to the specified project. Custom images are images you create that belong to your project. This method does not get any images that belong to other projects, including publicly-available images, like Debian 8. If you want to get a list of publicly-available images, use this method to make a request to the respective image project, such as debian-cloud or windows-cloud. |
| POST | /projects/{project}/global/images | Creates an image in the specified project using the data included in the request. |
| GET | /projects/{project}/global/images/family/{family} | Returns the latest image that is part of an image family and is not deprecated. For more information on image families, see Public image families documentation. |
| DELETE | /projects/{project}/global/images/{image} | Deletes the specified image. |
| GET | /projects/{project}/global/images/{image} | Returns the specified image. |
| PATCH | /projects/{project}/global/images/{image} | Patches the specified image with the data included in the request. Only the following fields can be modified: family, description, deprecation status. |
| POST | /projects/{project}/global/images/{image}/deprecate | Sets the deprecation status of an image. If an empty request body is given, clears the deprecation status instead. |
| GET | /projects/{project}/global/images/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/global/images/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/global/images/{resource}/setLabels | Sets the labels on an image. To learn more about labels, read the Labeling Resources documentation. |
| POST | /projects/{project}/global/images/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/global/instanceTemplates | Retrieves a list of instance templates that are contained within the specified project. |
| POST | /projects/{project}/global/instanceTemplates | Creates an instance template in the specified project using the data that is included in the request. If you are creating a new template to update an existing instance group, your new instance template must use the same network or, if applicable, the same subnetwork as the original template. |
| DELETE | /projects/{project}/global/instanceTemplates/{instanceTemplate} | Deletes the specified instance template. Deleting an instance template is permanent and cannot be undone. It is not possible to delete templates that are already in use by a managed instance group. |
| GET | /projects/{project}/global/instanceTemplates/{instanceTemplate} | Returns the specified instance template. |
| GET | /projects/{project}/global/instanceTemplates/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/global/instanceTemplates/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/global/instanceTemplates/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/global/interconnectLocations | Retrieves the list of interconnect locations available to the specified project. |
| GET | /projects/{project}/global/interconnectLocations/{interconnectLocation} | Returns the details for the specified interconnect location. Gets a list of available interconnect locations by making a list() request. |
| GET | /projects/{project}/global/interconnects | Retrieves the list of Interconnects available to the specified project. |
| POST | /projects/{project}/global/interconnects | Creates an Interconnect in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/interconnects/{interconnect} | Deletes the specified Interconnect. |
| GET | /projects/{project}/global/interconnects/{interconnect} | Returns the specified Interconnect. Get a list of available Interconnects by making a list() request. |
| PATCH | /projects/{project}/global/interconnects/{interconnect} | Updates the specified Interconnect with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| GET | /projects/{project}/global/interconnects/{interconnect}/getDiagnostics | Returns the interconnectDiagnostics for the specified Interconnect. |
| POST | /projects/{project}/global/interconnects/{resource}/setLabels | Sets the labels on an Interconnect. To learn more about labels, read the Labeling Resources documentation. |
| GET | /projects/{project}/global/licenseCodes/{licenseCode} | Return a specified license code. License codes are mirrored across all projects that have permissions to read the License Code. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| POST | /projects/{project}/global/licenseCodes/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| GET | /projects/{project}/global/licenses | Retrieves the list of licenses available in the specified project. This method does not get any licenses that belong to other projects, including licenses attached to publicly-available images, like Debian 9. If you want to get a list of publicly-available licenses, use this method to make a request to the respective image project, such as debian-cloud or windows-cloud. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| POST | /projects/{project}/global/licenses | Create a License resource in the specified project. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| DELETE | /projects/{project}/global/licenses/{license} | Deletes the specified license. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| GET | /projects/{project}/global/licenses/{license} | Returns the specified License resource. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| GET | /projects/{project}/global/licenses/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| POST | /projects/{project}/global/licenses/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| POST | /projects/{project}/global/licenses/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. *Caution* This resource is intended for use only by third-party partners who are creating Cloud Marketplace images. |
| GET | /projects/{project}/global/machineImages | Retrieves a list of machine images that are contained within the specified project. |
| POST | /projects/{project}/global/machineImages | Creates a machine image in the specified project using the data that is included in the request. If you are creating a new machine image to update an existing instance, your new machine image should use the same network or, if applicable, the same subnetwork as the original instance. |
| DELETE | /projects/{project}/global/machineImages/{machineImage} | Deletes the specified machine image. Deleting a machine image is permanent and cannot be undone. |
| GET | /projects/{project}/global/machineImages/{machineImage} | Returns the specified machine image. |
| GET | /projects/{project}/global/machineImages/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/global/machineImages/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/global/machineImages/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/global/networkEndpointGroups | Retrieves the list of network endpoint groups that are located in the specified project. |
| POST | /projects/{project}/global/networkEndpointGroups | Creates a network endpoint group in the specified project using the parameters that are included in the request. |
| DELETE | /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup} | Deletes the specified network endpoint group.Note that the NEG cannot be deleted if there are backend services referencing it. |
| GET | /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup} | Returns the specified network endpoint group. |
| POST | /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup}/attachNetworkEndpoints | Attach a network endpoint to the specified network endpoint group. |
| POST | /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup}/detachNetworkEndpoints | Detach the network endpoint from the specified network endpoint group. |
| POST | /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup}/listNetworkEndpoints | Lists the network endpoints in the specified network endpoint group. |
| GET | /projects/{project}/global/networks | Retrieves the list of networks available to the specified project. |
| POST | /projects/{project}/global/networks | Creates a network in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/networks/{network} | Deletes the specified network. |
| GET | /projects/{project}/global/networks/{network} | Returns the specified network. |
| PATCH | /projects/{project}/global/networks/{network} | Patches the specified network with the data included in the request. Only the following fields can be modified: routingConfig.routingMode. |
| POST | /projects/{project}/global/networks/{network}/addPeering | Adds a peering to the specified network. |
| GET | /projects/{project}/global/networks/{network}/getEffectiveFirewalls | Returns the effective firewalls on a given network. |
| GET | /projects/{project}/global/networks/{network}/listPeeringRoutes | Lists the peering routes exchanged over peering connection. |
| POST | /projects/{project}/global/networks/{network}/removePeering | Removes a peering from the specified network. |
| POST | /projects/{project}/global/networks/{network}/switchToCustomMode | Switches the network mode from auto subnet mode to custom subnet mode. |
| PATCH | /projects/{project}/global/networks/{network}/updatePeering | Updates the specified network peering with the data included in the request. You can only modify the NetworkPeering.export_custom_routes field and the NetworkPeering.import_custom_routes field. |
| GET | /projects/{project}/global/operations | Retrieves a list of Operation resources contained within the specified project. |
| DELETE | /projects/{project}/global/operations/{operation} | Deletes the specified Operations resource. |
| GET | /projects/{project}/global/operations/{operation} | Retrieves the specified Operations resource. |
| POST | /projects/{project}/global/operations/{operation}/wait | Waits for the specified Operation resource to return as `DONE` or for the request to approach the 2 minute deadline, and retrieves the specified Operation resource. This method differs from the `GET` method in that it waits for no more than the default deadline (2 minutes) and then returns the current state of the operation, which might be `DONE` or still in progress. This method is called on a best-effort basis. Specifically: - In uncommon cases, when the server is overloaded, the request might return before the default deadline is reached, or might return after zero seconds. - If the default deadline is reached, there is no guarantee that the operation is actually done when the method returns. Be prepared to retry if the operation is not `DONE`. |
| GET | /projects/{project}/global/publicAdvertisedPrefixes | Lists the PublicAdvertisedPrefixes for a project. |
| POST | /projects/{project}/global/publicAdvertisedPrefixes | Creates a PublicAdvertisedPrefix in the specified project using the parameters that are included in the request. |
| DELETE | /projects/{project}/global/publicAdvertisedPrefixes/{publicAdvertisedPrefix} | Deletes the specified PublicAdvertisedPrefix |
| GET | /projects/{project}/global/publicAdvertisedPrefixes/{publicAdvertisedPrefix} | Returns the specified PublicAdvertisedPrefix resource. |
| PATCH | /projects/{project}/global/publicAdvertisedPrefixes/{publicAdvertisedPrefix} | Patches the specified Router resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| GET | /projects/{project}/global/publicDelegatedPrefixes | Lists the global PublicDelegatedPrefixes for a project. |
| POST | /projects/{project}/global/publicDelegatedPrefixes | Creates a global PublicDelegatedPrefix in the specified project using the parameters that are included in the request. |
| DELETE | /projects/{project}/global/publicDelegatedPrefixes/{publicDelegatedPrefix} | Deletes the specified global PublicDelegatedPrefix. |
| GET | /projects/{project}/global/publicDelegatedPrefixes/{publicDelegatedPrefix} | Returns the specified global PublicDelegatedPrefix resource. |
| PATCH | /projects/{project}/global/publicDelegatedPrefixes/{publicDelegatedPrefix} | Patches the specified global PublicDelegatedPrefix resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| GET | /projects/{project}/global/routes | Retrieves the list of Route resources available to the specified project. |
| POST | /projects/{project}/global/routes | Creates a Route resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/routes/{route} | Deletes the specified Route resource. |
| GET | /projects/{project}/global/routes/{route} | Returns the specified Route resource. |
| GET | /projects/{project}/global/securityPolicies | List all the policies that have been configured for the specified project. |
| POST | /projects/{project}/global/securityPolicies | Creates a new policy in the specified project using the data included in the request. |
| GET | /projects/{project}/global/securityPolicies/listPreconfiguredExpressionSets | Gets the current list of preconfigured Web Application Firewall (WAF) expressions. |
| POST | /projects/{project}/global/securityPolicies/{resource}/setLabels | Sets the labels on a security policy. To learn more about labels, read the Labeling Resources documentation. |
| DELETE | /projects/{project}/global/securityPolicies/{securityPolicy} | Deletes the specified policy. |
| GET | /projects/{project}/global/securityPolicies/{securityPolicy} | List all of the ordered rules present in a single specified policy. |
| PATCH | /projects/{project}/global/securityPolicies/{securityPolicy} | Patches the specified policy with the data included in the request. To clear fields in the rule, leave the fields empty and specify them in the updateMask. This cannot be used to be update the rules in the policy. Please use the per rule methods like addRule, patchRule, and removeRule instead. |
| POST | /projects/{project}/global/securityPolicies/{securityPolicy}/addRule | Inserts a rule into a security policy. |
| GET | /projects/{project}/global/securityPolicies/{securityPolicy}/getRule | Gets a rule at the specified priority. |
| POST | /projects/{project}/global/securityPolicies/{securityPolicy}/patchRule | Patches a rule at the specified priority. |
| POST | /projects/{project}/global/securityPolicies/{securityPolicy}/removeRule | Deletes a rule at the specified priority. |
| GET | /projects/{project}/global/snapshots | Retrieves the list of Snapshot resources contained within the specified project. |
| POST | /projects/{project}/global/snapshots | Creates a snapshot in the specified project using the data included in the request. For regular snapshot creation, consider using this method instead of disks.createSnapshot, as this method supports more features, such as creating snapshots in a project different from the source disk project. |
| GET | /projects/{project}/global/snapshots/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/global/snapshots/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/global/snapshots/{resource}/setLabels | Sets the labels on a snapshot. To learn more about labels, read the Labeling Resources documentation. |
| POST | /projects/{project}/global/snapshots/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| DELETE | /projects/{project}/global/snapshots/{snapshot} | Deletes the specified Snapshot resource. Keep in mind that deleting a single snapshot might not necessarily delete all the data on that snapshot. If any data on the snapshot that is marked for deletion is needed for subsequent snapshots, the data will be moved to the next corresponding snapshot. For more information, see Deleting snapshots. |
| GET | /projects/{project}/global/snapshots/{snapshot} | Returns the specified Snapshot resource. |
| GET | /projects/{project}/global/sslCertificates | Retrieves the list of SslCertificate resources available to the specified project. |
| POST | /projects/{project}/global/sslCertificates | Creates a SslCertificate resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/sslCertificates/{sslCertificate} | Deletes the specified SslCertificate resource. |
| GET | /projects/{project}/global/sslCertificates/{sslCertificate} | Returns the specified SslCertificate resource. |
| GET | /projects/{project}/global/sslPolicies | Lists all the SSL policies that have been configured for the specified project. |
| POST | /projects/{project}/global/sslPolicies | Returns the specified SSL policy resource. |
| GET | /projects/{project}/global/sslPolicies/listAvailableFeatures | Lists all features that can be specified in the SSL policy when using custom profile. |
| DELETE | /projects/{project}/global/sslPolicies/{sslPolicy} | Deletes the specified SSL policy. The SSL policy resource can be deleted only if it is not in use by any TargetHttpsProxy or TargetSslProxy resources. |
| GET | /projects/{project}/global/sslPolicies/{sslPolicy} | Lists all of the ordered rules present in a single specified policy. |
| PATCH | /projects/{project}/global/sslPolicies/{sslPolicy} | Patches the specified SSL policy with the data included in the request. |
| GET | /projects/{project}/global/targetGrpcProxies | Lists the TargetGrpcProxies for a project in the given scope. |
| POST | /projects/{project}/global/targetGrpcProxies | Creates a TargetGrpcProxy in the specified project in the given scope using the parameters that are included in the request. |
| DELETE | /projects/{project}/global/targetGrpcProxies/{targetGrpcProxy} | Deletes the specified TargetGrpcProxy in the given scope |
| GET | /projects/{project}/global/targetGrpcProxies/{targetGrpcProxy} | Returns the specified TargetGrpcProxy resource in the given scope. |
| PATCH | /projects/{project}/global/targetGrpcProxies/{targetGrpcProxy} | Patches the specified TargetGrpcProxy resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| GET | /projects/{project}/global/targetHttpProxies | Retrieves the list of TargetHttpProxy resources available to the specified project. |
| POST | /projects/{project}/global/targetHttpProxies | Creates a TargetHttpProxy resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/targetHttpProxies/{targetHttpProxy} | Deletes the specified TargetHttpProxy resource. |
| GET | /projects/{project}/global/targetHttpProxies/{targetHttpProxy} | Returns the specified TargetHttpProxy resource. |
| PATCH | /projects/{project}/global/targetHttpProxies/{targetHttpProxy} | Patches the specified TargetHttpProxy resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| GET | /projects/{project}/global/targetHttpsProxies | Retrieves the list of TargetHttpsProxy resources available to the specified project. |
| POST | /projects/{project}/global/targetHttpsProxies | Creates a TargetHttpsProxy resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy} | Deletes the specified TargetHttpsProxy resource. |
| GET | /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy} | Returns the specified TargetHttpsProxy resource. |
| PATCH | /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy} | Patches the specified TargetHttpsProxy resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| POST | /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}/setCertificateMap | Changes the Certificate Map for TargetHttpsProxy. |
| POST | /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}/setQuicOverride | Sets the QUIC override policy for TargetHttpsProxy. |
| POST | /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}/setSslPolicy | Sets the SSL policy for TargetHttpsProxy. The SSL policy specifies the server-side support for SSL features. This affects connections between clients and the HTTPS proxy load balancer. They do not affect the connection between the load balancer and the backends. |
| GET | /projects/{project}/global/targetSslProxies | Retrieves the list of TargetSslProxy resources available to the specified project. |
| POST | /projects/{project}/global/targetSslProxies | Creates a TargetSslProxy resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/targetSslProxies/{targetSslProxy} | Deletes the specified TargetSslProxy resource. |
| GET | /projects/{project}/global/targetSslProxies/{targetSslProxy} | Returns the specified TargetSslProxy resource. |
| POST | /projects/{project}/global/targetSslProxies/{targetSslProxy}/setBackendService | Changes the BackendService for TargetSslProxy. |
| POST | /projects/{project}/global/targetSslProxies/{targetSslProxy}/setCertificateMap | Changes the Certificate Map for TargetSslProxy. |
| POST | /projects/{project}/global/targetSslProxies/{targetSslProxy}/setProxyHeader | Changes the ProxyHeaderType for TargetSslProxy. |
| POST | /projects/{project}/global/targetSslProxies/{targetSslProxy}/setSslCertificates | Changes SslCertificates for TargetSslProxy. |
| POST | /projects/{project}/global/targetSslProxies/{targetSslProxy}/setSslPolicy | Sets the SSL policy for TargetSslProxy. The SSL policy specifies the server-side support for SSL features. This affects connections between clients and the SSL proxy load balancer. They do not affect the connection between the load balancer and the backends. |
| GET | /projects/{project}/global/targetTcpProxies | Retrieves the list of TargetTcpProxy resources available to the specified project. |
| POST | /projects/{project}/global/targetTcpProxies | Creates a TargetTcpProxy resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/targetTcpProxies/{targetTcpProxy} | Deletes the specified TargetTcpProxy resource. |
| GET | /projects/{project}/global/targetTcpProxies/{targetTcpProxy} | Returns the specified TargetTcpProxy resource. |
| POST | /projects/{project}/global/targetTcpProxies/{targetTcpProxy}/setBackendService | Changes the BackendService for TargetTcpProxy. |
| POST | /projects/{project}/global/targetTcpProxies/{targetTcpProxy}/setProxyHeader | Changes the ProxyHeaderType for TargetTcpProxy. |
| GET | /projects/{project}/global/urlMaps | Retrieves the list of UrlMap resources available to the specified project. |
| POST | /projects/{project}/global/urlMaps | Creates a UrlMap resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/global/urlMaps/{urlMap} | Deletes the specified UrlMap resource. |
| GET | /projects/{project}/global/urlMaps/{urlMap} | Returns the specified UrlMap resource. |
| PATCH | /projects/{project}/global/urlMaps/{urlMap} | Patches the specified UrlMap resource with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/global/urlMaps/{urlMap} | Updates the specified UrlMap resource with the data included in the request. |
| POST | /projects/{project}/global/urlMaps/{urlMap}/invalidateCache | Initiates a cache invalidation operation, invalidating the specified path, scoped to the specified UrlMap. For more information, see [Invalidating cached content](/cdn/docs/invalidating-cached-content). |
| POST | /projects/{project}/global/urlMaps/{urlMap}/validate | Runs static validation for the UrlMap. In particular, the tests of the provided UrlMap will be run. Calling this method does NOT create the UrlMap. |
| POST | /projects/{project}/listXpnHosts | Lists all shared VPC host projects visible to the user in an organization. |
| POST | /projects/{project}/moveDisk | Moves a persistent disk from one zone to another. |
| POST | /projects/{project}/moveInstance | Moves an instance and its attached persistent disks from one zone to another. *Note*: Moving VMs or disks by using this method might cause unexpected behavior. For more information, see the [known issue](/compute/docs/troubleshooting/known-issues#moving_vms_or_disks_using_the_moveinstance_api_or_the_causes_unexpected_behavior). |
| GET | /projects/{project}/regions | Retrieves the list of region resources available to the specified project. To decrease latency for this method, you can optionally omit any unneeded information from the response by using a field mask. This practice is especially recommended for unused quota information (the `items.quotas` field). To exclude one or more fields, set your request's `fields` query parameter to only include the fields you need. For example, to only include the `id` and `selfLink` fields, add the query parameter `?fields=id,selfLink` to your request. |
| GET | /projects/{project}/regions/{region} | Returns the specified Region resource. To decrease latency for this method, you can optionally omit any unneeded information from the response by using a field mask. This practice is especially recommended for unused quota information (the `quotas` field). To exclude one or more fields, set your request's `fields` query parameter to only include the fields you need. For example, to only include the `id` and `selfLink` fields, add the query parameter `?fields=id,selfLink` to your request. |
| GET | /projects/{project}/regions/{region}/addresses | Retrieves a list of addresses contained within the specified region. |
| POST | /projects/{project}/regions/{region}/addresses | Creates an address resource in the specified project by using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/addresses/{address} | Deletes the specified address resource. |
| GET | /projects/{project}/regions/{region}/addresses/{address} | Returns the specified address resource. |
| POST | /projects/{project}/regions/{region}/addresses/{resource}/setLabels | Sets the labels on an Address. To learn more about labels, read the Labeling Resources documentation. |
| GET | /projects/{project}/regions/{region}/autoscalers | Retrieves a list of autoscalers contained within the specified region. |
| PATCH | /projects/{project}/regions/{region}/autoscalers | Updates an autoscaler in the specified project using the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| POST | /projects/{project}/regions/{region}/autoscalers | Creates an autoscaler in the specified project using the data included in the request. |
| PUT | /projects/{project}/regions/{region}/autoscalers | Updates an autoscaler in the specified project using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/autoscalers/{autoscaler} | Deletes the specified autoscaler. |
| GET | /projects/{project}/regions/{region}/autoscalers/{autoscaler} | Returns the specified autoscaler. |
| GET | /projects/{project}/regions/{region}/backendServices | Retrieves the list of regional BackendService resources available to the specified project in the given region. |
| POST | /projects/{project}/regions/{region}/backendServices | Creates a regional BackendService resource in the specified project using the data included in the request. For more information, see Backend services overview. |
| DELETE | /projects/{project}/regions/{region}/backendServices/{backendService} | Deletes the specified regional BackendService resource. |
| GET | /projects/{project}/regions/{region}/backendServices/{backendService} | Returns the specified regional BackendService resource. |
| PATCH | /projects/{project}/regions/{region}/backendServices/{backendService} | Updates the specified regional BackendService resource with the data included in the request. For more information, see Understanding backend services This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/regions/{region}/backendServices/{backendService} | Updates the specified regional BackendService resource with the data included in the request. For more information, see Backend services overview . |
| POST | /projects/{project}/regions/{region}/backendServices/{backendService}/getHealth | Gets the most recent health check results for this regional BackendService. |
| GET | /projects/{project}/regions/{region}/backendServices/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/regions/{region}/backendServices/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| GET | /projects/{project}/regions/{region}/commitments | Retrieves a list of commitments contained within the specified region. |
| POST | /projects/{project}/regions/{region}/commitments | Creates a commitment in the specified project using the data included in the request. |
| GET | /projects/{project}/regions/{region}/commitments/{commitment} | Returns the specified commitment resource. |
| PATCH | /projects/{project}/regions/{region}/commitments/{commitment} | Updates the specified commitment with the data included in the request. Update is performed only on selected fields included as part of update-mask. Only the following fields can be modified: auto_renew. |
| GET | /projects/{project}/regions/{region}/diskTypes | Retrieves a list of regional disk types available to the specified project. |
| GET | /projects/{project}/regions/{region}/diskTypes/{diskType} | Returns the specified regional disk type. |
| GET | /projects/{project}/regions/{region}/disks | Retrieves the list of persistent disks contained within the specified region. |
| POST | /projects/{project}/regions/{region}/disks | Creates a persistent regional disk in the specified project using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/disks/{disk} | Deletes the specified regional persistent disk. Deleting a regional disk removes all the replicas of its data permanently and is irreversible. However, deleting a disk does not delete any snapshots previously made from the disk. You must separately delete snapshots. |
| GET | /projects/{project}/regions/{region}/disks/{disk} | Returns a specified regional persistent disk. |
| PATCH | /projects/{project}/regions/{region}/disks/{disk} | Update the specified disk with the data included in the request. Update is performed only on selected fields included as part of update-mask. Only the following fields can be modified: user_license. |
| POST | /projects/{project}/regions/{region}/disks/{disk}/addResourcePolicies | Adds existing resource policies to a regional disk. You can only add one policy which will be applied to this disk for scheduling snapshot creation. |
| POST | /projects/{project}/regions/{region}/disks/{disk}/createSnapshot | Creates a snapshot of a specified persistent disk. For regular snapshot creation, consider using snapshots.insert instead, as that method supports more features, such as creating snapshots in a project different from the source disk project. |
| POST | /projects/{project}/regions/{region}/disks/{disk}/removeResourcePolicies | Removes resource policies from a regional disk. |
| POST | /projects/{project}/regions/{region}/disks/{disk}/resize | Resizes the specified regional persistent disk. |
| GET | /projects/{project}/regions/{region}/disks/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/regions/{region}/disks/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/regions/{region}/disks/{resource}/setLabels | Sets the labels on the target regional disk. |
| POST | /projects/{project}/regions/{region}/disks/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/regions/{region}/firewallPolicies | Lists all the network firewall policies that have been configured for the specified project in the given region. |
| POST | /projects/{project}/regions/{region}/firewallPolicies | Creates a new network firewall policy in the specified project and region. |
| GET | /projects/{project}/regions/{region}/firewallPolicies/getEffectiveFirewalls | Returns the effective firewalls on a given network. |
| DELETE | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy} | Deletes the specified network firewall policy. |
| GET | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy} | Returns the specified network firewall policy. |
| PATCH | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy} | Patches the specified network firewall policy. |
| POST | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/addAssociation | Inserts an association for the specified network firewall policy. |
| POST | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/addRule | Inserts a rule into a network firewall policy. |
| POST | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/cloneRules | Copies rules to the specified network firewall policy. |
| GET | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/getAssociation | Gets an association with the specified name. |
| GET | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/getRule | Gets a rule of the specified priority. |
| POST | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/patchRule | Patches a rule of the specified priority. |
| POST | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/removeAssociation | Removes an association for the specified network firewall policy. |
| POST | /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/removeRule | Deletes a rule of the specified priority. |
| GET | /projects/{project}/regions/{region}/firewallPolicies/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/regions/{region}/firewallPolicies/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/regions/{region}/firewallPolicies/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/regions/{region}/forwardingRules | Retrieves a list of ForwardingRule resources available to the specified project and region. |
| POST | /projects/{project}/regions/{region}/forwardingRules | Creates a ForwardingRule resource in the specified project and region using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/forwardingRules/{forwardingRule} | Deletes the specified ForwardingRule resource. |
| GET | /projects/{project}/regions/{region}/forwardingRules/{forwardingRule} | Returns the specified ForwardingRule resource. |
| PATCH | /projects/{project}/regions/{region}/forwardingRules/{forwardingRule} | Updates the specified forwarding rule with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. Currently, you can only patch the network_tier field. |
| POST | /projects/{project}/regions/{region}/forwardingRules/{forwardingRule}/setTarget | Changes target URL for forwarding rule. The new target should be of the same type as the old target. |
| POST | /projects/{project}/regions/{region}/forwardingRules/{resource}/setLabels | Sets the labels on the specified resource. To learn more about labels, read the Labeling Resources documentation. |
| GET | /projects/{project}/regions/{region}/healthCheckServices | Lists all the HealthCheckService resources that have been configured for the specified project in the given region. |
| POST | /projects/{project}/regions/{region}/healthCheckServices | Creates a regional HealthCheckService resource in the specified project and region using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/healthCheckServices/{healthCheckService} | Deletes the specified regional HealthCheckService. |
| GET | /projects/{project}/regions/{region}/healthCheckServices/{healthCheckService} | Returns the specified regional HealthCheckService resource. |
| PATCH | /projects/{project}/regions/{region}/healthCheckServices/{healthCheckService} | Updates the specified regional HealthCheckService resource with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| GET | /projects/{project}/regions/{region}/healthChecks | Retrieves the list of HealthCheck resources available to the specified project. |
| POST | /projects/{project}/regions/{region}/healthChecks | Creates a HealthCheck resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/healthChecks/{healthCheck} | Deletes the specified HealthCheck resource. |
| GET | /projects/{project}/regions/{region}/healthChecks/{healthCheck} | Returns the specified HealthCheck resource. |
| PATCH | /projects/{project}/regions/{region}/healthChecks/{healthCheck} | Updates a HealthCheck resource in the specified project using the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PUT | /projects/{project}/regions/{region}/healthChecks/{healthCheck} | Updates a HealthCheck resource in the specified project using the data included in the request. |
| GET | /projects/{project}/regions/{region}/instanceGroupManagers | Retrieves the list of managed instance groups that are contained within the specified region. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers | Creates a managed instance group using the information that you specify in the request. After the group is created, instances in the group are created using the specified instance template. This operation is marked as DONE when the group is created even if the instances in the group have not yet been created. You must separately verify the status of the individual instances with the listmanagedinstances method. A regional managed instance group can contain up to 2000 instances. |
| DELETE | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager} | Deletes the specified managed instance group and all of the instances in that group. |
| GET | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager} | Returns all of the details about the specified managed instance group. |
| PATCH | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager} | Updates a managed instance group using the information that you specify in the request. This operation is marked as DONE when the group is patched even if the instances in the group are still in the process of being patched. You must separately verify the status of the individual instances with the listmanagedinstances method. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. If you update your group to specify a new template or instance configuration, it's possible that your intended specification for each VM in the group is different from the current state of that VM. To learn how to apply an updated configuration to the VMs in a MIG, see Updating instances in a MIG. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/abandonInstances | Flags the specified instances to be immediately removed from the managed instance group. Abandoning an instance does not delete the instance, but it does remove the instance from any target pools that are applied by the managed instance group. This method reduces the targetSize of the managed instance group by the number of instances that you abandon. This operation is marked as DONE when the action is scheduled even if the instances have not yet been removed from the group. You must separately verify the status of the abandoning action with the listmanagedinstances method. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration has elapsed before the VM instance is removed or deleted. You can specify a maximum of 1000 instances with this method per request. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/applyUpdatesToInstances | Apply updates to selected instances the managed instance group. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/createInstances | Creates instances with per-instance configurations in this regional managed instance group. Instances are created using the current instance template. The create instances operation is marked DONE if the createInstances request is successful. The underlying actions take additional time. You must separately verify the status of the creating or actions with the listmanagedinstances method. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/deleteInstances | Flags the specified instances in the managed instance group to be immediately deleted. The instances are also removed from any target pools of which they were a member. This method reduces the targetSize of the managed instance group by the number of instances that you delete. The deleteInstances operation is marked DONE if the deleteInstances request is successful. The underlying actions take additional time. You must separately verify the status of the deleting action with the listmanagedinstances method. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration has elapsed before the VM instance is removed or deleted. You can specify a maximum of 1000 instances with this method per request. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/deletePerInstanceConfigs | Deletes selected per-instance configurations for the managed instance group. |
| GET | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/listErrors | Lists all errors thrown by actions on instances for a given regional managed instance group. The filter and orderBy query parameters are not supported. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/listManagedInstances | Lists the instances in the managed instance group and instances that are scheduled to be created. The list includes any current actions that the group has scheduled for its instances. The orderBy query parameter is not supported. The `pageToken` query parameter is supported only in the alpha and beta API and only if the group's `listManagedInstancesResults` field is set to `PAGINATED`. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/listPerInstanceConfigs | Lists all of the per-instance configurations defined for the managed instance group. The orderBy query parameter is not supported. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/patchPerInstanceConfigs | Inserts or patches per-instance configurations for the managed instance group. perInstanceConfig.name serves as a key used to distinguish whether to perform insert or patch. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/recreateInstances | Flags the specified VM instances in the managed instance group to be immediately recreated. Each instance is recreated using the group's current configuration. This operation is marked as DONE when the flag is set even if the instances have not yet been recreated. You must separately verify the status of each instance by checking its currentAction field; for more information, see Checking the status of managed instances. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration has elapsed before the VM instance is removed or deleted. You can specify a maximum of 1000 instances with this method per request. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/resize | Changes the intended size of the managed instance group. If you increase the size, the group creates new instances using the current instance template. If you decrease the size, the group deletes one or more instances. The resize operation is marked DONE if the resize request is successful. The underlying actions take additional time. You must separately verify the status of the creating or deleting actions with the listmanagedinstances method. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration has elapsed before the VM instance is removed or deleted. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/setInstanceTemplate | Sets the instance template to use when creating new instances or recreating instances in this group. Existing instances are not affected. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/setTargetPools | Modifies the target pools to which all new instances in this group are assigned. Existing instances in the group are not affected. |
| POST | /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/updatePerInstanceConfigs | Inserts or updates per-instance configurations for the managed instance group. perInstanceConfig.name serves as a key used to distinguish whether to perform insert or patch. |
| GET | /projects/{project}/regions/{region}/instanceGroups | Retrieves the list of instance group resources contained within the specified region. |
| GET | /projects/{project}/regions/{region}/instanceGroups/{instanceGroup} | Returns the specified instance group resource. |
| POST | /projects/{project}/regions/{region}/instanceGroups/{instanceGroup}/listInstances | Lists the instances in the specified instance group and displays information about the named ports. Depending on the specified options, this method can list all instances or only the instances that are running. The orderBy query parameter is not supported. |
| POST | /projects/{project}/regions/{region}/instanceGroups/{instanceGroup}/setNamedPorts | Sets the named ports for the specified regional instance group. |
| POST | /projects/{project}/regions/{region}/instances/bulkInsert | Creates multiple instances in a given region. Count specifies the number of instances to create. |
| GET | /projects/{project}/regions/{region}/interconnectAttachments | Retrieves the list of interconnect attachments contained within the specified region. |
| POST | /projects/{project}/regions/{region}/interconnectAttachments | Creates an InterconnectAttachment in the specified project using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/interconnectAttachments/{interconnectAttachment} | Deletes the specified interconnect attachment. |
| GET | /projects/{project}/regions/{region}/interconnectAttachments/{interconnectAttachment} | Returns the specified interconnect attachment. |
| PATCH | /projects/{project}/regions/{region}/interconnectAttachments/{interconnectAttachment} | Updates the specified interconnect attachment with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| POST | /projects/{project}/regions/{region}/interconnectAttachments/{resource}/setLabels | Sets the labels on an InterconnectAttachment. To learn more about labels, read the Labeling Resources documentation. |
| GET | /projects/{project}/regions/{region}/networkAttachments | Lists the NetworkAttachments for a project in the given scope. |
| POST | /projects/{project}/regions/{region}/networkAttachments | Creates a NetworkAttachment in the specified project in the given scope using the parameters that are included in the request. |
| DELETE | /projects/{project}/regions/{region}/networkAttachments/{networkAttachment} | Deletes the specified NetworkAttachment in the given scope |
| GET | /projects/{project}/regions/{region}/networkAttachments/{networkAttachment} | Returns the specified NetworkAttachment resource in the given scope. |
| GET | /projects/{project}/regions/{region}/networkAttachments/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/regions/{region}/networkAttachments/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/regions/{region}/networkAttachments/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| POST | /projects/{project}/regions/{region}/networkEdgeSecurityServices | Creates a new service in the specified project using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/networkEdgeSecurityServices/{networkEdgeSecurityService} | Deletes the specified service. |
| GET | /projects/{project}/regions/{region}/networkEdgeSecurityServices/{networkEdgeSecurityService} | Gets a specified NetworkEdgeSecurityService. |
| PATCH | /projects/{project}/regions/{region}/networkEdgeSecurityServices/{networkEdgeSecurityService} | Patches the specified policy with the data included in the request. |
| GET | /projects/{project}/regions/{region}/networkEndpointGroups | Retrieves the list of regional network endpoint groups available to the specified project in the given region. |
| POST | /projects/{project}/regions/{region}/networkEndpointGroups | Creates a network endpoint group in the specified project using the parameters that are included in the request. |
| DELETE | /projects/{project}/regions/{region}/networkEndpointGroups/{networkEndpointGroup} | Deletes the specified network endpoint group. Note that the NEG cannot be deleted if it is configured as a backend of a backend service. |
| GET | /projects/{project}/regions/{region}/networkEndpointGroups/{networkEndpointGroup} | Returns the specified network endpoint group. |
| GET | /projects/{project}/regions/{region}/nodeTemplates | Retrieves a list of node templates available to the specified project. |
| POST | /projects/{project}/regions/{region}/nodeTemplates | Creates a NodeTemplate resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/nodeTemplates/{nodeTemplate} | Deletes the specified NodeTemplate resource. |
| GET | /projects/{project}/regions/{region}/nodeTemplates/{nodeTemplate} | Returns the specified node template. |
| GET | /projects/{project}/regions/{region}/nodeTemplates/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/regions/{region}/nodeTemplates/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/regions/{region}/nodeTemplates/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/regions/{region}/notificationEndpoints | Lists the NotificationEndpoints for a project in the given region. |
| POST | /projects/{project}/regions/{region}/notificationEndpoints | Create a NotificationEndpoint in the specified project in the given region using the parameters that are included in the request. |
| DELETE | /projects/{project}/regions/{region}/notificationEndpoints/{notificationEndpoint} | Deletes the specified NotificationEndpoint in the given region |
| GET | /projects/{project}/regions/{region}/notificationEndpoints/{notificationEndpoint} | Returns the specified NotificationEndpoint resource in the given region. |
| GET | /projects/{project}/regions/{region}/operations | Retrieves a list of Operation resources contained within the specified region. |
| DELETE | /projects/{project}/regions/{region}/operations/{operation} | Deletes the specified region-specific Operations resource. |
| GET | /projects/{project}/regions/{region}/operations/{operation} | Retrieves the specified region-specific Operations resource. |
| POST | /projects/{project}/regions/{region}/operations/{operation}/wait | Waits for the specified Operation resource to return as `DONE` or for the request to approach the 2 minute deadline, and retrieves the specified Operation resource. This method differs from the `GET` method in that it waits for no more than the default deadline (2 minutes) and then returns the current state of the operation, which might be `DONE` or still in progress. This method is called on a best-effort basis. Specifically: - In uncommon cases, when the server is overloaded, the request might return before the default deadline is reached, or might return after zero seconds. - If the default deadline is reached, there is no guarantee that the operation is actually done when the method returns. Be prepared to retry if the operation is not `DONE`. |
| GET | /projects/{project}/regions/{region}/packetMirrorings | Retrieves a list of PacketMirroring resources available to the specified project and region. |
| POST | /projects/{project}/regions/{region}/packetMirrorings | Creates a PacketMirroring resource in the specified project and region using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/packetMirrorings/{packetMirroring} | Deletes the specified PacketMirroring resource. |
| GET | /projects/{project}/regions/{region}/packetMirrorings/{packetMirroring} | Returns the specified PacketMirroring resource. |
| PATCH | /projects/{project}/regions/{region}/packetMirrorings/{packetMirroring} | Patches the specified PacketMirroring resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| POST | /projects/{project}/regions/{region}/packetMirrorings/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/regions/{region}/publicDelegatedPrefixes | Lists the PublicDelegatedPrefixes for a project in the given region. |
| POST | /projects/{project}/regions/{region}/publicDelegatedPrefixes | Creates a PublicDelegatedPrefix in the specified project in the given region using the parameters that are included in the request. |
| DELETE | /projects/{project}/regions/{region}/publicDelegatedPrefixes/{publicDelegatedPrefix} | Deletes the specified PublicDelegatedPrefix in the given region. |
| GET | /projects/{project}/regions/{region}/publicDelegatedPrefixes/{publicDelegatedPrefix} | Returns the specified PublicDelegatedPrefix resource in the given region. |
| PATCH | /projects/{project}/regions/{region}/publicDelegatedPrefixes/{publicDelegatedPrefix} | Patches the specified PublicDelegatedPrefix resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| GET | /projects/{project}/regions/{region}/resourcePolicies | A list all the resource policies that have been configured for the specified project in specified region. |
| POST | /projects/{project}/regions/{region}/resourcePolicies | Creates a new resource policy. |
| DELETE | /projects/{project}/regions/{region}/resourcePolicies/{resourcePolicy} | Deletes the specified resource policy. |
| GET | /projects/{project}/regions/{region}/resourcePolicies/{resourcePolicy} | Retrieves all information of the specified resource policy. |
| GET | /projects/{project}/regions/{region}/resourcePolicies/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/regions/{region}/resourcePolicies/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/regions/{region}/resourcePolicies/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/regions/{region}/routers | Retrieves a list of Router resources available to the specified project. |
| POST | /projects/{project}/regions/{region}/routers | Creates a Router resource in the specified project and region using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/routers/{router} | Deletes the specified Router resource. |
| GET | /projects/{project}/regions/{region}/routers/{router} | Returns the specified Router resource. |
| PATCH | /projects/{project}/regions/{region}/routers/{router} | Patches the specified Router resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| PUT | /projects/{project}/regions/{region}/routers/{router} | Updates the specified Router resource with the data included in the request. This method conforms to PUT semantics, which requests that the state of the target resource be created or replaced with the state defined by the representation enclosed in the request message payload. |
| GET | /projects/{project}/regions/{region}/routers/{router}/getNatMappingInfo | Retrieves runtime Nat mapping information of VM endpoints. |
| GET | /projects/{project}/regions/{region}/routers/{router}/getRouterStatus | Retrieves runtime information of the specified router. |
| POST | /projects/{project}/regions/{region}/routers/{router}/preview | Preview fields auto-generated during router create and update operations. Calling this method does NOT create or update the router. |
| GET | /projects/{project}/regions/{region}/securityPolicies | List all the policies that have been configured for the specified project and region. |
| POST | /projects/{project}/regions/{region}/securityPolicies | Creates a new policy in the specified project using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/securityPolicies/{securityPolicy} | Deletes the specified policy. |
| GET | /projects/{project}/regions/{region}/securityPolicies/{securityPolicy} | List all of the ordered rules present in a single specified policy. |
| PATCH | /projects/{project}/regions/{region}/securityPolicies/{securityPolicy} | Patches the specified policy with the data included in the request. To clear fields in the rule, leave the fields empty and specify them in the updateMask. This cannot be used to be update the rules in the policy. Please use the per rule methods like addRule, patchRule, and removeRule instead. |
| GET | /projects/{project}/regions/{region}/serviceAttachments | Lists the ServiceAttachments for a project in the given scope. |
| POST | /projects/{project}/regions/{region}/serviceAttachments | Creates a ServiceAttachment in the specified project in the given scope using the parameters that are included in the request. |
| GET | /projects/{project}/regions/{region}/serviceAttachments/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/regions/{region}/serviceAttachments/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/regions/{region}/serviceAttachments/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| DELETE | /projects/{project}/regions/{region}/serviceAttachments/{serviceAttachment} | Deletes the specified ServiceAttachment in the given scope |
| GET | /projects/{project}/regions/{region}/serviceAttachments/{serviceAttachment} | Returns the specified ServiceAttachment resource in the given scope. |
| PATCH | /projects/{project}/regions/{region}/serviceAttachments/{serviceAttachment} | Patches the specified ServiceAttachment resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| GET | /projects/{project}/regions/{region}/sslCertificates | Retrieves the list of SslCertificate resources available to the specified project in the specified region. |
| POST | /projects/{project}/regions/{region}/sslCertificates | Creates a SslCertificate resource in the specified project and region using the data included in the request |
| DELETE | /projects/{project}/regions/{region}/sslCertificates/{sslCertificate} | Deletes the specified SslCertificate resource in the region. |
| GET | /projects/{project}/regions/{region}/sslCertificates/{sslCertificate} | Returns the specified SslCertificate resource in the specified region. Get a list of available SSL certificates by making a list() request. |
| GET | /projects/{project}/regions/{region}/sslPolicies | Lists all the SSL policies that have been configured for the specified project and region. |
| POST | /projects/{project}/regions/{region}/sslPolicies | Creates a new policy in the specified project and region using the data included in the request. |
| GET | /projects/{project}/regions/{region}/sslPolicies/listAvailableFeatures | Lists all features that can be specified in the SSL policy when using custom profile. |
| DELETE | /projects/{project}/regions/{region}/sslPolicies/{sslPolicy} | Deletes the specified SSL policy. The SSL policy resource can be deleted only if it is not in use by any TargetHttpsProxy or TargetSslProxy resources. |
| GET | /projects/{project}/regions/{region}/sslPolicies/{sslPolicy} | Lists all of the ordered rules present in a single specified policy. |
| PATCH | /projects/{project}/regions/{region}/sslPolicies/{sslPolicy} | Patches the specified SSL policy with the data included in the request. |
| GET | /projects/{project}/regions/{region}/subnetworks | Retrieves a list of subnetworks available to the specified project. |
| POST | /projects/{project}/regions/{region}/subnetworks | Creates a subnetwork in the specified project using the data included in the request. |
| GET | /projects/{project}/regions/{region}/subnetworks/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/regions/{region}/subnetworks/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/regions/{region}/subnetworks/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| DELETE | /projects/{project}/regions/{region}/subnetworks/{subnetwork} | Deletes the specified subnetwork. |
| GET | /projects/{project}/regions/{region}/subnetworks/{subnetwork} | Returns the specified subnetwork. |
| PATCH | /projects/{project}/regions/{region}/subnetworks/{subnetwork} | Patches the specified subnetwork with the data included in the request. Only certain fields can be updated with a patch request as indicated in the field descriptions. You must specify the current fingerprint of the subnetwork resource being patched. |
| POST | /projects/{project}/regions/{region}/subnetworks/{subnetwork}/expandIpCidrRange | Expands the IP CIDR range of the subnetwork to a specified value. |
| POST | /projects/{project}/regions/{region}/subnetworks/{subnetwork}/setPrivateIpGoogleAccess | Set whether VMs in this subnet can access Google services without assigning external IP addresses through Private Google Access. |
| GET | /projects/{project}/regions/{region}/targetHttpProxies | Retrieves the list of TargetHttpProxy resources available to the specified project in the specified region. |
| POST | /projects/{project}/regions/{region}/targetHttpProxies | Creates a TargetHttpProxy resource in the specified project and region using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/targetHttpProxies/{targetHttpProxy} | Deletes the specified TargetHttpProxy resource. |
| GET | /projects/{project}/regions/{region}/targetHttpProxies/{targetHttpProxy} | Returns the specified TargetHttpProxy resource in the specified region. |
| POST | /projects/{project}/regions/{region}/targetHttpProxies/{targetHttpProxy}/setUrlMap | Changes the URL map for TargetHttpProxy. |
| GET | /projects/{project}/regions/{region}/targetHttpsProxies | Retrieves the list of TargetHttpsProxy resources available to the specified project in the specified region. |
| POST | /projects/{project}/regions/{region}/targetHttpsProxies | Creates a TargetHttpsProxy resource in the specified project and region using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy} | Deletes the specified TargetHttpsProxy resource. |
| GET | /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy} | Returns the specified TargetHttpsProxy resource in the specified region. |
| PATCH | /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy} | Patches the specified regional TargetHttpsProxy resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| POST | /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy}/setSslCertificates | Replaces SslCertificates for TargetHttpsProxy. |
| POST | /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy}/setUrlMap | Changes the URL map for TargetHttpsProxy. |
| GET | /projects/{project}/regions/{region}/targetPools | Retrieves a list of target pools available to the specified project and region. |
| POST | /projects/{project}/regions/{region}/targetPools | Creates a target pool in the specified project and region using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/targetPools/{targetPool} | Deletes the specified target pool. |
| GET | /projects/{project}/regions/{region}/targetPools/{targetPool} | Returns the specified target pool. |
| POST | /projects/{project}/regions/{region}/targetPools/{targetPool}/addHealthCheck | Adds health check URLs to a target pool. |
| POST | /projects/{project}/regions/{region}/targetPools/{targetPool}/addInstance | Adds an instance to a target pool. |
| POST | /projects/{project}/regions/{region}/targetPools/{targetPool}/getHealth | Gets the most recent health check results for each IP for the instance that is referenced by the given target pool. |
| POST | /projects/{project}/regions/{region}/targetPools/{targetPool}/removeHealthCheck | Removes health check URL from a target pool. |
| POST | /projects/{project}/regions/{region}/targetPools/{targetPool}/removeInstance | Removes instance URL from a target pool. |
| POST | /projects/{project}/regions/{region}/targetPools/{targetPool}/setBackup | Changes a backup target pool's configurations. |
| GET | /projects/{project}/regions/{region}/targetTcpProxies | Retrieves a list of TargetTcpProxy resources available to the specified project in a given region. |
| POST | /projects/{project}/regions/{region}/targetTcpProxies | Creates a TargetTcpProxy resource in the specified project and region using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/targetTcpProxies/{targetTcpProxy} | Deletes the specified TargetTcpProxy resource. |
| GET | /projects/{project}/regions/{region}/targetTcpProxies/{targetTcpProxy} | Returns the specified TargetTcpProxy resource. |
| GET | /projects/{project}/regions/{region}/targetVpnGateways | Retrieves a list of target VPN gateways available to the specified project and region. |
| POST | /projects/{project}/regions/{region}/targetVpnGateways | Creates a target VPN gateway in the specified project and region using the data included in the request. |
| POST | /projects/{project}/regions/{region}/targetVpnGateways/{resource}/setLabels | Sets the labels on a TargetVpnGateway. To learn more about labels, read the Labeling Resources documentation. |
| DELETE | /projects/{project}/regions/{region}/targetVpnGateways/{targetVpnGateway} | Deletes the specified target VPN gateway. |
| GET | /projects/{project}/regions/{region}/targetVpnGateways/{targetVpnGateway} | Returns the specified target VPN gateway. |
| GET | /projects/{project}/regions/{region}/urlMaps | Retrieves the list of UrlMap resources available to the specified project in the specified region. |
| POST | /projects/{project}/regions/{region}/urlMaps | Creates a UrlMap resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/regions/{region}/urlMaps/{urlMap} | Deletes the specified UrlMap resource. |
| GET | /projects/{project}/regions/{region}/urlMaps/{urlMap} | Returns the specified UrlMap resource. |
| PATCH | /projects/{project}/regions/{region}/urlMaps/{urlMap} | Patches the specified UrlMap resource with the data included in the request. This method supports PATCH semantics and uses JSON merge patch format and processing rules. |
| PUT | /projects/{project}/regions/{region}/urlMaps/{urlMap} | Updates the specified UrlMap resource with the data included in the request. |
| POST | /projects/{project}/regions/{region}/urlMaps/{urlMap}/validate | Runs static validation for the UrlMap. In particular, the tests of the provided UrlMap will be run. Calling this method does NOT create the UrlMap. |
| GET | /projects/{project}/regions/{region}/vpnGateways | Retrieves a list of VPN gateways available to the specified project and region. |
| POST | /projects/{project}/regions/{region}/vpnGateways | Creates a VPN gateway in the specified project and region using the data included in the request. |
| POST | /projects/{project}/regions/{region}/vpnGateways/{resource}/setLabels | Sets the labels on a VpnGateway. To learn more about labels, read the Labeling Resources documentation. |
| POST | /projects/{project}/regions/{region}/vpnGateways/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| DELETE | /projects/{project}/regions/{region}/vpnGateways/{vpnGateway} | Deletes the specified VPN gateway. |
| GET | /projects/{project}/regions/{region}/vpnGateways/{vpnGateway} | Returns the specified VPN gateway. |
| GET | /projects/{project}/regions/{region}/vpnGateways/{vpnGateway}/getStatus | Returns the status for the specified VPN gateway. |
| GET | /projects/{project}/regions/{region}/vpnTunnels | Retrieves a list of VpnTunnel resources contained in the specified project and region. |
| POST | /projects/{project}/regions/{region}/vpnTunnels | Creates a VpnTunnel resource in the specified project and region using the data included in the request. |
| POST | /projects/{project}/regions/{region}/vpnTunnels/{resource}/setLabels | Sets the labels on a VpnTunnel. To learn more about labels, read the Labeling Resources documentation. |
| DELETE | /projects/{project}/regions/{region}/vpnTunnels/{vpnTunnel} | Deletes the specified VpnTunnel resource. |
| GET | /projects/{project}/regions/{region}/vpnTunnels/{vpnTunnel} | Returns the specified VpnTunnel resource. |
| POST | /projects/{project}/setCommonInstanceMetadata | Sets metadata common to all instances within the specified project using the data included in the request. |
| POST | /projects/{project}/setDefaultNetworkTier | Sets the default network tier of the project. The default network tier is used when an address/forwardingRule/instance is created without specifying the network tier field. |
| POST | /projects/{project}/setUsageExportBucket | Enables the usage export feature and sets the usage export bucket where reports are stored. If you provide an empty request body using this method, the usage export feature will be disabled. |
| POST | /projects/{project}/targetHttpProxies/{targetHttpProxy}/setUrlMap | Changes the URL map for TargetHttpProxy. |
| POST | /projects/{project}/targetHttpsProxies/{targetHttpsProxy}/setSslCertificates | Replaces SslCertificates for TargetHttpsProxy. |
| POST | /projects/{project}/targetHttpsProxies/{targetHttpsProxy}/setUrlMap | Changes the URL map for TargetHttpsProxy. |
| GET | /projects/{project}/zones | Retrieves the list of Zone resources available to the specified project. |
| GET | /projects/{project}/zones/{zone} | Returns the specified Zone resource. |
| GET | /projects/{project}/zones/{zone}/acceleratorTypes | Retrieves a list of accelerator types that are available to the specified project. |
| GET | /projects/{project}/zones/{zone}/acceleratorTypes/{acceleratorType} | Returns the specified accelerator type. |
| GET | /projects/{project}/zones/{zone}/autoscalers | Retrieves a list of autoscalers contained within the specified zone. |
| PATCH | /projects/{project}/zones/{zone}/autoscalers | Updates an autoscaler in the specified project using the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| POST | /projects/{project}/zones/{zone}/autoscalers | Creates an autoscaler in the specified project using the data included in the request. |
| PUT | /projects/{project}/zones/{zone}/autoscalers | Updates an autoscaler in the specified project using the data included in the request. |
| DELETE | /projects/{project}/zones/{zone}/autoscalers/{autoscaler} | Deletes the specified autoscaler. |
| GET | /projects/{project}/zones/{zone}/autoscalers/{autoscaler} | Returns the specified autoscaler resource. |
| GET | /projects/{project}/zones/{zone}/diskTypes | Retrieves a list of disk types available to the specified project. |
| GET | /projects/{project}/zones/{zone}/diskTypes/{diskType} | Returns the specified disk type. |
| GET | /projects/{project}/zones/{zone}/disks | Retrieves a list of persistent disks contained within the specified zone. |
| POST | /projects/{project}/zones/{zone}/disks | Creates a persistent disk in the specified project using the data in the request. You can create a disk from a source (sourceImage, sourceSnapshot, or sourceDisk) or create an empty 500 GB data disk by omitting all properties. You can also create a disk that is larger than the default size by specifying the sizeGb property. |
| DELETE | /projects/{project}/zones/{zone}/disks/{disk} | Deletes the specified persistent disk. Deleting a disk removes its data permanently and is irreversible. However, deleting a disk does not delete any snapshots previously made from the disk. You must separately delete snapshots. |
| GET | /projects/{project}/zones/{zone}/disks/{disk} | Returns the specified persistent disk. |
| PATCH | /projects/{project}/zones/{zone}/disks/{disk} | Updates the specified disk with the data included in the request. The update is performed only on selected fields included as part of update-mask. Only the following fields can be modified: user_license. |
| POST | /projects/{project}/zones/{zone}/disks/{disk}/addResourcePolicies | Adds existing resource policies to a disk. You can only add one policy which will be applied to this disk for scheduling snapshot creation. |
| POST | /projects/{project}/zones/{zone}/disks/{disk}/createSnapshot | Creates a snapshot of a specified persistent disk. For regular snapshot creation, consider using snapshots.insert instead, as that method supports more features, such as creating snapshots in a project different from the source disk project. |
| POST | /projects/{project}/zones/{zone}/disks/{disk}/removeResourcePolicies | Removes resource policies from a disk. |
| POST | /projects/{project}/zones/{zone}/disks/{disk}/resize | Resizes the specified persistent disk. You can only increase the size of the disk. |
| GET | /projects/{project}/zones/{zone}/disks/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/zones/{zone}/disks/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/zones/{zone}/disks/{resource}/setLabels | Sets the labels on a disk. To learn more about labels, read the Labeling Resources documentation. |
| POST | /projects/{project}/zones/{zone}/disks/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/zones/{zone}/imageFamilyViews/{family} | Returns the latest image that is part of an image family, is not deprecated and is rolled out in the specified zone. |
| GET | /projects/{project}/zones/{zone}/instanceGroupManagers | Retrieves a list of managed instance groups that are contained within the specified project and zone. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers | Creates a managed instance group using the information that you specify in the request. After the group is created, instances in the group are created using the specified instance template. This operation is marked as DONE when the group is created even if the instances in the group have not yet been created. You must separately verify the status of the individual instances with the listmanagedinstances method. A managed instance group can have up to 1000 VM instances per group. Please contact Cloud Support if you need an increase in this limit. |
| DELETE | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager} | Deletes the specified managed instance group and all of the instances in that group. Note that the instance group must not belong to a backend service. Read Deleting an instance group for more information. |
| GET | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager} | Returns all of the details about the specified managed instance group. |
| PATCH | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager} | Updates a managed instance group using the information that you specify in the request. This operation is marked as DONE when the group is patched even if the instances in the group are still in the process of being patched. You must separately verify the status of the individual instances with the listManagedInstances method. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. If you update your group to specify a new template or instance configuration, it's possible that your intended specification for each VM in the group is different from the current state of that VM. To learn how to apply an updated configuration to the VMs in a MIG, see Updating instances in a MIG. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/abandonInstances | Flags the specified instances to be removed from the managed instance group. Abandoning an instance does not delete the instance, but it does remove the instance from any target pools that are applied by the managed instance group. This method reduces the targetSize of the managed instance group by the number of instances that you abandon. This operation is marked as DONE when the action is scheduled even if the instances have not yet been removed from the group. You must separately verify the status of the abandoning action with the listmanagedinstances method. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration has elapsed before the VM instance is removed or deleted. You can specify a maximum of 1000 instances with this method per request. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/applyUpdatesToInstances | Applies changes to selected instances on the managed instance group. This method can be used to apply new overrides and/or new versions. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/createInstances | Creates instances with per-instance configurations in this managed instance group. Instances are created using the current instance template. The create instances operation is marked DONE if the createInstances request is successful. The underlying actions take additional time. You must separately verify the status of the creating or actions with the listmanagedinstances method. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/deleteInstances | Flags the specified instances in the managed instance group for immediate deletion. The instances are also removed from any target pools of which they were a member. This method reduces the targetSize of the managed instance group by the number of instances that you delete. This operation is marked as DONE when the action is scheduled even if the instances are still being deleted. You must separately verify the status of the deleting action with the listmanagedinstances method. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration has elapsed before the VM instance is removed or deleted. You can specify a maximum of 1000 instances with this method per request. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/deletePerInstanceConfigs | Deletes selected per-instance configurations for the managed instance group. |
| GET | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/listErrors | Lists all errors thrown by actions on instances for a given managed instance group. The filter and orderBy query parameters are not supported. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/listManagedInstances | Lists all of the instances in the managed instance group. Each instance in the list has a currentAction, which indicates the action that the managed instance group is performing on the instance. For example, if the group is still creating an instance, the currentAction is CREATING. If a previous action failed, the list displays the errors for that failed action. The orderBy query parameter is not supported. The `pageToken` query parameter is supported only in the alpha and beta API and only if the group's `listManagedInstancesResults` field is set to `PAGINATED`. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/listPerInstanceConfigs | Lists all of the per-instance configurations defined for the managed instance group. The orderBy query parameter is not supported. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/patchPerInstanceConfigs | Inserts or patches per-instance configurations for the managed instance group. perInstanceConfig.name serves as a key used to distinguish whether to perform insert or patch. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/recreateInstances | Flags the specified VM instances in the managed instance group to be immediately recreated. Each instance is recreated using the group's current configuration. This operation is marked as DONE when the flag is set even if the instances have not yet been recreated. You must separately verify the status of each instance by checking its currentAction field; for more information, see Checking the status of managed instances. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration has elapsed before the VM instance is removed or deleted. You can specify a maximum of 1000 instances with this method per request. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/resize | Resizes the managed instance group. If you increase the size, the group creates new instances using the current instance template. If you decrease the size, the group deletes instances. The resize operation is marked DONE when the resize actions are scheduled even if the group has not yet added or deleted any instances. You must separately verify the status of the creating or deleting actions with the listmanagedinstances method. When resizing down, the instance group arbitrarily chooses the order in which VMs are deleted. The group takes into account some VM attributes when making the selection including: + The status of the VM instance. + The health of the VM instance. + The instance template version the VM is based on. + For regional managed instance groups, the location of the VM instance. This list is subject to change. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration has elapsed before the VM instance is removed or deleted. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/setInstanceTemplate | Specifies the instance template to use when creating new instances in this group. The templates for existing instances in the group do not change unless you run recreateInstances, run applyUpdatesToInstances, or set the group's updatePolicy.type to PROACTIVE. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/setTargetPools | Modifies the target pools to which all instances in this managed instance group are assigned. The target pools automatically apply to all of the instances in the managed instance group. This operation is marked DONE when you make the request even if the instances have not yet been added to their target pools. The change might take some time to apply to all of the instances in the group depending on the size of the group. |
| POST | /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/updatePerInstanceConfigs | Inserts or updates per-instance configurations for the managed instance group. perInstanceConfig.name serves as a key used to distinguish whether to perform insert or patch. |
| GET | /projects/{project}/zones/{zone}/instanceGroups | Retrieves the list of zonal instance group resources contained within the specified zone. For managed instance groups, use the instanceGroupManagers or regionInstanceGroupManagers methods instead. |
| POST | /projects/{project}/zones/{zone}/instanceGroups | Creates an instance group in the specified project using the parameters that are included in the request. |
| DELETE | /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup} | Deletes the specified instance group. The instances in the group are not deleted. Note that instance group must not belong to a backend service. Read Deleting an instance group for more information. |
| GET | /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup} | Returns the specified zonal instance group. Get a list of available zonal instance groups by making a list() request. For managed instance groups, use the instanceGroupManagers or regionInstanceGroupManagers methods instead. |
| POST | /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}/addInstances | Adds a list of instances to the specified instance group. All of the instances in the instance group must be in the same network/subnetwork. Read Adding instances for more information. |
| POST | /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}/listInstances | Lists the instances in the specified instance group. The orderBy query parameter is not supported. The filter query parameter is supported, but only for expressions that use `eq` (equal) or `ne` (not equal) operators. |
| POST | /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}/removeInstances | Removes one or more instances from the specified instance group, but does not delete those instances. If the group is part of a backend service that has enabled connection draining, it can take up to 60 seconds after the connection draining duration before the VM instance is removed or deleted. |
| POST | /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}/setNamedPorts | Sets the named ports for the specified instance group. |
| GET | /projects/{project}/zones/{zone}/instances | Retrieves the list of instances contained within the specified zone. |
| POST | /projects/{project}/zones/{zone}/instances | Creates an instance resource in the specified project using the data included in the request. |
| POST | /projects/{project}/zones/{zone}/instances/bulkInsert | Creates multiple instances. Count specifies the number of instances to create. For more information, see About bulk creation of VMs. |
| DELETE | /projects/{project}/zones/{zone}/instances/{instance} | Deletes the specified Instance resource. For more information, see Deleting an instance. |
| GET | /projects/{project}/zones/{zone}/instances/{instance} | Returns the specified Instance resource. |
| PUT | /projects/{project}/zones/{zone}/instances/{instance} | Updates an instance only if the necessary resources are available. This method can update only a specific set of instance properties. See Updating a running instance for a list of updatable instance properties. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/addAccessConfig | Adds an access config to an instance's network interface. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/addResourcePolicies | Adds existing resource policies to an instance. You can only add one policy right now which will be applied to this instance for scheduling live migrations. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/attachDisk | Attaches an existing Disk resource to an instance. You must first create the disk before you can attach it. It is not possible to create and attach a disk at the same time. For more information, read Adding a persistent disk to your instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/deleteAccessConfig | Deletes an access config from an instance's network interface. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/detachDisk | Detaches a disk from an instance. |
| GET | /projects/{project}/zones/{zone}/instances/{instance}/getEffectiveFirewalls | Returns effective firewalls applied to an interface of the instance. |
| GET | /projects/{project}/zones/{zone}/instances/{instance}/getGuestAttributes | Returns the specified guest attributes entry. |
| GET | /projects/{project}/zones/{zone}/instances/{instance}/getShieldedInstanceIdentity | Returns the Shielded Instance Identity of an instance |
| GET | /projects/{project}/zones/{zone}/instances/{instance}/referrers | Retrieves a list of resources that refer to the VM instance specified in the request. For example, if the VM instance is part of a managed or unmanaged instance group, the referrers list includes the instance group. For more information, read Viewing referrers to VM instances. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/removeResourcePolicies | Removes resource policies from an instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/reset | Performs a reset on the instance. This is a hard reset. The VM does not do a graceful shutdown. For more information, see Resetting an instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/resume | Resumes an instance that was suspended using the instances().suspend method. |
| GET | /projects/{project}/zones/{zone}/instances/{instance}/screenshot | Returns the screenshot from the specified instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/sendDiagnosticInterrupt | Sends diagnostic interrupt to the instance. |
| GET | /projects/{project}/zones/{zone}/instances/{instance}/serialPort | Returns the last 1 MB of serial port output from the specified instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setDiskAutoDelete | Sets the auto-delete flag for a disk attached to an instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setLabels | Sets labels on an instance. To learn more about labels, read the Labeling Resources documentation. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setMachineResources | Changes the number and/or type of accelerator for a stopped instance to the values specified in the request. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setMachineType | Changes the machine type for a stopped instance to the machine type specified in the request. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setMetadata | Sets metadata for the specified instance to the data included in the request. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setMinCpuPlatform | Changes the minimum CPU platform that this instance should use. This method can only be called on a stopped instance. For more information, read Specifying a Minimum CPU Platform. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setName | Sets name of an instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setScheduling | Sets an instance's scheduling options. You can only call this method on a stopped instance, that is, a VM instance that is in a `TERMINATED` state. See Instance Life Cycle for more information on the possible instance states. For more information about setting scheduling options for a VM, see Set VM host maintenance policy. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setServiceAccount | Sets the service account on the instance. For more information, read Changing the service account and access scopes for an instance. |
| PATCH | /projects/{project}/zones/{zone}/instances/{instance}/setShieldedInstanceIntegrityPolicy | Sets the Shielded Instance integrity policy for an instance. You can only use this method on a running instance. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/setTags | Sets network tags for the specified instance to the data included in the request. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/simulateMaintenanceEvent | Simulates a host maintenance event on a VM. For more information, see Simulate a host maintenance event. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/start | Starts an instance that was stopped using the instances().stop method. For more information, see Restart an instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/startWithEncryptionKey | Starts an instance that was stopped using the instances().stop method. For more information, see Restart an instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/stop | Stops a running instance, shutting it down cleanly, and allows you to restart the instance at a later time. Stopped instances do not incur VM usage charges while they are stopped. However, resources that the VM is using, such as persistent disks and static IP addresses, will continue to be charged until they are deleted. For more information, see Stopping an instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/suspend | This method suspends a running instance, saving its state to persistent storage, and allows you to resume the instance at a later time. Suspended instances have no compute costs (cores or RAM), and incur only storage charges for the saved VM memory and localSSD data. Any charged resources the virtual machine was using, such as persistent disks and static IP addresses, will continue to be charged while the instance is suspended. For more information, see Suspending and resuming an instance. |
| POST | /projects/{project}/zones/{zone}/instances/{instance}/updateAccessConfig | Updates the specified access config from an instance's network interface with the data included in the request. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PATCH | /projects/{project}/zones/{zone}/instances/{instance}/updateDisplayDevice | Updates the Display config for a VM instance. You can only use this method on a stopped VM instance. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| PATCH | /projects/{project}/zones/{zone}/instances/{instance}/updateNetworkInterface | Updates an instance's network interface. This method can only update an interface's alias IP range and attached network. See Modifying alias IP ranges for an existing instance for instructions on changing alias IP ranges. See Migrating a VM between networks for instructions on migrating an interface. This method follows PATCH semantics. |
| PATCH | /projects/{project}/zones/{zone}/instances/{instance}/updateShieldedInstanceConfig | Updates the Shielded Instance config for an instance. You can only use this method on a stopped instance. This method supports PATCH semantics and uses the JSON merge patch format and processing rules. |
| GET | /projects/{project}/zones/{zone}/instances/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/zones/{zone}/instances/{resource}/setDeletionProtection | Sets deletion protection on the instance. |
| POST | /projects/{project}/zones/{zone}/instances/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/zones/{zone}/instances/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/zones/{zone}/machineTypes | Retrieves a list of machine types available to the specified project. |
| GET | /projects/{project}/zones/{zone}/machineTypes/{machineType} | Returns the specified machine type. |
| GET | /projects/{project}/zones/{zone}/networkEndpointGroups | Retrieves the list of network endpoint groups that are located in the specified project and zone. |
| POST | /projects/{project}/zones/{zone}/networkEndpointGroups | Creates a network endpoint group in the specified project using the parameters that are included in the request. |
| DELETE | /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup} | Deletes the specified network endpoint group. The network endpoints in the NEG and the VM instances they belong to are not terminated when the NEG is deleted. Note that the NEG cannot be deleted if there are backend services referencing it. |
| GET | /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup} | Returns the specified network endpoint group. |
| POST | /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup}/attachNetworkEndpoints | Attach a list of network endpoints to the specified network endpoint group. |
| POST | /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup}/detachNetworkEndpoints | Detach a list of network endpoints from the specified network endpoint group. |
| POST | /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup}/listNetworkEndpoints | Lists the network endpoints in the specified network endpoint group. |
| POST | /projects/{project}/zones/{zone}/networkEndpointGroups/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/zones/{zone}/nodeGroups | Retrieves a list of node groups available to the specified project. Note: use nodeGroups.listNodes for more details about each group. |
| POST | /projects/{project}/zones/{zone}/nodeGroups | Creates a NodeGroup resource in the specified project using the data included in the request. |
| DELETE | /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup} | Deletes the specified NodeGroup resource. |
| GET | /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup} | Returns the specified NodeGroup. Get a list of available NodeGroups by making a list() request. Note: the "nodes" field should not be used. Use nodeGroups.listNodes instead. |
| PATCH | /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup} | Updates the specified node group. |
| POST | /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/addNodes | Adds specified number of nodes to the node group. |
| POST | /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/deleteNodes | Deletes specified nodes from the node group. |
| POST | /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/listNodes | Lists nodes in the node group. |
| POST | /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/setNodeTemplate | Updates the node template of the node group. |
| POST | /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/simulateMaintenanceEvent | Simulates maintenance event on specified nodes from the node group. |
| GET | /projects/{project}/zones/{zone}/nodeGroups/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/zones/{zone}/nodeGroups/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/zones/{zone}/nodeGroups/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/zones/{zone}/nodeTypes | Retrieves a list of node types available to the specified project. |
| GET | /projects/{project}/zones/{zone}/nodeTypes/{nodeType} | Returns the specified node type. |
| GET | /projects/{project}/zones/{zone}/operations | Retrieves a list of Operation resources contained within the specified zone. |
| DELETE | /projects/{project}/zones/{zone}/operations/{operation} | Deletes the specified zone-specific Operations resource. |
| GET | /projects/{project}/zones/{zone}/operations/{operation} | Retrieves the specified zone-specific Operations resource. |
| POST | /projects/{project}/zones/{zone}/operations/{operation}/wait | Waits for the specified Operation resource to return as `DONE` or for the request to approach the 2 minute deadline, and retrieves the specified Operation resource. This method waits for no more than the 2 minutes and then returns the current state of the operation, which might be `DONE` or still in progress. This method is called on a best-effort basis. Specifically: - In uncommon cases, when the server is overloaded, the request might return before the default deadline is reached, or might return after zero seconds. - If the default deadline is reached, there is no guarantee that the operation is actually done when the method returns. Be prepared to retry if the operation is not `DONE`. |
| GET | /projects/{project}/zones/{zone}/reservations | A list of all the reservations that have been configured for the specified project in specified zone. |
| POST | /projects/{project}/zones/{zone}/reservations | Creates a new reservation. For more information, read Reserving zonal resources. |
| DELETE | /projects/{project}/zones/{zone}/reservations/{reservation} | Deletes the specified reservation. |
| GET | /projects/{project}/zones/{zone}/reservations/{reservation} | Retrieves information about the specified reservation. |
| PATCH | /projects/{project}/zones/{zone}/reservations/{reservation} | Update share settings of the reservation. |
| POST | /projects/{project}/zones/{zone}/reservations/{reservation}/resize | Resizes the reservation (applicable to standalone reservations only). For more information, read Modifying reservations. |
| GET | /projects/{project}/zones/{zone}/reservations/{resource}/getIamPolicy | Gets the access control policy for a resource. May be empty if no such policy or resource exists. |
| POST | /projects/{project}/zones/{zone}/reservations/{resource}/setIamPolicy | Sets the access control policy on the specified resource. Replaces any existing policy. |
| POST | /projects/{project}/zones/{zone}/reservations/{resource}/testIamPermissions | Returns permissions that a caller has on the specified resource. |
| GET | /projects/{project}/zones/{zone}/targetInstances | Retrieves a list of TargetInstance resources available to the specified project and zone. |
| POST | /projects/{project}/zones/{zone}/targetInstances | Creates a TargetInstance resource in the specified project and zone using the data included in the request. |
| DELETE | /projects/{project}/zones/{zone}/targetInstances/{targetInstance} | Deletes the specified TargetInstance resource. |
| GET | /projects/{project}/zones/{zone}/targetInstances/{targetInstance} | Returns the specified TargetInstance resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all firewallPolicies?" -> GET /locations/global/firewallPolicies
- "Create a firewallPolicy?" -> POST /locations/global/firewallPolicies
- "List all listAssociations?" -> GET /locations/global/firewallPolicies/listAssociations
- "Delete a firewallPolicy?" -> DELETE /locations/global/firewallPolicies/{firewallPolicy}
- "Get firewallPolicy details?" -> GET /locations/global/firewallPolicies/{firewallPolicy}
- "Partially update a firewallPolicy?" -> PATCH /locations/global/firewallPolicies/{firewallPolicy}
- "Create a addAssociation?" -> POST /locations/global/firewallPolicies/{firewallPolicy}/addAssociation
- "Create a addRule?" -> POST /locations/global/firewallPolicies/{firewallPolicy}/addRule
- "Create a cloneRule?" -> POST /locations/global/firewallPolicies/{firewallPolicy}/cloneRules
- "List all getAssociation?" -> GET /locations/global/firewallPolicies/{firewallPolicy}/getAssociation
- "List all getRule?" -> GET /locations/global/firewallPolicies/{firewallPolicy}/getRule
- "Create a move?" -> POST /locations/global/firewallPolicies/{firewallPolicy}/move
- "Create a patchRule?" -> POST /locations/global/firewallPolicies/{firewallPolicy}/patchRule
- "Create a removeAssociation?" -> POST /locations/global/firewallPolicies/{firewallPolicy}/removeAssociation
- "Create a removeRule?" -> POST /locations/global/firewallPolicies/{firewallPolicy}/removeRule
- "List all getIamPolicy?" -> GET /locations/global/firewallPolicies/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /locations/global/firewallPolicies/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /locations/global/firewallPolicies/{resource}/testIamPermissions
- "List all operations?" -> GET /locations/global/operations
- "Delete a operation?" -> DELETE /locations/global/operations/{operation}
- "Get operation details?" -> GET /locations/global/operations/{operation}
- "Get project details?" -> GET /projects/{project}
- "List all acceleratorTypes?" -> GET /projects/{project}/aggregated/acceleratorTypes
- "List all addresses?" -> GET /projects/{project}/aggregated/addresses
- "List all autoscalers?" -> GET /projects/{project}/aggregated/autoscalers
- "List all backendServices?" -> GET /projects/{project}/aggregated/backendServices
- "List all commitments?" -> GET /projects/{project}/aggregated/commitments
- "List all diskTypes?" -> GET /projects/{project}/aggregated/diskTypes
- "List all disks?" -> GET /projects/{project}/aggregated/disks
- "List all forwardingRules?" -> GET /projects/{project}/aggregated/forwardingRules
- "List all healthChecks?" -> GET /projects/{project}/aggregated/healthChecks
- "List all instanceGroupManagers?" -> GET /projects/{project}/aggregated/instanceGroupManagers
- "List all instanceGroups?" -> GET /projects/{project}/aggregated/instanceGroups
- "List all instanceTemplates?" -> GET /projects/{project}/aggregated/instanceTemplates
- "List all instances?" -> GET /projects/{project}/aggregated/instances
- "List all interconnectAttachments?" -> GET /projects/{project}/aggregated/interconnectAttachments
- "List all machineTypes?" -> GET /projects/{project}/aggregated/machineTypes
- "List all networkAttachments?" -> GET /projects/{project}/aggregated/networkAttachments
- "List all networkEdgeSecurityServices?" -> GET /projects/{project}/aggregated/networkEdgeSecurityServices
- "List all networkEndpointGroups?" -> GET /projects/{project}/aggregated/networkEndpointGroups
- "List all nodeGroups?" -> GET /projects/{project}/aggregated/nodeGroups
- "List all nodeTemplates?" -> GET /projects/{project}/aggregated/nodeTemplates
- "List all nodeTypes?" -> GET /projects/{project}/aggregated/nodeTypes
- "List all operations?" -> GET /projects/{project}/aggregated/operations
- "List all packetMirrorings?" -> GET /projects/{project}/aggregated/packetMirrorings
- "List all publicDelegatedPrefixes?" -> GET /projects/{project}/aggregated/publicDelegatedPrefixes
- "List all reservations?" -> GET /projects/{project}/aggregated/reservations
- "List all resourcePolicies?" -> GET /projects/{project}/aggregated/resourcePolicies
- "List all routers?" -> GET /projects/{project}/aggregated/routers
- "List all securityPolicies?" -> GET /projects/{project}/aggregated/securityPolicies
- "List all serviceAttachments?" -> GET /projects/{project}/aggregated/serviceAttachments
- "List all sslCertificates?" -> GET /projects/{project}/aggregated/sslCertificates
- "List all sslPolicies?" -> GET /projects/{project}/aggregated/sslPolicies
- "List all subnetworks?" -> GET /projects/{project}/aggregated/subnetworks
- "List all listUsable?" -> GET /projects/{project}/aggregated/subnetworks/listUsable
- "List all targetHttpProxies?" -> GET /projects/{project}/aggregated/targetHttpProxies
- "List all targetHttpsProxies?" -> GET /projects/{project}/aggregated/targetHttpsProxies
- "List all targetInstances?" -> GET /projects/{project}/aggregated/targetInstances
- "List all targetPools?" -> GET /projects/{project}/aggregated/targetPools
- "List all targetTcpProxies?" -> GET /projects/{project}/aggregated/targetTcpProxies
- "List all targetVpnGateways?" -> GET /projects/{project}/aggregated/targetVpnGateways
- "List all urlMaps?" -> GET /projects/{project}/aggregated/urlMaps
- "List all vpnGateways?" -> GET /projects/{project}/aggregated/vpnGateways
- "List all vpnTunnels?" -> GET /projects/{project}/aggregated/vpnTunnels
- "Create a disableXpnHost?" -> POST /projects/{project}/disableXpnHost
- "Create a disableXpnResource?" -> POST /projects/{project}/disableXpnResource
- "Create a enableXpnHost?" -> POST /projects/{project}/enableXpnHost
- "Create a enableXpnResource?" -> POST /projects/{project}/enableXpnResource
- "List all getXpnHost?" -> GET /projects/{project}/getXpnHost
- "List all getXpnResources?" -> GET /projects/{project}/getXpnResources
- "List all addresses?" -> GET /projects/{project}/global/addresses
- "Create a address?" -> POST /projects/{project}/global/addresses
- "Delete a address?" -> DELETE /projects/{project}/global/addresses/{address}
- "Get address details?" -> GET /projects/{project}/global/addresses/{address}
- "Create a setLabel?" -> POST /projects/{project}/global/addresses/{resource}/setLabels
- "List all backendBuckets?" -> GET /projects/{project}/global/backendBuckets
- "Create a backendBucket?" -> POST /projects/{project}/global/backendBuckets
- "Delete a backendBucket?" -> DELETE /projects/{project}/global/backendBuckets/{backendBucket}
- "Get backendBucket details?" -> GET /projects/{project}/global/backendBuckets/{backendBucket}
- "Partially update a backendBucket?" -> PATCH /projects/{project}/global/backendBuckets/{backendBucket}
- "Update a backendBucket?" -> PUT /projects/{project}/global/backendBuckets/{backendBucket}
- "Create a addSignedUrlKey?" -> POST /projects/{project}/global/backendBuckets/{backendBucket}/addSignedUrlKey
- "Create a deleteSignedUrlKey?" -> POST /projects/{project}/global/backendBuckets/{backendBucket}/deleteSignedUrlKey
- "Create a setEdgeSecurityPolicy?" -> POST /projects/{project}/global/backendBuckets/{backendBucket}/setEdgeSecurityPolicy
- "List all backendServices?" -> GET /projects/{project}/global/backendServices
- "Create a backendService?" -> POST /projects/{project}/global/backendServices
- "Delete a backendService?" -> DELETE /projects/{project}/global/backendServices/{backendService}
- "Get backendService details?" -> GET /projects/{project}/global/backendServices/{backendService}
- "Partially update a backendService?" -> PATCH /projects/{project}/global/backendServices/{backendService}
- "Update a backendService?" -> PUT /projects/{project}/global/backendServices/{backendService}
- "Create a addSignedUrlKey?" -> POST /projects/{project}/global/backendServices/{backendService}/addSignedUrlKey
- "Create a deleteSignedUrlKey?" -> POST /projects/{project}/global/backendServices/{backendService}/deleteSignedUrlKey
- "Create a getHealth?" -> POST /projects/{project}/global/backendServices/{backendService}/getHealth
- "Create a setEdgeSecurityPolicy?" -> POST /projects/{project}/global/backendServices/{backendService}/setEdgeSecurityPolicy
- "Create a setSecurityPolicy?" -> POST /projects/{project}/global/backendServices/{backendService}/setSecurityPolicy
- "List all getIamPolicy?" -> GET /projects/{project}/global/backendServices/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/global/backendServices/{resource}/setIamPolicy
- "List all externalVpnGateways?" -> GET /projects/{project}/global/externalVpnGateways
- "Create a externalVpnGateway?" -> POST /projects/{project}/global/externalVpnGateways
- "Delete a externalVpnGateway?" -> DELETE /projects/{project}/global/externalVpnGateways/{externalVpnGateway}
- "Get externalVpnGateway details?" -> GET /projects/{project}/global/externalVpnGateways/{externalVpnGateway}
- "Create a setLabel?" -> POST /projects/{project}/global/externalVpnGateways/{resource}/setLabels
- "Create a testIamPermission?" -> POST /projects/{project}/global/externalVpnGateways/{resource}/testIamPermissions
- "List all firewallPolicies?" -> GET /projects/{project}/global/firewallPolicies
- "Create a firewallPolicy?" -> POST /projects/{project}/global/firewallPolicies
- "Delete a firewallPolicy?" -> DELETE /projects/{project}/global/firewallPolicies/{firewallPolicy}
- "Get firewallPolicy details?" -> GET /projects/{project}/global/firewallPolicies/{firewallPolicy}
- "Partially update a firewallPolicy?" -> PATCH /projects/{project}/global/firewallPolicies/{firewallPolicy}
- "Create a addAssociation?" -> POST /projects/{project}/global/firewallPolicies/{firewallPolicy}/addAssociation
- "Create a addRule?" -> POST /projects/{project}/global/firewallPolicies/{firewallPolicy}/addRule
- "Create a cloneRule?" -> POST /projects/{project}/global/firewallPolicies/{firewallPolicy}/cloneRules
- "List all getAssociation?" -> GET /projects/{project}/global/firewallPolicies/{firewallPolicy}/getAssociation
- "List all getRule?" -> GET /projects/{project}/global/firewallPolicies/{firewallPolicy}/getRule
- "Create a patchRule?" -> POST /projects/{project}/global/firewallPolicies/{firewallPolicy}/patchRule
- "Create a removeAssociation?" -> POST /projects/{project}/global/firewallPolicies/{firewallPolicy}/removeAssociation
- "Create a removeRule?" -> POST /projects/{project}/global/firewallPolicies/{firewallPolicy}/removeRule
- "List all getIamPolicy?" -> GET /projects/{project}/global/firewallPolicies/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/global/firewallPolicies/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/global/firewallPolicies/{resource}/testIamPermissions
- "List all firewalls?" -> GET /projects/{project}/global/firewalls
- "Create a firewall?" -> POST /projects/{project}/global/firewalls
- "Delete a firewall?" -> DELETE /projects/{project}/global/firewalls/{firewall}
- "Get firewall details?" -> GET /projects/{project}/global/firewalls/{firewall}
- "Partially update a firewall?" -> PATCH /projects/{project}/global/firewalls/{firewall}
- "Update a firewall?" -> PUT /projects/{project}/global/firewalls/{firewall}
- "List all forwardingRules?" -> GET /projects/{project}/global/forwardingRules
- "Create a forwardingRule?" -> POST /projects/{project}/global/forwardingRules
- "Delete a forwardingRule?" -> DELETE /projects/{project}/global/forwardingRules/{forwardingRule}
- "Get forwardingRule details?" -> GET /projects/{project}/global/forwardingRules/{forwardingRule}
- "Partially update a forwardingRule?" -> PATCH /projects/{project}/global/forwardingRules/{forwardingRule}
- "Create a setTarget?" -> POST /projects/{project}/global/forwardingRules/{forwardingRule}/setTarget
- "Create a setLabel?" -> POST /projects/{project}/global/forwardingRules/{resource}/setLabels
- "List all healthChecks?" -> GET /projects/{project}/global/healthChecks
- "Create a healthCheck?" -> POST /projects/{project}/global/healthChecks
- "Delete a healthCheck?" -> DELETE /projects/{project}/global/healthChecks/{healthCheck}
- "Get healthCheck details?" -> GET /projects/{project}/global/healthChecks/{healthCheck}
- "Partially update a healthCheck?" -> PATCH /projects/{project}/global/healthChecks/{healthCheck}
- "Update a healthCheck?" -> PUT /projects/{project}/global/healthChecks/{healthCheck}
- "List all httpHealthChecks?" -> GET /projects/{project}/global/httpHealthChecks
- "Create a httpHealthCheck?" -> POST /projects/{project}/global/httpHealthChecks
- "Delete a httpHealthCheck?" -> DELETE /projects/{project}/global/httpHealthChecks/{httpHealthCheck}
- "Get httpHealthCheck details?" -> GET /projects/{project}/global/httpHealthChecks/{httpHealthCheck}
- "Partially update a httpHealthCheck?" -> PATCH /projects/{project}/global/httpHealthChecks/{httpHealthCheck}
- "Update a httpHealthCheck?" -> PUT /projects/{project}/global/httpHealthChecks/{httpHealthCheck}
- "List all httpsHealthChecks?" -> GET /projects/{project}/global/httpsHealthChecks
- "Create a httpsHealthCheck?" -> POST /projects/{project}/global/httpsHealthChecks
- "Delete a httpsHealthCheck?" -> DELETE /projects/{project}/global/httpsHealthChecks/{httpsHealthCheck}
- "Get httpsHealthCheck details?" -> GET /projects/{project}/global/httpsHealthChecks/{httpsHealthCheck}
- "Partially update a httpsHealthCheck?" -> PATCH /projects/{project}/global/httpsHealthChecks/{httpsHealthCheck}
- "Update a httpsHealthCheck?" -> PUT /projects/{project}/global/httpsHealthChecks/{httpsHealthCheck}
- "List all images?" -> GET /projects/{project}/global/images
- "Create a image?" -> POST /projects/{project}/global/images
- "Get family details?" -> GET /projects/{project}/global/images/family/{family}
- "Delete a image?" -> DELETE /projects/{project}/global/images/{image}
- "Get image details?" -> GET /projects/{project}/global/images/{image}
- "Partially update a image?" -> PATCH /projects/{project}/global/images/{image}
- "Create a deprecate?" -> POST /projects/{project}/global/images/{image}/deprecate
- "List all getIamPolicy?" -> GET /projects/{project}/global/images/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/global/images/{resource}/setIamPolicy
- "Create a setLabel?" -> POST /projects/{project}/global/images/{resource}/setLabels
- "Create a testIamPermission?" -> POST /projects/{project}/global/images/{resource}/testIamPermissions
- "List all instanceTemplates?" -> GET /projects/{project}/global/instanceTemplates
- "Create a instanceTemplate?" -> POST /projects/{project}/global/instanceTemplates
- "Delete a instanceTemplate?" -> DELETE /projects/{project}/global/instanceTemplates/{instanceTemplate}
- "Get instanceTemplate details?" -> GET /projects/{project}/global/instanceTemplates/{instanceTemplate}
- "List all getIamPolicy?" -> GET /projects/{project}/global/instanceTemplates/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/global/instanceTemplates/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/global/instanceTemplates/{resource}/testIamPermissions
- "List all interconnectLocations?" -> GET /projects/{project}/global/interconnectLocations
- "Get interconnectLocation details?" -> GET /projects/{project}/global/interconnectLocations/{interconnectLocation}
- "List all interconnects?" -> GET /projects/{project}/global/interconnects
- "Create a interconnect?" -> POST /projects/{project}/global/interconnects
- "Delete a interconnect?" -> DELETE /projects/{project}/global/interconnects/{interconnect}
- "Get interconnect details?" -> GET /projects/{project}/global/interconnects/{interconnect}
- "Partially update a interconnect?" -> PATCH /projects/{project}/global/interconnects/{interconnect}
- "List all getDiagnostics?" -> GET /projects/{project}/global/interconnects/{interconnect}/getDiagnostics
- "Create a setLabel?" -> POST /projects/{project}/global/interconnects/{resource}/setLabels
- "Get licenseCode details?" -> GET /projects/{project}/global/licenseCodes/{licenseCode}
- "Create a testIamPermission?" -> POST /projects/{project}/global/licenseCodes/{resource}/testIamPermissions
- "List all licenses?" -> GET /projects/{project}/global/licenses
- "Create a license?" -> POST /projects/{project}/global/licenses
- "Delete a license?" -> DELETE /projects/{project}/global/licenses/{license}
- "Get license details?" -> GET /projects/{project}/global/licenses/{license}
- "List all getIamPolicy?" -> GET /projects/{project}/global/licenses/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/global/licenses/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/global/licenses/{resource}/testIamPermissions
- "List all machineImages?" -> GET /projects/{project}/global/machineImages
- "Create a machineImage?" -> POST /projects/{project}/global/machineImages
- "Delete a machineImage?" -> DELETE /projects/{project}/global/machineImages/{machineImage}
- "Get machineImage details?" -> GET /projects/{project}/global/machineImages/{machineImage}
- "List all getIamPolicy?" -> GET /projects/{project}/global/machineImages/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/global/machineImages/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/global/machineImages/{resource}/testIamPermissions
- "List all networkEndpointGroups?" -> GET /projects/{project}/global/networkEndpointGroups
- "Create a networkEndpointGroup?" -> POST /projects/{project}/global/networkEndpointGroups
- "Delete a networkEndpointGroup?" -> DELETE /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup}
- "Get networkEndpointGroup details?" -> GET /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup}
- "Create a attachNetworkEndpoint?" -> POST /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup}/attachNetworkEndpoints
- "Create a detachNetworkEndpoint?" -> POST /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup}/detachNetworkEndpoints
- "Create a listNetworkEndpoint?" -> POST /projects/{project}/global/networkEndpointGroups/{networkEndpointGroup}/listNetworkEndpoints
- "List all networks?" -> GET /projects/{project}/global/networks
- "Create a network?" -> POST /projects/{project}/global/networks
- "Delete a network?" -> DELETE /projects/{project}/global/networks/{network}
- "Get network details?" -> GET /projects/{project}/global/networks/{network}
- "Partially update a network?" -> PATCH /projects/{project}/global/networks/{network}
- "Create a addPeering?" -> POST /projects/{project}/global/networks/{network}/addPeering
- "List all getEffectiveFirewalls?" -> GET /projects/{project}/global/networks/{network}/getEffectiveFirewalls
- "List all listPeeringRoutes?" -> GET /projects/{project}/global/networks/{network}/listPeeringRoutes
- "Create a removePeering?" -> POST /projects/{project}/global/networks/{network}/removePeering
- "Create a switchToCustomMode?" -> POST /projects/{project}/global/networks/{network}/switchToCustomMode
- "List all operations?" -> GET /projects/{project}/global/operations
- "Delete a operation?" -> DELETE /projects/{project}/global/operations/{operation}
- "Get operation details?" -> GET /projects/{project}/global/operations/{operation}
- "Create a wait?" -> POST /projects/{project}/global/operations/{operation}/wait
- "List all publicAdvertisedPrefixes?" -> GET /projects/{project}/global/publicAdvertisedPrefixes
- "Create a publicAdvertisedPrefixe?" -> POST /projects/{project}/global/publicAdvertisedPrefixes
- "Delete a publicAdvertisedPrefixe?" -> DELETE /projects/{project}/global/publicAdvertisedPrefixes/{publicAdvertisedPrefix}
- "Get publicAdvertisedPrefixe details?" -> GET /projects/{project}/global/publicAdvertisedPrefixes/{publicAdvertisedPrefix}
- "Partially update a publicAdvertisedPrefixe?" -> PATCH /projects/{project}/global/publicAdvertisedPrefixes/{publicAdvertisedPrefix}
- "List all publicDelegatedPrefixes?" -> GET /projects/{project}/global/publicDelegatedPrefixes
- "Create a publicDelegatedPrefixe?" -> POST /projects/{project}/global/publicDelegatedPrefixes
- "Delete a publicDelegatedPrefixe?" -> DELETE /projects/{project}/global/publicDelegatedPrefixes/{publicDelegatedPrefix}
- "Get publicDelegatedPrefixe details?" -> GET /projects/{project}/global/publicDelegatedPrefixes/{publicDelegatedPrefix}
- "Partially update a publicDelegatedPrefixe?" -> PATCH /projects/{project}/global/publicDelegatedPrefixes/{publicDelegatedPrefix}
- "List all routes?" -> GET /projects/{project}/global/routes
- "Create a route?" -> POST /projects/{project}/global/routes
- "Delete a route?" -> DELETE /projects/{project}/global/routes/{route}
- "Get route details?" -> GET /projects/{project}/global/routes/{route}
- "List all securityPolicies?" -> GET /projects/{project}/global/securityPolicies
- "Create a securityPolicy?" -> POST /projects/{project}/global/securityPolicies
- "List all listPreconfiguredExpressionSets?" -> GET /projects/{project}/global/securityPolicies/listPreconfiguredExpressionSets
- "Create a setLabel?" -> POST /projects/{project}/global/securityPolicies/{resource}/setLabels
- "Delete a securityPolicy?" -> DELETE /projects/{project}/global/securityPolicies/{securityPolicy}
- "Get securityPolicy details?" -> GET /projects/{project}/global/securityPolicies/{securityPolicy}
- "Partially update a securityPolicy?" -> PATCH /projects/{project}/global/securityPolicies/{securityPolicy}
- "Create a addRule?" -> POST /projects/{project}/global/securityPolicies/{securityPolicy}/addRule
- "List all getRule?" -> GET /projects/{project}/global/securityPolicies/{securityPolicy}/getRule
- "Create a patchRule?" -> POST /projects/{project}/global/securityPolicies/{securityPolicy}/patchRule
- "Create a removeRule?" -> POST /projects/{project}/global/securityPolicies/{securityPolicy}/removeRule
- "List all snapshots?" -> GET /projects/{project}/global/snapshots
- "Create a snapshot?" -> POST /projects/{project}/global/snapshots
- "List all getIamPolicy?" -> GET /projects/{project}/global/snapshots/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/global/snapshots/{resource}/setIamPolicy
- "Create a setLabel?" -> POST /projects/{project}/global/snapshots/{resource}/setLabels
- "Create a testIamPermission?" -> POST /projects/{project}/global/snapshots/{resource}/testIamPermissions
- "Delete a snapshot?" -> DELETE /projects/{project}/global/snapshots/{snapshot}
- "Get snapshot details?" -> GET /projects/{project}/global/snapshots/{snapshot}
- "List all sslCertificates?" -> GET /projects/{project}/global/sslCertificates
- "Create a sslCertificate?" -> POST /projects/{project}/global/sslCertificates
- "Delete a sslCertificate?" -> DELETE /projects/{project}/global/sslCertificates/{sslCertificate}
- "Get sslCertificate details?" -> GET /projects/{project}/global/sslCertificates/{sslCertificate}
- "List all sslPolicies?" -> GET /projects/{project}/global/sslPolicies
- "Create a sslPolicy?" -> POST /projects/{project}/global/sslPolicies
- "List all listAvailableFeatures?" -> GET /projects/{project}/global/sslPolicies/listAvailableFeatures
- "Delete a sslPolicy?" -> DELETE /projects/{project}/global/sslPolicies/{sslPolicy}
- "Get sslPolicy details?" -> GET /projects/{project}/global/sslPolicies/{sslPolicy}
- "Partially update a sslPolicy?" -> PATCH /projects/{project}/global/sslPolicies/{sslPolicy}
- "List all targetGrpcProxies?" -> GET /projects/{project}/global/targetGrpcProxies
- "Create a targetGrpcProxy?" -> POST /projects/{project}/global/targetGrpcProxies
- "Delete a targetGrpcProxy?" -> DELETE /projects/{project}/global/targetGrpcProxies/{targetGrpcProxy}
- "Get targetGrpcProxy details?" -> GET /projects/{project}/global/targetGrpcProxies/{targetGrpcProxy}
- "Partially update a targetGrpcProxy?" -> PATCH /projects/{project}/global/targetGrpcProxies/{targetGrpcProxy}
- "List all targetHttpProxies?" -> GET /projects/{project}/global/targetHttpProxies
- "Create a targetHttpProxy?" -> POST /projects/{project}/global/targetHttpProxies
- "Delete a targetHttpProxy?" -> DELETE /projects/{project}/global/targetHttpProxies/{targetHttpProxy}
- "Get targetHttpProxy details?" -> GET /projects/{project}/global/targetHttpProxies/{targetHttpProxy}
- "Partially update a targetHttpProxy?" -> PATCH /projects/{project}/global/targetHttpProxies/{targetHttpProxy}
- "List all targetHttpsProxies?" -> GET /projects/{project}/global/targetHttpsProxies
- "Create a targetHttpsProxy?" -> POST /projects/{project}/global/targetHttpsProxies
- "Delete a targetHttpsProxy?" -> DELETE /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}
- "Get targetHttpsProxy details?" -> GET /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}
- "Partially update a targetHttpsProxy?" -> PATCH /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}
- "Create a setCertificateMap?" -> POST /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}/setCertificateMap
- "Create a setQuicOverride?" -> POST /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}/setQuicOverride
- "Create a setSslPolicy?" -> POST /projects/{project}/global/targetHttpsProxies/{targetHttpsProxy}/setSslPolicy
- "List all targetSslProxies?" -> GET /projects/{project}/global/targetSslProxies
- "Create a targetSslProxy?" -> POST /projects/{project}/global/targetSslProxies
- "Delete a targetSslProxy?" -> DELETE /projects/{project}/global/targetSslProxies/{targetSslProxy}
- "Get targetSslProxy details?" -> GET /projects/{project}/global/targetSslProxies/{targetSslProxy}
- "Create a setBackendService?" -> POST /projects/{project}/global/targetSslProxies/{targetSslProxy}/setBackendService
- "Create a setCertificateMap?" -> POST /projects/{project}/global/targetSslProxies/{targetSslProxy}/setCertificateMap
- "Create a setProxyHeader?" -> POST /projects/{project}/global/targetSslProxies/{targetSslProxy}/setProxyHeader
- "Create a setSslCertificate?" -> POST /projects/{project}/global/targetSslProxies/{targetSslProxy}/setSslCertificates
- "Create a setSslPolicy?" -> POST /projects/{project}/global/targetSslProxies/{targetSslProxy}/setSslPolicy
- "List all targetTcpProxies?" -> GET /projects/{project}/global/targetTcpProxies
- "Create a targetTcpProxy?" -> POST /projects/{project}/global/targetTcpProxies
- "Delete a targetTcpProxy?" -> DELETE /projects/{project}/global/targetTcpProxies/{targetTcpProxy}
- "Get targetTcpProxy details?" -> GET /projects/{project}/global/targetTcpProxies/{targetTcpProxy}
- "Create a setBackendService?" -> POST /projects/{project}/global/targetTcpProxies/{targetTcpProxy}/setBackendService
- "Create a setProxyHeader?" -> POST /projects/{project}/global/targetTcpProxies/{targetTcpProxy}/setProxyHeader
- "List all urlMaps?" -> GET /projects/{project}/global/urlMaps
- "Create a urlMap?" -> POST /projects/{project}/global/urlMaps
- "Delete a urlMap?" -> DELETE /projects/{project}/global/urlMaps/{urlMap}
- "Get urlMap details?" -> GET /projects/{project}/global/urlMaps/{urlMap}
- "Partially update a urlMap?" -> PATCH /projects/{project}/global/urlMaps/{urlMap}
- "Update a urlMap?" -> PUT /projects/{project}/global/urlMaps/{urlMap}
- "Create a invalidateCache?" -> POST /projects/{project}/global/urlMaps/{urlMap}/invalidateCache
- "Create a validate?" -> POST /projects/{project}/global/urlMaps/{urlMap}/validate
- "Create a listXpnHost?" -> POST /projects/{project}/listXpnHosts
- "Create a moveDisk?" -> POST /projects/{project}/moveDisk
- "Create a moveInstance?" -> POST /projects/{project}/moveInstance
- "List all regions?" -> GET /projects/{project}/regions
- "Get region details?" -> GET /projects/{project}/regions/{region}
- "List all addresses?" -> GET /projects/{project}/regions/{region}/addresses
- "Create a address?" -> POST /projects/{project}/regions/{region}/addresses
- "Delete a address?" -> DELETE /projects/{project}/regions/{region}/addresses/{address}
- "Get address details?" -> GET /projects/{project}/regions/{region}/addresses/{address}
- "Create a setLabel?" -> POST /projects/{project}/regions/{region}/addresses/{resource}/setLabels
- "List all autoscalers?" -> GET /projects/{project}/regions/{region}/autoscalers
- "Create a autoscaler?" -> POST /projects/{project}/regions/{region}/autoscalers
- "Delete a autoscaler?" -> DELETE /projects/{project}/regions/{region}/autoscalers/{autoscaler}
- "Get autoscaler details?" -> GET /projects/{project}/regions/{region}/autoscalers/{autoscaler}
- "List all backendServices?" -> GET /projects/{project}/regions/{region}/backendServices
- "Create a backendService?" -> POST /projects/{project}/regions/{region}/backendServices
- "Delete a backendService?" -> DELETE /projects/{project}/regions/{region}/backendServices/{backendService}
- "Get backendService details?" -> GET /projects/{project}/regions/{region}/backendServices/{backendService}
- "Partially update a backendService?" -> PATCH /projects/{project}/regions/{region}/backendServices/{backendService}
- "Update a backendService?" -> PUT /projects/{project}/regions/{region}/backendServices/{backendService}
- "Create a getHealth?" -> POST /projects/{project}/regions/{region}/backendServices/{backendService}/getHealth
- "List all getIamPolicy?" -> GET /projects/{project}/regions/{region}/backendServices/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/regions/{region}/backendServices/{resource}/setIamPolicy
- "List all commitments?" -> GET /projects/{project}/regions/{region}/commitments
- "Create a commitment?" -> POST /projects/{project}/regions/{region}/commitments
- "Get commitment details?" -> GET /projects/{project}/regions/{region}/commitments/{commitment}
- "Partially update a commitment?" -> PATCH /projects/{project}/regions/{region}/commitments/{commitment}
- "List all diskTypes?" -> GET /projects/{project}/regions/{region}/diskTypes
- "Get diskType details?" -> GET /projects/{project}/regions/{region}/diskTypes/{diskType}
- "List all disks?" -> GET /projects/{project}/regions/{region}/disks
- "Create a disk?" -> POST /projects/{project}/regions/{region}/disks
- "Delete a disk?" -> DELETE /projects/{project}/regions/{region}/disks/{disk}
- "Get disk details?" -> GET /projects/{project}/regions/{region}/disks/{disk}
- "Partially update a disk?" -> PATCH /projects/{project}/regions/{region}/disks/{disk}
- "Create a addResourcePolicy?" -> POST /projects/{project}/regions/{region}/disks/{disk}/addResourcePolicies
- "Create a createSnapshot?" -> POST /projects/{project}/regions/{region}/disks/{disk}/createSnapshot
- "Create a removeResourcePolicy?" -> POST /projects/{project}/regions/{region}/disks/{disk}/removeResourcePolicies
- "Create a resize?" -> POST /projects/{project}/regions/{region}/disks/{disk}/resize
- "List all getIamPolicy?" -> GET /projects/{project}/regions/{region}/disks/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/regions/{region}/disks/{resource}/setIamPolicy
- "Create a setLabel?" -> POST /projects/{project}/regions/{region}/disks/{resource}/setLabels
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/disks/{resource}/testIamPermissions
- "List all firewallPolicies?" -> GET /projects/{project}/regions/{region}/firewallPolicies
- "Create a firewallPolicy?" -> POST /projects/{project}/regions/{region}/firewallPolicies
- "List all getEffectiveFirewalls?" -> GET /projects/{project}/regions/{region}/firewallPolicies/getEffectiveFirewalls
- "Delete a firewallPolicy?" -> DELETE /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}
- "Get firewallPolicy details?" -> GET /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}
- "Partially update a firewallPolicy?" -> PATCH /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}
- "Create a addAssociation?" -> POST /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/addAssociation
- "Create a addRule?" -> POST /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/addRule
- "Create a cloneRule?" -> POST /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/cloneRules
- "List all getAssociation?" -> GET /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/getAssociation
- "List all getRule?" -> GET /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/getRule
- "Create a patchRule?" -> POST /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/patchRule
- "Create a removeAssociation?" -> POST /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/removeAssociation
- "Create a removeRule?" -> POST /projects/{project}/regions/{region}/firewallPolicies/{firewallPolicy}/removeRule
- "List all getIamPolicy?" -> GET /projects/{project}/regions/{region}/firewallPolicies/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/regions/{region}/firewallPolicies/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/firewallPolicies/{resource}/testIamPermissions
- "List all forwardingRules?" -> GET /projects/{project}/regions/{region}/forwardingRules
- "Create a forwardingRule?" -> POST /projects/{project}/regions/{region}/forwardingRules
- "Delete a forwardingRule?" -> DELETE /projects/{project}/regions/{region}/forwardingRules/{forwardingRule}
- "Get forwardingRule details?" -> GET /projects/{project}/regions/{region}/forwardingRules/{forwardingRule}
- "Partially update a forwardingRule?" -> PATCH /projects/{project}/regions/{region}/forwardingRules/{forwardingRule}
- "Create a setTarget?" -> POST /projects/{project}/regions/{region}/forwardingRules/{forwardingRule}/setTarget
- "Create a setLabel?" -> POST /projects/{project}/regions/{region}/forwardingRules/{resource}/setLabels
- "List all healthCheckServices?" -> GET /projects/{project}/regions/{region}/healthCheckServices
- "Create a healthCheckService?" -> POST /projects/{project}/regions/{region}/healthCheckServices
- "Delete a healthCheckService?" -> DELETE /projects/{project}/regions/{region}/healthCheckServices/{healthCheckService}
- "Get healthCheckService details?" -> GET /projects/{project}/regions/{region}/healthCheckServices/{healthCheckService}
- "Partially update a healthCheckService?" -> PATCH /projects/{project}/regions/{region}/healthCheckServices/{healthCheckService}
- "List all healthChecks?" -> GET /projects/{project}/regions/{region}/healthChecks
- "Create a healthCheck?" -> POST /projects/{project}/regions/{region}/healthChecks
- "Delete a healthCheck?" -> DELETE /projects/{project}/regions/{region}/healthChecks/{healthCheck}
- "Get healthCheck details?" -> GET /projects/{project}/regions/{region}/healthChecks/{healthCheck}
- "Partially update a healthCheck?" -> PATCH /projects/{project}/regions/{region}/healthChecks/{healthCheck}
- "Update a healthCheck?" -> PUT /projects/{project}/regions/{region}/healthChecks/{healthCheck}
- "List all instanceGroupManagers?" -> GET /projects/{project}/regions/{region}/instanceGroupManagers
- "Create a instanceGroupManager?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers
- "Delete a instanceGroupManager?" -> DELETE /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}
- "Get instanceGroupManager details?" -> GET /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}
- "Partially update a instanceGroupManager?" -> PATCH /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}
- "Create a abandonInstance?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/abandonInstances
- "Create a applyUpdatesToInstance?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/applyUpdatesToInstances
- "Create a createInstance?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/createInstances
- "Create a deleteInstance?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/deleteInstances
- "Create a deletePerInstanceConfig?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/deletePerInstanceConfigs
- "List all listErrors?" -> GET /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/listErrors
- "Create a listManagedInstance?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/listManagedInstances
- "Create a listPerInstanceConfig?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/listPerInstanceConfigs
- "Create a patchPerInstanceConfig?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/patchPerInstanceConfigs
- "Create a recreateInstance?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/recreateInstances
- "Create a resize?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/resize
- "Create a setInstanceTemplate?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/setInstanceTemplate
- "Create a setTargetPool?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/setTargetPools
- "Create a updatePerInstanceConfig?" -> POST /projects/{project}/regions/{region}/instanceGroupManagers/{instanceGroupManager}/updatePerInstanceConfigs
- "List all instanceGroups?" -> GET /projects/{project}/regions/{region}/instanceGroups
- "Get instanceGroup details?" -> GET /projects/{project}/regions/{region}/instanceGroups/{instanceGroup}
- "Create a listInstance?" -> POST /projects/{project}/regions/{region}/instanceGroups/{instanceGroup}/listInstances
- "Create a setNamedPort?" -> POST /projects/{project}/regions/{region}/instanceGroups/{instanceGroup}/setNamedPorts
- "Create a bulkInsert?" -> POST /projects/{project}/regions/{region}/instances/bulkInsert
- "List all interconnectAttachments?" -> GET /projects/{project}/regions/{region}/interconnectAttachments
- "Create a interconnectAttachment?" -> POST /projects/{project}/regions/{region}/interconnectAttachments
- "Delete a interconnectAttachment?" -> DELETE /projects/{project}/regions/{region}/interconnectAttachments/{interconnectAttachment}
- "Get interconnectAttachment details?" -> GET /projects/{project}/regions/{region}/interconnectAttachments/{interconnectAttachment}
- "Partially update a interconnectAttachment?" -> PATCH /projects/{project}/regions/{region}/interconnectAttachments/{interconnectAttachment}
- "Create a setLabel?" -> POST /projects/{project}/regions/{region}/interconnectAttachments/{resource}/setLabels
- "List all networkAttachments?" -> GET /projects/{project}/regions/{region}/networkAttachments
- "Create a networkAttachment?" -> POST /projects/{project}/regions/{region}/networkAttachments
- "Delete a networkAttachment?" -> DELETE /projects/{project}/regions/{region}/networkAttachments/{networkAttachment}
- "Get networkAttachment details?" -> GET /projects/{project}/regions/{region}/networkAttachments/{networkAttachment}
- "List all getIamPolicy?" -> GET /projects/{project}/regions/{region}/networkAttachments/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/regions/{region}/networkAttachments/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/networkAttachments/{resource}/testIamPermissions
- "Create a networkEdgeSecurityService?" -> POST /projects/{project}/regions/{region}/networkEdgeSecurityServices
- "Delete a networkEdgeSecurityService?" -> DELETE /projects/{project}/regions/{region}/networkEdgeSecurityServices/{networkEdgeSecurityService}
- "Get networkEdgeSecurityService details?" -> GET /projects/{project}/regions/{region}/networkEdgeSecurityServices/{networkEdgeSecurityService}
- "Partially update a networkEdgeSecurityService?" -> PATCH /projects/{project}/regions/{region}/networkEdgeSecurityServices/{networkEdgeSecurityService}
- "List all networkEndpointGroups?" -> GET /projects/{project}/regions/{region}/networkEndpointGroups
- "Create a networkEndpointGroup?" -> POST /projects/{project}/regions/{region}/networkEndpointGroups
- "Delete a networkEndpointGroup?" -> DELETE /projects/{project}/regions/{region}/networkEndpointGroups/{networkEndpointGroup}
- "Get networkEndpointGroup details?" -> GET /projects/{project}/regions/{region}/networkEndpointGroups/{networkEndpointGroup}
- "List all nodeTemplates?" -> GET /projects/{project}/regions/{region}/nodeTemplates
- "Create a nodeTemplate?" -> POST /projects/{project}/regions/{region}/nodeTemplates
- "Delete a nodeTemplate?" -> DELETE /projects/{project}/regions/{region}/nodeTemplates/{nodeTemplate}
- "Get nodeTemplate details?" -> GET /projects/{project}/regions/{region}/nodeTemplates/{nodeTemplate}
- "List all getIamPolicy?" -> GET /projects/{project}/regions/{region}/nodeTemplates/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/regions/{region}/nodeTemplates/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/nodeTemplates/{resource}/testIamPermissions
- "List all notificationEndpoints?" -> GET /projects/{project}/regions/{region}/notificationEndpoints
- "Create a notificationEndpoint?" -> POST /projects/{project}/regions/{region}/notificationEndpoints
- "Delete a notificationEndpoint?" -> DELETE /projects/{project}/regions/{region}/notificationEndpoints/{notificationEndpoint}
- "Get notificationEndpoint details?" -> GET /projects/{project}/regions/{region}/notificationEndpoints/{notificationEndpoint}
- "List all operations?" -> GET /projects/{project}/regions/{region}/operations
- "Delete a operation?" -> DELETE /projects/{project}/regions/{region}/operations/{operation}
- "Get operation details?" -> GET /projects/{project}/regions/{region}/operations/{operation}
- "Create a wait?" -> POST /projects/{project}/regions/{region}/operations/{operation}/wait
- "List all packetMirrorings?" -> GET /projects/{project}/regions/{region}/packetMirrorings
- "Create a packetMirroring?" -> POST /projects/{project}/regions/{region}/packetMirrorings
- "Delete a packetMirroring?" -> DELETE /projects/{project}/regions/{region}/packetMirrorings/{packetMirroring}
- "Get packetMirroring details?" -> GET /projects/{project}/regions/{region}/packetMirrorings/{packetMirroring}
- "Partially update a packetMirroring?" -> PATCH /projects/{project}/regions/{region}/packetMirrorings/{packetMirroring}
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/packetMirrorings/{resource}/testIamPermissions
- "List all publicDelegatedPrefixes?" -> GET /projects/{project}/regions/{region}/publicDelegatedPrefixes
- "Create a publicDelegatedPrefixe?" -> POST /projects/{project}/regions/{region}/publicDelegatedPrefixes
- "Delete a publicDelegatedPrefixe?" -> DELETE /projects/{project}/regions/{region}/publicDelegatedPrefixes/{publicDelegatedPrefix}
- "Get publicDelegatedPrefixe details?" -> GET /projects/{project}/regions/{region}/publicDelegatedPrefixes/{publicDelegatedPrefix}
- "Partially update a publicDelegatedPrefixe?" -> PATCH /projects/{project}/regions/{region}/publicDelegatedPrefixes/{publicDelegatedPrefix}
- "List all resourcePolicies?" -> GET /projects/{project}/regions/{region}/resourcePolicies
- "Create a resourcePolicy?" -> POST /projects/{project}/regions/{region}/resourcePolicies
- "Delete a resourcePolicy?" -> DELETE /projects/{project}/regions/{region}/resourcePolicies/{resourcePolicy}
- "Get resourcePolicy details?" -> GET /projects/{project}/regions/{region}/resourcePolicies/{resourcePolicy}
- "List all getIamPolicy?" -> GET /projects/{project}/regions/{region}/resourcePolicies/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/regions/{region}/resourcePolicies/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/resourcePolicies/{resource}/testIamPermissions
- "List all routers?" -> GET /projects/{project}/regions/{region}/routers
- "Create a router?" -> POST /projects/{project}/regions/{region}/routers
- "Delete a router?" -> DELETE /projects/{project}/regions/{region}/routers/{router}
- "Get router details?" -> GET /projects/{project}/regions/{region}/routers/{router}
- "Partially update a router?" -> PATCH /projects/{project}/regions/{region}/routers/{router}
- "Update a router?" -> PUT /projects/{project}/regions/{region}/routers/{router}
- "List all getNatMappingInfo?" -> GET /projects/{project}/regions/{region}/routers/{router}/getNatMappingInfo
- "List all getRouterStatus?" -> GET /projects/{project}/regions/{region}/routers/{router}/getRouterStatus
- "Create a preview?" -> POST /projects/{project}/regions/{region}/routers/{router}/preview
- "List all securityPolicies?" -> GET /projects/{project}/regions/{region}/securityPolicies
- "Create a securityPolicy?" -> POST /projects/{project}/regions/{region}/securityPolicies
- "Delete a securityPolicy?" -> DELETE /projects/{project}/regions/{region}/securityPolicies/{securityPolicy}
- "Get securityPolicy details?" -> GET /projects/{project}/regions/{region}/securityPolicies/{securityPolicy}
- "Partially update a securityPolicy?" -> PATCH /projects/{project}/regions/{region}/securityPolicies/{securityPolicy}
- "List all serviceAttachments?" -> GET /projects/{project}/regions/{region}/serviceAttachments
- "Create a serviceAttachment?" -> POST /projects/{project}/regions/{region}/serviceAttachments
- "List all getIamPolicy?" -> GET /projects/{project}/regions/{region}/serviceAttachments/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/regions/{region}/serviceAttachments/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/serviceAttachments/{resource}/testIamPermissions
- "Delete a serviceAttachment?" -> DELETE /projects/{project}/regions/{region}/serviceAttachments/{serviceAttachment}
- "Get serviceAttachment details?" -> GET /projects/{project}/regions/{region}/serviceAttachments/{serviceAttachment}
- "Partially update a serviceAttachment?" -> PATCH /projects/{project}/regions/{region}/serviceAttachments/{serviceAttachment}
- "List all sslCertificates?" -> GET /projects/{project}/regions/{region}/sslCertificates
- "Create a sslCertificate?" -> POST /projects/{project}/regions/{region}/sslCertificates
- "Delete a sslCertificate?" -> DELETE /projects/{project}/regions/{region}/sslCertificates/{sslCertificate}
- "Get sslCertificate details?" -> GET /projects/{project}/regions/{region}/sslCertificates/{sslCertificate}
- "List all sslPolicies?" -> GET /projects/{project}/regions/{region}/sslPolicies
- "Create a sslPolicy?" -> POST /projects/{project}/regions/{region}/sslPolicies
- "List all listAvailableFeatures?" -> GET /projects/{project}/regions/{region}/sslPolicies/listAvailableFeatures
- "Delete a sslPolicy?" -> DELETE /projects/{project}/regions/{region}/sslPolicies/{sslPolicy}
- "Get sslPolicy details?" -> GET /projects/{project}/regions/{region}/sslPolicies/{sslPolicy}
- "Partially update a sslPolicy?" -> PATCH /projects/{project}/regions/{region}/sslPolicies/{sslPolicy}
- "List all subnetworks?" -> GET /projects/{project}/regions/{region}/subnetworks
- "Create a subnetwork?" -> POST /projects/{project}/regions/{region}/subnetworks
- "List all getIamPolicy?" -> GET /projects/{project}/regions/{region}/subnetworks/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/regions/{region}/subnetworks/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/subnetworks/{resource}/testIamPermissions
- "Delete a subnetwork?" -> DELETE /projects/{project}/regions/{region}/subnetworks/{subnetwork}
- "Get subnetwork details?" -> GET /projects/{project}/regions/{region}/subnetworks/{subnetwork}
- "Partially update a subnetwork?" -> PATCH /projects/{project}/regions/{region}/subnetworks/{subnetwork}
- "Create a expandIpCidrRange?" -> POST /projects/{project}/regions/{region}/subnetworks/{subnetwork}/expandIpCidrRange
- "Create a setPrivateIpGoogleAccess?" -> POST /projects/{project}/regions/{region}/subnetworks/{subnetwork}/setPrivateIpGoogleAccess
- "List all targetHttpProxies?" -> GET /projects/{project}/regions/{region}/targetHttpProxies
- "Create a targetHttpProxy?" -> POST /projects/{project}/regions/{region}/targetHttpProxies
- "Delete a targetHttpProxy?" -> DELETE /projects/{project}/regions/{region}/targetHttpProxies/{targetHttpProxy}
- "Get targetHttpProxy details?" -> GET /projects/{project}/regions/{region}/targetHttpProxies/{targetHttpProxy}
- "Create a setUrlMap?" -> POST /projects/{project}/regions/{region}/targetHttpProxies/{targetHttpProxy}/setUrlMap
- "List all targetHttpsProxies?" -> GET /projects/{project}/regions/{region}/targetHttpsProxies
- "Create a targetHttpsProxy?" -> POST /projects/{project}/regions/{region}/targetHttpsProxies
- "Delete a targetHttpsProxy?" -> DELETE /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy}
- "Get targetHttpsProxy details?" -> GET /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy}
- "Partially update a targetHttpsProxy?" -> PATCH /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy}
- "Create a setSslCertificate?" -> POST /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy}/setSslCertificates
- "Create a setUrlMap?" -> POST /projects/{project}/regions/{region}/targetHttpsProxies/{targetHttpsProxy}/setUrlMap
- "List all targetPools?" -> GET /projects/{project}/regions/{region}/targetPools
- "Create a targetPool?" -> POST /projects/{project}/regions/{region}/targetPools
- "Delete a targetPool?" -> DELETE /projects/{project}/regions/{region}/targetPools/{targetPool}
- "Get targetPool details?" -> GET /projects/{project}/regions/{region}/targetPools/{targetPool}
- "Create a addHealthCheck?" -> POST /projects/{project}/regions/{region}/targetPools/{targetPool}/addHealthCheck
- "Create a addInstance?" -> POST /projects/{project}/regions/{region}/targetPools/{targetPool}/addInstance
- "Create a getHealth?" -> POST /projects/{project}/regions/{region}/targetPools/{targetPool}/getHealth
- "Create a removeHealthCheck?" -> POST /projects/{project}/regions/{region}/targetPools/{targetPool}/removeHealthCheck
- "Create a removeInstance?" -> POST /projects/{project}/regions/{region}/targetPools/{targetPool}/removeInstance
- "Create a setBackup?" -> POST /projects/{project}/regions/{region}/targetPools/{targetPool}/setBackup
- "List all targetTcpProxies?" -> GET /projects/{project}/regions/{region}/targetTcpProxies
- "Create a targetTcpProxy?" -> POST /projects/{project}/regions/{region}/targetTcpProxies
- "Delete a targetTcpProxy?" -> DELETE /projects/{project}/regions/{region}/targetTcpProxies/{targetTcpProxy}
- "Get targetTcpProxy details?" -> GET /projects/{project}/regions/{region}/targetTcpProxies/{targetTcpProxy}
- "List all targetVpnGateways?" -> GET /projects/{project}/regions/{region}/targetVpnGateways
- "Create a targetVpnGateway?" -> POST /projects/{project}/regions/{region}/targetVpnGateways
- "Create a setLabel?" -> POST /projects/{project}/regions/{region}/targetVpnGateways/{resource}/setLabels
- "Delete a targetVpnGateway?" -> DELETE /projects/{project}/regions/{region}/targetVpnGateways/{targetVpnGateway}
- "Get targetVpnGateway details?" -> GET /projects/{project}/regions/{region}/targetVpnGateways/{targetVpnGateway}
- "List all urlMaps?" -> GET /projects/{project}/regions/{region}/urlMaps
- "Create a urlMap?" -> POST /projects/{project}/regions/{region}/urlMaps
- "Delete a urlMap?" -> DELETE /projects/{project}/regions/{region}/urlMaps/{urlMap}
- "Get urlMap details?" -> GET /projects/{project}/regions/{region}/urlMaps/{urlMap}
- "Partially update a urlMap?" -> PATCH /projects/{project}/regions/{region}/urlMaps/{urlMap}
- "Update a urlMap?" -> PUT /projects/{project}/regions/{region}/urlMaps/{urlMap}
- "Create a validate?" -> POST /projects/{project}/regions/{region}/urlMaps/{urlMap}/validate
- "List all vpnGateways?" -> GET /projects/{project}/regions/{region}/vpnGateways
- "Create a vpnGateway?" -> POST /projects/{project}/regions/{region}/vpnGateways
- "Create a setLabel?" -> POST /projects/{project}/regions/{region}/vpnGateways/{resource}/setLabels
- "Create a testIamPermission?" -> POST /projects/{project}/regions/{region}/vpnGateways/{resource}/testIamPermissions
- "Delete a vpnGateway?" -> DELETE /projects/{project}/regions/{region}/vpnGateways/{vpnGateway}
- "Get vpnGateway details?" -> GET /projects/{project}/regions/{region}/vpnGateways/{vpnGateway}
- "List all getStatus?" -> GET /projects/{project}/regions/{region}/vpnGateways/{vpnGateway}/getStatus
- "List all vpnTunnels?" -> GET /projects/{project}/regions/{region}/vpnTunnels
- "Create a vpnTunnel?" -> POST /projects/{project}/regions/{region}/vpnTunnels
- "Create a setLabel?" -> POST /projects/{project}/regions/{region}/vpnTunnels/{resource}/setLabels
- "Delete a vpnTunnel?" -> DELETE /projects/{project}/regions/{region}/vpnTunnels/{vpnTunnel}
- "Get vpnTunnel details?" -> GET /projects/{project}/regions/{region}/vpnTunnels/{vpnTunnel}
- "Create a setCommonInstanceMetadata?" -> POST /projects/{project}/setCommonInstanceMetadata
- "Create a setDefaultNetworkTier?" -> POST /projects/{project}/setDefaultNetworkTier
- "Create a setUsageExportBucket?" -> POST /projects/{project}/setUsageExportBucket
- "Create a setUrlMap?" -> POST /projects/{project}/targetHttpProxies/{targetHttpProxy}/setUrlMap
- "Create a setSslCertificate?" -> POST /projects/{project}/targetHttpsProxies/{targetHttpsProxy}/setSslCertificates
- "Create a setUrlMap?" -> POST /projects/{project}/targetHttpsProxies/{targetHttpsProxy}/setUrlMap
- "List all zones?" -> GET /projects/{project}/zones
- "Get zone details?" -> GET /projects/{project}/zones/{zone}
- "List all acceleratorTypes?" -> GET /projects/{project}/zones/{zone}/acceleratorTypes
- "Get acceleratorType details?" -> GET /projects/{project}/zones/{zone}/acceleratorTypes/{acceleratorType}
- "List all autoscalers?" -> GET /projects/{project}/zones/{zone}/autoscalers
- "Create a autoscaler?" -> POST /projects/{project}/zones/{zone}/autoscalers
- "Delete a autoscaler?" -> DELETE /projects/{project}/zones/{zone}/autoscalers/{autoscaler}
- "Get autoscaler details?" -> GET /projects/{project}/zones/{zone}/autoscalers/{autoscaler}
- "List all diskTypes?" -> GET /projects/{project}/zones/{zone}/diskTypes
- "Get diskType details?" -> GET /projects/{project}/zones/{zone}/diskTypes/{diskType}
- "List all disks?" -> GET /projects/{project}/zones/{zone}/disks
- "Create a disk?" -> POST /projects/{project}/zones/{zone}/disks
- "Delete a disk?" -> DELETE /projects/{project}/zones/{zone}/disks/{disk}
- "Get disk details?" -> GET /projects/{project}/zones/{zone}/disks/{disk}
- "Partially update a disk?" -> PATCH /projects/{project}/zones/{zone}/disks/{disk}
- "Create a addResourcePolicy?" -> POST /projects/{project}/zones/{zone}/disks/{disk}/addResourcePolicies
- "Create a createSnapshot?" -> POST /projects/{project}/zones/{zone}/disks/{disk}/createSnapshot
- "Create a removeResourcePolicy?" -> POST /projects/{project}/zones/{zone}/disks/{disk}/removeResourcePolicies
- "Create a resize?" -> POST /projects/{project}/zones/{zone}/disks/{disk}/resize
- "List all getIamPolicy?" -> GET /projects/{project}/zones/{zone}/disks/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/zones/{zone}/disks/{resource}/setIamPolicy
- "Create a setLabel?" -> POST /projects/{project}/zones/{zone}/disks/{resource}/setLabels
- "Create a testIamPermission?" -> POST /projects/{project}/zones/{zone}/disks/{resource}/testIamPermissions
- "Get imageFamilyView details?" -> GET /projects/{project}/zones/{zone}/imageFamilyViews/{family}
- "List all instanceGroupManagers?" -> GET /projects/{project}/zones/{zone}/instanceGroupManagers
- "Create a instanceGroupManager?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers
- "Delete a instanceGroupManager?" -> DELETE /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}
- "Get instanceGroupManager details?" -> GET /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}
- "Partially update a instanceGroupManager?" -> PATCH /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}
- "Create a abandonInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/abandonInstances
- "Create a applyUpdatesToInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/applyUpdatesToInstances
- "Create a createInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/createInstances
- "Create a deleteInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/deleteInstances
- "Create a deletePerInstanceConfig?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/deletePerInstanceConfigs
- "List all listErrors?" -> GET /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/listErrors
- "Create a listManagedInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/listManagedInstances
- "Create a listPerInstanceConfig?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/listPerInstanceConfigs
- "Create a patchPerInstanceConfig?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/patchPerInstanceConfigs
- "Create a recreateInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/recreateInstances
- "Create a resize?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/resize
- "Create a setInstanceTemplate?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/setInstanceTemplate
- "Create a setTargetPool?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/setTargetPools
- "Create a updatePerInstanceConfig?" -> POST /projects/{project}/zones/{zone}/instanceGroupManagers/{instanceGroupManager}/updatePerInstanceConfigs
- "List all instanceGroups?" -> GET /projects/{project}/zones/{zone}/instanceGroups
- "Create a instanceGroup?" -> POST /projects/{project}/zones/{zone}/instanceGroups
- "Delete a instanceGroup?" -> DELETE /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}
- "Get instanceGroup details?" -> GET /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}
- "Create a addInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}/addInstances
- "Create a listInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}/listInstances
- "Create a removeInstance?" -> POST /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}/removeInstances
- "Create a setNamedPort?" -> POST /projects/{project}/zones/{zone}/instanceGroups/{instanceGroup}/setNamedPorts
- "List all instances?" -> GET /projects/{project}/zones/{zone}/instances
- "Create a instance?" -> POST /projects/{project}/zones/{zone}/instances
- "Create a bulkInsert?" -> POST /projects/{project}/zones/{zone}/instances/bulkInsert
- "Delete a instance?" -> DELETE /projects/{project}/zones/{zone}/instances/{instance}
- "Get instance details?" -> GET /projects/{project}/zones/{zone}/instances/{instance}
- "Update a instance?" -> PUT /projects/{project}/zones/{zone}/instances/{instance}
- "Create a addAccessConfig?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/addAccessConfig
- "Create a addResourcePolicy?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/addResourcePolicies
- "Create a attachDisk?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/attachDisk
- "Create a deleteAccessConfig?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/deleteAccessConfig
- "Create a detachDisk?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/detachDisk
- "List all getEffectiveFirewalls?" -> GET /projects/{project}/zones/{zone}/instances/{instance}/getEffectiveFirewalls
- "List all getGuestAttributes?" -> GET /projects/{project}/zones/{zone}/instances/{instance}/getGuestAttributes
- "List all getShieldedInstanceIdentity?" -> GET /projects/{project}/zones/{zone}/instances/{instance}/getShieldedInstanceIdentity
- "List all referrers?" -> GET /projects/{project}/zones/{zone}/instances/{instance}/referrers
- "Create a removeResourcePolicy?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/removeResourcePolicies
- "Create a reset?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/reset
- "Create a resume?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/resume
- "List all screenshot?" -> GET /projects/{project}/zones/{zone}/instances/{instance}/screenshot
- "Create a sendDiagnosticInterrupt?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/sendDiagnosticInterrupt
- "List all serialPort?" -> GET /projects/{project}/zones/{zone}/instances/{instance}/serialPort
- "Create a setDiskAutoDelete?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setDiskAutoDelete
- "Create a setLabel?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setLabels
- "Create a setMachineResource?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setMachineResources
- "Create a setMachineType?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setMachineType
- "Create a setMetadata?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setMetadata
- "Create a setMinCpuPlatform?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setMinCpuPlatform
- "Create a setName?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setName
- "Create a setScheduling?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setScheduling
- "Create a setServiceAccount?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setServiceAccount
- "Create a setTag?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/setTags
- "Create a simulateMaintenanceEvent?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/simulateMaintenanceEvent
- "Create a start?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/start
- "Create a startWithEncryptionKey?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/startWithEncryptionKey
- "Create a stop?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/stop
- "Create a suspend?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/suspend
- "Create a updateAccessConfig?" -> POST /projects/{project}/zones/{zone}/instances/{instance}/updateAccessConfig
- "List all getIamPolicy?" -> GET /projects/{project}/zones/{zone}/instances/{resource}/getIamPolicy
- "Create a setDeletionProtection?" -> POST /projects/{project}/zones/{zone}/instances/{resource}/setDeletionProtection
- "Create a setIamPolicy?" -> POST /projects/{project}/zones/{zone}/instances/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/zones/{zone}/instances/{resource}/testIamPermissions
- "List all machineTypes?" -> GET /projects/{project}/zones/{zone}/machineTypes
- "Get machineType details?" -> GET /projects/{project}/zones/{zone}/machineTypes/{machineType}
- "List all networkEndpointGroups?" -> GET /projects/{project}/zones/{zone}/networkEndpointGroups
- "Create a networkEndpointGroup?" -> POST /projects/{project}/zones/{zone}/networkEndpointGroups
- "Delete a networkEndpointGroup?" -> DELETE /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup}
- "Get networkEndpointGroup details?" -> GET /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup}
- "Create a attachNetworkEndpoint?" -> POST /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup}/attachNetworkEndpoints
- "Create a detachNetworkEndpoint?" -> POST /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup}/detachNetworkEndpoints
- "Create a listNetworkEndpoint?" -> POST /projects/{project}/zones/{zone}/networkEndpointGroups/{networkEndpointGroup}/listNetworkEndpoints
- "Create a testIamPermission?" -> POST /projects/{project}/zones/{zone}/networkEndpointGroups/{resource}/testIamPermissions
- "List all nodeGroups?" -> GET /projects/{project}/zones/{zone}/nodeGroups
- "Create a nodeGroup?" -> POST /projects/{project}/zones/{zone}/nodeGroups
- "Delete a nodeGroup?" -> DELETE /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}
- "Get nodeGroup details?" -> GET /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}
- "Partially update a nodeGroup?" -> PATCH /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}
- "Create a addNode?" -> POST /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/addNodes
- "Create a deleteNode?" -> POST /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/deleteNodes
- "Create a listNode?" -> POST /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/listNodes
- "Create a setNodeTemplate?" -> POST /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/setNodeTemplate
- "Create a simulateMaintenanceEvent?" -> POST /projects/{project}/zones/{zone}/nodeGroups/{nodeGroup}/simulateMaintenanceEvent
- "List all getIamPolicy?" -> GET /projects/{project}/zones/{zone}/nodeGroups/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/zones/{zone}/nodeGroups/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/zones/{zone}/nodeGroups/{resource}/testIamPermissions
- "List all nodeTypes?" -> GET /projects/{project}/zones/{zone}/nodeTypes
- "Get nodeType details?" -> GET /projects/{project}/zones/{zone}/nodeTypes/{nodeType}
- "List all operations?" -> GET /projects/{project}/zones/{zone}/operations
- "Delete a operation?" -> DELETE /projects/{project}/zones/{zone}/operations/{operation}
- "Get operation details?" -> GET /projects/{project}/zones/{zone}/operations/{operation}
- "Create a wait?" -> POST /projects/{project}/zones/{zone}/operations/{operation}/wait
- "List all reservations?" -> GET /projects/{project}/zones/{zone}/reservations
- "Create a reservation?" -> POST /projects/{project}/zones/{zone}/reservations
- "Delete a reservation?" -> DELETE /projects/{project}/zones/{zone}/reservations/{reservation}
- "Get reservation details?" -> GET /projects/{project}/zones/{zone}/reservations/{reservation}
- "Partially update a reservation?" -> PATCH /projects/{project}/zones/{zone}/reservations/{reservation}
- "Create a resize?" -> POST /projects/{project}/zones/{zone}/reservations/{reservation}/resize
- "List all getIamPolicy?" -> GET /projects/{project}/zones/{zone}/reservations/{resource}/getIamPolicy
- "Create a setIamPolicy?" -> POST /projects/{project}/zones/{zone}/reservations/{resource}/setIamPolicy
- "Create a testIamPermission?" -> POST /projects/{project}/zones/{zone}/reservations/{resource}/testIamPermissions
- "List all targetInstances?" -> GET /projects/{project}/zones/{zone}/targetInstances
- "Create a targetInstance?" -> POST /projects/{project}/zones/{zone}/targetInstances
- "Delete a targetInstance?" -> DELETE /projects/{project}/zones/{zone}/targetInstances/{targetInstance}
- "Get targetInstance details?" -> GET /projects/{project}/zones/{zone}/targetInstances/{targetInstance}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
