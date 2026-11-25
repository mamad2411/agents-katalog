---
name: ui-page-local-business
description: "How to build a page for a local business or service that phone visitors can act on: hours, address, phone and booking in the first screen, opening hours as a table with today and exceptions, map and directions links instead of a heavy embed, tap-to-call and WhatsApp, services and prices, real photos and reviews, access information, LocalBusiness structured data with real values, languages, and a page that loads fast on a slow connection. Read before building or reworking one."
---

# Local business or service page

The generated page for a bakery, a clinic or a salon opens on a full-screen
stock photo under a slogan, keeps the hours in the footer and the phone
number in an image, loads a map embed of a megabyte, shows five-star
reviews nobody wrote and prices the owner never set. Its visitors are
mostly on phones, often outdoors on mobile data, looking for four facts
and one button. This skill puts those first, as text and links that work
on a slow connection.

One kind of page. The measures are in `ui-layout`; its parts (header,
images, social proof, back to top) have their own `ui-part-*` skills.
Facts about the business you were not given stay visible placeholders on
the page and are listed in your report (`ui` section 11, `writing`).

## 1. What visitors come for

What, where, when, how much, how to book. No slogans before facts.

| The visitor asks | The page answers with | Where |
|---|---|---|
| Are you open now? | Today's hours and an open or closed status | First screen, hours |
| Where are you? | The address as text, a map link, directions | First screen, location |
| Can I call or message? | Tap-to-call, WhatsApp when the business uses it | First screen, header |
| Can I book or order? | The one primary action | Header, first screen |
| What do you offer, for how much? | Services or the menu with prices | Second section |
| Can I trust you? | Real photos, real reviews with their source | After the offer |
| Can I get in, park, pay? | Access, parking, languages, payment | Location section |

## 2. The first screen

```
┌────────────────────────────────┐
│ [Name]             [ Book ]    │ 56px, sticky
├────────────────────────────────┤
│ Physiotherapy in [Area]        │ h1: what and where
│ [Who it is for, in one line]   │
│ ● Open now · until 20:00       │
│ [        Book a visit        ] │ primary
│ (Call) (WhatsApp) (Directions) │
│ [Street, number, area]         │
│ Today 08:00 to 20:00 · Hours › │
│ [photo of the entrance]        │
└────────────────────────────────┘
```

- On a 360px phone, without scrolling: what it is and where (the `h1`),
  the open status, the primary action (Book, Order, Reserve), then Call,
  WhatsApp and Directions as secondary buttons at 44px or more, and the
  address and today's hours as text.
- On wide screens: those facts in 7 of 12 columns beside a real photo of
  the place in 5; the name in the header.
- The header sticks with the booking action in it, so booking is one tap
  from anywhere on the page (`ui-part-header`).

## 3. Opening hours

- A table or `dl` of all seven days, in the page's HTML: "Closed" on the
  days it is closed, split days written out ("09:00 to 12:00, 14:00 to
  18:00"), the locale's time format (24-hour in Indonesia and most of
  Europe). A summary may group days ("Mon to Fri"); the table lists each.
- Today marked by weight and the word "Today", not by colour alone.
- The status ("Open now · until 20:00", "Closed · opens Mon 08:00")
  computed in the business's time zone, not the visitor's; the table is
  complete without the script, which only adds "Today" and the status.

```js
// The business's own clock, wherever the visitor is.
function clockIn(timeZone) {
  const format = new Intl.DateTimeFormat("en-US", {
    timeZone, weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23",
  });
  const p = Object.fromEntries(format.formatToParts(new Date()).map((x) => [x.type, x.value]));
  return { day: p.weekday, minutes: Number(p.hour) * 60 + Number(p.minute) };
}
// clockIn("Asia/Jakarta") -> { day: "Tue", minutes: 845 }
```

- Exceptions (public holidays, a closure for renovation) above the table
  while they apply, with their dates, and in the structured data.
- One source for the hours (a data file) feeding the table, the footer and
  the JSON-LD, so they never disagree.

## 4. Location and getting there

- The address as text in an `<address>`, copyable, with what helps find
  the door when given: a landmark, the floor, the entrance, parking,
  public transport. A photo of the entrance helps more than a map.
- A link, not an embed, by default: "Open in Maps" to
  `https://www.google.com/maps/search/?api=1&query=<encoded name and
  address>` and "Directions" to
  `https://www.google.com/maps/dir/?api=1&destination=<encoded address>`;
  both open the Maps app on a phone.
- An interactive map only on request: a static image (its alt text says
  where, "next to [landmark]") and a "Show map" button that loads the
  embed, which costs hundreds of kilobytes and sets cookies.

## 5. Calling, messaging, booking

- `<a href="tel:+62211234567">(021) 123 4567</a>`: the international form
  in the link, the local form in the text.
- WhatsApp where the business uses it (common for small businesses in
  Indonesia): `https://wa.me/62812xxxxxxx?text=` with a short, URL-encoded
  message ("Hello, I would like to book a visit"); the number with its
  country code, no plus sign and no leading zero.
- The primary action goes to the business's real system: its booking
  tool, a reservation service, the delivery apps it is on (GoFood,
  GrabFood, ShopeeFood), or a short request form (`ui-page-form`) that says
  how and when they confirm. A booking button that goes nowhere is a lie.
