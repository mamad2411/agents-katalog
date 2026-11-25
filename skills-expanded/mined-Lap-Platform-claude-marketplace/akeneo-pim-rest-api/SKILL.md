---
name: akeneo-pim-rest-api
description: "Akeneo PIM REST API skill. Use when working with Akeneo PIM REST for api. Covers 137 endpoints."
version: 1.0.0
generator: lapsh
---

# Akeneo PIM REST API
API version: 1.0.0

## Auth
ApiKey Authorization in header

## Base URL
http://demo.akeneo.com

## Setup
1. Set your API key in the appropriate header
2. GET /api/rest/v1/products-uuid -- verify access
3. POST /api/rest/v1/products-uuid -- create first products-uuid

## Endpoints

137 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/rest/v1/products-uuid | Get list of products |
| POST | /api/rest/v1/products-uuid | Create a new product |
| PATCH | /api/rest/v1/products-uuid | Update/create several products |
| POST | /api/rest/v1/products-uuid/search | Search list of products |
| GET | /api/rest/v1/products-uuid/{uuid} | Get a product |
| PATCH | /api/rest/v1/products-uuid/{uuid} | Update/create a product |
| DELETE | /api/rest/v1/products-uuid/{uuid} | Delete a product |
| POST | /api/rest/v1/products-uuid/{uuid}/proposal | Submit a draft for approval |
| GET | /api/rest/v1/products-uuid/{uuid}/draft | Get a draft |
| GET | /api/rest/v1/products | Get list of products |
| POST | /api/rest/v1/products | Create a new product |
| PATCH | /api/rest/v1/products | Update/create several products |
| GET | /api/rest/v1/products/{code} | Get a product |
| PATCH | /api/rest/v1/products/{code} | Update/create a product |
| DELETE | /api/rest/v1/products/{code} | Delete a product |
| POST | /api/rest/v1/products/{code}/proposal | Submit a draft for approval |
| GET | /api/rest/v1/products/{code}/draft | Get a draft |
| GET | /api/rest/v1/product-models | Get list of product models |
| POST | /api/rest/v1/product-models | Create a new product model |
| PATCH | /api/rest/v1/product-models | Update/create several product models |
| GET | /api/rest/v1/product-models/{code} | Get a product model |
| PATCH | /api/rest/v1/product-models/{code} | Update/create a product model |
| DELETE | /api/rest/v1/product-models/{code} | Delete a product model |
| POST | /api/rest/v1/product-models/{code}/proposal | Submit a draft for approval |
| GET | /api/rest/v1/product-models/{code}/draft | Get a draft |
| GET | /api/rest/v1/published-products | Get list of published products |
| GET | /api/rest/v1/published-products/{code} | Get a published product |
| GET | /api/rest/v1/media-files | Get a list of product media files |
| POST | /api/rest/v1/media-files | Create a new product media file |
| GET | /api/rest/v1/media-files/{code} | Get a product media file |
| GET | /api/rest/v1/media-files/{code}/download | Download a product media file |
| POST | /api/rest/v1/jobs/export/{code} | Launch export job by code |
| POST | /api/rest/v1/jobs/import/{code} | Launch import job by code |
| GET | /api/rest/v1/families | Get list of families |
| POST | /api/rest/v1/families | Create a new family |
| PATCH | /api/rest/v1/families | Update/create several families |
| GET | /api/rest/v1/families/{code} | Get a family |
| PATCH | /api/rest/v1/families/{code} | Update/create a family |
| DELETE | /api/rest/v1/families/{code} | Delete a family |
| GET | /api/rest/v1/families/{family_code}/variants | Get list of family variants |
| POST | /api/rest/v1/families/{family_code}/variants | Create a new family variant |
| PATCH | /api/rest/v1/families/{family_code}/variants | Update/create several family variants |
| GET | /api/rest/v1/families/{family_code}/variants/{code} | Get a family variant |
| PATCH | /api/rest/v1/families/{family_code}/variants/{code} | Update/create a family variant |
| GET | /api/rest/v1/attributes | Get list of attributes |
| POST | /api/rest/v1/attributes | Create a new attribute |
| PATCH | /api/rest/v1/attributes | Update/create several attributes |
| GET | /api/rest/v1/attributes/{code} | Get an attribute |
| PATCH | /api/rest/v1/attributes/{code} | Update/create an attribute |
| GET | /api/rest/v1/attributes/{attribute_code}/options | Get list of attribute options |
| POST | /api/rest/v1/attributes/{attribute_code}/options | Create a new attribute option |
| PATCH | /api/rest/v1/attributes/{attribute_code}/options | Update/create several attribute options |
| GET | /api/rest/v1/attributes/{attribute_code}/options/{code} | Get an attribute option |
| PATCH | /api/rest/v1/attributes/{attribute_code}/options/{code} | Update/create an attribute option |
| GET | /api/rest/v1/attribute-groups | Get list of attribute groups |
| POST | /api/rest/v1/attribute-groups | Create a new attribute group |
| PATCH | /api/rest/v1/attribute-groups | Update/create several attribute groups |
| GET | /api/rest/v1/attribute-groups/{code} | Get an attribute group |
| PATCH | /api/rest/v1/attribute-groups/{code} | Update/create an attribute group |
| GET | /api/rest/v1/association-types | Get a list of association types |
| POST | /api/rest/v1/association-types | Create a new association type |
| PATCH | /api/rest/v1/association-types | Update/create several association types |
| GET | /api/rest/v1/association-types/{code} | Get an association type |
| PATCH | /api/rest/v1/association-types/{code} | Update/create an association type |
| GET | /api/rest/v1/channels | Get a list of channels |
| POST | /api/rest/v1/channels | Create a new channel |
| PATCH | /api/rest/v1/channels | Update/create several channels |
| GET | /api/rest/v1/channels/{code} | Get a channel |
| PATCH | /api/rest/v1/channels/{code} | Update/create a channel |
| GET | /api/rest/v1/locales | Get a list of locales |
| GET | /api/rest/v1/locales/{code} | Get a locale |
| GET | /api/rest/v1/categories | Get list of categories |
| POST | /api/rest/v1/categories | Create a new category |
| PATCH | /api/rest/v1/categories | Update/create several categories |
| GET | /api/rest/v1/categories/{code} | Get a category |
| PATCH | /api/rest/v1/categories/{code} | Update/create a category |
| POST | /api/rest/v1/category-media-files | Create a category media file |
| GET | /api/rest/v1/category-media-files/{file_path}/download | Download a category media file |
| GET | /api/rest/v1/currencies | Get a list of currencies |
| GET | /api/rest/v1/currencies/{code} | Get a currency |
| GET | /api/rest/v1/measure-families | Get list of measure families (deprecated as of v5.0) |
| GET | /api/rest/v1/measure-families/{code} | Get a measure family (deprecated as of v5.0) |
| GET | /api/rest/v1/measurement-families | Get list of measurement families |
| PATCH | /api/rest/v1/measurement-families | Update/create several measurement families |
| GET | /api/rest/v1/reference-entities | Get list of reference entities |
| GET | /api/rest/v1/reference-entities/{code} | Get a reference entity |
| PATCH | /api/rest/v1/reference-entities/{code} | Update/create a reference entity |
| GET | /api/rest/v1/reference-entities/{reference_entity_code}/attributes | Get the list of attributes of a given reference entity |
| GET | /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{code} | Get an attribute of a given reference entity |
| PATCH | /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{code} | Update/create an attribute of a given reference entity |
| GET | /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{attribute_code}/options | Get a list of attribute options of a given attribute for a given reference entity |
| GET | /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{attribute_code}/options/{code} | Get an attribute option for a given attribute of a given reference entity |
| PATCH | /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{attribute_code}/options/{code} | Update/create a reference entity attribute option |
| GET | /api/rest/v1/reference-entities/{reference_entity_code}/records | Get the list of the records of a reference entity |
| PATCH | /api/rest/v1/reference-entities/{reference_entity_code}/records | Update/create several reference entity records |
| GET | /api/rest/v1/reference-entities/{reference_entity_code}/records/{code} | Get a record of a given reference entity |
| PATCH | /api/rest/v1/reference-entities/{reference_entity_code}/records/{code} | Update/create a record of a given reference entity |
| POST | /api/rest/v1/reference-entities-media-files | Create a new media file for a reference entity or a record |
| GET | /api/rest/v1/reference-entities-media-files/{code} | Download the media file associated to a reference entity or a record |
| GET | /api/rest/v1/asset-families | Get list of asset families |
| GET | /api/rest/v1/asset-families/{code} | Get an asset family |
| PATCH | /api/rest/v1/asset-families/{code} | Update/create an asset family |
| GET | /api/rest/v1/asset-families/{asset_family_code}/attributes | Get the list of attributes of a given asset family |
| GET | /api/rest/v1/asset-families/{asset_family_code}/attributes/{code} | Get an attribute of a given asset family |
| PATCH | /api/rest/v1/asset-families/{asset_family_code}/attributes/{code} | Update/create an attribute of a given asset family |
| GET | /api/rest/v1/asset-families/{asset_family_code}/attributes/{attribute_code}/options | Get a list of attribute options of a given attribute for a given asset family |
| GET | /api/rest/v1/asset-families/{asset_family_code}/attributes/{attribute_code}/options/{code} | Get an attribute option for a given attribute of a given asset family |
| PATCH | /api/rest/v1/asset-families/{asset_family_code}/attributes/{attribute_code}/options/{code} | Update/create an asset attribute option for a given asset family |
| POST | /api/rest/v1/asset-media-files | Create a new media file for an asset |
| GET | /api/rest/v1/asset-media-files/{code} | Download the media file associated to an asset |
| GET | /api/rest/v1/asset-families/{asset_family_code}/assets | Get the list of the assets of a given asset family |
| PATCH | /api/rest/v1/asset-families/{asset_family_code}/assets | Update/create several assets |
| GET | /api/rest/v1/asset-families/{asset_family_code}/assets/{code} | Get an asset of a given asset family |
| PATCH | /api/rest/v1/asset-families/{asset_family_code}/assets/{code} | Update/create an asset |
| DELETE | /api/rest/v1/asset-families/{asset_family_code}/assets/{code} | Delete an asset |
| GET | /api/rest/v1/assets | Get list of PAM assets |
| POST | /api/rest/v1/assets | Create a new PAM asset |
| PATCH | /api/rest/v1/assets | Update/create several PAM assets |
| GET | /api/rest/v1/assets/{code} | Get a PAM asset |
| PATCH | /api/rest/v1/assets/{code} | Update/create a PAM asset |
| GET | /api/rest/v1/assets/{asset_code}/reference-files/{locale_code} | Get a reference file |
| POST | /api/rest/v1/assets/{asset_code}/reference-files/{locale_code} | Upload a new reference file |
| GET | /api/rest/v1/assets/{asset_code}/reference-files/{locale_code}/download | Download a reference file |
| GET | /api/rest/v1/assets/{asset_code}/variation-files/{channel_code}/{locale_code} | Get a variation file |
| POST | /api/rest/v1/assets/{asset_code}/variation-files/{channel_code}/{locale_code} | Upload a new variation file |
| GET | /api/rest/v1/assets/{asset_code}/variation-files/{channel_code}/{locale_code}/download | Download a variation file |
| GET | /api/rest/v1/asset-categories | Get list of PAM asset categories |
| POST | /api/rest/v1/asset-categories | Create a new PAM asset category |
| PATCH | /api/rest/v1/asset-categories | Update/create several PAM asset categories |
| GET | /api/rest/v1/asset-categories/{code} | Get a PAM asset category |
| PATCH | /api/rest/v1/asset-categories/{code} | Update/create a PAM asset category |
| GET | /api/rest/v1/asset-tags | Get list of PAM asset tags |
| GET | /api/rest/v1/asset-tags/{code} | Get a PAM asset tag |
| PATCH | /api/rest/v1/asset-tags/{code} | Update/create a PAM asset tag |
| GET | /api/rest/v1 | Get list of all endpoints |
| POST | /api/oauth/v1/token | Get authentication token |
| GET | /api/rest/v1/system-information | Get system information |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search products-uuid?" -> GET /api/rest/v1/products-uuid
- "Create a products-uuid?" -> POST /api/rest/v1/products-uuid
- "Create a search?" -> POST /api/rest/v1/products-uuid/search
- "Get products-uuid details?" -> GET /api/rest/v1/products-uuid/{uuid}
- "Partially update a products-uuid?" -> PATCH /api/rest/v1/products-uuid/{uuid}
- "Delete a products-uuid?" -> DELETE /api/rest/v1/products-uuid/{uuid}
- "Create a proposal?" -> POST /api/rest/v1/products-uuid/{uuid}/proposal
- "List all draft?" -> GET /api/rest/v1/products-uuid/{uuid}/draft
- "Search products?" -> GET /api/rest/v1/products
- "Create a product?" -> POST /api/rest/v1/products
- "Get product details?" -> GET /api/rest/v1/products/{code}
- "Partially update a product?" -> PATCH /api/rest/v1/products/{code}
- "Delete a product?" -> DELETE /api/rest/v1/products/{code}
- "Create a proposal?" -> POST /api/rest/v1/products/{code}/proposal
- "List all draft?" -> GET /api/rest/v1/products/{code}/draft
- "Search product-models?" -> GET /api/rest/v1/product-models
- "Create a product-model?" -> POST /api/rest/v1/product-models
- "Get product-model details?" -> GET /api/rest/v1/product-models/{code}
- "Partially update a product-model?" -> PATCH /api/rest/v1/product-models/{code}
- "Delete a product-model?" -> DELETE /api/rest/v1/product-models/{code}
- "Create a proposal?" -> POST /api/rest/v1/product-models/{code}/proposal
- "List all draft?" -> GET /api/rest/v1/product-models/{code}/draft
- "Search published-products?" -> GET /api/rest/v1/published-products
- "Get published-product details?" -> GET /api/rest/v1/published-products/{code}
- "List all media-files?" -> GET /api/rest/v1/media-files
- "Create a media-file?" -> POST /api/rest/v1/media-files
- "Get media-file details?" -> GET /api/rest/v1/media-files/{code}
- "List all download?" -> GET /api/rest/v1/media-files/{code}/download
- "Search families?" -> GET /api/rest/v1/families
- "Create a family?" -> POST /api/rest/v1/families
- "Get family details?" -> GET /api/rest/v1/families/{code}
- "Partially update a family?" -> PATCH /api/rest/v1/families/{code}
- "Delete a family?" -> DELETE /api/rest/v1/families/{code}
- "List all variants?" -> GET /api/rest/v1/families/{family_code}/variants
- "Create a variant?" -> POST /api/rest/v1/families/{family_code}/variants
- "Get variant details?" -> GET /api/rest/v1/families/{family_code}/variants/{code}
- "Partially update a variant?" -> PATCH /api/rest/v1/families/{family_code}/variants/{code}
- "Search attributes?" -> GET /api/rest/v1/attributes
- "Create a attribute?" -> POST /api/rest/v1/attributes
- "Get attribute details?" -> GET /api/rest/v1/attributes/{code}
- "Partially update a attribute?" -> PATCH /api/rest/v1/attributes/{code}
- "List all options?" -> GET /api/rest/v1/attributes/{attribute_code}/options
- "Create a option?" -> POST /api/rest/v1/attributes/{attribute_code}/options
- "Get option details?" -> GET /api/rest/v1/attributes/{attribute_code}/options/{code}
- "Partially update a option?" -> PATCH /api/rest/v1/attributes/{attribute_code}/options/{code}
- "Search attribute-groups?" -> GET /api/rest/v1/attribute-groups
- "Create a attribute-group?" -> POST /api/rest/v1/attribute-groups
- "Get attribute-group details?" -> GET /api/rest/v1/attribute-groups/{code}
- "Partially update a attribute-group?" -> PATCH /api/rest/v1/attribute-groups/{code}
- "List all association-types?" -> GET /api/rest/v1/association-types
- "Create a association-type?" -> POST /api/rest/v1/association-types
- "Get association-type details?" -> GET /api/rest/v1/association-types/{code}
- "Partially update a association-type?" -> PATCH /api/rest/v1/association-types/{code}
- "List all channels?" -> GET /api/rest/v1/channels
- "Create a channel?" -> POST /api/rest/v1/channels
- "Get channel details?" -> GET /api/rest/v1/channels/{code}
- "Partially update a channel?" -> PATCH /api/rest/v1/channels/{code}
- "Search locales?" -> GET /api/rest/v1/locales
- "Get locale details?" -> GET /api/rest/v1/locales/{code}
- "Search categories?" -> GET /api/rest/v1/categories
- "Create a category?" -> POST /api/rest/v1/categories
- "Get category details?" -> GET /api/rest/v1/categories/{code}
- "Partially update a category?" -> PATCH /api/rest/v1/categories/{code}
- "Create a category-media-file?" -> POST /api/rest/v1/category-media-files
- "List all download?" -> GET /api/rest/v1/category-media-files/{file_path}/download
- "Search currencies?" -> GET /api/rest/v1/currencies
- "Get currency details?" -> GET /api/rest/v1/currencies/{code}
- "List all measure-families?" -> GET /api/rest/v1/measure-families
- "Get measure-family details?" -> GET /api/rest/v1/measure-families/{code}
- "List all measurement-families?" -> GET /api/rest/v1/measurement-families
- "List all reference-entities?" -> GET /api/rest/v1/reference-entities
- "Get reference-entity details?" -> GET /api/rest/v1/reference-entities/{code}
- "Partially update a reference-entity?" -> PATCH /api/rest/v1/reference-entities/{code}
- "List all attributes?" -> GET /api/rest/v1/reference-entities/{reference_entity_code}/attributes
- "Get attribute details?" -> GET /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{code}
- "Partially update a attribute?" -> PATCH /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{code}
- "List all options?" -> GET /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{attribute_code}/options
- "Get option details?" -> GET /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{attribute_code}/options/{code}
- "Partially update a option?" -> PATCH /api/rest/v1/reference-entities/{reference_entity_code}/attributes/{attribute_code}/options/{code}
- "Search records?" -> GET /api/rest/v1/reference-entities/{reference_entity_code}/records
- "Get record details?" -> GET /api/rest/v1/reference-entities/{reference_entity_code}/records/{code}
- "Partially update a record?" -> PATCH /api/rest/v1/reference-entities/{reference_entity_code}/records/{code}
- "Create a reference-entities-media-file?" -> POST /api/rest/v1/reference-entities-media-files
- "Get reference-entities-media-file details?" -> GET /api/rest/v1/reference-entities-media-files/{code}
- "List all asset-families?" -> GET /api/rest/v1/asset-families
- "Get asset-family details?" -> GET /api/rest/v1/asset-families/{code}
- "Partially update a asset-family?" -> PATCH /api/rest/v1/asset-families/{code}
- "List all attributes?" -> GET /api/rest/v1/asset-families/{asset_family_code}/attributes
- "Get attribute details?" -> GET /api/rest/v1/asset-families/{asset_family_code}/attributes/{code}
- "Partially update a attribute?" -> PATCH /api/rest/v1/asset-families/{asset_family_code}/attributes/{code}
- "List all options?" -> GET /api/rest/v1/asset-families/{asset_family_code}/attributes/{attribute_code}/options
- "Get option details?" -> GET /api/rest/v1/asset-families/{asset_family_code}/attributes/{attribute_code}/options/{code}
- "Partially update a option?" -> PATCH /api/rest/v1/asset-families/{asset_family_code}/attributes/{attribute_code}/options/{code}
- "Create a asset-media-file?" -> POST /api/rest/v1/asset-media-files
- "Get asset-media-file details?" -> GET /api/rest/v1/asset-media-files/{code}
- "Search assets?" -> GET /api/rest/v1/asset-families/{asset_family_code}/assets
- "Get asset details?" -> GET /api/rest/v1/asset-families/{asset_family_code}/assets/{code}
- "Partially update a asset?" -> PATCH /api/rest/v1/asset-families/{asset_family_code}/assets/{code}
- "Delete a asset?" -> DELETE /api/rest/v1/asset-families/{asset_family_code}/assets/{code}
- "List all assets?" -> GET /api/rest/v1/assets
- "Create a asset?" -> POST /api/rest/v1/assets
- "Get asset details?" -> GET /api/rest/v1/assets/{code}
- "Partially update a asset?" -> PATCH /api/rest/v1/assets/{code}
- "Get reference-file details?" -> GET /api/rest/v1/assets/{asset_code}/reference-files/{locale_code}
- "List all download?" -> GET /api/rest/v1/assets/{asset_code}/reference-files/{locale_code}/download
- "Get variation-file details?" -> GET /api/rest/v1/assets/{asset_code}/variation-files/{channel_code}/{locale_code}
- "List all download?" -> GET /api/rest/v1/assets/{asset_code}/variation-files/{channel_code}/{locale_code}/download
- "List all asset-categories?" -> GET /api/rest/v1/asset-categories
- "Create a asset-category?" -> POST /api/rest/v1/asset-categories
- "Get asset-category details?" -> GET /api/rest/v1/asset-categories/{code}
- "Partially update a asset-category?" -> PATCH /api/rest/v1/asset-categories/{code}
- "List all asset-tags?" -> GET /api/rest/v1/asset-tags
- "Get asset-tag details?" -> GET /api/rest/v1/asset-tags/{code}
- "Partially update a asset-tag?" -> PATCH /api/rest/v1/asset-tags/{code}
- "List all rest?" -> GET /api/rest/v1
- "Create a token?" -> POST /api/oauth/v1/token
- "List all system-information?" -> GET /api/rest/v1/system-information
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
