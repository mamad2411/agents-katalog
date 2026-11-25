---
name: aws-appsync
description: "AWS AppSync API skill. Use when working with AWS AppSync for domainnames, sourceApis, mergedApis. Covers 64 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS AppSync
API version: 2017-07-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/domainnames -- verify access
3. POST /v1/domainnames/{domainName}/apiassociation -- create first apiassociation

## Endpoints

64 endpoints across 8 groups. See references/api-spec.lap for full details.

### domainnames
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/domainnames/{domainName}/apiassociation | Maps an endpoint to your custom domain. |
| POST | /v1/domainnames | Creates a custom DomainName object. |
| DELETE | /v1/domainnames/{domainName} | Deletes a custom DomainName object. |
| DELETE | /v1/domainnames/{domainName}/apiassociation | Removes an ApiAssociation object from a custom domain. |
| GET | /v1/domainnames/{domainName}/apiassociation | Retrieves an ApiAssociation object. |
| GET | /v1/domainnames/{domainName} | Retrieves a custom DomainName object. |
| GET | /v1/domainnames | Lists multiple custom domain names. |
| POST | /v1/domainnames/{domainName} | Updates a custom DomainName object. |

### sourceApis
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/sourceApis/{sourceApiIdentifier}/mergedApiAssociations | Creates an association between a Merged API and source API using the source API's identifier. |
| DELETE | /v1/sourceApis/{sourceApiIdentifier}/mergedApiAssociations/{associationId} | Deletes an association between a Merged API and source API using the source API's identifier and the association ID. |

### mergedApis
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations | Creates an association between a Merged API and source API using the Merged API's identifier. |
| DELETE | /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId} | Deletes an association between a Merged API and source API using the Merged API's identifier and the association ID. |
| GET | /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId} | Retrieves a SourceApiAssociation object. |
| GET | /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId}/types | Lists Type objects by the source API association ID. |
| POST | /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId}/merge | Initiates a merge operation. Returns a status that shows the result of the merge operation. |
| POST | /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId} | Updates some of the configuration choices of a particular source API association. |

