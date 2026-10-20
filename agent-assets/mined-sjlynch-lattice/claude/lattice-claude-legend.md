# frontend/src/components/legend

The right-side legend overlay's two modes: the default extension legend (shape +
color per file extension) and the `h`-key code-health breakdown panel. Which one
renders is driven by the App-level `healthMode` prop.

## Files

- `HealthLegendPanel.tsx` — the health legend panel layout shown while `h` is held
- `healthComponents.ts` — assembly logic that maps the backend's serializable
  `backend/src/health/scoreMetadata.ts` (score ids, weights, thresholds,
  ordering — do not duplicate those values here) onto the UI copy, exposing the
  `HealthComponentId` / `DetailEntry` / `HealthComponent` types and the
  assembled `HEALTH_COMPONENTS`.
- `healthComponentCopy.ts` — the static explanatory copy (`HEALTH_COMPONENT_COPY`):
  per-component label, one-line note, and structured tooltip detail. Kept apart
  from the assembly logic above so the large prose block stays isolated.
- `HealthInfoIcon.tsx` — info icon and portal-rendered popover for each health row
- `LegendRow.tsx` — render-only extension row button used by the default legend
- `useLegendRows.ts` — extension tallying plus visible/all-known row derivation
- `ShapePreview.tsx` — small inline-SVG preview of an extension's sprite shape
  (matching the canvas-drawn graph sprites), reused by `LegendRow` and the
  regular Legend's toggle button

Per-extension shapes and colors come from `frontend/src/extensionStyles.ts` —
the single source of truth shared by the 3D graph and this legend. Health score
metadata comes from `backend/src/health/scoreMetadata.ts`; backend `scoreModel.ts`
adds only the metric extractor functions used by scoring.
