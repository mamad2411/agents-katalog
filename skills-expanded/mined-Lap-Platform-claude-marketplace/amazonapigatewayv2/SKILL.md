---
name: amazonapigatewayv2
description: "AmazonApiGatewayV2 API skill. Use when working with AmazonApiGatewayV2 for apis, domainnames, vpclinks. Covers 72 endpoints."
version: 1.0.0
generator: lapsh
---

# AmazonApiGatewayV2
API version: 2018-11-29

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v2/apis -- verify access
3. POST /v2/apis -- create first apis

## Endpoints

72 endpoints across 4 groups. See references/api-spec.lap for full details.

### apis
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/apis | Creates an Api resource. |
| POST | /v2/apis/{apiId}/authorizers | Creates an Authorizer for an API. |
| POST | /v2/apis/{apiId}/deployments | Creates a Deployment for an API. |
| POST | /v2/apis/{apiId}/integrations | Creates an Integration. |
| POST | /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses | Creates an IntegrationResponses. |
| POST | /v2/apis/{apiId}/models | Creates a Model for an API. |
| POST | /v2/apis/{apiId}/routes | Creates a Route for an API. |
| POST | /v2/apis/{apiId}/routes/{routeId}/routeresponses | Creates a RouteResponse for a Route. |
| POST | /v2/apis/{apiId}/stages | Creates a Stage for an API. |
| DELETE | /v2/apis/{apiId}/stages/{stageName}/accesslogsettings | Deletes the AccessLogSettings for a Stage. To disable access logging for a Stage, delete its AccessLogSettings. |
| DELETE | /v2/apis/{apiId} | Deletes an Api resource. |
| DELETE | /v2/apis/{apiId}/authorizers/{authorizerId} | Deletes an Authorizer. |
| DELETE | /v2/apis/{apiId}/cors | Deletes a CORS configuration. |
| DELETE | /v2/apis/{apiId}/deployments/{deploymentId} | Deletes a Deployment. |
| DELETE | /v2/apis/{apiId}/integrations/{integrationId} | Deletes an Integration. |
| DELETE | /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses/{integrationResponseId} | Deletes an IntegrationResponses. |
| DELETE | /v2/apis/{apiId}/models/{modelId} | Deletes a Model. |
| DELETE | /v2/apis/{apiId}/routes/{routeId} | Deletes a Route. |
| DELETE | /v2/apis/{apiId}/routes/{routeId}/requestparameters/{requestParameterKey} | Deletes a route request parameter. Supported only for WebSocket APIs. |
| DELETE | /v2/apis/{apiId}/routes/{routeId}/routeresponses/{routeResponseId} | Deletes a RouteResponse. |
| DELETE | /v2/apis/{apiId}/stages/{stageName}/routesettings/{routeKey} | Deletes the RouteSettings for a stage. |
| DELETE | /v2/apis/{apiId}/stages/{stageName} | Deletes a Stage. |
| GET | /v2/apis/{apiId}/exports/{specification} |  |
| DELETE | /v2/apis/{apiId}/stages/{stageName}/cache/authorizers | Resets all authorizer cache entries on a stage. Supported only for HTTP APIs. |
| GET | /v2/apis/{apiId} | Gets an Api resource. |
| GET | /v2/apis | Gets a collection of Api resources. |
| GET | /v2/apis/{apiId}/authorizers/{authorizerId} | Gets an Authorizer. |
| GET | /v2/apis/{apiId}/authorizers | Gets the Authorizers for an API. |
| GET | /v2/apis/{apiId}/deployments/{deploymentId} | Gets a Deployment. |
| GET | /v2/apis/{apiId}/deployments | Gets the Deployments for an API. |
| GET | /v2/apis/{apiId}/integrations/{integrationId} | Gets an Integration. |
| GET | /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses/{integrationResponseId} | Gets an IntegrationResponses. |
| GET | /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses | Gets the IntegrationResponses for an Integration. |
| GET | /v2/apis/{apiId}/integrations | Gets the Integrations for an API. |
| GET | /v2/apis/{apiId}/models/{modelId} | Gets a Model. |
| GET | /v2/apis/{apiId}/models/{modelId}/template | Gets a model template. |
| GET | /v2/apis/{apiId}/models | Gets the Models for an API. |
| GET | /v2/apis/{apiId}/routes/{routeId} | Gets a Route. |
| GET | /v2/apis/{apiId}/routes/{routeId}/routeresponses/{routeResponseId} | Gets a RouteResponse. |
| GET | /v2/apis/{apiId}/routes/{routeId}/routeresponses | Gets the RouteResponses for a Route. |
| GET | /v2/apis/{apiId}/routes | Gets the Routes for an API. |
| GET | /v2/apis/{apiId}/stages/{stageName} | Gets a Stage. |
| GET | /v2/apis/{apiId}/stages | Gets the Stages for an API. |
| PUT | /v2/apis | Imports an API. |
| PUT | /v2/apis/{apiId} | Puts an Api resource. |
| PATCH | /v2/apis/{apiId} | Updates an Api resource. |
| PATCH | /v2/apis/{apiId}/authorizers/{authorizerId} | Updates an Authorizer. |
| PATCH | /v2/apis/{apiId}/deployments/{deploymentId} | Updates a Deployment. |
| PATCH | /v2/apis/{apiId}/integrations/{integrationId} | Updates an Integration. |
| PATCH | /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses/{integrationResponseId} | Updates an IntegrationResponses. |
| PATCH | /v2/apis/{apiId}/models/{modelId} | Updates a Model. |
| PATCH | /v2/apis/{apiId}/routes/{routeId} | Updates a Route. |
| PATCH | /v2/apis/{apiId}/routes/{routeId}/routeresponses/{routeResponseId} | Updates a RouteResponse. |
| PATCH | /v2/apis/{apiId}/stages/{stageName} | Updates a Stage. |