### apis
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/apis/{apiId}/ApiCaches | Creates a cache for the GraphQL API. |
| POST | /v1/apis/{apiId}/apikeys | Creates a unique key that you can distribute to clients who invoke your API. |
| POST | /v1/apis/{apiId}/datasources | Creates a DataSource object. |
| POST | /v1/apis/{apiId}/functions | Creates a Function object. A function is a reusable entity. You can use multiple functions to compose the resolver logic. |
| POST | /v1/apis | Creates a GraphqlApi object. |
| POST | /v1/apis/{apiId}/types/{typeName}/resolvers | Creates a Resolver object. A resolver converts incoming requests into a format that a data source can understand, and converts the data source's responses into GraphQL. |
| POST | /v1/apis/{apiId}/types | Creates a Type object. |
| DELETE | /v1/apis/{apiId}/ApiCaches | Deletes an ApiCache object. |
| DELETE | /v1/apis/{apiId}/apikeys/{id} | Deletes an API key. |
| DELETE | /v1/apis/{apiId}/datasources/{name} | Deletes a DataSource object. |
| DELETE | /v1/apis/{apiId}/functions/{functionId} | Deletes a Function. |
| DELETE | /v1/apis/{apiId} | Deletes a GraphqlApi object. |
| DELETE | /v1/apis/{apiId}/types/{typeName}/resolvers/{fieldName} | Deletes a Resolver object. |
| DELETE | /v1/apis/{apiId}/types/{typeName} | Deletes a Type object. |
| DELETE | /v1/apis/{apiId}/FlushCache | Flushes an ApiCache object. |
| GET | /v1/apis/{apiId}/ApiCaches | Retrieves an ApiCache object. |
| GET | /v1/apis/{apiId}/datasources/{name} | Retrieves a DataSource object. |
| GET | /v1/apis/{apiId}/functions/{functionId} | Get a Function. |
| GET | /v1/apis/{apiId} | Retrieves a GraphqlApi object. |
| GET | /v1/apis/{apiId}/environmentVariables | Retrieves the list of environmental variable key-value pairs associated with an API by its ID value. |
| GET | /v1/apis/{apiId}/schema | Retrieves the introspection schema for a GraphQL API. |
| GET | /v1/apis/{apiId}/types/{typeName}/resolvers/{fieldName} | Retrieves a Resolver object. |
| GET | /v1/apis/{apiId}/schemacreation | Retrieves the current status of a schema creation operation. |
| GET | /v1/apis/{apiId}/types/{typeName} | Retrieves a Type object. |
| GET | /v1/apis/{apiId}/apikeys | Lists the API keys for a given API.  API keys are deleted automatically 60 days after they expire. However, they may still be included in the response until they have actually been deleted. You can safely call DeleteApiKey to manually delete a key before it's automatically deleted. |
| GET | /v1/apis/{apiId}/datasources | Lists the data sources for a given API. |
| GET | /v1/apis/{apiId}/functions | List multiple functions. |
| GET | /v1/apis | Lists your GraphQL APIs. |
| GET | /v1/apis/{apiId}/types/{typeName}/resolvers | Lists the resolvers for a given API and type. |
| GET | /v1/apis/{apiId}/functions/{functionId}/resolvers | List the resolvers that are associated with a specific function. |
| GET | /v1/apis/{apiId}/sourceApiAssociations | Lists the SourceApiAssociationSummary data. |
| GET | /v1/apis/{apiId}/types | Lists the types for a given API. |
| PUT | /v1/apis/{apiId}/environmentVariables | Creates a list of environmental variables in an API by its ID value.  When creating an environmental variable, it must follow the constraints below:   Both JavaScript and VTL templates support environmental variables.   Environmental variables are not evaluated before function invocation.   Environmental variables only support string values.   Any defined value in an environmental variable is considered a string literal and not expanded.   Variable evaluations should ideally be performed in the function code.   When creating an environmental variable key-value pair, it must follow the additional constraints below:   Keys must begin with a letter.   Keys must be at least two characters long.   Keys can only contain letters, numbers, and the underscore character (_).   Values can be up to 512 characters long.   You can configure up to 50 key-value pairs in a GraphQL API.   You can create a list of environmental variables by adding it to the environmentVariables payload as a list in the format {"key1":"value1","key2":"value2", …}. Note that each call of the PutGraphqlApiEnvironmentVariables action will result in the overwriting of the existing environmental variable list of that API. This means the existing environmental variables will be lost. To avoid this, you must include all existing and new environmental variables in the list each time you call this action. |
| POST | /v1/apis/{apiId}/schemacreation | Adds a new schema to your GraphQL API. This operation is asynchronous. Use to determine when it has completed. |
| POST | /v1/apis/{apiId}/ApiCaches/update | Updates the cache for the GraphQL API. |
| POST | /v1/apis/{apiId}/apikeys/{id} | Updates an API key. You can update the key as long as it's not deleted. |
| POST | /v1/apis/{apiId}/datasources/{name} | Updates a DataSource object. |
| POST | /v1/apis/{apiId}/functions/{functionId} | Updates a Function object. |
| POST | /v1/apis/{apiId} | Updates a GraphqlApi object. |
| POST | /v1/apis/{apiId}/types/{typeName}/resolvers/{fieldName} | Updates a Resolver object. |
| POST | /v1/apis/{apiId}/types/{typeName} | Updates a Type object. |

### dataplane-evaluatecode
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/dataplane-evaluatecode | Evaluates the given code and returns the response. The code definition requirements depend on the specified runtime. For APPSYNC_JS runtimes, the code defines the request and response functions. The request function takes the incoming request after a GraphQL operation is parsed and converts it into a request configuration for the selected data source operation. The response function interprets responses from the data source and maps it to the shape of the GraphQL field output type. |

### dataplane-evaluatetemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/dataplane-evaluatetemplate | Evaluates a given template and returns the response. The mapping template can be a request or response template. Request templates take the incoming request after a GraphQL operation is parsed and convert it into a request configuration for the selected data source operation. Response templates interpret responses from the data source and map it to the shape of the GraphQL field output type. Mapping templates are written in the Apache Velocity Template Language (VTL). |

