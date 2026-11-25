---
name: amazon-clouddirectory
description: "Amazon CloudDirectory API skill. Use when working with Amazon CloudDirectory for amazonclouddirectory. Covers 66 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon CloudDirectory
API version: 2017-01-11

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /amazonclouddirectory/2017-01-11/batchread -- create first batchread

## Endpoints

66 endpoints across 1 groups. See references/api-spec.lap for full details.

### amazonclouddirectory
| Method | Path | Description |
|--------|------|-------------|
| PUT | /amazonclouddirectory/2017-01-11/object/facets | Adds a new Facet to an object. An object can have more than one facet applied on it. |
| PUT | /amazonclouddirectory/2017-01-11/schema/apply | Copies the input published schema, at the specified version, into the Directory with the same name and version as that of the published schema. |
| PUT | /amazonclouddirectory/2017-01-11/object/attach | Attaches an existing object to another object. An object can be accessed in two ways:   Using the path   Using ObjectIdentifier |
| PUT | /amazonclouddirectory/2017-01-11/policy/attach | Attaches a policy object to a regular object. An object can have a limited number of attached policies. |
| PUT | /amazonclouddirectory/2017-01-11/index/attach | Attaches the specified object to the specified index. |
| PUT | /amazonclouddirectory/2017-01-11/typedlink/attach | Attaches a typed link to a specified source and target object. For more information, see Typed Links. |
| POST | /amazonclouddirectory/2017-01-11/batchread | Performs all the read operations in a batch. |
| PUT | /amazonclouddirectory/2017-01-11/batchwrite | Performs all the write operations in a batch. Either all the operations succeed or none. |
| PUT | /amazonclouddirectory/2017-01-11/directory/create | Creates a Directory by copying the published schema into the directory. A directory cannot be created without a schema. You can also quickly create a directory using a managed schema, called the QuickStartSchema. For more information, see Managed Schema in the Amazon Cloud Directory Developer Guide. |
| PUT | /amazonclouddirectory/2017-01-11/facet/create | Creates a new Facet in a schema. Facet creation is allowed only in development or applied schemas. |
| PUT | /amazonclouddirectory/2017-01-11/index | Creates an index object. See Indexing and search for more information. |
| PUT | /amazonclouddirectory/2017-01-11/object | Creates an object in a Directory. Additionally attaches the object to a parent, if a parent reference and LinkName is specified. An object is simply a collection of Facet attributes. You can also use this API call to create a policy object, if the facet from which you create the object is a policy facet. |
| PUT | /amazonclouddirectory/2017-01-11/schema/create | Creates a new schema in a development state. A schema can exist in three phases:    Development: This is a mutable phase of the schema. All new schemas are in the development phase. Once the schema is finalized, it can be published.    Published: Published schemas are immutable and have a version associated with them.    Applied: Applied schemas are mutable in a way that allows you to add new schema facets. You can also add new, nonrequired attributes to existing schema facets. You can apply only published schemas to directories. |
| PUT | /amazonclouddirectory/2017-01-11/typedlink/facet/create | Creates a TypedLinkFacet. For more information, see Typed Links. |
| PUT | /amazonclouddirectory/2017-01-11/directory | Deletes a directory. Only disabled directories can be deleted. A deleted directory cannot be undone. Exercise extreme caution when deleting directories. |
| PUT | /amazonclouddirectory/2017-01-11/facet/delete | Deletes a given Facet. All attributes and Rules that are associated with the facet will be deleted. Only development schema facets are allowed deletion. |
| PUT | /amazonclouddirectory/2017-01-11/object/delete | Deletes an object and its associated attributes. Only objects with no children and no parents can be deleted. The maximum number of attributes that can be deleted during an object deletion is 30. For more information, see Amazon Cloud Directory Limits. |
| PUT | /amazonclouddirectory/2017-01-11/schema | Deletes a given schema. Schemas in a development and published state can only be deleted. |
| PUT | /amazonclouddirectory/2017-01-11/typedlink/facet/delete | Deletes a TypedLinkFacet. For more information, see Typed Links. |
| PUT | /amazonclouddirectory/2017-01-11/index/detach | Detaches the specified object from the specified index. |
| PUT | /amazonclouddirectory/2017-01-11/object/detach | Detaches a given object from the parent object. The object that is to be detached from the parent is specified by the link name. |
| PUT | /amazonclouddirectory/2017-01-11/policy/detach | Detaches a policy from an object. |
| PUT | /amazonclouddirectory/2017-01-11/typedlink/detach | Detaches a typed link from a specified source and target object. For more information, see Typed Links. |
| PUT | /amazonclouddirectory/2017-01-11/directory/disable | Disables the specified directory. Disabled directories cannot be read or written to. Only enabled directories can be disabled. Disabled directories may be reenabled. |
| PUT | /amazonclouddirectory/2017-01-11/directory/enable | Enables the specified directory. Only disabled directories can be enabled. Once enabled, the directory can then be read and written to. |
| POST | /amazonclouddirectory/2017-01-11/schema/getappliedschema | Returns current applied schema version ARN, including the minor version in use. |
| POST | /amazonclouddirectory/2017-01-11/directory/get | Retrieves metadata about a directory. |
| POST | /amazonclouddirectory/2017-01-11/facet | Gets details of the Facet, such as facet name, attributes, Rules, or ObjectType. You can call this on all kinds of schema facets -- published, development, or applied. |
| POST | /amazonclouddirectory/2017-01-11/typedlink/attributes/get | Retrieves attributes that are associated with a typed link. |
| POST | /amazonclouddirectory/2017-01-11/object/attributes/get | Retrieves attributes within a facet that are associated with an object. |
| POST | /amazonclouddirectory/2017-01-11/object/information | Retrieves metadata about an object. |
| POST | /amazonclouddirectory/2017-01-11/schema/json | Retrieves a JSON representation of the schema. See JSON Schema Format for more information. |
| POST | /amazonclouddirectory/2017-01-11/typedlink/facet/get | Returns the identity attribute order for a specific TypedLinkFacet. For more information, see Typed Links. |
| POST | /amazonclouddirectory/2017-01-11/schema/applied | Lists schema major versions applied to a directory. If SchemaArn is provided, lists the minor version. |
| POST | /amazonclouddirectory/2017-01-11/object/indices | Lists indices attached to the specified object. |
| POST | /amazonclouddirectory/2017-01-11/schema/development | Retrieves each Amazon Resource Name (ARN) of schemas in the development state. |
| POST | /amazonclouddirectory/2017-01-11/directory/list | Lists directories created within an account. |
| POST | /amazonclouddirectory/2017-01-11/facet/attributes | Retrieves attributes attached to the facet. |
| POST | /amazonclouddirectory/2017-01-11/facet/list | Retrieves the names of facets that exist in a schema. |
| POST | /amazonclouddirectory/2017-01-11/typedlink/incoming | Returns a paginated list of all the incoming TypedLinkSpecifier information for an object. It also supports filtering by typed link facet and identity attributes. For more information, see Typed Links. |
| POST | /amazonclouddirectory/2017-01-11/index/targets | Lists objects attached to the specified index. |
| POST | /amazonclouddirectory/2017-01-11/schema/managed | Lists the major version families of each managed schema. If a major version ARN is provided as SchemaArn, the minor version revisions in that family are listed instead. |
| POST | /amazonclouddirectory/2017-01-11/object/attributes | Lists all attributes that are associated with an object. |
| POST | /amazonclouddirectory/2017-01-11/object/children | Returns a paginated list of child objects that are associated with a given object. |
| POST | /amazonclouddirectory/2017-01-11/object/parentpaths | Retrieves all available parent paths for any object type such as node, leaf node, policy node, and index node objects. For more information about objects, see Directory Structure. Use this API to evaluate all parents for an object. The call returns all objects from the root of the directory up to the requested object. The API returns the number of paths based on user-defined MaxResults, in case there are multiple paths to the parent. The order of the paths and nodes returned is consistent among multiple API calls unless the objects are deleted or moved. Paths not leading to the directory root are ignored from the target object. |
| POST | /amazonclouddirectory/2017-01-11/object/parent | Lists parent objects that are associated with a given object in pagination fashion. |
| POST | /amazonclouddirectory/2017-01-11/object/policy | Returns policies attached to an object in pagination fashion. |
| POST | /amazonclouddirectory/2017-01-11/typedlink/outgoing | Returns a paginated list of all the outgoing TypedLinkSpecifier information for an object. It also supports filtering by typed link facet and identity attributes. For more information, see Typed Links. |
| POST | /amazonclouddirectory/2017-01-11/policy/attachment | Returns all of the ObjectIdentifiers to which a given policy is attached. |
| POST | /amazonclouddirectory/2017-01-11/schema/published | Lists the major version families of each published schema. If a major version ARN is provided as SchemaArn, the minor version revisions in that family are listed instead. |
| POST | /amazonclouddirectory/2017-01-11/tags | Returns tags for a resource. Tagging is currently supported only for directories with a limit of 50 tags per directory. All 50 tags are returned for a given directory with this API call. |
| POST | /amazonclouddirectory/2017-01-11/typedlink/facet/attributes | Returns a paginated list of all attribute definitions for a particular TypedLinkFacet. For more information, see Typed Links. |
| POST | /amazonclouddirectory/2017-01-11/typedlink/facet/list | Returns a paginated list of TypedLink facet names for a particular schema. For more information, see Typed Links. |
| POST | /amazonclouddirectory/2017-01-11/policy/lookup | Lists all policies from the root of the Directory to the object specified. If there are no policies present, an empty list is returned. If policies are present, and if some objects don't have the policies attached, it returns the ObjectIdentifier for such objects. If policies are present, it returns ObjectIdentifier, policyId, and policyType. Paths that don't lead to the root from the target object are ignored. For more information, see Policies. |
| PUT | /amazonclouddirectory/2017-01-11/schema/publish | Publishes a development schema with a major version and a recommended minor version. |
| PUT | /amazonclouddirectory/2017-01-11/schema/json | Allows a schema to be updated using JSON upload. Only available for development schemas. See JSON Schema Format for more information. |
| PUT | /amazonclouddirectory/2017-01-11/object/facets/delete | Removes the specified facet from the specified object. |
| PUT | /amazonclouddirectory/2017-01-11/tags/add | An API operation for adding tags to a resource. |
| PUT | /amazonclouddirectory/2017-01-11/tags/remove | An API operation for removing tags from a resource. |
| PUT | /amazonclouddirectory/2017-01-11/facet | Does the following:   Adds new Attributes, Rules, or ObjectTypes.   Updates existing Attributes, Rules, or ObjectTypes.   Deletes existing Attributes, Rules, or ObjectTypes. |
| POST | /amazonclouddirectory/2017-01-11/typedlink/attributes/update | Updates a given typed link’s attributes. Attributes to be updated must not contribute to the typed link’s identity, as defined by its IdentityAttributeOrder. |
| PUT | /amazonclouddirectory/2017-01-11/object/update | Updates a given object's attributes. |
| PUT | /amazonclouddirectory/2017-01-11/schema/update | Updates the schema name with a new name. Only development schema names can be updated. |
| PUT | /amazonclouddirectory/2017-01-11/typedlink/facet | Updates a TypedLinkFacet. For more information, see Typed Links. |
| PUT | /amazonclouddirectory/2017-01-11/schema/upgradeapplied | Upgrades a single directory in-place using the PublishedSchemaArn with schema updates found in MinorVersion. Backwards-compatible minor version upgrades are instantaneously available for readers on all objects in the directory. Note: This is a synchronous API call and upgrades only one schema on a given directory per call. To upgrade multiple directories from one schema, you would need to call this API on each directory. |
| PUT | /amazonclouddirectory/2017-01-11/schema/upgradepublished | Upgrades a published schema under a new minor version revision using the current contents of DevelopmentSchemaArn. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batchread?" -> POST /amazonclouddirectory/2017-01-11/batchread
- "Create a getappliedschema?" -> POST /amazonclouddirectory/2017-01-11/schema/getappliedschema
- "Create a get?" -> POST /amazonclouddirectory/2017-01-11/directory/get
- "Create a facet?" -> POST /amazonclouddirectory/2017-01-11/facet
- "Create a get?" -> POST /amazonclouddirectory/2017-01-11/typedlink/attributes/get
- "Create a get?" -> POST /amazonclouddirectory/2017-01-11/object/attributes/get
- "Create a information?" -> POST /amazonclouddirectory/2017-01-11/object/information
- "Create a json?" -> POST /amazonclouddirectory/2017-01-11/schema/json
- "Create a get?" -> POST /amazonclouddirectory/2017-01-11/typedlink/facet/get
- "Create a applied?" -> POST /amazonclouddirectory/2017-01-11/schema/applied
- "Create a indice?" -> POST /amazonclouddirectory/2017-01-11/object/indices
- "Create a development?" -> POST /amazonclouddirectory/2017-01-11/schema/development
- "Create a list?" -> POST /amazonclouddirectory/2017-01-11/directory/list
- "Create a attribute?" -> POST /amazonclouddirectory/2017-01-11/facet/attributes
- "Create a list?" -> POST /amazonclouddirectory/2017-01-11/facet/list
- "Create a incoming?" -> POST /amazonclouddirectory/2017-01-11/typedlink/incoming
- "Create a target?" -> POST /amazonclouddirectory/2017-01-11/index/targets
- "Create a managed?" -> POST /amazonclouddirectory/2017-01-11/schema/managed
- "Create a attribute?" -> POST /amazonclouddirectory/2017-01-11/object/attributes
- "Create a children?" -> POST /amazonclouddirectory/2017-01-11/object/children
- "Create a parentpath?" -> POST /amazonclouddirectory/2017-01-11/object/parentpaths
- "Create a parent?" -> POST /amazonclouddirectory/2017-01-11/object/parent
- "Create a policy?" -> POST /amazonclouddirectory/2017-01-11/object/policy
- "Create a outgoing?" -> POST /amazonclouddirectory/2017-01-11/typedlink/outgoing
- "Create a attachment?" -> POST /amazonclouddirectory/2017-01-11/policy/attachment
- "Create a published?" -> POST /amazonclouddirectory/2017-01-11/schema/published
- "Create a tag?" -> POST /amazonclouddirectory/2017-01-11/tags
- "Create a attribute?" -> POST /amazonclouddirectory/2017-01-11/typedlink/facet/attributes
- "Create a list?" -> POST /amazonclouddirectory/2017-01-11/typedlink/facet/list
- "Create a lookup?" -> POST /amazonclouddirectory/2017-01-11/policy/lookup
- "Create a update?" -> POST /amazonclouddirectory/2017-01-11/typedlink/attributes/update
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
