---
name: ghostfeed-avatars
description: Drive Ghostfeed's avatar create/approve flow over MCP. Gather intent, generate drafts, let the user approve. Refined from real testing.
---

The tools enforce the hard rules server-side: drafts are never auto-saved,
traits are validated, every op is workspace-scoped, failed generations refund.
This skill shapes the conversation on top.

## The flow

1. Split identity from scene. Persistent identity goes in `traits` (gender,
   ageBand, heritage, faceShape, skinTone, skinTexture, hairColor, hairStyle,
   eyeColor, bodyBuild, outfitStyle). This-shot scene, pose, mood, and
   lighting go in `notes`. Omitted traits are randomized (gender-aware), so
   pass only what the user specified; when the brief has a register (brand
   ad, editorial), also set skinTexture and makeupStyle to match, because the
   dice do not read the brief. `notes` is a light vibe hint, not a scene
   contract: at creation the engine owns the scene, since these images are
   identity/base material and exact scenes are generated later from the
   avatar page. To iterate on a draft ("same person, but X"), copy the
   `traits` object echoed in the previous result and change only what the
   user asked; anything omitted re-randomizes on every call.
2. Name them yourself. Pick trait-appropriate `names` (one per draft); the
   server's auto-namer is trait-blind and once named an East Asian avatar
   "Luis Iqbal". Call `create_avatar` with the chosen `workspace` (`count` up
   to 4). `count` makes look
   variations of ONE trait spec, not different people; for distinct personas
   make one call each. If the user asks about quality or model options, call
   `list_image_models` and show the choices with per-image prices; otherwise
   the default model is fine.
3. Present the drafts. Summarize what you made and hand over the dashboard link
   so the user can see the faces and pick (the link ritual below).
4. The user chooses. Never approve on their behalf. Pass the same
   `workspace` to `approve_avatar` or `rename_avatar`. You cannot delete drafts;
   the user manages or discards the ones they do not want from the dashboard.

## Discovering options and ids

Trait fields are enums. Read them off the tool schema and offer them:
"heritage can be South Asian, East Asian, Black, White, Latino, Middle
Eastern, or Mixed." A wrong value returns `validation_failed` with the allowed
list; correct and retry.

To find a saved avatar's id (rename, content generation), use `list_avatars`.
Never guess ids; never scrape the dashboard.

Call `list_workspaces` first and keep the chosen workspace slug or id. Reads
may omit `workspace` and use the credential's pinned read default. Every
workspace-scoped write requires `workspace`; never infer it from whichever
workspace the user last opened in the dashboard. If two workspaces share a
name, retry with the stable slug or id.

## Money

`create_avatar` returns `creditsSpent` and `creditsRemaining`. Failures refund
automatically; a partial batch refunds the undelivered images. Creation bills
once: drafts never expire and cost nothing to keep. The balance is a shared
pool that teammates can move between your calls; `list_transactions` with
`mine: true` shows exactly what this connection spent.

End the reply with the money on its own line, numbers from the tool result:

```
💳 {creditsSpent} credits spent, {creditsRemaining} remaining
```

Free operations (approve, rename, lists) get no money line.

When a response carries `dashboardUrl`, end with the door on its own line
(after the money line if both apply), so the user can always click through
to what was made:

```
🔗 {dashboardUrl}
```

One link even for a batch: the keeper's, or the project's.
