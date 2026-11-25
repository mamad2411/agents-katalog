---
name: amazon-api-gateway
description: "Amazon API Gateway API skill. Use when working with Amazon API Gateway for apikeys, restapis, domainnames. Covers 120 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon API Gateway
API version: 2015-07-09

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /account -- verify access
3. POST /apikeys -- create first apikeys

## Endpoints

120 endpoints across 11 groups. See references/api-spec.lap for full details.

### apikeys
| Method | Path | Description |
|--------|------|-------------|
| POST | /apikeys | Create an ApiKey resource. |
| DELETE | /apikeys/{api_Key} | Deletes the ApiKey resource. |
| GET | /apikeys/{api_Key} | Gets information about the current ApiKey resource. |
| GET | /apikeys | Gets information about the current ApiKeys resource. |
| PATCH | /apikeys/{api_Key} | Changes information about an ApiKey resource. |

### restapis
| Method | Path | Description |
|--------|------|-------------|
| POST | /restapis/{restapi_id}/authorizers | Adds a new Authorizer resource to an existing RestApi resource. |
| POST | /restapis/{restapi_id}/deployments | Creates a Deployment resource, which makes a specified RestApi callable over the internet. |
| POST | /restapis/{restapi_id}/documentation/parts | Creates a documentation part. |
| POST | /restapis/{restapi_id}/documentation/versions | Creates a documentation version |
| POST | /restapis/{restapi_id}/models | Adds a new Model resource to an existing RestApi resource. |
| POST | /restapis/{restapi_id}/requestvalidators | Creates a RequestValidator of a given RestApi. |
| POST | /restapis/{restapi_id}/resources/{parent_id} | Creates a Resource resource. |
| POST | /restapis | Creates a new RestApi resource. |
| POST | /restapis/{restapi_id}/stages | Creates a new Stage resource that references a pre-existing Deployment for the API. |
| DELETE | /restapis/{restapi_id}/authorizers/{authorizer_id} | Deletes an existing Authorizer resource. |
| DELETE | /restapis/{restapi_id}/deployments/{deployment_id} | Deletes a Deployment resource. Deleting a deployment will only succeed if there are no Stage resources associated with it. |
| DELETE | /restapis/{restapi_id}/documentation/parts/{part_id} | Deletes a documentation part |
| DELETE | /restapis/{restapi_id}/documentation/versions/{doc_version} | Deletes a documentation version. |
| DELETE | /restapis/{restapi_id}/gatewayresponses/{response_type} | Clears any customization of a GatewayResponse of a specified response type on the given RestApi and resets it with the default settings. |
| DELETE | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration | Represents a delete integration. |
| DELETE | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration/responses/{status_code} | Represents a delete integration response. |
| DELETE | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method} | Deletes an existing Method resource. |
| DELETE | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/responses/{status_code} | Deletes an existing MethodResponse resource. |
| DELETE | /restapis/{restapi_id}/models/{model_name} | Deletes a model. |
| DELETE | /restapis/{restapi_id}/requestvalidators/{requestvalidator_id} | Deletes a RequestValidator of a given RestApi. |
| DELETE | /restapis/{restapi_id}/resources/{resource_id} | Deletes a Resource resource. |
| DELETE | /restapis/{restapi_id} | Deletes the specified API. |
| DELETE | /restapis/{restapi_id}/stages/{stage_name} | Deletes a Stage resource. |
| DELETE | /restapis/{restapi_id}/stages/{stage_name}/cache/authorizers | Flushes all authorizer cache entries on a stage. |
| DELETE | /restapis/{restapi_id}/stages/{stage_name}/cache/data | Flushes a stage's cache. |
| GET | /restapis/{restapi_id}/authorizers/{authorizer_id} | Describe an existing Authorizer resource. |
| GET | /restapis/{restapi_id}/authorizers | Describe an existing Authorizers resource. |
| GET | /restapis/{restapi_id}/deployments/{deployment_id} | Gets information about a Deployment resource. |
| GET | /restapis/{restapi_id}/deployments | Gets information about a Deployments collection. |
| GET | /restapis/{restapi_id}/documentation/parts/{part_id} | Gets a documentation part. |
| GET | /restapis/{restapi_id}/documentation/parts | Gets documentation parts. |
| GET | /restapis/{restapi_id}/documentation/versions/{doc_version} | Gets a documentation version. |
| GET | /restapis/{restapi_id}/documentation/versions | Gets documentation versions. |
| GET | /restapis/{restapi_id}/stages/{stage_name}/exports/{export_type} | Exports a deployed version of a RestApi in a specified format. |
| GET | /restapis/{restapi_id}/gatewayresponses/{response_type} | Gets a GatewayResponse of a specified response type on the given RestApi. |
| GET | /restapis/{restapi_id}/gatewayresponses | Gets the GatewayResponses collection on the given RestApi. If an API developer has not added any definitions for gateway responses, the result will be the API Gateway-generated default GatewayResponses collection for the supported response types. |
| GET | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration | Get the integration settings. |
| GET | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration/responses/{status_code} | Represents a get integration response. |
| GET | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method} | Describe an existing Method resource. |
| GET | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/responses/{status_code} | Describes a MethodResponse resource. |
| GET | /restapis/{restapi_id}/models/{model_name} | Describes an existing model defined for a RestApi resource. |
| GET | /restapis/{restapi_id}/models/{model_name}/default_template | Generates a sample mapping template that can be used to transform a payload into the structure of a model. |
| GET | /restapis/{restapi_id}/models | Describes existing Models defined for a RestApi resource. |
| GET | /restapis/{restapi_id}/requestvalidators/{requestvalidator_id} | Gets a RequestValidator of a given RestApi. |
| GET | /restapis/{restapi_id}/requestvalidators | Gets the RequestValidators collection of a given RestApi. |
| GET | /restapis/{restapi_id}/resources/{resource_id} | Lists information about a resource. |
| GET | /restapis/{restapi_id}/resources | Lists information about a collection of Resource resources. |
| GET | /restapis/{restapi_id} | Lists the RestApi resource in the collection. |
| GET | /restapis | Lists the RestApis resources for your collection. |
| GET | /restapis/{restapi_id}/stages/{stage_name}/sdks/{sdk_type} | Generates a client SDK for a RestApi and Stage. |
| GET | /restapis/{restapi_id}/stages/{stage_name} | Gets information about a Stage resource. |
| GET | /restapis/{restapi_id}/stages | Gets information about one or more Stage resources. |
| PUT | /restapis/{restapi_id}/documentation/parts | Imports documentation parts |
| PUT | /restapis/{restapi_id}/gatewayresponses/{response_type} | Creates a customization of a GatewayResponse of a specified response type and status code on the given RestApi. |
| PUT | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration | Sets up a method's integration. |
| PUT | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration/responses/{status_code} | Represents a put integration. |
| PUT | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method} | Add a method to an existing Resource resource. |
| PUT | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/responses/{status_code} | Adds a MethodResponse to an existing Method resource. |
| PUT | /restapis/{restapi_id} | A feature of the API Gateway control service for updating an existing API with an input of external API definitions. The update can take the form of merging the supplied definition into the existing API or overwriting the existing API. |
| POST | /restapis/{restapi_id}/authorizers/{authorizer_id} | Simulate the execution of an Authorizer in your RestApi with headers, parameters, and an incoming request body. |
| POST | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method} | Simulate the invocation of a Method in your RestApi with headers, parameters, and an incoming request body. |
| PATCH | /restapis/{restapi_id}/authorizers/{authorizer_id} | Updates an existing Authorizer resource. |
| PATCH | /restapis/{restapi_id}/deployments/{deployment_id} | Changes information about a Deployment resource. |
| PATCH | /restapis/{restapi_id}/documentation/parts/{part_id} | Updates a documentation part. |
| PATCH | /restapis/{restapi_id}/documentation/versions/{doc_version} | Updates a documentation version. |
| PATCH | /restapis/{restapi_id}/gatewayresponses/{response_type} | Updates a GatewayResponse of a specified response type on the given RestApi. |
| PATCH | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration | Represents an update integration. |
| PATCH | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration/responses/{status_code} | Represents an update integration response. |
| PATCH | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method} | Updates an existing Method resource. |
| PATCH | /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/responses/{status_code} | Updates an existing MethodResponse resource. |
| PATCH | /restapis/{restapi_id}/models/{model_name} | Changes information about a model. The maximum size of the model is 400 KB. |
| PATCH | /restapis/{restapi_id}/requestvalidators/{requestvalidator_id} | Updates a RequestValidator of a given RestApi. |
| PATCH | /restapis/{restapi_id}/resources/{resource_id} | Changes information about a Resource resource. |
| PATCH | /restapis/{restapi_id} | Changes information about the specified API. |
| PATCH | /restapis/{restapi_id}/stages/{stage_name} | Changes information about a Stage resource. |

