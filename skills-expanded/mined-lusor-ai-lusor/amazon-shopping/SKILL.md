---
name: amazon-shopping
description: Navigate and automate the Amazon Shopping Android app. Use when the task involves searching Amazon, browsing products, adding to cart, or checking out.
keywords: [amazon, shopping, buy, purchase, cart, add to cart, product, search amazon, price, checkout, order]
platform: android
app_package: com.amazon.mShop.android.shopping
---

# Amazon Shopping App: Navigation & Automation

## App Launch
- Package: `com.amazon.mShop.android.shopping`
- Launch via verb: `launch({ app: "com.amazon.mShop.android.shopping", activity: ".HomeActivity" })`
  (or omit `activity` to dispatch the LAUNCHER intent).
- Cold start takes 3-5s; wait before interacting.

## Search Flow
1. Tap the search bar at the top of the home screen (resource_id: `com.amazon.mShop.android.shopping:id/chrome_search_hint_view`) via `tap_element({ index })`.
2. Type your query with `type({ text: "<query>" })` (plain text, no encoding). Pass `clear: true` to wipe a stale query.
3. Press Enter via `key({ keyCode: 66 })`; do NOT tap a suggestion unless specifically required.
4. **Wait 2-3s** for search results to load. Results appear in a scrollable list.

## Search Results
- Product cards are vertically stacked. Each card contains title, price, rating, and Prime badge.
- Prices are often in a separate text view below the title.
- The same product may appear multiple times as different color variants (e.g., "soundcore P20i" in Black and Blue as separate listings). When looking for unique products, check the product title, not just position in the results list.
- The first 1-2 results are typically **Sponsored** (marked with a "Sponsored Ad" prefix). Sponsored products are real products and can be tapped into for full details and reviews. The "Customers say" summary availability varies on sponsored products.
- To scroll results: `swipe({ startX: 540, startY: 1800, endX: 540, endY: 600, durationMs: 300 })` (swipe up).

## Product Detail Page
- After tapping a product, the detail page loads in 1-2s.
- The **Add to Cart** button is usually below the fold. Scroll down to find it.
- Resource ID for Add to Cart: `com.amazon.mShop.android.shopping:id/add-to-cart-button`
- "Buy Now" is nearby and places the order in one step: use it when the user asks to buy now; otherwise add to cart.
- Product title, price, and rating are near the top of the page.

## Cart
- Cart icon is in the top-right corner of most screens.
- Resource ID: `com.amazon.mShop.android.shopping:id/chrome_action_bar_cart_count`
- Cart page shows item list with quantities and subtotal.

## "Customers Say" AI Summary
- Not all products have the AI-generated "Customers say" summary in their reviews. It typically appears on products with a large number of reviews (5,000+), but there is no hard threshold.
- When present, the summary text lives inside the `aw-udpv3-customer-reviews_feature_div` element in the review section.
- If a product lacks this summary after checking the review section, extract it as "N/A"; do not scroll endlessly looking for it.

## Navigating to Reviews
- Tapping the review count (e.g., "98,305 Reviews") on a product page scrolls DOWN on the same page; it does NOT open a new page.
- After viewing reviews, pressing Back returns to SEARCH RESULTS, not to the top of the product page. Plan accordingly.
- The review section uses tab buttons: Details | Explore | Reviews | Top. The "Customers say" summary appears under the Reviews tab content.

## Common Pitfalls
- **Popups**: Amazon often shows location, notification, or sign-in prompts. Dismiss with `key({key:"back"})` or tap "Not now"/"Skip" via `tap_element`.
- **Loading spinners**: Wait at least 2s after any navigation before asserting state.
- **Bottom sheets**: "Choose your location" or delivery prompts may overlay content. Dismiss before interacting with underlying elements.
- **Sign-in walls**: Some actions (Add to Cart, Checkout) require sign-in. If a sign-in screen appears, the task may be blocked.

## Filters & Sliders: What to Avoid
- **NEVER open the "All Filters" panel.** Use discrete filter buttons visible on the search results page instead (e.g. "Under $20", "$20 to $30" buttons that appear below the search bar).
- **NEVER attempt to drag sliders.** The accessibility tree cannot report slider thumb positions, making drag operations unreliable. Use tap-based price range buttons instead of the price slider.
- If you accidentally enter a filter or overlay page, scan the element list for **close, dismiss, or X buttons** (usually top-right) before trying `key({key:"back"})`.
- Prefer scrolling through results and using on-page filter chips over opening any filter panel.

## Timing Guidelines
| Action | Expected Wait |
|--------|--------------|
| App cold start | 3-5s |
| Search results load | 2-3s |
| Product page load | 1-2s |
| Add to Cart confirmation | 1-2s |
| Page scroll settle | 500ms |
