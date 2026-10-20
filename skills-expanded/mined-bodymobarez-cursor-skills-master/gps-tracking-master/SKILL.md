---
name: gps-tracking-master
description: >-
  Master hub for professional GPS/GNSS & location tracking of every kind, integrated and easy to use.
  Use for GNSS fundamentals (GPS/GLONASS/Galileo/BeiDou, A-GPS, NMEA, WGS84), centimeter RTK/DGPS/PPP
  precision (NTRIP), hardware tracker integration & protocols (Teltonika Codec, Concox GT06, JT/T 808,
  u-blox, LTE-M/NB-IoT, MQTT/TCP), browser + mobile geolocation (Expo Location, FusedLocation/CoreLocation,
  background tracking), geofencing (enter/exit/dwell), fleet/asset telematics platforms, and PostGIS
  geospatial storage/queries. Bundles 7 specialized skills (in skills/<name>/GUIDE.md).
---

# GPS & Tracking — Master Hub (all GNSS, integrated)

Work with **every** GPS/location technology like a senior geolocation/telematics engineer: from the
browser to centimeter-grade RTK to LTE-M IoT trackers — ingested, stored, geofenced, and mapped.

## How to use this hub

1. Start with **gps-gnss-fundamentals** (how positioning works, accuracy, NMEA, datums).
2. Pick the integration path: web/mobile, hardware trackers, or RTK precision.
3. Add geofencing, the fleet/asset platform, and PostGIS storage as needed.
4. For map UI + routing use **`ride-hailing-maps-master`**; for basic GIS, `backend-api-master`.

## Bundled skills

- **gps-gnss-fundamentals** ⭐ — GNSS constellations, trilateration, accuracy factors (multipath, DOP),
  A-GPS, NMEA 0183 parsing, WGS84/datums/coordinate systems, accuracy tiers.  
  → `skills/gps-gnss-fundamentals/GUIDE.md`
- **web-mobile-geolocation** ⭐ — Browser Geolocation API (`watchPosition`), Expo Location, Android
  FusedLocation / iOS CoreLocation, background tracking, permissions, accuracy vs battery.  
  → `skills/web-mobile-geolocation/GUIDE.md`
- **device-integration-protocols** ⭐ — Hardware trackers & protocols: Teltonika Codec 8, Concox/GT06,
  JT/T 808, u-blox, serial/NMEA, cellular (LTE-M/NB-IoT), TCP/MQTT ingestion server.  
  → `skills/device-integration-protocols/GUIDE.md`
- **precision-positioning-rtk** — Centimeter accuracy: RTK / DGPS / PPP, base & rover, NTRIP caster,
  correction services, surveying/drone/agriculture use.  
  → `skills/precision-positioning-rtk/GUIDE.md`
- **geofencing-events** ⭐ — Circular/polygon geofences, enter/exit/dwell, device-side vs server-side,
  PostGIS `ST_Contains`/`ST_DWithin`, debouncing, alerting.  
  → `skills/geofencing-events/GUIDE.md`
- **fleet-asset-tracking-platform** ⭐ — Telematics platform: ingestion pipeline, trip detection,
  route history, speeding/idle/geofence events, live map, dashboards, scale.  
  → `skills/fleet-asset-tracking-platform/GUIDE.md`
- **geospatial-data-postgis** — PostGIS storage, GiST/SP-GiST indexes, nearest/within/distance queries,
  trajectory + time-series location storage, performance & retention.  
  → `skills/geospatial-data-postgis/GUIDE.md`

## Pairs well with

`ride-hailing-maps-master` (maps rendering, routing, live dispatch), `backend-api-master` (gps-integration,
gis-maps), `systems-platforms-master` (Postgres/Neon, queues), `integrations-master` (device webhooks/MQTT).

## Note

Bundled skills use `GUIDE.md` so only this master appears in Cursor's skills list.
