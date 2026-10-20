# GEODATA DOMAIN

**Generated:** 2026-03-03
**Domain:** Geospatial Data Management & Layer Orchestration

## OVERVIEW
Advanced management of geospatial layers including multi-format ingestion (GeoJSON, SHP, CSV), attribute inspection, and dynamic symbology configuration.

## WHERE TO LOOK
| Component | Responsibility | Key Logic |
|-----------|----------------|-----------|
| `GeoDataManager.tsx` | Main dashboard for admins | Layer CRUD, batch export, validation loops |
| `LayerUploader.tsx` | Data ingestion engine | `shpjs` parsing, CRS selection (EPSG:4326/3857/32749) |
| `LayerInspector.tsx` | Deep-dive configuration | Metadata editing, dynamic symbology (Point/Line/Poly) |
| `LayerAttributeTable.tsx` | Tabular data explorer | Virtualized attribute filtering, pagination |

## CONVENTIONS
- **CRS Handling**: Default to `EPSG:4326`. Always provide selection for UTM zones if applicable.
- **Validation**: Geometry validation (ring closure, min coordinates) must run before persistence.
- **Caching**: Use `dataCache` (Ref-based) in inspectors to prevent redundant Supabase fetches for large GeoJSON blobs.
- **Persistence**: Layer data is stored in `geo_layers` table with a unified `data` JSONB column containing `featureCollection`, `meta`, and `style`.

## ANTI-PATTERNS
- **Direct State Blobs**: Never store raw `FeatureCollection` in global state; keep it local to the inspector or uploader.
- **Sync Validation**: Avoid running heavy geometry validation on the main thread for >1000 features; use the 300ms debounced effect.
- **Hardcoded Styles**: Do not hardcode Leaflet path options; always derive from the `style` property in the layer's JSONB data.
