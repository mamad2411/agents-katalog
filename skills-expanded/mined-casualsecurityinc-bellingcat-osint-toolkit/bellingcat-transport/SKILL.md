---
name: bellingcat-transport
description: >
  Track and investigate ships, aircraft, trains, and vehicles. Monitor vessel
  movements (AIS), flight paths (ADS-B), rail networks, and license plates.
  Use when the user mentions a ship name, IMO/MMSI number, flight number,
  tail number, aircraft registration, vehicle, or train, even if they don't
  mention "transport" or "OSINT."
compatibility: Requires internet access to fetch tool detail pages from bellingcat.gitbook.io
---

# Bellingcat Transport Investigation Tools

Tools for tracking and investigating ships, aircraft, trains, and vehicles using AIS, ADS-B, and other data sources.

## Choosing Tools

- Start with the strongest identifier available, such as an IMO/MMSI, tail number, flight number, or registration plate.
- Compare tracking sources and normalize timestamps before inferring a route, ownership, or event.

## Tools

| Tool | Best for | Cost | Description | Guide |
|------|----------|------|-------------|-------|
| [ADS-B Exchange](https://globe.adsbexchange.com/) | Live flight tracker (including many miltiary aircraft). | Free | Live flight tracker (including many miltiary aircraft). Live data available for the past month. Historical data avail... |  |
| [Airframes](http://www.airframes.org/) | A database of aircraft details | Free | A database of aircraft details |  |
| [Aviation Safety Network](https://aviation-safety.net/) | Aircraft incident database; can be searched by country, registration, year, etc. | Free | Aircraft incident database; can be searched by country, registration, year, etc. |  |
| [Chronotrains](https://www.chronotrains.com/en) | A free interactive map designed to explore the reach of Europe’s extensive rail network. | Free | Chronotrains is a free interactive map designed to explore the reach of Europe’s extensive rail network. Enter a star... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/chronotrains) |
| [Equasis](https://www.equasis.org/) | Vessel ownership and safety records, as well as shipping company fleet information. | Free | Equasis provides vessel ownership and safety records, as well as shipping company fleet information. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/equasis) |
| [Federal Aviation Administration](http://registry.faa.gov/aircraftinquiry/NNum\_inquiry.aspx) | Nationwide Plane Registry. | Free | Nationwide Plane Registry. Search by N-Number (a.k.a. callsign). Comprehensive list of privately owned planes in the US. |  |
| [FlightAware](https://www.flightaware.com/live/) | A global flight-tracking platform that provides real-time data on aircraft movements. | Partially Free | FlightAware is a global flight-tracking platform that provides real-time data on aircraft movements. It offers live t... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/flightaware) |
| [Flightradar24](https://www.flightradar24.com) | , a real-time flight tracking service, that provides comprehensive information about… | Partially Free | Flightradar24, a real-time flight tracking service, that provides comprehensive information about aircraft positions,... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/flightradar24) |
| [Global Fishing Watch](https://globalfishingwatch.org/map) | A digital platform for investigating fishing activities and vessel movements worldwide by… | Free | A digital platform for investigating fishing activities and vessel movements worldwide by utilising satellite and AIS... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/global-fishing-watch-map) |
| [GPSJam](https://gpsjam.org/) | .org is a daily map that visualizes the GPS/GNSS disruptions on aircraft worldwide. | Free | GPSJam.org is a daily map that visualizes the GPS/GNSS disruptions on aircraft worldwide. It collects and presents 24... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/gpsjam) |
| [Illegal, unreported, unregular fishing Vessels List](https://iuu-vessels.org/Home/Search) | A combined list of known illegal, unreported, unregular fishing vessels | Free | A combined list of known illegal, unreported, unregular fishing vessels |  |
| [IMO Registry](http://webaccounts.imo.org/) | Ship/shipping-related information from the IMO | Free | Ship/shipping-related information from the IMO |  |
| [License Plate Maps](https://bellingcat.gitbook.io/toolkit/more/all-tools/license-plate-maps) | Collection of tools and maps for discerning license plates by country | Free | Collection of tools and maps for discerning license plates by country | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/license-plate-maps) |
| [Live ATC](http://liveatc.net/) | Audio from air traffic control towers in the United States. | Free | Audio from air traffic control towers in the United States. Aircraft have to identify themselves to ATC towers, so in... |  |
| [MarineTraffic](https://www.marinetraffic.com/en/ais/home/centerx:25.0/centery:-34.5/zoom:8) | An open, community-based project, providing (near) real-time information on the movements… | Partially Free | An open, community-based project, providing (near) real-time information on the movements of ships and their location... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/marinetraffic) |
| [OpenRailwayMap](https://wiki.openstreetmap.org/wiki/OpenRailwayMap) | A detailed online map of the world's railway infrastructure | Free | a detailed online map of the world's railway infrastructure |  |
| [OpenSky-Network](http://opensky-network.org/) | Community, open source flight tracking network. | Free | Community, open source flight tracking network. |  |
| [ShipFinder](https://shipfinder.co/) | An application designed to track vessels in near real-time across the globe, available on… | Partially Free | ShipFinder is an application designed to track vessels in near real-time across the globe, available on iPhone and An... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/shipfinder) |
| [VesselFinder](https://www.vesselfinder.com/) | Live marine vessel tracker | Partially Free | Live marine vessel tracker | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/vesselfinder) |

## Investigation Tips

- For ships: cross-reference MarineTraffic, VesselFinder, and Equasis for ownership and movement history
- For aircraft: use Flightradar24, FlightAware, and ADS-B Exchange (includes military aircraft)
- Check Global Fishing Watch to identify fishing vessel activity vs regular shipping
- GPSJam shows GPS interference patterns that may indicate electronic warfare activity
- Use Live ATC for air traffic control audio as a supplementary tracking source
- License Plate Maps helps identify vehicle registration plates by country
