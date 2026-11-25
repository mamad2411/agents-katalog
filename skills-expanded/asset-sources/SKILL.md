# Where assets can come from (optional advice)

Genex's view on sourcing a game's assets. The lanes, their providers and their limits are facts in
the `genex__asset` tool and the `genex-tool-*` cards; the person's own choices (procedural only, no
paid assets, a budget, Local Blender) always come first, and code-built assets are a fine choice
whenever they suit the game.

## A split that tends to work

- **Hard-surface pieces** (weapons, props, vehicles, buildings, kit pieces): Local Blender when it
  is enabled, where they can be modelled and adjusted precisely; the model lane (Tripo, with
  `auto-size`) for an occasional hero prop.
- **Rigged characters and creatures:** Genex's character and creature lanes (Meshy), with clips from
  the free catalog.
- **Sound and music:** Genex's sfx, music and voice lanes.
- **Surfaces:** Genex's texture lane for tiling sets; `terrain` for ground planes.
- **Flat things** (decals, signage, UI art, icons): Genex's image lane. A picture standing in for
  something the game shows in 3D (a crowd, a building, scenery) usually reads as flat in play.

## Settings by role

- **Character face budget** (`polycount`, or `approve-remesh` when finalizing): around 10000 for
  crowds and distant figures, 20000-30000 for a third-person player body, 50000 or more only for a
  close-up hero. A crowd enemy is often `polycount` 10000 with `no-ultra` and a 2k texture.
- **Character textures:** 8k pays off in close-ups; `no-ultra` suits stand-ins and crowds.
- **Models:** `geometry` detailed suits hero pieces; `low-poly` or a lower `face-limit` suits props
  the scene shows many of.
- Naming the settings chosen for each asset in one line helps the person follow the cost.
- The free animation library (`animations.search`) is worth searching before generating a clip:
  a library clip costs nothing.

## When a lane does not deliver

- A mesh no rig accepts can ship static, or move in code.
- When the texture lane fails, an `image` (base colour only) or a material made in the engine can
  stand in.
- When the same lane fails repeatedly, building the piece in code, or moving on and saying so in
  one line, keeps the game moving.
- A visible repeating grid on a large surface is one of the most noticeable signs of a generated
  texture; `terrain`, or a smaller repeat on screen, usually hides it.

## Planning a set

- When planning a game or an asset-related change, a small, concrete asset set, with where each
  piece comes from, helps the person see what generation will cost and what they will get.
- Using suitable assets the game already has before making more saves credits; generating to fill
  a quota does not.
- Checking `genex__asset {"operation":"status"}` before a batch shows whether the account can
  generate and which lanes are live.
- The first playable loop can keep moving while assets generate; saying which generated assets were
  actually wired in keeps the person's picture of the game accurate.
- When a lane lacks the provider the person asked for, saying so once and naming what will be used
  instead avoids surprises.
