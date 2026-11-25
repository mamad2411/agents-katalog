---
name: ui-page-shop
description: "How to build a shop's pages: the product listing with filters, the product page with every buying fact, the cart, a short checkout with a payment provider, and the order confirmation, with real prices, stock and delivery terms. Read before building an online store or a checkout."
---

# A shop: listing, product, cart, checkout

The generated shop opens with a "Summer sale" banner, lists products with
invented prices and five-star ratings, hides "Add to cart" until hover,
demands an account before checkout, builds its own card fields, and ends on
a toast. A shopper needs three answers on every screen: what exactly is
this, what will it cost in total, and when will it arrive. Every price,
stock figure, rating and delivery promise comes from real data or stays a
visible placeholder (`[Price]`, `[Delivery time]`). The measures are in
`ui-layout`, a worked store in `ui-reference-marketplace`, each part in its
`ui-part-*` skill.

## 1. The screens

| Screen | URL | Its job |
|---|---|---|
| Listing | `/shop`, `/shop/chairs`, `/search?q=` | Narrow many products to a few worth opening |
| Product | `/products/oak-dining-chair` | Answer every buying question, then add to cart |
| Cart | `/cart`, and a drawer | Confirm what, how many, and the total |
| Checkout | `/checkout` | Contact, delivery and payment with the least typing |
| Confirmation | `/orders/[number]` | Say it worked and what happens next |

## 2. The listing

```
│ Logo  [ Search chairs, tables, lamps ............ ]     Account  Cart (2) │
│ Home › Chairs                                                             │
│ Chairs · 48                                                               │
│ [Category ▾] [Price ▾] [Material ▾] [In stock]           Sort [Newest ▾]  │
│ Oak ✕   Under Rp 2.000.000 ✕   Clear all                                  │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│ │  image,  │ │          │ │          │ │          │  one ratio for all     │
│ │   4:5    │ │          │ │          │ │          │                        │
│ │ Name     │ │ Name     │ │ Name     │ │ Name     │                        │
│ │ [Price]  │ │ [Price]  │ │ [Price]  │ │ [Price]  │                        │
│ │ 3 colours│ │ Ships    │ │ 2 left   │ │ Sold out │  one fact that matters │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘                        │
│                   Showing 24 of 48   [ Show more ]                         │
```

- Filters and sort in a toolbar above the grid for up to about five facets;
  a left column (240 to 280px) of facet groups when there are many (sizes,
  brands, materials, a price range). Real counts per option; active filters
  as removable chips with "Clear all"; all of it in the URL.
- The card: one image ratio for the whole grid (1:1 or 4:5,
  `object-fit: cover`); the name in at most two lines; the price with its
  currency; a sale price beside the previous one only when that price was
  real (in the EU, the lowest of the previous 30 days); the variant hint
  ("3 colours", "Sizes 38 to 44"); one stock or delivery fact when it
  matters; the rating with its count only from real reviews. The card is
  one link (`ui-part-cards`); a quick Add only for products without
  variants, visible without hover.
- 4 columns on wide screens (3 beside a filter column), 2 on phones, gaps
  16 to 24px.
- "Show more" with the count, the page in the URL, the scroll position
  restored on Back; numbered pages for very large catalogues
  (`ui-part-pagination`).
- Sort by what exists: Newest, Price low to high, Price high to low; Best
  selling or Top rated only when real data backs them.

## 3. The product page

```
│ Home › Chairs › Oak dining chair                                          │
│ ┌──────────────────────────────┐   Oak dining chair                  (h1) │
│ │                              │   Rp [price] · incl. VAT                 │
│ │          main image          │   ★ [rating] · [n] reviews, real only    │
│ │                              │   Colour: Natural                        │
│ └──────────────────────────────┘   (●) Natural  (○) Walnut  (○) Black     │
│ [▪] [▪] [▪] [▪] [▪]                 Size: [ Seat 45 ] [ Seat 50 · 1 left ] │
│                                     Quantity [ − 1 + ]                    │
│                                     [          Add to cart          ]     │
│                                     Arrives [date range] · [returns line] │
│ Description · Dimensions · Materials and care · Delivery and returns      │
│ Reviews · Goes with                                                       │
```

