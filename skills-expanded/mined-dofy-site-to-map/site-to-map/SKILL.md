---
name: site-to-map
description: Create or edit a folded-paper 3D navigation map from a personal homepage, link-in-bio page, navigation site or bookmarks. Use when turning such content into a site-to-map page or changing an existing site-to-map world, towns, links or appearance.
---

# site-to-map

Converts a link-heavy site into the map used on yahaha.net: a generated paper-craft world
(coasts, islands, gulfs or lakes, mountain ranges, rivers and roads from a seed) with up to
nine towns, ink-line rendering, local-time daylight, multilingual text, tour mode and
keyboard shortcuts. Forests mix tree shapes, peaks vary between snow, rock and vegetation,
and birds, boats and small schools of fish add life where the world permits. You write one
`site.json`; the engine in `engine/` does the rest.

Read `references/site-schema.md` before writing `site.json`, and pick building shapes from
`references/kinds.json`. The schema file contains a complete annotated example, and
yahaha.net's production config (`src/data/map.json` in dofy/yahaha) is a full one to copy from.

## Edit an existing map

Locate the existing map configuration and integration before editing. Change only what the
user requested; preserve other links, languages, names and world settings. A framework
integration may use a different filename (yahaha uses `src/data/map.json`) and may vendor
the engine rather than use the standalone builder. Respect the project's own workflow.

Changing the seed, town count or slots can change the generated land; with `townSize: "fit"`,
building count changes can also shift it. Explain material layout changes to the user. For a
standalone page, rebuild from its configuration; for an integrated page, validate the actual
integration. Check the affected views and screenshots when the change is visual.

## Create a map

1. **Get the source.** Ask for a URL, an exported bookmarks file, or a pasted list if the
   user has not given one. For a URL run
   `node scripts/extract.mjs <url> extract.json` from this skill's folder. If `node_modules`
   is missing there, run `npm install` in that folder first. Playwright renders client-side
   sites and is needed by `check.mjs`; the static HTML fallback cannot render them. Read the result: every
   section has `heading`, `parent` (the h2 it sits under), a little `text` and its `links`.
   Open the page yourself if the extract looks thin.
2. **Plan the towns.** Group links into **three to nine towns**, usually one per top-level
   category. Merge tiny categories; five is the sweet spot, and above six the world grows
   (up to ×1.8 at nine) and the overview gets busier.
   - **The user's structure wins.** If the user names a number of towns or a grouping
     ("four towns", "merge A and B", "one town per tag"), follow it exactly within the 3–9
     range, even where you would have grouped differently; only say so if it forces
     something odd, such as a town of one link. Otherwise derive the towns from the site's
     own categories. For a flat list without categories, group by what the links are, and
     tell the user which groups you made.
   - Drop in-page anchors, share buttons and duplicate links. A link that appears in two
     categories goes in the one where it means most; a short mention elsewhere can stay
     as a prop.
   - Up to **nine buildings** per town. Everything beyond that, and anything minor, becomes
     a **prop** (tree, rock, signpost, flower bed, statue, lamp…). Props are clickable and
     named like buildings, and sit in a ring just outside town. Do not drop links to fit.
   - Choose a role (`slot`) for each town by character; the first five are unique, `town`
     can repeat for the sixth to ninth:
     `center` walled main town (the core category) · `coast` harbour with piers and a
     lighthouse (things that ship: apps, products) · `south` workshop quarter (code,
     side projects) · `east` market town with a fountain (social, contact) ·
     `highland` quiet plateau with a gate and waterfall (small or special sets, best ≤ 4) ·
     `town` any further town on open land.