### domainnames
| Method | Path | Description |
|--------|------|-------------|
| POST | /domainnames/{domain_name}/basepathmappings | Creates a new BasePathMapping resource. |
| POST | /domainnames | Creates a new domain name. |
| DELETE | /domainnames/{domain_name}/basepathmappings/{base_path} | Deletes the BasePathMapping resource. |
| DELETE | /domainnames/{domain_name} | Deletes the DomainName resource. |
| GET | /domainnames/{domain_name}/basepathmappings/{base_path} | Describe a BasePathMapping resource. |
| GET | /domainnames/{domain_name}/basepathmappings | Represents a collection of BasePathMapping resources. |
| GET | /domainnames/{domain_name} | Represents a domain name that is contained in a simpler, more intuitive URL that can be called. |
| GET | /domainnames | Represents a collection of DomainName resources. |
| PATCH | /domainnames/{domain_name}/basepathmappings/{base_path} | Changes information about the BasePathMapping resource. |
| PATCH | /domainnames/{domain_name} | Changes information about the DomainName resource. |

### usageplans
| Method | Path | Description |
|--------|------|-------------|
| POST | /usageplans | Creates a usage plan with the throttle and quota limits, as well as the associated API stages, specified in the payload. |
| POST | /usageplans/{usageplanId}/keys | Creates a usage plan key for adding an existing API key to a usage plan. |
| DELETE | /usageplans/{usageplanId} | Deletes a usage plan of a given plan Id. |
| DELETE | /usageplans/{usageplanId}/keys/{keyId} | Deletes a usage plan key and remove the underlying API key from the associated usage plan. |
| GET | /usageplans/{usageplanId}/usage | Gets the usage data of a usage plan in a specified time interval. |
| GET | /usageplans/{usageplanId} | Gets a usage plan of a given plan identifier. |
| GET | /usageplans/{usageplanId}/keys/{keyId} | Gets a usage plan key of a given key identifier. |
| GET | /usageplans/{usageplanId}/keys | Gets all the usage plan keys representing the API keys added to a specified usage plan. |
| GET | /usageplans | Gets all the usage plans of the caller's account. |
| PATCH | /usageplans/{usageplanId}/keys/{keyId}/usage | Grants a temporary extension to the remaining quota of a usage plan associated with a specified API key. |
| PATCH | /usageplans/{usageplanId} | Updates a usage plan of a given plan Id. |

