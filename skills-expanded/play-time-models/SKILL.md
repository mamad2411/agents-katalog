# Models at play time (optional advice)

Genex's experience with games that call a language model while somebody plays. None of this is
required: the platform facts (the player pays and approves, text or JSON only, no author key, the
codes) are in `genex__skill {"name":"genex-tool-llm"}` and `genex__skill {"name":"genex-llm-in-games"}`,
and the game's design is its own. Use what fits, ignore what does not.

## When the feature cannot be a model call

- When the person does not want a play-time model, or the lane is off on the stand, an authored
  version often serves as well: a written dialogue tree, a table of lines, a rule-based director.
  Most good games are built that way.
- When somebody asks for something the lane cannot return (a 3D model typed into existence, paid by
  the player), JSON parameters, then render, is the shape that works: the model returns a
  structured description and the game builds it from assets and code it already ships (a creature
  assembled from generated parts, a room laid out from prefab ids, a palette, a stat block, a line
  delivered from pre-generated voice clips).
- Saying plainly in the handoff that the lane was off, or that the feature runs on its authored
  fallback, keeps the person's picture of the game accurate.

## Keeping the feature playable

- A feature built behind a graceful `unavailable` state (the NPC uses its authored lines, the quest
  falls back to the written one) never promises the player something that 404s.
- In the Genex app (`getShell() === "app"`) the lane has no approval surface; leaving the feature's
  entry point out and playing the authored fallback reads better than an error.
- Guests hold no wallet: showing the feature as sign-in-to-use, rather than hiding it, tells them
  what signing in gives them.
- Offering the featured models, and the full catalog only when someone asks, keeps the picker short.

## When a standing budget ends

| code | what tends to work |
| --- | --- |
| `grant_limit_reached` | authored behaviour returns; a button offers to re-request |
| `grant_stopped` | accept it silently and keep playing |
| `grant_expired` | as stopped; re-request on the next deliberate click |
| `waiting_for_plan` | wait out the stated time |
| `grant_insufficient_funds` | pause the thinking NPCs, say so once, stay playable |

## Keeping the burn low

- Batching several NPCs into one call that returns all their decisions, caching a decision until the
  situation that caused it changes, and picking the cheapest model that passes the game's own check
  all lower what a player spends.
- A call fired on a timer the player cannot see is spend they did not ask for.
- When the game hits `grant_concurrency` or `grant_rate_limited`, batching and caching usually fix
  it better than raising the limits.
