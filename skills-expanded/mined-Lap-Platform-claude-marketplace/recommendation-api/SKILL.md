---
name: recommendation-api
description: "Recommendation API skill. Use when working with Recommendation for find. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Recommendation API
API version: v1.1.0

## Auth
OAuth2

## Base URL
https://api.ebay.com/sell/recommendation/v1

## Setup
1. Configure auth: OAuth2
3. POST /find -- create first find

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### find
| Method | Path | Description |
|--------|------|-------------|
| POST | /find | The <b>find</b> method currently returns information for a single recommendation type (<code>AD</code>) which contains information that sellers can use to configure <a href="/api-docs/sell/static/marketing/promoted-listings.html" title="Selling Integration Guide">Promoted Listings</a> ad campaigns. <p>The response from this method includes an array of the seller's listing IDs, where each element in the array contains recommendations related to the associated listing ID. For details on how to use this method, see <a href="/api-docs/sell/static/marketing/pl-reco-api.html" title="Selling Integration Guide">Using the Recommendation API to help configure campaigns</a>.</p>  <h3>The AD recommendation type</h3>  </p>  <p>The <code>AD</code> type contains two sets of information:</p>  <ul><li><b>The promoteWithAd indicator</b> <br>The <b>promoteWithAd</b> response field indicates whether or not eBay recommends you place the associated listing in a Promoted Listings ad campaign. <p>The returned value is set to either <code>RECOMMENDED</code> or <code>UNDETERMINED</code>, where <code>RECOMMENDED</code> identifies the listings that will benefit the most from having them included in an ad campaign.</p></li>  <li><b>The bid percentage</b> <br>Also known as the "ad rate," the <b>bidPercentage</b> field provides the current trending bid percentage of similarly promoted items in the marketplace. <p>The ad rate is a user-specified value that indicates the level of promotion that eBay applies to the campaign across the marketplace. The value is also used to calculate the Promotion Listings fee, which is assessed to the seller if a Promoted Listings action results in the sale of an item.</p></li></ul>  <h3>Configuring the request</h3> <p>You can configure a request to review all of a seller's currently active listings, or just a subset of them.</p>  <ul><li><b>All active listings</b> &ndash; If you leave the request body empty, the request targets <i>all</i> the items currently listed by the seller. <p>Here, the response is filtered to contain only the items where <b>promoteWithAd</b> equals <code>RECOMMENDED</code>. In this case, eBay recommends that all the returned listings should be included in a Promoted Listings ad campaign.</p></li> <li><b>Selected listing IDs</b> &ndash; If you populate the request body with a set of <b>listingIds</b>, the response contains data for all the specified listing IDs. <p>In this scenario, the response provides you with information on listings where the <b>promoteWithAd</b> can be either <code>RECOMMENDED</code> or <code>UNDETERMINED</code>.</li></ul>  <h3>The paginated response</h3>  <p>Because the response can contain many listing IDs, the <b>findListingRecommendations</b> method paginates the response set.</p> <p>You can control size of the returned pages, as well as an offset that dictates where to start the pagination, using query parameters in the request. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a find?" -> POST /find
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
