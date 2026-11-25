---
name: aws-service-catalog-app-registry
description: "AWS Service Catalog App Registry API skill. Use when working with AWS Service Catalog App Registry for applications, attribute-groups, configuration. Covers 24 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Service Catalog App Registry
API version: 2020-06-24

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /configuration -- verify access
3. POST /applications -- create first applications

## Endpoints

24 endpoints across 5 groups. See references/api-spec.lap for full details.

### applications
| Method | Path | Description |
|--------|------|-------------|
| PUT | /applications/{application}/attribute-groups/{attributeGroup} | Associates an attribute group with an application to augment the application's metadata with the group's attributes. This feature enables applications to be described with user-defined details that are machine-readable, such as third-party integrations. |
| PUT | /applications/{application}/resources/{resourceType}/{resource} | Associates a resource with an application. The resource can be specified by its ARN or name. The application can be specified by ARN, ID, or name.   Minimum permissions   You must have the following permissions to associate a resource using the OPTIONS parameter set to APPLY_APPLICATION_TAG.     tag:GetResources     tag:TagResources     You must also have these additional permissions if you don't use the AWSServiceCatalogAppRegistryFullAccess policy. For more information, see AWSServiceCatalogAppRegistryFullAccess in the AppRegistry Administrator Guide.     resource-groups:AssociateResource     cloudformation:UpdateStack     cloudformation:DescribeStacks      In addition, you must have the tagging permission defined by the Amazon Web Services service that creates the resource. For more information, see TagResources in the Resource Groups Tagging API Reference. |
| POST | /applications | Creates a new application that is the top-level node in a hierarchy of related cloud resource abstractions. |
| DELETE | /applications/{application} | Deletes an application that is specified either by its application ID, name, or ARN. All associated attribute groups and resources must be disassociated from it before deleting an application. |
| DELETE | /applications/{application}/attribute-groups/{attributeGroup} | Disassociates an attribute group from an application to remove the extra attributes contained in the attribute group from the application's metadata. This operation reverts AssociateAttributeGroup. |
| DELETE | /applications/{application}/resources/{resourceType}/{resource} | Disassociates a resource from application. Both the resource and the application can be specified either by ID or name.   Minimum permissions   You must have the following permissions to remove a resource that's been associated with an application using the APPLY_APPLICATION_TAG option for AssociateResource.     tag:GetResources     tag:UntagResources     You must also have the following permissions if you don't use the AWSServiceCatalogAppRegistryFullAccess policy. For more information, see AWSServiceCatalogAppRegistryFullAccess in the AppRegistry Administrator Guide.     resource-groups:DisassociateResource     cloudformation:UpdateStack     cloudformation:DescribeStacks      In addition, you must have the tagging permission defined by the Amazon Web Services service that creates the resource. For more information, see UntagResources in the Resource Groups Tagging API Reference. |
| GET | /applications/{application} | Retrieves metadata information about one of your applications. The application can be specified by its ARN, ID, or name (which is unique within one account in one region at a given point in time). Specify by ARN or ID in automated workflows if you want to make sure that the exact same application is returned or a ResourceNotFoundException is thrown, avoiding the ABA addressing problem. |
| GET | /applications/{application}/resources/{resourceType}/{resource} | Gets the resource associated with the application. |
| GET | /applications | Retrieves a list of all of your applications. Results are paginated. |
| GET | /applications/{application}/attribute-groups | Lists all attribute groups that are associated with specified application. Results are paginated. |
| GET | /applications/{application}/resources | Lists all of the resources that are associated with the specified application. Results are paginated.    If you share an application, and a consumer account associates a tag query to the application, all of the users who can access the application can also view the tag values in all accounts that are associated with it using this API. |
| GET | /applications/{application}/attribute-group-details | Lists the details of all attribute groups associated with a specific application. The results display in pages. |
| PATCH | /applications/{application} | Updates an existing application with new attributes. |

### attribute-groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /attribute-groups | Creates a new attribute group as a container for user-defined attributes. This feature enables users to have full control over their cloud application's metadata in a rich machine-readable format to facilitate integration with automated workflows and third-party tools. |
| DELETE | /attribute-groups/{attributeGroup} | Deletes an attribute group, specified either by its attribute group ID, name, or ARN. |
| GET | /attribute-groups/{attributeGroup} | Retrieves an attribute group by its ARN, ID, or name. The attribute group can be specified by its ARN, ID, or name. |
| GET | /attribute-groups | Lists all attribute groups which you have access to. Results are paginated. |
| PATCH | /attribute-groups/{attributeGroup} | Updates an existing attribute group with new details. |

### configuration
| Method | Path | Description |
|--------|------|-------------|
| GET | /configuration | Retrieves a TagKey configuration from an account. |
| PUT | /configuration | Associates a TagKey configuration to an account. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists all of the tags on the resource. |
| POST | /tags/{resourceArn} | Assigns one or more tags (key-value pairs) to the specified resource. Each tag consists of a key and an optional value. If a tag with the same key is already associated with the resource, this action updates its value. This operation returns an empty response if the call was successful. |
| DELETE | /tags/{resourceArn} | Removes tags from a resource. This operation returns an empty response if the call was successful. |

### sync
| Method | Path | Description |
|--------|------|-------------|
| POST | /sync/{resourceType}/{resource} | Syncs the resource with current AppRegistry records. Specifically, the resource’s AppRegistry system tags sync with its associated application. We remove the resource's AppRegistry system tags if it does not associate with the application. The caller must have permissions to read and update the resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a attribute-group?" -> PUT /applications/{application}/attribute-groups/{attributeGroup}
- "Update a resource?" -> PUT /applications/{application}/resources/{resourceType}/{resource}
- "Create a application?" -> POST /applications
- "Create a attribute-group?" -> POST /attribute-groups
- "Delete a application?" -> DELETE /applications/{application}
- "Delete a attribute-group?" -> DELETE /attribute-groups/{attributeGroup}
- "Delete a attribute-group?" -> DELETE /applications/{application}/attribute-groups/{attributeGroup}
- "Delete a resource?" -> DELETE /applications/{application}/resources/{resourceType}/{resource}
- "Get application details?" -> GET /applications/{application}
- "Get resource details?" -> GET /applications/{application}/resources/{resourceType}/{resource}
- "Get attribute-group details?" -> GET /attribute-groups/{attributeGroup}
- "List all configuration?" -> GET /configuration
- "List all applications?" -> GET /applications
- "List all attribute-groups?" -> GET /applications/{application}/attribute-groups
- "List all resources?" -> GET /applications/{application}/resources
- "List all attribute-groups?" -> GET /attribute-groups
- "List all attribute-group-details?" -> GET /applications/{application}/attribute-group-details
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a application?" -> PATCH /applications/{application}
- "Partially update a attribute-group?" -> PATCH /attribute-groups/{attributeGroup}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
