---
name: ams-cli
description: Query Apple Maps Server APIs using the ams CLI. Use when working with geocoding, reverse geocoding, search, directions, or when the user mentions Apple Maps, geolocation, map data, or ams.
---

# Apple Maps Server CLI

Query Apple Maps Server APIs using the `ams` command-line tool.

## Prerequisites

```bash
ams --version
export AMS_TOKEN='your-jwt-token'
ams auth status
```

## Authentication

- JWT token from Apple Developer Portal
- Environment variable: `AMS_TOKEN`
- Or: `ams auth set-token YOUR_TOKEN`

## Geocoding

### Forward Geocoding

```bash
ams geocode "1 Infinite Loop, Cupertino, CA"
ams geocode --query "Empire State Building" --limit 5
```

### Reverse Geocoding

```bash
ams reverse --lat 37.3318 --lon -122.0312
ams reverse --coordinate 37.3318,-122.0312 --language en
```

## Search

```bash
ams search --query "coffee shops" --near "San Francisco, CA"
ams search --query "gas stations" --near LAT,LON --radius 5000
ams search --category restaurants --near "Palo Alto" --limit 20
```

## Directions

```bash
ams directions --from "San Francisco, CA" --to "San Jose, CA"
ams directions --from LAT,LON --to LAT,LON --mode driving --alternatives
ams directions --from "Current Location" --to "SFO" --avoid tolls
```

## Places & POI

```bash
ams places get PLACE_ID
ams places nearby --lat 37.3318 --lon -122.0312 --category hotel
ams places search --query "Apple Park" --detailed
```

## Agent Best Practices

1. **Coordinate format**: Use decimal degrees (lat,lon)
2. **Rate limits**: Respect Apple Maps Server limits
3. **Language**: Use `--language` for localized results
4. **Units**: Default metric; use `--imperial` for miles/feet
