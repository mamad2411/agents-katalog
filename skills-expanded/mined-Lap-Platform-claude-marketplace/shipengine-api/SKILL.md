---
name: shipengine-api
description: "ShipEngine API skill. Use when working with ShipEngine for account, addresses, batches. Covers 95 endpoints."
version: 1.0.0
generator: lapsh
---

# ShipEngine API
API version: 1.1.202602041002

## Auth
ApiKey API-Key in header

## Base URL
https://api.shipengine.com

## Setup
1. Set your API key in the appropriate header
2. GET /v1/account/settings -- verify access
3. POST /v1/account/settings/images -- create first images

## Endpoints

95 endpoints across 20 groups. See references/api-spec.lap for full details.

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/account/settings | List Account Settings |
| GET | /v1/account/settings/images | List Account Images |
| POST | /v1/account/settings/images | Create an Account Image |
| GET | /v1/account/settings/images/{label_image_id} | Get Account Image By ID |
| PUT | /v1/account/settings/images/{label_image_id} | Update Account Image By ID |
| DELETE | /v1/account/settings/images/{label_image_id} | Delete Account Image By Id |

### addresses
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v1/addresses/recognize | Parse an address |
| POST | /v1/addresses/validate | Validate An Address |

### batches
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/batches | List Batches |
| POST | /v1/batches | Create A Batch |
| GET | /v1/batches/external_batch_id/{external_batch_id} | Get Batch By External ID |
| DELETE | /v1/batches/{batch_id} | Delete Batch By Id |
| GET | /v1/batches/{batch_id} | Get Batch By ID |
| PUT | /v1/batches/{batch_id} | Update Batch By Id |
| POST | /v1/batches/{batch_id}/add | Add to a Batch |
| GET | /v1/batches/{batch_id}/errors | Get Batch Errors |
| POST | /v1/batches/{batch_id}/process/labels | Process Batch ID Labels |
| POST | /v1/batches/{batch_id}/remove | Remove From Batch |

### carriers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/carriers | List Carriers |
| GET | /v1/carriers/{carrier_id} | Get Carrier By ID |
| DELETE | /v1/carriers/{carrier_id} | Disconnect Carrier by ID |
| PUT | /v1/carriers/{carrier_id}/add_funds | Add Funds To Carrier |
| GET | /v1/carriers/{carrier_id}/options | Get Carrier Options |
| GET | /v1/carriers/{carrier_id}/packages | List Carrier Package Types |
| GET | /v1/carriers/{carrier_id}/services | List Carrier Services |

### connections
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/connections/carriers/{carrier_name} | Connect a carrier account |
| DELETE | /v1/connections/carriers/{carrier_name}/{carrier_id} | Disconnect a carrier |
| GET | /v1/connections/carriers/{carrier_name}/{carrier_id}/settings | Get carrier settings |
| PUT | /v1/connections/carriers/{carrier_name}/{carrier_id}/settings | Update carrier settings |
| DELETE | /v1/connections/insurance/shipsurance | Disconnect a Shipsurance Account |
| POST | /v1/connections/insurance/shipsurance | Connect a Shipsurance Account |

### documents
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/documents/combined_labels | Created Combined Label Document |

### downloads
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/downloads/{dir}/{subdir}/{filename} | Download File |

### environment
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/environment/webhooks | List Webhooks |
| POST | /v1/environment/webhooks | Create a Webhook |
| GET | /v1/environment/webhooks/{webhook_id} | Get Webhook By ID |
| PUT | /v1/environment/webhooks/{webhook_id} | Update a Webhook |
| DELETE | /v1/environment/webhooks/{webhook_id} | Delete Webhook By ID |

### insurance
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /v1/insurance/shipsurance/add_funds | Add Funds To Insurance |
| GET | /v1/insurance/shipsurance/balance | Get Insurance Funds Balance |

### labels
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/labels | List labels |
| POST | /v1/labels | Purchase Label |
| GET | /v1/labels/external_shipment_id/{external_shipment_id} | Get Label By External Shipment ID |
| POST | /v1/labels/rates/{rate_id} | Purchase Label with Rate ID |
| POST | /v1/labels/shipment/{shipment_id} | Purchase Label with Shipment ID |
| GET | /v1/labels/{label_id} | Get Label By ID |
| POST | /v1/labels/{label_id}/return | Create a return label |
| GET | /v1/labels/{label_id}/track | Get Label Tracking Information |
| PUT | /v1/labels/{label_id}/void | Void a Label By ID |

