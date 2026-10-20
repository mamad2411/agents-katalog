# Video Games — curation hints

## What belongs here

Physical video game software (cartridges, discs) as the collectible unit.
Not hardware (consoles/handhelds themselves) — a platform directory
represents where its games were released, not a purchasable item in this
category. Hardware could become its own collection someday, but that's a
separate concern from cataloging the games.

## Directory structure

```
video-games/
  CLAUDE.md
  item-attributes.schema.json  # generic fallback; each platform overrides it
  _collection.yaml
  <manufacturer>/
    _collection.yaml
    <platform>/
      CLAUDE.md                  # platform-specific conventions — required
      item-attributes.schema.json  # platform-specific attributes — required
      _collection.yaml
      <game>.yaml
```

**The top level under `video-games/` is always a manufacturer** — never a
genre, era, or region. Manufacturer is its own directory level (not folded
into platform) to keep the top level bounded at "number of manufacturers"
rather than "number of platforms ever made" — Nintendo alone spans a
dozen-plus handhelds/consoles, and that's before Sega, Sony, Atari, and
Microsoft are added. Follow the shape of
[`nintendo/game-boy/CLAUDE.md`](nintendo/game-boy/CLAUDE.md) as a worked
example.

## Adding a new platform

1. Create `<manufacturer>/<platform>/` (create `<manufacturer>/` too if it
   doesn't exist yet — it only needs a `_collection.yaml`, no `CLAUDE.md`/
   schema of its own unless it has platforms that need different
   conventions).
2. Write the platform's `CLAUDE.md` — identification scheme (many platforms
   have official per-game catalog/product codes printed on the
   cartridge/box/disc; verify the exact format before assuming it applies
   uniformly, and check whether it varies by region), naming convention,
   known pitfalls (region-locked releases, re-releases/reprints, compilation
   or multi-cart titles).
3. Write `item-attributes.schema.json` — don't reuse another platform's attributes
   as-is; verify against the actual platform rather than assuming they
   match.
4. Write `_collection.yaml`.
5. Run the validator before opening a PR.