- Gallery: the main image large (6 or 7 of 12 columns), thumbnails or a
  swipeable strip with a counter ("2 of 6"), a lightbox for zoom, images
  that follow the chosen variant, alt text that says what differs
  ("Walnut finish, side view", `ui-part-images`).
- The buy box, in this order: name (`h1`); price with currency and the tax
  note, and the unit price where the law asks for it (per kg, per litre);
  the real rating linking to the reviews; the variants; quantity; Add to
  cart; the delivery estimate and the returns summary beside the button.
  It sticks beside the gallery on wide screens.
- Variants as radio groups (`fieldset` and `legend`: "Colour", "Size"),
  swatches with their names in text, the chosen one marked by more than
  colour, stock per variant ("1 left", "Sold out"). A sold-out variant stays
  selectable and turns the button into "Notify me when it is back", rather
  than a greyed swatch with no reason (`ui-part-choices`).
- Price, stock and images change with the variant without moving the
  layout; the URL carries the variant (`?variant=walnut-50`).
- Add to cart is the one primary action. After it, the button says "Added"
  for 2 seconds, the cart count changes (announced politely), and a small
  drawer shows the item with "View cart" and "Checkout", without leaving
  the page.
- Below: the description in the shop's own words, dimensions with units,
  materials and care, delivery and returns in full, the specification as a
  table or `dl`, reviews (real only, with count and distribution, "No
  reviews yet" when there are none), and related products from real
  relations ("Goes with", "Also in walnut").

## 4. The cart

- Each line: image, name as a link, the variant, unit price, a quantity
  stepper (buttons named "Decrease quantity" and "Increase quantity", the
  number typeable), the line total, and Remove, which shows "Removed Oak
  dining chair · Undo".
- The summary: subtotal, delivery (its price, a free-delivery threshold only
  if one exists, or "Calculated at checkout"), tax (included or added, as
  the market expects), discounts, the total, and Checkout as the one
  primary action; "Continue shopping" as a link.
- The promo code collapsed behind "Have a promo code?", so people without
  one do not leave to hunt for one; its result said in place ("SAVE10
  applied", or why it was refused).
- Changes since adding are said on the line: "Price changed from Rp X to Rp
  Y", "Only 1 left: quantity set to 1".
- Kept on the server for signed-in shoppers, by a cookie id for guests;
  totals always recomputed on the server. Empty: "Your cart is empty" and a
  link back to the shop.

## 5. Checkout

```
│ Logo                                              ‹ Back to cart          │
│ [ Apple Pay ] [ Google Pay ] [ PayPal ]        ┌ Order summary ────────┐  │
│ ───────────── or pay by card ─────────────     │ [img] Oak chair ×2     │  │
│ Contact    Email [.......................]     │ Subtotal     Rp [..]   │  │
│ Delivery   Country [Indonesia ▾]               │ Delivery     Rp [..]   │  │
│            Name [..........]  Address [...]    │ Total        Rp [..]   │  │
│            (●) Regular · Rp [..] · [dates]     └────────────────────────┘  │
│            (○) Express · Rp [..] · [date]                                 │
│ Payment    [ the provider's payment element ]                             │
│            [ Pay Rp [total] ]                                             │
```

- Guest checkout allowed; an account offered after the order ("Save your
  details for next time"), never required before it.
- As few steps as the task allows: contact, delivery, payment, on one page
  in sections or as three steps (`ui-part-steps`); the header cut down to
  the logo and a way back to the cart.
- Express wallets at the top (Apple Pay, Google Pay, PayPal, and the ones
  the market uses), through the provider (Stripe's Express Checkout
  Element and its equivalents).
- The email first; the phone only when the courier needs it, saying so.
- Country first (it decides the address fields), `autocomplete` on every
  field (`email`, `shipping name`, `shipping street-address`, `shipping
  postal-code`, `shipping country`, `tel`), address suggestions as help,
  never as a requirement; billing the same as delivery by default.
- Delivery options as radio cards with price and the dates they promise.
- Payment inside the provider's own fields (Stripe Payment Element, Adyen
  Drop-in, Mollie Components, Midtrans Snap or Xendit in Indonesia): card
  numbers never touch your server, which keeps most of PCI DSS off you,
  and 3-D Secure and local methods (bank transfer, virtual accounts,
  e-wallets, QRIS) come with them.
- The order summary in view throughout: a right column on wide screens, a
  collapsed "Show order summary · Rp [total]" at the top on phones.
- Errors on the field that caused them; a declined card in plain words with
  the way forward ("Your card was declined. Try another card or method.");
  nothing typed is lost.
- The Pay button names the amount. The server recomputes every price,
  discount, tax and delivery cost at submit, creates the order with an
  idempotency key, and marks it paid only from the provider's webhook
  (`backend-integrations`, `backend-api`). No pre-ticked extras or
  marketing boxes.

## 6. The confirmation

- A page reached by redirect after payment: "Order [number] is confirmed",
  what was bought, the delivery address and expected dates, the payment
  status ("Paid", or for a transfer "Waiting for your payment of Rp [total]
  to [account] before [time]"), what happens next, where the receipt was
  emailed (only if it was), a link to track the order, and the account
  offer for guests.
- Reload and Back do not order again; the purchase is recorded once.

## 7. States

- Sold out: the product stays findable, says "Sold out", offers "Notify
  me" and similar products.
- A price or stock change during checkout is said above the summary before
  paying, never charged silently. A failed payment keeps the cart and the
  details; a pending one (a transfer, a bank redirect) says what to do and
  by when.
- Loading keeps the layout: image and text skeletons in the grid, the buy
  box never shifting when the price arrives.

## 8. On a phone

- Listing: two columns, search at the top, filters and sort in a sheet
  from one "Filters (2)" button, its apply button showing the result
  ("Show 18 products").
- Product: the gallery first (swipe, with a counter), then name, price,
  variants and the button; once that button scrolls away, a bar fixed to
  the bottom with the price and Add to cart, above the safe area.
- Cart and checkout in one column, the summary collapsed at the top, Pay
  full width at the end, inputs at 16px so iOS does not zoom.

## 9. SEO and speed

- Listing and product pages rendered on the server with their real text;
  one canonical URL per product (variant parameters point to it); filter
  combinations `noindex` or canonical to the category (`frontend-seo`).
- Product structured data (JSON-LD) from the data the page shows: name,
  image, description, sku, brand, `offers` with price, currency,
  availability and url, `aggregateRating` only from reviews on the page,
  shipping and return policies when real; BreadcrumbList. Cart, checkout
  and confirmation are `noindex`.
- Images in AVIF or WebP with `srcset`; the product page's first image
  eager with `fetchpriority="high"`, grid images below the fold lazy; fixed
  ratios so nothing shifts (`frontend-performance`).

## Check it

- Buy end to end in the provider's test mode (for Stripe, 4242 4242 4242
  4242, and 4000 0027 6000 3184 for a 3-D Secure challenge), as a guest and
  signed in, at 360px and 1440px.
- The confirmation's total equals the server's order record; a price
  changed in the database mid-checkout is said before paying.
- Keyboard only through variants, cart quantities and checkout; a screen
  reader hears the variant, its stock and the cart count change.
- `preview` at 360, 768 and 1440px on every screen; the Rich Results Test on
  a product page; `curl` a product URL and find its name and price in the
  HTML.

## Avoid

Invented prices, ratings, reviews, stock counts or countdowns; a struck-out
price that never existed; Add to cart only on hover; swatches without
names; sold-out options greyed with no reason; an account required before
paying; hand-built card fields; totals computed in the browser; pre-ticked
extras; a promo field that sends people away to hunt; a confirmation that
is only a toast; a cart that forgets itself.