3. **Name things.** Default to **original names** that fit the owner and the site:
   town names, the world name, and the nine place-name anchors (mountains, two rivers,
   forest, fields, sea, bay, western range, lake). Use a borrowed setting (Tolkien, a
   game, a film) only when the user asks for it, and say that it is fan naming. Give
   user-facing strings in the site's own language as plain strings, and set `site.lang`
   to its code. **Do not translate** and do not add other languages, even if the source
   site is multilingual: convert the main language only, and tell the user that other
   languages can be added by hand (see `references/site-schema.md`, *Languages*). The
   interface has built-in Simplified Chinese, Traditional Chinese, Japanese and English;
   for any other language, also write its interface strings in `text.<lang>` (keys listed
   in the schema). Keep proper nouns as the
   owner writes them.
   - Number keys 1–9 reach towns by link count, largest first (ties keep their configured order). Town `key` (only used with `ui.shortcuts`): one letter, ideally the initial of the
     English name, unique, and not `H O T V L I` (overview, orbit, tour, top view,
     language, info card).
4. **Pick shapes.** Read `references/kinds.json` and choose a distinct building `kind` for
   each link in a town by what it *is* (a bot → `dovecote`, an IP tool → `radio`, a blog →
   `scriptorium`). Compare both the `silhouette` field and overview screenshots: different
   kinds can all read as the same gabled house or tower. Mix open, round, low, object and
   taller silhouettes where they fit the links; do not chase variety by misrepresenting an
   item. Address builder warnings and check each town at overview and close-up, in daytime
   and at night. Repeat a kind only for a deliberate reason, or when explicitly requested;
   preserve kinds already chosen by the site owner. Vary prop kinds too. If a kind is omitted,
   the engine balances silhouettes deterministically but cannot infer the item's meaning;
   explicit kinds are never rewritten.
   Descriptions are one short line taken from the source, not invented claims.
5. **Shape the world.** The land is generated from `world.seed` (default: brand + town
   ids), so every site gets different coasts, mountains, rivers, lakes and roads. Pick a
   `world.type` that suits the site (`coast`, `twoCoasts`, `island`, `gulf`, `lakeland`) or
   leave it to the seed. Build an initial page with `node scripts/build.mjs site.json out/`,
   then try two or three seeds with
   `node scripts/check.mjs out/ --query "seed=foo&world=island"` and keep the one where the
   towns read best; **write that seed into `site.json`** so renaming the site never
   reshuffles the land. For a site on several domains, `"seed": "{domain}"` gives each domain its own
   land. Keep `townSize` at its default `fixed` unless the user wants towns
   packed tighter and accepts that adding buildings may move things (`fit`). `layout: "classic"`
   reproduces the legacy fixed five-slot continent.
6. **Style each town.** `style.walls` and `style.roofs` are palette tokens (see schema);
   give each town its own roof family so towns read apart, and set `features`
   (`walls`, `hedge`, `lamps`, `centerpiece`).
7. **Build and look.** `node scripts/build.mjs site.json out/` writes a standalone
   `out/index.html` (three.js and fonts from CDNs). Then `node scripts/check.mjs out/`
   writes to `out/_check/`: the overview and every town at 10:00 and 21:00, a phone view,
   `sheet.png` with all of them on one page and `report.json`. It also checks that the
   held frame is deterministic, that reduced motion holds still, that the page does not
   scroll sideways on a phone and that the no-WebGL fallback shows. Add `--finishes` to
   shoot every finish, `--finish <name>` to check in one, `--hours 9,19` for other hours
   and `--quick` (overview and phone only) when comparing seeds. Exit code 1 means a
   problem; notes (hidden labels, frame cost) are questions. **Open `sheet.png` and look**:
   passing checks do not make a readable map. Shorten names or move items to props when a
   town is crowded, rebuild, and check once more. Never say the look is done without
   opening the screenshots; without a browser, say the look is unverified.
8. **Deliver.** Hand over `site.json`, the built folder and the screenshots. Tell the user
   what you merged, dropped or turned into props, and which names you invented.

## Options

Everything below is optional and set in `site.json` → `ui` (defaults in brackets). Use the
defaults unless the user's request or the existing map calls for another setting.

