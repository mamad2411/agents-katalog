---
name: theme-trip-search
description: Search MyRealTrip flights, stays, activities, and itinerary inputs for a destination, dates, travelers, budget, and theme. Use for travel recommendations and HTML itinerary proposals; full-trip and itinerary requests always include stay recommendations unless the user explicitly declines lodging.
---

# Theme Trip Search

Use this skill when the user wants MyRealTrip product recommendations, travel product discovery, flight and stay comparison, itinerary candidates, or an itinerary recommendation for a theme. When the user asks for 일정 추천, 여행 일정, 코스 추천, itinerary, travel plan, or trip proposal, the default deliverable must be an HTML proposal artifact, not text-only recommendations.

## Workflow

1. Extract the travel request:
   - Destination, preferably city-level.
   - Dates or trip length.
   - Number and type of travelers.
   - Budget or price sensitivity.
   - Theme, constraints, and deal-breakers.
   - Product types requested: flights, stays, tours, tickets, activities, or full trip package.
   - Review filter needs such as low walking burden, parents-friendly, kids-friendly, guide quality, food depth, shopping time, beginner-friendly pacing, room comfort, or station access.
2. Use the bundled MyRealTrip MCP tools when available. If they are not visible, use tool discovery for `myrealtrip`.
3. For incomplete planning requests, call `planTravel` first when available.
   - If dates remain unknown, do not use tomorrow as the itinerary date. Apply the missing-date value-flight workflow below.
   - If traveler count remains unknown, use 1 adult and label it as an assumption.
4. Search every relevant product type. Do not stop after the first product type when the user asks for multiple categories:
   - Flights: use `searchInternationalFlights` for overseas destinations and `searchDomesticFlights` only when both origin and destination are Korean cities.
   - Flight discounts or cheapest-date requests: call `getPromotionAirlines` and `flightsFareCalendar` before or alongside real-time flight search.
   - Stays: use `searchStays` for hotels, accommodations, pensions, resorts, and lodging.
   - Stay details: use `getStayDetail` after `searchStays` when room types, per-room pricing, facilities, amenities, location fit, reviews, or detailed comparison matter.
   - Tours, tickets, and activities: use `searchTnas` for experiences and attractions.
   - **Itinerary/full-trip default:** call `searchStays` even when the user did not mention lodging. Skip stays only when the user explicitly declines lodging or the trip has no overnight stay.
   - Use the selected dates, traveler counts, value sorting, and a route-hub keyword. Fetch `getStayDetail` for the top 2-3 viable candidates and apply `review-theme-filter` to each.
5. Build an initial shortlist by theme and value fit, not only by price:
   - Theme evidence from title, category, duration, location, rating, and tags.
   - Practical fit for traveler type.
   - Schedule feasibility.
   - Price, cancellation value, and booking friction.

### Per-item booking-link contract

- Preserve one booking URL on every displayed flight, stay, and activity item. Never use one category-level CTA for multiple rows/cards.
- Flights: copy each result's complete `reservationUrl` byte-for-byte; never shorten it or replace it with a generic search URL.
- Stays: fetch `getStayDetail` for every displayed shortlist item and preserve its returned `shareWebLink`. If detail lookup fails, do not display the item as bookable; label it `예약 링크 미검증`.
- Activities: use the canonical `https://experiences.myrealtrip.com/products/{gid}` URL per item.
- Carry an explicit `booking_url` field beside each product through ranking and HTML generation so links cannot be detached from their source item.


## HTML Proposal Trigger

When the user asks for any itinerary-style output, create an HTML proposal immediately after the required MyRealTrip searches and review filtering. Do not stop with text-only recommendations unless the user explicitly says they do not want a file.

Trigger phrases include:

- 일정 추천, 여행 일정, 여행 계획, 코스 추천, 루트 추천, 일정 짜줘, 계획 짜줘
- itinerary, travel plan, trip plan, route plan, proposal, HTML, PPT, report
- Any request that combines destination + dates/trip length + traveler/theme and asks what to do or what to book

Required behavior:

1. Run the relevant MyRealTrip searches first. For every overnight itinerary/full-trip proposal, stays are mandatory even if lodging was not named; search flights and activities when implied.
2. Fetch details and filtered review cards for shortlisted non-flight products when available.
   - Preserve booking URLs returned by the search/detail tools. For tours, tickets, and activities, the canonical public URL is `https://experiences.myrealtrip.com/products/{gid}`. Never construct the legacy `https://www.myrealtrip.com/traveler-experiences/{gid}` URL; normalize that legacy form if encountered.
