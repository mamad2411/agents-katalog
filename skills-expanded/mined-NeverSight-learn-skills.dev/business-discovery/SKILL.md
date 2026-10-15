---
name: business-discovery
description: Discover top businesses matching a specified purpose/service within a given radius of a location, ranked by ratings (max 50 results) using Google Maps API.
---

# Business Discovery Skill

Find top-rated businesses, service providers, or points of interest within a specified geographical radius (in meters) of a location or area using the Google Maps API.

## Key Features

- **Rating-based Ranking**: Returns top businesses ordered by highest average rating and total rating count (max 50 results).
- **Average Rating & Review Counts**: Every result includes `average_rating` (out of 5.0) and `user_ratings_total` (number of ratings).
- **Geocoding & Distance**: Resolves location queries (e.g. `"Paldi, Ahmedabad, Gujarat, India"`) and calculates exact Haversine distance in meters and kilometers.
- **Pagination**: Automatically navigates Google Places API pagination to gather up to 50 top results.

## Environment Requirements

The skill requires a Google Maps API Key with **Geocoding API** and **Places API** enabled.
Set the key in your shell environment or `.env` file:

```bash
export GOOGLE_MAPS_API_KEY="your-google-maps-api-key"
```

## Input Parameters

| Parameter | Required | Description | Default | Example |
| :--- | :---: | :--- | :---: | :--- |
| `area` | Yes | Target locality, city, address, or geographic query | - | `"Paldi, Ahmedabad, Gujarat, India"` |
| `radius` | Yes | Search radius in meters | - | `5000` |
| `purpose` | Yes | Type of business, service, or keyword | - | `"plumbers"` |
| `max_results` | No | Maximum top results to return (capped at 50) | `50` | `50` |
| `sort_by` | No | Ranking criteria (`rating` or `distance`) | `rating` | `rating` |
| `fetch_details` | No | Fetch phone number & website for each place | `false` | `--fetch-details` |
| `json` | No | Return output as structured JSON | `false` | `--json` |
| `output_csv` | No | Generate CSV file stored in current working directory | - | `plumbers_paldi.csv` |
| `output_kml` | No | Generate KML file stored in current working directory | - | `plumbers_paldi.kml` |

## Execution Instructions

Run the python discovery, CSV, or KML exporter tools using `uv` from the repository root:

### Direct KML Export (Live Search saved to Current Working Directory)
```bash
uv run skills/business-discovery/scripts/export_kml.py \
  --area "Paldi, Ahmedabad, Gujarat, India" \
  --radius 5000 \
  --purpose "plumbers" \
  --output "plumbers_paldi.kml"
```

### Convert Existing JSON Discovery Results to KML
```bash
uv run skills/business-discovery/scripts/export_kml.py \
  --input-json "results.json" \
  --output "plumbers.kml"
```

### Direct CSV Export (Live Search saved to Current Working Directory)
```bash
uv run skills/business-discovery/scripts/export_csv.py \
  --area "Paldi, Ahmedabad, Gujarat, India" \
  --radius 5000 \
  --purpose "plumbers" \
  --output "plumbers_paldi.csv"
```

### Convert Existing JSON Discovery Results to CSV
```bash
uv run skills/business-discovery/scripts/export_csv.py \
  --input-json "results.json" \
  --output "plumbers.csv"
```

### Standard Execution (Top 50 rated businesses, JSON output for AI parsing)
```bash
uv run skills/business-discovery/scripts/discover.py \
  --area "Paldi, Ahmedabad, Gujarat, India" \
  --radius 5000 \
  --purpose "plumbers" \
  --max-results 50 \
  --sort-by rating \
  --json
```

### Discovery Execution with CSV Export
```bash
uv run skills/business-discovery/scripts/discover.py \
  --area "Paldi, Ahmedabad, Gujarat, India" \
  --radius 5000 \
  --purpose "plumbers" \
  --fetch-details \
  --output-csv "plumbers_detailed.csv"
```

### Formatted Terminal Output (Human readable table)
```bash
uv run skills/business-discovery/scripts/discover.py \
  --area "Paldi, Ahmedabad, Gujarat, India" \
  --radius 5000 \
  --purpose "plumbers"
```

## Interpreting Output

When `--json` is provided, the script returns a structured JSON payload with average rating and total ratings:

```json
{
  "origin": {
    "query_address": "Paldi, Ahmedabad, Gujarat, India",
    "formatted_address": "Paldi, Ahmedabad, Gujarat 380007, India",
    "coordinates": {
      "latitude": 23.0120,
      "longitude": 72.5630
    }
  },
  "radius_meters": 5000,
  "purpose": "plumbers",
  "total_found": 50,
  "businesses": [
    {
      "place_id": "ChIJ...",
      "name": "Top Plumber Ahmedabad",
      "address": "Paldi Cross Rd, Ahmedabad",
      "coordinates": {
        "latitude": 23.0132,
        "longitude": 72.5641
      },
      "distance_meters": 178.5,
      "average_rating": 4.9,
      "rating": 4.9,
      "user_ratings_total": 128,
      "total_ratings": 128,
      "business_status": "OPERATIONAL",
      "phone_number": "+91 98765 43210",
      "website": "https://example.com",
      "google_maps_url": "https://www.google.com/maps/place/?q=place_id:ChIJ...",
      "types": ["plumber", "point_of_interest"]
    }
  ]
}
```

## Error Handling

If an error occurs, the script exits with non-zero code and returns a helpful error payload:
- **`ConfigurationError`**: `GOOGLE_MAPS_API_KEY` missing. Remind the user to export the key.
- **`GeocodingError`**: Location string could not be resolved. Ask user for a clearer address.
- **`PlacesSearchError`**: Google Maps Places API request failed or quota exceeded.
