# Bluey Poseable Figures — curation hints

## Format

Fully articulated (moving arms and torso) figures, roughly 2.5-3" tall —
larger and more detailed than the hard-plastic Mini Figures (see
[`../mini-figures/CLAUDE.md`](../mini-figures/CLAUDE.md)).

## The figure is the collectible, not the retail pack

Moose Toys sells these figures bundled — named multi-packs ("Bluey & Family
Figure 4-Pack") and single-figure "Story Starter" packs (a figure plus one
episode-themed prop and a mini postcard) — but **the pack box is retail
packaging, not a collectible in its own right**: owning every figure from a
multi-pack loose is the same as owning the multi-pack. Don't catalog the
pack itself as a `type: pack` item. Instead, catalog each figure directly
as its own plain `type: figure` item sitting flat in this directory — the
same way Pokémon TCG catalogs individual cards, not sealed booster boxes.

**One collectible per visually distinct sculpt, not per pack appearance.**
A character reappears across many multi-packs wearing its plain everyday
look — that's one figure, filed once, regardless of how many different
packs happened to include it. A character with a costume, a held/worn prop
that's part of the sculpted pose, or a distinctly different sculpted
expression is a *different* collectible and gets its own entry — record
what makes it different in `attributes.variant`
(e.g. `"Vampire Costume"`, `"Fishing Hat"`, `"Silly Expression"`). Leave
`attributes.variant` off entirely for a character's plain/default sculpt.

**A loose, unattached accessory sitting in its own blister-tray cavity does
not make a figure distinct** — only a costume/prop actually worn or held by
the sculpt itself counts. E.g. Bluey & Bingo's Pool Time 2-Pack includes two
loose swim-goggle pairs neither figure is shown wearing — both figures stay
their plain sculpt, no `variant`. Check the pack's own product photo before
deciding; don't infer a costume from a pack's marketing name alone (a pack
themed "Doctor Checkup" turned out to bundle unworn props with two
plain-sculpt figures, not costumed ones).

Story Starters are simpler to judge — the single included prop (a plush toy,
a crown, a hay bale) is always what the figure is shown holding/using, so
it's always worth its own `variant` entry, even for a character that
otherwise has no other costumed variants.

## Naming files

`<character-slug>.yaml` for a character's plain sculpt (e.g. `bluey.yaml`).
`<character-slug>-<variant-slug>.yaml` for a distinct variant (e.g.
`bluey-vampire-costume.yaml`, `bluey-hay-bale.yaml`). Don't file the same
character+variant combination twice even if it recurs across multiple packs
— treat a recurring sculpt as one entry, not one per pack it shipped in.

A few named characters (`Baby Bluey`, `Young Bandit`, `Young Chilli`) are
distinct enough in the source material that they get their own `name`
rather than being modeled as a "variant" of the adult character — keep
following that precedent rather than retrofitting them under
`attributes.variant`.

## No printed catalog number

Neither pack type prints a collector/catalog number — identify a figure by
character name plus its `attributes.variant` description. Retailer SKUs
(Amazon/Target item numbers) are not Moose Toys catalog numbers — don't
record them as `attributes.number`.

## Images

Many figures — especially plain sculpts and multi-figure variants — have no
photo of themselves alone; the only available source is the shared pack
product photo. That's fine per the retailer/marketplace-photo fallback
documented in [`docs/primitives/ITEM.md`](../../../../../docs/primitives/ITEM.md)
as long as the photo genuinely shows that figure's own appearance clearly —
don't use a pack photo where the figure in question isn't identifiable
within it.