3. Build a day-by-day timetable from the selected products and practical travel constraints.
4. Invoke the `trip-proposal-html` workflow and write a self-contained HTML file into the workspace.
5. In the final response, provide the generated HTML file path and a short summary. Do not make the user ask a second time for HTML.

If essential planning inputs are missing and `planTravel` is available, call `planTravel` first. After planning details are collected, continue into searches and HTML generation automatically. If dates or traveler count are still missing, apply the defaults below without blocking.

## Missing Date And Traveler Defaults

For itinerary, course, route, or full-trip planning requests:

- Missing traveler count: set `adultCount: 1`, `childCount: 0` and state the assumption.
- Missing dates: choose dates from value airfare in the current calendar month and the next calendar month. Do not default the itinerary to today or tomorrow.
- Use the requested trip length to set the fare-calendar `period`. Interpret `3박 4일` as a 4-day period and a return date 3 nights after departure.
- For international destinations, default the origin to `ICN`; for Korean domestic destinations, default the origin to `GMP`, unless the user specified another origin.
- Start the current-month lookup on the earliest valid future departure date. Start the next-month lookup on the first valid date of the next calendar month.
- Call `flightsFareCalendar` once for the remaining current-month window and once for the next-month window. Compare both returned candidate sets, not only each response's first item.
- Select a value date using total fare first, then directness/transfer preference and schedule feasibility when available. State the exact selected departure and return dates and whether the winning candidate came from this month or next month.
- Follow the chosen cached calendar candidate with `searchInternationalFlights` or `searchDomesticFlights` for real-time validation. If real-time search has no usable result, try the next-best calendar date before falling back.
- Use the selected flight dates consistently for stays, date-specific activity options, timetable labels, filenames, and the HTML title slide.
- Clearly label fare-calendar values as estimates and live-search values as real-time prices that may change at booking.
- If `flightsFareCalendar` is unavailable or returns no candidates for both months, use the earliest feasible future dates matching the trip length, label this as a fallback, and continue.
## Flight Value Rules

Use this section whenever the user asks for 항공권, 항공편, 비행기표, airfare, cheapest flights, 가성비 항공권, 최저가, 할인, 특가, or flexible dates.

- Default origin: `ICN` for international flights, `GMP` for domestic flights, unless the user specifies otherwise.
- Default departure date for flight-only quick searches: tomorrow. For itinerary/full-trip planning with missing dates, use the two-month value-flight workflow above instead.
- International route: use `searchInternationalFlights` for destinations outside Korea.
- Domestic route: use `searchDomesticFlights` only when both origin and destination are Korean airports.
- Cheap/discount intent: call `getPromotionAirlines` and use relevant airline codes as candidates for `preferredAirline` searches when applicable.
- Flexible-date or cheapest-date intent: call `flightsFareCalendar` with the route, departure date, trip duration, and transfer preference.
- Always follow calendar estimates with real-time flight search for the chosen date when possible, because fare-calendar data is not real-time.
- Compare value, not only absolute price:
  - total price and per-person price when available
  - direct vs transfer
  - departure/arrival time quality
  - trip duration and red-eye burden
  - baggage or fare caveats when returned by the tool
  - airline promotion match
  - reservation URL availability
- Output a clear verdict such as `최저가`, `가성비 추천`, `시간대 우수`, or `비추천/주의`.
- Always include reservation URLs returned by the flight tools.
- Always tell the user that flight prices are real-time and may differ at booking.

## Stay Value Rules

Use this section whenever the user asks for 숙소, 호텔, accommodation, lodging, stay, 가성비 숙소, 가족 숙소, 위치 좋은 숙소, 조식, 수영장, 무료취소, 시설, 리뷰, or room details.

Also use this section automatically for every itinerary/full-trip request with at least one overnight stay. Do not wait for the user to ask for lodging. Treat the selected stay as the route origin/end point and include its verified price in the total budget. Skip only on explicit user refusal.

- Default stay dates for stay-only quick searches: today through tomorrow. For itinerary/full-trip planning, use the dates selected by the two-month value-flight workflow instead.
- Call `searchStays` with destination keyword, check-in/out, traveler counts, domestic/international flag, and value filters when implied.
- For value-focused stays, consider `order: price_asc`, `discount_rate_desc`, `minReviewRating`, `freeCancellation`, and relevant services such as `WIFI`, `POOL`, `PARKING`, or `FITNESS`.
- For top candidates, call `getStayDetail` when the recommendation depends on room price, room type, amenities, cancellation policy, location fit, or reviews.
- Compare value using:
  - total stay price and per-night price when available
  - rating and review count
  - cancellation/refund tags
  - room availability and no-room status
  - included breakfast or amenities
  - location fit for the itinerary
  - family/parents/kids buying factors when details or reviews support them