### manifests
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/manifests | List Manifests |
| POST | /v1/manifests | Create Manifest |
| GET | /v1/manifests/{manifest_id} | Get Manifest By Id |
| GET | /v1/manifests/requests/{manifest_request_id} | Get Manifest Request By Id |

### packages
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/packages | List Custom Package Types |
| POST | /v1/packages | Create Custom Package Type |
| GET | /v1/packages/{package_id} | Get Custom Package Type By ID |
| PUT | /v1/packages/{package_id} | Update Custom Package Type By ID |
| DELETE | /v1/packages/{package_id} | Delete A Custom Package By ID |

### pickups
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/pickups | List Scheduled Pickups |
| POST | /v1/pickups | Schedule a Pickup |
| GET | /v1/pickups/{pickup_id} | Get Pickup By ID |
| DELETE | /v1/pickups/{pickup_id} | Delete a Scheduled Pickup |

### rates
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/rates | Get Shipping Rates |
| POST | /v1/rates/bulk | Get Bulk Rates |
| POST | /v1/rates/estimate | Estimate Rates |
| GET | /v1/rates/{rate_id} | Get Rate By ID |

### service_points
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/service_points/list | List Service Points |
| GET | /v1/service_points/{carrier_code}/{country_code}/{service_point_id} | Get Service Point By ID |

### shipments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/shipments | List Shipments |
| POST | /v1/shipments | Create Shipments |
| GET | /v1/shipments/external_shipment_id/{external_shipment_id} | Get Shipment By External ID |
| PUT | /v1/shipments/recognize | Parse shipping info |
| GET | /v1/shipments/{shipment_id} | Get Shipment By ID |
| PUT | /v1/shipments/{shipment_id} | Update Shipment By ID |
| PUT | /v1/shipments/{shipment_id}/cancel | Cancel a Shipment |
| GET | /v1/shipments/{shipment_id}/rates | Get Shipment Rates |
| PUT | /v1/shipments/tags | Update Shipments Tags |
| GET | /v1/shipments/{shipment_id}/tags | Get Shipment Tags |
| POST | /v1/shipments/{shipment_id}/tags/{tag_name} | Add Tag to Shipment |
| DELETE | /v1/shipments/{shipment_id}/tags/{tag_name} | Remove Tag from Shipment |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/tags | Get Tags |
| POST | /v1/tags | Create a New Tag |
| POST | /v1/tags/{tag_name} | Create a New Tag |
| DELETE | /v1/tags/{tag_name} | Delete Tag |
| PUT | /v1/tags/{tag_name}/{new_tag_name} | Update Tag Name |

### tokens
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/tokens/ephemeral | Get Ephemeral Token |

### tracking
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/tracking | Get Tracking Information |
| POST | /v1/tracking/start | Start Tracking a Package |
| POST | /v1/tracking/stop | Stop Tracking a Package |

