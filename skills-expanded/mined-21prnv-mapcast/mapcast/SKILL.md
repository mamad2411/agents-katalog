---
name: mapcast
description: Make animated map videos and images where countries are highlighted on real satellite imagery or an old paper map, with a tracing border, colour fill, flag, glow, label, capital marker or data-driven colours, the look of documentary and explainer YouTube videos. Use when the user asks for a map animation, a country highlight, "show <country> on a map", a map for a video/Short/Reel, a flag map, a historical/parchment map, or a map coloured by data (GDP, population, ...).
---

# mapcast: animated country maps

mapcast turns a small JSON **scene** into an MP4, GIF, PNG or JPG. You write the scene; a fixed renderer
does the drawing, so the look stays consistent. Never draw maps by hand or write your own map code for these requests.

## 1. Pick how to run it

- **MCP tools available** (`render_map`, `preview_map` from the `mapcast` server): use them. Pass the scene as an
  object, not a string.
- **Otherwise use the CLI** (Node 20+, ffmpeg and Playwright Chromium required):
  ```bash
  npx -y mapcast render scene.json -o out/map.mp4     # video
  npx -y mapcast render scene.json -o out/map.png     # still of the final frame
  npx -y mapcast schema                               # every option, as JSON Schema
  ```
  Write the scene to a file first, and type the command out in full each time (a command stored in a shell
  variable breaks in zsh). If `npx` cannot find the package, ask the user where mapcast is checked out
  and run `node <checkout>/bin/mapcast.js` instead. The first run downloads map data (about 40 MB, cached in
  `~/.cache/mapcast`). If it reports that Chromium is missing, run `npx playwright install chromium` once.

## 2. Write the scene

Start from the smallest scene and add only what the request asks for. The defaults are tuned to look good.

```json
{ "highlights": [{ "country": "India" }] }
```

That alone gives: satellite basemap, slow push-in, white glowing border that traces itself on, red fill that keeps
the terrain visible, "INDIA" rising in, 5 seconds at 1920x1080.

Map the request to fields:

| The user says | Set |
|---|---|
| a colour ("in green", "gold") | `highlights[].color` |
| "with its flag", "flag colours" | `style: "flag"` |
| "everything else dark/grey", "spotlight" | `style: "highlight"` |
| "just the outline/border" | `style: "outline"` |
| "old map", "history", "parchment", "medieval" | `basemap: "paper"` |
| "from space", "spinning globe", "dive in from Earth" | `camera: "globe"` (7 s default) |
| "zoom in from far away / from the region" | `camera: "zoom-in"` |
| "tour", "travel from X to Y", "visit A then B" | `camera: "fly"`, highlights in visiting order |
| a state or province ("California", "Kerala") | `region: "California"` instead of `country` |
| "no movement" | `camera: "static"` |
| Shorts, Reels, TikTok, vertical, phone | `aspect: "9:16"` |
| Instagram post | `aspect: "4:5"` (or `"1:1"`) |
| "mark the capital" | `capital: true` (the official capital: Ankara for Turkey, Brasília for Brazil) |
| "show Mumbai / Istanbul / any city" | `capital: "Istanbul"` (any city in that country) |
| "cinematic", "like a documentary" | `effects: { "blur": 0.7, "grid": true }` |
| "typewriter text" / "letters spreading" | `labelAnim: "type"` / `"spread"` |
| "no text" | `label: false` |
| a second line ("India, 1.4 billion people") | `label: "INDIA\n1.4 BILLION"` |
| several countries | several `highlights`, colours assigned automatically |
| "compare by GDP/population/..." | `data: { values, title, unit }` (see below) |
| "show neighbouring borders" | `effects: { "borders": true }` |

Full field list: [references/scene-format.md](references/scene-format.md). Worked examples for 27 common requests:
[references/examples.md](references/examples.md). Read the examples file when a request combines several options.

### Data maps

`data.values` maps country to number and adds a legend:

```json
{ "data": { "title": "Population (millions)", "unit": "M", "scheme": "blues",
            "values": { "India": 1441, "China": 1425, "United States": 341 } } }
```

- Show the numbers on the map with `"labels": "value"` (just the number) or `"labels": "both"` (name over number).
  `prefix` and `unit` are added to every number shown, on the map and in the legend (`"unit": "%"` gives "11.4%").
- Pick the scheme from what the number means: `reds` or `heat` when high is bad (unemployment, emissions),
  `greens` or `blues` when high is good or neutral (GDP, population), `diverging` for values around zero (growth).

Only use numbers the user gave you or that you can cite. If you look figures up, tell the user the source and year.
Never make up values to fill a map.

## 3. Check before the full render

Rendering a video takes 10-60 seconds, so look at one frame first:

- MCP: call `preview_map` and look at the returned image.
- CLI: render `out/preview.png` and open it with your image-reading tool.

A still shows the **final** frame. To check motion, also look at an early moment: `--at 0.5` on the CLI or
`"at": 0.5` in `preview_map` (with `camera: "zoom-in"` that frame should show a wide view of the region).

Check: is the right country highlighted, is the label readable and inside the country, are colours what was asked.
If a label spills out of a small country or is too small to read, set `labelSize` on that highlight (0.7 to shrink,
1.3 to enlarge), shorten the text (`label: "UAE"`), or drop it (`label: false`).
Adjust the scene and preview again if needed, then render the video.

## 4. Deliver

Report the output path, size and length (the CLI prints them; MCP returns them), and the **credit line** mapcast
prints, for example "NASA Blue Marble (public domain, via NASA GIBS)". That line is the complete imagery credit;
tell the user to include it where they publish. Sentinel-2 imagery (used for close zooms) legally requires it.
For data maps, the data source is separate: name where the numbers came from so the user can credit it too.

## Things to know

- **Disputed borders:** by default mapcast draws borders the way the highlighted country officially does
  (`pov: "auto"`), so India includes all of Kashmir and China includes Aksai Chin. If the user wants a neutral or
  another country's view, set `pov` to `"default"` or a code such as `"pak"`, `"chn"`, `"ind"`. Mention this when a
  highlighted country has disputed borders (India, Pakistan, China, Israel and Palestine, Morocco and Western Sahara,
  Cyprus, Serbia and Kosovo, Russia and Ukraine, Taiwan). When two of these appear together, `pov: "default"` is
  the neutral choice.
- **Country names:** common names and ISO codes work ("UK", "USA", "South Korea", "IN"). On "Unknown country",
  try the official name or the ISO 3-letter code.
- **States and provinces:** `region` takes a name in English or the local language ("Bavaria" or "Bayern") or an
  ISO 3166-2 code ("US-CA"). If a name exists in several countries, add `country`. Neighbouring state lines are
  drawn automatically. State borders are drawn as each country controls them, so `pov` does not change them.
- **Globe:** it uses satellite imagery; with `basemap: "paper"` mapcast zooms in from a wide view instead.
- **Not supported yet:** districts and cities as areas, routes or arrows between places, custom basemaps or video
  backgrounds. Say so plainly rather than approximating with something else.
- Errors from mapcast are written to be fixed: read the message, correct the scene, retry.
