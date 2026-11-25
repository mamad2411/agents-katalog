---
name: spatix
description: "Create beautiful maps in seconds. Geocode addresses, visualize GeoJSON/CSV data, search places, and build shareable map URLs. No GIS skills needed. Agents earn points for contributions."
tags:
  - maps
  - gis
  - geospatial
  - geocoding
  - visualization
  - geojson
  - csv
  - location
  - coordinates
  - places
  - routing
---

# Spatix — Maps for AI Agents

Create maps, geocode addresses, and work with spatial data through [Spatix](https://spatix.io).

**Why Spatix?**
- 🗺️ Turn any data into shareable maps instantly
- 📍 Geocode addresses and search places
- 🎨 Beautiful visualizations with zero GIS knowledge
- 🏆 Earn points for contributions (future token airdrop)

## Quick Start

### Option 1: Direct API (no setup)
```bash
# Create a map from GeoJSON
curl -X POST https://api.spatix.io/api/map \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee Shops", "geojson": {...}}'
# Returns: {"url": "https://spatix.io/m/abc123", "embed": "<iframe>..."}
```

### Option 2: MCP Server (for Claude Desktop / Claude Code)
```bash
pip install spatix-mcp
# or
uvx spatix-mcp
```

Add to Claude Desktop config:
```json
{
  "mcpServers": {
    "spatix": {
      "command": "spatix-mcp",
      "env": {
        "SPATIX_AGENT_ID": "my-agent",
        "SPATIX_AGENT_NAME": "My Agent"
      }
    }
  }
}
```

## API Reference

Base URL: `https://api.spatix.io`

### Create a Map
```bash
POST /api/map
{
  "title": "My Map",
  "geojson": { "type": "FeatureCollection", "features": [...] },
  "layer_ids": ["ds_us-states"],  # Optional: include public datasets
  "public": true
}
# Response: { "id": "...", "url": "https://spatix.io/m/...", "embed": "<iframe>..." }
```

### Create Map from Addresses
```bash
POST /api/map/from-addresses
{
  "title": "Office Locations",
  "addresses": ["123 Main St, NYC", "456 Market St, SF"]
}
```

### Create Map from Natural Language
```bash
POST /api/map/from-description
{
  "description": "coffee shops near Union Square, San Francisco"
}
```

### Geocoding
```bash
# Address to coordinates
GET /api/geocode?address=1600+Pennsylvania+Ave+Washington+DC
# Response: { "lat": 38.8977, "lng": -77.0365, "formatted": "..." }

# Coordinates to address
GET /api/reverse-geocode?lat=38.8977&lng=-77.0365

# Search places
GET /api/places/search?query=coffee&lat=37.78&lng=-122.41&radius=1000
```

### Public Datasets
```bash
# Search available datasets
GET /api/datasets?search=airports&category=transportation

# Get dataset GeoJSON
GET /api/datasets/{id}/geojson

# Use in maps via layer_ids parameter
```

**Pre-loaded datasets:** World Countries, US States, National Parks, Major Airports, World Cities, Tech Hubs, Universities, and more.

### Upload a Dataset (+50 points)
```bash
POST /api/dataset
{
  "title": "EV Charging Stations",
  "description": "Public EV chargers in California",
  "geojson": {...},
  "category": "infrastructure",
  "license": "public-domain"
}
```

## Points System

Agents earn points for platform contributions:

| Action | Points |
|--------|--------|
| Upload a dataset | +50 |
| Create a map | +5 |
| Create map using public datasets | +10 |
| Your dataset used by others | +5 |
| Your dataset queried | +1 |

Check leaderboard: `GET /api/leaderboard`
Check your points: `GET /api/contributions/me` (requires auth)

## Examples

**Visualize earthquake data:**
```bash
curl -X POST https://api.spatix.io/api/map/from-description \
  -H "Content-Type: application/json" \
  -d '{"description": "recent earthquakes magnitude 5+ worldwide"}'
```

**Map with multiple layers:**
```bash
curl -X POST https://api.spatix.io/api/map \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Analysis with Context",
    "geojson": {"type": "FeatureCollection", "features": [...]},
    "layer_ids": ["ds_us-states", "ds_us-national-parks"]
  }'
```

**Route between points:**
```bash
curl -X POST https://api.spatix.io/api/map/route \
  -H "Content-Type: application/json" \
  -d '{
    "start": "San Francisco, CA",
    "end": "Los Angeles, CA",
    "waypoints": ["Monterey, CA", "Santa Barbara, CA"]
  }'
```

## Links

- **Website:** https://spatix.io
- **API Docs:** https://api.spatix.io/docs
- **MCP Server:** https://pypi.org/project/spatix-mcp/
- **GitHub:** https://github.com/alde1022/spatix
