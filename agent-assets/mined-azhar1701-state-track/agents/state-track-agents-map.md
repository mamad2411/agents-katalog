# Map Module Knowledge Base

## OVERVIEW
The Map module is the core of SIPASDA, handling high-density geospatial rendering and Enterprise-Grade routing.

## STRUCTURE
```text
src/features/map/
├── MapView.tsx             # Main entry point (Large file)
├── routeOptimization.ts    # OSRM pathfinding logic
├── BasemapSwitcher.tsx     # Tile layer management & Offline caching
├── RouteOptimizationPanel.tsx # Technical navigation UI
├── ModernMapOverlay.tsx    # Desktop floating UI
└── MobileMapControls.tsx   # Mobile-optimized Command Hub
```

## CORE LOGIC
- **OSRM Routing**: Dynamic fetch from `router.project-osrm.org`.
- **Offline Caching**: Toggle-able map tile persistence for field operations.
- **Markers**: Use `createCustomIcon` for status-based visual indicators.

## CONVENTIONS
- **Layers**: GeoJSON layers must be sanitized before rendering.
- **Elevation**: Use `glass-overlay` for detail drawers to ensure visual immersion.

## ANTI-PATTERNS
- **Prop Drilling**: Use specialized hooks (like `useLayerHighlight`).
- **Heavy Re-renders**: Memoize `renderedLayers` and `legendOverlays`.
- **Leaflet Defaults**: Never use unstyled gray buttons; use Liquid Glass components.

## WHERE TO LOOK
| Feature | File |
|---------|------|
| Routing API | `MapView.tsx` -> `fetchRoute` |
| Route UI | `ReportDetailView.tsx` -> `onRoute` |
| URL Logic | `mapExport.ts` |


## WHERE TO LOOK
| Feature | File |
|---------|------|
| Report Markers | `MapView.tsx` -> `createCustomIcon` |
| Real-time Sync | `MapView.tsx` -> `useEffect` (reports-changes) |
| URL Parsing | `mapExport.ts` |