### domainnames
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/domainnames/{domainName}/apimappings | Creates an API mapping. |
| POST | /v2/domainnames | Creates a domain name. |
| DELETE | /v2/domainnames/{domainName}/apimappings/{apiMappingId} | Deletes an API mapping. |
| DELETE | /v2/domainnames/{domainName} | Deletes a domain name. |
| GET | /v2/domainnames/{domainName}/apimappings/{apiMappingId} | Gets an API mapping. |
| GET | /v2/domainnames/{domainName}/apimappings | Gets API mappings. |
| GET | /v2/domainnames/{domainName} | Gets a domain name. |
| GET | /v2/domainnames | Gets the domain names for an AWS account. |
| PATCH | /v2/domainnames/{domainName}/apimappings/{apiMappingId} | The API mapping. |
| PATCH | /v2/domainnames/{domainName} | Updates a domain name. |

### vpclinks
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/vpclinks | Creates a VPC link. |
| DELETE | /v2/vpclinks/{vpcLinkId} | Deletes a VPC link. |
| GET | /v2/vpclinks/{vpcLinkId} | Gets a VPC link. |
| GET | /v2/vpclinks | Gets a collection of VPC links. |
| PATCH | /v2/vpclinks/{vpcLinkId} | Updates a VPC link. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/tags/{resource-arn} | Gets a collection of Tag resources. |
| POST | /v2/tags/{resource-arn} | Creates a new Tag resource to represent a tag. |
| DELETE | /v2/tags/{resource-arn} | Deletes a Tag. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a apis?" -> POST /v2/apis
- "Create a apimapping?" -> POST /v2/domainnames/{domainName}/apimappings
- "Create a authorizer?" -> POST /v2/apis/{apiId}/authorizers
- "Create a deployment?" -> POST /v2/apis/{apiId}/deployments
- "Create a domainname?" -> POST /v2/domainnames
- "Create a integration?" -> POST /v2/apis/{apiId}/integrations
- "Create a integrationrespons?" -> POST /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses
- "Create a model?" -> POST /v2/apis/{apiId}/models
- "Create a route?" -> POST /v2/apis/{apiId}/routes
- "Create a routerespons?" -> POST /v2/apis/{apiId}/routes/{routeId}/routeresponses
- "Create a stage?" -> POST /v2/apis/{apiId}/stages
- "Create a vpclink?" -> POST /v2/vpclinks
- "Delete a apis?" -> DELETE /v2/apis/{apiId}
- "Delete a apimapping?" -> DELETE /v2/domainnames/{domainName}/apimappings/{apiMappingId}
- "Delete a authorizer?" -> DELETE /v2/apis/{apiId}/authorizers/{authorizerId}
- "Delete a deployment?" -> DELETE /v2/apis/{apiId}/deployments/{deploymentId}
- "Delete a domainname?" -> DELETE /v2/domainnames/{domainName}
- "Delete a integration?" -> DELETE /v2/apis/{apiId}/integrations/{integrationId}
- "Delete a integrationrespons?" -> DELETE /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses/{integrationResponseId}
- "Delete a model?" -> DELETE /v2/apis/{apiId}/models/{modelId}
- "Delete a route?" -> DELETE /v2/apis/{apiId}/routes/{routeId}
- "Delete a requestparameter?" -> DELETE /v2/apis/{apiId}/routes/{routeId}/requestparameters/{requestParameterKey}
- "Delete a routerespons?" -> DELETE /v2/apis/{apiId}/routes/{routeId}/routeresponses/{routeResponseId}
- "Delete a routesetting?" -> DELETE /v2/apis/{apiId}/stages/{stageName}/routesettings/{routeKey}
- "Delete a stage?" -> DELETE /v2/apis/{apiId}/stages/{stageName}
- "Delete a vpclink?" -> DELETE /v2/vpclinks/{vpcLinkId}
- "Get export details?" -> GET /v2/apis/{apiId}/exports/{specification}
- "Get apis details?" -> GET /v2/apis/{apiId}
- "Get apimapping details?" -> GET /v2/domainnames/{domainName}/apimappings/{apiMappingId}
- "List all apimappings?" -> GET /v2/domainnames/{domainName}/apimappings
- "List all apis?" -> GET /v2/apis
- "Get authorizer details?" -> GET /v2/apis/{apiId}/authorizers/{authorizerId}
- "List all authorizers?" -> GET /v2/apis/{apiId}/authorizers
- "Get deployment details?" -> GET /v2/apis/{apiId}/deployments/{deploymentId}
- "List all deployments?" -> GET /v2/apis/{apiId}/deployments
- "Get domainname details?" -> GET /v2/domainnames/{domainName}
- "List all domainnames?" -> GET /v2/domainnames
- "Get integration details?" -> GET /v2/apis/{apiId}/integrations/{integrationId}
- "Get integrationrespons details?" -> GET /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses/{integrationResponseId}
- "List all integrationresponses?" -> GET /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses
- "List all integrations?" -> GET /v2/apis/{apiId}/integrations
- "Get model details?" -> GET /v2/apis/{apiId}/models/{modelId}
- "List all template?" -> GET /v2/apis/{apiId}/models/{modelId}/template
- "List all models?" -> GET /v2/apis/{apiId}/models
- "Get route details?" -> GET /v2/apis/{apiId}/routes/{routeId}
- "Get routerespons details?" -> GET /v2/apis/{apiId}/routes/{routeId}/routeresponses/{routeResponseId}
- "List all routeresponses?" -> GET /v2/apis/{apiId}/routes/{routeId}/routeresponses
- "List all routes?" -> GET /v2/apis/{apiId}/routes
- "Get stage details?" -> GET /v2/apis/{apiId}/stages/{stageName}
- "List all stages?" -> GET /v2/apis/{apiId}/stages
- "Get tag details?" -> GET /v2/tags/{resource-arn}
- "Get vpclink details?" -> GET /v2/vpclinks/{vpcLinkId}
- "List all vpclinks?" -> GET /v2/vpclinks
- "Update a apis?" -> PUT /v2/apis/{apiId}
- "Delete a tag?" -> DELETE /v2/tags/{resource-arn}
- "Partially update a apis?" -> PATCH /v2/apis/{apiId}
- "Partially update a apimapping?" -> PATCH /v2/domainnames/{domainName}/apimappings/{apiMappingId}
- "Partially update a authorizer?" -> PATCH /v2/apis/{apiId}/authorizers/{authorizerId}
- "Partially update a deployment?" -> PATCH /v2/apis/{apiId}/deployments/{deploymentId}
- "Partially update a domainname?" -> PATCH /v2/domainnames/{domainName}
- "Partially update a integration?" -> PATCH /v2/apis/{apiId}/integrations/{integrationId}
- "Partially update a integrationrespons?" -> PATCH /v2/apis/{apiId}/integrations/{integrationId}/integrationresponses/{integrationResponseId}
- "Partially update a model?" -> PATCH /v2/apis/{apiId}/models/{modelId}
- "Partially update a route?" -> PATCH /v2/apis/{apiId}/routes/{routeId}
- "Partially update a routerespons?" -> PATCH /v2/apis/{apiId}/routes/{routeId}/routeresponses/{routeResponseId}
- "Partially update a stage?" -> PATCH /v2/apis/{apiId}/stages/{stageName}
- "Partially update a vpclink?" -> PATCH /v2/vpclinks/{vpcLinkId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
