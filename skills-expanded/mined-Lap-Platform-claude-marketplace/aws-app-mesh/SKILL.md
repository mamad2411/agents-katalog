---
name: aws-app-mesh
description: "AWS App Mesh API skill. Use when working with AWS App Mesh for meshes, tags, tag. Covers 38 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS App Mesh
API version: 2019-01-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v20190125/meshes -- verify access

## Endpoints

38 endpoints across 4 groups. See references/api-spec.lap for full details.

### meshes
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes | Creates a gateway route. A gateway route is attached to a virtual gateway and routes traffic to an existing virtual service. If a route matches a request, it can distribute traffic to a target virtual service. For more information about gateway routes, see Gateway routes. |
| PUT | /v20190125/meshes | Creates a service mesh.  A service mesh is a logical boundary for network traffic between services that are represented by resources within the mesh. After you create your service mesh, you can create virtual services, virtual nodes, virtual routers, and routes to distribute traffic between the applications in your mesh. For more information about service meshes, see Service meshes. |
| PUT | /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes | Creates a route that is associated with a virtual router.  You can route several different protocols and define a retry policy for a route. Traffic can be routed to one or more virtual nodes. For more information about routes, see Routes. |
| PUT | /v20190125/meshes/{meshName}/virtualGateways | Creates a virtual gateway. A virtual gateway allows resources outside your mesh to communicate to resources that are inside your mesh. The virtual gateway represents an Envoy proxy running in an Amazon ECS task, in a Kubernetes service, or on an Amazon EC2 instance. Unlike a virtual node, which represents an Envoy running with an application, a virtual gateway represents Envoy deployed by itself. For more information about virtual gateways, see Virtual gateways. |
| PUT | /v20190125/meshes/{meshName}/virtualNodes | Creates a virtual node within a service mesh.  A virtual node acts as a logical pointer to a particular task group, such as an Amazon ECS service or a Kubernetes deployment. When you create a virtual node, you can specify the service discovery information for your task group, and whether the proxy running in a task group will communicate with other proxies using Transport Layer Security (TLS). You define a listener for any inbound traffic that your virtual node expects. Any virtual service that your virtual node expects to communicate to is specified as a backend. The response metadata for your new virtual node contains the arn that is associated with the virtual node. Set this value to the full ARN; for example, arn:aws:appmesh:us-west-2:123456789012:myMesh/default/virtualNode/myApp) as the APPMESH_RESOURCE_ARN environment variable for your task group's Envoy proxy container in your task definition or pod spec. This is then mapped to the node.id and node.cluster Envoy parameters.  By default, App Mesh uses the name of the resource you specified in APPMESH_RESOURCE_ARN when Envoy is referring to itself in metrics and traces. You can override this behavior by setting the APPMESH_RESOURCE_CLUSTER environment variable with your own name.  For more information about virtual nodes, see Virtual nodes. You must be using 1.15.0 or later of the Envoy image when setting these variables. For more information aboutApp Mesh Envoy variables, see Envoy image in the App Mesh User Guide. |
| PUT | /v20190125/meshes/{meshName}/virtualRouters | Creates a virtual router within a service mesh. Specify a listener for any inbound traffic that your virtual router receives. Create a virtual router for each protocol and port that you need to route. Virtual routers handle traffic for one or more virtual services within your mesh. After you create your virtual router, create and associate routes for your virtual router that direct incoming requests to different virtual nodes. For more information about virtual routers, see Virtual routers. |
| PUT | /v20190125/meshes/{meshName}/virtualServices | Creates a virtual service within a service mesh. A virtual service is an abstraction of a real service that is provided by a virtual node directly or indirectly by means of a virtual router. Dependent services call your virtual service by its virtualServiceName, and those requests are routed to the virtual node or virtual router that is specified as the provider for the virtual service. For more information about virtual services, see Virtual services. |
| DELETE | /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes/{gatewayRouteName} | Deletes an existing gateway route. |
| DELETE | /v20190125/meshes/{meshName} | Deletes an existing service mesh. You must delete all resources (virtual services, routes, virtual routers, and virtual nodes) in the service mesh before you can delete the mesh itself. |
| DELETE | /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes/{routeName} | Deletes an existing route. |
| DELETE | /v20190125/meshes/{meshName}/virtualGateways/{virtualGatewayName} | Deletes an existing virtual gateway. You cannot delete a virtual gateway if any gateway routes are associated to it. |
| DELETE | /v20190125/meshes/{meshName}/virtualNodes/{virtualNodeName} | Deletes an existing virtual node. You must delete any virtual services that list a virtual node as a service provider before you can delete the virtual node itself. |
| DELETE | /v20190125/meshes/{meshName}/virtualRouters/{virtualRouterName} | Deletes an existing virtual router. You must delete any routes associated with the virtual router before you can delete the router itself. |
| DELETE | /v20190125/meshes/{meshName}/virtualServices/{virtualServiceName} | Deletes an existing virtual service. |
| GET | /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes/{gatewayRouteName} | Describes an existing gateway route. |
| GET | /v20190125/meshes/{meshName} | Describes an existing service mesh. |
| GET | /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes/{routeName} | Describes an existing route. |
| GET | /v20190125/meshes/{meshName}/virtualGateways/{virtualGatewayName} | Describes an existing virtual gateway. |
| GET | /v20190125/meshes/{meshName}/virtualNodes/{virtualNodeName} | Describes an existing virtual node. |
| GET | /v20190125/meshes/{meshName}/virtualRouters/{virtualRouterName} | Describes an existing virtual router. |
| GET | /v20190125/meshes/{meshName}/virtualServices/{virtualServiceName} | Describes an existing virtual service. |
| GET | /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes | Returns a list of existing gateway routes that are associated to a virtual gateway. |
| GET | /v20190125/meshes | Returns a list of existing service meshes. |
| GET | /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes | Returns a list of existing routes in a service mesh. |
| GET | /v20190125/meshes/{meshName}/virtualGateways | Returns a list of existing virtual gateways in a service mesh. |
| GET | /v20190125/meshes/{meshName}/virtualNodes | Returns a list of existing virtual nodes. |
| GET | /v20190125/meshes/{meshName}/virtualRouters | Returns a list of existing virtual routers in a service mesh. |
| GET | /v20190125/meshes/{meshName}/virtualServices | Returns a list of existing virtual services in a service mesh. |
| PUT | /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes/{gatewayRouteName} | Updates an existing gateway route that is associated to a specified virtual gateway in a service mesh. |
| PUT | /v20190125/meshes/{meshName} | Updates an existing service mesh. |
| PUT | /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes/{routeName} | Updates an existing route for a specified service mesh and virtual router. |
| PUT | /v20190125/meshes/{meshName}/virtualGateways/{virtualGatewayName} | Updates an existing virtual gateway in a specified service mesh. |
| PUT | /v20190125/meshes/{meshName}/virtualNodes/{virtualNodeName} | Updates an existing virtual node in a specified service mesh. |
| PUT | /v20190125/meshes/{meshName}/virtualRouters/{virtualRouterName} | Updates an existing virtual router in a specified service mesh. |
| PUT | /v20190125/meshes/{meshName}/virtualServices/{virtualServiceName} | Updates an existing virtual service in a specified service mesh. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v20190125/tags | List the tags for an App Mesh resource. |

