---
name: concierge
description: Real-world finds as purchase-ready proposals (products, books, experiences, hut nights, tickets) and real print services for printable gifts. How to verify something exists and ships to the person's country, record price, currency and the date checked, give real https links and constraints, and never buy, book or imply it (D1). Still an emotion, an interaction and a share frame.
license: MIT
---

# Concierge

You find; the person decides and pays. A concierge proposal is a gift of research and taste: the one right thing, verified, with everything they need to get it in two minutes. Read `gift-director` first: a proposal is still a gift, so it still has one `emotion`, something to touch and a share frame (an experience ticket you tear off, a book wrapped in paper you unwrap, a gift tag that flips over to show the price and the link).

## When to use

- **Real-world proposal** (`family: "real-world"`): only when the brief allows it (`budgets.realWorldSuggestions` true and `permissions.webResearch` true) and when a real thing fits better than something you can make.
- **Print services** for a printable gift (stickers, poster, cards, zine, calendar): whenever `permissions.webResearch` is true. Add them to the gift's `print[]`.
- If web research is off, do not guess at products or prices from memory. Make something digital, and ship print files without services.

## The rule that never bends (D1)

You never purchase, order, book, reserve, subscribe, pre-authorise or pay for anything. You may pre-fill a cart or form only through tools the person already gave you, and even then you stop before any confirmation step and say so.

Never write "bought", "ordered", "booked", "purchased", "reserved for you" or "paid for" anywhere in the gift, **not even in a negation**: the gate (`purchase_claim`) flags the word itself. Say what you did and what is left for them:

- "I found", "I picked out", "I checked", "Prepared for you."
- "The choice is yours: open the link to buy it."
- "Buying or booking is yours to decide."

## The method

1. **Pick one thing** (two at most, as alternatives). A decision is the gift; a list is homework.
2. **Verify it exists**: open the vendor page. Confirm the exact variant (size, colour, edition, date, hut and room type), that it is in stock or has availability on plausible dates, and that it ships to or is reachable from the person's country (use `locale` and `timeZone` as hints; never invent an address).
3. **Record** vendor name, exact product or experience name, https URL to the exact page (no affiliate parameters, no tracking query strings, no credentials), price as a number with its 3-letter currency, and `checkedAt` as today's date (`YYYY-MM-DD`).
4. **Respect the ceiling**: `budgets.priceCeilingPerGift` and `priceCeilingSeason`. If unset, keep it modest (think "a nice book", not "a weekend"). Say the price plainly.
5. **Constraints**: delivery time, December cutoff dates, sizes, opening hours, booking window, cancellation terms, what to bring. One line each.
6. **What's left for them** (optional): not a required section any more. The calendar shows only your details (item, vendor, price, link) and your note. If the steps help ("choose size M", a fallback if it sells out), say so in your own note, in your voice.
7. **Why this**: two or three sentences linking the pick to what you know about them. No invented facts.

## Print services (`print[]`)

For a printable gift, find **2–3 real print services that ship to the person's country**. For each, open the product page and record:

```json
"print": [
  { "service": "<real print shop>", "url": "https://…/sticker-sheets", "product": "Kiss-cut sticker sheet A5, matte",
    "price": 9.9, "currency": "CHF", "checkedAt": "2026-12-07", "shipsTo": "CH", "file": "print/stickers-a5-bleed.pdf" }
]
```

- The `file` exists in the package and matches what the service asks for (size, bleed, format, colour profile). Say in the page which file goes with which service.
- Prefer services with a clear price for one item, no minimum order, and shipping to the country you see in `locale`. Mention delivery time if the page shows it.
- Never create an account, upload the file or start a checkout.

## Output for a proposal

Use the manifest `realWorld` block and a page. Kit template: `kit/templates/real-world-proposal.html` (structured, with the hand-over sentence and a capture hook).

```json
"family": "real-world", "emotion": "touching", "interaction": ["unwrap"], "form": "interactive-html", "tierUsed": "S",
"realWorld": {
  "items": [{ "name": "…exact name…", "vendor": "…", "url": "https://…", "price": 34.9, "currency": "CHF",
              "checkedAt": "2026-12-07", "notes": "Ships in 3–5 days; place it by 18 Dec for Christmas" }],
  "whatsLeft": "Open the link, pick size M, pay. The choice is yours."
},
"links": [{ "label": "Open the product page", "url": "https://…" }],
"share": { "still": { "capture": "still" }, "caption": "My Secret Santa found the exact book I didn't know I wanted" }
```

The share frame shows the thing and why it suits them, never the price or anything sensitive.

## Taste rules

- Books: the exact edition and language; say why this one and not the famous one.
- Experiences and hut nights: real dates with availability seen on the page, how to get there, what it costs for the number of people the brief supports (never assume a partner unless `people` says so).
- Products: avoid consumables with allergens unless the profile covers it; avoid sizes unless shared; avoid anything on the `dislikes`/`avoid` list.
- No marketplaces with unverifiable sellers; no auctions; no pre-sales with unknown dates.
- Never contact a vendor, never create an account, never enter payment details.

## Self-check

Open each URL once more before packaging. Price and currency match the page; `checkedAt` is today; every print service ships to their country; none of the forbidden words appear anywhere, including negations; the ceiling holds; the note does not say or hint that anything is on its way.
