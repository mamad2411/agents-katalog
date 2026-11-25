---
name: terra-routes
description: Push GPS routes to users' fitness devices with Terra API Routes (pre-release). Use when creating GPS courses or navigation routes, defining waypoints and course points, pushing a route to Garmin, COROS, or Wahoo devices, handling GPX or FIT route formats, or building turn-by-turn navigation onto wearables. Covers the create-then-push workflow, the RouteTemplate and Waypoint data model, per-provider wire formats and feature gaps, cascade re-pushes, and route deletion.
license: MIT
compatibility: Requires network access to docs.tryterra.co for full payload examples
metadata:
  author: terra
  version: "1.0.0"
---

# Terra API Routes

Terra API Routes is a write-to-device product (pre-release): define a GPS route once with waypoints, and Terra API pushes it to your users' connected devices for on-device navigation. The route appears on the watch or bike computer after the user's next device sync, so your app never has to speak each provider's native route format.

Only Garmin, COROS, and Wahoo are supported. Feature coverage differs sharply between them (see the provider matrix below), so design routes for the lowest common denominator unless you know every user is on Garmin.

## Two-Phase Workflow

Routes always take two steps: create a reusable template, then push that template to one or more users.

```
Phase 1  POST /routes                          -> route_id           (create template once)
Phase 2  POST /routes/{route_id}/push?user_id=X -> pushed_route_id    (push to a user's device)
                                                    provider_route_id
```

The route reaches the device on the user's next sync. Base URL is `https://access.tryterra.co/api/v2`. Every request needs two headers: `dev-id` and `x-api-key`.

```bash
curl -X POST "https://access.tryterra.co/api/v2/routes" \
  -H "Content-Type: application/json" \
  -H "dev-id: YOUR_DEV_ID" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "name": "Morning Run Loop",
    "sport": "running",
    "waypoints": [
      { "latitude": 51.5074, "longitude": -0.1278 },
      { "latitude": 51.5150, "longitude": -0.1200 }
    ]
  }'
# -> { "status": "success", "route_id": "295581149349019648" }

curl -X POST "https://access.tryterra.co/api/v2/routes/295581149349019648/push?user_id=USER_ID" \
  -H "dev-id: YOUR_DEV_ID" \
  -H "x-api-key: YOUR_API_KEY"
# -> { "status": "success", "pushed_route_id": "...", "provider_route_id": "..." }
```

## Endpoints

| Method   | Endpoint                       | Description                                    |
| -------- | ------------------------------ | ---------------------------------------------- |
| `POST`   | `/routes`                      | Create a route template                        |
| `GET`    | `/routes`                      | List all templates                             |
| `GET`    | `/routes/{id}`                 | Get one template                               |
| `PUT`    | `/routes/{id}`                 | Update a template, partial update (200)        |
| `PUT`    | `/routes/{id}?cascade`         | Update and re-push to all devices, async (202) |
| `DELETE` | `/routes/{id}`                 | Delete a template                              |
| `POST`   | `/routes/{id}/push?user_id=X`  | Push route to a user's device                  |
| `GET`    | `/pushedRoutes?user_id=X`      | List a user's pushed routes                    |
| `GET`    | `/pushedRoutes/{id}?user_id=X` | Get one pushed route                           |
| `DELETE` | `/pushedRoutes/{id}?user_id=X` | Remove a pushed route                          |

**Update semantics.** `PUT /routes/{id}` behaves like a patch and returns `200`: every field is optional and only the fields you provide are updated (waypoints, `speed_meters_per_second`, and elevation as well as name, description, and sport). It does not touch already-pushed devices. Add `?cascade` to also re-push the updated route to every device it was sent to; this runs asynchronously and returns `202 Accepted`. Cascade is fire-and-forget: re-push failures are only logged server-side, never surfaced in the response or in `GET /pushedRoutes`, so a partial failure is invisible to the API. To confirm a device actually received the update, re-push to that user explicitly or verify out of band on the device.

## Data Model

**RouteTemplate**

| Field                     | Required | Notes                                    |
| ------------------------- | -------- | ---------------------------------------- |
| `name`                    | Yes      | Route name shown on device, non-empty    |
| `sport`                   | Yes      | One of the sport types below             |
| `waypoints`               | Yes      | Array of GPS points, minimum 2           |
| `description`             | No       | Garmin only                              |
| `elevation_gain_meters`   | No       | Total gain in meters                     |
| `elevation_loss_meters`   | No       | Total loss in meters                     |
| `speed_meters_per_second` | No       | Average course speed target, Garmin only |

**Waypoint**

