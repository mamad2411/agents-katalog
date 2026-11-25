---
name: cis-automotive-api
description: "CIS Automotive API skill. Use when working with CIS Automotive for getToken, makeSubUserKey, revokeSubUserKey. Covers 35 endpoints."
version: 1.0.0
generator: lapsh
---

# CIS Automotive API
API version: 1.0

## Auth
ApiKey apiKey in query

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /getToken -- verify access
3. POST /getToken -- create first getToken

## Endpoints

35 endpoints across 34 groups. See references/api-spec.lap for full details.

### getToken
| Method | Path | Description |
|--------|------|-------------|
| GET | /getToken | Get a JWT from your API credentials |
| POST | /getToken | Get a JWT from your API credentials |

### makeSubUserKey
| Method | Path | Description |
|--------|------|-------------|
| POST | /makeSubUserKey | Generate a Sub User Key that can be used by your users to make API calls in frontend applications. |

### revokeSubUserKey
| Method | Path | Description |
|--------|------|-------------|
| PUT | /revokeSubUserKey | Revoke a Sub User Key associated with your account. |

### getSubUserKeys
| Method | Path | Description |
|--------|------|-------------|
| GET | /getSubUserKeys | Get all Sub User Keys associated with your account. |

### getRegions
| Method | Path | Description |
|--------|------|-------------|
| GET | /getRegions | Get a list of region names |

### getBrands
| Method | Path | Description |
|--------|------|-------------|
| GET | /getBrands | Get a list of brand names |

### getModels
| Method | Path | Description |
|--------|------|-------------|
| GET | /getModels | Get a list of model names |

### getInactiveModels
| Method | Path | Description |
|--------|------|-------------|
| GET | /getInactiveModels | Get a list of model names including discontinued models |

### daysToSell
| Method | Path | Description |
|--------|------|-------------|
| GET | /daysToSell | Days a vehicle takes to sell |

### daysSupply
| Method | Path | Description |
|--------|------|-------------|
| GET | /daysSupply | Days worth of supply left on dealer lots |

### listPrice
| Method | Path | Description |
|--------|------|-------------|
| GET | /listPrice | Stats on ask price of new vehicles |

### salePrice
| Method | Path | Description |
|--------|------|-------------|
| GET | /salePrice | Stats on sale price of new vehicles |

### salePriceHistogram
| Method | Path | Description |
|--------|------|-------------|
| GET | /salePriceHistogram | Histogram of sales price of new vehicles by model |

### modelYearDist
| Method | Path | Description |
|--------|------|-------------|
| GET | /modelYearDist | Used market share of model year by model |

### topModels
| Method | Path | Description |
|--------|------|-------------|
| GET | /topModels | Top models in a given region |

### getRegionBrandMarketShare
| Method | Path | Description |
|--------|------|-------------|
| GET | /getRegionBrandMarketShare | Market share of a brand in region |

### getRegionMarketShare
| Method | Path | Description |
|--------|------|-------------|
| GET | /getRegionMarketShare | Market share of all brands in region |

### getDealers
| Method | Path | Description |
|--------|------|-------------|
| GET | /getDealers | Premium. Dealers in a zip code. |

### getDealersByRegion
| Method | Path | Description |
|--------|------|-------------|
| GET | /getDealersByRegion | Premium. Dealers in a region. |

### getDealersByID
| Method | Path | Description |
|--------|------|-------------|
| GET | /getDealersByID | Premium. Dealers by ID |

### regionSales
| Method | Path | Description |
|--------|------|-------------|
| GET | /regionSales | Premium. Brand sales by region and month |

### regionDailySales
| Method | Path | Description |
|--------|------|-------------|
| GET | /regionDailySales | Brand sales by region and Day |

### vehicleHistory
| Method | Path | Description |
|--------|------|-------------|
| GET | /vehicleHistory | Premium. Simple Vehicle History Report |

### similarSalePrice
| Method | Path | Description |
|--------|------|-------------|
| GET | /similarSalePrice | Premium. Simple Vehicle Market Report |

### valuation
| Method | Path | Description |
|--------|------|-------------|
| GET | /valuation | Premium. Simple Vehicle Market Report Over Arbitrary Locations and Vehicles. |

### vehicleSeen
| Method | Path | Description |
|--------|------|-------------|
| GET | /vehicleSeen | Checks if a VIN appeared on the market on or after a given date. |

### vinDecode
| Method | Path | Description |
|--------|------|-------------|
| GET | /vinDecode | Vin decoder and Recall Info |

### listings2
| Method | Path | Description |
|--------|------|-------------|
| GET | /listings2 | Flexible Listing Search |

### listings
| Method | Path | Description |
|--------|------|-------------|
| GET | /listings | Listings by Dealer ID |

### listingsByDate
| Method | Path | Description |
|--------|------|-------------|
| GET | /listingsByDate | Listings by Dealer ID and Date |

### listingsByRegion
| Method | Path | Description |
|--------|------|-------------|
| GET | /listingsByRegion | Listings by Region |

### listingsByRegionAndDate
| Method | Path | Description |
|--------|------|-------------|
| GET | /listingsByRegionAndDate | Listings by Region and Date |

### listingsByZipCode
| Method | Path | Description |
|--------|------|-------------|
| GET | /listingsByZipCode | Listings by ZipCode |

### listingsByZipCodeAndDate
| Method | Path | Description |
|--------|------|-------------|
| GET | /listingsByZipCodeAndDate | Listings by ZipCode and Date |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all getToken?" -> GET /getToken
- "Create a getToken?" -> POST /getToken
- "Create a makeSubUserKey?" -> POST /makeSubUserKey
- "List all getSubUserKeys?" -> GET /getSubUserKeys
- "List all getRegions?" -> GET /getRegions
- "List all getBrands?" -> GET /getBrands
- "List all getModels?" -> GET /getModels
- "List all getInactiveModels?" -> GET /getInactiveModels
- "List all daysToSell?" -> GET /daysToSell
- "List all daysSupply?" -> GET /daysSupply
- "List all listPrice?" -> GET /listPrice
- "List all salePrice?" -> GET /salePrice
- "List all salePriceHistogram?" -> GET /salePriceHistogram
- "List all modelYearDist?" -> GET /modelYearDist
- "List all topModels?" -> GET /topModels
- "List all getRegionBrandMarketShare?" -> GET /getRegionBrandMarketShare
- "List all getRegionMarketShare?" -> GET /getRegionMarketShare
- "List all getDealers?" -> GET /getDealers
- "List all getDealersByRegion?" -> GET /getDealersByRegion
- "List all getDealersByID?" -> GET /getDealersByID
- "List all regionSales?" -> GET /regionSales
- "List all regionDailySales?" -> GET /regionDailySales
- "List all vehicleHistory?" -> GET /vehicleHistory
- "List all similarSalePrice?" -> GET /similarSalePrice
- "List all valuation?" -> GET /valuation
- "List all vehicleSeen?" -> GET /vehicleSeen
- "List all vinDecode?" -> GET /vinDecode
- "List all listings2?" -> GET /listings2
- "List all listings?" -> GET /listings
- "List all listingsByDate?" -> GET /listingsByDate
- "List all listingsByRegion?" -> GET /listingsByRegion
- "List all listingsByRegionAndDate?" -> GET /listingsByRegionAndDate
- "List all listingsByZipCode?" -> GET /listingsByZipCode
- "List all listingsByZipCodeAndDate?" -> GET /listingsByZipCodeAndDate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