### warehouses
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/warehouses | List Warehouses |
| POST | /v1/warehouses | Create Warehouse |
| GET | /v1/warehouses/{warehouse_id} | Get Warehouse By Id |
| PUT | /v1/warehouses/{warehouse_id} | Update Warehouse By Id |
| DELETE | /v1/warehouses/{warehouse_id} | Delete Warehouse By ID |
| PUT | /v1/warehouses/{warehouse_id}/settings | Update Warehouse Settings |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all settings?" -> GET /v1/account/settings
- "List all images?" -> GET /v1/account/settings/images
- "Create a image?" -> POST /v1/account/settings/images
- "Get image details?" -> GET /v1/account/settings/images/{label_image_id}
- "Update a image?" -> PUT /v1/account/settings/images/{label_image_id}
- "Delete a image?" -> DELETE /v1/account/settings/images/{label_image_id}
- "Create a validate?" -> POST /v1/addresses/validate
- "List all batches?" -> GET /v1/batches
- "Create a batche?" -> POST /v1/batches
- "Get external_batch_id details?" -> GET /v1/batches/external_batch_id/{external_batch_id}
- "Delete a batche?" -> DELETE /v1/batches/{batch_id}
- "Get batche details?" -> GET /v1/batches/{batch_id}
- "Update a batche?" -> PUT /v1/batches/{batch_id}
- "Create a add?" -> POST /v1/batches/{batch_id}/add
- "List all errors?" -> GET /v1/batches/{batch_id}/errors
- "Create a label?" -> POST /v1/batches/{batch_id}/process/labels
- "Create a remove?" -> POST /v1/batches/{batch_id}/remove
- "List all carriers?" -> GET /v1/carriers
- "Get carrier details?" -> GET /v1/carriers/{carrier_id}
- "Delete a carrier?" -> DELETE /v1/carriers/{carrier_id}
- "List all options?" -> GET /v1/carriers/{carrier_id}/options
- "List all packages?" -> GET /v1/carriers/{carrier_id}/packages
- "List all services?" -> GET /v1/carriers/{carrier_id}/services
- "Delete a carrier?" -> DELETE /v1/connections/carriers/{carrier_name}/{carrier_id}
- "List all settings?" -> GET /v1/connections/carriers/{carrier_name}/{carrier_id}/settings
- "Create a shipsurance?" -> POST /v1/connections/insurance/shipsurance
- "Create a combined_label?" -> POST /v1/documents/combined_labels
- "Get download details?" -> GET /v1/downloads/{dir}/{subdir}/{filename}
- "List all webhooks?" -> GET /v1/environment/webhooks
- "Create a webhook?" -> POST /v1/environment/webhooks
- "Get webhook details?" -> GET /v1/environment/webhooks/{webhook_id}
- "Update a webhook?" -> PUT /v1/environment/webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /v1/environment/webhooks/{webhook_id}
- "List all balance?" -> GET /v1/insurance/shipsurance/balance
- "List all labels?" -> GET /v1/labels
- "Create a label?" -> POST /v1/labels
- "Get external_shipment_id details?" -> GET /v1/labels/external_shipment_id/{external_shipment_id}
- "Get label details?" -> GET /v1/labels/{label_id}
- "Create a return?" -> POST /v1/labels/{label_id}/return
- "List all track?" -> GET /v1/labels/{label_id}/track
- "List all manifests?" -> GET /v1/manifests
- "Create a manifest?" -> POST /v1/manifests
- "Get manifest details?" -> GET /v1/manifests/{manifest_id}
- "Get request details?" -> GET /v1/manifests/requests/{manifest_request_id}
- "List all packages?" -> GET /v1/packages
- "Create a package?" -> POST /v1/packages
- "Get package details?" -> GET /v1/packages/{package_id}
- "Update a package?" -> PUT /v1/packages/{package_id}
- "Delete a package?" -> DELETE /v1/packages/{package_id}
- "List all pickups?" -> GET /v1/pickups
- "Create a pickup?" -> POST /v1/pickups
- "Get pickup details?" -> GET /v1/pickups/{pickup_id}
- "Delete a pickup?" -> DELETE /v1/pickups/{pickup_id}
- "Create a rate?" -> POST /v1/rates
- "Create a bulk?" -> POST /v1/rates/bulk
- "Create a estimate?" -> POST /v1/rates/estimate
- "Get rate details?" -> GET /v1/rates/{rate_id}
- "Create a list?" -> POST /v1/service_points/list
- "Get service_point details?" -> GET /v1/service_points/{carrier_code}/{country_code}/{service_point_id}
- "List all shipments?" -> GET /v1/shipments
- "Create a shipment?" -> POST /v1/shipments
- "Get external_shipment_id details?" -> GET /v1/shipments/external_shipment_id/{external_shipment_id}
- "Get shipment details?" -> GET /v1/shipments/{shipment_id}
- "Update a shipment?" -> PUT /v1/shipments/{shipment_id}
- "List all rates?" -> GET /v1/shipments/{shipment_id}/rates
- "List all tags?" -> GET /v1/shipments/{shipment_id}/tags
- "Delete a tag?" -> DELETE /v1/shipments/{shipment_id}/tags/{tag_name}
- "List all tags?" -> GET /v1/tags
- "Create a tag?" -> POST /v1/tags
- "Delete a tag?" -> DELETE /v1/tags/{tag_name}
- "Update a tag?" -> PUT /v1/tags/{tag_name}/{new_tag_name}
- "Create a ephemeral?" -> POST /v1/tokens/ephemeral
- "List all tracking?" -> GET /v1/tracking
- "Create a start?" -> POST /v1/tracking/start
- "Create a stop?" -> POST /v1/tracking/stop
- "List all warehouses?" -> GET /v1/warehouses
- "Create a warehouse?" -> POST /v1/warehouses
- "Get warehouse details?" -> GET /v1/warehouses/{warehouse_id}
- "Update a warehouse?" -> PUT /v1/warehouses/{warehouse_id}
- "Delete a warehouse?" -> DELETE /v1/warehouses/{warehouse_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
