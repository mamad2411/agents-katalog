---
name: bellingcat-osint
description: >
  Entry point for Bellingcat's OSINT toolkit. Maps entity types
  (ships, planes, people, emails, phones, photos, videos, domains, companies,
  social media, wildlife, munitions) to investigation categories and tools.
  Use when investigating any entity and need to find the right open source
  investigation tools, even if the user doesn't mention "OSINT" or "Bellingcat."
compatibility: Requires internet access to fetch tool detail pages from bellingcat.gitbook.io
---

# Bellingcat OSINT Toolkit — Navigator

## Entity Type → Investigation Category

| If investigating... | Category skill | Key tools |
|---|---|---|
| Ship / vessel / IMO / MMSI | `bellingcat-transport` | MarineTraffic, VesselFinder, Equasis, ShipFinder |
| Aircraft / flight / tail number | `bellingcat-transport` | FlightAware, Flightradar24, ADS-B Exchange, OpenSky |
| Person (name, email, phone, username) | `bellingcat-people` | Sherlock, Blackbird, Maigret, Have I Been Pwned |
| Photo / image | `bellingcat-image-video` | Google Lens, TinEye, InVID, PimEyes |
| Video | `bellingcat-image-video` | InVID, Azure AI Video Indexer |
| Domain / website / IP | `bellingcat-websites` | Wayback Machine, Shodan, urlscan.io, ICANN Lookup |
| Company / business / finance | `bellingcat-companies-finance` | OpenCorporates, EDGAR, ICIJ Offshore Leaks |
| Social media account | `bellingcat-social-media` | Platform-specific tools (see category skill) |
| Geographic location | `bellingcat-geolocation` | SunCalc, GeoHints, ShadowMap, Spot |
| Satellite imagery | `bellingcat-maps-satellites` | Copernicus Browser, NASA Worldview, Planet Labs |
| Map / street view | `bellingcat-maps-satellites` | Google Maps, Yandex Maps, Mapillary, KartaView |
| Conflict / weapons / munitions | `bellingcat-conflict` | ACLED, LiveUAMap, OSMP, Bulletpicker |
| Wildlife / environment / deforestation | `bellingcat-environment-wildlife` | Global Forest Watch, CITES, Wildlife Trade Portal |
| Archiving / preserving web content | `bellingcat-archiving` | Wayback Machine, Archive.today, Auto Archiver |
| Data analysis / visualization | `bellingcat-data-analysis` | 4CAT, Datawrapper, Gephi, Datasette |

## How to Use

1. Identify the entity type from the user's request
2. Load the matching category skill listed above
3. The category skill lists tools with brief descriptions
4. For detailed usage instructions, fetch the tool's guide:
   `https://bellingcat.gitbook.io/toolkit/more/all-tools/<tool-slug>.md`
