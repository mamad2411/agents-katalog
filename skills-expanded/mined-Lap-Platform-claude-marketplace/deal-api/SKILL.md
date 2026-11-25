---
name: deal-api
description: "Deal API skill. Use when working with Deal for deal_item, event, event_item. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Deal API
API version: v1.3.0

## Auth
OAuth2

## Base URL
https://api.ebay.com/buy/deal/v1

## Setup
1. Configure auth: OAuth2
2. GET /deal_item -- verify access

## Endpoints

4 endpoints across 3 groups. See references/api-spec.lap for full details.

### deal_item
| Method | Path | Description |
|--------|------|-------------|
| GET | /deal_item | This method retrieves a paginated set of deal items. The result set contains all deal items associated with the specified search criteria and marketplace ID.<h3>Restrictions</h3>This method can return a maximum of 10,000 items. For a list of supported sites and other restrictions, see <a href="/api-docs/buy/browse/overview.html#API" target="_blank">API Restrictions</a>.<br><br><span class="tablenote"><b>eBay Partner Network: </b> In order to receive a commission for your sales, you must use the URL returned in the <code>itemAffiliateWebUrl</code> field to forward your buyer to the ebay.com site.</span> |

### event
| Method | Path | Description |
|--------|------|-------------|
| GET | /event/{event_id} | This method retrieves the details for an eBay event. The result set contains detailed information associated with the specified event ID, such as applicable coupons, start and end dates, and event terms.<h3><b>Restrictions </b></h3>This method can return a maximum of 10,000 items. For a list of supported sites and other restrictions, see <a href="/api-docs/buy/browse/overview.html#API" target="_blank">API Restrictions</a>.<br><br><span class="tablenote"><b>eBay Partner Network: </b> In order to receive a commission for your sales, you must use the URL returned in the <code>itemAffiliateWebUrl</code> field to forward your buyer to the ebay.com site. </span> |
| GET | /event | This method returns paginated results containing all eBay events for the specified marketplace.<h3><b>Restrictions </b></h3>This method can return a maximum of 10,000 items. For a list of supported sites and other restrictions, see <a href="/api-docs/buy/browse/overview.html#API" target="_blank ">API Restrictions</a>.<br><br><span class="tablenote"><b>eBay Partner Network: </b> In order to receive a commission for your sales, you must use the URL returned in the <code>itemAffiliateWebUrl</code> field to forward your buyer to the ebay.com site. </span> |

### event_item
| Method | Path | Description |
|--------|------|-------------|
| GET | /event_item | This method returns a paginated set of event items. The result set contains all event items associated with the specified search criteria and marketplace ID.<h3><b>Restrictions </b></h3>This method can return a maximum of 10,000 items. For a list of supported sites and other restrictions, see <a href="/api-docs/buy/browse/overview.html#API" target="_blank ">API Restrictions</a>.<br><br><span class="tablenote"><b>eBay Partner Network: </b> In order to receive a commission for your sales, you must use the URL returned in the <code>itemAffiliateWebUrl</code> field to forward your buyer to the ebay.com site. </span> |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all deal_item?" -> GET /deal_item
- "Get event details?" -> GET /event/{event_id}
- "List all event?" -> GET /event
- "List all event_item?" -> GET /event_item
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
