# Sitting Cuties — curation hints

## What this line is

Palm-sized Pokémon plush, each weighted with microbeads so it sits upright
on its own. Released in Japan since July 2018 under the name **"Pokémon
fit"**; sold internationally (US/Canada Pokémon Center) as **"Sitting
Cuties."** Both names refer to the same line — don't treat them as separate
collections.

The line ships in discrete numbered **series** ("第N弾"), each of which
debuts every Pokémon (and often every distinct form — regional variants,
Alolan/Galarian forms, Rotom's appliance forms, etc.) from a given
generation in one uniform style, rather than one-off single-character
releases. Known series so far:

| Series | Region  | Generation | Count | Release date | Extra forms beyond base dex |
|--------|---------|------------|-------|---------------|------------------------------|
| 1      | Kanto   | I          | 30    | 2018-07-13    | — |
| 2      | Kanto   | I          | 121   | 2018-11-16    | — (30+121=151, completes Kanto) |
| 3      | Johto   | II         | 127   | 2019-06-08    | Unown ×28 letter/symbol forms (99 species + 28) |
| 4      | Hoenn   | III        | 141   | 2021-01-30    | Deoxys ×4 formes, Castform ×4 weather forms (135 species + 6) |
| 5      | Sinnoh  | IV         | 121   | 2021-11-19    | Burmy/Wormadam ×3 cloaks each, Shellos/Gastrodon ×2, Cherrim ×2, Rotom ×6, Giratina ×2, Shaymin ×2 (107 species + 14) |
| 6      | Unova   | V          | 174   | 2023-01-14    | Basculin/Darmanitan/Meloetta/Keldeo ×2 each, Deerling/Sawsbuck ×4 seasons each, Kyurem ×3, gender pairs (Unfezant/Frillish/Jellicent), Incarnate/Therian ×2 (Tornadus/Thundurus/Landorus) (156 species + 18) |
| 7      | Kalos   | VI         | 107   | 2024-06-15    | Vivillon ×20 patterns, Furfrou ×10 trims, Pyroar/Meowstic gender pairs, Aegislash ×2, Zygarde ×4, Hoopa ×2 (72 species + 35) |
| 8      | Alola   | VII        | 116   | 2025-05-08    | Alolan forms for 18 Kanto species, Oricorio ×4 styles, Lycanroc ×3 forms, Wishiwashi ×2 forms, Type: Null/Silvally, Minior (Meteor + one core color), Mimikyu ×2 forms, Necrozma ×4 forms (base/Dusk Mane/Dawn Wings/Ultra), Marshadow ×2 (base/Zenith) |

Every series above has been fully filed and cross-checked against at least
two independent sources (Bulbapedia's `Sitting_Cuties/<Region>` subpage plus
an official Pokémon Co. Japan announcement, Pokemon.com news post, or
equivalent) — see `collections/plush/pokemon-center/sitting-cuties/<region>/`
for the actual entries. Two corrections worth noting for anyone re-deriving this
table: series 6's date was previously guessed as "2022+" but is actually
2023-01-14 (Japan launch; US Pokémon Center availability didn't follow until
April 2023), and series 7's date is 2024-06-15 (original Japan release), not
2024-09-11 (that's when it became available at the US Pokémon Center).

## Directory structure

```
pokemon-center/                 # the brand — Pokémon Center's own retail line-up
  sitting-cuties/               # this line
    CLAUDE.md
    item-attributes.schema.json
    _collection.yaml            # the whole line
    kanto/                      # one directory per region/generation,
      _collection.yaml          # spanning every series released for it
      <slugified-pokemon-name>.yaml
    johto/
      ...
```

One directory per **region** (matching Bulbapedia's own subpage split), not
per series — Kanto spans series 1 and 2, but it's one continuous roster from
the collector's point of view. Record which series a figure actually shipped
in via `attributes.series`, since that's not recoverable from directory
position alone.

## No printed catalog number

Unlike Squishmallows, individual Sitting Cuties plush carry no collector
number on their hangtag — identify by the Pokémon depicted, the same way
[`../../figures-and-models/re-ment/pokemon/`](../../figures-and-models/re-ment/CLAUDE.md)
does for the same franchise. File as `<slugified-pokemon-name>.yaml`, no
numeric prefix (per the root [`CLAUDE.md`](../../../CLAUDE.md) naming rule
for un-numbered collections).

## Forms and disambiguation

Some series include multiple forms of the same species as separate plush
(e.g. Sinnoh's five Rotom appliance forms, or a species' regional variant
sold alongside its original). Use the form name as the actual `name` (e.g.
`Wash Rotom`, not `Rotom` with a form attribute) — that's how Bulbapedia and
the Pokémon Center itself label these — and slug accordingly
(`wash-rotom.yaml`). This avoids filename collisions within one region
directory without inventing a parenthetical scheme.

## Manufacturer

Pokémon Center plush (Sitting Cuties included) are manufactured under
license by **San-Ei Boeki Co., Ltd.** for the Japan-market line. Don't
hardcode this — check the actual hangtag/box credit per item where possible,
the same caveat as [`../squishmallows/CLAUDE.md`](../squishmallows/CLAUDE.md)
gives for its own manufacturer field. Chinese-market Pokémon plush (a
separate, mainland-China-only retail line manufactured by a different
licensee — confirmed example: 深圳市盟世奇文化产业有限公司, Shenzhen
Mengshiqi Culture Industry Co., Ltd.) are **not** Sitting Cuties and don't
belong in this directory even if visually similar — verify the tag's
territory restriction and manufacturer credit before filing.

## Images

`pokemoncenter.com` product pages return a bot-detection interstitial to
automated fetches — don't assume a fetch failure means the product doesn't
exist. Prefer sourcing product photography from Bulbapedia's
`Sitting_Cuties/<Region>` gallery (official Pokémon Center photos, re-hosted)
or a Pokémon Center product page reachable through a search result snippet,
per the root image-sourcing guidance — retailer/fan re-hosts of the actual
official product photo are an acceptable fallback per
[`../../CLAUDE.md`](../../CLAUDE.md) when the manufacturer's own site can't
be fetched directly.

## Dates

Use the figure's series release date (see table above) for individual
plush unless a source gives a more specific per-figure date (uncommon — most
figures in a series release simultaneously).
