---
name: tcgplayer
description: TCGplayer Documentation documentation and resources. Use this skill when working with TCGplayer Documentation or when the user mentions tcgplayer documentation.
metadata:
  source: llms.txt
  source_url: https://docs.tcgplayer.com/llms.txt
  generated: 2026-05-04T13:02:26.116Z
---

# TCGplayer Documentation

## Available Resources

### Guides

- **Welcome!**
  - URL: https://docs.tcgplayer.com/docs/welcome.md

- **FAQ**
  - URL: https://docs.tcgplayer.com/docs/announcements.md

- **Getting Started with TCGplayer API**: This page will help you get started with TCGplayer. You'll be up and running in a jiffy!
  - URL: https://docs.tcgplayer.com/docs/getting-started.md

- **TCGplayer Affiliate Program**: This page displays the details of our affiliate program and the steps necessary to get involved. It also covers linking to receive referral credit.
  - URL: https://docs.tcgplayer.com/docs/tcgplayer-affiliate-program.md

- **External Kickbacks API**: Run this script to determine if TCGplayer is running and active kickback and it's details
  - URL: https://docs.tcgplayer.com/docs/external-kickbacks-api.md

- **Store Authorization Workflow**
  - URL: https://docs.tcgplayer.com/docs/store-authorization-workflow.md

- **Advanced Search**
  - URL: https://docs.tcgplayer.com/docs/advanced-search.md

- **v1.39.0**
  - URL: https://docs.tcgplayer.com/docs/v1390.md

### API Reference

- **Authorize an Application**: Create an application key based on an previously generated
  - URL: https://docs.tcgplayer.com/reference/app_authorizeapplication.md

- **Catalog**
  - URL: https://docs.tcgplayer.com/reference/catalog.md

- **List All Categories**: This endpoint returns a paged list of all categories supported by TCGplayer.
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategories-1.md

- **Get Category Details**: This endpoint returns an array of categories whose Ids were specified in the
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategory-1.md

- **Get Category Search Manifest**: This endpoint returns a search manifest for the specified category.  The search
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategorysearchmanifest.md

- **Search Category Products**: This endpoint returns an array of product Ids that match the provided search critera.
  - URL: https://docs.tcgplayer.com/reference/catalog_searchcategory.md

- **List All Category Groups**: This endpoint returns a paged list of all the groups associated with the specified
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategorygroups-1.md

- **List All Category Rarities**: This endpoint returns all available rarities associated with the specified category.
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategoryrarities.md

- **List All Category Printings**: This endpoint returns all available printings associated with the specified category.
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategoryprintings.md

- **List All Category Conditions**: This endpoint returns all available conditions associated with the specified
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategoryconditions.md

- **List All Category Languages**: This endpoint returns all available languages associated with the specified category.
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategorylanguages.md

- **List All Category Media**: This endpoint returns all available media (e.g. images) associated with the specified
  - URL: https://docs.tcgplayer.com/reference/catalog_getcategorymedia.md

- **List All Groups Details**: This endpoint returns all groups that match the specified criteria.
  - URL: https://docs.tcgplayer.com/reference/catalog_getgroups-1.md

- **Get Group Details**: This endpoint returns an array of groups whose Ids were specified in the groupIds
  - URL: https://docs.tcgplayer.com/reference/catalog_getgroup-1.md

- **List All Group Media**: This endpoint returns all available media (e.g. images) associated with the
  - URL: https://docs.tcgplayer.com/reference/catalog_getgroupmedia.md

- **List All Products**: This endpoint returns all products that match the specified criteria.
  - URL: https://docs.tcgplayer.com/reference/catalog_getproducts-1.md

- **Get Product Details**: This endpoint returns an array of products whose Ids were specified in the productIds
  - URL: https://docs.tcgplayer.com/reference/catalog_getproduct-1.md

- **Get Product Details By GTIN**: This endpoint returns a Product's details using a code from the GTIN family of
  - URL: https://docs.tcgplayer.com/reference/catalog_getproductbygtin-1.md

- **List Product SKUs**: This endpoint returns all of the available SKUs for the specified product.
  - URL: https://docs.tcgplayer.com/reference/catalog_getskusbyproductid.md

- **List Related Products**: Returns other products that are commonly found in the same orders as the specified
  - URL: https://docs.tcgplayer.com/reference/catalog_getproductsalsopurchasedbyproductid-1.md

- **List All Product Media Types**: Returns all available media (e.g. images) associated with the specified product.
  - URL: https://docs.tcgplayer.com/reference/catalog_getproductmedia.md

- **Get SKU details**: This endpoint returns an array of SKUs whose Ids were specified in the skuIds
  - URL: https://docs.tcgplayer.com/reference/catalog_getskus.md

- **List Conditions**: This endpoint returns an array contain all of the normalized conditions
  - URL: https://docs.tcgplayer.com/reference/catalog_getconditions.md

