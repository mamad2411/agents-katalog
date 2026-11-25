---
name: bellingcat-geolocation
description: >
  Determine where a photo, video, or description was taken. Analyze shadows,
  sun position, terrain, and infrastructure to pinpoint locations. Use when
  the user needs to geolocate an image, find a place, or verify coordinates,
  even if they don't mention "geolocation" or "OSINT."
compatibility: Requires internet access to fetch tool detail pages from bellingcat.gitbook.io
---

# Bellingcat Geolocation Tools

Tools for determining the precise location where photos, videos, or descriptions were captured. Combine shadow analysis, sun position, and OpenStreetMap queries to narrow down locations.

## Choosing Tools

- Use visual-cue and shadow tools to narrow a location; use map and OpenStreetMap search tools to test a candidate location.
- Confirm a location with more than one independent clue or source.

## Tools

| Tool | Best for | Cost | Description | Guide |
|------|----------|------|-------------|-------|
| [GeoHints](https://geohints.com/) | A website that provides information about things like traffic lights, utility poles,… | Free | GeoHints is a website that provides information about things like traffic lights, utility poles, bollards etc. for di... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/geohints) |
| [GeoNames](http://www.geonames.org/) | The GeoNames geographical database covers all countries and contains over eleven million… | Free | The GeoNames geographical database covers all countries and contains over eleven million place names that are availab... |  |
| [Bellingcat OpenStreetMap Search](https://osm-search.bellingcat.com/) | A user interface to search OpenStreetMap data for features in proximity to each other. | Free | A user interface to search OpenStreetMap data for features in proximity to each other. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/openstreetmap-search-tool) |
| [Photo-Map.RU](http://photo-map.ru/) | Geotagged VK posts. | Free | Geotagged VK posts. |  |
| [ShadeMap](https://shademap.app) | A global simulation of mountain, building & tree shadows for a given date & time. | Partially Free | ShadeMap is a global simulation of mountain, building & tree shadows for a given date & time. Base data is free, but ... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/shademap) |
| [Shadow Finder](https://github.com/bellingcat/ShadowFinder) | To analyse shadows in source imagery, Shadow Finder maps all points on the earth where a… | Free | To analyse shadows in source imagery, Shadow Finder maps all points on the earth where a shadow of given length could... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/shadow-finder) |
| [ShadowMap](https://app.shadowmap.org/) | Global map of 3D buildlings and the shadows they cast at a specific time a day | Free | Global map of 3D buildlings and the shadows they cast at a specific time a day | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/shadowmap) |
| [Spot](https://www.findthatspot.io/) | A natural language interface for querying the OpenStreetMap database to find locations… | Free | A natural language interface for querying the OpenStreetMap database to find locations which meet the search criteria... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/spot) |
| [SunCalc](https://www.suncalc.org/) | Suncalc models the relationship between the date, time of day, the geographic location of… | Free | Suncalc models the relationship between the date, time of day, the geographic location of a place, and the position o... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/suncalc) |

## Investigation Tips

- Start with SunCalc to determine possible dates/times based on shadow length and direction
- Use ShadowMap or ShadeMap to simulate shadows for a specific date/time at a candidate location
- GeoHints provides regional visual cues (traffic lights, utility poles) to narrow down countries
- Spot and OpenStreetMap Search let you query OSM features near coordinates using natural language
- Combine multiple tools to cross-verify: SunCalc for sun position, GeoHints for regional clues, OSM for feature proximity
