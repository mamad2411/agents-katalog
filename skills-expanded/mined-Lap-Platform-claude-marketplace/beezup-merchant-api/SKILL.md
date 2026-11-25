---
name: beezup-merchant-api
description: "BeezUP Merchant API skill. Use when working with BeezUP Merchant for public, user, orders. Covers 249 endpoints."
version: 1.0.0
generator: lapsh
---

# BeezUP Merchant API
API version: 2.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.beezup.com

## Setup
1. Set your API key in the appropriate header
2. GET /v2/public/channels/ -- verify access
3. POST /v2/public/security/login -- create first login

## Endpoints

249 endpoints across 3 groups. See references/api-spec.lap for full details.

### public
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/public/security/login | Login |
| POST | /v2/public/security/login/mfa | Login |
| POST | /v2/public/security/register | User Registration |
| POST | /v2/public/security/lostpassword | Lost password |
| GET | /v2/public/channels/ | Get public channel index |
| GET | /v2/public/channels/{countryIsoCode} | The channel list for one country |
| GET | /v2/public/lov/ | Get all list names |
| GET | /v2/public/lov/{listName} | Get the list of values related to this list name |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/user/lov/ | Get all list names |
| GET | /v2/user/lov/{listName} | Get the list of values related to this list name |
| GET | /v2/user/customer/ | The index of all operations and LOV |
| GET | /v2/user/customer/account | Get user account information |
| POST | /v2/user/customer/account/resendEmailActivation | Resend email activation |
| POST | /v2/user/customer/account/activate | Activate the user account |
| PUT | /v2/user/customer/account/personalInfo | Save user personal information |
| PUT | /v2/user/customer/account/companyInfo | Change company information |
| GET | /v2/user/customer/account/profilePictureInfo | Get profile picture information |
| PUT | /v2/user/customer/account/profilePictureInfo | Change user picture information |
| GET | /v2/user/customer/account/creditCardInfo | Get credit card information |
| PUT | /v2/user/customer/account/creditCardInfo | Save user credit card info |
| POST | /v2/user/customer/account/changeEmail | Change user email |
| POST | /v2/user/customer/account/changePassword | Change user password |
| POST | /v2/user/customer/security/logout | Log out the current user from go2 |
| GET | /v2/user/customer/zendeskToken | Zendesk token |
| GET | /v2/user/customer/stores | Get store list |
| POST | /v2/user/customer/stores | Create a new store |
| GET | /v2/user/customer/stores/{storeId} | Get store's information |
| PATCH | /v2/user/customer/stores/{storeId} | Update some store's information. |
| DELETE | /v2/user/customer/stores/{storeId} | Delete a store |
| GET | /v2/user/customer/stores/{storeId}/rights | Get store's rights |
| GET | /v2/user/customer/stores/{storeId}/alerts | Get store's alerts |
| POST | /v2/user/customer/stores/{storeId}/alerts | Save store alerts |
| GET | /v2/user/customer/stores/{storeId}/shares | Get shares related to this store |
| POST | /v2/user/customer/stores/{storeId}/shares | Share a store to another user |
| DELETE | /v2/user/customer/stores/{storeId}/shares/{userId} | Delete a share of a store to another user |
| GET | /v2/user/customer/friends/{userId} | Get friend information |
| GET | /v2/user/customer/billingPeriods | Get billing periods conditions |
| GET | /v2/user/customer/offers | Get all standard offers |
| POST | /v2/user/customer/offers | Get offer pricing |
| GET | /v2/user/customer/contracts | Get contract list |
| POST | /v2/user/customer/contracts | Create a new contract |
| POST | /v2/user/customer/contracts/current/disableAutoRenewal | Schedule termination of your current contract at the end of the commitment. |
| POST | /v2/user/customer/contracts/current/reenableAutoRenewal | Reactivate your terminated contract. |
| DELETE | /v2/user/customer/contracts/next | Delete your next contract |
| GET | /v2/user/customer/invoices | Get all your invoices |
| GET | /v2/user/catalogs/ | Get the index of the catalog API |
| GET | /v2/user/catalogs/beezupColumns | Get the BeezUP columns |
| GET | /v2/user/catalogs/{storeId} | Get the index of the catalog API for this store |
| GET | /v2/user/catalogs/{storeId}/inputConfiguration | Get the last input configuration |
| GET | /v2/user/catalogs/{storeId}/catalogColumns | Get catalog column list |
| POST | /v2/user/catalogs/{storeId}/catalogColumns/{columnId}/rename | Change Catalog Column User Name |
| GET | /v2/user/catalogs/{storeId}/customColumns | Get custom column list |
| PUT | /v2/user/catalogs/{storeId}/customColumns/{columnId} | Create or replace a custom column |
| DELETE | /v2/user/catalogs/{storeId}/customColumns/{columnId} | Delete custom column |
| POST | /v2/user/catalogs/{storeId}/customColumns/{columnId}/rename | Change Custom Column User Name |
| GET | /v2/user/catalogs/{storeId}/customColumns/{columnId}/expression | Get the encrypted custom column expression |
| PUT | /v2/user/catalogs/{storeId}/customColumns/{columnId}/expression | Change custom column expression |
| POST | /v2/user/catalogs/{storeId}/customColumns/computeExpression | Compute the expression for this catalog. |
| GET | /v2/user/catalogs/{storeId}/categories | Get category list |
| POST | /v2/user/catalogs/{storeId}/products/list | Get product list |
| GET | /v2/user/catalogs/{storeId}/products/random | Get random product list |
| GET | /v2/user/catalogs/{storeId}/products/{productId} | Get product by ProductId |
| GET | /v2/user/catalogs/{storeId}/products | Get product by Sku |
| POST | /v2/user/catalogs/{storeId}/products/batches/{actionType} | Push product batches |
| GET | /v2/user/catalogs/{storeId}/importations/{batchId}/getReportUrl | Get Reporting By BatchId |
| GET | /v2/user/catalogs/{storeId}/beezUPColumns | Get the BeezUPColumns' Mapping of a Store |
| PATCH | /v2/user/catalogs/{storeId}/beezUPColumns | Patch the BeezUPColumns' Mapping of a Store. |
| PUT | /v2/user/catalogs/{storeId}/beezUPColumns | Replace the BeezUPColumns' Mapping of a Store. |
| PUT | /v2/user/catalogs/{storeId}/beezUPColumns/{beezUPColumnName} | Replace the BeezUPColumns' Mapping of a Store. |
| DELETE | /v2/user/catalogs/{storeId}/beezUPColumns/{beezUPColumnName} | Delete the BeezUPColumn' Mapping of a Store. |
| GET | /v2/user/catalogs/importations | Get the latest catalog importation reporting for all your stores |
| GET | /v2/user/catalogs/{storeId}/importations | Get the latest catalog importation reporting |
| POST | /v2/user/catalogs/{storeId}/importations/start | Start Manual Import |
| GET | /v2/user/catalogs/{storeId}/importations/{executionId} | Get the importation status |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/cancel | Cancel importation |
| GET | /v2/user/catalogs/{storeId}/importations/{executionId}/technicalProgression | Get technical progression |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/configureRemainingCatalogColumns | Configure remaining catalog columns |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/commitColumns | Commit columns |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/commit | Commit Importation |
| GET | /v2/user/catalogs/{storeId}/importations/{executionId}/productSamples/{productSampleIndex} | Get the product sample related to this importation with all columns (catalog and custom) |
| GET | /v2/user/catalogs/{storeId}/importations/{executionId}/productSamples/{productSampleIndex}/customColumns/{columnId} | Get product sample custom column value related to this importation. |
| GET | /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns | Get detected catalog columns during this importation. |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId} | Configure catalog column |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId}/ignore | Ignore Column |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId}/reattend | Reattend Column |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId}/map | Map catalog column to a BeezUP column |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId}/unmap | Unmap catalog column |
| GET | /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns | Get custom columns currently place in this importation |
| GET | /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId}/expression | Get the encrypted custom column expression in this importation |
| PUT | /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId} | Create or replace a custom column |
| DELETE | /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId} | Delete Custom Column |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId}/map | Map custom column to a BeezUP column |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId}/unmap | Unmap custom column |
| POST | /v2/user/catalogs/{storeId}/importations/{executionId}/products/list | Importation Get Products Report |
| GET | /v2/user/catalogs/{storeId}/importations/{executionId}/report | Importation Get Report |
| POST | /v2/user/catalogs/{storeId}/autoImport/activate | Activate the auto importation of the last successful manual catalog importation. |
| GET | /v2/user/catalogs/{storeId}/autoImport | Get the auto import configuration |
| DELETE | /v2/user/catalogs/{storeId}/autoImport | Delete Auto Import |
| POST | /v2/user/catalogs/{storeId}/autoImport/start | Start Auto Import Manually |
| POST | /v2/user/catalogs/{storeId}/autoImport/pause | Pause Auto Import |
| POST | /v2/user/catalogs/{storeId}/autoImport/resume | Resume Auto Import |
| POST | /v2/user/catalogs/{storeId}/autoImport/scheduling/interval | Configure Auto Import Interval |
| POST | /v2/user/catalogs/{storeId}/autoImport/scheduling/schedules | Configure Auto Import Schedules |
| GET | /v2/user/catalogs/{storeId}/replication/to | [PREVIEW] [Mocked] Get Store's Replicated To Configuration |
| PUT | /v2/user/catalogs/{storeId}/replication/to | [PREVIEW] [Mocked] Put Store's Replicated To Configuration |
| PATCH | /v2/user/catalogs/{storeId}/replication/to | [PREVIEW] [Mocked] Patch Store's Replicated To Configuration |
| GET | /v2/user/catalogs/{storeId}/replication/from | [PREVIEW] [Mocked] Get Store's Replicated From Configuration |
| GET | /v2/user/catalogs/{storeId}/replication/logs | [PREVIEW] [Mocked] Get Replication Logs - Can be filtered by ExecutionId |
| GET | /v2/user/channels/ | List all available channel for this store |
| GET | /v2/user/channels/{channelId} | Get channel information |
| GET | /v2/user/channels/{channelId}/categories | Get channel categories |
| POST | /v2/user/channels/{channelId}/columns | Get channel columns |
| GET | /v2/user/channelCatalogs/ | List all your current channel catalogs |
| POST | /v2/user/channelCatalogs/ | Add a new channel catalog |
| GET | /v2/user/channelCatalogs/{channelCatalogId} | Get the channel catalog information |
| DELETE | /v2/user/channelCatalogs/{channelCatalogId} | Delete the channel catalog |
| GET | /v2/user/channelCatalogs/filterOperators | Get channel catalog filter operators |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/enable | Enable a channel catalog |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/disable | Disable a channel catalog |
| PUT | /v2/user/channelCatalogs/{channelCatalogId}/settings/general | Configure channel catalog general settings |
| PUT | /v2/user/channelCatalogs/{channelCatalogId}/settings/cost | Configure channel catalog cost settings |
| PUT | /v2/user/channelCatalogs/{channelCatalogId}/columnMappings | Configure channel catalog column mappings |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/categories | Get channel catalog categories |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/categories/disableMapping | Disable a channel catalog category mapping |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/categories/reenableMapping | Reenable a channel catalog category mapping |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/categories/configure | Configure channel catalog category |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/exclusionFilters | Get channel catalog exclusion filters |
| PUT | /v2/user/channelCatalogs/{channelCatalogId}/exclusionFilters | Configure channel catalog exclusion filters |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/products | Get channel catalog product information list |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/products/export | Export channel catalog product information list |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/products/counters | Get channel catalog products' counters |
| POST | /v2/user/channelCatalogs/products | Get channel catalog products related to these channel catalogs |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/products/{productId} | Get channel catalog product information |
| PUT | /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/overrides | Override channel catalog product values |
| DELETE | /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/overrides/{channelColumnId} | Delete a specific channel catalog product value override |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/overrides/copy | Get channel catalog product value override compatibilities status |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/overrides/copy | Copy channel catalog product value override |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/disable | Disable channel catalog product |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/reenable | Reenable channel catalog product |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/exportations/cache | Get the exportation cache information |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/exportations/cache/clear | Clear the exportation cache |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/exportations/history | Get the exportation history |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/attributes | Get the Concerned Channel Catalog Attributes |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/attributes/counters | Get Attributes Value Mapping Counters |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/attributes/{channelAttributeId}/mapping | Get the Channel Catalog Attribute Value Mapping |
| POST | /v2/user/channelCatalogs/{channelCatalogId}/attributes/{channelAttributeId}/mapping | Set the Channel Catalog Attribute Value Mapping |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/replication/to | [PREVIEW] [Mocked] Get ChannelCatalog's Replicated To Configuration |
| PUT | /v2/user/channelCatalogs/{channelCatalogId}/replication/to | [PREVIEW] [Mocked] Put ChannelCatalog's Replicated To Configuration |
| PATCH | /v2/user/channelCatalogs/{channelCatalogId}/replication/to | [PREVIEW] [Mocked] Patch ChannelCatalog's Replicated To Configuration |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/replication/from | [PREVIEW] [Mocked] Get ChannelCatalog's Replicated From Configuration |
| GET | /v2/user/channelCatalogs/{channelCatalogId}/replication/logs | [PREVIEW] [Mocked] Get Replication Logs - Can be filtered by ExecutionId. |
| GET | /v2/user/marketplaces/channelcatalogs/ | Get your marketplace channel catalog list |
| POST | /v2/user/marketplaces/channelcatalogs/publications/{marketplaceTechnicalCode}/{accountId}/publish | Launch a publication of the catalog to the marketplace |
| GET | /v2/user/marketplaces/channelcatalogs/publications/{marketplaceTechnicalCode}/{accountId}/history | Fetch the publication history for an account, sorted by descending start date |
| GET | /v2/user/marketplaces/channelcatalogs/{channelCatalogId}/properties | Get the marketplace properties for a channel catalog |
| GET | /v2/user/marketplaces/channelcatalogs/{channelCatalogId}/settings | Get the marketplace settings for a channel catalog |
| POST | /v2/user/marketplaces/channelcatalogs/{channelCatalogId}/settings | Save new marketplace settings for a channel catalog |
| GET | /v2/user/marketplaces/orders/ | [DEPRECATED] Get all actions you can do on the order API |
| GET | /v2/user/marketplaces/orders/status | [DEPRECATED] Get current synchronization status between your marketplaces and BeezUP accounts |
| POST | /v2/user/marketplaces/orders/harvest | [DEPRECATED] Send harvest request to all your marketplaces |
| GET | /v2/user/marketplaces/orders/automaticTransitions | Get list of configured automatic Order status transitions |
| POST | /v2/user/marketplaces/orders/automaticTransitions | Configure new or existing automatic Order status transition |
| POST | /v2/user/marketplaces/orders/list/full | [DEPRECATED] Get a paginated list of all Orders with all Order and Order Item(s) properties |
| POST | /v2/user/marketplaces/orders/list/light | [DEPRECATED] Get a paginated list of all Orders without details |
| GET | /v2/user/marketplaces/orders/exportations | Get a paginated list of Order report exportations |
| POST | /v2/user/marketplaces/orders/exportations | Request a new Order report exportation to be generated |
| POST | /v2/user/marketplaces/orders/batches/setMerchantOrderInfos | [DEPRECATED] Send a batch of operations to set an Order's merchant information  (max 100 items per call) |
| POST | /v2/user/marketplaces/orders/batches/clearMerchantOrderInfos | [DEPRECATED] Send a batch of operations to clear an Order's merchant information (max 100 items per call) |
| POST | /v2/user/marketplaces/orders/batches/changeOrders/{changeOrderType} | [DEPRECATED] Send a batch of operations to change your marketplace Order information: accept, ship, etc.  (max 100 items per call) |
| HEAD | /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId} | [DEPRECATED] DEPRECATED - Get the meta information about the order (ETag, Last-Modified) |
| GET | /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId} | [DEPRECATED] DEPRECATED - Get full Order and Order Item(s) properties |
| GET | /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/history | [DEPRECATED] Get an Order's harvest and change history |
| POST | /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/harvest | [DEPRECATED] Send harvest request for a single Order |
| POST | /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/setMerchantOrderInfo | [DEPRECATED] Set an Order's merchant information |
| POST | /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/clearMerchantOrderInfo | [DEPRECATED] Clear an Order's merchant information |
| POST | /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/{changeOrderType} | [DEPRECATED] Change your marketplace Order Information (accept, ship, etc.) |
| GET | /v2/user/marketplaces/orders/subscriptions/ | Get the subscription list |
| POST | /v2/user/marketplaces/orders/subscriptions/{id} | Creates a subscription to the orders |
| GET | /v2/user/marketplaces/orders/subscriptions/{id} | Get a subscription to the orders |
| DELETE | /v2/user/marketplaces/orders/subscriptions/{id} | Delete a subscription to the orders |
| GET | /v2/user/marketplaces/orders/subscriptions/{id}/reporting | Get the push reporting related to this subscription |
| POST | /v2/user/marketplaces/orders/subscriptions/{id}/activate | Activate a subscription to the orders |
| POST | /v2/user/marketplaces/orders/subscriptions/{id}/deactivate | Deactivate a subscription to the orders |
| POST | /v2/user/marketplaces/orders/subscriptions/{id}/retry | Force retry push orders immediatly |
| GET | /v2/user/analytics/ | Get the Analytics API operation index |
| GET | /v2/user/analytics/{storeId} | Get the Analytics API operation index for one store |
| GET | /v2/user/analytics/tracking/status | Get the global synchronization status of clicks and orders |
| GET | /v2/user/analytics/{storeId}/tracking/status | Get the synchronization status of clicks and orders of a store |
| GET | /v2/user/analytics/{storeId}/tracking/clicks | Get the latest tracked clicks |
| GET | /v2/user/analytics/{storeId}/tracking/orders | Get the latest tracked orders |
| GET | /v2/user/analytics/{storeId}/tracking/externalorders | Get the latest tracked external orders |
| POST | /v2/user/analytics/reports/byday | Get the report by day for a StoreId |
| POST | /v2/user/analytics/{storeId}/reports/byday | Get the report by day for a StoreId |
| POST | /v2/user/analytics/{storeId}/reports/bychannel | Get the report by channel |
| POST | /v2/user/analytics/{storeId}/reports/bycategory | Get the report by category |
| POST | /v2/user/analytics/{storeId}/reports/byproduct | Get the report by product |
| POST | /v2/user/analytics/{storeId}/optimisations/all/{actionName} | Optimise all products |
| POST | /v2/user/analytics/{storeId}/optimisations/{actionName} | Optimise products by page |
| POST | /v2/user/analytics/{storeId}/optimisations/bychannel/{channelId}/{actionName} | Optimise products by channel |
| POST | /v2/user/analytics/{storeId}/optimisations/bycategory/{catalogCategoryId}/{actionName} | Optimise products by category |
| POST | /v2/user/analytics/{storeId}/optimisations/byproduct/{productId}/{actionName} | Optimise product |
| POST | /v2/user/analytics/{storeId}/optimisations/copy | Copy product optimisations between 2 channels |
| GET | /v2/user/analytics/{storeId}/reports/filters | Get report filter list for the given store |
| GET | /v2/user/analytics/{storeId}/reports/filters/{reportFilterId} | Get the report filter description |
| PUT | /v2/user/analytics/{storeId}/reports/filters/{reportFilterId} | Save the report filter |
| DELETE | /v2/user/analytics/{storeId}/reports/filters/{reportFilterId} | Delete the report filter |
| GET | /v2/user/analytics/{storeId}/rules | Gets the list of rules for a given store |
| POST | /v2/user/analytics/{storeId}/rules | Rule creation |
| GET | /v2/user/analytics/{storeId}/rules/{ruleId} | Gets the rule |
| PATCH | /v2/user/analytics/{storeId}/rules/{ruleId} | Update Rule |
| DELETE | /v2/user/analytics/{storeId}/rules/{ruleId} | Delete Rule |
| POST | /v2/user/analytics/{storeId}/rules/{ruleId}/moveup | Move the rule up |
| POST | /v2/user/analytics/{storeId}/rules/{ruleId}/movedown | Move the rule down |
| POST | /v2/user/analytics/{storeId}/rules/{ruleId}/enable | Enable rule |
| POST | /v2/user/analytics/{storeId}/rules/{ruleId}/disable | Disable rule |
| POST | /v2/user/analytics/{storeId}/rules/run | Run all rules for this store |
| POST | /v2/user/analytics/{storeId}/rules/{ruleId}/run | Run rule |
| GET | /v2/user/analytics/{storeId}/rules/executions | Get the rules execution history |
| GET | /v2/user/legacyTracking/channelCatalogs/ | List all your current channel catalogs configured to use legacy tracking format |
| GET | /v2/user/legacyTracking/channelCatalogs/{channelCatalogId} | Get the channel catalog configured to use legacy tracking format information |
| POST | /v2/user/legacyTracking/channelCatalogs/{channelCatalogId}/migrate | Migrate a channel catalog to current tracking format |
| PUT | /v2/user/marketplaces/orders/invoices/settings/general | Save Order Invoice general settings |
| GET | /v2/user/marketplaces/orders/invoices/settings/general | Get Order Invoice general settings |
| PUT | /v2/user/marketplaces/orders/invoices/settings/design | Save Order Invoice design settings |
| GET | /v2/user/marketplaces/orders/invoices/settings/design | Get Order Invoice design settings |
| POST | /v2/user/marketplaces/orders/invoices/settings/design/preview | View a preview an Order Invoice using custom design settings |
| POST | /v2/user/marketplaces/orders/invoices/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderUUID}/generate | Generate an Order Invoice |
| POST | /v2/user/marketplaces/orders/invoices/generate | Generate an Order Invoice batch |
| POST | /v2/user/marketplaces/orders/invoices/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderUUID}/preview | View a preview an Order Invoice |
| POST | /v2/user/marketplaces/orders/invoices/getPdfInvoice | Returns the PDF version of the invoice |

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders/v3//lov/orderManagementReadyMarketplaceBusinessCode | Get the list of MarketplaceBusinessCode ready for Order Management |
| GET | /orders/v3//status | Get current synchronization status between your marketplaces and BeezUP accounts |
| POST | /orders/v3//harvest | Send harvest request to all your marketplaces |
| POST | /orders/v3//list/full | Get a paginated list of all Orders with all Order and Order Item(s) properties |
| POST | /orders/v3//list/light | Get a paginated list of all Orders without details |
| HEAD | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId} | Get the meta information about the order (ETag, Last-Modified) |
| GET | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId} | Get full Order and Order Item(s) properties |
| POST | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/{changeOrderType} | Change your marketplace Order Information (accept, ship, etc.) |
| POST | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/closeIncident | Mark an order incident as resolved |
| GET | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/history | Get an Order's harvest and change history |
| POST | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/harvest | Send harvest request for a single Order |
| POST | /orders/v3//{marketplaceTechnicalCode}/{accountId}/harvest | Send harvest request for an Account |
| GET | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/history/{orderChangeExecutionUUID} | Get the order change reporting |
| POST | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/setMerchantOrderInfo | Set an Order's merchant information |
| POST | /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/clearMerchantOrderInfo | Clear an Order's merchant information |
| POST | /orders/v3//batches/setMerchantOrderInfos | Send a batch of operations to set an Order's merchant information  (max 100 items per call) |
| POST | /orders/v3//batches/clearMerchantOrderInfos | Send a batch of operations to clear an Order's merchant information (max 100 items per call) |
| POST | /orders/v3//batches/changeOrders/{changeOrderType} | Send a batch of operations to change your marketplace Order information: accept, ship, etc.  (max 100 items per call) |
| POST | /orders/v3//batches/changeOrders | Send a batch of operations to change your marketplace Order information: accept, ship, etc.  (max 100 items per call) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a login?" -> POST /v2/public/security/login
- "Create a mfa?" -> POST /v2/public/security/login/mfa
- "Create a register?" -> POST /v2/public/security/register
- "Create a lostpassword?" -> POST /v2/public/security/lostpassword
- "List all channels?" -> GET /v2/public/channels/
- "Get channel details?" -> GET /v2/public/channels/{countryIsoCode}
- "List all lov?" -> GET /v2/public/lov/
- "Get lov details?" -> GET /v2/public/lov/{listName}
- "List all lov?" -> GET /v2/user/lov/
- "Get lov details?" -> GET /v2/user/lov/{listName}
- "List all customer?" -> GET /v2/user/customer/
- "List all account?" -> GET /v2/user/customer/account
- "Create a resendEmailActivation?" -> POST /v2/user/customer/account/resendEmailActivation
- "Create a activate?" -> POST /v2/user/customer/account/activate
- "List all profilePictureInfo?" -> GET /v2/user/customer/account/profilePictureInfo
- "List all creditCardInfo?" -> GET /v2/user/customer/account/creditCardInfo
- "Create a changeEmail?" -> POST /v2/user/customer/account/changeEmail
- "Create a changePassword?" -> POST /v2/user/customer/account/changePassword
- "Create a logout?" -> POST /v2/user/customer/security/logout
- "List all zendeskToken?" -> GET /v2/user/customer/zendeskToken
- "List all stores?" -> GET /v2/user/customer/stores
- "Create a store?" -> POST /v2/user/customer/stores
- "Get store details?" -> GET /v2/user/customer/stores/{storeId}
- "Partially update a store?" -> PATCH /v2/user/customer/stores/{storeId}
- "Delete a store?" -> DELETE /v2/user/customer/stores/{storeId}
- "List all rights?" -> GET /v2/user/customer/stores/{storeId}/rights
- "List all alerts?" -> GET /v2/user/customer/stores/{storeId}/alerts
- "Create a alert?" -> POST /v2/user/customer/stores/{storeId}/alerts
- "List all shares?" -> GET /v2/user/customer/stores/{storeId}/shares
- "Create a share?" -> POST /v2/user/customer/stores/{storeId}/shares
- "Delete a share?" -> DELETE /v2/user/customer/stores/{storeId}/shares/{userId}
- "Get friend details?" -> GET /v2/user/customer/friends/{userId}
- "List all billingPeriods?" -> GET /v2/user/customer/billingPeriods
- "List all offers?" -> GET /v2/user/customer/offers
- "Create a offer?" -> POST /v2/user/customer/offers
- "List all contracts?" -> GET /v2/user/customer/contracts
- "Create a contract?" -> POST /v2/user/customer/contracts
- "Create a disableAutoRenewal?" -> POST /v2/user/customer/contracts/current/disableAutoRenewal
- "Create a reenableAutoRenewal?" -> POST /v2/user/customer/contracts/current/reenableAutoRenewal
- "List all invoices?" -> GET /v2/user/customer/invoices
- "List all catalogs?" -> GET /v2/user/catalogs/
- "List all beezupColumns?" -> GET /v2/user/catalogs/beezupColumns
- "Get catalog details?" -> GET /v2/user/catalogs/{storeId}
- "List all inputConfiguration?" -> GET /v2/user/catalogs/{storeId}/inputConfiguration
- "List all catalogColumns?" -> GET /v2/user/catalogs/{storeId}/catalogColumns
- "Create a rename?" -> POST /v2/user/catalogs/{storeId}/catalogColumns/{columnId}/rename
- "List all customColumns?" -> GET /v2/user/catalogs/{storeId}/customColumns
- "Update a customColumn?" -> PUT /v2/user/catalogs/{storeId}/customColumns/{columnId}
- "Delete a customColumn?" -> DELETE /v2/user/catalogs/{storeId}/customColumns/{columnId}
- "Create a rename?" -> POST /v2/user/catalogs/{storeId}/customColumns/{columnId}/rename
- "List all expression?" -> GET /v2/user/catalogs/{storeId}/customColumns/{columnId}/expression
- "Create a computeExpression?" -> POST /v2/user/catalogs/{storeId}/customColumns/computeExpression
- "List all categories?" -> GET /v2/user/catalogs/{storeId}/categories
- "Create a list?" -> POST /v2/user/catalogs/{storeId}/products/list
- "List all random?" -> GET /v2/user/catalogs/{storeId}/products/random
- "Get product details?" -> GET /v2/user/catalogs/{storeId}/products/{productId}
- "List all products?" -> GET /v2/user/catalogs/{storeId}/products
- "List all getReportUrl?" -> GET /v2/user/catalogs/{storeId}/importations/{batchId}/getReportUrl
- "List all beezUPColumns?" -> GET /v2/user/catalogs/{storeId}/beezUPColumns
- "Update a beezUPColumn?" -> PUT /v2/user/catalogs/{storeId}/beezUPColumns/{beezUPColumnName}
- "Delete a beezUPColumn?" -> DELETE /v2/user/catalogs/{storeId}/beezUPColumns/{beezUPColumnName}
- "List all importations?" -> GET /v2/user/catalogs/importations
- "List all importations?" -> GET /v2/user/catalogs/{storeId}/importations
- "Create a start?" -> POST /v2/user/catalogs/{storeId}/importations/start
- "Get importation details?" -> GET /v2/user/catalogs/{storeId}/importations/{executionId}
- "Create a cancel?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/cancel
- "List all technicalProgression?" -> GET /v2/user/catalogs/{storeId}/importations/{executionId}/technicalProgression
- "Create a configureRemainingCatalogColumn?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/configureRemainingCatalogColumns
- "Create a commitColumn?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/commitColumns
- "Create a commit?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/commit
- "Get productSample details?" -> GET /v2/user/catalogs/{storeId}/importations/{executionId}/productSamples/{productSampleIndex}
- "Get customColumn details?" -> GET /v2/user/catalogs/{storeId}/importations/{executionId}/productSamples/{productSampleIndex}/customColumns/{columnId}
- "List all catalogColumns?" -> GET /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns
- "Create a ignore?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId}/ignore
- "Create a reattend?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId}/reattend
- "Create a map?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId}/map
- "Create a unmap?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/catalogColumns/{columnId}/unmap
- "List all customColumns?" -> GET /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns
- "List all expression?" -> GET /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId}/expression
- "Update a customColumn?" -> PUT /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId}
- "Delete a customColumn?" -> DELETE /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId}
- "Create a map?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId}/map
- "Create a unmap?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/customColumns/{columnId}/unmap
- "Create a list?" -> POST /v2/user/catalogs/{storeId}/importations/{executionId}/products/list
- "List all report?" -> GET /v2/user/catalogs/{storeId}/importations/{executionId}/report
- "Create a activate?" -> POST /v2/user/catalogs/{storeId}/autoImport/activate
- "List all autoImport?" -> GET /v2/user/catalogs/{storeId}/autoImport
- "Create a start?" -> POST /v2/user/catalogs/{storeId}/autoImport/start
- "Create a pause?" -> POST /v2/user/catalogs/{storeId}/autoImport/pause
- "Create a resume?" -> POST /v2/user/catalogs/{storeId}/autoImport/resume
- "Create a interval?" -> POST /v2/user/catalogs/{storeId}/autoImport/scheduling/interval
- "Create a schedule?" -> POST /v2/user/catalogs/{storeId}/autoImport/scheduling/schedules
- "List all to?" -> GET /v2/user/catalogs/{storeId}/replication/to
- "List all from?" -> GET /v2/user/catalogs/{storeId}/replication/from
- "List all logs?" -> GET /v2/user/catalogs/{storeId}/replication/logs
- "List all channels?" -> GET /v2/user/channels/
- "Get channel details?" -> GET /v2/user/channels/{channelId}
- "List all categories?" -> GET /v2/user/channels/{channelId}/categories
- "Create a column?" -> POST /v2/user/channels/{channelId}/columns
- "List all channelCatalogs?" -> GET /v2/user/channelCatalogs/
- "Create a channelCatalog?" -> POST /v2/user/channelCatalogs/
- "Get channelCatalog details?" -> GET /v2/user/channelCatalogs/{channelCatalogId}
- "Delete a channelCatalog?" -> DELETE /v2/user/channelCatalogs/{channelCatalogId}
- "List all filterOperators?" -> GET /v2/user/channelCatalogs/filterOperators
- "Create a enable?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/enable
- "Create a disable?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/disable
- "List all categories?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/categories
- "Create a disableMapping?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/categories/disableMapping
- "Create a reenableMapping?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/categories/reenableMapping
- "Create a configure?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/categories/configure
- "List all exclusionFilters?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/exclusionFilters
- "Create a product?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/products
- "Create a export?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/products/export
- "List all counters?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/products/counters
- "Create a product?" -> POST /v2/user/channelCatalogs/products
- "Get product details?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}
- "Delete a override?" -> DELETE /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/overrides/{channelColumnId}
- "List all copy?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/overrides/copy
- "Create a copy?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/overrides/copy
- "Create a disable?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/disable
- "Create a reenable?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/products/{productId}/reenable
- "List all cache?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/exportations/cache
- "Create a clear?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/exportations/cache/clear
- "List all history?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/exportations/history
- "List all attributes?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/attributes
- "List all counters?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/attributes/counters
- "List all mapping?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/attributes/{channelAttributeId}/mapping
- "Create a mapping?" -> POST /v2/user/channelCatalogs/{channelCatalogId}/attributes/{channelAttributeId}/mapping
- "List all to?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/replication/to
- "List all from?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/replication/from
- "List all logs?" -> GET /v2/user/channelCatalogs/{channelCatalogId}/replication/logs
- "List all channelcatalogs?" -> GET /v2/user/marketplaces/channelcatalogs/
- "Create a publish?" -> POST /v2/user/marketplaces/channelcatalogs/publications/{marketplaceTechnicalCode}/{accountId}/publish
- "List all history?" -> GET /v2/user/marketplaces/channelcatalogs/publications/{marketplaceTechnicalCode}/{accountId}/history
- "List all properties?" -> GET /v2/user/marketplaces/channelcatalogs/{channelCatalogId}/properties
- "List all settings?" -> GET /v2/user/marketplaces/channelcatalogs/{channelCatalogId}/settings
- "Create a setting?" -> POST /v2/user/marketplaces/channelcatalogs/{channelCatalogId}/settings
- "List all orders?" -> GET /v2/user/marketplaces/orders/
- "List all status?" -> GET /v2/user/marketplaces/orders/status
- "Create a harvest?" -> POST /v2/user/marketplaces/orders/harvest
- "List all automaticTransitions?" -> GET /v2/user/marketplaces/orders/automaticTransitions
- "Create a automaticTransition?" -> POST /v2/user/marketplaces/orders/automaticTransitions
- "Create a full?" -> POST /v2/user/marketplaces/orders/list/full
- "Create a light?" -> POST /v2/user/marketplaces/orders/list/light
- "List all exportations?" -> GET /v2/user/marketplaces/orders/exportations
- "Create a exportation?" -> POST /v2/user/marketplaces/orders/exportations
- "Create a setMerchantOrderInfo?" -> POST /v2/user/marketplaces/orders/batches/setMerchantOrderInfos
- "Create a clearMerchantOrderInfo?" -> POST /v2/user/marketplaces/orders/batches/clearMerchantOrderInfos
- "Get order details?" -> GET /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}
- "List all history?" -> GET /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/history
- "Create a harvest?" -> POST /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/harvest
- "Create a setMerchantOrderInfo?" -> POST /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/setMerchantOrderInfo
- "Create a clearMerchantOrderInfo?" -> POST /v2/user/marketplaces/orders/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/clearMerchantOrderInfo
- "List all orderManagementReadyMarketplaceBusinessCode?" -> GET /orders/v3//lov/orderManagementReadyMarketplaceBusinessCode
- "List all status?" -> GET /orders/v3//status
- "Create a harvest?" -> POST /orders/v3//harvest
- "Create a full?" -> POST /orders/v3//list/full
- "Create a light?" -> POST /orders/v3//list/light
- "Get order details?" -> GET /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}
- "Create a closeIncident?" -> POST /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/closeIncident
- "List all history?" -> GET /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/history
- "Create a harvest?" -> POST /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/harvest
- "Create a harvest?" -> POST /orders/v3//{marketplaceTechnicalCode}/{accountId}/harvest
- "Get history details?" -> GET /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/history/{orderChangeExecutionUUID}
- "Create a setMerchantOrderInfo?" -> POST /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/setMerchantOrderInfo
- "Create a clearMerchantOrderInfo?" -> POST /orders/v3//{marketplaceTechnicalCode}/{accountId}/{beezUPOrderId}/clearMerchantOrderInfo
- "Create a setMerchantOrderInfo?" -> POST /orders/v3//batches/setMerchantOrderInfos
- "Create a clearMerchantOrderInfo?" -> POST /orders/v3//batches/clearMerchantOrderInfos
- "Create a changeOrder?" -> POST /orders/v3//batches/changeOrders
- "List all subscriptions?" -> GET /v2/user/marketplaces/orders/subscriptions/
- "Get subscription details?" -> GET /v2/user/marketplaces/orders/subscriptions/{id}
- "Delete a subscription?" -> DELETE /v2/user/marketplaces/orders/subscriptions/{id}
- "List all reporting?" -> GET /v2/user/marketplaces/orders/subscriptions/{id}/reporting
- "Create a activate?" -> POST /v2/user/marketplaces/orders/subscriptions/{id}/activate
- "Create a deactivate?" -> POST /v2/user/marketplaces/orders/subscriptions/{id}/deactivate
- "Create a retry?" -> POST /v2/user/marketplaces/orders/subscriptions/{id}/retry
- "List all analytics?" -> GET /v2/user/analytics/
- "Get analytic details?" -> GET /v2/user/analytics/{storeId}
- "List all status?" -> GET /v2/user/analytics/tracking/status
- "List all status?" -> GET /v2/user/analytics/{storeId}/tracking/status
- "List all clicks?" -> GET /v2/user/analytics/{storeId}/tracking/clicks
- "List all orders?" -> GET /v2/user/analytics/{storeId}/tracking/orders
- "List all externalorders?" -> GET /v2/user/analytics/{storeId}/tracking/externalorders
- "Create a byday?" -> POST /v2/user/analytics/reports/byday
- "Create a byday?" -> POST /v2/user/analytics/{storeId}/reports/byday
- "Create a bychannel?" -> POST /v2/user/analytics/{storeId}/reports/bychannel
- "Create a bycategory?" -> POST /v2/user/analytics/{storeId}/reports/bycategory
- "Create a byproduct?" -> POST /v2/user/analytics/{storeId}/reports/byproduct
- "Create a copy?" -> POST /v2/user/analytics/{storeId}/optimisations/copy
- "List all filters?" -> GET /v2/user/analytics/{storeId}/reports/filters
- "Get filter details?" -> GET /v2/user/analytics/{storeId}/reports/filters/{reportFilterId}
- "Update a filter?" -> PUT /v2/user/analytics/{storeId}/reports/filters/{reportFilterId}
- "Delete a filter?" -> DELETE /v2/user/analytics/{storeId}/reports/filters/{reportFilterId}
- "List all rules?" -> GET /v2/user/analytics/{storeId}/rules
- "Create a rule?" -> POST /v2/user/analytics/{storeId}/rules
- "Get rule details?" -> GET /v2/user/analytics/{storeId}/rules/{ruleId}
- "Partially update a rule?" -> PATCH /v2/user/analytics/{storeId}/rules/{ruleId}
- "Delete a rule?" -> DELETE /v2/user/analytics/{storeId}/rules/{ruleId}
- "Create a moveup?" -> POST /v2/user/analytics/{storeId}/rules/{ruleId}/moveup
- "Create a movedown?" -> POST /v2/user/analytics/{storeId}/rules/{ruleId}/movedown
- "Create a enable?" -> POST /v2/user/analytics/{storeId}/rules/{ruleId}/enable
- "Create a disable?" -> POST /v2/user/analytics/{storeId}/rules/{ruleId}/disable
- "Create a run?" -> POST /v2/user/analytics/{storeId}/rules/run
- "Create a run?" -> POST /v2/user/analytics/{storeId}/rules/{ruleId}/run
- "List all executions?" -> GET /v2/user/analytics/{storeId}/rules/executions
- "List all channelCatalogs?" -> GET /v2/user/legacyTracking/channelCatalogs/
- "Get channelCatalog details?" -> GET /v2/user/legacyTracking/channelCatalogs/{channelCatalogId}
- "Create a migrate?" -> POST /v2/user/legacyTracking/channelCatalogs/{channelCatalogId}/migrate
- "List all general?" -> GET /v2/user/marketplaces/orders/invoices/settings/general
- "List all design?" -> GET /v2/user/marketplaces/orders/invoices/settings/design
- "Create a preview?" -> POST /v2/user/marketplaces/orders/invoices/settings/design/preview
- "Create a generate?" -> POST /v2/user/marketplaces/orders/invoices/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderUUID}/generate
- "Create a generate?" -> POST /v2/user/marketplaces/orders/invoices/generate
- "Create a preview?" -> POST /v2/user/marketplaces/orders/invoices/{marketplaceTechnicalCode}/{accountId}/{beezUPOrderUUID}/preview
- "Create a getPdfInvoice?" -> POST /v2/user/marketplaces/orders/invoices/getPdfInvoice
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
