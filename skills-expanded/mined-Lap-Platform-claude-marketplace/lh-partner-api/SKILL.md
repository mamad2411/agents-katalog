---
name: lh-partner-api
description: "LH Partner API skill. Use when working with LH Partner for promotions, references, orders. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# LH Partner API
API version: 1.0

## Auth
OAuth2

## Base URL
https://api.lufthansa.com/v1

## Setup
1. Configure auth: OAuth2
2. GET /offers/fares/fares -- verify access

## Endpoints

16 endpoints across 6 groups. See references/api-spec.lap for full details.

### promotions
| Method | Path | Description |
|--------|------|-------------|
| GET | /promotions/priceoffers/flights/ond/{origin}/{destination} | Price Offers |

### references
| Method | Path | Description |
|--------|------|-------------|
| GET | /references/seatdetails/{aircraftCode}/{cabinCode} | Seat Details |

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders/orders/{orderID}/{name} | Orders |

### preflight
| Method | Path | Description |
|--------|------|-------------|
| PUT | /preflight/autocheckin/{ticketnumber} | Auto Check-In |

### baggage
| Method | Path | Description |
|--------|------|-------------|
| GET | /baggage/baggagetripandcontact/{searchID} | Baggage Trip and Contact |

### offers
| Method | Path | Description |
|--------|------|-------------|
| GET | /offers/fares/fares | Fares |
| GET | /offers/fares/allfares | All Fares |
| GET | /offers/fares/lowestfares | Lowest Fares |
| GET | /offers/fares/bestfares | Best Fares |
| GET | /offers/fares/subscriptions | Fares Subscriptions |
| GET | /offers/fares/deeplink/ffp | LH Deep Links - FFP |
| GET | /offers/fares/deeplink/itco | LH Deep Links - ITCO |
| GET | /offers/fares/deeplink | Deep Links |
| GET | /offers/ond/route/{origin}/{destination} | OND Route |
| GET | /offers/ond/top | Top OND |
| GET | /offers/ond/status | OND Status |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get ond details?" -> GET /promotions/priceoffers/flights/ond/{origin}/{destination}
- "Get seatdetail details?" -> GET /references/seatdetails/{aircraftCode}/{cabinCode}
- "Get order details?" -> GET /orders/orders/{orderID}/{name}
- "Update a autocheckin?" -> PUT /preflight/autocheckin/{ticketnumber}
- "Get baggagetripandcontact details?" -> GET /baggage/baggagetripandcontact/{searchID}
- "List all fares?" -> GET /offers/fares/fares
- "List all allfares?" -> GET /offers/fares/allfares
- "List all lowestfares?" -> GET /offers/fares/lowestfares
- "List all bestfares?" -> GET /offers/fares/bestfares
- "List all subscriptions?" -> GET /offers/fares/subscriptions
- "List all ffp?" -> GET /offers/fares/deeplink/ffp
- "List all itco?" -> GET /offers/fares/deeplink/itco
- "List all deeplink?" -> GET /offers/fares/deeplink
- "Get route details?" -> GET /offers/ond/route/{origin}/{destination}
- "List all top?" -> GET /offers/ond/top
- "List all status?" -> GET /offers/ond/status
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
