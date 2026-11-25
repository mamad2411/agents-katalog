---
name: consumptionmanagementclient
description: "ConsumptionManagementClient API skill. Use when working with ConsumptionManagementClient for {scope}, providers, subscriptions. Covers 25 endpoints."
version: 1.0.0
generator: lapsh
---

# ConsumptionManagementClient
API version: 2019-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Consumption/operations -- verify access

## Endpoints

25 endpoints across 3 groups. See references/api-spec.lap for full details.

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.Consumption/usageDetails | Lists the usage details for the defined scope. Usage details are available via this API only for May 1, 2014 or later. |
| GET | /{scope}/providers/Microsoft.Consumption/marketplaces | Lists the marketplaces for a scope at the defined scope. Marketplaces are available via this API only for May 1, 2014 or later. |
| GET | /{scope}/providers/Microsoft.Consumption/budgets | Lists all budgets for the defined scope. |
| GET | /{scope}/providers/Microsoft.Consumption/budgets/{budgetName} | Gets the budget for the scope by budget name. |
| PUT | /{scope}/providers/Microsoft.Consumption/budgets/{budgetName} | The operation to create or update a budget. Update operation requires latest eTag to be set in the request mandatorily. You may obtain the latest eTag by performing a get operation. Create operation does not require eTag. |
| DELETE | /{scope}/providers/Microsoft.Consumption/budgets/{budgetName} | The operation to delete a budget. |
| GET | /{scope}/providers/Microsoft.Consumption/tags | Get all available tag keys for the defined scope |
| GET | /{scope}/providers/Microsoft.Consumption/charges | Lists the charges based for the defined scope. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Consumption/balances | Gets the balances for a scope by billingAccountId. Balances are available via this API only for May 1, 2014 or later. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Billing/billingPeriods/{billingPeriodName}/providers/Microsoft.Consumption/balances | Gets the balances for a scope by billing period and billingAccountId. Balances are available via this API only for May 1, 2014 or later. |
| GET | /providers/Microsoft.Capacity/reservationorders/{reservationOrderId}/providers/Microsoft.Consumption/reservationSummaries | Lists the reservations summaries for daily or monthly grain. |
| GET | /providers/Microsoft.Capacity/reservationorders/{reservationOrderId}/reservations/{reservationId}/providers/Microsoft.Consumption/reservationSummaries | Lists the reservations summaries for daily or monthly grain. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Consumption/reservationSummaries | Lists the reservations summaries for daily or monthly grain. |
| GET | /providers/Microsoft.Capacity/reservationorders/{reservationOrderId}/providers/Microsoft.Consumption/reservationDetails | Lists the reservations details for provided date range. |
| GET | /providers/Microsoft.Capacity/reservationorders/{reservationOrderId}/reservations/{reservationId}/providers/Microsoft.Consumption/reservationDetails | Lists the reservations details for provided date range. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Consumption/reservationDetails | Lists the reservations details for provided date range. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/microsoft.consumption/ReservationRecommendations | List of recommendations for purchasing reserved instances on billing account scope |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Consumption/reservationTransactions | List of transactions for reserved instances on billing account scope |
| GET | /providers/Microsoft.Consumption/operations | Lists all of the available consumption REST API operations. |
| GET | /providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Consumption/aggregatedcost | Provides the aggregate cost of a management group and all child management groups by current billing period. |
| GET | /providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Billing/billingPeriods/{billingPeriodName}/Microsoft.Consumption/aggregatedcost | Provides the aggregate cost of a management group and all child management groups by specified billing period |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Consumption/reservationRecommendations | List of recommendations for purchasing reserved instances. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Consumption/pricesheets/default | Gets the price sheet for a scope by subscriptionId. Price sheet is available via this API only for May 1, 2014 or later. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Billing/billingPeriods/{billingPeriodName}/providers/Microsoft.Consumption/pricesheets/default | Get the price sheet for a scope by subscriptionId and billing period. Price sheet is available via this API only for May 1, 2014 or later. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Consumption/forecasts | Lists the forecast charges by subscriptionId. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all usageDetails?" -> GET /{scope}/providers/Microsoft.Consumption/usageDetails
- "List all marketplaces?" -> GET /{scope}/providers/Microsoft.Consumption/marketplaces
- "List all budgets?" -> GET /{scope}/providers/Microsoft.Consumption/budgets
- "Get budget details?" -> GET /{scope}/providers/Microsoft.Consumption/budgets/{budgetName}
- "Update a budget?" -> PUT /{scope}/providers/Microsoft.Consumption/budgets/{budgetName}
- "Delete a budget?" -> DELETE /{scope}/providers/Microsoft.Consumption/budgets/{budgetName}
- "List all tags?" -> GET /{scope}/providers/Microsoft.Consumption/tags
- "List all charges?" -> GET /{scope}/providers/Microsoft.Consumption/charges
- "List all balances?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Consumption/balances
- "List all balances?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Billing/billingPeriods/{billingPeriodName}/providers/Microsoft.Consumption/balances
- "List all reservationSummaries?" -> GET /providers/Microsoft.Capacity/reservationorders/{reservationOrderId}/providers/Microsoft.Consumption/reservationSummaries
- "List all reservationSummaries?" -> GET /providers/Microsoft.Capacity/reservationorders/{reservationOrderId}/reservations/{reservationId}/providers/Microsoft.Consumption/reservationSummaries
- "List all reservationSummaries?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Consumption/reservationSummaries
- "List all reservationDetails?" -> GET /providers/Microsoft.Capacity/reservationorders/{reservationOrderId}/providers/Microsoft.Consumption/reservationDetails
- "List all reservationDetails?" -> GET /providers/Microsoft.Capacity/reservationorders/{reservationOrderId}/reservations/{reservationId}/providers/Microsoft.Consumption/reservationDetails
- "List all reservationDetails?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Consumption/reservationDetails
- "List all reservationRecommendations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Consumption/reservationRecommendations
- "List all ReservationRecommendations?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/microsoft.consumption/ReservationRecommendations
- "List all reservationTransactions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.Consumption/reservationTransactions
- "List all default?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Consumption/pricesheets/default
- "List all default?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Billing/billingPeriods/{billingPeriodName}/providers/Microsoft.Consumption/pricesheets/default
- "List all forecasts?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Consumption/forecasts
- "List all operations?" -> GET /providers/Microsoft.Consumption/operations
- "List all aggregatedcost?" -> GET /providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Consumption/aggregatedcost
- "List all aggregatedcost?" -> GET /providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Billing/billingPeriods/{billingPeriodName}/Microsoft.Consumption/aggregatedcost
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
