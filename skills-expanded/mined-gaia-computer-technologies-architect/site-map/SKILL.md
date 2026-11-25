---
name: site-map
description: Makes a figure-ground and a context map of a site from OpenStreetMap (or a GeoJSON the architect already has), covering buildings, streets, green space, water and the site boundary, with a scale bar, north point and ODbL attribution, measures site area and building coverage in a projected coordinate system, and labels every OSM building height as tagged, assumed or unknown. Outputs PNG and SVG, plus an optional DXF base in local metres. Use when the architect wants a "figure-ground", "site location plan base", "context map", "Nolli plan", "urban grain study", "site plan from OSM", or "how big is this site". Hands its facts to site-context for the design reading and to massing-study for neighbouring heights.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Site Map

Get from an address to a usable context base in a few minutes: a figure-ground that shows the urban grain, a context map with streets, green space and water, and a site area measured properly. Everything is drawn from OpenStreetMap, which is excellent in some cities and patchy in others. The skill says which.

## When to use

- At the start of a project, for the urban-grain read and the base for site-analysis diagrams.
- For a quick site area and coverage figure before a survey exists.
- For a CAD base (DXF) to sketch over, until a measured survey arrives.

## Input

- A location: **lat/lon** (decimal degrees) and a radius in metres (20 to 1,500 m). If the architect gives only an address, geocode it with a tool you actually have and show them the coordinates to confirm. Never guess coordinates for an address.
- Optionally, the **site boundary** as a GeoJSON polygon (WGS84), drawn from a title plan, a survey, or traced on a web map. Without it there is no site area, only context.
- Offline alternative: a **GeoJSON** of context features with OSM-style tag columns (`building`, `highway`, `height`, `building:levels`, `leisure`, `landuse`, `natural`, `waterway`).

## Process

1. **Confirm the point** (and the boundary, if given) with the architect before fetching.
2. **Run the script.**
   `uv run scripts/site_map.py --point LAT LON --radius 250 --site site.geojson --out out/site --dxf`
   or offline: `uv run scripts/site_map.py --geojson context.geojson --site site.geojson --out out/site`
   It fetches from the public Overpass API through OSMnx, which caches responses in `./cache`. A 150 to 250 m radius usually takes under a minute. If Overpass is busy or rate-limited, the script refuses with the error. Wait and retry, or use `--geojson`.
3. **Check the images.** Is the site outline where the architect expects it? Are there obvious holes in the building footprints? Missing buildings are common in suburbs and small towns. If coverage looks thin, say so plainly.
4. **Report the numbers with their basis.** Every area is computed in the UTM zone the script picks (printed as an EPSG code), never in degrees. Site area comes from the supplied boundary, not from OSM.
5. **Hand over** the figure-ground, context map, optional DXF, the report, and the attribution line. Then hand to `site-context` for what it means for the design.

Geocoding options, Overpass etiquette and QGIS/MCP notes are in [references/tool-notes.md](references/tool-notes.md).

## Domain knowledge

- **Figure-ground** (a Nolli plan): buildings black on white, nothing else. It shows grain, block size, permeability and where the open space is. Read it for the pattern the new building joins or breaks.
- **Projected CRS.** Areas measured in latitude and longitude are wrong. A degree of longitude shrinks towards the poles. UTM keeps area error well below what matters at site scale. The DXF is written in local metres with the UTM origin recorded on the drawing, so it can be re-registered later.
- **North.** The north point shows grid north of the UTM projection, which differs from true north by up to a couple of degrees away from the zone's central meridian. That's fine for a context map. For solar work or a drawing that will be issued, take north from a survey.
- **OSM heights are not data you can design to.** Usually only a minority of buildings carry a `height` tag, even in well-mapped cities. The script counts them for the area you fetched, so quote that count. `building:levels` times an assumed floor height (3.0 m by default; set `--floor-height`) is labelled ASSUMED. Everything else is UNKNOWN. Treat all of it as indicative for massing, never for rights-of-light, daylight or overshadowing assessments.
- **Completeness varies.** OSM is volunteered. Some dense, well-mapped cities are close to complete. Rural areas, informal settlements and newly built areas can be badly incomplete. Judge from the image, not from a reputation. Coverage percentages inherit that.
- **Licence.** OSM data is under ODbL 1.0. Any map using it must credit "(c) OpenStreetMap contributors". The script draws the credit on every image and puts it in the DXF. Don't crop it off.
- **Better sources exist locally.** National mapping agencies (Ordnance Survey MasterMap in the UK, Kadaster BGT and 3D BAG in the Netherlands, IGN in France, city open-data 3D models, county GIS in the US) are often more accurate and sometimes free. Recommend them for anything beyond early-stage work. Don't claim a dataset exists for a place unless you have checked.

## Output format

```
## Site map: [name]

Files: site_figure_ground.png/.svg, site_context.png/.svg, [site.dxf]
Source: OpenStreetMap via Overpass, [radius] m around [lat, lon], fetched [date]  |  CRS: EPSG:[code]

| Measure | Value | Basis |
|---|---|---|
| Site area | 9,181 m2 (0.918 ha) | supplied boundary, projected; not a survey |
| Site perimeter | 384 m | supplied boundary |
| Building coverage in radius | 49% | OSM footprints; completeness [good / patchy / poor] |
| Context heights | 6-43 m | 7 tagged, 7 assumed (levels x 3.0 m), 22 unknown |

Reading of the grain: [two or three sentences: block size, street pattern, open space]
Gaps: [missing buildings, odd tags, what to get from a survey or national mapping]
(c) OpenStreetMap contributors, ODbL 1.0
```

## What you don't do

- Don't invent coordinates, boundaries or heights. An address with no confirmed point means no map yet.
- Don't present a site area from a traced boundary as the legal or surveyed area. Title, survey and planning areas can differ.
- Don't use OSM heights for daylight, rights-of-light or overshadowing conclusions. They need measured data and a qualified assessor.
- Don't strip the ODbL attribution.
- Don't hammer the public Overpass servers: keep the radius sensible and reuse the cache.