### tag
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v20190125/tag | Associates the specified tags to a resource with the specified resourceArn. If existing tags on a resource aren't specified in the request parameters, they aren't changed. When a resource is deleted, the tags associated with that resource are also deleted. |

### untag
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v20190125/untag | Deletes specified tags from a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a gatewayRoute?" -> DELETE /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes/{gatewayRouteName}
- "Delete a meshe?" -> DELETE /v20190125/meshes/{meshName}
- "Delete a route?" -> DELETE /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes/{routeName}
- "Delete a virtualGateway?" -> DELETE /v20190125/meshes/{meshName}/virtualGateways/{virtualGatewayName}
- "Delete a virtualNode?" -> DELETE /v20190125/meshes/{meshName}/virtualNodes/{virtualNodeName}
- "Delete a virtualRouter?" -> DELETE /v20190125/meshes/{meshName}/virtualRouters/{virtualRouterName}
- "Delete a virtualService?" -> DELETE /v20190125/meshes/{meshName}/virtualServices/{virtualServiceName}
- "Get gatewayRoute details?" -> GET /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes/{gatewayRouteName}
- "Get meshe details?" -> GET /v20190125/meshes/{meshName}
- "Get route details?" -> GET /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes/{routeName}
- "Get virtualGateway details?" -> GET /v20190125/meshes/{meshName}/virtualGateways/{virtualGatewayName}
- "Get virtualNode details?" -> GET /v20190125/meshes/{meshName}/virtualNodes/{virtualNodeName}
- "Get virtualRouter details?" -> GET /v20190125/meshes/{meshName}/virtualRouters/{virtualRouterName}
- "Get virtualService details?" -> GET /v20190125/meshes/{meshName}/virtualServices/{virtualServiceName}
- "List all gatewayRoutes?" -> GET /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes
- "List all meshes?" -> GET /v20190125/meshes
- "List all routes?" -> GET /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes
- "List all tags?" -> GET /v20190125/tags
- "List all virtualGateways?" -> GET /v20190125/meshes/{meshName}/virtualGateways
- "List all virtualNodes?" -> GET /v20190125/meshes/{meshName}/virtualNodes
- "List all virtualRouters?" -> GET /v20190125/meshes/{meshName}/virtualRouters
- "List all virtualServices?" -> GET /v20190125/meshes/{meshName}/virtualServices
- "Update a gatewayRoute?" -> PUT /v20190125/meshes/{meshName}/virtualGateway/{virtualGatewayName}/gatewayRoutes/{gatewayRouteName}
- "Update a meshe?" -> PUT /v20190125/meshes/{meshName}
- "Update a route?" -> PUT /v20190125/meshes/{meshName}/virtualRouter/{virtualRouterName}/routes/{routeName}
- "Update a virtualGateway?" -> PUT /v20190125/meshes/{meshName}/virtualGateways/{virtualGatewayName}
- "Update a virtualNode?" -> PUT /v20190125/meshes/{meshName}/virtualNodes/{virtualNodeName}
- "Update a virtualRouter?" -> PUT /v20190125/meshes/{meshName}/virtualRouters/{virtualRouterName}
- "Update a virtualService?" -> PUT /v20190125/meshes/{meshName}/virtualServices/{virtualServiceName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
