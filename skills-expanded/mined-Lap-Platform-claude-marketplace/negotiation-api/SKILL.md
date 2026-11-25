---
name: negotiation-api
description: "Negotiation API skill. Use when working with Negotiation for find_eligible_items, send_offer_to_interested_buyers. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Negotiation API
API version: v1.1.0

## Auth
OAuth2

## Base URL
https://api.ebay.com/sell/negotiation/v1

## Setup
1. Configure auth: OAuth2
2. GET /find_eligible_items -- verify access
3. POST /send_offer_to_interested_buyers -- create first send_offer_to_interested_buyers

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### find_eligible_items
| Method | Path | Description |
|--------|------|-------------|
| GET | /find_eligible_items | This method evaluates a seller's current listings and returns the set of IDs that are eligible for a seller-initiated discount offer to a buyer.  <br><br>A listing ID is returned only when one or more buyers have shown an "interest" in the listing.  <br><br>If any buyers have shown interest in a listing, the seller can initiate a "negotiation" with them by calling <a href="/api-docs/sell/negotiation/resources/offer/methods/sendOfferToInterestedBuyers">sendOfferToInterestedBuyers</a>, which sends all interested buyers a message that offers the listing at a discount.  <br><br>For details about how to create seller offers to buyers, see <a href="/api-docs/sell/static/marketing/offers-to-buyers.html" title="Selling Integration Guide">Sending offers to buyers</a>. |

### send_offer_to_interested_buyers
| Method | Path | Description |
|--------|------|-------------|
| POST | /send_offer_to_interested_buyers | This method sends eligible buyers offers to purchase items in a listing at a discount.  <br><br>When a buyer has shown <i>interest</i> in a listing, they become "eligible" to receive a seller-initiated offer to purchase the item(s).  <br><br>Sellers use <a href="/api-docs/sell/negotiation/resources/offer/methods/findEligibleItems">findEligibleItems</a> to get the set of listings that have interested buyers. If a listing has interested buyers, sellers can use this method (<b>sendOfferToInterestedBuyers</b>) to send an offer to the buyers who are interested in the listing. The offer gives buyers the ability to purchase the associated listings at a discounted price.  <br><br>For details about how to create seller offers to buyers, see <a href="/api-docs/sell/static/marketing/offers-to-buyers.html" title="Selling Integration Guide">Sending offers to buyers</a>. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all find_eligible_items?" -> GET /find_eligible_items
- "Create a send_offer_to_interested_buyer?" -> POST /send_offer_to_interested_buyers
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
