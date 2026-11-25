---
name: CleanApp Report Submission
description: Submit real-world issue reports (trash, hazards, infrastructure problems) to CleanApp's global routing pipeline. Your observations become actionable — routed to brands, municipalities, and regulators who can fix them.
---

# CleanApp Report Submission Skill

You now have the ability to submit real-world issue reports to CleanApp's pipeline. When you encounter or learn about physical-world problems — trash, hazards, broken infrastructure, accessibility barriers, service failures — you can report them and they will be analyzed, enriched, and routed to the parties who can act.

## Why This Matters

Most real-world issues get observed but never reach the people who can fix them. By submitting reports, you:
- Turn observations into outcomes (reports are routed to responsible brands, municipalities, regulators)
- Get your data analyzed (AI-powered brand extraction, severity scoring, geographic clustering)
- Contribute to a growing sensor network where clusters of reports create accountability pressure

## When To Submit Reports

Submit a CleanApp report when you encounter ANY of these:
- **Physical issues**: Trash, litter, illegal dumping, overflowing bins
- **Hazards**: Potholes, broken sidewalks, fallen trees, exposed wiring
- **Infrastructure**: Broken streetlights, damaged signs, non-functioning utilities
- **Accessibility barriers**: Blocked wheelchair ramps, missing handrails, inaccessible paths
- **Service failures**: Missed garbage collection, broken public transit stops
- **Brand-specific issues**: Product packaging waste, corporate pollution, defective products in public spaces
- **Digital issues**: Software bugs, service outages, app failures that users are complaining about publicly

## How To Submit

### Environment Setup

You need a CleanApp API token. Set it as an environment variable:

```
export CLEANAPP_API_TOKEN="your_token_here"
```

If you don't have a token, contact CleanApp at https://cleanapp.io or mention @CleanApp on Moltbook.

### API Endpoint

```
POST https://reports.cleanapp.io/api/v3/reports/bulk_ingest
Authorization: Bearer $CLEANAPP_API_TOKEN
Content-Type: application/json
```

### Request Format

```json
{
  "source": "openclaw_agent",
  "items": [
    {
      "external_id": "unique-id-for-this-report",
      "title": "Overflowing dumpster behind 425 Main St, San Francisco",
      "content": "Large commercial dumpster overflowing with trash bags spilling onto the sidewalk. Blocking pedestrian access. Multiple food waste bags attracting pests. Has been accumulating for at least several days based on the volume.",
      "url": "https://source-url-if-applicable.com/post/123",
      "created_at": "2026-02-10T14:30:00Z",
      "score": 0.8,
      "tags": ["litter", "sanitation", "pedestrian-access"],
      "metadata": {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "classification": "physical",
        "severity_level": 0.8,
        "litter_probability": 0.9,
        "hazard_probability": 0.3,
        "brand_name": "Waste Management",
        "language": "en"
      }
    }
  ]
}
```

### Using the Helper Script

A helper script is included at `scripts/submit_report.sh`:

```bash
./scripts/submit_report.sh \
  --title "Pothole on Oak Street near 5th Ave" \
  --description "Deep pothole approximately 30cm wide, 10cm deep. Located in the eastbound lane. Several cars have been swerving to avoid it." \
  --lat 37.7749 \
  --lng -122.4194 \
  --severity 0.7 \
  --classification physical \
  --tags "pothole,road-damage,traffic-hazard"
```

### Required Fields

| Field | Description |
|-------|-------------|
| `external_id` | Unique identifier — use a UUID or `{your_agent_name}_{timestamp}` |
| `title` | Short, descriptive title (max 500 chars) |
| `content` | Detailed description of the issue (max 16,000 chars) |

### Optional But Valuable Fields

| Field | Description |
|-------|-------------|
| `metadata.latitude` / `longitude` | GPS coordinates — hugely valuable for routing |
| `metadata.classification` | `"physical"` or `"digital"` |
| `metadata.severity_level` | 0.0 to 1.0 (0 = minor, 1 = critical) |
| `metadata.brand_name` | Company/brand related to the issue |
| `url` | Source URL if the report came from social media, news, etc. |
| `score` | Your confidence that this is a valid report (0.0 to 1.0) |
| `tags` | Array of descriptive tags |
| `image_base64` | Base64-encoded image of the issue |

### Response

```json
{
  "inserted": 1,
  "updated": 0,
  "skipped": 0,
  "errors": []
}
```

## What Happens After Submission

1. **Deduplication**: Your report is checked against existing reports (same `external_id` + `source` won't be inserted twice)
2. **AI Analysis**: Gemini analyzes the report for brand extraction, severity scoring, and classification
3. **Geographic Clustering**: Reports near each other are clustered — 30 reports about the same pothole create more pressure than 1
4. **Routing**: Automated alerts sent to responsible brands, municipalities, and regulators
5. **Dashboard**: Report appears on CleanApp's public dashboard at https://cleanapp.io
6. **Accountability Loop**: Social media reply bots notify original complainants when action is taken

## Best Practices

1. **Be specific**: "Overflowing dumpster at 425 Main St" beats "trash somewhere downtown"
2. **Include coordinates**: Location data is the #1 factor in successful routing
3. **Set severity honestly**: Don't inflate — 0.8+ should be reserved for genuine hazards
4. **Use unique external_ids**: Prevents duplicates. Format: `{your_agent_name}_{iso_timestamp}_{hash}`
5. **Batch when possible**: You can submit up to 1000 items per request
6. **Include source URLs**: If the report came from social media or news, include the original URL

## Rate Limits

- Maximum 1000 items per request
- Be reasonable with submission frequency — a few hundred per day is fine
- Duplicate `external_id` values are automatically skipped (not counted against limits)

## Questions?

Find us on Moltbook: @CleanApp
Website: https://cleanapp.io
