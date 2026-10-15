---
name: optimize-store-listing
description: "Optimize store listing: metadata, creatives, conversion, compliance."
---

# Optimize Store Listing

Create one truthful channel listing and creative sequence for install,
wishlist, trial, or purchase.

## Method

1. Open [store listing patterns](references/store-listing-optimization-patterns.md).
2. Define the exact product release, channel, territories, locales, audience,
   job, positioning promise, conversion event, price model, devices, inputs,
   age modes, and current listing.
3. Retrieve the channel's current metadata, asset, rating, disclosure,
   experiment, accessibility, and localization requirements.
4. Map audience questions to a narrative: distinctive outcome, first value,
   core interaction, depth or workflow, social value when real, trust,
   compatibility, commercial terms, and call to action.
5. Specify metadata and ordered media requests for icon/key art, screenshots,
   video, captions, transcript, alt text, compatibility, privacy, price, IAP,
   subscription, ads, and support links.
6. Route exact rendered media to `produce-product-assets`. Validate the returned
   files against the current product UI, rights, dimensions, safe zones,
   legibility, accessibility, locale, and channel rules.
7. Give each locale its own search language, cultural meaning, typography,
   reading direction, image treatment, prices, dates, and native-language QA.
8. When the channel supports experiments, define variants, assignment,
   exposure, conversion, activation, retention, refund, support, review, and
   trust measures.
9. Hand the accepted listing and media to `build-distribution-readiness`, then
   read back the published page when publication is part of the request.

## Output

Return a Channel Listing and Creative Sequence with product/channel identity,
audience, narrative, metadata, ordered asset requests, locale briefs, current
channel requirements, experiment, publication handoff, and live readback when
requested.

Listing claims come from the shipped product, price, rights, policy, and
channel owners. Asset files come from Product Asset Production.