| option | default | what it does |
|---|---|---|
| `languageSwitch` | off | language button and `L` key, cycling through available languages; enable when multiple languages are present and wanted |
| `shortcuts` | off | 1–9 and town letters, ↑/↓ to switch towns, ←/→ to switch buildings in a town, Enter, +/−, T/O/V/I, the `?` help panel and its hint. `Esc` (back) and Shift/Space + drag (pan) always work |
| `tour` | on | Tour button that flies through every town |
| `views` | on | Orbit and Top view buttons |
| `clock` | on | time-of-day chip in the footer |
| `compass` | on | compass in the corner |
| `daylight` | `"auto"` | local-time sky, lighting and shadows update every 20 seconds; a number (e.g. `10.5`) freezes the hour |
| `intro` | on | pop-up-book entrance animation |
| `motion` | on | boats, walkers, smoke, flags and clouds moving |
| `blur` | on | depth-of-field and tilt-shift blur (off in the `pixel` finish) |
| `finish` | `"paper"` | rendering style over the same world: `paper` (ink lines on paper), `blueprint` (blue planes, pale edges, drafting grid), `halftone` (warm and cool ink dots on ivory), `pixel` (3 px grid, 2 px on phones, ordered dither). Set only when asked; preview with `?finish=` |
| `infoOpen` | on | info card open at start on wide screens; phones and tablets show a selection bubble |

On phones and tablets, the city navigation button opens a list of towns. Selecting a town or
building displays a compact information bubble; buildings include an open-link button.

The opening camera angle is chosen by the world generator: from the sea looking inland
when there is an open coast, otherwise from opposite the main mountain range, nudged so no
peak stands between the camera and a town. The Map button (and `0`/`H`) returns to that
angle, the overview zoom and tilt, and switches orbit, top view and tour off.

Other things that are optional simply by leaving them out: `site.links` (a few site-level links beside the brand, such as GitHub or contact, each
with a name, URL and icon; add them only when the source site shows such links prominently),
`site.copyright` (footer line), `site.version` / `site.releaseUrl` (version link), `places`
(map lettering), town `features` (walls, hedge, lamps, centrepiece, suburbs) and `world`
(land generation, see step 5). `?t=18` previews an hour, `?seed=` / `?world=` another
world and `?finish=` another finish without editing the file. `?still` (or `?still=8`)
holds boats, walkers and smoke at that second and skips the entrance and camera flights,
so screenshots and posters are reproducible; `check.mjs` always uses it.

## Integrating into an existing site

The standalone build is enough for most people. To embed in a framework (Astro, Next,
Vite): copy `engine/map-engine.js`, `world-gen.js`, `daylight.js` and `map.css` into the project, inline
`daylight.js` as a plain script in `<head>` (so the first paint has the right time-of-day colours), install
`three@0.170.0`, render the markup from `engine/template.html` (everything inside `<body>`),
and call `mountMap(site)` from a module script. Self-host the fonts there
(Manrope, JetBrains Mono, Cormorant Garamond italic) instead of Google Fonts. yahaha.net
is the reference integration.

## Rules

- Never invent links, people or claims; every `url` and description comes from the source
  or from the user.
- Keep the owner's copyright line and brand; `site.copyright.owner` is required for a
  personal site.
- Links to the site's own pages use root-relative paths (`/tools`, not
  `https://example.com/tools`), so the map works on every domain, preview deploy and
  localhost the site is served from. `extract.mjs` already writes same-origin links this way;
  keep them relative and strip the scheme and host from any the user pastes. Subdomains
  and other domains are separate sites and stay absolute.
- Email links stay as `mailto:`; private or login-only links are left out unless asked.
- The page needs WebGL. The build always writes a `<noscript>` link list, so content stays
  reachable without JavaScript.

## Limits

- Up to nine towns (more than five makes the world larger), nine buildings each; any
  number of props, but more than about twelve per town gets crowded. `layout: "classic"`
  has only five spots.
- The world is generated, not painted: you choose a seed and a type, not exact coastlines.
  Fewer towns simply leave more countryside.
- Building shapes come from the catalogue. A link that deserves a one-off landmark needs a
  new kind added to `engine/map-engine.js` (`makeBuilding`) and `references/kinds.json`.