| Field              | Required | Notes                                    |
| ------------------ | -------- | ---------------------------------------- |
| `latitude`         | Yes      | Decimal degrees, -90 to 90               |
| `longitude`        | Yes      | Decimal degrees, -180 to 180             |
| `elevation_meters` | No       | Metres above sea level                   |
| `course_point`     | No       | POI marker at this waypoint, Garmin only |

**course_point** is `{ "type": ..., "name": ... }`. The API schema contains 15 types: `generic`, `summit`, `valley`, `water`, `food`, `danger`, `first_aid`, `sprint`, `segment_start`, `segment_end`, `left`, `right`, `straight`, `left_fork`, `right_fork`. Garmin support is documented for the first 10 (the POI types) only; do not rely on the five turn-direction types unless verified against current provider behavior (see Gotchas).

**Sports** (8): `running`, `trail_running`, `hiking`, `cycling`, `road_biking`, `mountain_biking`, `gravel_cycling`, `other`. `cycling` is distinct from `road_biking` but maps to ROAD_CYCLING on Garmin.

**Validation** (hard `400` on create and update): `name` non-empty, max 255 chars; `description` max 2,000 chars; `sport` valid; 2 to 10,000 waypoints; latitude in -90..90; longitude in -180..180; `elevation_meters` in -500..9000; `speed_meters_per_second` > 0.

## Provider Matrix

| Capability           | Garmin | COROS                 | Wahoo      |
| -------------------- | ------ | --------------------- | ---------- |
| Wire format          | JSON   | GPX                   | base64 FIT |
| Push                 | Yes    | Yes                   | Yes        |
| Re-sync              | Yes    | Yes (re-POST new GPX) | Yes        |
| Delete               | Yes    | No                    | Yes        |
| Course points (POIs) | Yes    | No                    | No         |
| Speed target         | Yes    | No                    | No         |
| Description          | Yes    | No                    | No         |

All three support re-sync. COROS has no in-place update, so a re-sync re-POSTs a fresh GPX file while the `provider_route_id` stays stable. Delete works on Garmin and Wahoo only.

## Gotchas

- **Garmin-only fields fail silently elsewhere.** `course_point`, `speed_meters_per_second`, and `description` are honored on Garmin but silently ignored by COROS and Wahoo. Do not depend on them unless every target user is on Garmin.
- **Garmin elevation is all-or-nothing per route.** If some waypoints carry `elevation_meters` and others do not, Terra API drops all elevation values and lets Garmin's own elevation model fill them in. Supply elevation on every waypoint or none.
- **Course-point failures happen at different stages.** An invalid `type` string fails at `POST /routes` with `400` (creation-time enum validation). The five turn-direction types (`left`, `right`, `straight`, `left_fork`, `right_fork`) pass creation-time validation but are not among the 10 documented Garmin course-point types – how the push handles them is not guaranteed (it may error or drop them), so stick to the 10 Garmin-supported POI types unless you have verified current behavior.
- **COROS is the most limited provider.** No delete (a delete only removes the record from Terra API's database; the route stays on the device), no retrieve, and it collapses all sports into two internal types (run and cycle), so the device display may not distinguish, say, gravel cycling from road biking.
- **Pushing the same template repeatedly creates duplicate pushed routes.** Each push is a new pushed route; there is no dedup. Track `pushed_route_id` values yourself if you need to avoid duplicates on a device.
- **Elevation is auto-computed when absent**, and the exact handling is provider-dependent.
- **Unsupported operations still return success.** A delete against COROS, for example, returns a success response even though the route remains on the device.

## References

- `references/provider-details.md` – per-provider behavior: Garmin PUT-then-POST re-sync and elevation normalization, Wahoo stable `terra-{pushed_route_id}` external ID and granular sport mapping, COROS unique-GPX-per-push and `provider_route_id` meaning. Read when a route behaves differently across devices or you are debugging a re-sync or delete.

For full payload examples beyond the one above (trail running with course points, road biking with a speed target, the minimal 2-waypoint route), fetch the live page: https://docs.tryterra.co/routes-api-pre-release/sport-specific-examples.md

Full docs: [Routes API overview](https://docs.tryterra.co/routes-api-pre-release/overview), [introduction](https://docs.tryterra.co/routes-api-pre-release/introduction), [core concepts](https://docs.tryterra.co/routes-api-pre-release/core-concepts), [provider compatibility](https://docs.tryterra.co/routes-api-pre-release/provider-compatibility). If the terra-docs MCP server (`https://docs.tryterra.co/~gitbook/mcp`) is connected, use its tools to search and fetch the docs instead.

Note: the Routes docs space is pre-release and may not be published yet. If a page above returns "Page Not Found", rely on this skill's bundled references and verify against the live API.