### vpclinks
| Method | Path | Description |
|--------|------|-------------|
| POST | /vpclinks | Creates a VPC link, under the caller's account in a selected region, in an asynchronous operation that typically takes 2-4 minutes to complete and become operational. The caller must have permissions to create and update VPC Endpoint services. |
| DELETE | /vpclinks/{vpclink_id} | Deletes an existing VpcLink of a specified identifier. |
| GET | /vpclinks/{vpclink_id} | Gets a specified VPC link under the caller's account in a region. |
| GET | /vpclinks | Gets the VpcLinks collection under the caller's account in a selected region. |
| PATCH | /vpclinks/{vpclink_id} | Updates an existing VpcLink of a specified identifier. |

### clientcertificates
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /clientcertificates/{clientcertificate_id} | Deletes the ClientCertificate resource. |
| POST | /clientcertificates | Generates a ClientCertificate resource. |
| GET | /clientcertificates/{clientcertificate_id} | Gets information about the current ClientCertificate resource. |
| GET | /clientcertificates | Gets a collection of ClientCertificate resources. |
| PATCH | /clientcertificates/{clientcertificate_id} | Changes information about an ClientCertificate resource. |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Gets information about the current Account resource. |
| PATCH | /account | Changes information about the current Account resource. |

### sdktypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /sdktypes/{sdktype_id} | Gets an SDK type. |
| GET | /sdktypes | Gets SDK types |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resource_arn} | Gets the Tags collection for a given resource. |
| PUT | /tags/{resource_arn} | Adds or updates a tag on a given resource. |
| DELETE | /tags/{resource_arn} | Removes a tag from a given resource. |

### apikeys?mode=import
| Method | Path | Description |
|--------|------|-------------|
| POST | /apikeys?mode=import | Import API keys from an external source, such as a CSV-formatted file. |