- **Inventory**
  - URL: https://docs.tcgplayer.com/reference/inventory.md

- **Get ProductList By Id**: Returns the ProductList specified by using the ProductListId.
  - URL: https://docs.tcgplayer.com/reference/inventory_getproductlistbyid-1.md

- **Get ProductList By Key**: Returns the ProductList specified by using the ProductListKey.
  - URL: https://docs.tcgplayer.com/reference/inventory_getproductlistbykey-1.md

- **List All ProductLists**: This lists all the accessible ProductLists to the user identified in the bearer token making the API call.
  - URL: https://docs.tcgplayer.com/reference/inventory_getproductlist-1.md

- **Create ProductList**
  - URL: https://docs.tcgplayer.com/reference/inventory_createproductlist-1.md

- **Pricing**
  - URL: https://docs.tcgplayer.com/reference/pricing.md

- **Get Market Price by SKU**: Gets the current Market Price for the specified SKU.
  - URL: https://docs.tcgplayer.com/reference/pricing_getmarketpricebyproductconditionid-1.md

- **List Product Prices by Group**: Returns all product prices associated with the specified Group.
  - URL: https://docs.tcgplayer.com/reference/pricing_getgroupprices.md

- **List Product Market Prices**: Returns all product market prices for the Ids specified.  Market prices that could
  - URL: https://docs.tcgplayer.com/reference/pricing_getproductprices-1.md

- **List SKU Market Prices**: Returns all SKU market prices for the Ids specified.  Market prices that could
  - URL: https://docs.tcgplayer.com/reference/pricing_getproductconditionprices-1.md

- **List Product Buylist Prices**: Returns all product buylist prices for the Ids specified.  Buylist prices that could
  - URL: https://docs.tcgplayer.com/reference/pricing_getproductbuylistprices-1.md

- **List SKU Buylist Prices**: Returns all SKU buylist prices for the Ids specified.  Buylist prices that could
  - URL: https://docs.tcgplayer.com/reference/pricing_getproductconditionbuylistprices-1.md

- **List Product Buylist Prices by Group**: Returns all product buylist prices associated with the specified Group.
  - URL: https://docs.tcgplayer.com/reference/pricing_getgroupbuylistprices.md

- **Stores**
  - URL: https://docs.tcgplayer.com/reference/stores.md

- **Batch Update Store Buylist Prices**: Perform multiple buylist updates asynchronously in a batch.  The response will
  - URL: https://docs.tcgplayer.com/reference/stores_batchupdatestorebuylistprices.md

- **Create SKU Buylist**
  - URL: https://docs.tcgplayer.com/reference/stores_createstorebuylistsku-1.md

- **Update SKU Buylist Price**
  - URL: https://docs.tcgplayer.com/reference/stores_updatestorebuylistskuprice-1.md

- **Update SKU Buylist Quantity**
  - URL: https://docs.tcgplayer.com/reference/stores_updatestorebuylistskuquantity-1.md

- **Get Buylist Categories**
  - URL: https://docs.tcgplayer.com/reference/stores_getsellerbuylistcategories.md

- **Get Buylist Groups**
  - URL: https://docs.tcgplayer.com/reference/stores_getsellerbuylistsets.md

- **Get Store Buylist Settings**
  - URL: https://docs.tcgplayer.com/reference/stores_getsellerbuylistsettings.md

- **Get a Store's Buylist Products for Kiosk use.**
  - URL: https://docs.tcgplayer.com/reference/stores_getbuylistproducts.md

- **Get the Product Conditions for a Product on a Store's Buylist.**
  - URL: https://docs.tcgplayer.com/reference/stores_getbuylistproductconditions.md

- **Search Stores**: Returns a collection of storeKey values based on the search parameters.
  - URL: https://docs.tcgplayer.com/reference/stores_getstores-1.md

- **Get Free Shipping Option**: Gets the current Store's Free Shipping option (if exists) whose Seller is associated with the user's bearer token making this API call.
  - URL: https://docs.tcgplayer.com/reference/stores_freeshippingoptions-1.md

- **Get Store Address**: Return address information about the Store specified by the storeKey.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreaddress-1.md

- **Get Store Feedback**: Return feedback information about the Store specified by the storeKey.
  - URL: https://docs.tcgplayer.com/reference/stores_getstorefeedback-1.md

- **Set Store Status**: If a store's status is either Live or Hold - User Request then this action may be called to flip the store between the
  - URL: https://docs.tcgplayer.com/reference/stores_setstorestatus-1.md

- **Get Customer Summary**: Returns the total number of orders and total product dollar amount for all orders a customer has place with the seller.
  - URL: https://docs.tcgplayer.com/reference/stores_getstorecustomer-1.md

- **Search Store Customers**: Search Store Customers.
  - URL: https://docs.tcgplayer.com/reference/stores_getstorecustomers-1.md