### datasources
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/datasources/introspections/{introspectionId} | Retrieves the record of an existing introspection. If the retrieval is successful, the result of the instrospection will also be returned. If the retrieval fails the operation, an error message will be returned instead. |
| POST | /v1/datasources/introspections | Creates a new introspection. Returns the introspectionId of the new introspection after its creation. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/tags/{resourceArn} | Lists the tags for a resource. |
| POST | /v1/tags/{resourceArn} | Tags a resource with user-supplied tags. |
| DELETE | /v1/tags/{resourceArn} | Untags a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a apiassociation?" -> POST /v1/domainnames/{domainName}/apiassociation
- "Create a mergedApiAssociation?" -> POST /v1/sourceApis/{sourceApiIdentifier}/mergedApiAssociations
- "Create a sourceApiAssociation?" -> POST /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations
- "Create a ApiCache?" -> POST /v1/apis/{apiId}/ApiCaches
- "Create a apikey?" -> POST /v1/apis/{apiId}/apikeys
- "Create a datasource?" -> POST /v1/apis/{apiId}/datasources
- "Create a domainname?" -> POST /v1/domainnames
- "Create a function?" -> POST /v1/apis/{apiId}/functions
- "Create a apis?" -> POST /v1/apis
- "Create a resolver?" -> POST /v1/apis/{apiId}/types/{typeName}/resolvers
- "Create a type?" -> POST /v1/apis/{apiId}/types
- "Delete a apikey?" -> DELETE /v1/apis/{apiId}/apikeys/{id}
- "Delete a datasource?" -> DELETE /v1/apis/{apiId}/datasources/{name}
- "Delete a domainname?" -> DELETE /v1/domainnames/{domainName}
- "Delete a function?" -> DELETE /v1/apis/{apiId}/functions/{functionId}
- "Delete a apis?" -> DELETE /v1/apis/{apiId}
- "Delete a resolver?" -> DELETE /v1/apis/{apiId}/types/{typeName}/resolvers/{fieldName}
- "Delete a type?" -> DELETE /v1/apis/{apiId}/types/{typeName}
- "Delete a mergedApiAssociation?" -> DELETE /v1/sourceApis/{sourceApiIdentifier}/mergedApiAssociations/{associationId}
- "Delete a sourceApiAssociation?" -> DELETE /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId}
- "Create a dataplane-evaluatecode?" -> POST /v1/dataplane-evaluatecode
- "Create a dataplane-evaluatetemplate?" -> POST /v1/dataplane-evaluatetemplate
- "List all apiassociation?" -> GET /v1/domainnames/{domainName}/apiassociation
- "List all ApiCaches?" -> GET /v1/apis/{apiId}/ApiCaches
- "Get datasource details?" -> GET /v1/apis/{apiId}/datasources/{name}
- "Get introspection details?" -> GET /v1/datasources/introspections/{introspectionId}
- "Get domainname details?" -> GET /v1/domainnames/{domainName}
- "Get function details?" -> GET /v1/apis/{apiId}/functions/{functionId}
- "Get apis details?" -> GET /v1/apis/{apiId}
- "List all environmentVariables?" -> GET /v1/apis/{apiId}/environmentVariables
- "List all schema?" -> GET /v1/apis/{apiId}/schema
- "Get resolver details?" -> GET /v1/apis/{apiId}/types/{typeName}/resolvers/{fieldName}
- "List all schemacreation?" -> GET /v1/apis/{apiId}/schemacreation
- "Get sourceApiAssociation details?" -> GET /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId}
- "Get type details?" -> GET /v1/apis/{apiId}/types/{typeName}
- "List all apikeys?" -> GET /v1/apis/{apiId}/apikeys
- "List all datasources?" -> GET /v1/apis/{apiId}/datasources
- "List all domainnames?" -> GET /v1/domainnames
- "List all functions?" -> GET /v1/apis/{apiId}/functions
- "List all apis?" -> GET /v1/apis
- "List all resolvers?" -> GET /v1/apis/{apiId}/types/{typeName}/resolvers
- "List all resolvers?" -> GET /v1/apis/{apiId}/functions/{functionId}/resolvers
- "List all sourceApiAssociations?" -> GET /v1/apis/{apiId}/sourceApiAssociations
- "Get tag details?" -> GET /v1/tags/{resourceArn}
- "List all types?" -> GET /v1/apis/{apiId}/types
- "List all types?" -> GET /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId}/types
- "Create a introspection?" -> POST /v1/datasources/introspections
- "Create a schemacreation?" -> POST /v1/apis/{apiId}/schemacreation
- "Create a merge?" -> POST /v1/mergedApis/{mergedApiIdentifier}/sourceApiAssociations/{associationId}/merge
- "Delete a tag?" -> DELETE /v1/tags/{resourceArn}
- "Create a update?" -> POST /v1/apis/{apiId}/ApiCaches/update
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
