---
name: taiwan-real-estate-search
title: Taiwan Real Estate Search
description: Efficiently navigate and extract property data from major Taiwan real estate platforms (Sinyi, Yungching) handling UI flakiness.
---

# Taiwan Real Estate Search

Efficiently navigate and extract property data from major Taiwan real estate platforms (Sinyi 信義房屋, Yungching 永慶房屋) while handling UI flakiness and market-specific nuances.

## Trigger Conditions
- User asks for property prices or listings in Taiwan.
- User specifies "second-hand houses" (中古屋), "apartments" (公寓), or "elevator buildings" (電梯大樓).
- Task involves searching near a specific landmark or MRT station.

## Workflow

### 1. Initial Search and Mandatory Fallback Order
Use this order to avoid unnecessary Firecrawl usage:

1. **Browser first**
   - **Sinyi (信義房屋)**: Use the main search box with keywords like "南港車站" or "捷運永春站".
   - **Yungching (永慶房屋)**: Similarly, use the keyword search.
   - If the user provides a landmark, type it directly into the search bar rather than navigating through tiered region menus.
2. **`web_search` second**
   - If browser search, navigation, or page loading fails, use ordinary `web_search` before any Firecrawl search.
   - Prefer targeted queries such as `site:sinyi.com.tw 台北市 新成屋 屋齡5年以下`.
   - If results are weak, retry once with revised keywords or another property platform.
3. **`firecrawl_scrape` only for a known URL**
   - Use it only after search identifies an authoritative page and its search snippet lacks required details.
   - Do not repeatedly scrape a page that returns reCAPTCHA, 400, 403, or 404.
4. **`firecrawl_search` is last resort**
   - Use only when ordinary `web_search` errors or remains unusable after one revised query.
   - Briefly state why ordinary search was insufficient before using it.

A browser failure does **not** imply ordinary search is unavailable. Never jump directly from a failed browser interaction to `firecrawl_search`.

### 2. Handling Filter Failures & Advanced Navigation
- **The "Verified Direct URL" Strategy**: If UI filters are unresponsive, use a filtered URL only when it was obtained from a real link, browser navigation, or search result. Do not guess URL encodings or undocumented path structures.
- **The "Small Result" Strategy**: If total results are < 20, do not waste turns filtering. Inspect all visible results and filter manually in the summary.
- **Visual Verification**: Use `browser screenshot` and `browser get text` to confirm whether a landmark search actually applied or silently defaulted to a broader district.

### 3. User Interaction - Visual Feedback
- **Step-by-Step Reporting**: If the user requests visual confirmation, capture `browser screenshot` after significant actions and attach the resulting screenshot path.

### 3. Data Extraction & Categorization
Taiwan property prices vary wildly based on building type. Always categorize results into these three tiers:
1. **公寓 (Gongyu)**: Walk-up apartments, usually 30-50 years old. Lowest price tier.
2. **電梯大樓/華廈 (Dalu/Huaxia)**: Elevator buildings, 10-30 years old. Middle to high price tier. Often includes "公設" (public facilities).
3. **指標建案/新成屋 (Premium/New)**: New builds or luxury towers. Highest price tier.

### 4. Key Metrics to Capture
- **Price (總價)**: Note if it "含車位" (includes parking).
- **Age (屋齡)**: Critical for determining loan terms and renovation needs.
- **Layout (格局)**: Look for "三房", "兩房", etc. Watch out for "含加蓋" (rooftop additions).
- **Floor (樓層)**: Apartment top floors or ground floors have unique pricing.

## Pitfalls
- **Ref ID Volatility**: Real estate sites update their DOM frequently. Always run `browser snapshot -i` again if a click reports a missing or stale ref.
- **Search Scope**: Sometimes "Nangang Station" search returns results from nearby "Xinyi" or "Songshan" districts. Clarify locations in the summary.
- **Parking Prices**: Parking spaces in Taipei/Nangang can cost 200-400k NTD. If a price is "含車位", the "ping price" (單價) calculation must subtract the parking value.

## Verification
- Cross-reference prices between Sinyi and Yungching to provide a "Market Price Range" (行情) rather than just a single list.
- Check the "关注人数" (number of watchers) on Sinyi to gauge market demand for a specific unit.
- Distinguish similarly named MRT lines by city before summarizing results; do not assume that an ambiguous term such as "藍線" means a specific city.
- Treat search snippets as discovery evidence, not proof that every listing still exists; verify critical price, age, location, and availability details on the listing page when accessible.