- Mark stays with missing details as `detail_unverified` instead of presenting them as fully validated.
- Do not invent room prices, amenities, review counts, or cancellation policies.

## Product Review Filtering Rules
Review filtering is mandatory for every shortlisted non-flight product and is a blocking completion gate. A detail response containing only an aggregate score/count is not review evidence.

- Compare aggregate review counts with returned individual review records.
- If an authoritative product search, detail response, or review API explicitly reports aggregate review count 0, set no_reviews and skip the collector and filtering.
- Do not infer zero from null, omitted, missing, or failed fields. An unknown count remains review_pending and requires collection.
- Treat no_reviews as a valid terminal state and display 등록된 리뷰 없음 separately from unavailable_after_attempt.
- When detail tools omit review bodies or return fewer records than the aggregate count, run ../../scripts/collect_all_reviews_selenium.py immediately using the canonical public product URL.
- Run default public-review API mode first; retry --method selenium when applicable if API collection fails or remains incomplete.
- Do not mark a product unavailable merely because the detail tool omitted reviews. Use unavailable_after_attempt only after the collector was executed and its failure or zero-result was recorded.
- Do not finalize rankings or invoke HTML generation while any shortlisted product is review_pending.
- Record collection method, collected count, aggregate/API/statistic/visible totals, completeness, and failure details for every product.

For every shortlisted non-flight product, fetch detail/review evidence when a detail tool is available:

- Tours, tickets, and activities: call detail tools for the top candidates before final ranking when reviews/detail text are needed.
- Stays: call stay detail tools when amenities, room fit, location, or review fit matters.
- If review data is unavailable, keep the product but mark the review source as unavailable.

Apply `review-theme-filter` logic to each non-flight product separately:

- Convert the user's request into explicit review filter tags.
- Search all available reviews for those tags, constraints, and deal-breakers.
- Select about 5 reviews per product that help the user decide whether to buy.
- Include a mix of matching, practical-detail, and caution/deal-breaker reviews when available.
- If the detail tool omits the full review list and the public site provides an auto-scrolling all-reviews view, use the bundled Selenium collector to enumerate all publicly visible reviews before selecting the decision cards.
- Display need tags, review-type labels, and review warnings in the language of the user's request.
- Display each review's individual star rating when available; show a localized no-rating label when absent and never substitute the aggregate product rating.
- Do not output a review score or grade; show filtered review cards instead.
- Do not let a high rating replace filtered review evidence.

## Final Ranking

Rank final results using product-specific evidence by category:

- Flights: value score from real-time price, calendar/promotion signal, schedule quality, directness, and booking URL.
- Stays: value score from price, rating, detail verification, cancellation value, amenities, location fit, and filtered review evidence.
- Tours/activities: theme fit, availability, price, filtered review evidence, schedule feasibility, and cancellation value.

Clearly separate products with unavailable reviews or unverified details from products with useful filtered reviews.

## Output Standard

Prefer Korean output unless the user asks otherwise. Include source-backed fields from the tool results and avoid inventing prices, availability, ratings, reviews, amenities, room details, flight times, baggage rules, or policies.

For flights, include this minimum line:

```text
항공권 가성비 판단: 최저가 | 가성비 추천 | 시간대 우수 | 주의
근거: 실시간 가격, 최저가 캘린더/프로모션 여부, 직항/경유, 출도착 시간, 예약 URL
```

For stays and activities, include filtered review cards instead of a review score:

```text
구매 판단용 리뷰 필터: available | limited | unavailable
필터 기준: low-walking, parent-friendly, guide-quality, ...
리뷰 1: [match/caution/deal_breaker/practical_detail] 짧은 발췌 + 구매 판단 포인트
...
리뷰 5: ...
확인 안 된 부분: 리뷰에서 판단하기 어려운 리스크
```

If review evidence was not available for a product, say so explicitly instead of presenting it as equally validated.

For itinerary recommendation requests, the output standard is an HTML file plus a concise completion summary. Text-only output is acceptable only for quick clarifying notes, errors, or when the user explicitly asks not to create a file.