- **Get Customer Addresses**: Returns the shipping addresses associated with the orders a customer has placed with the seller.
  - URL: https://docs.tcgplayer.com/reference/stores_getstorecustomeraddresses-1.md

- **Get Customer Orders**: Returns a list of orders containing the total product quantity and total product dollar amount for each order a customer has placed with the seller.
  - URL: https://docs.tcgplayer.com/reference/stores_getstorecustomerordersummary-1.md

- **Get Store Info**: Return general information about the current Store associated with the current bearer token.
  - URL: https://docs.tcgplayer.com/reference/stores_getidentity-1.md

- **Get Store Info**: Return general information about the stores specified by the store keys.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoresbystorekey-1.md

- **Get Product Inventory Quantities**: Get Product Inventory Quantities.
  - URL: https://docs.tcgplayer.com/reference/stores_getinventoryproductquantity-1.md

- **List Product Summary**: List Product Summary.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreinventory-1.md

- **List Product SKUs**
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreproductskus-1.md

- **List Related Products**: Related Products are other Products that are often purchased along with the specified Product.
  - URL: https://docs.tcgplayer.com/reference/stores_getrelatedproducts-1.md

- **List Shipping Options**
  - URL: https://docs.tcgplayer.com/reference/stores_shippingoptions-1.md

- **Get SKU Quantity**: Get SKU Quantity.
  - URL: https://docs.tcgplayer.com/reference/stores_getinventoryskuquantity-1.md

- **Increment SKU Inventory Quantity**: Increments the current store's inventory of this SKU from the current Store's inventory whose Seller is associated with the user's bearer token making this API call.
  - URL: https://docs.tcgplayer.com/reference/stores_updatestoreskuquantity-1.md

- **Update SKU inventory**: Adds or updates a SKU to the current Store's inventory whose Seller is associated with the user's bearer token making this API call.
  - URL: https://docs.tcgplayer.com/reference/stores_createstoresku-1.md

- **Batch Update Store Sku Prices**: Perform multiple price updates asynchronously in a batch.  The response will contain a single GUID to identify the batch.  All price updates
  - URL: https://docs.tcgplayer.com/reference/stores_batchupdatestoreskuprices-1.md

- **Update SKU Inventory Price**: Updates the current store's pricing of this SKU from the current Store's inventory whose Seller is associated with the user's bearer token making this API call.
  - URL: https://docs.tcgplayer.com/reference/stores_updatestoreskuprice-1.md

- **List SKU List Price**: This listing comes from the current Store's inventory whose Seller is associated with the user's bearer token making this API call.
  - URL: https://docs.tcgplayer.com/reference/stores_getinventoryskuprices-1.md

- **Get SKU List Price**: Get SKU List Price.
  - URL: https://docs.tcgplayer.com/reference/stores_getinventoryskuprice-1.md

- **List All Groups**: This listing comes from the current Store's inventory whose Seller is associated with the user's bearer token making this API call.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoregroups-1.md

- **List All Categories.**: List All Categories.
  - URL: https://docs.tcgplayer.com/reference/stores_getstorecategories.md

- **List Product Summary By Category**: List all products based on criteria
  - URL: https://docs.tcgplayer.com/reference/stores_productsearchbycategory.md

- **List Store Channels**: List All Channels for a Store.
  - URL: https://docs.tcgplayer.com/reference/stores_getstorechannels.md

- **List Top Sold Products**: This listing comes from the current Store's inventory whose Seller is associated with the user's bearer token making this API call.
  - URL: https://docs.tcgplayer.com/reference/stores_gettopsalesforseller-1.md

- **Search Top Sold Products**: This listing comes from the current Store's inventory whose Seller is associated with the user's bearer token making this API call.
  - URL: https://docs.tcgplayer.com/reference/stores_topsalessearch-1.md

- **List Catalog Objects**: SearchResults returned can include Product, Groups, and Categories.
  - URL: https://docs.tcgplayer.com/reference/stores_searchinventory-1.md

- **Search Custom Listings.**: Retrieves the custom listing by the criteria passed in the querystring.
  - URL: https://docs.tcgplayer.com/reference/stores_getcustomlisting.md

- **Get Order Manifest**: Get Order Manifest.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreordermanifest-1.md

- **Get Order Details**: Get Order Details.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreordersbyordernumber-1.md

- **Get Order Feedback**: Get Order Feedback.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreorderfeedback-1.md

- **Search Orders**: Search Orders.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreorders-1.md

- **Get Order Items**: Get Order Items.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreorderlineitems-1.md

- **Get Order Tracking Numbers**: Get Order Tracking Numbers.
  - URL: https://docs.tcgplayer.com/reference/stores_getstoreordertracking-1.md

- **Add Order Tracking Number**: Add Order Tracking Number.
  - URL: https://docs.tcgplayer.com/reference/stores_createstoreordertracking-1.md

## How to Use This Skill

Reference these resources when working with TCGplayer Documentation.