---
name: ui-reference-marketplace
description: "A worked reference, measured from a hand-designed marketplace: a store of many products from many sellers, organised in shelves, with search first, product cards that carry every buying fact, and a playful but systematic look. Its skeleton, wireframes, measures and component anatomy, and what to take from it. Read before building a store, marketplace or product catalogue."
---

# Reference: a marketplace of shelves

Measured from a hand-designed store (mastumbas.id, a marketplace for digital
products). Take its structure and its decisions; its words, name, colours
and window motif belong to it. Its concept is its own: find yours from your
store (the `ui` skill, section 1).

**Its concept**: a retro desktop. Every shelf of products is a window with a
title bar and its buttons; each category has its own colour, carried from
the shelf's title bar to the header strip of every card in it. Loud, but
every loud thing is a rule applied the same way everywhere.

## Skeleton

1. A ticker across the top: live facts (a discount, a new listing, a stock
   note), moving slowly.
2. Header, sticky, 62px: logo, a wide search field, Catalogue, Categories,
   notifications, cart, account.
3. Hero window: the promise in one line, a second search field, and one
   featured deal.
4. Shelves, one after another: best sellers, newly listed, then one per
   category, each four products wide with "See all".
5. Footer: the promise in one line, "Explore" links, "Help and legal" links.

Search appears twice above the fold: in a store, finding is the job.

## Wireframes (wide screen)

```
│ ◀ ticker: 99% off · item name · just listed · stock tip · ... ◀     │
│ [logo]  [ ⌕ Search products or shops ....................... ]      │
│                    [CATALOGUE] [CATEGORIES▾] [bell] [cart] [account] │ sticky
│ ┌ WINDOW_NAME [HOME] ─────────────────────────────────── _ □ ✕ ┐   │
│ │ [tag] [tag]                                                    │   │
│ │ THE PROMISE IN CAPITALS WITH ONE [HIGHLIGHTED] WORD            │   │
│ │ Two lines on what is sold and how it is protected.             │   │
│ │ [ > search again ...................................... ][⌕]   │   │
│ │ ┌──────┬─────────────────────────────────────┬──────────────┐ │   │
│ │ │ 99%  │ FEATURED DEAL NAME                  │ [ GET IT ]   │ │   │
│ │ │ OFF  │ Rp 1.200  Rp 170.000                │              │ │   │
│ │ └──────┴─────────────────────────────────────┴──────────────┘ │   │
│ └────────────────────────────────────────────────────────────────┘   │
│ ┌ BEST_SELLERS ───────────────────────────── [SEE ALL →] _ □ ✕ ┐   │
│ │ ┌card────────┐ ┌card────────┐ ┌card────────┐ ┌card────────┐  │   │
│ └────────────────────────────────────────────────────────────────┘   │
```

A product card:

```
┌──────────────────────────────────────┐
│ [icon] CATEGORY     [TAG]    [heart] │ header strip in the category's colour
├──────────────────────────────────────┤
│ [icon INSTANT]               [-98%] │ chips over the image
│              product image           │
│ [#1 BEST SELLER]                     │
├──────────────────────────────────────┤
│ Product name on one line, cut with … │
│ [icon] Shop name                     │
│ Rp 123.456  Save 98%                 │ old price struck through
│ WHOLESALE FROM 15 PCS                │
│ Rp 2.400                             │ the price, largest
│ ★ 5 (5) · 210 SOLD                   │ meta in small monospace capitals
└──────────────────────────────────────┘
```

On a phone: the ticker stays; the header keeps the logo, search and cart;
shelves go two cards wide; card chips shrink but stay.

## Measures

- Content 1180px wide, centred. Shelves: 4 columns of 334px, gap 12px,
  inside a window with 12px padding; 2 columns on phones.
- Borders 1.5 to 2px in the ink colour on every window, card, chip and
  button; hard offset shadows (no blur) on windows; square corners or 4px.
- Type: a grotesque (Space Grotesk) in capitals for headings and titles, a
  humanist sans (Plus Jakarta Sans) for body text, a monospace in small
  capitals for meta, tags and window names.
- Colour: a pale lavender page with a faint grid and soft colour in two
  corners; ink near-black; one colour per category (blue, pink, purple,
  green) on title bars and card strips; yellow for actions and highlights;
  pink for discounts. Each colour has one job.

## Anatomy worth taking

- **Search first**: a wide field in the sticky header, and again in the hero,
  with example queries as its placeholder.
- **Shelves, not one endless grid**: best sellers, newly listed, then one
  shelf per category, each with its title and "See all"; the order says what
  matters.
- **A card that answers every buying question**: category, delivery time,
  discount, rank or age, name, seller, old and new price, wholesale terms,
  rating, sold count, stock or guarantee. Each fact in a fixed place, so the
  eye compares cards without reading them.
- **Category colour as a system**: the same colour on the shelf's title bar,
  the card's strip and the category chips, so a colour means a category.
- **Real, live facts in the ticker**, not slogans.
- **Footer as help**: what the store is in one line, the shopper's links
  (catalogue, orders, cart, affiliate), and the legal ones (terms, privacy,
  refunds, contact, FAQ).

## When it fits, and when not

For a store with many products and sellers, a young audience, and a brand
that can be playful. The window motif is this store's identity: a pharmacy,
a furniture shop or a bookshop keeps the structure (search first, shelves,
the fact-complete card, colour as a system) and takes a quieter look from
its own concept.