### restapis?mode=import
| Method | Path | Description |
|--------|------|-------------|
| POST | /restapis?mode=import | A feature of the API Gateway control service for creating a new API from an external API definition file. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a apikey?" -> POST /apikeys
- "Create a authorizer?" -> POST /restapis/{restapi_id}/authorizers
- "Create a basepathmapping?" -> POST /domainnames/{domain_name}/basepathmappings
- "Create a deployment?" -> POST /restapis/{restapi_id}/deployments
- "Create a part?" -> POST /restapis/{restapi_id}/documentation/parts
- "Create a version?" -> POST /restapis/{restapi_id}/documentation/versions
- "Create a domainname?" -> POST /domainnames
- "Create a model?" -> POST /restapis/{restapi_id}/models
- "Create a requestvalidator?" -> POST /restapis/{restapi_id}/requestvalidators
- "Create a restapis?" -> POST /restapis
- "Create a stage?" -> POST /restapis/{restapi_id}/stages
- "Create a usageplan?" -> POST /usageplans
- "Create a key?" -> POST /usageplans/{usageplanId}/keys
- "Create a vpclink?" -> POST /vpclinks
- "Delete a apikey?" -> DELETE /apikeys/{api_Key}
- "Delete a authorizer?" -> DELETE /restapis/{restapi_id}/authorizers/{authorizer_id}
- "Delete a basepathmapping?" -> DELETE /domainnames/{domain_name}/basepathmappings/{base_path}
- "Delete a clientcertificate?" -> DELETE /clientcertificates/{clientcertificate_id}
- "Delete a deployment?" -> DELETE /restapis/{restapi_id}/deployments/{deployment_id}
- "Delete a part?" -> DELETE /restapis/{restapi_id}/documentation/parts/{part_id}
- "Delete a version?" -> DELETE /restapis/{restapi_id}/documentation/versions/{doc_version}
- "Delete a domainname?" -> DELETE /domainnames/{domain_name}
- "Delete a gatewayrespons?" -> DELETE /restapis/{restapi_id}/gatewayresponses/{response_type}
- "Delete a response?" -> DELETE /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration/responses/{status_code}
- "Delete a method?" -> DELETE /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}
- "Delete a response?" -> DELETE /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/responses/{status_code}
- "Delete a model?" -> DELETE /restapis/{restapi_id}/models/{model_name}
- "Delete a requestvalidator?" -> DELETE /restapis/{restapi_id}/requestvalidators/{requestvalidator_id}
- "Delete a resource?" -> DELETE /restapis/{restapi_id}/resources/{resource_id}
- "Delete a restapis?" -> DELETE /restapis/{restapi_id}
- "Delete a stage?" -> DELETE /restapis/{restapi_id}/stages/{stage_name}
- "Delete a usageplan?" -> DELETE /usageplans/{usageplanId}
- "Delete a key?" -> DELETE /usageplans/{usageplanId}/keys/{keyId}
- "Delete a vpclink?" -> DELETE /vpclinks/{vpclink_id}
- "Create a clientcertificate?" -> POST /clientcertificates
- "List all account?" -> GET /account
- "Get apikey details?" -> GET /apikeys/{api_Key}
- "List all apikeys?" -> GET /apikeys
- "Get authorizer details?" -> GET /restapis/{restapi_id}/authorizers/{authorizer_id}
- "List all authorizers?" -> GET /restapis/{restapi_id}/authorizers
- "Get basepathmapping details?" -> GET /domainnames/{domain_name}/basepathmappings/{base_path}
- "List all basepathmappings?" -> GET /domainnames/{domain_name}/basepathmappings
- "Get clientcertificate details?" -> GET /clientcertificates/{clientcertificate_id}
- "List all clientcertificates?" -> GET /clientcertificates
- "Get deployment details?" -> GET /restapis/{restapi_id}/deployments/{deployment_id}
- "List all deployments?" -> GET /restapis/{restapi_id}/deployments
- "Get part details?" -> GET /restapis/{restapi_id}/documentation/parts/{part_id}
- "List all parts?" -> GET /restapis/{restapi_id}/documentation/parts
- "Get version details?" -> GET /restapis/{restapi_id}/documentation/versions/{doc_version}
- "List all versions?" -> GET /restapis/{restapi_id}/documentation/versions
- "Get domainname details?" -> GET /domainnames/{domain_name}
- "List all domainnames?" -> GET /domainnames
- "Get export details?" -> GET /restapis/{restapi_id}/stages/{stage_name}/exports/{export_type}
- "Get gatewayrespons details?" -> GET /restapis/{restapi_id}/gatewayresponses/{response_type}
- "List all gatewayresponses?" -> GET /restapis/{restapi_id}/gatewayresponses
- "List all integration?" -> GET /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration
- "Get response details?" -> GET /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration/responses/{status_code}
- "Get method details?" -> GET /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}
- "Get response details?" -> GET /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/responses/{status_code}
- "Get model details?" -> GET /restapis/{restapi_id}/models/{model_name}
- "List all default_template?" -> GET /restapis/{restapi_id}/models/{model_name}/default_template
- "List all models?" -> GET /restapis/{restapi_id}/models
- "Get requestvalidator details?" -> GET /restapis/{restapi_id}/requestvalidators/{requestvalidator_id}
- "List all requestvalidators?" -> GET /restapis/{restapi_id}/requestvalidators
- "Get resource details?" -> GET /restapis/{restapi_id}/resources/{resource_id}
- "List all resources?" -> GET /restapis/{restapi_id}/resources
- "Get restapis details?" -> GET /restapis/{restapi_id}
- "List all restapis?" -> GET /restapis
- "Get sdk details?" -> GET /restapis/{restapi_id}/stages/{stage_name}/sdks/{sdk_type}
- "Get sdktype details?" -> GET /sdktypes/{sdktype_id}
- "List all sdktypes?" -> GET /sdktypes
- "Get stage details?" -> GET /restapis/{restapi_id}/stages/{stage_name}
- "List all stages?" -> GET /restapis/{restapi_id}/stages
- "Get tag details?" -> GET /tags/{resource_arn}
- "List all usage?" -> GET /usageplans/{usageplanId}/usage
- "Get usageplan details?" -> GET /usageplans/{usageplanId}
- "Get key details?" -> GET /usageplans/{usageplanId}/keys/{keyId}
- "List all keys?" -> GET /usageplans/{usageplanId}/keys
- "List all usageplans?" -> GET /usageplans
- "Get vpclink details?" -> GET /vpclinks/{vpclink_id}
- "List all vpclinks?" -> GET /vpclinks
- "Create a apikeys?mode=import?" -> POST /apikeys?mode=import
- "Create a restapis?mode=import?" -> POST /restapis?mode=import
- "Update a gatewayrespons?" -> PUT /restapis/{restapi_id}/gatewayresponses/{response_type}
- "Update a response?" -> PUT /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration/responses/{status_code}
- "Update a method?" -> PUT /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}
- "Update a response?" -> PUT /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/responses/{status_code}
- "Update a restapis?" -> PUT /restapis/{restapi_id}
- "Update a tag?" -> PUT /tags/{resource_arn}
- "Delete a tag?" -> DELETE /tags/{resource_arn}
- "Partially update a apikey?" -> PATCH /apikeys/{api_Key}
- "Partially update a authorizer?" -> PATCH /restapis/{restapi_id}/authorizers/{authorizer_id}
- "Partially update a basepathmapping?" -> PATCH /domainnames/{domain_name}/basepathmappings/{base_path}
- "Partially update a clientcertificate?" -> PATCH /clientcertificates/{clientcertificate_id}
- "Partially update a deployment?" -> PATCH /restapis/{restapi_id}/deployments/{deployment_id}
- "Partially update a part?" -> PATCH /restapis/{restapi_id}/documentation/parts/{part_id}
- "Partially update a version?" -> PATCH /restapis/{restapi_id}/documentation/versions/{doc_version}
- "Partially update a domainname?" -> PATCH /domainnames/{domain_name}
- "Partially update a gatewayrespons?" -> PATCH /restapis/{restapi_id}/gatewayresponses/{response_type}
- "Partially update a response?" -> PATCH /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/integration/responses/{status_code}
- "Partially update a method?" -> PATCH /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}
- "Partially update a response?" -> PATCH /restapis/{restapi_id}/resources/{resource_id}/methods/{http_method}/responses/{status_code}
- "Partially update a model?" -> PATCH /restapis/{restapi_id}/models/{model_name}
- "Partially update a requestvalidator?" -> PATCH /restapis/{restapi_id}/requestvalidators/{requestvalidator_id}
- "Partially update a resource?" -> PATCH /restapis/{restapi_id}/resources/{resource_id}
- "Partially update a restapis?" -> PATCH /restapis/{restapi_id}
- "Partially update a stage?" -> PATCH /restapis/{restapi_id}/stages/{stage_name}
- "Partially update a usageplan?" -> PATCH /usageplans/{usageplanId}
- "Partially update a vpclink?" -> PATCH /vpclinks/{vpclink_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
