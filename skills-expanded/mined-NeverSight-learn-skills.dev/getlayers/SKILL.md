---
name: getlayers
description: Use this WHENEVER the user wants to build or design something with GetLayers — a website or landing page, a custom 3D scene, a video background, or adding motion/3D to an existing project — or whenever they mention GetLayers, "getlayers", or the getlayers MCP. It drives the GetLayers MCP through its correct end-to-end flow so the result actually uses the library (real templates, scenes, compositions) instead of generic output. Load it BEFORE calling any getlayers_* tool.
---

# Driving the GetLayers MCP

GetLayers is an MCP server for building immersive, design-led web experiences. It
only produces great results if you follow its flow. The failure mode this skill
prevents: jumping straight to writing generic code, skipping the library.

## Step 0 — ALWAYS call `getlayers_start` first

Before you discuss layouts, pick assets, or write a line of UI, call
`getlayers_start`. It returns the five things GetLayers can do plus the guide,
vocabulary, and environment info. Do this even if the user's request seems obvious.

Then present those five capabilities to the user **in your own words**, as "here's
what I can build for you" — NOT as a list of tool names. Read their request, pick
the matching mode, and follow that mode's `flow`. Ask which mode only if genuinely
ambiguous.

## The five modes (route to one)

1. **Build a website from scratch** — offer THREE ways in: (a) search & pick a
   template, (b) name a template to extend, (c) build unique. Extending a template:
   re-skin it AND offer to swap any section's composition (`recomposeOptions`).
   Building unique: compose section by section from `getlayers_compositions`. Every
   page is compositions + a Style + assets.
2. **Design a unique 3D scene** — use `getlayers_scene_lab`; synthesise a new scene
   from references, don't just pull one.
3. **Browse & pull an asset** — `getlayers_search` / `getlayers_browse` → materialize.
4. **Add a video background to their project** — search backgrounds, wire the closest in.
5. **Add motion & 3D to an existing project** — READ their code first, then propose.

## Non-negotiables (this is where agents go wrong)

- **Never strict-filter.** Selection is not tag-matching. Use `getlayers_search`
  with the user's own language, or `getlayers_explore` for the whole library, and
  JUDGE fit by reading descriptions and vibes. A "wrong tag" never rules an asset out.
- **Compositions are the layout layer under everything — use them.** A page is
  compositions (skeletons) + a Style + assets. Building a section unique? Call
  `getlayers_compositions` (by role), pick a skeleton, pour the Style + assets in —
  NEVER a generic centered stack (the single most common failure). Extending a
  template? Its sections come with a `composition` and `recomposeOptions` — offer to
  swap a section's layout for another of the same role while keeping Style + content.