- Email as `mailto:`, secondary. A contact form is never the only way in.

## 6. Services, menu and prices

- A list or table: the name, one line on what is included, the duration
  where it matters, the price; grouped by kind.
- Prices in the local format (`Rp 150.000`):
  `new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR",
  minimumFractionDigits: 0, maximumFractionDigits: 0 })`. "From" only when
  true. Prices not given are `[Price]`, never guessed, never "Affordable".
- The menu as HTML text, not a PDF or a photo of the board (unreadable on
  a phone, invisible to search and screen readers); a PDF as an extra.
  Dietary and allergen marks in words, or letters with a key ("V:
  vegetarian"), not icons alone.

## 7. Photos, team and reviews

- Real photos: the entrance, the inside, the work (the bread, a finished
  cut), the team, each with alt text that says what it shows
  (`ui-part-images`). None given: a text-led page and `[Photo of the shop
  front]` in the report, never stock photos of smiling people.
- The team with names, roles and qualifications (a clinic's registration
  numbers) only as given.
- Reviews only when real: the rating with its source, count and date
  linked to the listing ("[rating] on Google Maps, [n] reviews, [month]"), and
  quotes with the reviewer's first name and date, with permission. None:
  no section (`ui-part-social-proof`).

## 8. Access and practical facts

- A short list in words: step-free entrance, lift, accessible toilet,
  parking (and accessible bays), baby changing, pets, quiet hours,
  languages spoken, payment methods (cash, cards, QRIS), Wi-Fi. Only what
  is true; an unknown stays out, or a placeholder.
- The page in the customers' language; a second language (English for
  visitors) as a real translation through `i18n`, with `lang` and
  `hreflang` (`frontend-seo`).

## 9. Structured data and search

- JSON-LD with the most specific type that fits (`Bakery`, `Dentist`,
  `Restaurant`, `HairSalon`, else `LocalBusiness`), generated from the same
  data as the page. A field whose value is still a placeholder is left out
  until it is real. The shape:

```json
{
  "@context": "https://schema.org",
  "@type": "Bakery",
  "name": "[Business name]",
  "url": "https://[domain]/",
  "telephone": "+62[number]",
  "address": { "@type": "PostalAddress", "streetAddress": "[Street]",
    "addressLocality": "[City]", "postalCode": "[Postcode]", "addressCountry": "ID" },
  "openingHoursSpecification": [{ "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "07:00", "closes": "19:00" }]
}
```

- Add `geo`, `image`, `priceRange`, `servesCuisine` or `menu`, and
  `specialOpeningHoursSpecification` for holidays, as the facts arrive. No
  `AggregateRating` for reviews the business shows about itself: Google
  stopped showing stars for such self-serving markup in 2019.
- The name, address and phone written the same everywhere: the page, the
  Google Business Profile, maps and directories. The profile's hours are
  what search shows first, so they must match the page.
- Title "[Kind] in [Area] · [Name]" within 60 characters, a description
  with the area and what to do; one page per branch, each with its own
  hours, phone and JSON-LD.

## 10. Fast on a slow connection

- The facts, the actions and the hours are HTML that works with no
  JavaScript; script adds only the status and small touches.
- Budgets for mobile data: script under about 50 kB, the first photo under
  about 150 kB (AVIF or WebP with `srcset`, width and height set), one or
  two `woff2` fonts or a system stack, everything below the fold lazy
  (`frontend-performance`).
- No map iframe on load, no autoplaying video, no carousel, no social feed
  embeds (link to the profile instead), no animation library.

## 11. The rest of the page

1. Header, sticky, with the booking action.
2. First screen (section 2).
3. Services or the menu with prices.
4. Photos of the place and the work; the team in three or four sentences
   with specifics; reviews, when real.
5. Location and hours in full: the table, exceptions, directions, access.
6. How booking works, and questions people really ask (walk-ins, deposits,
   cancelling), when given.
7. Footer: the name, address, phone and hours again, the profiles and the
   legal pages that exist.

On a phone this runs past three screens, so the page has a back-to-top
control (`ui-part-back-to-top`), stacked clear of any bottom bar.

## Check it

- `preview` at 360px: the first screen shows what, where, today's hours,
  the phone and the booking action without scrolling; touch targets, the
  sticky header and back to top pass at every width.
- Read every action's `href`: `tel:` in international form, `wa.me` with
  no plus or leading zero, maps URLs encoded. Tap them on a phone if one is
  at hand.
- Set another time zone on the machine: the status still follows the
  business's clock. Validate the JSON-LD (Rich Results Test,
  validator.schema.org) and check each value against the page.
- DevTools with Slow 4G and a 4x slower CPU, then with JavaScript off: the
  facts and links are all there and readable within a few seconds.
- `ui_check`; list every placeholder (prices, hours, photos, reviews) in
  your report.

## Avoid

A slogan over a stock photo as the first screen; hours only in the footer
or in an image; a phone number that cannot be tapped; a map embed on load;
a menu only as a PDF; invented prices, reviews, stars, awards or founding
years; self-serving rating markup; stock photos as the team; a carousel;
an open status in the visitor's time zone; a booking button that goes
nowhere; a contact form as the only way in; three copies of the hours that
disagree.
