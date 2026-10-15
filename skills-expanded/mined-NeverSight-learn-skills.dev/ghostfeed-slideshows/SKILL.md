---
name: ghostfeed-slideshows
description: Build TikTok photo slideshows over MCP as the art director. Start a blank deck, search and cast every background, write the text, review, hand over the link. Refined from real founder dogfooding.
---

The tools enforce the hard rules server-side: image picks are gated (browser-
displayable, 720px+ on the short side), text is positioned into TikTok's safe
zones for you, every op is workspace-scoped. This skill makes you the art
director on top.

You build the deck slide by slide, and that is deliberate. The server has a
one-shot composer, but it runs on a small vision model with a limited viewing
budget, so YOUR vision beats it: you search, LOOK at real candidates, and place
every background and text box yourself.

Three ways to start, all the same hand-build: from an idea (the flow below),
from a TikTok or Instagram link (Remixing), or as a variant of an existing deck
(Variants).

## The flow

1. Start a deck. `create_blank_slideshow` with the required `workspace` and a
   `slideCount` (add or remove later with add_slide / remove_slide, cap 12). It
   returns the slideshow id you edit against.
2. Cast each background. For every slide, `search_pinterest` (up to 8 queries)
   for SCENES, not topics: a real moment someone photographed, never the topic
   or concept words, which fetch infographics and stock. Then LOOK at the
   returned urls yourself before choosing; that is the whole point.
   `set_slide_background` with the winner. A pick under 720px on the short side
   is rejected, so choose another.
3. Write the text. `set_slide_texts` with 1 to 5 texts, each carrying a `role`
   (heading, subheading, body, cta; role sets the size) and a `placement` (top,
   center, bottom). Positions are computed server-side into the safe zones, so
   you give the words and the role, never coordinates.
4. Caption and review. `set_caption` for the post caption. Read the deck back
   with `get_slideshow` (each slide's texts and `backgroundSource`), summarize
   the arc in a sentence or two, and hand over the dashboard link. The dashboard
   updates live as you build, so do not tell the user to refresh.

## What makes a deck good

The tools gate the floor (nothing blurry, tiny, or outside the safe zones
ships); the taste is on you. Three things carry it.

- Judge every image by the camera-roll test: could a real person have shot
  this? YES to candid mid-action subjects who ignore the camera, film or flash
  light, lived-in imperfect rooms. NO on sight to any baked-in text or designed
  layout, stock posing (a model smiling at the lens), brand logos or watermarks
  (check the corners), pixelation, or waxy AI-render perfection. Use a distinct
  scene per slide and vary the setting and light across the deck.
- Write copy that stops the scroll. The heading is one short punchy line (about
  3 to 6 words), usually ALL CAPS. The body scales with what the slide carries:
  10 to 40 words, the fuller end when the slide has a fact, number, mechanism,
  step, or reason (give the "why", not a restatement of the heading), the lower
  end for a vibe beat. Never pad, and never truncate a useful explanation just
  to stay punchy.
- Build an arc, not a list: a hook slide that earns the swipe, body beats that
  pay it off, at most ONE soft product plug in a peer-recommendation voice (no
  "buy" or "click"), and a closer.

## Remixing a TikTok or Instagram post

When the user gives a TikTok Photo Mode or Instagram carousel link, `read_social_post`
returns the source caption, slide count, and each slide's image url. That is the
SOURCE, not your deck: LOOK at the images and read the caption to grasp the
structure and voice, then hand-build the remix through the flow above. Match the
beat structure, but write your OWN copy (never copy verbatim) and cast FRESH
images. Decks cap at 12 slides: if the source carousel has more than 12, condense
to at most 12 (merge or drop the weakest beats) rather than truncating. A remix is
a normal Studio build, so it costs the same 1 credit on your first build edit.

## Variants (A/B versions of a deck)

`create_variant` returns a COPY of the base deck with a new `variantIndex`. You
turn it into an A/B the same way the dashboard's Director shuffles a variant,
except you do it with your own eyes. After `create_variant`, walk every slide
and pass the `variantIndex` to differentiate it:

- Pinterest slide: `search_pinterest` again and `set_slide_background` a
  DIFFERENT pick, a fresh scene, not the base image.
- Collection or avatar slide: `set_slide_background` a different image from the
  SAME collection or avatar (browse with the list tools).
- An uploaded, pasted-url, or AI-generated image: keep it as-is.
- Rewrite the copy on each slide with `set_slide_texts`: same beat, new words.

A variant costs 1 credit at `create_variant`, matching a dashboard-generated one.

## Casting the user's own images, products, and avatars

The user's own assets are cast the same way as Pinterest: browse, then place.

- Collections: `list_collections` to discover folders, `list_collection_images`
  to browse one, then `set_slide_background` (type collection) with an image you
  chose.
- Avatars: `list_avatars` for saved identities, `list_avatar_images` to browse
  an avatar's photo pool (a live source that includes frames from that avatar's
  own UGC videos), then `set_slide_background` (type avatar) to put the person
  on a slide.
- Products: `list_products` shows each product's `linkedCollections` (its own
  photos). Plug a product on ONE slide in a soft peer-recommendation voice:
  browse a linked collection and cast a real product image there.
- A local image file the user hands you: call `request_slide_image_upload` for a
  short-lived presigned URL, PUT the raw bytes to `uploadUrl` (never pass image
  bytes as a tool argument), then `set_slide_background` type `url` with the
  returned `fileUrl`. Any other external image url works with type `url` too and
  is re-hosted to our storage automatically so the slide never breaks; you do
  not need to upload a url that already points at a real image.

## Workspaces

Call `list_workspaces` first and keep the chosen slug or id. Reads may omit
`workspace` and use the credential's pinned read default. Every write requires
`workspace`; never infer it from whichever workspace the user last opened. A
typo fails with remediation listing the valid names, slugs, and ids.

## Money and link

Creating a slideshow costs the same whichever door builds it. When a response
carries `creditsSpent` and `creditsRemaining`, state them on their own line,
numbers from the tool result:

```
💳 {creditsSpent} credits spent, {creditsRemaining} remaining
```

Reads and lists get no money line. `get_credits` has the balance if the user
asks.

When a response carries `dashboardUrl`, end your reply with the door on its own
line:

```
🔗 {dashboardUrl}
```