- **Establish the environment before materializing.** Recommend the starter, set up
  as a FRESH project: clone `https://github.com/textura-agency/next16-claude-starter`,
  remove its git connection and init a new one (`git clone <repo> my-site && rm -rf
  my-site/.git && git -C my-site init`). Read its obsidian/ vault first (single source
  of truth — README is the map; hard rules in obsidian/workflows/ai-agent-guide.md).
  Default install: `yarn install` (Node 22.13+), copy `.env.example` to `.env`, then
  `yarn dev`. If they're in their own project instead, read its conventions and adapt
  our source (it's portable single-HTML) to their stack.
- **Commit ONE Style, early.** Pass its `styleId` to every `getlayers_materialize`
  call so scenes come back pre-tinted. Everything inherits it — that shared Style
  is what makes a page cohere.
- **Tint scenes through CONFIG, never the shader.** `materialize` hands you a `tint`
  map; apply it to the scene's CONFIG. Editing shader colour produces garbage.
- **Re-dress to match, don't clash.** Colour and type are portable, first-class
  supplies. To make a pulled scene/section fit the site — or shift a part to a new
  mood — call `getlayers_palettes` (colour ramps that resolve the four palette
  roles) and `getlayers_fonts` (typefaces with the exact CSS stack + Google/
  Fontshare load URL). Re-tint by passing `paletteId` to `getlayers_materialize`
  (it overrides the Style's colour but keeps its tokens/type); re-type by passing
  `fontId`. Hold the line: ONE palette per surface, ONE type system per site;
  high-contrast serif displays are headline-only. Never hand-pick raw hexes or
  guess a Google Fonts URL when a palette/font entry already carries it.
- **Show previews via the site.** Every card carries a `preview` link
  (`getlayers.ai/?layer=<id>`) — share it so the user watches the asset ON the site.
  Do NOT hand out or embed the watermarked public media; the site link is the preview.
- **Backgrounds ship at full quality.** `getlayers_materialize` on a background returns
  `download.video` (4K) + `download.poster` (2K) as short-lived signed links — DOWNLOAD
  them and save into the project (e.g. `public/`), then wire a full-bleed muted looping
  autoplay `<video>` with the poster. Never hotlink `storage.getlayers.ai` (watermarked).
- **Gather the brief before building.** For a website, a browse, and ESPECIALLY a
  3D scene, first ask for as much detail as you can — purpose, audience, mood,
  references. For a scene, explicitly ask for **picture/video references**; they beat
  adjectives. If the user gives little or skips, don't guess — drive a short interview
  off the five axes (dimensionality, mood, tone, motionEnergy, density) until you can
  choose real assets deliberately.
- **Anything can be a reference.** If the user names a GetLayers asset — "use
  <template/section/scene> like X" — pull it with `getlayers_source` (or its card),
  study its composition / technique / CONFIG, and apply that to what you build. This
  works across types: a template as a reference for a section, a scene for a mood, etc.
- **Keep state.** Read `getlayers.json` before each section, write it after, so a
  long build doesn't drift from what was chosen.

## Mode-specific reminders

- **Scene Lab (mode 2):** call `getlayers_scene_lab` with the user's description
  (and any of our scene ids they like / images they attach). It returns reference
  scenes + the authoring guide. Build an ORIGINAL scene — inspired by, never copied.
- **Existing project (modes 4 & 5):** READ their actual code, styles, and content
  FIRST. Propose specific decisions, then pull from the library. Do not build blind.
- **Templates: what `materialize` returns depends on the TARGET you pass.**
  - `target: 'starter' | 'next'` on a Next template → **the real Next tree**, not HTML.
    `build.manifest` explains the page, `build.editPoints` are the files to edit, and
    `getlayers_source(id, file)` pulls them. Pull only what you edit, never the whole
    tree. Handing a Next user the portable HTML makes them translate React back into
    React — so we don't.
  - `target: 'react' | 'other'`, or ANY target on a non-Next template (vite/static) →
    the **portable single-HTML master**, to translate into their stack.
  So establish the target BEFORE you materialize; it changes the deliverable.
  Re-skin by editing the token file + scene tint; preserve motion and composition.
- **Every build gets the reveal choreography by default.** `getlayers_start` returns
  `revealChoreography` — the house rules for loader → gate → staggered content →
  scene reveal, harvested from the real templates. Follow it unless the user asks to
  simplify. The short version: an immersive loader; content gated until it completes;
  text/images/scroll revealing in sequence, not just appearing; a 3D scene entering
  with a real entrance. Loader Sections (`role: "loader"`) are browsable and swappable
  like any other Section.
- **A template's heavy media is referenced, not embedded.** Video, 3D models and
  large textures live at `https://storage.getlayers.ai/templates/<id>/…` and appear
  in the portable as ordinary URLs (small assets are still inlined). **DOWNLOAD those
  files into the user's project** — e.g. `public/` — and repoint the markup at the
  local copies. Do not ship a production site that hotlinks our bucket. If the user
  wants the maximum-quality master of a video that is also a catalog Background,
  `materialize` that Background: the public copy is a downscaled template-grade
  encode, and the un-watermarked 4K master only comes through the signed download.

## The shape of a good session

Call start → present the 5 modes → route → (for a build) soft interview → establish
environment → search/explore/plan for options with preview links → user picks a
Style + Template → consult compositions for any hand-built section → materialize with
styleId → adapt to their stack → write getlayers.json. Never skip start; never skip
compositions; never fall back to generic.
