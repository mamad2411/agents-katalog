---
name: aws-outposts
description: "AWS Outposts API skill. Use when working with AWS Outposts for outposts, orders, sites. Covers 31 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Outposts
API version: 2019-12-03

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /capacity/tasks -- verify access
3. POST /outposts/{OutpostId}/capacity/{CapacityTaskId} -- create first capacity

## Endpoints

31 endpoints across 8 groups. See references/api-spec.lap for full details.

### outposts
| Method | Path | Description |
|--------|------|-------------|
| POST | /outposts/{OutpostId}/capacity/{CapacityTaskId} | Cancels the capacity task. |
| POST | /outposts | Creates an Outpost. You can specify either an Availability one or an AZ ID. |
| DELETE | /outposts/{OutpostId} | Deletes the specified Outpost. |
| GET | /outposts/{OutpostId}/capacity/{CapacityTaskId} | Gets details of the specified capacity task. |
| GET | /outposts/{OutpostId} | Gets information about the specified Outpost. |
| GET | /outposts/{OutpostId}/instanceTypes | Gets the instance types for the specified Outpost. |
| GET | /outposts/{OutpostId}/supportedInstanceTypes | Gets the instance types that an Outpost can support in InstanceTypeCapacity. This will generally include instance types that are not currently configured and therefore cannot be launched with the current Outpost capacity configuration. |
| GET | /outposts/{OutpostId}/assets | Lists the hardware assets for the specified Outpost. Use filters to return specific results. If you specify multiple filters, the results include only the resources that match all of the specified filters. For a filter where you can specify multiple values, the results include items that match any of the values that you specify for the filter. |
| GET | /outposts | Lists the Outposts for your Amazon Web Services account. Use filters to return specific results. If you specify multiple filters, the results include only the resources that match all of the specified filters. For a filter where you can specify multiple values, the results include items that match any of the values that you specify for the filter. |
| POST | /outposts/{OutpostId}/capacity | Starts the specified capacity task. You can have one active capacity task for an order. |
| PATCH | /outposts/{OutpostId} | Updates an Outpost. |

### orders
| Method | Path | Description |
|--------|------|-------------|
| POST | /orders/{OrderId}/cancel | Cancels the specified order for an Outpost. |
| POST | /orders | Creates an order for an Outpost. |
| GET | /orders/{OrderId} | Gets information about the specified order. |

### sites
| Method | Path | Description |
|--------|------|-------------|
| POST | /sites | Creates a site for an Outpost. |
| DELETE | /sites/{SiteId} | Deletes the specified site. |
| GET | /sites/{SiteId} | Gets information about the specified Outpost site. |
| GET | /sites/{SiteId}/address | Gets the site address of the specified site. |
| GET | /sites | Lists the Outpost sites for your Amazon Web Services account. Use filters to return specific results. Use filters to return specific results. If you specify multiple filters, the results include only the resources that match all of the specified filters. For a filter where you can specify multiple values, the results include items that match any of the values that you specify for the filter. |
| PATCH | /sites/{SiteId} | Updates the specified site. |
| PUT | /sites/{SiteId}/address | Updates the address of the specified site. You can't update a site address if there is an order in progress. You must wait for the order to complete or cancel the order. You can update the operating address before you place an order at the site, or after all Outposts that belong to the site have been deactivated. |
| PATCH | /sites/{SiteId}/rackPhysicalProperties | Update the physical and logistical details for a rack at a site. For more information about hardware requirements for racks, see Network readiness checklist in the Amazon Web Services Outposts User Guide.  To update a rack at a site with an order of IN_PROGRESS, you must wait for the order to complete or cancel the order. |

### catalog
| Method | Path | Description |
|--------|------|-------------|
| GET | /catalog/item/{CatalogItemId} | Gets information about the specified catalog item. |
| GET | /catalog/items | Lists the items in the catalog. Use filters to return specific results. If you specify multiple filters, the results include only the resources that match all of the specified filters. For a filter where you can specify multiple values, the results include items that match any of the values that you specify for the filter. |

### connections
| Method | Path | Description |
|--------|------|-------------|
| GET | /connections/{ConnectionId} | Amazon Web Services uses this action to install Outpost servers.   Gets information about the specified connection.   Use CloudTrail to monitor this action or Amazon Web Services managed policy for Amazon Web Services Outposts to secure it. For more information, see  Amazon Web Services managed policies for Amazon Web Services Outposts and  Logging Amazon Web Services Outposts API calls with Amazon Web Services CloudTrail in the Amazon Web Services Outposts User Guide. |
| POST | /connections | Amazon Web Services uses this action to install Outpost servers.   Starts the connection required for Outpost server installation.   Use CloudTrail to monitor this action or Amazon Web Services managed policy for Amazon Web Services Outposts to secure it. For more information, see  Amazon Web Services managed policies for Amazon Web Services Outposts and  Logging Amazon Web Services Outposts API calls with Amazon Web Services CloudTrail in the Amazon Web Services Outposts User Guide. |

### capacity
| Method | Path | Description |
|--------|------|-------------|
| GET | /capacity/tasks | Lists the capacity tasks for your Amazon Web Services account. Use filters to return specific results. If you specify multiple filters, the results include only the resources that match all of the specified filters. For a filter where you can specify multiple values, the results include items that match any of the values that you specify for the filter. |

### list-orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /list-orders | Lists the Outpost orders for your Amazon Web Services account. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | Lists the tags for the specified resource. |
| POST | /tags/{ResourceArn} | Adds tags to the specified resource. |
| DELETE | /tags/{ResourceArn} | Removes tags from the specified resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a cancel?" -> POST /orders/{OrderId}/cancel
- "Create a order?" -> POST /orders
- "Create a outpost?" -> POST /outposts
- "Create a site?" -> POST /sites
- "Delete a outpost?" -> DELETE /outposts/{OutpostId}
- "Delete a site?" -> DELETE /sites/{SiteId}
- "Get capacity details?" -> GET /outposts/{OutpostId}/capacity/{CapacityTaskId}
- "Get item details?" -> GET /catalog/item/{CatalogItemId}
- "Get connection details?" -> GET /connections/{ConnectionId}
- "Get order details?" -> GET /orders/{OrderId}
- "Get outpost details?" -> GET /outposts/{OutpostId}
- "List all instanceTypes?" -> GET /outposts/{OutpostId}/instanceTypes
- "List all supportedInstanceTypes?" -> GET /outposts/{OutpostId}/supportedInstanceTypes
- "Get site details?" -> GET /sites/{SiteId}
- "List all address?" -> GET /sites/{SiteId}/address
- "List all assets?" -> GET /outposts/{OutpostId}/assets
- "List all tasks?" -> GET /capacity/tasks
- "List all items?" -> GET /catalog/items
- "List all list-orders?" -> GET /list-orders
- "List all outposts?" -> GET /outposts
- "List all sites?" -> GET /sites
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Create a capacity?" -> POST /outposts/{OutpostId}/capacity
- "Create a connection?" -> POST /connections
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Partially update a outpost?" -> PATCH /outposts/{OutpostId}
- "Partially update a site?" -> PATCH /sites/{SiteId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
